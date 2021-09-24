__all__ = ('Font',)

from lwf.format.string_base import StringBase


class Font(StringBase):
    def __init__(self):
        super().__init__()
        self.letter_spacing = 0.0

    def __str__(self):
        return f"Font <Name: {self.string}, Letter Spacing: {self.letter_spacing}>"
