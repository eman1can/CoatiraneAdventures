from src.spine.utils.gl.disposable import Disposable
from src.spine.utils.gl.vertexattribute import VertexAttributes


class VertexData(Disposable):
    def getNumVertices(self):
        pass

    def getNumMaxVertices(self):
        pass

    def getAttributes(self):
        pass

    def setVertices(self, vertices, offset, count):
        pass

    def updateVertices(self, targetOffset, vertices, sourceOffset, count):
        pass

    def getBuffer(self):
        pass

    def bind(self, shader, locations=None):
        pass

    def unbind(self, shader, locations=None):
        pass

    def invalidate(self):
        pass

    def dispose(self):
        pass


class VertexArray(VertexData):
    def __init__(self, numVertices, *attributes):
        self.attributes = None
        self.buffer = None
        self.byteBuffer = None
        self.isBound = False

        self.attributes = VertexAttributes(*attributes)
        # self.byteBuffer = newUnsafeByteBuffer(self.attributes.vertexSize * numVertices)
        # self.buffer = self.byteBuffer.asFloatBuffer()
        # self.buffer.flip()
        # self.byteBuffer.flip()

    def dispose(self):
        disposeUnsafeByteBuffer(self.byteBuffer)

    def getBuffer(self):
        return self.buffer

    def getNumVertices(self):
        return self.buffer.limit() * 4 / self.attributes.vertexSize

    def getNumMaxVertices(self):
        return self.byteBuffer.capacity() / self.attributes.vertexSize

    def setVertices(self, vertices, offset, count):
        copy(vertices, self.byteBuffer, count, offset)
        self.buffer.position(0)
        self.buffer.limit(count)

    def bind(self, shader, locations=None):
        numAttributes = len(self.attributes)
        self.byteBuffer.limit(self.buffer.limit() * 4)
        if locations is None:
            for i in range(numAttributes):
                attribute = self.attributes.get(i)
                location = shader.getAttributeLocation(attribute.alias)
                if location < 0:
                    continue
                shader.enableVertexAttribute(location)

                if attribute.type == GL_FLOAT:
                    self.buffer.position(attribute.offset / 4)
                    shader.setVertexAttribute(location, attribute.numComponents, attribute.type, attribute.normalized, self.attributes.vertexSize, self.buffer)
                else:
                    self.byteBuffer.position(attribute.offset)
                    shader.setVertexAttribute(location, attribute.numComponents, attribute.type, attribute.normalized, self.attributes.vertexSize, self.byteBuffer)
        else:
            for i in range(numAttributes):
                attribute = self.attributes.get(i)
                location = locations[i]
                if location < 0:
                    continue
                shader.enableVertexAttribute(location)

                if attribute.type == GL_FLOAT:
                    self.buffer.position(attribute.offset / 4)
                    shader.setVertexAttribute(location, attribute.numComponents, attribute.type, attribute.normalized, self.attributes.vertexSize, self.buffer)
                else:
                    self.byteBuffer.position(attribute.offset)
                    shader.setVertexAttribute(location, attribute.numComponents, attribute.type, attribute.normalized, self.attributes.vertexSize, self.byteBuffer)
        self.isBound = True

    def unbind(self, shader, locations=None):
        numAttributes = len(self.attributes)
        if locations is None:
            for i in range(numAttributes):
                shader.disableVertexAttribute(self.attributes.get(i).alias)
        else:
            for i in range(numAttributes):
                location = locations[i]
                if location >= 0:
                    shader.disableVertexAttribute(location)
        self.isBound = False

    def getAttributes(self):
        return self.attributes

    def invalidate(self):
        pass