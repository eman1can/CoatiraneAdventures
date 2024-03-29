__all__ = ('GraphicObject',)


class GraphicObject:
    BITMAP = 0
    BITMAP_EX = 1
    TEXT = 2
    GRAPHIC_OBJECT_MAX = 3

    def __init__(self):
        self.graphic_object_type = 0
        self.graphic_object_id = 0

    def __str__(self):
        return f"Graphic Object <Object Type: {'Bitmap' if self.graphic_object_type == GraphicObject.BITMAP else 'Bitmap Ex' if self.graphic_object_type == GraphicObject.BITMAP_EX else 'Text'}, Object Id: {self.graphic_object_id}>"
