__all__ = ('Graphic', 'GraphicObject')

from .object import GraphicObject


class Graphic:
    def __init__(self):
        self.graphic_object_id = 0
        self.graphic_objects = 0

    def __str__(self):
        return f"Graphic <Object Id: {self.graphic_object_id}, Objects: {self.graphic_objects}>"
