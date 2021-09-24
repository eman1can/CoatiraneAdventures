__all__ = ('ProgramObject',)

from lwf.format.string_base import StringBase


class ProgramObject(StringBase):
    def __init__(self):
        super().__init__()
        self.width = 0
        self.height = 0
        self.matrix_id = 0
        self.color_transform_id = 0

    def __str__(self):
        return f"Program Object <Width: {self.width}, Height: {self.height}, Matrix Id: {self.matrix_id}, CT Id: {self.color_transform_id}>"
