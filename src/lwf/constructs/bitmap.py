__all__ = ('Bitmap',)

from .object import Object
from ..format.object_data import BITMAP


class Bitmap(Object):
    def __init__(self, lwf, parent, type_id, obj_id):
        super().__init__(lwf, parent, type_id, obj_id)

        if type_id == BITMAP:
            bitmap = self.lwf.data.bitmaps[obj_id]
        else:
            bitmap = self.lwf.data.bitmap_exs[obj_id]
        self.data_matrix_id = bitmap.matrix_id
        self.renderer = self.lwf.renderer_factory.construct_bitmap(self.lwf, obj_id, bitmap.texture_fragment_id)
        del bitmap

    def __str__(self):
        return f"Bitmap - {self.object_id} - <{self.data_matrix_id}>"
