__all__ = ('String', 'StringBase',)

from .base import StringBase


class String:
    def __init__(self):
        self.string_offset = 0
        self.string_length = 0

    def __str__(self):
        return f"String <Offset: {self.string_offset}, Length: {self.string_length}>"
