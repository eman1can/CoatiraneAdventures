class Color(object):

    def __init__(self, r, g, b, a):
        self.r = r
        self.g = g
        self.b = b
        self.a = a
        self.clamp()

    def getR(self):
        return self.r

    def getG(self):
        return self.g

    def getB(self):
        return self.b

    def getA(self):
        return self.a

    def set(self, color):
        self.r = color.r
        self.g = color.g
        self.b = color.b
        self.a = color.a
        return self.clamp()

    def setFromString(self, color):
        self.r = int(color[0:2], 16)
        self.g = int(color[2:4], 16)
        self.b = int(color[4:6], 16)
        self.a = int(color[6:8], 16)

    def mulValue(self, value):
        self.r *= value
        self.g *= value
        self.b *= value
        self.a *= value
        return self.clamp()

    def mulColor(self, color):
        self.r *= color.r
        self.g *= color.g
        self.b *= color.b
        self.a *= color.a
        return self.clamp()

    def add(self, color):
        self.r += color.r
        self.g += color.g
        self.b += color.b
        self.a += color.a
        return this.clamp()

    def sub(self, color):
        self.r -= color.r
        self.g -= color.g
        self.b -= color.b
        self.a -= color.a
        return self.clamp()

    def clamp(self):
        if self.r < 0:
            self.r = 0
        elif self.r > 1:
            self.r = 1

        if self.g < 0:
            self.g = 0
        elif self.g > 1:
            self.g = 1

        if self.b < 0:
            self.b = 0
        elif self.b > 1:
            self.b = 1

        if self.a < 0:
            self.a = 0
        elif self.a > 1:
            self.a = 1
        return self;

    def premultiplyAlpha(self):
        self.r *= self.a;
        self.g *= self.a;
        self.b *= self.a;
        return self;

    @staticmethod
    def valueOf(hex):
        if hex is not None:
            if hex[0] == '#':
                hex = hex[1:]

            r = int(hex[0:2], 16);
            g = int(hex[2:4], 16);
            b = int(hex[4:6], 16);

            if len(hex) == 8:
                a = int(hex[6:8], 16)
            else:
                a = 255
            return Color(r / 255, g / 255, b / 255, a / 255);

    def toString(self):
        return str(hex(int(self.r*255)))[2:].zfill(2) + str(hex(int(self.g*255)))[2:].zfill(2) + str(hex(int(self.b*255)))[2:].zfill(2) + str(hex(int(self.a*255)))[2:].zfill(2)