from src.spine.attachment.attachment import Attachment


class BoundingBoxAttachment(Attachment):

    def __init__(self, name):

        self.vertices = None

        super().__init__(name)

    def computeWorldVertices(self, bone, worldVertices):
        skeleton = bone.getSkeleton()
        x, y = skeleton.getX() + bone.getWorldX(), skeleton.getY() + bone.getWorldY()
        m00, m01, m10, m11 = bone.getM00(), bone.getM01(), bone.getM10(), bone.getM11()
        vertices = self.vertices
        i, n = 0, len(vertices)
        while i < n:
            px, py = vertices[i], vertices[i + 1]
            worldVertices[i] = px * m00 + py * m01 + x
            worldVertices[i + 1] = px * m10 + py * m11 + y
            i += 2

    def getVertices(self):
        return self.vertices

    def setVertices(self, vertices):
        self.vertices = vertices
