class Dictionary:
    data = {}

    def __init__(self, *args):
        if len(args) > 0:
            assert isinstance(args[0], Dictionary)
            self.data = args[0].copy()

    def __len__(self):
        return len(self.data)

    def get(self, key):
        return self.data[key]

    def set(self, key, value):
        self.data[key] = value

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def copy(self):
        return self.data.copy()

    def contains(self, item):
        return self.data.contains(item)

    def __delete__(self, instance):
        del self.data

    def remove(self, key):
        del self.data[key]

    def clear(self):
        self.data = {}

    def items(self):
        return self.data.items()

    def values(self):
        return self.data.values()

    def keys(self):
        return self.data.keys()

    def TryGetValue(self, key):
        if key in self.data:
            return True, self.data[key]
        else:
            return False, None

    def __iter__(self):
        self.posistion = 0
        return self

    def __next__(self):
        self.posistion += 1
        return self.posistion < len(self.data.keys())

    def current(self):
        return self.data.keys[self.posistion]


class Dict(dict):
    def __init__(self):
        super().__init__()
    def TryGetValue(self, key):
        if key in self.keys():
            return True, self[key]
        else:
            return False, None

class Action:
    def __init__(self):
        self.value = None

    def __set__(self, instance, value):
        self.value = value

    def __get__(self, instance, owner):
        return self.value

    def __delete__(self, instance):
        del self.value


class SortedList(list):

    def Sort(self, comparison, left=0, r=0):
        if r is 0:
            r = len(self) - 1
        if left >= r:
            return

        pivot = self[r]
        cnt = left
        for i in range(left, r + 1):
            if comparison(self[i], pivot):
                self[cnt], self[i] = self[i], self[cnt]
                cnt += 1
        self.Sort(comparison, left, cnt - 2)
        self.Sort(comparison, cnt, r)


class Point:
    x = 0.0
    y = 0.0

    def __init__(self, px=0, py=0):
        self.x = px
        self.y = py


class Translate:
    translateX = 0.0
    translateY = 0.0

    def __init__(self, *args):
        if len(args) == 1:
            if isinstance(args[0], BinaryReader):
                br = args[0]
                self.translateX = br.ReadSingle()
                self.translateY = br.ReadSingle()
        else:
            self.translateX = 0.0
            self.translateY = 0.0


class Matrix:
    scaleX = 0.0
    scaleY = 0.0
    skew0 = 0.0
    skew1 = 0.0
    translateX = 0.0
    translateY = 0.0

    def __init__(self, *args):
        if len(args) is 0:
            self.Clear()
        elif len(args) is 1:
            if isinstance(args[0], BinaryReader):
                br = args[0]
                self.scaleX = br.ReadSingle()
                self.scaleY = br.ReadSingle()
                self.skew0 = br.ReadSingle()
                self.skew1 = br.ReadSingle()
                self.translateX = br.ReadSingle()
                self.translateY = br.ReadSingle()
            else:
                self.Set(args[0])
        else:
            self.scaleX, self.scaleY, self.skew0, self.skew1, self.translateX, self.translateY = args[0:6]

    def Clear(self):
        self.scaleX = 1
        self.scaleY = 1
        self.skew0 = 0
        self.skew1 = 0
        self.translateX = 0
        self.translateY = 0

    def Set(self, m):
        self.scaleX = m.scaleX
        self.scaleY = m.scaleY
        self.skew0 = m.skew0
        self.skew1 = m.skew1
        self.translateX = m.translateX
        self.translateY = m.translateY
        return self

    def SetWithComparing(self, m):
        if m is None:
            return False
        sX = m.scaleX
        sY = m.scaleY
        s0 = m.skew0
        s1 = m.skew1
        tX = m.translateX
        tY = m.translateY
        changed = False
        if self.scaleX is not sX:
            self.scaleX = sX
            changed = True
        if self.scaleY is not sY:
            self.scaleY = sY
            changed = True
        if self.skew0 is not s0:
            self.skew0 = s0
            changed = True
        if self.skew1 is not s1:
            self.skew1 = s1
            changed = True
        if self.translateX is not tX:
            self.translateX = tX
            changed = True
        if self.translateY is not tY:
            self.translateY = tY
            changed = True
        return changed


class Color:
    red = 0
    green = 0
    blue = 0
    alpha = 0

    def __init__(self, *args):
        if len(args) > 0:
            if isinstance(args[0], BinaryReader):
                br = args[0]
                self.red = br.ReadSingle()
                self.green = br.ReadSingle()
                self.blue = br.ReadSingle()
                self.alpha = br.ReadSingle()
            else:
                self.Set(args[0], args[1], args[2], args[3])

    def Set(self, r, g, b, a):
        self.red, self.green, self.blue, self.alpha = r, g, b, a

    def Equals(self, c):
        return self.red == c.red and self.green == c.green and self.blue == c.blue and self.alpha == c.alpha


class AlphaTransform:
    alpha = 0

    def __init__(self, *args):
        if len(args) is 0:
            self.alpha = 1
        else:
            if isinstance(args[0], BinaryReader):
                br = args[0]
                self.alpha = br.ReadSingle()
            else:
                self.alpha = args[0]


class ColorTransform:
    multi = None
    add = None

    def __init__(self, *args):
        if len(args) is 1:
            if isinstance(args[0], BinaryReader):
                br = args[0]
                self.multi = Color(br)
                self.add = Color(br)
            else:
                self.multi = Color()
                self.add = Color()
                self.Set(args[0])
        elif len(args) == 8:
            self.multi = Color(args[0], args[1], args[2], args[3])
            self.add = Color(args[4], args[5], args[6], args[7])
        else:
            self.multi = Color(1, 1, 1, 1)
            self.add = Color(0, 0, 0, 0)

    def Clear(self):
        self.multi.Set(1, 1, 1, 1)
        self.add.Set(0, 0, 0, 0)

    def Set(self, c):
        self.multi.Set(c.multi.red, c.multi.green, c.multi.blue, c.multi.alpha)
        self.add.Set(c.add.red, c.add.green, c.add.blue, c.add.alpha)

    def SetWithComparing(self, c):
        if c is None:
            return False
        cm = c.multi
        red = cm.red
        blue = cm.blue
        green = cm.green
        alpha = cm.alpha
        changed = False
        m = self.multi
        if m.red is not red:
            m.red = red
            changed = True
        if m.green is not green:
            m.green = green
            changed = True
        if m.blue is not blue:
            m.blue = blue
            changed = True
        if m.alpha is not alpha:
            m.alpha = alpha
            changed = True

        ca = c.add
        red = ca.red
        green = ca.green
        blue = ca.blue
        alpha = ca.alpha
        a = self.add
        if a.red is not red:
            a.red = red
            changed = True
        if a.green is not green:
            a.green = green
            changed = True
        if a.blue is not blue:
            a.blue = blue
            changed = True
        if a.alpha is not alpha:
            a.alpha = alpha
            changed = True

        return changed


class Bounds:
    xMin: float = 0.0
    xMax: float = 0.0
    yMin: float = 0.0
    yMax: float = 0.0

    def __init__(self, pxMin: float = 0.0, pxMax=0.0, pyMin: float = 0.0, pyMax: float = 0.0):
        self.xMin = pxMin
        self.xMax = pxMax
        self.yMin = pyMin
        self.yMax = pyMax


class HandlerWrapper:
    id = 0

class SortedDictionary(SortedDict):
    def TryGetValue(self, key):
        if key in self:
            return True, self[key]
        else:
            return False, None

    def __iter__(self):
        self.position = 0
        return self

    def __next__(self):
        self.position += 1
        return self.position < len(self.keys())

    def current(self):
        return self.keys()[self.position]

    def remove(self, key):
        self._list_remove(key)


class DetachDict(Dictionary):
    pass


class BitmapClips(SortedDictionary):
    pass



