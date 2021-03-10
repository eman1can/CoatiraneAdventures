from math import degrees as Degrees, atan2 as Atan2, sqrt as Sqrt, acos as Acos, sin as Sin

from src.spine.utils import clamp
from src.spine.utils.vector2 import Vector2


class IkConstraint:

    def __init__(self, *args):

        self.temp = Vector2()

        self.data = None
        self.bones = None
        self.target = None
        self.mix = 1
        self.bendDirection = 0

        if len(args) == 2:
            self.data = args[0]
            self.mix = self.data.mix
            self.bendDirection = self.data.bendDirection

            self.bones = []
            if args[1] is not None:
                for boneData in self.data.bones:
                    self.bones.append(args[1].findBone(boneData.name))
                self.target = args[1].findBone(self.data.target.name)
        else:
            ikConstraint, bones, target = args
            self.data = ikConstraint.data
            self.bones = bones.copy()
            self.target = target
            self.mix = ikConstraint.mix
            self.bendDirection = ikConstraint.bendDirection

    def apply(self, *args):
        if len(args) == 0:
            if len(self.bones) == 1:
                self.apply(self.bones[0], self.target.worldX, self.target.worldY, self.mix)
            elif len(self.bones) == 2:
                self.apply(self.bones[0], self.bones[1], self.target.worldX, self.target.worldY, self.bendDirection, self.mix)
        elif len(args) == 4:
            bone, targetX, targetY, alpha = args
            parentRotation = 0 if (not bone.data.inheritRotation or bone.parent is None) else bone.parent.worldRotation
            rotation = bone.rotation
            rotationIK = float(Degrees(Atan2(targetY - bone.worldY, targetX - bone.worldX)) - parentRotation)
            bone.rotationIK = rotation + (rotationIK - rotation) * alpha
        else:
            parent, child, targetX, targetY, bendDirection, alpha = args
            childRotation, parentRotation = child.rotation, parent.rotation
            if alpha == 0:
                child.rotationIK = childRotation
                parent.rotationIK = parentRotation
                return
            position = self.temp
            parentParent = parent.parent
            if parentParent is not None:
                parentParent.worldToLocal(position.set(targetX, targetY))
                targetX = (position.x - parent.x) * parentParent.worldScaleX
                targetY = (position.y - parent.y) * parentParent.worldScaleY
            else:
                targetX -= parent.x
                targetY -= parent.y
            if child.parent == parent:
                position.set(child.x, child.y)
            else:
                parent.worldToLocal(child.parent.localToWorld(position.set(child.x, child.y)))
            childX, childY = position.x * parent.worldScaleX, position.y * parent.worldScaleY
            offset = float(Atan2(childY, childX))
            len1, len2 = float(Sqrt(childX * childX + childY * childY)), child.data.length * child.worldScaleX

            cosDenom = 2 * len1 * len2
            if cosDenom < 0.0001:
                child.rotationIK = childRotation + ((float(Degrees(float(Atan2(targetY, targetX)))) - parentRotation - childRotation) * alpha)
                return
            cos = clamp((targetX * targetX + targetY * targetY - len1 * len1 - len2 * len2) / cosDenom, -1, 1)
            childAngle = Acos(cos) * bendDirection
            adjacent, opposite = len1 + len2 * cos, len2 * Sin(childAngle)
            parentAngle = Atan2(targetY * adjacent - targetX * opposite, targetX * adjacent + targetY * opposite)
            rotation = Degrees(parentAngle - offset) - parentRotation
            if rotation > 180:
                rotation -= 360
            elif rotation < -180:
                rotation += 360
            parent.rotationIK = parentRotation + rotation * alpha
            rotation = Degrees(childAngle + offset) - childRotation
            if rotation > 180:
                rotation -= 360
            elif rotation < -180:
                rotation += 360
            child.rotationIK = childRotation + (rotation + parent.worldRotation - child.parent.worldRotation) * alpha

    def getBones(self):
        return self.bones

    def getTarget(self):
        return self.target

    def setTarget(self, target):
        self.target = target

    def getMix(self):
        return self.mix

    def setMix(self, mix):
        self.mix = mix

    def getBendDirection(self):
        return self.bendDirection

    def setBendDirection(self, bendDirection):
        self.bendDirection = bendDirection

    def getData(self):
        return self.data

    def __str__(self):
        return self.data.name

