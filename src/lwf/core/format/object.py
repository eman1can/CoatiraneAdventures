__all__ = ('Object',)


class Object:
    BUTTON = 0
    GRAPHIC = 1
    MOVIE = 2
    BITMAP = 3
    BITMAP_EX = 4
    TEXT = 5
    PARTICLE = 6
    PROGRAM_OBJECT = 7
    ATTACHED_MOVIE = 8
    OBJECT_MAX = 9

    def __init__(self):
        self.object_type = 0
        self.object_id = 0

    def __str__(self):
        obj_type = None
        if self.object_type == Object.BUTTON:
            obj_type = 'Button'
        elif self.object_type == Object.GRAPHIC:
            obj_type = 'Graphic'
        elif self.object_type == Object.MOVIE:
            obj_type = 'Movie'
        elif self.object_type == Object.BITMAP:
            obj_type = 'Bitmap'
        elif self.object_type == Object.BITMAP_EX:
            obj_type = 'Bitmap Ex'
        elif self.object_type == Object.TEXT:
            obj_type = 'Text'
        elif self.object_type == Object.PARTICLE:
            obj_type = 'Particle'
        elif self.object_type == Object.PROGRAM_OBJECT:
            obj_type = 'Program Object'
        else:
            obj_type = 'Attached Movie'
        return f"Object <Type: {obj_type}, Id: {self.object_id}>"
