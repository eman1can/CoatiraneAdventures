__all__ = ('TextureFragmentCompat',)


class TextureFragmentCompat:
    def __init__(self):
        self.string_id = 0
        self.texture_id = 0
        self.rotated = 0
        self.x = 0
        self.y = 0
        self.u = 0
        self.v = 0
        self.w = 0
        self.h = 0

    def convert(self, fragment_class):
        f = fragment_class()
        f.string_id = self.string_id
        f.texture_id = self.texture_id
        f.rotated = self.rotated
        f.x = self.x
        f.y = self.y
        f.u = self.u
        f.v = self.v
        f.w = self.w
        f.h = self.h
        f.ow = self.w
        f.oh = self.h
        return f

    def __str__(self):
        return f"Texture Fragment Compat <String Id: {self.string_id}, Texture Id: {self.texture_id}, Rotated: {self.rotated}, X: {self.x}, Y: {self.y}, U: {self.u}, V: {self.v}, W: {self.w}, H: {self.h}>"
