class IndexData:
    def getNumIndices(self):
        pass

    def getNumMaxIndices(self):
        pass

    def setIndices(self, indices, offset, count):
        pass

    def updateIndices(self, targetOffset, indices, sourceOffset, count):
        pass

    def getBuffer(self):
        pass

    def bind(self, shader):
        pass

    def unbind(self, shader):
        pass

    def invalidate(self):
        pass

    def dispose(self):
        pass


class IndexArray(IndexData):
    def __init__(self, maxIndices):
        self.empty = maxIndices == 0
        if self.empty:
            maxIndices = 1

        # self.byteBuffer = newUnsafeByteBugger(maxIndices * 2)
        # self.buffer = self.byteBuffer.asShortBuffer()
        # self.buffer.flip()
        # self.byteBuffer.flip()