__all__ = ('ColorTransform',)

from lwf.modules.color import Color


class ColorTransform:
    def __init__(self, mr=1, mg=1, mb=1, ma=1, ar=0, ag=0, ab=0, aa=0):
        self.c = [mr, mg, mb, ma, ar, ag, ab, aa]

    def clear(self):
        self.c = [1, 1, 1, 1, 0, 0, 0, 0]

    def set(self, mr=1, mg=1, mb=1, ma=1, ar=0, ag=0, ab=0, aa=0):
        self.c = [mr, mg, mb, ma, ar, ag, ab, aa]
        return self

    def set_with_comparing(self, c):
        if c is None:
            return False

        changed = False
        for index in range(8):
            if self.c[index] != c.c[index]:
                self.c[index] = c.c[index]
                changed |= True

        return changed

    def __str__(self):
        return f'ColorTransform <{self.c}>'
