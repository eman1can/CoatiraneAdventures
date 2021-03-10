import math

from src.spine.bone.bonedata import BoneData
from src.spine.utils.matrix3 import Matrix3


class Bone(object):

    def __init__(self, *args):

        self.boneData = None
        self.skeleton = None
        self.parent = None

        self.x = 0.0
        self.y = 0.0
        self.rotation = 0.0
        self.rotationIK = 0.0
        self.scaleX = 1
        self.scaleY = 1
        self.flipX = False
        self.flipY = False

        self.m00 = 0  # a
        self.m01 = 0  # b
        self.worldX = 0  # x
        self.m10 = 0  # c
        self.m11 = 0  # d
        self.worldY = 0  # y

        self.worldRotation = 0.0
        self.worldScaleX = 0.0
        self.worldScaleY = 0.0
        self.worldFlipX = False
        self.worldFlipY = False

        super(Bone, self).__init__()
        if len(args) == 1:
            self.data = args[0]
            self.parent = None
            self.skeleton = None
        else:
            if args[0] is None:
                raise Exception("IllegalArgumentException: data/bone cannot be None")
            if isinstance(args[0], BoneData):
                data, skeleton, parent = args[0], args[1], args[2]
                if skeleton is None:
                    raise Exception("IllegalArgumentException: skeleton cannot be None")
                self.data = data
                self.skeleton = skeleton
                self.parent = parent
                self.setToSetupPose()
            else:
                bone, skeleton, parent = args[0], args[1], args[2]
                self.skeleton = skeleton
                self.parent = parent
                self.data = bone.data
                self.x, self.y = bone.x, bone.y
                self.rotation, self.rotationIK = bone.rotation, bone.rotationIK
                self.scaleX, self.scaleY = bone.scaleX, bone.scaleY
                self.flipX, self.flipY = bone.flipX, bone.flipY

    def updateWorldTransform(self):
        skeleton = self.skeleton
        parent = self.parent
        x, y = self.x, self.y
        if parent:
            self.worldX = x * parent.m00 + y * parent.m01 + parent.worldX
            self.worldY = x * parent.m10 + y * parent.m11 + parent.worldY
            if self.data.inheritScale:
                self.worldScaleX = parent.worldScaleX * self.scaleX
                self.worldScaleY = parent.worldScaleY * self.scaleY
            else:
                self.worldScaleX = self.scaleX
                self.worldScaleY = self.scaleY
            self.worldRotation = (parent.worldRotation + self.rotationIK) if self.data.inheritRotation else self.rotationIK
            self.worldFlipX = parent.worldFlipX ^ self.flipX
            self.worldFlipY = parent.worldFlipY ^ self.flipY
        else:
            skeletonFlipX, skeletonFlipY = skeleton.flipX, skeleton.flipY
            self.worldX = -x if skeletonFlipX else x
            self.worldY = -y if skeletonFlipY else y
            self.worldScaleX = self.scaleX
            self.worldScaleY = self.scaleY
            self.worldRotation = self.rotationIK
            self.worldFlipX = skeletonFlipX ^ self.flipX
            self.worldFlipY = skeletonFlipY ^ self.flipY

        radians = math.radians(self.worldRotation)
        cos = math.cos(radians)
        sin = math.sin(radians)

        if self.worldFlipX:
            self.m00 = -cos * self.worldScaleX
            self.m01 = sin * self.worldScaleY
        else:
            self.m00 = cos * self.worldScaleX
            self.m01 = -sin * self.worldScaleY

        if self.worldFlipY:
            self.m10 = -sin * self.worldScaleX
            self.m11 = -cos * self.worldScaleY
        else:
            self.m10 = sin * self.worldScaleX
            self.m11 = cos * self.worldScaleY

    def setToSetupPose(self):
        data = self.data
        self.x, self.y = data.x, data.y
        self.rotation, self.rotationIK = data.rotation, data.rotation
        self.scaleX, self.scaleY = data.scaleX, data.scaleY
        self.flipX, self.flipY = data.flipX, data.flipY

    def getData(self):
        return self.data

    def getSkeleton(self):
        return self.skeleton

    def getParent(self):
        return self.parent

    def getX(self):
        return self.x

    def setX(self, x):
        self.x = x

    def getY(self):
        return self.y

    def setY(self, y):
        self.y = y

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def getRotation(self):
        return self.rotation

    def setRotation(self, rotation):
        self.rotation = rotation

    def getRotationIK(self):
        return self.rotationIK

    def setRotationIK(self, rotationIK):
        self.rotationIK = rotationIK

    def getScaleX(self):
        return self.scaleX

    def setScaleX(self, scaleX):
        self.scaleX = scaleX

    def getScaleY(self):
        return self.scaleY

    def setScaleY(self, scaleY):
        self.scaleY = scaleY

    def setScale(self, scaleX, scaleY):
        self.scaleX = scaleX
        self.scaleY = scaleY

    def getFlipX(self):
        return self.flipX

    def setFlipX(self, flipX):
        self.flipX = flipX

    def getFlipY(self):
        return self.flipY

    def setFlipY(self, flipY):
        self.flipY = flipY

    def getM00(self):
        return self.m00

    def getM01(self):
        return self.m01

    def getM10(self):
        return self.m10

    def getM11(self):
        return self.m11

    def getWorldX(self):
        return self.worldX

    def getWorldY(self):
        return self.worldY

    def getWorldRotation(self):
        return self.worldRotation

    def getWorldScaleX(self):
        return self.worldScaleX

    def getWorldScaleY(self):
        return self.worldScaleY

    def getWorldFlipX(self):
        return self.worldFlipX

    def getWorldFlipY(self):
        return self.worldFlipY

    def getWorldTransform(self, worldTransform):
        if worldTransform is None:
            raise Exception("IllegalArgumentException: worldTransform cannot be None")
        val = worldTransform.val
        val[Matrix3.M00] = self.m00
        val[Matrix3.M01] = self.m01
        val[Matrix3.M10] = self.m10
        val[Matrix3.M11] = self.m11
        val[Matrix3.M02] = self.worldX
        val[Matrix3.M12] = self.worldY
        val[Matrix3.M20] = 0
        val[Matrix3.M21] = 0
        val[Matrix3.M22] = 1
        return worldTransform

    def worldToLocal(self, world):
        x, y = world.x - self.worldX, world.y - self.worldY
        m00, m10, m01, m11 = self.m00, self.m10, self.m01, self.m11
        if self.worldFlipX is not self.worldFlipY:
            m00 = -m00
            m11 = -m11
        invDet = 1.0 / (m00 * m11 - m01 * m10)
        world.x = x * m00 * invDet - y * m01 * invDet
        world.y = y * m11 * invDet - x * m10 * invDet
        return world

    def localToWorld(self, local):
        x, y = local.x, local.y
        local.x = x * self.m00 + y * self.m01 + self.worldX
        local.y = x * self.m10 + y * self.m11 + self.worldY
        return local

    def __str__(self):
        return self.data.name
