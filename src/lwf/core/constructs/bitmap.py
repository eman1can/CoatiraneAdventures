__all__ = ('Bitmap',)

from .object import Object
from ..format.object import Object as ObjectType


class Bitmap(Object):
    def __init__(self, lwf, parent, obj_id):
        super().__init__(lwf, parent, ObjectType.BITMAP, obj_id)

        self.data_matrix_id = lwf.data.bitmaps[obj_id].matrix_id
        self.renderer = lwf.renderer_factory.construct_bitmap(lwf, obj_id, self)

    def is_construct(self):
        return True

    def is_bitmap(self):
        return True

    def __str__(self):
        return f"BitmapConstruct <{self.data_matrix_id}>"
