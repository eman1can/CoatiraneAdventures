from kivy.graphics import Color
from kivy.graphics.instructions import Canvas
from kivy.graphics.opengl import GL_ONE, GL_SRC_ALPHA, GL_BLEND, GL_ONE_MINUS_SRC_ALPHA, glEnable, glBlendFunc
from kivy.graphics.vertex_instructions import Rectangle, Line

from src.spine.attachment.meshattachment import MeshAttachment
from src.spine.attachment.regionattachment import RegionAttachment, X1, X2, X3, X4, Y1, Y2, Y3, Y4
from src.spine.attachment.skinnedmeshattachment import SkinnedMeshAttachment
from src.spine.skeleton.skeletonbounds import SkeletonBounds


class SkeletonRendererDebug:
    boneLineColor = Color(1, 0, 0, 1)
    boneOriginColor = Color(0, 1, 0, 1)
    attachmentLineColor = Color(0, 0, 1, 0.5)
    triangleLineColor = Color(1, 0.64, 0, 0.5)
    boundingBoxColor = Color(0, 1, 0, 0.8)
    aabbColor = Color(0, 1, 0, 0.5)

    def __init__(self, canvas=None):

        self.drawBones = True
        self.drawRegionAttachments = True
        self.drawBoundingBoxes = True
        self.drawMeshHull = True
        self.drawMeshTriangles = True
        self.bounds = SkeletonBounds()
        self.shapes = None
        self.scale = 1
        self.boneWidth = 2
        self.preMultipliedAlpha = False

        if canvas is None:
            self.shapes = Canvas()
        else:
            self.shapes = canvas

    def draw(self, skeleton):
        self.shapes.clear()
        skeletonX = skeleton.getX()
        skeletonY = skeleton.getY()

        glEnable(GL_BLEND)
        srcFunc = GL_ONE if self.preMultipliedAlpha else GL_SRC_ALPHA
        glBlendFunc(srcFunc, GL_ONE_MINUS_SRC_ALPHA)

        bones = skeleton.getBones()
        if self.drawBones:
            self.shapes.add(self.boneLineColor)
            for i in range(len(bones)):
                bone = bones[i]
                if bone.parent is None:
                    continue
                x = skeletonX + bone.data.length * bone.m00 + bone.worldX
                y = skeletonY + bone.data.length * bone.m10 + bone.worldY
                self.shapes.add(Line(points=[skeletonX + bone.worldX, skeletonY + bone.worldY, x, y], width=self.boneWidth * self.scale))
            self.shapes.add(Line(circle=(skeletonX, skeletonY, 4 * self.scale)))

        if self.drawRegionAttachments:
            self.shapes.add(self.attachmentLineColor)
            slots = skeleton.getSlots()
            for i in range(len(slots)):
                slot = slots[i]
                attachment = slot.attachment
                if isinstance(attachment, RegionAttachment):
                    attachment.updateWorldVertices(slot, False)
                    vertices = attachment.getWorldVertices()
                    self.shapes.add(Line(points=([vertices[X1], vertices[Y1], vertices[X2], vertices[Y2]])))
                    self.shapes.add(Line(points=([vertices[X2], vertices[Y2], vertices[X3], vertices[Y3]])))
                    self.shapes.add(Line(points=([vertices[X3], vertices[Y3], vertices[X4], vertices[Y4]])))
                    self.shapes.add(Line(points=([vertices[X4], vertices[Y4], vertices[X1], vertices[Y1]])))

        if self.drawMeshHull or self.drawMeshTriangles:
            slots = skeleton.getSlots()
            for i in range(len(slots)):
                slot = slots[i]
                attachment = slot.attachment
                vertices = None
                triangles = None
                hullLength = 0
                if isinstance(attachment, MeshAttachment):
                    attachment.updateWorldVertices(slot, False)
                    vertices = attachment.getWorldVertices()
                    triangles = attachment.getTriangles()
                    hullLength = attachment.getHullLength()
                elif isinstance(attachment, SkinnedMeshAttachment):
                    attachment.updateWorldVertices(slot, False)
                    vertices = attachment.getWorldVertices()
                    triangles = attachment.getTriangles()
                    hullLength = attachment.getHullLength()
                if vertices is None or triangles is None:
                    continue
                if self.drawMeshTriangles:
                    self.shapes.add(self.triangleLineColor)
                    for ii in range(0, len(triangles), 3):
                        v1, v2, v3 = triangles[ii] * 5, triangles[ii + 1] * 5, triangles[ii + 3] * 5
                        self.shapes.add(Line(points=[vertices[v1], vertices[v1 + 1], vertices[v2], vertices[v2 + 1], vertices[v3], vertices[v3 + 1]]))
                if self.drawMeshHull and hullLength > 0:
                    self.shapes.add(self.attachmentLineColor)
                    hullLength = hullLength / 2 * 5
                    lastX, lastY = vertices[hullLength - 5], vertices[hullLength - 4]
                    for ii in range(0, hullLength, 5):
                        x, y = vertices[ii], vertices[ii + 1]
                        self.shapes.add(Line(points=[x, y, lastX, lastY]))
                        lastX = x
                        lastY = y

        if self.drawBoundingBoxes:
            bounds = self.bounds
            bounds.update(skeleton, True)
            self.shapes.add(self.aabbColor)
            self.shapes.add(Rectangle(x=bounds.getMinX(), y=bounds.getMinY(), width=bounds.getWidth(), height=bounds.getHeight()))
            self.shapes.add(self.boundingBoxColor)
            polygons = bounds.getPolygons()
            for polygon in polygons:
                self.shapes.add(Line(points=polygon))

        if self.drawBones:
            self.shapes.add(self.boneOriginColor)
            for bone in bones:
                self.shapes.add(Color(0, 1, 0, 1))
                self.shapes.add(Line(circle=(skeletonX + bone.worldX, skeletonY + bone.worldY, 3 * self.scale)))
        del bones

    def getShapeRenderer(self):
        return self.shapes

    def setBones(self, bones):
        self.drawBones = bones

    def setScale(self, scale):
        self.scale = scale

    def setRegionAttachments(self, regionAttachments):
        self.drawRegionAttachments = regionAttachments

    def setBoundingBoxes(self, boundingBoxes):
        self.drawBoundingBoxes = boundingBoxes

    def setMeshHull(self, meshHull):
        self.drawMeshHull = meshHull

    def setMeshTriangles(self, meshTriangles):
        self.drawMeshTriangles = meshTriangles

    def setPremultipliedAlpha(self, premultipliedAlpha):
        self.preMultipliedAlpha = premultipliedAlpha