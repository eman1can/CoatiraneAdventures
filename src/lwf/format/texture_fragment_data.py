__all__ = ('TextureFragment',)


class TextureFragment:
    def __init__(self):
        self.filename = None
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

        self.vertices = None

    def init(self, texture):
        x1, y1 = self.x + self.w, self.y + self.h

        if not self.rotated:
            u0 = self.u / texture.width
            v0 = self.v / texture.height
            u1 = (self.u + self.w) / texture.width
            v1 = (self.v + self.h) / texture.height

            self.vertices = [x1, self.y, u1, v0, x1, y1, u1, v1, self.x, self.y, u0, v0, self.x, y1, u0, v1]
        else:
            u0 = self.u / texture.width
            v0 = self.v / texture.height
            u1 = (self.u + self.h) / texture.width
            v1 = (self.v + self.w) / texture.height

            self.vertices = [x1, self.y, u1, v1, x1, y1, u0, v1, self.x, self.y, u1, v0, self.x, y1, u0, v0]

    def __str__(self):
        return f"TextureFragment <Filename: {self.filename}, Texture Id: {self.texture_id}, Rotated: {self.rotated}, X: {self.x}, Y: {self.y}, U: {self.u}, V: {self.v}, W: {self.w}, H: {self.h}, OW: {self.ow}, OH: {self.oh}>"
