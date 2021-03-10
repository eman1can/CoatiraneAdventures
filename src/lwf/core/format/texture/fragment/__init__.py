__all__ = ('TextureFragmentBase', 'TextureFragment', 'TextureFragmentCompat', 'convert_filename')

from .base import TextureFragmentBase
from .compat import TextureFragmentCompat


def convert_filename(data, string_id):
    s = data.strings[string_id]
    pos = s.rindex('.')
    if pos > 0:
        return s[0:pos]
    else:
        return s


class TextureFragment(TextureFragmentBase):
    def __init__(self, fragment_base=None):
        super().__init__()
        self.filename = None  # string

        if fragment_base is not None:
            self.string_id = fragment_base.string_id
            self.texture_id = fragment_base.texture_id
            self.rotated = fragment_base.rotated
            self.x = fragment_base.x
            self.y = fragment_base.y
            self.u = fragment_base.u
            self.v = fragment_base.v
            self.w = fragment_base.w
            self.h = fragment_base.h
            self.ow = fragment_base.ow
            self.oh = fragment_base.oh

    def set_filename(self, data):
        self.filename = convert_filename(data, self.string_id)

    def get_filename(self, data):
        return data.strings[self.string_id]

    def __str__(self):
        return f"Texture Fragment <Filename: {self.filename}, {super().__str__()}>"
