__all__ = ('Label',)

from src.lwf.core.format.string.base import StringBase


class Label(StringBase):
    def __init__(self):
        super().__init__()

        self.frame_no = 0

    def __str__(self):
        return f"Label <{super().__str__()}, Frame No: {self.frame_no}>"
