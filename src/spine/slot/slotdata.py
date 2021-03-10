from kivy.graphics import Color


class SlotData:

    def __init__(self, *args):

        self.name = None
        self.boneData = None
        self.color = Color(1, 1, 1, 1)
        self.attachmentName = None
        self.additiveBlending = None

        super().__init__()
        if len(args) == 0:
            self.name = ""
            self.boneData = None
        else:
            name, boneData = args[0], args[1]
            if name is None:
                raise Exception("IllegalArgumentException: Name cannot be None.")
            if boneData is None:
                raise Exception("IllegalArgumentException: boneData cannot be None.")

            self.name = name
            self.boneData = boneData

    def getName(self):
        return self.name

    def getBoneData(self):
        return self.boneData

    def getColor(self):
        return self.color

    def setAttachmentName(self, attachmentName):
        self.attachmentName = attachmentName

    def getAttachmentName(self):
        return self.attachmentName

    def getAdditiveBlending(self):
        return self.additiveBlending

    def setAdditiveBlending(self, additiveBlending):
        self.additiveBlending = additiveBlending

    def __str__(self):
        return self.name
