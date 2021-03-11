__all__ = ('BitmapClip',)

from math import cos, radians, sin

from .bitmap import Bitmap
from ..type import Matrix


class BitmapClip(Bitmap):
    def __init__(self, lwf, p, obj_id):
        super().__init__(lwf, p, obj_id)
        self.depth = -1
        self.visible = True
        self.name = None
        self.width = 0.0
        self.height = 0.0
        self.reg_x = 0.0
        self.reg_y = 0.0
        self.x = 0.0
        self.y = 0.0
        self.scale_x = 0.0
        self.scale_y = 0.0
        self.rotation = 0.0
        self.alpha = 1.0
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.original_width = 0.0
        self.original_height = 0.0

        data = lwf.data.bitmaps[obj_id]
        fragment = lwf.data.texture_fragments[data.texture_fragment_id]
        tex_data = lwf.data.textures[fragment.texture_id]
        self.width = fragment.w / tex_data.scale
        self.height = fragment.h / tex_data.scale
        self.offset_x = fragment.x
        self.offset_y = fragment.y
        self.original_width = fragment.ow
        self.original_height = fragment.oh

        self._scale_x = self.scale_x
        self._scale_y = self.scale_y
        self._rotation = self.rotation
        self._cos = 1.0
        self._sin = 0.0
        self._matrix = Matrix()

    def exec(self, m_id=0, c_id=0):
        pass

    def update(self, m, c):
        dirty = False
        if self.rotation != self._rotation:
            self._rotation = self.rotation
            radian = radians(self._rotation)
            self._cos = cos(radian)
            self._sin = sin(radian)
            dirty = True
        if dirty or self._scale_x != self.scale_x or self._scale_y != self.scale_y:
            self._scale_x = self.scale_x
            self._scale_y = self.scale_y
            self._matrix.scale_x = self._scale_x * self._cos
            self._matrix.skew_1 = self._scale_x * self._sin
            self._matrix.skew_0 = self._scale_y * -self._sin
            self._matrix.scale_y = self._scale_y * self._cos

        self._matrix.translate_x = self.x - self.reg_x
        self._matrix.translate_y = self.y - self.reg_y

        self.matrix.scale_x = m.scale_x * self._matrix.scale_x + m.skew_0 * self._matrix.skew_1
        self.matrix.skew_0 = m.scale_x * self._matrix.skew_0 + m.skew_0 * self._matrix.scale_y
        self.matrix.translate_x = m.scale_x * self.x + m.skew_0 * self.y + m.translate_x + m.scale_x * self.reg_x + m.skew_0 * self.reg_y + self.matrix.scale_x * -self.reg_x + self.matrix.skew_0 * -self.reg_y
        self.matrix.skew_1 = m.skew_1 * self._matrix.scale_x + m.scale_y * self._matrix.skew_1
        self.matrix.scale_y = m.skew_1 * self._matrix.skew_0 + m.scale_y * self._matrix.scale_y
        self.matrix.translate_y = m.skew_1 * self.x + m.scale_y * self.y + m.translate_y + m.skew_1 * self.reg_x + m.scale_y * self.reg_y + self.matrix.skew_1 * -self.reg_x + self.matrix.scale_y * -self.reg_y

        self.color_transform.set(c)
        self.color_transform.multi.alpha *= self.alpha

        self.lwf.render_object()

    def detach_from_parent(self):
        if self.parent:
            self.parent.detach_bitmap(self.depth)
            self.parent = None

    def is_bitmap_clip(self):
        return True

    def __str__(self):
        return f"Bitmap Clip <>"
