__all__ = ('Movie',)

from math import floor

from .bitmap import Bitmap
from .bitmap_clip import BitmapClip
from .bitmap_ex import BitmapEx
from .button import Button
from .container import LWFContainer
from .graphic import Graphic
from .iobject import IObject
from .movie_event_handlers import MovieEventHandlers
from .particle import Particle
from .program_object import ProgramObject
from .property import Property
from .text import Text
from ..format import Constant, Control as ControlType, MovieClipEvent as ClipEvent, Object as ObjectType
from ..tools import Utility
from ..type import Bounds, ColorTransform, Matrix, Point


class LabelData:
    def __init__(self):
        self.frame = 0
        self.name = None

    def __cmp__(self, other):
        return self.frame < other.frame


class Movie(IObject):
    def __init__(self, l, p, obj_id, inst_id, m_id=0, c_id=0, attached=False, handler=None, n=""):
        super().__init__(l, p, ObjectType.ATTACHED_MOVIE if attached else ObjectType.MOVIE, obj_id, inst_id)

        self.matrix_id = m_id
        self.color_transform_id = c_id

        if len(n) != 0:
            self.name = n

        self.data = self.lwf.data.movies[obj_id]
        self.attach_name = None

        self.total_frames = self.data.frames
        self.current_frame = 0
        self.depth = 0
        self.blend_mode = Constant.BLEND_MODE_NORMAL

        self.visible = True
        self.playing = True
        self.active = True
        self.has_button = False

        self._property = Property(self.lwf)
        self._instance_head = None
        self._instance_tail = None
        self._display_list = [None for _ in range(self.data.depths)]
        self._event_handlers = {}
        self._handler = MovieEventHandlers()
        self._attached_movies = {}
        self._attached_movie_list = {}
        self._detached_movies = {}
        self._attached_LWFs = {}
        self._attached_LWF_list = {}
        self._detached_LWFs = {}
        self._bitmap_clips = {}
        self._calculate_bounds_callbacks = []
        self._texts = {}

        self._current_frame_internal = -1
        self._current_frame_current = -1
        self._execed_frame = -1
        self._animation_played_frame = -1
        self._last_control_offset = -1
        self._last_controls = -1
        self._last_control_animation_offset = -1
        self._movie_exec_count = -1
        self._post_exec_count = -1

        self._jumped = False
        self._overriding = False
        self._post_loaded = False
        self._last_has_button = False
        self._skipped = False
        self._attach_movie_execed = False
        self._attach_move_post_execed = False
        self._is_root = obj_id == self.lwf.data.header.root_movie_id
        self._needs_update_attached_LWFs = False
        self._requested_calculate_bounds = False

        self._matrix_0 = Matrix()
        self._matrix_1 = Matrix()
        self._matrix_for_attached_LWFs = Matrix()
        self._color_transform_0 = ColorTransform()
        self._color_transform_1 = ColorTransform()
        self._color_transform_for_attached_LWFs = ColorTransform()
        self._bounds = Bounds()
        self._current_bounds = Bounds()
        self._current_labels_cache = []
        self._current_label_cache = {}
        self._current_labels_cached = False

        self._play_animation(ClipEvent.LOAD)

        self._handler.add(self.lwf.get_movie_event_handlers(self))
        self._handler.add(handler)
        if not self._handler.empty():
            self._handler.call(MovieEventHandlers.LOAD, self)

        self.lwf.exec_movie_command()

    def add_handlers(self, handlers):
        self._handler.add(handlers)

    def global_to_local(self, point):
        invert = Matrix()
        Utility.invert_matrix(invert, self.matrix)
        px, py = Utility.calc_matrix_to_point(point.x, point.y, invert)
        return Point(px, py)

    def local_to_global(self, point):
        px, py = Utility.calc_matrix_to_point(point.x, point.y, self.matrix)
        return Point(px, py)

    def _exec_object(self, dl_depth, obj_id, matrix_id, color_transform_id, inst_id, dl_blend_mode, update_blend_mode=False):
        if obj_id == -1:
            return
        data = self.lwf.data
        data_object = data.objects[obj_id]
        data_object_id = data_object.object_id
        obj = self._display_list[dl_depth]

        if obj and (obj.type != data_object.object_type or obj.object_id != data_object_id or (obj.is_movie() and obj.instance_id != inst_id)):
            if self._texts and obj.is_text():
                self.erase_text(obj.object_id)
            obj.destroy()
            obj = None

        if not obj:
            if data_object.object_type == ObjectType.BUTTON:
                obj = Button(self.lwf, self, data_object_id, inst_id, matrix_id, color_transform_id)
            elif data_object.object_type == ObjectType.GRAPHIC:
                obj = Graphic(self.lwf, self, data_object_id)
            elif data_object.object_type == ObjectType.MOVIE:
                obj = Movie(self.lwf, self, data_object_id, inst_id, matrix_id, color_transform_id)
                obj.blend_mode = dl_blend_mode
            elif data_object.object_type == ObjectType.BITMAP:
                obj = Bitmap(self.lwf, self, data_object_id)
            elif data_object.object_type == ObjectType.BITMAP_EX:
                obj = BitmapEx(self.lwf, self, data_object_id)
            elif data_object.object_type == ObjectType.TEXT:
                obj = Text(self.lwf, self, data_object_id, inst_id)
            elif data_object.object_type == ObjectType.PARTICLE:
                obj = Particle(self.lwf, self, data_object_id)
            else:
                obj = ProgramObject(self.lwf, self, data_object_id)

        if obj.is_movie() and update_blend_mode:
            obj.blend_mode = dl_blend_mode

        if obj.is_movie() or obj.is_button():
            obj.link_instance = None
            if not self._instance_head:
                self._instance_head = obj
            else:
                self._instance_tail.link_instance = obj
            self._instance_tail = obj
            if obj.is_button():
                self.has_button = True

        if self._texts and obj.is_text():
            self.insert_text(obj.object_id)

        self._display_list[dl_depth] = obj
        obj.exec_count = self._movie_exec_count
        obj.exec(matrix_id, color_transform_id)

    def override(self, overriding):
        self._overriding = overriding

    def exec(self, matrix_id=0, color_transform_id=0):
        self._attach_movie_execed = False
        self._attach_move_post_execed = False
        super().exec(matrix_id, color_transform_id)

    def post_exec(self, progressing):
        self.has_button = False
        if not self.active:
            return

        self._execed_frame = -1
        post_execed = self._post_exec_count == self.lwf.exec_count
        if progressing and self.playing and not self._jumped and not post_execed:
            self._current_frame_internal += 1
            self.current_frame = self._current_frame_internal + 1

        while True:
            if self._current_frame_internal < 0 or self._current_frame_internal >= self.total_frames:
                self._current_frame_internal = 0
                self.current_frame = self._current_frame_internal + 1
            if self._current_frame_internal == self._execed_frame:
                break

            self._current_frame_current = self._current_frame_internal
            self._execed_frame = self._current_frame_current
            d = self.lwf.data
            frame = d.frames[self.data.frame_offset + self._current_frame_current]

            if self._last_control_offset == frame.control_offset and self._last_controls == frame.controls:
                control_animation_offset = self._last_control_animation_offset
                if self._skipped:
                    instance = self._instance_head
                    while instance:
                        if instance.is_movie():
                            instance._attach_movie_execed = False
                            instance._attach_movie_post_execed = False
                        elif instance.is_button():
                            instance.enter_frame()
                        instance = instance.link_instance
                    self.has_button = self._last_has_button
                else:
                    for dl_depth in range(self.data.depths):
                        obj = self._display_list[dl_depth]
                        if obj:
                            if not post_execed:
                                obj.matrix_id_changed = False
                                obj.color_transform_id_changed = False
                            if obj.is_movie():
                                obj._attach_movie_execed = False
                                obj._attach_movie_post_execed = False
                            elif obj.is_button():
                                obj.enter_frame()
                                self.has_button = True
                    self._last_has_button = self.has_button
                    self._skipped = True
            else:
                self._movie_exec_count += 1
                self._instance_head = None
                self._instance_tail = None
                self._last_control_offset = frame.control_offset
                self._last_controls = frame.controls
                control_animation_offset = -1
                for i in range(frame.controls):
                    control = d.controls[frame.control_offset + i]

                    if control.control_type == ControlType.MOVE:
                        p = d.places[control.control_id]
                        self._exec_object(p.depth, p.object_id, p.matrix_id, 0, p.instance_id, p.blend_mode)
                    elif control.control_type == ControlType.MOVE_M:
                        ctrl = d.control_move_ms[control.control_id]
                        p = d.places[ctrl.place_id]
                        self._exec_object(p.depth, p.object_id, ctrl.matrix_id, 0, p.instance_id, p.blend_mode)
                    elif control.control_type == ControlType.MOVE_C:
                        ctrl = d.control_move_cs[control.control_id]
                        p = d.places[ctrl.place_id]
                        self._exec_object(p.depth, p.object_id, p.matrix_id, ctrl.color_transform_id, p.instance_id, p.blend_mode)
                    elif control.control_type == ControlType.MOVE_MC:
                        ctrl = d.control_move_mcs[control.control_id]
                        p = d.places[ctrl.place_id]
                        self._exec_object(p.depth, p.object_id, ctrl.matrix_id, ctrl.color_transform_id, p.instance_id, p.blend_mode)
                    elif control.control_type == ControlType.MOVE_MCB:
                        ctrl = d.control_move_mcs[control.control_id]
                        p = d.places[ctrl.place_id]
                        self._exec_object(p.depth, p.object_id, ctrl.matrix_id, ctrl.color_transform_id, p.instance_id, ctrl.blend_mode)
                    elif control.control_type == ControlType.ANIMATION:
                        if control_animation_offset == -1:
                            control_animation_offset = i
                self._last_control_animation_offset = control_animation_offset
                self._last_has_button = self.has_button

                for dl_depth in range(self.data.depths):
                    obj = self._display_list[dl_depth]
                    if obj and obj.exec_count != self._movie_exec_count:
                        if self._texts and obj.is_text():
                            self.erase_text(obj.object_id)
                        obj.destroy()
                        self._display_list[dl_depth] = None

            self._attach_movie_execed = True
            if len(self._attached_movies) != 0:
                for index, movie in self._attached_movie_list:
                    movie.exec()

            instance = self._instance_head
            while instance:
                if instance.is_movie():
                    instance.post_exec(progressing)
                    if not self.has_button and instance.has_button:
                        self.has_button = True
                instance = instance.link_instance

            self._attach_move_post_execed = True
            if len(self._attached_movies) != 0:
                for attach_name, v in self._detached_movies:
                    if attach_name in self._attached_movies:
                        self.delete_attached_movie(self, self._attached_movies[attach_name], True, False)
                self._detached_movies.clear()

                for movie in self._attached_movie_list.values():
                    movie.post_exec(progressing)
                    if not self.has_button and movie.has_button:
                        self.has_button = True

            if len(self._attached_LWFs) != 0:
                self.has_button = True

            if not self._post_loaded:
                self._post_loaded = True
                if not self._handler.empty():
                    self._handler.call(MovieEventHandlers.POST_LOAD, self)

            if control_animation_offset != -1 and self._execed_frame == self._current_frame_internal:
                animation_played = self._animation_played_frame == self._current_frame_current and not self._jumped
                if not animation_played:
                    for i in range(control_animation_offset, frame.controls):
                        control = d.controls[frame.control_offset + i]
                        self.lwf.play_animation(control.control_id, self)

            self._animation_played_frame = self._current_frame_current
            if self._current_frame_current == self._current_frame_internal:
                self._jumped = False

        self._play_animation(ClipEvent.ENTER_FRAME)
        if not self._handler.empty():
            self._handler.call(MovieEventHandlers.ENTER_FRAME, self)
        self._post_exec_count = self.lwf.exec_count

    def exec_attached_lwf(self, tick, current_progress):
        has_btn = False
        instance = self._instance_head
        while instance:
            if instance.is_movie():
                has_btn |= instance.exec_attached_lwf(tick, current_progress)
            instance = instance.link_instance

        if len(self._attached_movies) != 0:
            for movie in self._attached_movies.values():
                has_btn |= movie.exec_attached_lwf(tick, current_progress)

        if len(self._attached_LWFs) != 0:
            for attach_name, v in self._detached_LWFs:
                if attach_name in self._attached_LWFs:
                    self.delete_attached_lwf(self, self._attached_LWFs[attach_name], True, False)
            self._detached_LWFs.clear()

            for attached_lwf in self._attached_LWF_list.values():
                child = attached_lwf.child
                if child.tick == self.lwf.tick:
                    child.set_progress(current_progress)
                self.lwf.render_object(child.exec_internal(tick))
                has_btn |= child.root_movie.has_button
        return has_btn

    def _update_object(self, obj, m, c, matrix_changed, color_transform_changed):
        if obj.is_movie() and obj._property.has_matrix:
            obj_m = m
        elif matrix_changed or not obj.updated or obj.matrix_id_changed:
            obj_m = Utility.calc_matrix(self.lwf, self._matrix_1, m, obj.matrix_id)
        else:
            obj_m = None

        if obj.is_movie() and obj._property.has_color_transform:
            obj_c = c
        elif color_transform_changed or not obj.updated or obj.color_transform_id_changed:
            obj_c = Utility.calc_color_transform(self.lwf, self._color_transform_1, c, obj.color_transform_id)
        else:
            obj_c = None

        obj.update(obj_m, obj_c)

    def update(self, m, c):
        if not self.active:
            return

        if self._overriding:
            matrix_changed = True
            color_transform_changed = True
        else:
            matrix_changed = self.matrix.set_with_comparing(m)
            color_transform_changed = self.color_transform.set_with_comparing(c)

        if self._property.has_matrix:
            matrix_changed = True
            m = Utility.calc_matrix(self._matrix_0, self.matrix, self._property.matrix)
        else:
            m = self.matrix

        if self._property.has_color_transform:
            color_transform_changed = True
            c = Utility.calc_color_transform(self._color_transform_0, self.color_transform, self._property.color_transform)
        else:
            c = self.color_transform

        if len(self._attached_LWFs) != 0:
            self._needs_update_attached_LWFs = False
            self._needs_update_attached_LWFs |= self._matrix_for_attached_LWFs.set_with_comparing(m)
            self._needs_update_attached_LWFs |= self._color_transform_for_attached_LWFs.set_with_comparing(c)

        for dl_depth in range(self.data.depths):
            obj = self._display_list[dl_depth]
            if obj:
                self._update_object(obj, m, c, matrix_changed, color_transform_changed)

        if len(self._bitmap_clips) != 0:
            for bitmap_clip in self._bitmap_clips.values():
                bitmap_clip.update(m, c)

        if len(self._attached_movies) != 0:
            for movie in self._attached_movie_list.values():
                movie._update_object(movie, m, c, matrix_changed, color_transform_changed)

    def post_update(self):
        instance = self._instance_head
        while instance:
            if instance.is_movie():
                instance.post_update()
            instance = instance.link_instance

        if len(self._attached_movies) != 0:
            for movie in self._attached_movie_list.values():
                movie.post_update()

        if self._requested_calculate_bounds:
            self._current_bounds.x_min = 3.402823e+38
            self._current_bounds.x_max = -3.402823e+38
            self._current_bounds.y_min = 3.402823e+38
            self._current_bounds.y_max = -3.402823e+38

            self.inspect(lambda obj, x, y, z: self.calculate_bounds(obj), 0, 0, 0)
            if self.lwf.property.has_matrix:
                invert = Matrix()
                Utility.invert_matrix(invert, self.lwf.property.matrix)
                px, py = Utility.calc_matrix_to_point(self._current_bounds.x_min, self._current_bounds.y_min, invert)
                self._current_bounds.x_min = px
                self._current_bounds.y_min = py
                px, py = Utility.calc_matrix_to_point(self._current_bounds.x_max, self._current_bounds.y_max, invert)
                self._current_bounds.x_max = px
                self._current_bounds.y_max = py

            self._bounds = self._current_bounds
            self._requested_calculate_bounds = False
            if len(self._calculate_bounds_callbacks) != 0:
                for callback in self._calculate_bounds_callbacks:
                    callback(self)
                self._calculate_bounds_callbacks.clear()

        if not self._handler.empty():
            self._handler.call(MovieEventHandlers.UPDATE, self)

    def update_attached_LWF(self):
        instance = self._instance_head
        while instance:
            if instance.is_movie():
                instance.update_attached_LWF()
            instance = instance.link_instance

        if len(self._attached_movies) != 0:
            for movie in self._attached_movie_list.values():
                movie.update_attached_LWF()

        if len(self._attached_LWFs) != 0:
            for attached_lwf in self._attached_LWF_list.values():
                child = attached_lwf.child
                needs_update_attached_LWFs = child.needs_update or self._needs_update_attached_LWFs
                if needs_update_attached_LWFs:
                    child.update(self._matrix_for_attached_LWFs, self._color_transform_for_attached_LWFs)
                if child.is_LWF_attached:
                    child.root_movie.update_attached_LWF()
                if needs_update_attached_LWFs:
                    child.root_movie.post_update()

    def calculate_bounds(self, o):
        if o.type == ObjectType.GRAPHIC:
            d = o.display_list
            for obj in d:
                self.calculate_bounds(obj)
        elif o.type == ObjectType.BITMAP or o.type == ObjectType.BITMAP_EX:
            tf_id = -1
            if o.type == ObjectType.BITMAP:
                if o.object_id < len(o.lwf.data.bitmaps):
                    tf_id = o.lwf.data.bitmaps[o.object_id].texture_fragment_id
            else:
                if o.object_id < len(o.lwf.data.bitmap_exs):
                    tf_id = o.lwf.data.bitmap_exs[o.object_id].texture_fragment_id

            if tf_id >= 0:
                tf = o.lwf.data.texture_fragments[tf_id]
                self._update_bounds(o.matrix, tf.x, tf.x + tf.w, tf.y, tf.y + tf.h)
        elif o.type == ObjectType.BUTTON:
            self._update_bounds(o.matrix, o.width, 0, o.height)
        elif o.type == ObjectType.TEXT:
            text = o.lwf.data.texts[o.object_id]
            self._update_bounds(o.matrix, 0, text.width, 0, text.height)
        elif o.type == ObjectType.PROGRAM_OBJECT:
            p_obj = o.lwf.data.program_objects[o.object_id]
            self._update_bounds(o.matrix, 0, p_obj.width, 0, p_obj.height)

    def _update_bounds(self, *args):
        if len(args) == 5:
            m, x_min, x_max, y_min, y_max = args
            self._update_bounds(m, x_min, y_min)
            self._update_bounds(m, x_min, y_max)
            self._update_bounds(m, x_max, y_min)
            self._update_bounds(m, x_max, y_max)
        else:
            m, sx, sy = args
            px, py = Utility.calc_matrix_to_point(sx, sy, m)
            if px < self._current_bounds.x_min:
                self._current_bounds.x_min = px
            elif px > self._current_bounds.x_max:
                self._current_bounds.x_max = px
            if py < self._current_bounds.y_min:
                self._current_bounds.y_min = py
            elif py > self._current_bounds.y_max:
                self._current_bounds.y_max = py

    def link_button(self):
        if not self.visible or not self.active or not self.has_button:
            return

        for dl_depth in range(self.data.depths):
            obj = self._display_list[dl_depth]
            if obj:
                if obj.is_button():
                    obj.link_button()
                elif obj.is_movie():
                    if obj.has_button:
                        obj.link_button()

        if len(self._attached_movies) != 0:
            for movie in self._attached_movie_list.values():
                if movie and movie.has_button:
                    movie.link_button()

        if len(self._attached_LWFs) != 0:
            for attached_lwf in self._attached_LWF_list.values():
                if attached_lwf is not None:
                    attached_lwf.link_button()

    def render(self, v, r_offset):
        if not self.visible or not self.active:
            v = False

        print('Render Movie')

        use_blend_mode = False
        use_mask_mode = False
        if self.blend_mode != Constant.BLEND_MODE_NORMAL:
            if self.blend_mode == Constant.BLEND_MODE_ADD or self.blend_mode == Constant.BLEND_MODE_MULTIPLY or self.blend_mode == Constant.BLEND_MODE_SCREEN or self.blend_mode == Constant.BLEND_MODE_SUBTRACT:
                self.lwf.begin_blend_mode(self.blend_mode)
                use_blend_mode = True
            elif self.blend_mode == Constant.BLEND_MODE_ERASE or self.blend_mode == Constant.BLEND_MODE_LAYER or self.blend_mode == Constant.BLEND_MODE_MASK:
                self.lwf.begin_mask_mode(self.blend_mode)
                use_mask_mode = True

        if v and not self._handler.empty():
            self._handler.call(MovieEventHandlers.RENDER, self)

        if self._property.has_rendering_offset:
            self.lwf.render_offset()
            r_offset = self._property.rendering_offset

        if r_offset == -2147483648:
            self.lwf.clear_render_offset()

        for dl_depth in range(self.data.depths):
            obj = self._display_list[dl_depth]
            if obj is not None:
                obj.render(v, r_offset)

        if len(self._bitmap_clips) != 0:
            for bitmap_clip in self._bitmap_clips.values():
                bitmap_clip.render(v and bitmap_clip.visible, r_offset)

        if len(self._attached_movies) != 0:
            for movie in self._attached_movie_list.values():
                movie.render(v, r_offset)

        if len(self._attached_LWFs) != 0:
            for attached_lwf in self._attached_LWF_list.values():
                child = attached_lwf.child
                child.set_attach_visible(v)
                self.lwf.render_object(child.render(self.lwf.rendering_index, self.lwf.rendering_count, r_offset))

        if use_blend_mode:
            self.lwf.end_blend_mode()
        if use_mask_mode:
            self.lwf.end_mask_mode()

    def inspect(self, inspector, hierarchy, inspect_depth, r_offset):
        if self._property.has_rendering_offset:
            self.lwf.render_offset()
            r_offset = self._property.rendering_offset

        if r_offset == -2147483648:
            self.lwf.clear_render_offset()

        inspector(self, hierarchy, inspect_depth, r_offset)

        hierarchy += 1

        d = 0
        for d in range(self.data.depths):
            obj = self._display_list[d]
            if obj:
                obj.inspect(inspector, hierarchy, d, r_offset)

        if len(self._bitmap_clips) != 0:
            for bitmap_clip in self._bitmap_clips.values():
                bitmap_clip.inspect(inspector, hierarchy, d, r_offset)
                d += 1

        if len(self._attached_movies) != 0:
            for movie in self._attached_movie_list.values():
                movie.inspect(inspector, hierarchy, d, r_offset)
                d += 1

        if len(self._attached_LWFs) != 0:
            for attached_lwf in self._attached_LWF_list.values():
                self.lwf.render_object(attached_lwf.child.inspect(inspector, hierarchy, d, r_offset))
                d += 1

    def destroy(self):
        for dl_depth in range(self.data.depths):
            obj = self._display_list[dl_depth]
            if obj:
                obj.destroy()

        if len(self._bitmap_clips) != 0:
            for bitmap_clip in self._bitmap_clips.values():
                bitmap_clip.destroy()
            self._bitmap_clips.clear()

        if len(self._attached_movies) != 0:
            for movie in self._attached_movie_list.values():
                movie.destroy()
            self._attached_movies.clear()
            self._attached_movie_list.clear()
            self._detached_movies.clear()

        if len(self._attached_LWFs):
            for attached_lwf in self._attached_LWFs.values():
                if attached_lwf.child.detach_handler:
                    if attached_lwf.child.detach_handler(attached_lwf.child):
                        attached_lwf.child.destroy()
                else:
                    attached_lwf.child.destroy()
            self._attached_LWFs.clear()
            self._attached_LWF_list.clear()
            self._detached_LWFs.clear()

        self._play_animation(ClipEvent.UNLOAD)

        if not self._handler.empty():
            self._handler.call(MovieEventHandlers.UNLOAD, self)

        self._display_list.clear()
        self._property = None
        super().destroy()

    def _play_animation(self, clip_event):
        clip_events = self.lwf.data.movie_clip_events
        for i in range(self.data.clip_events):
            c = clip_events[self.data.clip_event_id + i]
            if (c.clip_event & clip_event) != 0:
                self.lwf.play_animation(c.animation_id, self)

    def search_frame(self, string):
        return self.lwf.search_frame(self, string)

    def search_movie_instance(self, argument, recursive=True):
        if isinstance(argument, str):
            string_id = self.lwf.get_string_id(argument)
            if string_id == -1:
                if len(self._attached_movies) != 0:
                    for attached_movie in self._attached_movie_list.values():
                        if attached_movie.attach_name == argument:
                            return attached_movie
                        elif recursive:
                            movie = attached_movie.search_movie_instance(argument, recursive)
                            if movie:
                                return movie
                if len(self._attached_LWFs) != 0:
                    for attached_lwf in self._attached_LWF_list.values():
                        child = attached_lwf.child
                        if child.attach_name == argument:
                            return child.root_movie
                        elif recursive:
                            movie = child.root_movie.search_movie_instance(argument, recursive)
                            if movie:
                                return movie
                return None
        else:
            string_id = argument

        if string_id == -1:
            return None

        instance = self._instance_head
        while instance is not None:
            if instance.is_movie() and self.lwf.get_instance_name_string_id(instance.instance_id) == string_id:
                return instance
            elif recursive and instance.is_movie():
                i = instance.search_move_instance(string_id, recursive)
                if i:
                    return i
            instance = instance.link_instance
        return None

    def __getitem__(self, instance_name):
        return self.search_movie_instance(instance_name, False)

    def search_movie_instance_by_instance_id(self, inst_id, recursive=True):
        instance = self._instance_head
        while instance is not None:
            if instance.is_movie() and instance.instance_id == inst_id:
                return instance
            elif recursive and instance.is_movie():
                i = instance.search_movie_instance_by_instance_id(inst_id, recursive)
                if i is not None:
                    return i
            instance = instance.link_instance
        return None

    def search_button_instance(self, argument, recursive=True):
        if isinstance(argument, str):
            string_id = self.lwf.get_string_id(argument)
            if string_id == -1:
                if len(self._attached_movies) != 0 and recursive:
                    for attached_movie in self._attached_movie_list.values():
                        button = attached_movie.search_button_instance(argument, recursive)
                        if button:
                            return button
                if len(self._attached_LWFs) != 0:
                    for attached_lwf in self._attached_LWF_list.values():
                        child = attached_lwf.child
                        button = child.root_movie.search_button_instance(argument, recursive)
                        if button:
                            return button
                return None
        else:
            string_id = argument

        if string_id == -1:
            return None

        instance = self._instance_head
        while instance is not None:
            if instance.is_button() and self.lwf.get_instance_name_string_id(instance.instance_id) == string_id:
                return instance
            elif recursive and instance.is_movie():
                i = instance.search_button_instance(string_id, recursive)
                if i:
                    return i
            instance = instance.link_instance
        return None

    def search_button_instance_by_instance_id(self, inst_id, recursive=True):
        instance = self._instance_head
        while instance is not None:
            if instance.is_button() and instance.instance_id == inst_id:
                return instance
            elif recursive and instance.is_movie():
                i = instance.search_button_instance_by_instance_id(inst_id, recursive)
                if i:
                    return i
            instance = instance.link_instance
        return None

    def insert_text(self, obj_id):
        text = self.lwf.data.texts[obj_id]
        if text.name_string_id != -1:
            self._texts[self.lwf.data.strings[text.name_string_id]] = True

    def erase_text(self, obj_id):
        text = self.lwf.data.texts[obj_id]
        if text.name_string_id != -1:
            self._texts.pop(self.lwf.data.strings[text.name_string_id])

    def search_text(self, text_name):
        if not self._texts:
            self._texts = {}
            for dl_depth in range(self.data.depths):
                obj = self._display_list[dl_depth]
                if obj and obj.is_text():
                    self.insert_text(obj.object_id)

        return text_name in self._texts

    def add_event_handler(self, event_name, event_handler):
        handler_id = self.lwf.get_event_offset()
        if self._handler.add(handler_id, event_name, event_handler):
            return handler_id
        
        if event_name not in self._event_handlers:
            self._event_handlers[event_name] = []
        self._event_handlers[event_name][handler_id] = event_handler

    def remove_event_handler(self, event_name, handler_id):
        if event_name in self._event_handlers:
            self._event_handlers.pop(handler_id)
        for handler_list in self._event_handlers:
            if event_name in handler_list:
                handler_list.pop(handler_id)

    def remove_movie_event_handler(self, handler_id):
        self._handler.remove(handler_id)

    def clear_event_handler(self, event_name):
        self._event_handlers.pop(event_name)
        self._handler.clear(event_name)

    def clear_movie_event_handler(self, event_name):
        self._handler.clear()

    def clear_all_event_handler(self):
        self._event_handlers.clear()
        self._handler.clear()

    def set_event_handler(self, event_name, event_handler):
        self.clear_event_handler(event_name)
        return self.add_event_handler(event_name, event_handler)

    def dispatch_event(self, event_name):
        if self._handler.call(event_name, self):
            return
        for handler in self._event_handlers[event_name].values():
            handler(self)

    def request_calculate_bounds(self, callback):
        if not self._requested_calculate_bounds:
            self._requested_calculate_bounds = True
            self._bounds.clear()
        if callback:
            self._calculate_bounds_callbacks.append(callback)

    def get_bounds(self):
        return self._bounds

    def _cache_current_labels(self):
        if self._current_labels_cached:
            return

        self._current_labels_cached = True
        labels = self.lwf.get_movie_labels(self)
        if not labels:
            return

        for string_id, frame_no in labels:
            label_data = LabelData()
            label_data.frame = frame_no + 1
            label_data.name = self.lwf.data.strings[string_id]
            self._current_labels_cache.append(label_data)
            self._current_labels_cache = sorted(self._current_labels_cache)

    def get_current_label(self):
        self._cache_current_labels()

        if len(self._current_labels_cache) == 0:
            return ""

        current_frame_temp = self._current_frame_internal + 1
        if current_frame_temp < 1:
            current_frame_temp = 1

        if current_frame_temp in self._current_labels_cache:
            label_name = self._current_labels_cache[current_frame_temp]
        else:
            first_label = self._current_labels_cache[0]
            last_label = self._current_labels_cache[-1]
            if current_frame_temp < first_label.frame:
                label_name = ""
            elif current_frame_temp == first_label.frame:
                label_name = first_label.name
            elif current_frame_temp >= last_label.frame:
                label_name = last_label.name
            else:
                l = 0
                ln = self._current_labels_cache[l].frame
                r = len(self._current_labels_cache) - 1
                rn = self._current_labels_cache[r].frame
                while True:
                    if l == r or r - l == 1:
                        if current_frame_temp < ln:
                            label_name = ""
                        elif current_frame_temp == rn:
                            label_name = self._current_labels_cache[r].name
                        else:
                            label_name = self._current_labels_cache[l].name
                        break
                    n = floor((r - l) / 2.0) + l
                    nn = self._current_labels_cache[n].frame
                    if current_frame_temp < nn:
                        r = n
                        rn = nn
                    elif current_frame_temp > nn:
                        l = n
                        ln = nn
                    else:
                        label_name = self._current_labels_cache[n].name
                        break
            self._current_labels_cache[current_frame_temp] = label_name
        return label_name

    def get_current_labels(self):
        self._cache_current_labels()
        return self._current_labels_cache

    def _reorder_attached_movie_list(self, reorder, index, movie):
        self._attached_movie_list[index] = movie
        if reorder:
            attach_list = self._attached_movie_list
            self._attached_movie_list.clear()
            for i, movie in enumerate(attach_list.values()):
                movie.depth = i
                self._attached_movie_list[i] = movie

    def _delete_attached_movie(self, p, movie, destroy=True, delete_from_detached_movies=True):
        attach_name = movie.attach_name
        attach_depth = movie.depth
        p._attached_movies.pop(attach_name)
        p._attached_movie_list.remove(attach_depth)

        if delete_from_detached_movies:
            p._detached_movies.pop(attach_name)
        if destroy:
            movie.destroy()

    def attach_movie(self, linkage_name, attach_name, h=None, a_depth=-1, reorder=False):
        if h is None:
            h = {}
        movie_id = self.lwf.search_movie_linkage(self.lwf.get_string_id(linkage_name))
        if movie_id == -1:
            return None

        handlers = MovieEventHandlers()
        handlers.add(self.lwf.get_event_offset(), h)
        movie = Movie(self.lwf, self, movie_id, -1, 0, 0, True, handlers, attach_name)
        if self._attach_movie_execed:
            movie.exec()
        if self._attach_move_post_execed:
            movie.post_exec(True)

        if attach_name in self._attached_movies:
            self._delete_attached_movie(self, self._attached_movies[attach_name])

        if not reorder and a_depth >= 0:
            if a_depth in self._attached_movie_list:
                self._delete_attached_movie(self, self._attached_movie_list[a_depth])

        if a_depth < 0:
            if len(self._attached_movie_list) == 0:
                a_depth = 0
            else:
                a_depth = list(self._attached_movie_list.keys())[-1] + 1

        movie.attach_name = attach_name
        movie.depth = a_depth
        self._attached_movies[attach_name] = movie
        self._reorder_attached_movie_list(reorder, movie.depth, movie)
        return movie

    def attach_empty_movie(self, attach_name, h=None, a_depth=-1, reorder=False):
        return self.attach_movie("_empty", attach_name, h, a_depth, reorder)

    def swap_attached_movie_depth(self, depth_0, depth_1):
        if len(self._attached_movies) == 0:
            return

        attached_movie_0 = None
        if depth_0 in self._attached_movie_list:
            attached_movie_0 = self._attached_movie_list[depth_0]

        attached_movie_1 = None
        if depth_1 in self._attached_movie_list:
            attached_movie_1 = self._attached_movie_list[depth_1]

        if attached_movie_0:
            attached_movie_0.depth = depth_1
            self._attached_movie_list[depth_1] = attached_movie_0
        else:
            self._attached_movie_list.pop(depth_1)

        if attached_movie_1:
            attached_movie_1.depth = depth_0
            self._attached_movie_list[depth_0] = attached_movie_1
        else:
            self._attached_movie_list.pop(depth_0)

    def get_attached_movie(self, attach):
        if isinstance(attach, str):
            if attach in self._attached_movies:
                return self._attached_movies[attach]
        else:
            if attach in self._attached_movie_list:
                return self._attached_movie_list[attach]
        return None

    def search_attached_movie(self, attach_name, recursive=True):
        movie = self.get_attached_movie(attach_name)
        if movie:
            return movie

        if not recursive:
            return None

        instance = self._instance_head
        while instance is not None:
            if instance.is_movie():
                i = instance.search_attached_movie(attach_name, recursive)
                if i:
                    return i
            instance = instance.link_instance

        if len(self._attached_movies) != 0:
            for movie in self._attached_movie_list.values():
                i = movie.search_attached_movie(attach_name, recursive)
                if i:
                    return i
        if len(self._attached_LWFs):
            for lwf in self._attached_LWF_list.values():
                child = lwf.child
                if child.attach_name == attach_name:
                    return child.root_movie
                else:
                    movie = child.root_movie.search_attached_movie(attach_name, recursive)
                    if movie:
                        return movie
        return None

    def detach_movie(self, attach):
        if isinstance(attach, str):
            self._detached_movies[attach] = True
        elif isinstance(attach, int):
            if attach in self._attached_movie_list:
                self._detached_movies[self._attached_movie_list[attach].attach_name] = True
        else:
            if attach and attach.attach_name:
                self._detached_movies[attach.attach_name] = True

    def detach_from_parent(self):
        if self.type != ObjectType.ATTACHED_MOVIE:
            return

        self.active = False
        if self.parent:
            self.parent.detach_movie(self.attach_name)

    def _reorder_attached_lwf_list(self, reorder, index, lwf_container):
        self._attached_LWF_list[index] = lwf_container
        if reorder:
            attach_list = self._attached_LWF_list
            self._attached_LWF_list.clear()
            for i, lwf in enumerate(attach_list.values()):
                lwf.child.depth = i
                self._attached_LWF_list[i] = lwf

    def _delete_attached_lwf(self, p, lwf_container, destroy=True, delete_from_detached_lwfs=True):
        attach_name = lwf_container.child.attach_name
        attach_depth = lwf_container.child.depth
        p._attached_LWFs.pop(attach_name)
        p._attached_LWF_list.pop(attach_depth)
        if delete_from_detached_lwfs:
            p._detached_LWFs.pop(attach_name)
        if destroy:
            l = lwf_container.child
            if l.detach_handler:
                if l.detach_handler(l):
                    l.destroy()
            else:
                l.destroy()

            l.parent = None
            l._root = None
            l.detach_handler = None
            l.attach_name = None
            l.depth = -1
            lwf_container.destroy()

    def attach_lwf(self, attach_lwf, attach_name, detach_handler=None, attach_depth=-1, reorder=False):
        if isinstance(attach_lwf, str):
            if not self.lwf.lwf_loader:
                return None
            child = self.lwf.lwf_loader(attach_lwf)
            if not child:
                return child
            self.attach_lwf(child, attach_name, detach_handler, attach_depth, reorder)
            return child
        else:
            # if not detach_handler:
            #     detach_handler = DetachHandler()
            if attach_lwf.parent:
                if attach_lwf.attach_name in attach_lwf.parent._attached_LWFs:
                    self._delete_attached_lwf(attach_lwf.parent, attach_lwf.parent._attached_LWFs[attach_lwf.attach_name], False)

            if attach_name in self._attached_LWFs:
                self._delete_attached_lwf(self, self._attached_LWFs[attach_name])

            if not reorder and attach_depth >= 0:
                if attach_depth in self._attached_LWF_list:
                    self._delete_attached_lwf(self, self._attached_LWF_list[attach_depth])

            lwf_container = LWFContainer(self, attach_lwf)

            if attach_lwf.interactive:
                self.lwf.interactive = True

            if attach_depth < 0:
                if len(self._attached_LWF_list) == 0:
                    attach_depth = 0
                else:
                    attach_depth = list(self._attached_LWF_list.keys())[-1] + 1

            attach_lwf.parent = self
            attach_lwf._root = self.lwf._root
            attach_lwf.scale_by_stage = self.lwf.scale_by_stage
            attach_lwf.detach_handler = detach_handler
            attach_lwf.attach_name = attach_name
            attach_lwf.depth = attach_depth
            self._attached_LWFs[attach_name] = lwf_container
            self._reorder_attached_lwf_list(reorder, attach_lwf.depth, lwf_container)
            self.lwf.set_lwf_attached()

    def swap_attached_lwf_depth(self, depth_0, depth_1):
        if len(self._attached_LWFs) == 0:
            return

        attached_lwf_0 = None
        if depth_0 in self._attached_LWF_list:
            attached_lwf_0 = self._attached_LWF_list[depth_0]

        attached_lwf_1 = None
        if depth_1 in self._attached_LWF_list:
            attached_lwf_1 = self._attached_LWF_list[depth_1]

        if attached_lwf_0:
            attached_lwf_0.depth = depth_1
            self._attached_LWF_list[depth_1] = attached_lwf_0
        else:
            self._attached_LWF_list.pop(depth_1)

        if attached_lwf_1:
            attached_lwf_1.depth = depth_0
            self._attached_LWF_list[depth_0] = attached_lwf_1
        else:
            self._attached_LWF_list.pop(depth_0)

    def get_attached_lwf(self, attach):
        if isinstance(attach, str):
            if attach in self._attached_LWFs:
                return self._attached_LWFs[attach].child
        else:
            if attach in self._attached_LWF_list:
                return self._attached_LWF_list[attach].child
        return None

    def search_attached_lwf(self, attach_name, recursive=True):
        attached_lwf = self.get_attached_lwf(attach_name)
        if attached_lwf is not None:
            return attached_lwf

        if not recursive:
            return None

        instance = self._instance_head
        while instance:
            if instance.is_movie():
                i = instance.search_attached_movie(attach_name, recursive)
                if i:
                    return i
            instance = instance.link_instance
        return None

    def detach_lwf(self, attach):
        if isinstance(attach, str):
            self._detached_LWFs[attach] = True
        elif isinstance(attach, int):
            if attach in self._attached_LWF_list:
                self._detached_LWFs[self._attached_LWF_list[attach].child.attach_name] = True
        else:
            if attach and attach.attach_name:
                self._detached_LWFs[attach.attach_name] = True

    def detach_all_lwfs(self):
        for attach in self._detached_LWFs.values():
            self._detached_LWFs[attach.child.attach_name] = True

    def remove_movie_clip(self):
        if self.type == ObjectType.ATTACHED_MOVIE:
            self.detach_from_parent()
        elif self.lwf.attach_name and self.lwf.parent:
            self.lwf.parent.detach_lwf(self.lwf.attach_name)

    def attach_bitmap(self, linkage_name, attach_depth):
        if linkage_name in self.lwf.data.bitmap_map:
            bitmap_clip = BitmapClip(self.lwf, self, self.lwf.data.bitmap_map[linkage_name])

            self.detach_bitmap(attach_depth)
            self._bitmap_clips[attach_depth] = bitmap_clip
            bitmap_clip.depth = attach_depth
            bitmap_clip.name = linkage_name
            return bitmap_clip
        return None

    def get_attached_bitmaps(self):
        return self._bitmap_clips

    def get_attached_bitmap(self, attach_depth):
        if attach_depth in self._bitmap_clips:
            return self._bitmap_clips[attach_depth]
        return None

    def swap_attached_bitmap_depth(self, depth_0, depth_1):
        if len(self._bitmap_clips) == 0:
            return

        attached_bitmap_0 = None
        if depth_0 in self._bitmap_clips:
            attached_bitmap_0 = self._bitmap_clips[depth_0]

        attached_bitmap_1 = None
        if depth_1 in self._bitmap_clips:
            attached_bitmap_1 = self._bitmap_clips[depth_1]

        if attached_bitmap_0:
            attached_bitmap_0.depth = depth_1
            self._bitmap_clips[depth_1] = attached_bitmap_0
        else:
            self._bitmap_clips.pop(depth_1)

        if attached_bitmap_1:
            attached_bitmap_1.depth = depth_0
            self._bitmap_clips[depth_0] = attached_bitmap_1
        else:
            self._bitmap_clips.pop(depth_0)

    def detach_bitmap(self, attach_depth):
        if attach_depth in self._bitmap_clips:
            self._bitmap_clips[attach_depth].destroy()
            self._bitmap_clips.pop(attach_depth)

    def play(self):
        self.playing = True
        return self

    def stop(self):
        self.playing = False
        return self

    def next_frame(self):
        self._jumped = True
        self.stop()
        self._current_frame_internal += 1
        self.current_frame = self._current_frame_internal + 1
        return self

    def prev_frame(self):
        self._jumped = True
        self.stop()
        self._current_frame_internal -= 1
        self.current_frame = self._current_frame_internal + 1
        return self

    def goto_frame(self, frame_number):
        self.goto_frame_internal(frame_number - 1)
        return self

    def goto_frame_internal(self, frame_number):
        self._jumped = True
        self.stop()
        self._current_frame_internal = frame_number
        self.current_frame = self._current_frame_internal + 1
        return self

    def set_visible(self, visible):
        self.visible = visible
        self.lwf.set_property_dirty()
        return self

    def goto_label(self, string):
        if isinstance(string, str):
            self.goto_label(self.lwf.get_string_id(string))
        else:
            self.goto_frame(self.lwf.search_frame(self, string))
        return self

    def goto_and_stop(self, frame):
        if isinstance(frame, str):
            self.goto_frame(self.lwf.search_frame(self, self.lwf.get_string_id(frame)))
        else:
            self.goto_frame(frame)
        self.stop()
        return self

    def goto_and_play(self, frame):
        if isinstance(frame, str):
            self.goto_frame(self.lwf.search_frame(self, self.lwf.get_string_id(frame)))
        else:
            self.goto_frame(frame)
        self.play()
        return self

    def move(self, vx, vy):
        if not self._property.has_matrix:
            Utility.sync_matrix(self)
        self._property.move(vx, vy)
        return self

    def move_to(self, vx, vy):
        if not self._property.has_matrix:
            Utility.sync_matrix(self)
        self._property.move_to(vx, vy)
        return self

    def rotate(self, degree):
        if not self._property.has_matrix:
            Utility.sync_matrix(self)
        self._property.rotate(degree)
        return self

    def rotate_to(self, degree):
        if not self._property.has_matrix:
            Utility.sync_matrix(self)
        self._property.rotate_to(degree)
        return self

    def scale(self, vx, vy):
        if not self._property.has_matrix:
            Utility.sync_matrix(self)
        self._property.scale(vx, vy)
        return self

    def scale_to(self, vx, vy):
        if not self._property.has_matrix:
            Utility.sync_matrix(self)
        self._property.scale_to(vx, vy)
        return self

    def set_matrix(self, m, sx=1, sy=1, r=0):
        self._property.set_matrix(m, sx, sy, r)
        return self

    def set_alpha_value(self, v):
        if not self._property.has_color_transform:
            Utility.sync_color_transform(self)
        self._property.set_alpha(v)
        return self

    def set_color_transform(self, c):
        self._property.set_color_transform(c)
        return self

    def set_rendering_offset(self, r_offset):
        self._property.set_rendering_offset(r_offset)
        return self

    def get_x(self):
        if self._property.has_matrix:
            return self._property.matrix.translate_x
        else:
            return Utility.get_x(self)

    def set_x(self, value):
        if self._property.has_matrix:
            Utility.sync_matrix(self)
        self._property.move_to(value, self._property.matrix.translate_y)

    def get_y(self):
        if self._property.has_matrix:
            return self._property.matrix.translate_y
        else:
            return Utility.get_y(self)

    def set_y(self, value):
        if self._property.has_matrix:
            Utility.sync_matrix(self)
        self._property.move_to(self._property.matrix.translate_x, value)

    def get_scale_x(self):
        if self._property.has_matrix:
            return self._property.matrix.scale_x
        else:
            return Utility.get_scale_x(self)

    def set_scale_x(self, value):
        if self._property.has_matrix:
            Utility.sync_matrix(self)
        self._property.scale_to(value, self._property.matrix.scale_y)

    def get_scale_y(self):
        if self._property.has_matrix:
            return self._property.matrix.scale_y
        else:
            return Utility.get_scale_y(self)

    def set_scale_y(self, value):
        if self._property.has_matrix:
            Utility.sync_matrix(self)
        self._property.scale_to(self._property.matrix.scale_x, value)

    def get_rotation(self):
        if self._property.has_matrix:
            return self._property.rotation
        else:
            return Utility.get_rotation(self)

    def set_rotation(self, value):
        if self._property.has_matrix:
            Utility.sync_matrix(self)
        self._property.rotate_to(value)

    def get_alpha(self):
        if self._property.has_color_transform:
            return self._property.color_transform.multi.alpha
        else:
            return Utility.get_alpha(self)

    def set_alpha(self, value):
        if self._property.has_color_transform:
            Utility.sync_color_transform(self)
        self._property.set_alpha(value)

    def get_red(self):
        if self._property.has_color_transform:
            return self._property.color_transform.multi.red
        else:
            return Utility.get_red(self)

    def set_red(self, value):
        if self._property.has_color_transform:
            Utility.sync_color_transform(self)
        self._property.set_red(value)

    def get_green(self):
        if self._property.has_color_transform:
            return self._property.color_transform.multi.green
        else:
            return Utility.get_green(self)

    def set_green(self, value):
        if self._property.has_color_transform:
            Utility.sync_color_transform(self)
        self._property.set_green(value)

    def get_blue(self):
        if self._property.has_color_transform:
            return self._property.color_transform.multi.blue
        else:
            return Utility.get_blue(self)

    def set_blue(self, value):
        if self._property.has_color_transform:
            Utility.sync_color_transform(self)
        self._property.set_blue(value)
