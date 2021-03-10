import math


class Vector2:

    def __init__(self, *args):

        self.x = 0
        self.y = 0

        if len(args) == 1:
            self.set(args[0])
        elif len(args) == 1:
            self.x, self.y = args[0], args[1]

    def __copy__(self):
        return Vector2(self)

    def len(self, *args):
        return math.sqrt(self.len2(*args))

    def len2(self, *args):
        if len(args) == 2:
            x, y = args[0], args[1]
        else:
            x, y = self.x, self.y
        return x * x + y * y

    def set(self, *args):
        if len(args) == 1:
            x, y = args[0].x, args[0].y
        else:
            x, y = args[0], args[1]
        self.x, self.y = x, y
        return self

    def sub(self, *args):
        if len(args) == 1:
            x, y = args[0].x, args[0].y
        else:
            x, y = args[0], args[1]
        self.x -= x
        self.y -= y
        return self

    def nor(self):
        len = self.len()
        if len != 0:
            self.x /= len
            self.y /= len
        return self

    def add(self, *args):
        if len(args) == 1:
            x, y = args[0].x, args[0].y
        else:
            x, y = args[0], args[1]
        self.x += x
        self.y += y
        return self

    def dot(self, *args):
        if len(args) == 1:
            return self.x * args[0].x + self.y * args[0].y
        elif len(args) == 2:
            return self.x * args[0] + self.y * args[1]
        else:
            return args[0] * args[2] + args[1] * args[3]

    def scl(self, *args):
        if len(args) == 1:
            if isinstance(args[0], float):
                scaleX, scaleY = args[0], args[0]
            else:
                scaleX, scaleY = args[0].x, args[0].y
        else:
            scaleX, scaleY = args[0], args[1]
        self.x *= scaleX
        self.y *= scaleY
        return self

    def mulAdd(self, vec, arg):
        if isinstance(arg, float):
            scaleX, scaleY = arg, arg
        else:
            scaleX, scaleY = arg.x, arg.y
        self.x += vec.x * scaleX
        self.y += vec.y * scaleY
        return self

    def dst(self, *args):
        if len(args) == 1:
            x1, y1, x2, y2 = self.x, self.y, args[0].x, args[0].y
        elif len(args) == 2:
            x1, y1, x2, y2 = self.x, self.y, args[0], args[1]
        else:
            x1, y1, x2, y2 = args[0], args[1], args[2], args[3]
        x_d = x2 - x1
        y_d = y2 - y1
        return math.sqrt(x_d * x_d + y_d * y_d)

    def dst2(self, *args):
        if len(args) == 1:
            x1, y1, x2, y2 = self.x, self.y, args[0].x, args[0].y
        elif len(args) == 2:
            x1, y1, x2, y2 = self.x, self.y, args[0], args[1]
        else:
            x1, y1, x2, y2 = args[0], args[1], args[2], args[3]
        x_d = x2 - x1
        y_d = y2 - y1
        return x_d * x_d + y_d * y_d

    def limit(self, limit):
        return self.limit2(limit * limit)

    def limit2(self, limit2):
        len2 = self.len2()
        if len2 > limit2:
            return self.scl(math.sqrt(limit2 / len2))
        return self

    def clamp(self, min, max):
        len2 = self.len2()
        if len2 == 0.0:
            return self
        max2 = max * max
        if len2 > max2:
            return self.scl(math.sqrt(max2 / len2))
        min2 = min * min
        if len2 < min2:
            return self.scl(math.sqrt(min2 / len2))
        return self

    def setLength(self, len):
        return self.setLength2(len * len)

    def setLength2(self, len2):
        oldLen2 = self.len2()
        return self if (oldLen2 == 0 or oldLen2 == len2) else self.scl(math.sqrt(len2 / oldLen2))

    def __str__(self):
        return f"({self.x}, {self.y})"

    def fromString(self, v):
        s = v.index(',', 1)
        if s != -1 and v[0] == '(' and v[len(v) - 1] == ')':
            try:
                x = float(v[1:s])
                y = float(v[s + 1: len(v) - 1])
                return self.set(x, y)
            except ValueError:
                pass
        raise Exception(f"Malformed vector2: {v}")

    def mul(self, mat):
        x = self.x * mat.val[0] + self.y * mat.val[3] + mat.val[6]
        y = self.x * mat.val[1] + self.y * mat.val[4] + mat.val[7]
        self.x = x
        self.y = y
        return self

    def crs(self, *args):
        if len(args) == 1:
            x, y = args[0].x, args[0].y
        else:
            x, y = args[0], args[1]
        return self.x * x, self.y * y

    def angle(self, *args):
        if len(args) == 1:
            return math.degrees(self.angleRad(args[0]))
        else:
            angle = math.degrees(self.angleRad())
            if angle < 0:
                angle += 360
            return angle

    def angleRad(self, *args):
        if len(args) == 1:
            return math.atan2(self.crs(args[0]), self.dot(args[0]))
        else:
            return math.atan2(self.y, self.x)

    def setAngle(self, degrees):
        return self.setAngleRad(math.radians(degrees))

    def setAngleRad(self, radians):
        self.set(self.len(), 0)
        self.rotateRad(radians)
        return self

    def rotate(self, degrees):
        return self.rotateRad(math.radians(degrees))

    def rotateAround(self, reference, degrees):
        return self.sub(reference).rotate(degrees).add(reference)

    def rotateRad(self, radians):
        cos = math.cos(radians)
        sin = math.sin(radians)

        newX = self.x * cos - self.y * sin
        newY = self.x * sin - self.y * cos

        self.x = newX
        self.y = newY

        return self

    def rotateAroundRad(self, reference, radians):
        return self.sub(reference).rotateRad(radians).add(reference)

    def rotate90(self, dir):
        x = self.x
        if dir >= 0:
            self.x = -self.y
            self.y = x
        else:
            self.x = self.y
            self.y = -x
        return self

    def lerp(self, target, alpha):
        invAlpha = 1.0 - alpha
        self.x = (self.x * invAlpha) + (target.x * alpha)
        self.y = (self.y * invAlpha) + (target.y * alpha)
        return self

    def interpolate(self, target, alpha, interpolation):
        return self.lerp(target, interpolation.apply(alpha))

    def __eq__(self, other):
        if self == other:
            return True
        if other is None:
            return False
        if self.__class__ != other.__class__:
            return False
        if self.x != other.x:
            return False
        if self.y != other.y:
            return False
        return True

    def setZero(self):
        self.x = 0
        self.y = 0
        return self


Zero = Vector2(0, 0)
X = Vector2(1, 0)
Y = Vector2(0, 1)
