__all__ = ('Matrix',)


class Matrix:
    def get_sx(self):
        return self.m[0]

    def set_sx(self, value):
        self.m[0] = value

    def del_sx(self):
        self.m[0] = 1

    scale_x = property(get_sx, set_sx, del_sx, "ScaleX")

    def get_sy(self):
        return self.m[1]

    def set_sy(self, value):
        self.m[1] = value

    def del_sy(self):
        self.m[1] = 1

    scale_y = property(get_sy, set_sy, del_sy, "ScaleY")

    def get_sk0(self):
        return self.m[2]

    def set_sk0(self, value):
        self.m[2] = value

    def del_sk0(self):
        self.m[2] = 0

    skew_0 = property(get_sk0, set_sk0, del_sk0, "Skew_0")

    def get_sk1(self):
        return self.m[3]

    def set_sk1(self, value):
        self.m[3] = value

    def del_sk1(self):
        self.m[3] = 0

    skew_1 = property(get_sk1, set_sk1, del_sk1, "Skew_0")

    def get_tx(self):
        return self.m[4]

    def set_tx(self, value):
        self.m[4] = value

    def del_tx(self):
        self.m[4] = 0

    translate_x = property(get_tx, set_tx, del_tx, "TranslateX")

    def get_ty(self):
        return self.m[5]

    def set_ty(self, value):
        self.m[5] = value

    def del_ty(self):
        self.m[5] = 0

    translate_y = property(get_ty, set_ty, del_ty, "TranslateY")

    def __init__(self):
        self.m = [1, 1, 0, 0, 0, 0]

    def __str__(self):
        return "SX: {:.4f}, SY: {:.4f}, SK0: {:.4f}, SK1: {:.4f}, TX: {:.4f}, TY: {:.4f}".format(*self.m)

    def __eq__(self, other):
        if other is None:
            return False
        equal = True
        for index, v in enumerate(self.m):
            equal &= v == other.m[index]
        return equal

    def clear(self):
        self.m = [1, 1, 0, 0, 0, 0]

    def invalidate(self):
        self.m = [0, 0, 0, 0, -1, -1]

    def set(self, m, sc_y=None, sk_0=None, sk_1=None, t_x=None, t_y=None):
        if sc_y is None:
            self.set(*m.m)
        else:
            self.m = [m, sc_y, sk_0, sk_1, t_x, t_y]
        return self

    def set_with_comparing(self, m):
        if m is None:
            return False

        changed = False
        for index in range(len(self.m)):
            if self.m[index] != m.m[index]:
                self.m[index] = m.m[index]
                changed = True
        return changed
