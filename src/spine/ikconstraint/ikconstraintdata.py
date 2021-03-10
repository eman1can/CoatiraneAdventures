class IkConstraintData:

    def __init__(self, name):

        self.name = None
        self.bones = []
        self.target = None
        self.bendDirection = 1
        self.mix = 1

        self.name = name

    def getName(self):
        return self.name

    def getBones(self):
        return self.bones

    def getTarget(self):
        return self.target

    def setTarget(self, target):
        self.target = target

    def getBendDirection(self):
        return self.bendDirection

    def setBendDirection(self, bendDirection):
        self.bendDirection = bendDirection

    def getMix(self):
        return self.mix

    def setMix(self, mix):
        self.mix = mix

    def __str__(self):
        return self.name
