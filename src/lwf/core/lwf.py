__all__ = ('LWF',)

from math import ceil
from datetime import datetime

from .constructs import Property, Movie, MovieEventHandlers, ButtonEventHandlers, Animation
from .format import Constant
from .tools import Utility
from .type import Matrix, ColorTransform


class LWF:
    class TweenMode:
        TweenModeMovie = 0
        TweenModeLWF = 1

    ROUND_OFF_TICK_RATE = 0.05

    _instance_offset = 0
    _i_object_offset = 0
    _texture_load_handler = None

    def __init__(self, d, r):
        self.data = d
        self.renderer_factory = None
        self.property = Property(self)
        self.root_movie = None
        self._root = None
        self.focus = None
        self.focus_on_link = False
        self.pressed = None
        self.button_head = None
        self.detach_handler = None
        self.parent = None
        self.event_functions = None
        self.lwf_loader = None
        self.lwf_unloader = None
        self.name = self.data.strings[self.data.header.name_string_id]
        self.attach_name = None

        self.frame_rate = self.data.header.frame_rate
        self.exec_limit = 3
        self.rendering_index = 0
        self.rendering_index_offsetted = 0
        self.rendering_count = 0
        self.depth = 0
        self.exec_count = 0
        self.update_count = 0
        self.instance_id = self._instance_offset + 1
        self.instance_id_string = str(self.instance_id)
        self.time = 0.0
        self.scale_by_stage = 1.0
        self.tick = 1.0 / self.frame_rate
        self.height = self.data.header.height
        self.width = self.data.header.width
        self.point_x = -3.402823e+38
        self.point_y = -3.402823e+38
        self.interactive = len(self.data.buttons) != 0
        self.is_exec_disabled = False
        self.pressing = False
        self.attach_visible = True
        self.is_property_dirty = False
        self.is_lwf_attached = False
        self.intercept_by_not_allow_or_deny_buttons = True
        self.intercepted = False
        self.needs_update = False
        self.playing = True
        self.alive = True
        self.private_data = None

        # self.lua_state = l
        # self.lua_error = None

        self._instances = {}
        self._event_handlers = None
        self._generic_event_handler_dictionary = {}
        self._movie_event_handlers = None
        self._button_event_handlers = None
        self._movie_event_handlers_by_full_name = {}
        self._button_event_handlers_by_full_name = {}
        self._movie_commands = []
        self._program_object_constructors = {}
        self._allow_button_list = {}
        self._deny_button_list = {}
        self._exec_handlers = []
        self._text_dictionary = {}
        self._blend_modes = []
        self._mask_modes = []
        self._progress = 0.0
        self._round_off_tick = self.tick * self.ROUND_OFF_TICK_RATE
        self._executed_for_exec_disabled = False
        self._matrix = Matrix()
        self._matrix_identity = Matrix()
        self._exec_matrix = Matrix()
        self._color_transform = ColorTransform()
        self._color_transform_identity = ColorTransform()
        self._exec_color_transform = ColorTransform()
        self._root_movie_string_id = 0
        self._event_offset = 0
        self._frame_skip = True
        self._fast_forward = False
        self._fast_forward_current = False
        self._fast_forward_timeout = 15
        self._needs_update_for_attach_lwf = False

        if not self.interactive and len(self.data.frames) == 1:
            self.disable_exec()

        self.init_event()

        self.init()

        self.set_renderer_factory(r)

    def set_renderer_factory(self, r):
        self.renderer_factory = r
        self.renderer_factory.init(self)

    def set_frame_rate(self, f):
        if f == 0:
            return
        self.frame_rate = f
        self.tick = 1.0 / self.frame_rate

    def set_preferred_frame_rate(self, f, e_limit=2):
        if f == 0:
            return
        self.exec_limit = ceil(self.frame_rate / f) + e_limit

    def set_interactive(self):
        self.interactive = True
        if self.parent:
            self.parent.set_interactive()

    def set_frame_skip(self, frame_skip):
        self._frame_skip = frame_skip
        self._progress = 0
        if self.parent:
            self.parent.lwf.set_frame_skip(frame_skip)

    def set_lwf_attached(self):
        self.is_lwf_attached = True
        self._needs_update_for_attach_lwf = True
        if self.parent:
            self.parent.set_lwf_attached()

    def set_fast_forward_timeout(self, fast_forward_timeout):
        self._fast_forward_timeout = fast_forward_timeout

    def set_fast_forward(self, fast_forward):
        self._fast_forward = fast_forward
        if self.parent:
            self.parent.lwf.set_fast_forward(fast_forward)

    def fit_for_height(self, stage_width, stage_height):
        self.renderer_factory.fit_for_height(self, stage_width, stage_height)

    def fit_for_width(self, stage_width, stage_height):
        self.renderer_factory.fit_for_height(self, stage_width, stage_height)

    def scale_for_height(self, stage_width, stage_height):
        self.renderer_factory.scale_for_height(self, stage_width, stage_height)

    def scale_for_width(self, stage_width, stage_height):
        self.renderer_factory.scale_for_width(self, stage_width, stage_height)

    def render_offset(self):
        self.rendering_index_offsetted = 0

    def clear_render_offset(self):
        self.rendering_index_offsetted = self.rendering_index

    def render_object(self, count=1):
        self.rendering_index += count
        self.rendering_index_offsetted += count
        return self.rendering_index

    def begin_blend_mode(self, blend_mode):
        print('\tBegin Blend Mode')
        self._blend_modes.append(blend_mode)
        self.renderer_factory.set_blend_mode(blend_mode)

    def end_blend_mode(self):
        print('\tEnd Blend Mode')
        self._blend_modes.pop()
        blend_mode = Constant.BLEND_MODE_NORMAL
        if len(self._blend_modes) != 0:
            blend_mode = self._blend_modes[-1]
        self.renderer_factory.set_blend_mode(blend_mode)

    def begin_mask_mode(self, mask_mode):
        self._mask_modes.append(mask_mode)
        self.renderer_factory.set_mask_mode(mask_mode)

    def end_mask_mode(self):
        self._mask_modes.pop()
        mask_mode = Constant.BLEND_MODE_NORMAL
        if len(self._mask_modes) != 0:
            mask_mode = self._mask_modes[-1]
        self.renderer_factory.set_mask_mode(mask_mode)

    def set_attach_visible(self, visible):
        self.attach_visible = visible

    def clear_focus(self, button):
        if self.focus == button:
            self.focus = None

    def clear_pressed(self, button):
        if self.pressed == button:
            self.pressed = None

    def clear_intercepted(self):
        self.intercepted = False

    @staticmethod
    def get_time_of_day():
        # Returns the time since EPOC in milliseconds; Since we are using this for a diff, we do not care about which EPOC
        time = datetime.utcnow()
        return (((time.day * 24 + time.hour) * 60 + time.minute) * 60 + time.second) * 1000 + time.microsecond / 1000.0

    def init(self):
        self.time = 0
        self._progress = 0

        self._instances.clear()
        self.focus = None
        self.pressed = None
        self.button_head = None

        self._movie_commands.clear()

        self._root_movie_string_id = self.get_string_id('_root')
        if self.root_movie:
            self.root_movie.destroy()
        self.root_movie = Movie(self, None, self.data.header.root_movie_id, self.search_instance_id(self._root_movie_string_id))
        self._root = self.root_movie

    def calc_matrix(self, matrix):
        p = self.property
        if p.has_matrix:
            if matrix:
                m = Utility.calc_matrix(self._matrix, matrix, p.matrix)
            else:
                m = p.matrix
        else:
            m = self._matrix_identity if matrix else matrix
        return m

    def calc_color_transform(self, color_transform):
        p = self.property
        if p.has_color_transform:
            if color_transform is not None:
                c = Utility.calc_color_transform(self._color_transform, color_transform, p.color_transform)
            else:
                c = p.color_transform
        else:
            c = self._color_transform_identity if not color_transform else color_transform
        return c

    def link_button(self):
        self.button_head = None
        if self.interactive and self.root_movie.has_button:
            self.focus_on_link = False
            self.root_movie.link_button()
            if self.focus and not self.focus_on_link:
                self.focus.roll_out()
                self.focus = None

    def exec_internal(self, t):
        if not self.playing:
            return self.rendering_count

        execed = False
        current_progress = self._progress

        if self.is_exec_disabled:
            if not self._executed_for_exec_disabled:
                self.exec_count += 1
                self.root_movie.exec()
                self.root_movie.post_exec(True)
                self._executed_for_exec_disabled = True
                execed = True
        else:
            progressing = True
            if t == 0:
                self._progress = self.tick
            elif t < 0:
                self._progress = self.tick
                progressing = False
            else:
                if self.time == 0:
                    self.time += self.tick
                    self._progress += self.tick
                else:
                    self.time += t
                    self._progress += t

            for hid, exec_handler in self._exec_handlers:
                exec_handler(self)

            e_limit = self.exec_limit
            while self._progress >= self.tick - self._round_off_tick:
                e_limit -= 1
                if e_limit < 0:
                    self._progress = 0
                    break
                self._progress -= self.tick
                self.exec_count += 1
                self.root_movie.exec()
                self.root_movie.post_exec(progressing)
                execed = True
                if not self._frame_skip:
                    break

            if self._progress < self._round_off_tick:
                self._progress = 0

            self.link_button()

        if self.is_lwf_attached:
            has_button = self.root_movie.exec_attached_lwf(t, current_progress)
            if has_button:
                self.link_button()

        self.needs_update = False
        if not self._fast_forward:
            if execed or self.is_property_dirty or self._needs_update_for_attach_lwf:
                self.needs_update = True

        if not self.is_exec_disabled:
            if t < 0:
                self._progress = current_progress

        return self.rendering_count

    def exec(self, t, matrix=None, color_transform=None):
        needs_to_call_update = False
        if matrix:
            needs_to_call_update |= self._exec_matrix.set_with_comparing(matrix)
        if color_transform:
            needs_to_call_update |= self._exec_color_transform.set_with_comparing(color_transform)

        start_time = None
        if not self.parent:
            self._fast_forward_current = self._fast_forward
            if self._fast_forward_current:
                t = self.tick
                start_time = self.get_time_of_day()
        while True:
            r_count = self.exec_internal(t)
            needs_to_call_update |= self.needs_update
            if needs_to_call_update:
                self.update(matrix, color_transform)
            if self.is_lwf_attached:
                self.root_movie.update_attached_lwf()
            if needs_to_call_update:
                self.root_movie.post_update()
            if self._fast_forward_current and self._fast_forward and not self.parent:
                now = self.get_time_of_day()
                diff = now - start_time
                if diff > self._fast_forward_timeout:
                    break
            else:
                break
        return r_count

    def force_exec(self, matrix=None, color_transform=None):
        return self.exec(0, matrix, color_transform)

    def force_exec_without_progress(self, matrix=None, color_transform=None):
        return self.exec(-1, matrix, color_transform)

    def update(self, matrix=None, color_transform=None):
        self.update_count += 1
        m = self.calc_matrix(matrix)
        c = self.calc_color_transform(color_transform)
        self.rendering_index = 0
        self.rendering_index_offsetted = 0
        self.root_movie.update(m, c)
        self.rendering_count = self.rendering_index
        self.is_property_dirty = False
        self._needs_update_for_attach_lwf = False

    def render(self, r_index=0, r_count=0, r_offset=-2147483648):
        print('Render LWF')
        if self._fast_forward_current:
            return 0
        if r_count > 0:
            self.rendering_count = r_count
        self.rendering_index = r_index
        self.rendering_index_offsetted = r_index
        if self.property.has_rendering_offset:
            self.render_offset()
            r_offset = self.property.rendering_offset

        self.renderer_factory.begin_render(self)
        self.root_movie.render(self.attach_visible, r_offset)
        self.renderer_factory.end_render(self)
        return self.rendering_index - r_index

    def inspect(self, inspector, hierarchy=0, inspect_depth=0, r_index=0, r_count=0, r_offset=-2147483648):
        if r_count > 0:
            self.rendering_count = r_count
        self.rendering_index = r_index
        self.rendering_index_offsetted = r_index
        if self.property.has_rendering_offset:
            self.render_offset()
            r_offset = self.property.rendering_offset

        self.root_movie.inspect(inspector, hierarchy, inspect_depth, r_offset)
        return self.rendering_index - r_index

    def destroy(self):
        self.root_movie.destroy()
        self.root_movie = None
        self._root = None
        self.alive = False
        if self.lwf_unloader:
            self.lwf_unloader()

    def get_i_object_offset(self):
        self._i_object_offset += 1
        return self._i_object_offset

    def search_movie_instance(self, string):
        if isinstance(string, int):
            return self.search_movie_instance_by_instance_id(self.search_instance_id(string))
        return self._search_movie_instance(string)

    def _search_movie_instance(self, instance_name):
        if "." in instance_name:
            names = instance_name.split('.')
            if names[0] != self.data.strings[self._root_movie_string_id]:
                return None

            m = self.root_movie
            for i in range(1, len(names)):
                m = m.seach_movie_instance(names[i], False)
                if not m:
                    return None
            return m

        string_id = self.get_string_id(instance_name)
        if string_id == -1:
            return self.root_movie.search_movie_instance(instance_name, True)
        return self.search_movie_instance(string_id)

    def __getitem__(self, instance_name):
        return self.search_movie_instance(instance_name)

    def search_movie_instance_by_instance_id(self, inst_id):
        if inst_id < 0 or inst_id >= len(self._instances):
            return None
        obj = self._instances[inst_id]
        while obj:
            if obj.is_movie():
                return obj
            obj = obj.next_instance
        return None

    def search_button_instance(self, string):
        if isinstance(string, int):
            return self.search_button_instance_by_instance_id(self.search_instance_id(string))
        return self._search_movie_instance(string)

    def _search_button_instance(self, instance_name):
        if "." in instance_name:
            names = instance_name.split('.')
            if names[0] is not self.data.strings[self._root_movie_string_id]:
                return None

            m = self.root_movie
            for i in range(1, len(names)):
                if i == len(names) - 1:
                    return m.search_button_instance(names[i], False)
                else:
                    m = m.search_movie_instance(names[i], False)
                    if not m:
                        return None
            return None

        string_id = self.get_string_id(instance_name)
        if string_id == -1:
            return self.root_movie.search_button_instance(instance_name, True)
        return self.search_button_instance(string_id)

    def search_button_instance_by_instance_id(self, inst_id):
        if inst_id < 0 or inst_id >= len(self._instances):
            return None
        obj = self._instances[inst_id]
        while obj:
            if obj.is_button():
                return obj
            obj = obj.next_instance
        return None

    def get_instance(self, inst_id):
        if inst_id in self._instances:
            return self._instances[inst_id]
        return None

    def set_instance(self, inst_id, instance):
        self._instances[inst_id] = instance

    def get_program_object_constructor(self, program_object):
        if isinstance(program_object, str):
            program_object = self.search_program_object_id(program_object)
        return self._get_program_object_constructor(program_object)

    def _get_program_object_constructor(self, program_object_id):
        if program_object_id < 0 or program_object_id >= len(self.data.program_objects):
            return None
        return self._program_object_constructors[program_object_id]

    def set_program_object_constructor(self, program_object, program_object_constructor):
        if isinstance(program_object, str):
            program_object = self.search_program_object_id(program_object)
        self._set_program_object_constructor_by_id(program_object, program_object_constructor)

    def _set_program_object_constructor_by_id(self, program_object_id, program_object_constructor):
        if program_object_id < 0 or program_object_id >= len(self.data.program_objects):
            return
        self._program_object_constructors[program_object_id] = program_object_constructor

    def exec_movie_command(self):
        if len(self._movie_commands) == 0:
            return

        deletes = []
        i = 0
        for instance_names, command in self._movie_commands:
            available = True
            movie = self.root_movie
            for instance in instance_names:
                movie = movie.search_movie_instance(instance)
                if not movie:
                    available = False
                    break
            if available:
                command(movie)
                deletes.append(i)
            i += 1
        for delete in reversed(deletes):
            self._movie_commands.pop(delete)

    def set_movie_command(self, instance_names, cmd):
        self._movie_commands.append((instance_names, cmd))
        self.exec_movie_command()

    def search_attached_movie(self, attach_name):
        return self.root_movie.search_attached_movie(attach_name)

    def search_attached_lwf(self, attach_name):
        return self.root_movie.search_attached_lwf(attach_name)

    def add_allow_button(self, button_name):
        inst_id = self.search_instance_id(self.get_string_id(button_name))
        if inst_id < 0:
            return False

        self._allow_button_list[inst_id] = True
        return True

    def remove_allow_button(self, button_name):
        inst_id = self.search_instance_id(self.get_string_id(button_name))
        if inst_id < 0:
            return False
        if inst_id in self._allow_button_list:
            self._allow_button_list.pop(inst_id)
            return True
        return False

    def clear_allow_button(self):
        self._allow_button_list.clear()

    def add_deny_button(self, button_name):
        inst_id = self.search_instance_id(self.get_string_id(button_name))
        if inst_id < 0:
            return False
        self._deny_button_list[inst_id] = True
        return True

    def deny_all_buttons(self):
        for inst_id in range(len(self._instances)):
            self._deny_button_list[inst_id] = True

    def remove_deny_button(self, button_name):
        inst_id = self.search_instance_id(self.get_string_id(button_name))
        if inst_id < 0:
            return False
        if inst_id in self._deny_button_list:
            self._deny_button_list.pop(inst_id)
            return True
        return False

    def clear_deny_button(self):
        self._deny_button_list.clear()

    def disable_exec(self):
        self.is_exec_disabled = True
        self._executed_for_exec_disabled = False

    def enable_exec(self):
        self.is_exec_disabled = False

    def set_property_dirty(self):
        self.is_property_dirty = True
        if self.parent:
            self.parent.lwf.set_property_dirty()

    def add_exec_handler(self, exec_handler):
        hid = self.get_event_offset()
        self._exec_handlers.append((hid, exec_handler))
        return hid

    def remove_exec_handler(self, hid):
        if len(self._exec_handlers) == 0:
            return
        for eid, h in self._exec_handlers:
            if eid == hid:
                self._exec_handlers.remove((eid, h))

    def clear_exec_handler(self):
        self._exec_handlers.clear()

    def set_exec_handler(self, exec_handler):
        self.clear_exec_handler()
        self.add_exec_handler(exec_handler)

    def set_text(self, text_name, text):
        if text_name in self._text_dictionary:
            if self._text_dictionary[text_name][1] is not None:
                self._text_dictionary[text_name][1].set_text(text)
            self._text_dictionary[text_name][0] = text
        else:
            self._text_dictionary[text_name] = (text, None)

    def get_text(self, text_name):
        if text_name in self._text_dictionary:
            return self._text_dictionary[text_name][0]
        return ""

    def set_text_renderer(self, full_path, text_name, text, text_renderer):
        set_text = False
        full_name = full_path + '.' + text_name
        if full_name in self._text_dictionary:
            self._text_dictionary[full_name][1] = text_renderer
            if len(self._text_dictionary[full_name][0]) > 0:
                text_renderer.set_text(self._text_dictionary[full_name][0])
                set_text = True
        else:
            self._text_dictionary[full_name] = ("", text_renderer)

        if text_name in self._text_dictionary:
            self._text_dictionary[text_name][1] = text_renderer
            if not set_text and len(self._text_dictionary[text_name][0]) != 0:
                text_renderer.set_text(self._text_dictionary[text_name][0])
                set_text = True
        else:
            self._text_dictionary[text_name] = ("", text_renderer)

        if not set_text:
            text_renderer.set_text(text)

    def clear_text_renderer(self, text_name):
        if text_name in self._text_dictionary:
            self._text_dictionary[text_name][1] = None

    def set_texture_load_handler(self, h):
        self._texture_load_handler = h

    def get_texture_load_handler(self):
        return self._texture_load_handler

    def play_animation(self, animation_id, movie, button=None):
        i = 0
        animations = self.data.animations[animation_id]
        target = movie
        while True:
            case = animations[i]
            i += 1
            if case == Animation.END:
                return
            if case == Animation.PLAY:
                target.play()
                continue
            if case == Animation.STOP:
                target.stop()
                continue
            if case == Animation.NEXT_FRAME:
                target.next_frame()
                continue
            if case == Animation.PREV_FRAME:
                target.prev_frame()
                continue
            if case == Animation.GOTO_FRAME:
                target.goto_frame_internal(animations[i])
                i += 1
                continue
            if case == Animation.GOTO_LABEL:
                target.goto_frame(self.search_frame(target, animations[i]))
                i += 1
                continue
            if case == Animation.SET_TARGET:
                target = movie
                count = animations[i]
                i += 1
                if count == 0:
                    continue

                for j in range(0, count):
                    inst_id = animations[i]
                    i += 1
                    if inst_id == Animation.INSTANCE_TARGET_ROOT:
                        target = self.root_movie
                        continue
                    if inst_id == Animation.INSTANCE_TARGET_PARENT:
                        target = target.parent
                        if target is None:
                            target = self.root_movie
                        continue
                    target = target.search_movie_instance_by_instance_id(inst_id, False)
                    if target is None:
                        target = movie
                    continue
            if case == Animation.EVENT:
                event_id = animations[i]
                i += 1
                if self._event_handlers[event_id] is not None:
                    for h in self._event_handlers[event_id].values():
                        h(movie, button)
                continue
            if case == Animation.CALL:
                i += 1

    def get_instance_name_string_id(self, inst_id):
        if inst_id < 0 or inst_id >= len(self.data.instance_names):
            return -1
        return self.data.instance_names[inst_id].string_id

    def get_string_id(self, string):
        if string in self.data.string_map:
            return self.data.string_map[string]
        else:
            return -1

    def search_instance_id(self, string_id):
        if string_id < 0 or string_id >= len(self.data.strings):
            return -1
        if string_id in self.data.instance_name_map:
            return self.data.instance_name_map[string_id]
        else:
            return -1

    def search_frame(self, movie, string):
        if isinstance(string, str):
            string = self.get_string_id(string)
        return self._search_frame(movie, string)

    def _search_frame(self, movie, string_id):
        if string_id < 0 or string_id >= len(self.data.strings):
            return -1

        m = self.data.label_map[movie.object_id]
        if string_id in m:
            return m[string_id] + 1
        else:
            return -1

    def get_movie_labels(self, linkage_name):
        object_id = self.search_movie_linkage(self.get_string_id(linkage_name))
        if object_id < 0:
            return None
        return self.data.label_map[object_id]

    def search_movie_linkage(self, string_id):
        if string_id < 0 or string_id >= len(self.data.strings):
            return -1
        if string_id in self.data.movie_linkage_map:
            return self.data.movie_linkages[self.data.movie_linkage_map[string_id]].movie_id
        else:
            return -1

    def get_movie_linkage_name(self, movie_id):
        if movie_id in self.data.movie_linkage_name_map:
            return self.data.strings[self.data.movie_linkage_name_map[movie_id]]
        else:
            return ""

    def search_event_id(self, event):
        if isinstance(event, str):
            event = self.get_string_id(event)
        return self._search_event_id(event)

    def _search_event_id(self, event_id):
        if event_id < 0 or event_id >= len(self.data.strings):
            return -1
        if event_id in self.data.event_map:
            return self.data.event_map[event_id]
        else:
            return -1

    def search_program_object_id(self, program_object):
        if isinstance(program_object, str):
            program_object = self.get_string_id(program_object)
        return self._search_program_object_id(program_object)

    def _search_program_object_id(self, program_object_id):
        if program_object_id < 0 or program_object_id >= len(self.data.strings):
            return -1

        if program_object_id in self.data.program_object_map:
            return self.data.program_object_map[program_object_id]
        else:
            return -1

    def input_point(self, px, py):
        self.intercepted = False

        if not self.interactive:
            return None

        x, y = px, py

        self.point_x, self.point_y = x, y

        found = False
        button = self.button_head
        while button:
            if button.check_hit(x, y):
                if len(self._allow_button_list) != 0:
                    if button.instance_id not in self._allow_button_list:
                        if self.intercept_by_not_allow_or_deny_buttons:
                            self.intercepted = True
                            break
                        else:
                            continue
                elif len(self._deny_button_list) != 0:
                    if button.instance_id in self._deny_button_list:
                        if self.intercept_by_not_allow_or_deny_buttons:
                            self.intercepted = True
                            break
                        else:
                            continue

                found = True
                if self.focus != button:
                    if self.focus is not None:
                        self.focus.roll_out()
                    self.focus = button
                    self.focus.roll_over()
                break
            button = button.button_link
        if not found and self.focus:
            self.focus.roll_out()
            self.focus = None
        return self.focus

    def input_press(self):
        if not self.interactive:
            return
        self.pressing = True
        if self.focus:
            self.pressed = self.focus
            self.focus.press()

    def input_release(self):
        if not self.interactive:
            return
        self.pressing = False

        if self.focus and self.pressed == self.focus:
            self.focus.release()
            self.pressed = None

    def input_key_press(self, code):
        if not self.interactive:
            return

        button = self.button_head
        while button:
            button.key_press(code)
            button = button.button_link

    def init_event(self):
        self._event_handlers = []  # vector<EventHandlerList> | EventHandlerList → vector<pair<int, EventHandler>>
        for x in range(len(self.data.events)):
            self._event_handlers.append([])
        self._movie_event_handlers = []  # vector<MovieEventHandlers>
        for x in range(len(self.data.instance_names)):
            self._movie_event_handlers.append(MovieEventHandlers())
        self._button_event_handlers = []  # vector<ButtonEventHandlers>
        for x in range(len(self.data.instance_names)):
            self._button_event_handlers.append(ButtonEventHandlers())

    def get_event_offset(self):
        self._event_offset += 1
        return self._event_offset

    def add_event_handler(self, event, event_handler):
        if isinstance(event, str):
            return self._add_event_handler_by_name(event, event_handler)
        return self._add_event_handler_by_id(event, event_handler)

    def _add_event_handler_by_name(self, event_name, event_handler):
        event_id = self.search_event_id(event_name)
        if 0 <= event_id < len(self.data.events):
            eid = self.add_event_handler(event_id, event_handler)
        else:
            if event_name not in self._generic_event_handler_dictionary:
                self._generic_event_handler_dictionary[event_name] = []
            eid = self.get_event_offset()
            self._generic_event_handler_dictionary[event_name].append((eid, event_handler))
        return eid

    def _add_event_handler_by_id(self, event_id, event_handler):
        if event_id < 0 or event_id >= len(self.data.events):
            return -1
        eid = self.get_event_offset()
        self._event_handlers[event_id].append((eid, event_handler))
        return eid

    def remove_event_handler(self, event, eid):
        if eid < 0:
            return
        if isinstance(event, str):
            self._remove_event_handler_by_name(event, eid)
        else:
            self._remove_event_handler_by_id(event, eid)

    def _remove_event_handler_by_name(self, event_name, eid):
        event_id = self.search_event_id(event_name)
        if 0 <= event_id < len(self.data.events):
            self.remove_event_handler(event_id, eid)
        else:
            if event_name in self._generic_event_handler_dictionary:
                elist = self._generic_event_handler_dictionary[event_name]
                for geid, handler in elist:
                    if geid == eid:
                        elist.remove((geid, handler))

    def _remove_event_handler_by_id(self, event_id, eid):
        if event_id < 0 or event_id >= len(self.data.events):
            return
        elist = self._event_handlers[event_id]
        for geid, handler in elist:
            if geid == eid:
                elist.remove((geid, handler))

    def clear_event_handler(self, event):
        if isinstance(event, str):
            self._clear_event_handler_by_name(event)
        else:
            self._clear_event_handler_by_id(event)

    def _clear_event_handler_by_name(self, event_name):
        event_id = self.search_event_id(event_name)
        if 0 <= event_id < len(self.data.events):
            self.clear_event_handler(event_id)
        else:
            self._generic_event_handler_dictionary.pop(event_name)

    def _clear_event_handler_by_id(self, event_id):
        if event_id < 0 or event_id >= len(self.data.events):
            return
        self._event_handlers[event_id].clear()

    def set_event_handler(self, event, event_handler):
        if isinstance(event, str):
            event = self.search_event_id(event)
        return self._set_event_handler(event, event_handler)

    def _set_event_handler(self, event_id, event_handler):
        self.clear_event_handler(event_id)
        return self.add_event_handler(event_id, event_handler)

    def dispatch_event(self, event_name, m=None, b=None):
        if m is None:
            m = self.root_movie
        event_id = self.search_event_id(event_name)
        elist = None
        if 0 <= event_id < len(self.data.events):
            elist = self._event_handlers[event_id]
        else:
            if event_name in self._generic_event_handler_dictionary:
                elist = self._generic_event_handler_dictionary[event_name]
        if elist and len(elist) != 0:
            for eid, handler in elist:
                handler(m, b)

    def get_movie_event_handlers(self, m):
        if len(self._movie_event_handlers_by_full_name) != 0:
            full_name = m.get_full_name()
            if len(full_name) != 0:
                if full_name in self._movie_event_handlers_by_full_name:
                    return self._movie_event_handlers_by_full_name[full_name]

        inst_id = m.instance_id
        if inst_id < 0 or inst_id >= len(self.data.instance_names):
            return None
        return self._movie_event_handlers[inst_id]

    def add_movie_event_handler(self, instance, h):
        if isinstance(instance, str):
            return self._add_movie_event_handler_by_name(instance, h)
        return self._add_movie_event_handler_by_id(instance, h)

    def _add_movie_event_handler_by_name(self, instance_name, h):
        if len(h) == 0:
            return -1

        inst_id = self.search_instance_id(self.get_string_id(instance_name))
        if inst_id >= 0:
            return self.add_movie_event_handler(inst_id, h)

        if "." not in instance_name:
            return -1

        if instance_name not in self._movie_event_handlers_by_full_name:
            self._movie_event_handlers_by_full_name[instance_name] = MovieEventHandlers()
        handlers = self._movie_event_handlers_by_full_name[instance_name]

        hid = self.get_event_offset()
        handlers.add(hid, h)

        m = self.search_movie_instance(inst_id)
        if m:
            m.add_handlers(handlers)
        return hid

    def _add_movie_event_handler_by_id(self, inst_id, h):
        if inst_id < 0 or inst_id >= len(self.data.instance_names):
            return -1

        hid = self.get_event_offset()
        self._movie_event_handlers[inst_id].add(hid, h)

        m = self.search_movie_instance_by_instance_id(inst_id)
        if m:
            m.add_handlers(self._movie_event_handlers[inst_id])
        return hid

    def remove_movie_event_handler(self, instance, hid):
        if isinstance(instance, str):
            self._remove_movie_event_handler_by_name(instance, hid)
        else:
            self._remove_movie_event_handler_by_id(instance, hid)

    def _remove_movie_event_handler_by_name(self, instance_name, hid):
        inst_id = self.search_instance_id(self.get_string_id(instance_name))
        if inst_id >= 0:
            self._remove_movie_event_handler_by_id(inst_id, hid)
            return

        if len(self._movie_event_handlers_by_full_name) == 0:
            return

        if instance_name not in self._movie_event_handlers_by_full_name:
            return
        self._movie_event_handlers_by_full_name[instance_name].remove(hid)

        m = self.search_movie_instance(instance_name)
        if m:
            m.remove_movie_event_handler(hid)

    def _remove_movie_event_handler_by_id(self, inst_id, hid):
        if inst_id < 0 or inst_id >= len(self.data.instance_names):
            return

        self._movie_event_handlers[inst_id].remove(hid)

        m = self.search_movie_instance_by_instance_id(inst_id)
        if m:
            m.remove_movie_event_handler(hid)

    def clear_movie_event_handler(self, instance, htype=None):
        if isinstance(instance, str):
            if htype is None:
                self._clear_movie_event_handler_by_name(instance)
            else:
                self._clear_movie_event_handler_by_name_and_type(instance, htype)
        else:
            if htype is None:
                self._clear_movie_event_handler_by_id(instance)
            else:
                self._clear_movie_event_handler_by_id_and_type(instance, htype)

    def _clear_movie_event_handler_by_name(self, instance_name):
        inst_id = self.search_instance_id(self.get_string_id(instance_name))
        if inst_id >= 0:
            self._clear_movie_event_handler_by_id(inst_id)
            return

        if len(self._movie_event_handlers_by_full_name) == 0:
            return

        if instance_name in self._movie_event_handlers_by_full_name:
            self._movie_event_handlers_by_full_name[instance_name].clear()

        m = self.search_movie_instance(instance_name)
        if m:
            m.clear_movie_event_handler()

    def _clear_movie_event_handler_by_name_and_type(self, instance_name, htype):
        inst_id = self.search_instance_id(self.get_string_id(instance_name))

        if inst_id >= 0:
            self._clear_movie_event_handler_by_id_and_type(inst_id, htype)
            return

        if len(self._movie_event_handlers_by_full_name) == 0:
            return

        if instance_name in self._movie_event_handlers_by_full_name:
            self._movie_event_handlers_by_full_name[instance_name].clear(htype)

        m = self.search_movie_instance(instance_name)
        if m:
            m.clear_event_handler(htype)

    def _clear_movie_event_handler_by_id(self, inst_id):
        if inst_id < 0 or inst_id >= len(self.data.instance_names):
            return

        self._movie_event_handlers[inst_id].clear()

        m = self.search_movie_instance_by_instance_id(inst_id)
        if m:
            m.clear_movie_event_handler()

    def _clear_movie_event_handler_by_id_and_type(self, inst_id, htype):
        if inst_id < 0 or inst_id >= len(self.data.instance_names):
            return

        self._movie_event_handlers[inst_id].clear(htype)

        m = self.search_movie_instance_by_instance_id(inst_id)
        if m:
            m.clear_event_handler(htype)

    def set_movie_event_handler(self, instance, h):
        self.clear_movie_event_handler(instance)
        self.add_movie_event_handler(instance, h)

    def get_button_event_handlers(self, b):
        if len(self._button_event_handlers_by_full_name) != 0:
            full_name = b.get_full_name()
            if len(full_name) != 0:
                if full_name in self._button_event_handlers_by_full_name:
                    return self._button_event_handlers_by_full_name[full_name]

        inst_id = b.instance_id
        if inst_id < 0 or inst_id >= len(self.data.instance_names):
            return None
        return self._button_event_handlers[inst_id]

    def add_button_event_handler(self, instance, h, kh):
        if isinstance(instance, str):
            return self._add_button_event_handler_by_name(instance, h, kh)
        return self._add_button_event_handler_by_id(instance, h, kh)

    def _add_button_event_handler_by_name(self, instance_name, h, kh):
        if len(h) == 0:
            return -1

        inst_id = self.search_instance_id(self.get_string_id(instance_name))
        if inst_id >= 0:
            self._add_button_event_handler_by_id(inst_id, h, kh)

        if '.' not in instance_name:
            return -1

        if instance_name not in self._button_event_handlers_by_full_name:
            self._button_event_handlers_by_full_name[instance_name] = ButtonEventHandlers()

        hid = self.get_event_offset()
        self._button_event_handlers_by_full_name[instance_name].add(hid, h, kh)

        b = self.search_button_instance(instance_name)
        if b:
            b.add_handlers(self._button_event_handlers_by_full_name[instance_name])
        return hid

    def _add_button_event_handler_by_id(self, inst_id, h, kh):
        if inst_id < 0 or inst_id >= len(self.data.instance_names):
            return -1

        hid = self.get_event_offset()
        self._button_event_handlers[inst_id].add(hid, h, kh)

        b = self.search_button_instance_by_instance_id(inst_id)
        if b:
            b.add_handlers(self._button_event_handlers[inst_id])
        return hid

    def remove_button_event_handler(self, instance, hid):
        if isinstance(instance, str):
            self._remove_button_event_handler_by_name(instance, hid)
        else:
            self._remove_button_event_handler_by_id(instance, hid)

    def _remove_button_event_handler_by_name(self, instance_name, hid):
        inst_id = self.search_instance_id(self.get_string_id(instance_name))
        if inst_id >= 0:
            self._remove_button_event_handler_by_id(inst_id, hid)
            return

        if len(self._button_event_handlers_by_full_name) == 0:
            return

        if instance_name not in self._button_event_handlers_by_full_name:
            return

        self._button_event_handlers_by_full_name[instance_name].remove(hid)

        b = self.search_button_instance(instance_name)
        if b:
            b.remove_button_event_handler(hid)

    def _remove_button_event_handler_by_id(self, inst_id, hid):
        if inst_id < 0 or inst_id >= len(self.data.instance_names):
            return -1

        self._button_event_handlers[inst_id].remove(hid)

        b = self.search_button_instance_by_instance_id(inst_id)
        if b:
            b.remove_button_event_handler(hid)
        return hid

    def clear_button_event_handler(self, instance, htype=None):
        if isinstance(instance, str):
            if htype is None:
                self._clear_button_event_handler_by_name(instance)
            else:
                self._clear_button_event_handler_by_name_and_type(instance, htype)
        else:
            if htype is None:
                self._clear_button_event_handler_by_id(instance)
            else:
                self._clear_button_event_handler_by_id_and_type(instance, htype)

    def _clear_button_event_handler_by_name(self, instance_name):
        inst_id = self.search_instance_id(self.get_string_id(instance_name))

        if inst_id >= 0:
            self._clear_button_event_handler_by_id(inst_id)
            return

        if len(self._button_event_handlers_by_full_name) == 0:
            return

        if instance_name not in self._button_event_handlers_by_full_name:
            return

        self._button_event_handlers_by_full_name[instance_name].clear()

        b = self.search_button_instance(instance_name)
        if b:
            b.clear_button_event_handler()

    def _clear_button_event_handler_by_name_and_type(self, instance_name, htype):
        inst_id = self.search_instance_id(self.get_string_id(instance_name))

        if inst_id >= 0:
            self._clear_button_event_handler_by_id_and_type(inst_id, htype)
            return

        if len(self._button_event_handlers_by_full_name) == 0:
            return

        if instance_name not in self._button_event_handlers_by_full_name:
            return

        self._button_event_handlers_by_full_name[instance_name].clear(htype)

        b = self.search_button_instance(instance_name)
        if b:
            b.clear_event_handler(htype)

    def _clear_button_event_handler_by_id(self, inst_id):
        if inst_id < 0 or inst_id >= len(self.data.instance_names):
            return

        self._button_event_handlers[inst_id].clear()

        b = self.search_button_instance_by_instance_id(inst_id)
        if b:
            b.clear_button_event_handler()

    def _clear_button_event_handler_by_id_and_type(self, inst_id, htype):
        if inst_id < 0 or inst_id >= len(self.data.instance_names):
            return

        self._button_event_handlers[inst_id].clear(htype)

        b = self.search_button_instance_by_instance_id(inst_id)
        if b:
            b.clear_event_handler(htype)

    def set_button_event_handler(self, instance, h, kh):
        self.clear_button_event_handler(instance)
        self.add_button_event_handler(instance, h, kh)

    def clear_all_event_handlers(self):
        self._event_handlers.clear()
        self._movie_event_handlers.clear()
        self._button_event_handlers.clear()
        self.init_event()
        self.inspect(lambda o, x, y, z: o.clear_all_event_handler(), 0, 0, 0)
