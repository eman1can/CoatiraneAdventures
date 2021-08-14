__all__ = ('Property',)

from math import cos, radians, sin

from lwf.modules.color_transform import ColorTransform
from lwf.modules.matrix import Matrix


class Property:
    def __init__(self):
        self.matrix = Matrix()
        self.color_transform = ColorTransform()

        self.rendering_offset = 0

        self.has_matrix = False
        self.has_color_transform = False
        self.has_rendering_offset = False

        self.scale_x = 1.0
        self.scale_y = 1.0
        self.rotation = 0.0

        self.is_dirty = False

        self.clear_rendering_offset()

    def clear(self):
        self.scale_x = 1
        self.scale_y = 1
        self.rotation = 0
        self.matrix.clear()
        self.color_transform.clear()
        if self.has_matrix or self.has_color_transform:
            self.is_dirty = True
            self.has_matrix = False
            self.has_color_transform = False
        self.clear_rendering_offset()

    def move(self, x, y):
        self.matrix.translate_x += x
        self.matrix.translate_y -= y
        self.has_matrix = True
        self.is_dirty = True

    def move_to(self, x, y):
        self.matrix.translate_x = x
        self.matrix.translate_y = -y
        self.has_matrix = True
        self.is_dirty = True

    def rotate(self, degree):
        self.rotate_to(self.rotation + degree)

    def rotate_to(self, degree):
        self.rotation = degree
        self._set_scale_and_rotation()

    def scale(self, x, y):
        self.scale_x *= x
        self.scale_y *= y
        self._set_scale_and_rotation()

    def scale_to(self, x, y):
        self.scale_x = x
        self.scale_y = y
        self._set_scale_and_rotation()

    def _set_scale_and_rotation(self):
        radian = radians(self.rotation)
        c = cos(radian)
        s = sin(radian)
        self.matrix.scale_x = self.scale_x * c
        self.matrix.skew_0 = self.scale_y * -s
        self.matrix.skew_1 = self.scale_x * s
        self.matrix.scale_y = self.scale_y * c
        self.has_matrix = True
        self.is_dirty = True

    def set_matrix(self, m, s_x=1, s_y=1, r=0):
        self.matrix.set(m)
        self.scale_x = s_x
        self.scale_y = s_y
        self.rotation = r
        self.has_matrix = True
        self.is_dirty = True

    def set_alpha(self, alpha):
        self.color_transform.c[4] = alpha
        self.has_color_transform = True
        self.is_dirty = True

    def set_red(self, red):
        self.color_transform.c[0] = red
        self.has_color_transform = True
        self.is_dirty = True

    def set_green(self, green):
        self.color_transform.c[1] = green
        self.has_color_transform = True
        self.is_dirty = True

    def set_blue(self, blue):
        self.color_transform.c[2] = blue
        self.has_color_transform = True
        self.is_dirty = True

    def set_color_transform(self, c):
        self.color_transform.set(*c.c)
        self.has_color_transform = True
        self.is_dirty = True

    def set_rendering_offset(self, r_offset):
        self.rendering_offset = r_offset

    def clear_rendering_offset(self):
        self.rendering_offset = -2147483648
        self.has_rendering_offset = False
