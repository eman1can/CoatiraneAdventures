from kivy.graphics import Color


class Slot:

    def __init__(self, *args):

        self.slotData = None
        self.bone = None
        self.color = None
        self.attachment = None
        self.attachmentTime = 0.0
        self.attachmentVertices = []

        super().__init__()
        if len(args) == 1:
            self.data = args[0]
            self.bone = None
            self.color = Color(1, 1, 1, 1)
        else:
            if args[0] is None:
                raise Exception("slot/slotData cannot be None.")
            if args[1] is None:
                raise Exception("bone cannot be None.")
            if isinstance(args[0], Slot):
                slot, bone = args[0], args[1]
                self.data = slot.data
                self.bone = bone
                self.color = Color(slot.color)
                self.attachment = slot.attachment
                self.attachmentTime = slot.attachmentTime
            else:
                data, bone = args[0], args[1]
                self.data = data
                self.bone = bone
                self.color = Color()
                self.setToSetupPose()

    def getData(self):
        return self.data

    def getBone(self):
        return self.bone

    def getSkeleton(self):
        return self.bone.skeleton

    def getColor(self):
        return self.color

    def getAttachment(self):
        return self.attachment

    def setAttachment(self, attachment):
        if self.attachment == attachment:
            return
        self.attachment = attachment
        self.attachmentTime = self.bone.skeleton.time
        self.attachmentVertices = []

    def setAttachmentTime(self, time):
        self.attachmentTime = self.bone.skeleton.time - time

    def getAttachmentTime(self):
        return self.bone.skeleton.time - self.attachmentTime

    def setAttachmentVertices(self, attachmentVertices):
        self.attachmentVertices = attachmentVertices

    def getAttachmentVertices(self):
        return self.attachmentVertices

    def setToSetupPose(self, *args):
        if len(args) == 0:
            self.setToSetupPose(self.bone.skeleton.data.slots.index(self.data))
        else:
            self.color.r = self.data.color.r
            self.color.g = self.data.color.g
            self.color.b = self.data.color.b
            self.color.a = self.data.color.a
            self.setAttachment(None if self.data.attachmentName is None else self.bone.skeleton.getAttachment(args[0], self.data.attachmentName))

    def __str__(self):
        return self.data.name