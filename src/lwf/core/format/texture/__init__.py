__all__ = ('TextureBase', 'Texture', 'TextureFragmentBase', 'TextureFragment', 'TextureFragmentCompat', 'TextureFragmentReplacement',)

from .base import TextureBase
from .fragment import TextureFragmentBase, TextureFragment, TextureFragmentCompat, convert_filename
from .fragment.replacement import TextureFragmentReplacement


class Texture(TextureBase):
    def __init__(self, texture_base=None):
        super().__init__()
        self.filename = None

        if texture_base is not None:
            self.string_id = texture_base.string_id
            self.format = texture_base.format
            self.width = texture_base.width
            self.height = texture_base.height
            self.scale = texture_base.scale

    def set_filename(self, data):
        self.filename = convert_filename(data, self.string_id)

    def get_filename(self, data):
        return data.strings[self.string_id]

    def __str__(self):
        return f"Texture <Filename: {self.filename}, {super().__str__()}>"


