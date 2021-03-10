__all__ = ('Animation',)


class Animation:
    def __init__(self):
        self.animation_offset = 0
        self.animation_length = 0

    def __str__(self):
        return f"Animation <Offset: {self.animation_offset}, Length: {self.animation_length}>"
