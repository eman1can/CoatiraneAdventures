class SkeletonData:

    def __init__(self):

        self.name = None
        self.bones = []
        self.slots = []
        self.skins = []
        self.defaultSkin = None
        self.events = []
        self.animations = []
        self.ikConstraints = []
        self.width = 0.0
        self.height = 0.0

        self.version = None
        self.hash = None
        self.imagesPath = None

    def getBones(self):
        return self.bones

    def findBone(self, boneName):
        if boneName is None:
            raise Exception("Bone Name cannot be None")
        bones = self.bones
        for i in range(len(bones)):
            bone = bones[i]
            if bone.name == boneName:
                return bone
        return None

    def findBoneIndex(self, boneName):
        if boneName is None:
            raise Exception("Bone Name cannot be None")
        bones = self.bones
        for i in range(len(bones)):
            bone = bones[i]
            if bone.name == boneName:
                return i
        return -1

    def getSlots(self):
        return self.slots

    def findSlot(self, slotName):
        if slotName is None:
            raise Exception("Slot Name cannot be None")
        slots = self.slots
        for i in range(len(slots)):
            slot = slots[i]
            if slot.name == slotName:
                return slot
        return None

    def findSlotIndex(self, slotName):
        if slotName is None:
            raise Exception("Slot Name cannot be None")
        slots = self.slots
        for i in range(len(slots)):
            slot = slots[i]
            if slot.name == slotName:
                return i
        return -1

    def getDefaultSkin(self):
        return self.defaultSkin

    def setDefaultSkin(self, defaultSkin):
        self.defaultSkin = defaultSkin

    def findSkin(self, skinName):
        if skinName is None:
            raise Exception("Slot name cannot be null")
        for skin in self.skins:
            if skin.name == skinName:
                return skin
        return None

    def getSkins(self):
        return self.skins

    def findEvent(self, eventName):
        if eventName is None:
            raise Exception("Event name cannot be null")

        for eventData in self.events:
            if eventData.name == eventName:
                return eventData
        return None

    def getEvents(self):
        return self.events

    def getAnimations(self):
        return self.animations

    def findAnimation(self, animationName):
        if animationName is None:
            raise Exception("animation name cannot be null")

        animations = self.animations
        for i in range(len(animations)):
            animation = animations[i]
            if animation.name == animationName:
                return animation
        return None

    def getIkConstraints(self):
        return self.ikConstraints

    def findIkConstraint(self, ikconstraintName):
        if ikconstraintName is None:
            raise Exception("Ik Constraint Name cannot be null")

        ikConstraints = self.ikConstraints
        for i in range(len(ikConstraints)):
            ikConstraint = ikConstraints[i]
            if ikConstraint.name == ikconstraintName:
                return ikConstraint
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

    def __str__(self):
        return None if self.name is None else super().__str__()
