from spine.Color import Color
class SlotData(object):
    def __init__(self, name, boneData):
        super(SlotData, self).__init__()
        if not name:
            raise Exception('Name cannot be None.')

        if not boneData:
            raise Exception('boneData cannot be None.')

        self.name = name
        self.boneData = boneData
        self.color = Color(255, 255, 255, 255)
        self.attachmentName = None
        self.blendMode = None

    def getName(self):
        return self.name

    def getBoneData(self):
        return self.boneData;

    def getColor(self):
        return self.color

    def setAttachmentName(self, attachmentName):
        self.attachmentName = attachmentName

    def getAttachmentName(self):
        return self.attachmentName

    def getBlendMode(self):
        return self.blendMode

    def setBlendMode(self, blendMode):
        self.blendMode = blendMode

    def toString(self):
        return self.name