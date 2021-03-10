__all__ = ('Translate',)


class Translate:
    def __init__(self):
        self.translate_x = 0.0
        self.translate_y = 0.0

    def __str__(self):
        return f"Translate <X: {self.translate_x}, Y: {self.translate_y}>"
