from copy import deepcopy

from kivy.graphics.instructions import InstructionGroup

from src.spine.attachment.attachment import Attachment
from kivy.graphics import Color, Mesh

from src.spine.utils.textureatlas import AtlasRegion


class SkinnedMeshAttachment(Attachment):

    def __init__(self, name):

        self.region = None
        self.path = None
        self.bones = None
        self.weights = None
        self.regionUVs = None
        self.triangles = None
        self.worldVertices = None
        self.color = Color(1, 1, 1, 1)
        self.hullLength = 0

        self.edges = None
        self.width = 0
        self.height = 0

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
        regionUVs = self.regionUVs
        verticesLength = len(regionUVs)
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
        worldVertices = self.worldVertices
        x, y = skeleton.getX(), skeleton.getY()
        skeletonBones = skeleton.getBones()
        weights = self.weights
        bones = self.bones

        ffdArray = slot.getAttachmentVertices()
        if len(ffdArray) == 0:
            w, v, b, n = 0, 0, 0, len(bones)
            while v < n:
                wx, wy = 0, 0
                nn = bones[v]
                v += 1
                nn += v
                while v < nn:
                    bone = skeletonBones[bones[v]]
                    vx, vy, weight = weights[b], weights[b + 1], weights[b + 2]
                    wx += (vx * bone.getM00() + vy * bone.getM01() + bone.getWorldX()) * weight
                    wy += (vx * bone.getM10() + vy * bone.getM11() + bone.getWorldY()) * weight
                    v += 1
                    b += 3
                worldVertices[w] = wx + x
                worldVertices[w + 1] = wy + y
                # worldVertices[w + 2] = color
                w += 4
        else:
            ffd = ffdArray
            w, v, b, f, n = 0, 0, 0, 0, len(bones)
            while v < n:
                wx, wy = 0, 0
                nn = bones[v]
                v += 1
                nn += v
                while v < nn:
                    bone = skeletonBones[bones[v]]
                    vx, vy, weight = weights[b] + ffd[f], weights[b + 1] + ffd[f + 1], weights[b + 2]
                    wx += (vx * bone.getM00() + vy * bone.getM01() + bone.getWorldX()) * weight
                    wy += (vx * bone.getM10() + vy * bone.getM11() + bone.getWorldY()) * weight
                    v += 1
                    b += 3
                    f += 2
                worldVertices[w] = wx + x
                worldVertices[w + 1] = wy + y
                # worldVertices[w + 2] = color
                w += 4

    def getWorldVertices(self):
        return self.worldVertices

    def getBones(self):
        return self.bones

    def setBones(self, bones):
        self.bones = bones

    def getWeights(self):
        return self.weights

    def setWeights(self, weights):
        self.weights = weights

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
        return f"<Skinned Mesh Attachment: {self.name}>"

    def __deepcopy__(self, memodict={}):
        new_skmesh = type(self)(self.name)
        if self.texture_set:
            new_skmesh.set_texture(self.mesh.texture)
            self.texture_set = True
        new_skmesh.regionUVs = deepcopy(self.regionUVs)
        new_skmesh.triangles = deepcopy(self.triangles)
        new_skmesh.bones = deepcopy(self.bones)
        new_skmesh.weights = deepcopy(self.weights)
        new_skmesh.edges = deepcopy(self.edges)
        new_skmesh.region = self.region
        new_skmesh.hullLength = self.hullLength
        new_skmesh.path = self.path
        new_skmesh.color = Color(self.color)
        new_skmesh.width, new_skmesh.height = self.width, self.height
