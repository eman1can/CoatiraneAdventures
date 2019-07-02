from spine import Enum
from spine import Skin
AttachmentType = Enum.enum(region=0, mesh=1, skinnedMesh = 2, boundingBox = 3)

class AttachmentLoader(object):
    def __init__(self):
        super(AttachmentLoader, self).__init__()

    def newAttachment(type, name):
        pass

    def newRegionAttachment(self, skin, name, path):
        pass

    def newMeshAttachment(self, skin, name, path):
        pass

    def newSkinnedMeshAttachment(self, skin, name, path):
        pass

    def newBoundingBoxAttachment(self, skin, name):
        pass