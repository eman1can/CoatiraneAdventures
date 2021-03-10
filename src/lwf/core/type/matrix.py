__all__ = ('Matrix',)


class Matrix:
    def __init__(self, *args):
        self.scale_x = 0.0
        self.scale_y = 0.0
        self.skew_0 = 0.0
        self.skew_1 = 0.0
        self.translate_x = 0.0
        self.translate_y = 0.0

        length = len(args)
        if length == 0:
            self.clear()
        elif length == 1:
            self.set(args[0])
        else:
            sc_x, sc_y, sk_0, sk_1, t_x, t_y = args
            self.scale_x = sc_x
            self.scale_y = sc_y
            self.skew_0 = sk_0
            self.skew_1 = sk_1
            self.translate_x = t_x
            self.translate_y = t_y

    def __str__(self):
        return f"SX: {self.scale_x}, SY: {self.scale_y}, SK0: {self.skew_0}, SK1: {self.skew_1}, TX: {self.translate_x}, TY: {self.translate_y}"

    def __eq__(self, other):
        return self.scale_x == other.scale_x and self.scale_y == other.scale_y and self.skew_0 == other.skew_0 and self.skew_1 == other.skew_1 and self.translate_x == other.translate_x and self.translate_y == other.translate_y

    def clear(self):
        self.scale_x = 1
        self.scale_y = 1
        self.skew_0 = 0
        self.skew_1 = 0
        self.translate_x = 0
        self.translate_y = 0

    def invalidate(self):
        self.scale_x = 0.0
        self.scale_y = 0.0
        self.skew_0 = 0.0
        self.skew_1 = 0.0
        self.translate_x = 3.40282347E+38
        self.translate_y = 3.40282347E+38

    def set(self, *args):
        if len(args) == 1:
            m = args[0]
            self.scale_x = m.scale_x
            self.scale_y = m.scale_y
            self.skew_0 = m.skew_0
            self.skew_1 = m.skew_1
            self.translate_x = m.translate_x
            self.translate_y = m.translate_y
        else:
            sc_x, sc_y, sk_0, sk_1, t_x, t_y = args
            self.scale_x = sc_x
            self.scale_y = sc_y
            self.skew_0 = sk_0
            self.skew_1 = sk_1
            self.translate_x = t_x
            self.translate_y = t_y
        return self

    def set_with_comparing(self, m):
        if m is None:
            return False
        s_x = m.scale_x
        s_y = m.scale_y
        s_0 = m.skew_0
        s_1 = m.skew_1
        t_x = m.translate_x
        t_y = m.translate_y
        changed = False
        if self.scale_x != s_x:
            self.scale_x = s_x
            changed = True
        if self.scale_y != s_y:
            self.scale_y = s_y
            changed = True
        if self.skew_0 != s_0:
            self.skew_0 = s_0
            changed = True
        if self.skew_1 != s_1:
            self.skew_1 = s_1
            changed = True
        if self.translate_x != t_x:
            self.translate_x = t_x
            changed = True
        if self.translate_y != t_y:
            self.translate_y = t_y
            changed = True
        return changed
