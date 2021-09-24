__all__ = ('Object',)

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


TO_STRING = {
    BUTTON: 'Button',
    GRAPHIC: 'Graphic',
    MOVIE: 'Movie',
    BITMAP: 'Bitmap',
    BITMAP_EX: 'Bitmap Ex',
    TEXT: 'Text',
    PARTICLE: 'Particle',
    PROGRAM_OBJECT: 'Program Object',
    ATTACHED_MOVIE: 'Attached Movie'
}


class Object:
    def __init__(self):
        self.object_type = 0
        self.object_id = 0

    def __str__(self):
        obj_type = TO_STRING[self.object_type]
        return f"Object <Type: {obj_type}, Id: {self.object_id}>"
