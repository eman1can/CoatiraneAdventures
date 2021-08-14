import copy

from kivy.graphics import Color

from src.spine.bone.bone import Bone
from src.spine.ikconstraint.ikconstraint import IkConstraint
from src.spine.skeleton.skeletondata import SkeletonData
from src.spine.slot.slot import Slot
from src.spine.utils.pool import MAX_VALUE, MIN_VALUE
from src.spine.attachment.regionattachment import RegionAttachment
from src.spine.attachment.meshattachment import MeshAttachment
from src.spine.attachment.skinnedmeshattachment import SkinnedMeshAttachment


class Skeleton:

    def __init__(self, arg):

        self.data = None
        self.clear_color = Color(1, 1, 1, 1)
        self.bones = None
        self.slots = None
        self.drawOrder = None
        self.ikConstraints = None
        self.boneCache = []
        self.skin = None
        self.color = None
        self.time = 0
        self.flipX = False
        self.flipY = False
        self.width = 0
        self.height = 0
        self.x = 0.0
        self.y = 0.0

        super(Skeleton, self).__init__()

        if isinstance(arg, SkeletonData):
            data = arg
            if data is None:
                raise Exception("IllegalArgumentException: data cannot be None")
            self.data = data

            self.bones = []
            for boneData in data.bones:
                parent = None if boneData.parent is None else self.bones[data.bones.index(boneData.parent)]
                self.bones.append(Bone(boneData, self, parent))

            self.slots = []
            self.drawOrder = []
            for slotData in data.slots:
                bone = self.bones[data.bones.index(slotData.boneData)]
                slot = Slot(slotData, bone)
                self.slots.append(slot)
                self.drawOrder.append(slot)

            self.ikConstraints = []
            for ikConstraintData in data.ikConstraints:
                self.ikConstraints.append(IkConstraint(ikConstraintData, self))

            self.color = Color(1, 1, 1, 1)
            self.updateCache()
        else:
            skeleton = arg
            if skeleton is None:
                raise Exception("IllegalArgumentException: skeleton cannot be None")
            self.data = copy.deepcopy(skeleton.data)

            self.bones = []
            bones = copy.deepcopy(skeleton.bones)
            for bone in bones:
                parent = None if bone.parent is None else self.bones[bones.index(bone.parent)]
                self.bones.append(Bone(bone, self, parent))

            self.slots = []
            slots = copy.deepcopy(skeleton.slots)
            for slot in slots:
                bone = self.bones[bones.index(slot.bone)]
                self.slots.append(Slot(slot, bone))

            self.drawOrder = []
            drawOrders = copy.deepcopy(skeleton.drawOrder)
            for slot in drawOrders:
                self.drawOrder.append(self.slots[slots.index(slot)])

            self.ikConstraints = []
            ikConstraints = copy.deepcopy(skeleton.ikConstraints)
            for ikConstraint in ikConstraints:
                target = self.bones[bones.index(ikConstraint.target)]
                ikBones = []
                for bone in ikConstraint.bones:
                    ikBones.append(self.bones[bones.index(bone)])
                self.ikConstraints.append(IkConstraint(ikConstraint, ikBones, target))

            self.skin = copy.deepcopy(skeleton.skin)
            self.color = Color(skeleton.color)
            self.time = skeleton.time
            self.flipX = skeleton.flipX
            self.flipY = skeleton.flipY

            self.updateCache()

    def updateCache(self):
        bones = self.bones
        boneCache = self.boneCache
        ikConstraints = self.ikConstraints
        ikConstraintsCount = len(ikConstraints)

        arrayCount = ikConstraintsCount + 1
        while len(boneCache) < arrayCount:
            boneCache.append([])
        for i in range(arrayCount):
            boneCache[i].clear()

        nonIkBones = boneCache[0]

        class Outer(Exception):
            pass

        outer = Outer()
        for i in range(len(bones)):
            try:
                bone = bones[i]
                current = bone
                while True:
                    for ii in range(ikConstraintsCount):
                        ikConstraint = ikConstraints[ii]
                        parent = ikConstraint.bones[0]
                        child = ikConstraint.bones[len(ikConstraint.bones) - 1]
                        while True:
                            if current == child:
                                boneCache[ii].append(bone)
                                boneCache[ii + 1].append(bone)
                                raise outer
                            if child == parent:
                                break
                            child = child.parent
                    current = current.parent
                    if current is None:
                        break
                nonIkBones.append(bone)
            except Outer:
                continue

    def updateWorldTransform(self):
        bones = self.bones
        for i in range(len(bones)):
            bone = bones[i]
            bone.rotationIK = bone.rotation
        boneCache = self.boneCache
        ikConstraints = self.ikConstraints
        i, last = 0, len(ikConstraints)
        while True:
            updateBones = boneCache[i]
            for ii in range(len(updateBones)):
                updateBones[ii].updateWorldTransform()
            if i == last:
                break
            ikConstraints[i].apply()
            i += 1

    def setToSetupPose(self):
        self.setBonesToSetupPose()
        self.setSlotsToSetupPose()

    def setBonesToSetupPose(self):
        bones = self.bones
        for i in range(len(bones)):
            bones[i].setToSetupPose()

        ikConstraints = self.ikConstraints
        for i in range(len(ikConstraints)):
            ikConstraint = ikConstraints[i]
            ikConstraint.bendDirection = ikConstraint.data.bendDirection
            ikConstraint.mix = ikConstraint.data.mix

    def setSlotsToSetupPose(self):
        slots = self.slots
        self.drawOrder = slots.copy()
        for i in range(len(slots)):
            slots[i].setToSetupPose(i)

    def getData(self):
        return self.data

    def getBones(self):
        return self.bones

    def getRootBones(self):
        if len(self.bones) == 0:
            return None
        return self.bones[0]

    def findBone(self, boneName):
        if boneName is None:
            raise Exception("IllegalArgumentException: boneName cannot be null")
        bones = self.bones
        for i in range(len(bones)):
            bone = bones[i]
            if bone.data.name == boneName:
                return bone
        return None

    def findBoneIndex(self, boneName):
        if boneName is None:
            raise Exception("IllegalArgumentException: boneName cannot be null")
        bones = self.bones
        for i in range(len(bones)):
            bone = bones[i]
            if bone.data.name == boneName:
                return i
        return -1

    def getSlots(self):
        return self.slots

    def findSlot(self, slotName):
        if slotName is None:
            raise Exception("IllegalArgumentException: slotName cannot be null")
        slots = self.slots
        for i in range(len(slots)):
            slot = slots[i]
            if slot.data.name == slotName:
                return slot
        return None

    def findSlotIndex(self, slotName):
        if slotName is None:
            raise Exception("IllegalArgumentException: slotName cannot be null")
        slots = self.slots
        for i in range(len(slots)):
            slot = slots[i]
            if slot.data.name == slotName:
                return i
        return -1

    def getDrawOrder(self):
        return self.drawOrder

    def setDrawOrder(self, drawOrder):
        self.drawOrder = drawOrder

    def getSkin(self):
        return self.skin

    def setSkin(self, arg):
        if isinstance(arg, str):
            skinName = arg
            skin = self.data.findSkin(skinName)
            if skin is None:
                raise Exception(f"IllegalArgumentException: Skin not found: {skinName}")
            self.setSkin(skin)
        else:
            newSkin = arg
            if newSkin is not None:
                if self.skin is not None:
                    newSkin.attachAll(self, self.skin)
                else:
                    for i, slot in enumerate(self.slots):
                        name = slot.data.attachmentName
                        if name is not None:
                            attachment = newSkin.getAttachment(i, name)
                            if attachment is not None:
                                slot.setAttachment(attachment)
            self.skin = newSkin

    def getAttachment(self, arg, attachmentName):
        if isinstance(arg, str):
            slotName = arg
            return self.getAttachment(self.data.findSlotIndex(slotName), attachmentName)
        else:
            slotIndex = arg
            if attachmentName is None:
                raise Exception("IllegalArgumentException: attachmentName cannot be None")
            if self.skin is not None:
                attachment = self.skin.getAttachment(slotIndex, attachmentName)
                if attachment is not None:
                    return attachment
            if self.data.defaultSkin is not None:
                return self.data.defaultSkin.getAttachment(slotIndex, attachmentName)
            return None

    def setAttachment(self, slotName, attachmentName):
        if slotName is None:
            raise Exception("IllegalArgumentException: slotName cannot be None")
        slots = self.slots
        for i in range(len(slots)):
            slot = slots[i]
            if slot.data.name == slotName:
                attachment = None
                if attachmentName is not None:
                    attachment = self.getAttachment(i, attachmentName)
                    if attachment is None:
                        raise Exception(f"IllegalArgumentException: Attachment not found: {attachmentName}, for slot: {slotName}")
                slot.setAttachment(attachment)
                return
        raise Exception(f"IllegalArgumentException: slot not found: {slotName}")

    def getIkConstraints(self):
        return self.ikConstraints

    def findIkConstraint(self, ikConstraintName):
        if ikConstraintName is None:
            raise Exception("IllegalArgumentException: ikConstraintName cannot be None")
        ikConstraints = self.ikConstraints
        for i in range(len(ikConstraints)):
            ikConstraint = ikConstraints[i]
            if ikConstraint.data.name == ikConstraintName:
                return ikConstraint
        return None

    def getBounds(self, offset, size):
        drawOrder = self.drawOrder
        minX, minY, maxX, maxY = MAX_VALUE, MAX_VALUE, MIN_VALUE, MIN_VALUE
        for i in range(len(drawOrder)):
            slot = drawOrder[i]
            vertices = None
            attachment = slot.attachment
            if isinstance(attachment, RegionAttachment):
                attachment.updateWorldVertices(slot, False)
                vertices = attachment.getWorldVertices()
            elif isinstance(attachment, MeshAttachment):
                attachment.updateWorldVertices(slot, True)
                vertices = attachment.getWorldVertices()
            elif isinstance(attachment, SkinnedMeshAttachment):
                attachment.updateWorldVertices(slot, True)
                vertices = attachment.getWorldVertices()
            if vertices is not None:
                for ii in range(0, len(vertices), 5):
                    x, y = vertices[ii], vertices[ii + 1]

                    minX = min(minX, x)
                    minY = min(minY, y)
                    maxX = max(maxX, x)
                    maxY = max(maxY, y)
        offset.set(minX, minY)
        size.set(maxX - minX, maxY - minY)

    def getColor(self):
        return self.color

    def setColor(self, color):
        self.color.rgba = color.rgba

    def getFlipX(self):
        return self.flipX

    def setFlipX(self, flipX):
        self.flipX = flipX

    def getFlipY(self):
        return self.flipY

    def setFlipY(self, flipY):
        self.flipY = flipY

    def setFlip(self, flipX, flipY):
        self.flipX = flipX
        self.flipY = flipY

    def getX(self):
        return self.x

    def setX(self, x):
        self.x = x

    def getY(self):
        return self.y

    def setY(self, y):
        self.y = y

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def getSize(self):
        return self.width, self.height

    def setHeight(self, height):
        self.height = height

    def setWidth(self, width):
        self.width = width

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def getTime(self):
        return self.time

    def setTime(self, time):
        self.time = time

    def update(self, delta):
        self.time += delta
        del delta

    def __str__(self):
        return super().__str__() if self.data.name is None else self.data.name
