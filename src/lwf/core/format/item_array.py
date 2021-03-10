__all__ = ('ItemArray',)


class ItemArray:
    def __init__(self):
        self.offset = 0
        self.length = 0

    def __str__(self):
        return f"Item Array <Offset: {self.offset}, Length: {self.length}>"
