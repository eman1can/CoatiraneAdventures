__all__ = ('Frame',)


class Frame:
    def __init__(self):
        self.control_offset = 0
        self.controls = 1

    def __str__(self):
        return f"Frame <Control Offset: {self.control_offset}, Controls: {self.controls}>"
