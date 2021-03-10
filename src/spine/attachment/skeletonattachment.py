from src.spine.attachment.attachment import Attachment


class SkeletonAttachment(Attachment):
    def __init__(self, name):
        self.skeleton = None

        super().__init__(name)

    def getSkeleton(self):
        return self.skeleton

    def setSkeleton(self, skeleton):
        self.skeleton = skeleton