__all__ = ('BitmapEx',)

from .object import Object
from ..format import Object as ObjectType


class BitmapEx(Object):
    def __init__(self, lwf, p, obj_id):
        super().__init__(lwf, p, ObjectType.BITMAP_EX, obj_id)

        self.data_matrix_id = lwf.data.bitmap_exs[obj_id].matrix_id
        self.renderer = lwf.renderer_factory.construct_bitmap_ex(lwf, obj_id, self)

    def __str__(self):
        return f"Bitmap Ex <>"
