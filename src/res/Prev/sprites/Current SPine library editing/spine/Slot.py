from spine.Color import Color
class Slot(object):
    def __init__(self, slotData, skeleton, bone):
        super(Slot, self).__init__()
        if not slotData:
            raise Exception('slotData cannot be None.')
        if not skeleton:
            raise Exception('skeleton cannot be None.')
        if not bone:
            raise Exception('bone cannot be None.')
        self.data = slotData
        self.skeleton = skeleton
        self.bone = bone
        self.color = Color(255, 255, 255, 255)
        self.attachment = None
        self.attachmentTime = 0.0
        self.setToBindPose()


    def setColor(self, r, g, b, a):
        self.color.set(Color(r, g, b, a))
                          
        
    def setAttachment(self, attachment):
        self.attachment = attachment
        self.attachmentTime = self.skeleton.time


    def setAttachmentTime(self, time):
        self.attachmentTime = self.skeleton.time - time


    def getAttachmentTime(self):
        return self.skeleton.time - self.attachmentTime

    
    def setToBindPose(self):
        for i, slot in enumerate(self.skeleton.data.slots):
            if self.data == slot:
                self.setToBindPoseWithIndex(i)


    def setToBindPoseWithIndex(self, slotIndex):
        self.setColor(self.data.color.getR(), self.data.color.getG(), self.data.color.getB(), self.data.color.getA())
        self.setAttachment(self.skeleton.getAttachmentByIndex(slotIndex, self.data.attachmentName) if self.data.attachmentName else None)
    
    
