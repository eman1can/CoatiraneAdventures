__all__ = ('TextureFragmentBase',)


class TextureFragmentBase:
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
        self.ow = 0
        self.oh = 0

    def __str__(self):
        return f"Texture Fragment Base <String Id: {self.string_id}, Texture Id: {self.texture_id}, Rotated: {self.rotated}, X: {self.x}, Y: {self.y}, U: {self.u}, V: {self.v}, W: {self.w}, H: {self.h}, OW: {self.ow}, OH: {self.oh}>"
