'''Vector
======

The :class:`Vector` represents a 3D vector (x, y, z).
Our implementation is built on top of a Python list.

 An example of constructing a Vector::

    >>> # Construct a point at 82,34,33
    >>> v = Vector3(82, 34, 33)
    >>> v[0]
    82
    >>> v.x
    82
    >>> v[1]
    34
    >>> v.y
    34
    >>> v[2]
    33
    >>> v.z
    33

    >>> # Construct by giving a list of 3 values
    >>> pos = (93, 45, 39)
    >>> v = Vector3(pos)
    >>> v[0]
    93
    >>> v.x
    93
    >>> v[1]
    45
    >>> v.y
    45
    >>> v[2]
    39
    >>> v.z
    39
'''

__all__ = ('Vector3', )

import math

class Vector3(list):
    '''Vector3 class. See module documentation for more information.
    '''

    def __init__(self, *largs):
        if len(largs) == 1:
            super().__init__(largs[0])
        elif len(largs) == 2:
            super().__init__(largs[0:2])
        elif len(largs) == 3:
            super().__init__(largs[0:3])
        else:
            raise Exception('Invalid vector')

    def _get_x(self):
        return self[0]

    def _set_x(self, x):
        self[0] = x

    x = property(_get_x, _set_x)
    ''':attr:`x` represents the first element in the list.

    >>> v = Vector(12, 23)
    >>> v[0]
    12
    >>> v.x
    12
    '''

    def _get_y(self):
        return self[1]

    def _set_y(self, y):
        self[1] = y

    y = property(_get_y, _set_y)
    ''':attr:`y` represents the second element in the list.

    >>> v = Vector(12, 23)
    >>> v[1]
    23
    >>> v.y
    23

    '''

    def _get_z(self):
        return self[2]

    def _set_z(self, z):
        self[2] = z

    z = property(_get_z, _set_z)
    ''':attr:`z` represents the third element in the list.

    >>> v = Vector(12, 23, 24)
    >>> v[2]
    24
    >>> v.z
    24

    '''

    def __getslice__(self, i, j):
        try:
            # use the list __getslice__ method and convert
            # result to vector
            return Vector3(super(Vector3, self).__getslice__(i, j))
        except Exception:
            raise TypeError('vector3::FAILURE in __getslice__')

    def __add__(self, val):
        return Vector3(list(map(lambda x, y, z: x + y + z, self, val)))

    def __iadd__(self, val):
        if type(val) in (int, float):
            self.x += val
            self.y += val
            self.z += val
        else:
            self.x += val.x
            self.y += val.y
            self.z += val.z
        return self

    def __neg__(self):
        return Vector3([-x for x in self])

    def __sub__(self, val):
        return Vector3(list(map(lambda x, y, z: x - y - z, self, val)))

    def __isub__(self, val):
        if type(val) in (int, float):
            self.x -= val
            self.y -= val
            self.z -= val
        else:
            self.x -= val.x
            self.y -= val.y
            self.z -= val.z
        return self

    def __mul__(self, val):
        try:
            return Vector3(list(map(lambda x, y, z: x * y * z, self, val)))
        except Exception:
            return Vector3([x * val for x in self])

    def __imul__(self, val):
        if type(val) in (int, float):
            self.x *= val
            self.y *= val
            self.z *= val
        else:
            self.x *= val.x
            self.y *= val.y
            self.z *= val.z
        return self

    def __rmul__(self, val):
        return (self * val)

    def __truediv__(self, val):
        try:
            return Vector3(list(map(lambda x, y, z: x / y / z, self, val)))
        except Exception:
            return Vector3([x / val for x in self])

    def __div__(self, val):
        try:
            return Vector3(list(map(lambda x, y, z: x / y / z, self, val)))
        except Exception:
            return Vector3([x / val for x in self])

    def __rtruediv__(self, val):
        try:
            return Vector3(*val) / self
        except Exception:
            return Vector3(val, val) / self

    def __rdiv__(self, val):
        try:
            return Vector3(*val) / self
        except Exception:
            return Vector3(val, val) / self

    def __idiv__(self, val):
        if type(val) in (int, float):
            self.x /= val
            self.y /= val
            self.z /= val
        else:
            self.x /= val.x
            self.y /= val.y
            self.z /= val.z
        return self

    def length(self):
        '''Returns the length of a vector.
        '''
        return math.sqrt(self[0] ** 2 + self[1] ** 2 + self[2] ** 2)

    def length2(self):
        '''Returns the length of a vector squared.
        '''
        return self[0] ** 2 + self[1] ** 2 + self[2] ** 2

    def distance(self, to):
        '''Returns the distance between two points.
        '''
        return math.sqrt((self[0] - to[0]) ** 2 + (self[1] - to[1]) ** 2 + (self[2] - to[2]) ** 2)

    def distance2(self, to):
        '''Returns the distance between two points squared.
        '''
        return (self[0] - to[0]) ** 2 + (self[1] - to[1]) ** 2

    def normalize(self):
        '''Returns a new vector3 that has the same direction as vec,
        but has a length of one.
        '''
        if self[0] == 0. and self[1] == 0. and self[2] == 0.:
            return Vector3(0., 0., 0.)
        return self / self.length()

    def dot(self, a):
        '''Computes the dot product of a and b.

        >>> Vector3(2, 4, 2).dot((2, 2, 2))
        16

        '''
        return self[0] * a[0] + self[1] * a[1] + self[2] * a[2]

    def angle(self, a):
        '''Computes the angle between a and b, and returns the angle in
        degrees.
        angle = norm * atan2(cross, dot)
        '''
        angle = -(180 / math.pi) * math.atan2(
            self[0] * a[1] - self[0] * a[2] - self[1] * a[0] + self[1] * a[2] + self[2] * a[0] - self[2] * a[1],
            self[0] * a[0] + self[1] * a[1] + self[2] * a[2])
        return angle

    # def rotate(self, angle):
    #     '''Rotate the vector with an angle in degrees.
    #     '''
    #     angle = math.radians(angle)
    #     return Vector3(
    #         (self[0] * math.cos(angle)) - (self[1] * math.sin(angle)),
    #         (self[1] * math.cos(angle)) + (self[0] * math.sin(angle)))

    # @staticmethod
    # def line_intersection(v1, v2, v3, v4):
    #     '''
    #     Finds the intersection point between the lines (1)v1->v2 and (2)v3->v4
    #     and returns it as a vector object.
    #
    #     >>> a = (98, 28)
    #     >>> b = (72, 33)
    #     >>> c = (10, -5)
    #     >>> d = (20, 88)
    #     >>> Vector.line_intersection(a, b, c, d)
    #     [15.25931928687196, 43.911669367909241]
    #
    #     .. warning::
    #
    #         This is a line intersection method, not a segment intersection.
    #
    #     For math see: http://en.wikipedia.org/wiki/Line-line_intersection
    #     '''
    #     # linear algebar sucks...seriously!!
    #     x1, x2, x3, x4 = float(v1[0]), float(v2[0]), float(v3[0]), float(v4[0])
    #     y1, y2, y3, y4 = float(v1[1]), float(v2[1]), float(v3[1]), float(v4[1])
    #
    #     u = (x1 * y2 - y1 * x2)
    #     v = (x3 * y4 - y3 * x4)
    #     denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    #     if denom == 0:
    #         return None
    #
    #     px = (u * (x3 - x4) - (x1 - x2) * v) / denom
    #     py = (u * (y3 - y4) - (y1 - y2) * v) / denom
    #
    #     return Vector(px, py)
    #
    # @staticmethod
    # def segment_intersection(v1, v2, v3, v4):
    #     '''
    #     Finds the intersection point between segments (1)v1->v2 and (2)v3->v4
    #     and returns it as a vector object.
    #
    #     >>> a = (98, 28)
    #     >>> b = (72, 33)
    #     >>> c = (10, -5)
    #     >>> d = (20, 88)
    #     >>> Vector.segment_intersection(a, b, c, d)
    #     None
    #
    #     >>> a = (0, 0)
    #     >>> b = (10, 10)
    #     >>> c = (0, 10)
    #     >>> d = (10, 0)
    #     >>> Vector.segment_intersection(a, b, c, d)
    #     [5, 5]
    #     '''
    #
    #     # Yaaay! I love linear algebra applied within the realms of geometry.
    #     x1, x2, x3, x4 = float(v1[0]), float(v2[0]), float(v3[0]), float(v4[0])
    #     y1, y2, y3, y4 = float(v1[1]), float(v2[1]), float(v3[1]), float(v4[1])
    #
    #     # This is mostly the same as the line_intersection
    #     u = (x1 * y2 - y1 * x2)
    #     v = (x3 * y4 - y3 * x4)
    #     denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    #     if denom == 0:
    #         return None
    #
    #     px = (u * (x3 - x4) - (x1 - x2) * v) / denom
    #     py = (u * (y3 - y4) - (y1 - y2) * v) / denom
    #     # Here are the new bits
    #     c1 = (x1 <= px <= x2) or (x2 <= px <= x1) or (x1 == x2)
    #     c2 = (y1 <= py <= y2) or (y2 <= py <= y1) or (y1 == y2)
    #     c3 = (x3 <= px <= x4) or (x4 <= px <= x3) or (x3 == x4)
    #     c4 = (y3 <= py <= y4) or (y4 <= py <= y3) or (y3 == y4)
    #
    #     if (c1 and c2) and (c3 and c4):
    #         return Vector(px, py)
    #     else:
    #         return None
    #
    # @staticmethod
    # def in_bbox(point, a, b):
    #     '''Return True if `point` is in the bounding box defined by `a`
    #     and `b`.
    #
    #     >>> bmin = (0, 0)
    #     >>> bmax = (100, 100)
    #     >>> Vector.in_bbox((50, 50), bmin, bmax)
    #     True
    #     >>> Vector.in_bbox((647, -10), bmin, bmax)
    #     False
    #
    #     '''
    #     return ((point[0] <= a[0] and point[0] >= b[0] or
    #              point[0] <= b[0] and point[0] >= a[0]) and
    #             (point[1] <= a[1] and point[1] >= b[1] or
    #              point[1] <= b[1] and point[1] >= a[1]))