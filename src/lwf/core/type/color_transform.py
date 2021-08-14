__all__ = ('ColorTransform',)

from .color import Color


class ColorTransform:
    def __init__(self, multi_red=1, multi_green=1, multi_blue=1, multi_alpha=1, add_red=0, add_green=0, add_blue=0, add_alpha=0):
        self.multi = Color()
        self.add = Color()

        if isinstance(multi_red, ColorTransform):
            self.set(multi_red)
        else:
            self.multi.set(multi_red, multi_green, multi_blue, multi_alpha)
            self.add.set(add_red, add_green, add_blue, add_alpha)

    def clear(self):
        self.multi.set(1, 1, 1, 1)
        self.add.set(0, 0, 0, 0)

    def set(self, multi_red=1, multi_green=1, multi_blue=1, multi_alpha=1, add_red=0, add_green=0, add_blue=0, add_alpha=0):
        if isinstance(multi_red, ColorTransform):
            self.multi.set(multi_red.multi)
            self.add.set(multi_red.add)
        else:
            self.multi.set(multi_red, multi_green, multi_blue, multi_alpha)
            self.add.set(add_red, add_green, add_blue, add_alpha)
        return self

    def set_with_comparing(self, c):
        if c is None:
            return False

        cm = c.multi
        red = cm.red
        blue = cm.blue
        green = cm.green
        alpha = cm.alpha
        changed = False
        m = self.multi
        if m.red != red:
            m.red = red
            changed = True
        if m.green != green:
            m.green = green
            changed = True
        if m.blue != blue:
            m.blue = blue
            changed = True
        if m.alpha != alpha:
            m.alpha = alpha
            changed = True

        ca = c.add
        red = ca.red
        green = ca.green
        blue = ca.blue
        alpha = ca.alpha
        a = self.add
        if a.red != red:
            a.red = red
            changed = True
        if a.green != green:
            a.green = green
            changed = True
        if a.blue != blue:
            a.blue = blue
            changed = True
        if a.alpha != alpha:
            a.alpha = alpha
            changed = True

        return changed

    def __str__(self):
        return f'ColorTransform <{self.multi} = {self.add}>'