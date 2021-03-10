__all__ = ('TextureReplacement',)

from . import Texture


class TextureReplacement(Texture):
    def __init__(self, fname, fmt, w, h, s):
        super().__init__()
        self.filename = fname
        self.format = fmt
        self.width = w
        self.height = h
        self.scale = s

    def get_filename(self, data):
        return self.filename

    def __str__(self):
        return f"Texture Replacement <{super().__str__()}>"
