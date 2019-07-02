
class SkeletonData(object):
    def __init__(self):
        super(SkeletonData, self).__init__()
        self.name = None
        self.bones = []
        self.slots = []
        self.skins = []
        self.defaultSkin = None
        self.events = []
        self.animations = []
        self.ikConstraints = []
        self.width = 0
        self.height = 0
        self.version = None
        self.hash = None
        self.imagespath = None

    def getBones(self):
        return self.bones

    def findBone(self, boneName):
        if boneName is not None:
            for i, bone in enumerate(self.bones):
                if bone.name == boneName:
                    return bone
        else:
            raise Exception("Bone Name cannot be None")
        return None

    def findBoneIndex(self, boneName):
        if boneName is not None:
            for i, bone in enumerate(self.bones):
                if bone.name == boneName:
                    return i
        else:
            raise Exception("Bone name cannot be null")
        return -1

    def getSlots(self):
        return self.slots

    def findSlot(self, slotName):
        if slotName is not None:
            for i, slot in enumerate(self.slots):
                if slot.name == slotName:
                    return slot
        else:
            raise Exception("Slot name cannot be null")
        return None

    
    def findSlotIndex(self, slotName):
        if slotName is not None:
            for i, slot in enumerate(self.slots):
                if slot.name == slotName:
                    return i
        else:
            raise Exception("Slot name cannot be null")
        return -1

    def getDefaultSkin(self):
        return self.defaultSkin

    def setDefaultSkin(self, defaultSkin):
        self.defaultSkin = defaultSkin

    def findSkin(self, skinName):
        if skinName is not None:
            for i, skin in enumerate(self.skins):
                if skin.name == skinName:
                    return skin
        else:
            raise Exception("Slot name cannot be null")
        return None

    def getSkins(self):
        return self.skins

    def findEvent(self, eventName):
        if eventName is not None:
            for i, event in enumerate(self.events):
                if event.name == eventName:
                    return event
        else:
            raise Exception("Event name cannot be null")
        return None

    def getEvents(self):
        return self.events

    def getAnimations(self):
        return self.animations

    def findAnimation(self, animationName):
        if animationName is not None:
            for i, animation in enumerate(self.animations):
                if animation.name == animationName:
                    return animation
        else:
            raise Exception("Animation name cannot be null")
        return None

    def findIkConstraint(self, ikconstraintName):
        if ikconstraintName is not None:
            for i, ikconstraint in enumerate(self.ikConstraints):
                if ikconstraint.name == ikconstraintName:
                    return ikconstraint
        else:
            raise Exception("Ik Constraint Name cannot be null")
        return None

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getWidth(self):
        return self.width

    def setWidth(self, width):
        self.width = width

    def getHeight(self):
        return self.height

    def setHeight(self, height):
        self.height = height

    def getVersion(self):
        return self.version

    def setVersion(self, version):
        self.version = version

    def getHash(self):
        return self.hash

    def setHash(self, hash):
        self.hash = hash

    def getImagesPath(self):
        return self.imagespath

    def setImagesPath(self, imagesPath):
        self.imagespath = imagesPath

    def toString(self):
        if self.name is not None:
            return self.name
        else:
            return ""
