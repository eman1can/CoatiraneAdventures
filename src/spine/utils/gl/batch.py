from src.spine.utils.gl.disposable import Disposable


class Batch(Disposable):
    def begin(self):
        pass

    def end(self):
        pass

    def setColor(self, *args):
        pass

    def getColor(self):
        pass

    def setPackedColor(self, packedColor):
        pass

    def getPackedColor(self):
        pass

    def draw(self, *args):
        pass

    def flush(self):
        pass

    def disableBlending(self):
        pass

    def enableBlending(self):
        pass

    def setBendFunction(self, srcFunc, dstFunc):
        pass

    def setBlendFunctionSeparate(self, srcFuncColor, dstFuncColor, srcFuncAlpha, dstFuncAlpha):
        pass

    def getBlendSrcFunc(self):
        pass

    def getBlendDstFunc(self):
        pass

    def getBlendSrcFuncAlpha(self):
        pass

    def getBlendDstFuncAlpha(self):
        pass

    def getProjectionMatrix(self):
        pass

    def getTransformationMatrix(self):
        pass

    def setProjectionMatrix(self, projection):
        pass

    def setTransformationMatrix(self, transformation):
        pass

    def setShader(self, shader):
        pass

    def getShader(self):
        pass

    def isBlendingEnabled(self):
        pass

    def isDrawing(self):
        pass

    X1 = 0
    Y1 = 1
    C1 = 2
    U1 = 3
    V1 = 4
    X2 = 5
    Y2 = 6
    C2 = 7
    U2 = 8
    V2 = 9
    X3 = 10
    Y3 = 11
    C3 = 12
    U3 = 13
    V3 = 14
    X4 = 15
    Y4 = 16
    C4 = 17
    U4 = 18
    V4 = 19


class PolygonBatch(Batch):
    def draw(self, *args):
        pass
