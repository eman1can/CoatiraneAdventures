__all__ = ('BitmapEx',)


class BitmapEx:
    class Attribute:
        REPEAT_S = (1 << 0)
        REPEAT_T = (1 << 1)

    def __init__(self):
        self.matrix_id = 0
        self.texture_fragment_id = 0
        self.attribute = 0
        self.u = 0.0
        self.v = 0.0
        self.w = 0.0
        self.h = 0.0

    def __str__(self):
        return f"Bitmap Ex <Matrix Id: {self.matrix_id}, TF Id: {self.texture_fragment_id}, Attribute: {'Repeat_S'if self.attribute == BitmapEx.Attribute.REPEAT_S else 'Repeat_T'}, U: {self.u}, V: {self.v}, W: {self.w}, H: {self.h}>"
