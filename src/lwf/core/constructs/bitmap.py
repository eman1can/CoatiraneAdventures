__all__ = ('Bitmap',)

from .object import Object
from ..format import Object as ObjectType


class Bitmap(Object):
    def __init__(self, lwf, parent, obj_id):
        super().__init__(lwf, parent, ObjectType.BITMAP, obj_id)

        self.data_matrix_id = lwf.data.bitmaps[obj_id].matrix_id
        self.renderer = lwf.renderer_factory.construct_bitmap(lwf, obj_id, self)

    def __str__(self):
        return f"Bitmap <>"
