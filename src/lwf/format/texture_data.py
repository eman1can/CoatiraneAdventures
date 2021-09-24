__all__ = ('Texture',)


class Texture:
    def __init__(self):
        self.filename = None
        self.string_id = 0
        self.format = 0
        self.width = 0
        self.height = 0
        self.scale = 0.0

    def __str__(self):
        return f"Texture <Filename: {self.filename}, Size: {self.width * self.scale} x {self.height * self.scale}>"


