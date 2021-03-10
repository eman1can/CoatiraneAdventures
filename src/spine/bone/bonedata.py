from kivy.graphics import Color


class BoneData:

    def __init__(self, arg, parent):

        self.parent = None
        self.name = None
        self.length = 0
        self.x = 0.0
        self.y = 0.0
        self.rotation = 0.0
        self.scaleX = 1
        self.scaleY = 1
        self.flipX = False
        self.flipY = False
        self.inheritScale = True
        self.inheritRotation = True
        self.color = Color(0.61, 0.61, 0.61, 1)

        super(BoneData, self).__init__()
        if arg is None:
            raise Exception("IllegalArgumentException: name/bone cannot be None")
        if isinstance(arg, str):
            name = arg
            self.name = name
            self.parent = parent
        else:
            bone = arg
            self.parent = parent
            self.name = bone.name
            self.length = bone.length
            self.x, self.y = bone.x, bone.y
            self.rotation = bone.rotation
            self.scaleX, self.scaleY = bone.scaleX, bone.scaleY
            self.flipX, self.flipY = bone.flipX, bone.flipY

    def getParent(self):
        return self.parent

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

    def setPosition(self, x, y):
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


