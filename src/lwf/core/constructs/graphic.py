__all__ = ('Graphic',)

from .object import Object
from .bitmap import Bitmap
from .bitmap_ex import BitmapEx
from .text import Text
from ..format import Object as ObjectType, GraphicObject as GraphicType


class Graphic(Object):
    def __init__(self, l, p, obj_id):
        super().__init__(l, p, ObjectType.GRAPHIC, obj_id)

        self.display_list = []

        data = self.lwf.data.graphics[obj_id]
        n = data.graphic_objects
        graphic_objects = self.lwf.data.graphic_objects
        for index in range(0, n):
            g_obj = graphic_objects[data.grapic_object_id + index]
            graphic_object_id = g_obj.graphic_object_id

            if graphic_object_id == -1:
                continue

            if g_obj.graphic_object_type == GraphicType.BITMAP:
                obj = Bitmap(self.lwf, self.parent, graphic_object_id)
            elif g_obj.graphic_object_type == GraphicType.BITMAP_EX:
                obj = BitmapEx(self.lwf, self.parent, graphic_object_id)
            else:
                obj = Text(self.lwf, self.parent, graphic_object_id)

            obj.exec()
            self.display_list.append(obj)

    def update(self, m, c):
        for obj in self.display_list:
            obj.update(m, c)

    def render(self, v, r_offset):
        if not v:
            return

        for obj in self.display_list:
            obj.render(v, r_offset)

    def destroy(self):
        for obj in self.display_list:
            obj.destroy()
        self.display_list.clear()
