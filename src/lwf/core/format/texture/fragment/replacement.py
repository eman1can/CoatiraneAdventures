__all__ = ('TextureFragmentReplacement',)

from . import TextureFragment


class TextureFragmentReplacement(TextureFragment):
    def __init__(self, fname, texId, rot, tx, ty, tu, tv, tw, th, tow, toh):
        super().__init__()
        self.filename = fname
        self.texture_id = texId
        self.rotated = rot
        self.x = tx
        self.y = ty
        self.u = tu
        self.v = tv
        self.w = tw
        self.h = th
        self.ow = tow
        self.oh = toh

    def get_filename(self, data):
        return self.filename

    def __str__(self):
        return f"Texture Fragment Replacement <{super().__str__()}>"
