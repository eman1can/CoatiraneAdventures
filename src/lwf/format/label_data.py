__all__ = ('Label',)

from lwf.format.string_base import StringBase


class Label(StringBase):
    def __init__(self):
        super().__init__()
        self.frame_no = 0

    def __str__(self):
        return f"Label <Name: {self.string}, Frame No: {self.frame_no}>"
