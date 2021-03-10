class Matrix4:
    M00 = 0
    M01 = 4
    M02 = 8
    M03 = 12
    M10 = 1
    M11 = 5
    M12 = 9
    M13 = 13
    M20 = 2
    M21 = 6
    M22 = 10
    M23 = 14
    M30 = 3
    M31 = 7
    M32 = 11
    M33 = 15

    def __init__(self, *args):
        self.tmp = [0.0 for x in range(16)]
        self.val = [0.0 for x in range(16)]

        if len(args) != 0:
            self.set(*args)
        else:
            self.val[self.M00] = 1
            self.val[self.M11] = 1
            self.val[self.M22] = 1
            self.val[self.M33] = 1

    def set(self, *args):
        if len(args) == 1:
            if isinstance(args[0], Matrix4):
                return self.set(args[0].val)
            elif isinstance(args[0], list):
                for i, value in enumerate(args[0]):
                    self.val[i] = value
                return self
        raise Exception("Not implemented")

    def cpy(self):
        return Matrix4(self)

    def trn(self, *args):
        if len(args) == 1:
            self.val[self.M03] += args[0].x
            self.val[self.M13] += args[0].y
            self.val[self.M23] += args[0].z
        else:
            self.val[self.M03] += args[0]
            self.val[self.M13] += args[1]
            self.val[self.M23] += args[2]
        return self

    def getValues(self):
        return self.val

    def mul(self, matrix):
        mata, matb = self.val, matrix.val
        tmp = [0.0 for x in range(16)]
        tmp[self.M00] = mata[self.M00] * matb[self.M00] + mata[self.M01] * matb[self.M10] + mata[self.M02] * matb[self.M20] + mata[self.M03] * matb[self.M30]
        tmp[self.M01] = mata[self.M00] * matb[self.M01] + mata[self.M01] * matb[self.M11] + mata[self.M02] * matb[self.M21] + mata[self.M03] * matb[self.M31]
        tmp[self.M02] = mata[self.M00] * matb[self.M02] + mata[self.M01] * matb[self.M12] + mata[self.M02] * matb[self.M22] + mata[self.M03] * matb[self.M32]
        tmp[self.M03] = mata[self.M00] * matb[self.M03] + mata[self.M01] * matb[self.M13] + mata[self.M02] * matb[self.M23] + mata[self.M03] * matb[self.M33]
        tmp[self.M10] = mata[self.M10] * matb[self.M00] + mata[self.M11] * matb[self.M10] + mata[self.M12] * matb[self.M20] + mata[self.M13] * matb[self.M30]
        tmp[self.M11] = mata[self.M10] * matb[self.M01] + mata[self.M11] * matb[self.M11] + mata[self.M12] * matb[self.M21] + mata[self.M13] * matb[self.M31]
        tmp[self.M12] = mata[self.M10] * matb[self.M02] + mata[self.M11] * matb[self.M12] + mata[self.M12] * matb[self.M22] + mata[self.M13] * matb[self.M32]
        tmp[self.M13] = mata[self.M10] * matb[self.M03] + mata[self.M11] * matb[self.M13] + mata[self.M12] * matb[self.M23] + mata[self.M13] * matb[self.M33]
        tmp[self.M20] = mata[self.M20] * matb[self.M00] + mata[self.M21] * matb[self.M10] + mata[self.M22] * matb[self.M20] + mata[self.M23] * matb[self.M30]
        tmp[self.M21] = mata[self.M20] * matb[self.M01] + mata[self.M21] * matb[self.M11] + mata[self.M22] * matb[self.M21] + mata[self.M23] * matb[self.M31]
        tmp[self.M22] = mata[self.M20] * matb[self.M02] + mata[self.M21] * matb[self.M12] + mata[self.M22] * matb[self.M22] + mata[self.M23] * matb[self.M32]
        tmp[self.M23] = mata[self.M20] * matb[self.M03] + mata[self.M21] * matb[self.M13] + mata[self.M22] * matb[self.M23] + mata[self.M23] * matb[self.M33]
        tmp[self.M30] = mata[self.M30] * matb[self.M00] + mata[self.M31] * matb[self.M10] + mata[self.M32] * matb[self.M20] + mata[self.M33] * matb[self.M30]
        tmp[self.M31] = mata[self.M30] * matb[self.M01] + mata[self.M31] * matb[self.M11] + mata[self.M32] * matb[self.M21] + mata[self.M33] * matb[self.M31]
        tmp[self.M32] = mata[self.M30] * matb[self.M02] + mata[self.M31] * matb[self.M12] + mata[self.M32] * matb[self.M22] + mata[self.M33] * matb[self.M32]
        tmp[self.M33] = mata[self.M30] * matb[self.M03] + mata[self.M31] * matb[self.M13] + mata[self.M32] * matb[self.M23] + mata[self.M33] * matb[self.M33]
        for i, val in enumerate(tmp):
            self.val[i] = val
        return self

    def setToOrtho2D(self, *args):
        if len(args) == 4:
            self.setToOrtho(args[0], args[0] + args[2], args[1], args[1] + args[3], 0, 1)
        elif len(args) == 6:
            self.setToOrtho(args[0], args[0] + args[2], args[1], args[1] + args[3], args[4], args[5])
        return self

    def setToOrtho(self, left, right, bottom, top, near, far):
        self.idt()
        x_orth = 2 / (right - left)
        y_orth = 2 / (top - bottom)
        z_orth = -2 / (far - near)

        tx = -(right + left) / (right - left)
        ty = -(top + bottom) / (top - bottom)
        tz = -(far + near) / (far - near)

        self.val[self.M00] = x_orth
        self.val[self.M10] = 0
        self.val[self.M20] = 0
        self.val[self.M30] = 0
        self.val[self.M01] = 0
        self.val[self.M11] = y_orth
        self.val[self.M21] = 0
        self.val[self.M31] = 0
        self.val[self.M02] = 0
        self.val[self.M12] = 0
        self.val[self.M22] = z_orth
        self.val[self.M32] = 0
        self.val[self.M03] = tx
        self.val[self.M13] = ty
        self.val[self.M23] = tz
        self.val[self.M33] = 1

        return self

    def idt(self):
        self.val[self.M00] = 1
        self.val[self.M01] = 0
        self.val[self.M02] = 0
        self.val[self.M03] = 0
        self.val[self.M10] = 0
        self.val[self.M11] = 1
        self.val[self.M12] = 0
        self.val[self.M13] = 0
        self.val[self.M20] = 0
        self.val[self.M21] = 0
        self.val[self.M22] = 1
        self.val[self.M23] = 0
        self.val[self.M30] = 0
        self.val[self.M31] = 0
        self.val[self.M32] = 0
        self.val[self.M33] = 1
        return self