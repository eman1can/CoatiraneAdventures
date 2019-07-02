from enum import Enum

class BlendMode(Enum):
    NORMAL = (0x0302, 1, 0x0303)
    ADDITIVE = (0x0302, 1, 1)
    MULTIPLY = (0x0306, 0x0306, 0x0303)
    SCREEN = (1, 1, 0x0301)

    def __init__(self, source, sourcePremultipliedAlpha, dest):
        self.source = source
        self.sourcePremultipliedAlpha = sourcePremultipliedAlpha
        self.dest = dest
        if (self.source == 0x0302 & self.sourcePremultipliedAlpha == 1 & self.dest == 0x0303):
            self.name = 'normal'
        if (self.source == 0x0302 & self.sourcePremultipliedAlpha == 1 & self.dest == 1):
            self.name = 'additive'
        if (self.source == 0x0306 & self.sourcePremultipliedAlpha == 0x0306 & self.dest == 0x0303):
            self.name = 'multiply'
        if (self.source == 1 & self.sourcePremultipliedAlpha == 1 & self.dest == 0x0301):
            self.name = 'screen'

    def getSource(self, PMA):
        if PMA:
            return self.sourcePremultipliedAlpha
        else:
            return self.source

    def getDest(self):
        return self.dest

    @staticmethod
    def valueOf(blend):
        if blend == 'normal':
            return BlendMode.NORMAL
        if blend == 'additive':
            return BlendMode.ADDITIVE
        if blend == 'multiply':
            return BlendMode.MULTIPLY
        if blend == 'screen':
            return BlendMode.SCREEN

    def toString(self):
        return self.name

