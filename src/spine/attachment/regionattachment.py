from copy import deepcopy

from kivy.graphics.instructions import InstructionGroup

from src.spine.attachment.attachment import Attachment
from src.spine.utils.textureatlas import AtlasRegion
from kivy.graphics import Color, Mesh
from math import cos as Cos, sin as Sin, radians as Radians

X1 = 0
Y1 = 1
U1 = 2
V1 = 3
X2 = 4
Y2 = 5
U2 = 6
V2 = 7
X3 = 8
Y3 = 9
U3 = 10
V3 = 11
X4 = 12
Y4 = 13
U4 = 14
V4 = 15


class RegionAttachment(Attachment):
    BLX = 0
    BLY = 1
    ULX = 2
    ULY = 3
    URX = 4
    URY = 5
    BRX = 6
    BRY = 7

    def __init__(self, name):

        self.region = None
        self.path = None
        self.x, self.y, self.scaleX, self.scaleY, self.rotation, self.width, self.height = 0, 0, 1, 1, 0, 0, 0
        self.vertices = [_ for _ in range(16)]
        self.offset = [_ for _ in range(8)]
        self.color = Color(1, 1, 1, 1)

        self.mesh = Mesh(mode='triangle_fan', group=name)
        self.mesh.indices = [0, 1, 2, 2, 3, 0]
        self.group = None
        self.texture_set = False

        super().__init__(name)

    def getMesh(self):
        self.updateMesh()
        return self.mesh

    def updateMesh(self):
        self.mesh.vertices = self.getWorldVertices()

    def set_texture(self, texture):
        self.mesh.texture = texture
        self.texture_set = True

    def is_tex_set(self):
        return self.texture_set

    def updateOffset(self):
        width = self.getWidth()
        height = self.getHeight()
        localX2 = width / 2.0
        localY2 = height / 2.0
        localX = -localX2
        localY = -localY2

        if isinstance(self.region, AtlasRegion):
            region = self.region
            if self.region.rotate:
                localX += region.offsetX / region.originalWidth * width
                localY += region.offsetY / region.originalHeight * height
                localX2 -= (region.originalWidth - region.offsetX - region.packedHeight) / region.originalWidth * width
                localY2 -= (region.originalHeight - region.offsetY - region.packedWidth) / region.originalHeight * height
            else:
                localX += region.offsetX / region.originalWidth * width
                localY += region.offsetY / region.originalHeight * height
                localX2 -= (region.originalWidth - region.offsetX - region.packedWidth) / region.originalWidth * width
                localY2 -= (region.originalHeight - region.offsetY - region.packedHeight) / region.originalHeight * height
        scaleX = self.getScaleX()
        scaleY = self.getScaleY()
        localX *= scaleX
        localY *= scaleY
        localX2 *= scaleX
        localY2 *= scaleY
        rotation = self.getRotation()
        radians = Radians(rotation)
        cos = Cos(radians)
        sin = Sin(radians)
        x = self.getX()
        y = self.getY()
        localXCos = localX * cos + x
        localXSin = localX * sin
        localYCos = localY * cos + y
        localYSin = localY * sin
        localX2Cos = localX2 * cos + self.x
        localX2Sin = localX2 * sin
        localY2Cos = localY2 * cos + self.y
        localY2Sin = localY2 * sin
        self.offset[self.BLX] = localXCos - localYSin
        self.offset[self.BLY] = localYCos + localXSin
        self.offset[self.ULX] = localXCos - localY2Sin
        self.offset[self.ULY] = localY2Cos + localXSin
        self.offset[self.URX] = localX2Cos - localY2Sin
        self.offset[self.URY] = localY2Cos + localX2Sin
        self.offset[self.BRX] = localX2Cos - localYSin
        self.offset[self.BRY] = localYCos + localX2Sin

    def setRegion(self, region):
        if region is None:
            raise Exception("Region cannot be None")
        if region.rotate:
            self.vertices[U3] = region.getU()
            self.vertices[V3] = region.getV2()
            self.vertices[U4] = region.getU()
            self.vertices[V4] = region.getV()
            self.vertices[U1] = region.getU2()
            self.vertices[V1] = region.getV()
            self.vertices[U2] = region.getU2()
            self.vertices[V2] = region.getV2()
        else:
            self.vertices[U2] = region.getU()
            self.vertices[V2] = region.getV2()
            self.vertices[U3] = region.getU()
            self.vertices[V3] = region.getV()
            self.vertices[U4] = region.getU2()
            self.vertices[V4] = region.getV()
            self.vertices[U1] = region.getU2()
            self.vertices[V1] = region.getV2()
        self.region = region

    def getRegion(self):
        if self.region is None:
            raise Exception(f"Region has noe been set: {self}")
        return self.region

    def updateWorldVertices(self, slot, premultipliedAlpha):
        skeleton = slot.getSkeleton()
        skeletonColor = skeleton.getColor()
        slotColor = slot.getColor()
        regionColor = self.color
        a = skeletonColor.a * slotColor.a * regionColor.a * 255
        multiplier = a if premultipliedAlpha else 255
        color = float(((int(a) << 24)
                       | (int(skeletonColor.b * slotColor.b * regionColor.b * multiplier) << 16)
                       | (int(skeletonColor.g * slotColor.g * regionColor.g * multiplier) << 8)
                       | (int(skeletonColor.r * slotColor.r * regionColor.r * multiplier))) & 0xfeffffff)
        offset = self.offset
        bone = slot.getBone()
        x, y = skeleton.getX() + bone.getWorldX(), skeleton.getY() + bone.getWorldY()
        m00, m01, m10, m11 = bone.getM00(), bone.getM01(), bone.getM10(), bone.getM11()

        offsetX = offset[self.BRX]
        offsetY = offset[self.BRY]
        self.vertices[X1] = offsetX * m00 + offsetY * m01 + x
        self.vertices[Y1] = offsetX * m10 + offsetY * m11 + y
        # self.vertices[C1] = color

        offsetX = offset[self.BLX]
        offsetY = offset[self.BLY]
        self.vertices[X2] = offsetX * m00 + offsetY * m01 + x
        self.vertices[Y2] = offsetX * m10 + offsetY * m11 + y
        # self.vertices[C2] = color

        offsetX = offset[self.ULX]
        offsetY = offset[self.ULY]
        self.vertices[X3] = offsetX * m00 + offsetY * m01 + x
        self.vertices[Y3] = offsetX * m10 + offsetY * m11 + y
        # self.vertices[C3] = color

        offsetX = offset[self.URX]
        offsetY = offset[self.URY]
        self.vertices[X4] = offsetX * m00 + offsetY * m01 + x
        self.vertices[Y4] = offsetX * m10 + offsetY * m11 + y
        # self.vertices[C4] = color

    def getWorldVertices(self):
        return self.vertices

    def getOffset(self):
        return self.offset

    def getX(self):
        return self.x

    def setX(self, x):
        self.x = x

    def getY(self):
        return self.y

    def setY(self, y):
        self.y = y

    def getScaleX(self):
        return self.scaleX

    def setScaleX(self, scaleX):
        self.scaleX = scaleX

    def getScaleY(self):
        return self.scaleY

    def setScaleY(self, scaleY):
        self.scaleY = scaleY

    def getRotation(self):
        return self.rotation

    def setRotation(self, rotation):
        self.rotation = rotation

    def getWidth(self):
        return self.width

    def setWidth(self, width):
        self.width = width

    def getHeight(self):
        return self.height

    def setHeight(self, height):
        self.height = height

    def getColor(self):
        return self.color

    def getPath(self):
        return self.path

    def setPath(self, path):
        self.path = path

    def __str__(self):
        return f"<Region Attachment: {self.name}>"

    def __deepcopy__(self, memodict={}):
        new_region = type(self)(self.name)
        if self.texture_set:
            new_region.set_texture(self.mesh.texture)
            self.texture_set = True
        new_region.vertices = deepcopy(self.vertices)
        new_region.offset = deepcopy(self.offset)
        new_region.region = self.region
        new_region.path = self.path
        new_region.color = Color(self.color)
        new_region.x, new_region.y, new_region.scaleX, new_region.scaleY, new_region.rotation, new_region.width, new_region.height = self.x, self.y, self.scaleX, self.scaleY, self.rotation, self.width, self.height



