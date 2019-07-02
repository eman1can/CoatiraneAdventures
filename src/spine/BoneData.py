from spine.Color import Color
class BoneData(object):
    def __init__(self, name, parent):
        super(BoneData, self).__init__()
        if name is not None:
            self.name = name
            self.parent = None
            self.length = 0.0
            self.x = 0.0
            self.y = 0.0
            self.rotation = 0.0
            self.scaleX = 1.0
            self.scaleY = 1.0
            self.flipX = False
            self.flipY = False
            self.inheritScale = True
            self.inheritRotation = True
            self.color = Color(0.61, 0.61, 0.61, 1)
        else:
            raise Exception("Name cannot be null")

    def getParent(self):
        return self.parent

    def setParent(self, parent):
        self.parent = parent

    def getName(self):
        return self.name

    def getLength(self):
        return self.length

    def setLength(self, length):
        self.length = length

    def getX(self):
        return self.x

    def setX(self, x):
        self.x = x

    def getY(self):
        return self.y

    def setY(self, y):
        self.y = y

    def setPosisition(self, x, y):
        self.x = x
        self.y = y

    def getRotation(self):
        return self.rotation

    def setRotation(self, rotation):
        self.rotation = rotation

    def getScaleX(self):
        return self.scaleX

    def setScaleX(self, scaleX):
        self.scaleX = scaleX

    def getScaleY(self):
        return self.scaleY

    def setScaleY(self, scaleY):
        self.scaleY = scaleY

    def setScale(self, scaleX, scaleY):
        self.scaleX = scaleX
        self.scaleY = scaleY

    def getFlipX(self):
        return self.flipX

    def setFlipX(self, flipX):
        self.flipX = flipX

    def getFlipY(self):
        return self.flipY

    def setFlipY(self, flipY):
        self.flipY = flipY

    def getInheritScale(self):
        return self.inheritScale

    def setInheritScale(self, inheritScale):
        self.inheritScale = inheritScale

    def getInheritRotation(self):
        return self.inheritRotation

    def setInheritRotation(self, inheritRotation):
        self.inheritRotation = inheritRotation

    def getColor(self):
        return self.color

    def toString(self):
        return self.name


