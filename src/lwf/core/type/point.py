__all__ = ('Point',)


class Point:
    def __init__(self, px=0.0, py=0.0):
        self.x = px
        self.y = py

    def __str__(self):
        return f"Point <X: {self.x}, Y: {self.y}>"
