__all__ = ('TextureBase',)


class TextureBase:
    def __init__(self):
        self.string_id = 0
        self.format = 0
        self.width = 0
        self.height = 0
        self.scale = 0.0

    def __str__(self):
        return f"Texture Base <String Id: {self.string_id}, Format: {self.format}, Width: {self.width}, Height: {self.height}, Scale: {self.scale}>"
