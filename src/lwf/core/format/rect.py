

class Rect:
    @staticmethod
    def zero():
        return Rect(0, 0, 0, 0)

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.size = width, height

    def set_size(self, size):
        self.width, self.height = size
        self.size = size

    def __str__(self):
        return f"x: {self.x}, Y: {self.y}, Width: {self.width}, Height: {self.height}"
