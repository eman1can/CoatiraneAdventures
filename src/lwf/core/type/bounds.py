__all__ = ('Bounds',)


class Bounds:
    def __init__(self, px_min=0.0, px_max=0.0, py_min=0.0, py_max=0.0):
        self.x_min = px_min
        self.x_max = px_max
        self.y_min = py_min
        self.y_max = py_max

    def clear(self):
        self.x_min = 0.0
        self.x_max = 0.0
        self.y_min = 0.0
        self.y_max = 0.0
