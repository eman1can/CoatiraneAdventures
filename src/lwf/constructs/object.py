__all__ = ('Object',)

from lwf.format.object_data import ATTACHED_MOVIE, BUTTON, MOVIE, PARTICLE, PROGRAM_OBJECT, TEXT
from lwf.modules.color_transform import ColorTransform
from lwf.modules.matrix import Matrix
from lwf.modules.utility import Utility

class Object:
    def __init__(self, *args):
        self.lwf = None
        self.parent = None

        self.type = 0
        self.exec_count = 0
        self.object_id = 0
        self.matrix_id = 0
        self.color_transform_id = 0

        self.matrix = Matrix()
        self.data_matrix_id = 0
        self.color_transform = ColorTransform()

        self.renderer = None

        self.matrix_id_changed = False
        self.color_transform_id_changed = False
        self.updated = False

        # Load Actual Data
        if len(args) > 0:
            l, p, t, obj_id = args
            self.lwf = l
            self.parent = p
            self.type = t
            self.exec_count = 0
            self.object_id = obj_id
            self.matrix_id = -1
            self.color_transform_id = -1
            self.data_matrix_id = -1
            self.matrix_id_changed = True
            self.color_transform_id_changed = True
            self.updated = False

            self.matrix.set(0, 0, 0, 0, 0, 0)
            self.color_transform.set(0, 0, 0, 0, 0, 0, 0, 0)

    def exec(self, m_id=0, c_id=0):
        if self.matrix_id != m_id:
            self.matrix_id_changed = True
            self.matrix_id = m_id
        if self.color_transform_id != c_id:
            self.color_transform_id_changed = True
            self.color_transform_id = c_id

    def update(self, m, c):
        self.updated = True
        if m:
            Utility.calc_matrix(self.lwf, self.matrix, m, self.data_matrix_id)
            self.matrix_id_changed = False
        if c:
            Utility.copy_color_transform(self.color_transform, c)
            self.color_transform_id_changed = False
        self.lwf.render_object()

    def render(self, v, r_offset):
        if self.renderer:
            r_index = self.lwf.rendering_index
            r_index_offsetted = self.lwf.rendering_index_offsetted
            r_count = self.lwf.rendering_count
            if r_offset != -2147483648:
                r_index = r_index_offsetted - r_offset + r_count
            self.renderer.render(self.matrix, self.color_transform, r_index, r_count, v)
        self.lwf.render_object()

    def inspect(self, inspector, hierarchy, depth, r_offset):
        r_index = self.lwf.renderingIndex
        r_index_offsetted = self.lwf.rendering_index_offsetted
        r_count = self.lwf.renderingCount
        if r_offset != -2147483648:
            r_index = r_index_offsetted + r_offset + r_count
        inspector(self, hierarchy, depth, r_index)
        self.lwf.render_object()

    def destroy(self):
        if self.renderer:
            self.renderer.destruct()
            self.renderer = None

    def clear_all_event_handler(self):
        pass

    def is_button(self):
        return self.type == BUTTON

    def is_movie(self):
        return self.type == MOVIE or self.type == ATTACHED_MOVIE

    def is_particle(self):
        return self.type == PARTICLE

    def is_program_object(self):
        return self.type == PROGRAM_OBJECT

    def is_text(self):
        return self.type == TEXT

    def is_bitmap_clip(self):
        return False