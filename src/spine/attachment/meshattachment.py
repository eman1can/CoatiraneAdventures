from copy import deepcopy

from kivy.graphics.instructions import InstructionGroup

from src.spine.attachment.attachment import Attachment
from kivy.graphics import Color, Mesh

from src.spine.utils.textureatlas import AtlasRegion


class MeshAttachment(Attachment):

    def __init__(self, name):

        self.region = None
        self.path = None
        self.vertices = None
        self.regionUVs = None
        self.triangles = None
        self.worldVertices = None
        self.color = Color(1, 1, 1, 1)
        self.hullLength = None

        self.edges = []
        self.width, self.height = 0.0, 0.0

        self.mesh = Mesh(mode='triangles', group=name)
        self.group = None
        self.texture_set = False

        super().__init__(name)

    def set_texture(self, texture):
        self.mesh.texture = texture
        self.texture_set = True

    def is_tex_set(self):
        return self.texture_set

    def getMesh(self):
        self.updateMesh()
        return self.mesh

    def updateMesh(self):
        self.mesh.vertices = self.getWorldVertices()
        self.mesh.indices = self.getTriangles()

    def setRegion(self, region):
        if region is None:
            raise Exception("Region cannot be None")
        self.region = region

    def getRegion(self):
        if self.region is None:
            raise Exception(f"Region has not been set: {self}")
        return self.region

    def updateUVs(self):
        verticesLength = len(self.vertices)
        worldVerticesLength = int(verticesLength / 2 * 4)
        if self.worldVertices is None or worldVerticesLength != len(self.worldVertices):
            self.worldVertices = [_ for _ in range(worldVerticesLength)]

        if self.region is None:
            u = v = 0
            width = height = 1
        else:
            u = self.region.getU()
            v = self.region.getV()
            width = self.region.getU2() - u
            height = self.region.getV2() - v
        regionUVs = self.regionUVs
        if isinstance(self.region, AtlasRegion) and self.region.rotate:
            i, w = 0, 2
            while i < verticesLength:
                self.worldVertices[w] = u + regionUVs[i + 1] * width
                self.worldVertices[w + 1] = v + height - regionUVs[i] * height
                i += 2
                w += 4
        else:
            i, w = 0, 2
            while i < verticesLength:
                self.worldVertices[w] = u + regionUVs[i] * width
                self.worldVertices[w + 1] = v + regionUVs[i + 1] * height
                i += 2
                w += 4

    def updateWorldVertices(self, slot, premultipliedAlpha):
        skeleton = slot.getSkeleton()
        skeletonColor = skeleton.getColor()
        slotColor = slot.getColor()
        meshColor = self.color
        a = skeletonColor.a * slotColor.a * meshColor.a * 255
        multiplier = a if premultipliedAlpha else 255
        color = float(((int(a) << 24)
                       | (int(skeletonColor.b * slotColor.b * meshColor.b * multiplier) << 16)
                       | (int(skeletonColor.g * slotColor.g * meshColor.g * multiplier) << 8)
                       | (int(skeletonColor.r * slotColor.r * meshColor.r * multiplier))) & 0xfeffffff)
        slotVertices = slot.getAttachmentVertices()
        vertices = self.vertices
        if len(slotVertices) == len(vertices):
            vertices = slotVertices
        bone = slot.getBone()
        x, y = skeleton.getX() + bone.getWorldX(), skeleton.getY() + bone.getWorldY()
        m00, m01, m10, m11 = bone.getM00(), bone.getM01(), bone.getM10(), bone.getM11()
        v, w, n = 0, 0, len(self.worldVertices)
        while w < n:
            vx = vertices[v]
            vy = vertices[v + 1]
            self.worldVertices[w] = vx * m00 + vy * m01 + x
            self.worldVertices[w + 1] = vx * m10 + vy * m11 + y
            # self.worldVertices[w + 2] = color
            v += 2
            w += 4

    def getWorldVertices(self):
        return self.worldVertices

    def getVertices(self):
        return self.vertices

    def setVertices(self, vertices):
        self.vertices = vertices

    def getTriangles(self):
        return self.triangles

    def setTriangles(self, triangles):
        self.triangles = triangles

    def getRegionUVs(self):
        return self.regionUVs

    def setRegionUVs(self, regionUVs):
        self.regionUVs = regionUVs

    def getColor(self):
        return self.color

    def getPath(self):
        return self.path

    def setPath(self, path):
        self.path = path

    def getHullLength(self):
        return self.hullLength

    def setHullLength(self, hullLength):
        self.hullLength = hullLength

    def getEdges(self):
        return self.edges

    def setEdges(self, edges):
        self.edges = edges

    def getWidth(self):
        return self.width

    def setWidth(self, width):
        self.width = width

    def getHeight(self):
        return self.height

    def setHeight(self, height):
        self.height = height

    def __str__(self):
        return f"<Mesh Attachment: {self.name}>"

    def __deepcopy__(self, memodict={}):
        new_mesh = type(self)(self.name)
        if self.texture_set:
            new_mesh.set_texture(self.mesh.texture)
            self.texture_set = True
        new_mesh.vertices = deepcopy(self.vertices)
        new_mesh.regionUVs = deepcopy(self.regionUVs)
        new_mesh.triangles = deepcopy(self.triangles)
        new_mesh.edges = deepcopy(self.edges)
        new_mesh.region = self.region
        new_mesh.path = self.path
        new_mesh.color = Color(self.color)
        new_mesh.width, new_mesh.height = self.width, self.height