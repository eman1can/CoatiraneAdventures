__all__ = ('Color',)


class Color:
    def __init__(self, r=0.0, g=0.0, b=0.0, a=0.0):
        self.red = 0.0
        self.green = 0.0
        self.blue = 0.0
        self.alpha = 0.0

        self.set(r, g, b, a)

    def set(self, c, g=None, b=None, a=None):
        if g is None:
            self.red = c.red
            self.green = c.green
            self.blue = c.blue
            self.alpha = c.alpha
        else:
            self.red = c
            self.green = g
            self.blue = b
            self.alpha = a

    def __eq__(self, c):
        return self.red == c.red and self.green == c.green and self.blue == c.blue and self.alpha == c.alpha

    def __str__(self):
        return "Color <{:.4f}, {:.4f}, {:.4f}, {:.4f}>".format(self.red, self.green, self.blue, self.alpha)
