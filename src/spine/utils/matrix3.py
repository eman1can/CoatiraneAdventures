import math


class Matrix3:
    M00 = 0
    M01 = 3
    M02 = 6
    M10 = 1
    M11 = 4
    M12 = 7
    M20 = 2
    M21 = 5
    M22 = 8

    def __init__(self, *args):

        self.val = []
        self.tmp = []

        if len(args) == 0:
            self.idt()
        else:
            self.set(args[0])

    def idt(self):
        val = self.val
        val[self.M00] = 1
        val[self.M10] = 0
        val[self.M20] = 0
        val[self.M01] = 0
        val[self.M11] = 1
        val[self.M21] = 0
        val[self.M02] = 0
        val[self.M12] = 0
        val[self.M22] = 1
        return self

    def mul(self, *args):
        if len(args) == 1:
            val = self.val
            mata, matb = val, args[0].val
        else:
            mata, matb = args[0], args[1]

        v00 = mata[self.M00] * matb[self.M00] + mata[self.M01] * matb[self.M10] + mata[self.M02] * matb[self.M20]
        v01 = mata[self.M00] * matb[self.M01] + mata[self.M01] * matb[self.M11] + mata[self.M02] * matb[self.M21]
        v02 = mata[self.M00] * matb[self.M02] + mata[self.M01] * matb[self.M12] + mata[self.M02] * matb[self.M22]

        v10 = mata[self.M10] * matb[self.M00] + mata[self.M11] * matb[self.M10] + mata[self.M12] * matb[self.M20]
        v11 = mata[self.M10] * matb[self.M01] + mata[self.M11] * matb[self.M11] + mata[self.M12] * matb[self.M21]
        v12 = mata[self.M10] * matb[self.M02] + mata[self.M11] * matb[self.M12] + mata[self.M12] * matb[self.M22]

        v20 = mata[self.M20] * matb[self.M00] + mata[self.M21] * matb[self.M10] + mata[self.M22] * matb[self.M20]
        v21 = mata[self.M20] * matb[self.M01] + mata[self.M21] * matb[self.M11] + mata[self.M22] * matb[self.M21]
        v22 = mata[self.M20] * matb[self.M02] + mata[self.M21] * matb[self.M12] + mata[self.M22] * matb[self.M22]

        mata[self.M00] = v00
        mata[self.M10] = v10
        mata[self.M20] = v20
        mata[self.M01] = v01
        mata[self.M11] = v11
        mata[self.M21] = v21
        mata[self.M02] = v02
        mata[self.M12] = v12
        mata[self.M22] = v22

        return self

    def mulLeft(self, m):
        val = self.val

        v00 = m.val[self.M00] * val[self.M00] + m.val[self.M01] * val[self.M10] + m.val[self.M02] * val[self.M20]
        v01 = m.val[self.M00] * val[self.M01] + m.val[self.M01] * val[self.M11] + m.val[self.M02] * val[self.M21]
        v02 = m.val[self.M00] * val[self.M02] + m.val[self.M01] * val[self.M12] + m.val[self.M02] * val[self.M22]

        v10 = m.val[self.M10] * val[self.M00] + m.val[self.M11] * val[self.M10] + m.val[self.M12] * val[self.M20]
        v11 = m.val[self.M10] * val[self.M01] + m.val[self.M11] * val[self.M11] + m.val[self.M12] * val[self.M21]
        v12 = m.val[self.M10] * val[self.M02] + m.val[self.M11] * val[self.M12] + m.val[self.M12] * val[self.M22]

        v20 = m.val[self.M20] * val[self.M00] + m.val[self.M21] * val[self.M10] + m.val[self.M22] * val[self.M20]
        v21 = m.val[self.M20] * val[self.M01] + m.val[self.M21] * val[self.M11] + m.val[self.M22] * val[self.M21]
        v22 = m.val[self.M20] * val[self.M02] + m.val[self.M21] * val[self.M12] + m.val[self.M22] * val[self.M22]

        val[self.M00] = v00
        val[self.M10] = v10
        val[self.M20] = v20
        val[self.M01] = v01
        val[self.M11] = v11
        val[self.M21] = v21
        val[self.M02] = v02
        val[self.M12] = v12
        val[self.M22] = v22

        return self

    def setToRotation(self, *args):
        if len(args) == 1:
            return self.setToRotationRad(math.radians(args[0]))
        elif len(args) == 2:
            radians = math.radians(args[1])
            return self.setToRotation(args[0], math.cos(radians), math.sin(radians))
        else:
            axis, cos, sin = args[0], args[1], args[2]
            val = self.val
            oc = 1.0 - cos
            val[self.M00] = oc * axis.x * axis.x + cos
            val[self.M10] = oc * axis.x * axis.y - axis.z * sin
            val[self.M20] = oc * axis.z * axis.x + axis.y * sin
            val[self.M01] = oc * axis.x * axis.y + axis.z * sin
            val[self.M11] = oc * axis.y * axis.y + cos
            val[self.M21] = oc * axis.y * axis.z - axis.x * sin
            val[self.M02] = oc * axis.z * axis.x - axis.y * sin
            val[self.M12] = oc * axis.y * axis.z + axis.x * sin
            val[self.M22] = oc * axis.z * axis.z + cos
            return self

    def setToRotationRad(self, radians):
        cos = math.cos(radians)
        sin = math.sin(radians)
        val = self.val

        val[self.M00] = cos
        val[self.M10] = sin
        val[self.M20] = 0

        val[self.M01] = -sin
        val[self.M11] = cos
        val[self.M21] = 0

        val[self.M02] = 0
        val[self.M12] = 0
        val[self.M22] = 1

        return self

    def setToTranslation(self, *args):
        if len(args) == 1:
            x, y = args[0].x, args[0].y
        else:
            x, y = args[0], args[1]

        val = self.val

        val[self.M00] = 1
        val[self.M10] = 0
        val[self.M20] = 0

        val[self.M01] = 0
        val[self.M11] = 1
        val[self.M21] = 0

        val[self.M02] = x
        val[self.M12] = y
        val[self.M22] = 1

        return self

    def setToScaling(self, *args):
        if len(args) == 1:
            scaleX, scaleY = args[0].x, args[0].y
        else:
            scaleX, scaleY = args[0], args[1]
        val = self.val
        val[self.M00] = scaleX
        val[self.M10] = 0
        val[self.M20] = 0
        val[self.M01] = 0
        val[self.M11] = scaleY
        val[self.M21] = 0
        val[self.M02] = 0
        val[self.M12] = 0
        val[self.M22] = 1
        return self

    def __str__(self):
        val = self.val
        return f"[ {val[self.M00]} | {val[self.M01]} | {val[self.M02]} ]\n" \
               f"[ {val[self.M10]} | {val[self.M11]} | {val[self.M12]} ]\n" \
               f"[ {val[self.M20]} | {val[self.M12]} | {val[self.M22]} ]"

    def det(self):
        val = self.val
        return val[self.M00] * val[self.M11] * val[self.M22] + val[self.M01] * val[self.M12] * val[self.M20] + val[self.M02] * val[self.M10] * val[self.M21] - val[self.M00] * val[self.M12] * val[self.M21] - val[self.M01] * val[self.M10] * val[self.M22] - val[self.M02] * val[self.M11] * val[self.M20]

    def inv(self):
        det = self.det()
        if det == 0:
            raise Exception("Can't Invert a singular matrix!")

        inv_det = 1.0 / det
        tmp, val = self.tmp, self.val

        tmp[self.M00] = val[self.M11] * val[self.M22] - val[self.M21] * val[self.M12]
        tmp[self.M10] = val[self.M20] * val[self.M12] - val[self.M10] * val[self.M22]
        tmp[self.M20] = val[self.M10] * val[self.M21] - val[self.M20] * val[self.M11]
        tmp[self.M01] = val[self.M21] * val[self.M02] - val[self.M01] * val[self.M22]
        tmp[self.M11] = val[self.M00] * val[self.M22] - val[self.M20] * val[self.M02]
        tmp[self.M21] = val[self.M20] * val[self.M01] - val[self.M00] * val[self.M21]
        tmp[self.M02] = val[self.M01] * val[self.M12] - val[self.M11] * val[self.M02]
        tmp[self.M12] = val[self.M10] * val[self.M02] - val[self.M00] * val[self.M12]
        tmp[self.M22] = val[self.M00] * val[self.M11] - val[self.M10] * val[self.M01]

        val[self.M00] = inv_det * tmp[self.M00]
        val[self.M10] = inv_det * tmp[self.M10]
        val[self.M20] = inv_det * tmp[self.M20]
        val[self.M01] = inv_det * tmp[self.M01]
        val[self.M11] = inv_det * tmp[self.M11]
        val[self.M21] = inv_det * tmp[self.M21]
        val[self.M02] = inv_det * tmp[self.M02]
        val[self.M12] = inv_det * tmp[self.M12]
        val[self.M22] = inv_det * tmp[self.M22]

        return self

    def set(self, arg):
        self.val = arg.copy()
        return self

    def trn(self, *args):
        if len(args) == 1:
            self.val[self.M02] += args[0].x
            self.val[self.M12] += args[0].y
        else:
            self.val[self.M02] += args[0]
            self.val[self.M12] += args[1]
        return self

    def translate(self, *args):
        if len(args) == 1:
            x, y = args[0].x, args[0].y
        else:
            x, y = args[0], args[1]
        val = self.val
        val[self.M00] = 1
        val[self.M10] = 0
        val[self.M20] = 0

        val[self.M01] = 0
        val[self.M11] = 1
        val[self.M21] = 0

        val[self.M02] = x
        val[self.M12] = y
        val[self.M22] = 1
        self.mul(val, self.tmp)
        return self

    def rotate(self, degrees):
        return self.rotateRad(math.radians(degrees))

    def rotateRad(self, radians):
        if radians == 0:
            return self
        cos = math.cos(radians)
        sin = math.sin(radians)
        tmp = self.tmp

        tmp[self.M00] = cos
        tmp[self.M00] = sin
        tmp[self.M00] = 0

        tmp[self.M00] = -sin
        tmp[self.M00] = cos
        tmp[self.M00] = 0

        tmp[self.M00] = 0
        tmp[self.M00] = 0
        tmp[self.M00] = 1

        self.mul(self.val, tmp)
        return self

    def scale(self, *args):
        if len(args) == 1:
            scaleX, scaleY = args[0].x, args[0].y
        else:
            scaleX, scaleY = args[0], args[1]
        tmp = self.tmp
        tmp[self.M00] = scaleX
        tmp[self.M10] = 0
        tmp[self.M20] = 0
        tmp[self.M01] = 0
        tmp[self.M11] = scaleY
        tmp[self.M21] = 0
        tmp[self.M02] = 0
        tmp[self.M12] = 0
        tmp[self.M22] = 1
        self.mul(self.val, tmp)
        return self

    def getValues(self):
        return self.val

    def getTranslation(self, position):
        position.x + self.val[self.M02]
        position.y + self.val[self.M12]
        return position

    def getScale(self, scale):
        val = self.val
        scale.x = math.sqrt(val[self.M00] * val[self.M00] + val[self.M01] * val[self.M01])
        scale.y = math.sqrt(val[self.M10] * val[self.M10] + val[self.M11] * val[self.M11])
        return scale

    def getRotation(self):
        return math.radians(self.getRotationRad())

    def getRotationRad(self):
        return math.atan2(self.val[self.M10], self.val[self.M00])

    def scl(self, arg):
        if isinstance(arg, float):
            scaleX, scaleY = arg, arg
        else:
            scaleX, scaleY = arg.x, arg.copy
        self.val[self.M00] *= scaleX
        self.val[self.M11] *= scaleY
        return self

    def transpose(self):
        val = self.val
        v01 = val[self.M10]
        v02 = val[self.M20]
        v10 = val[self.M01]
        v12 = val[self.M21]
        v20 = val[self.M02]
        v21 = val[self.M12]
        val[self.M01] = v01
        val[self.M02] = v02
        val[self.M10] = v10
        val[self.M12] = v12
        val[self.M20] = v20
        val[self.M21] = v21
        return self