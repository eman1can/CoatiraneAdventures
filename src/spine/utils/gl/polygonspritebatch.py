import struct

from kivy.app import App
from kivy.graphics.context_instructions import Color
from kivy.graphics.opengl import GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, glDepthMask, glDisable, GL_TRIANGLES, GL_BLEND, glEnable, glBlendFuncSeparate

from src.spine.utils.gl.batch import PolygonBatch
from src.spine.utils.gl.mesh import Mesh
from src.spine.utils.gl.spritebatch import SpriteBatch
from src.spine.utils.gl.vertexattribute import VertexAttribute, Usage, ShaderProgram
from src.spine.utils.matrix4 import Matrix4

VERTEX_SIZE = 2 + 1 + 2


def color_to_float_bits(color):
    color_int = (int(255 * color.a) << 24) | (int(255 * color.b) << 16) | (int(255 * color.g) << 8) | (int(255 * color.r))
    int_bits = color_int & 0xfeffffff
    return struct.unpack('<f', struct.pack('<I', int_bits))[0]


def abgr8888ToColor(color, value):
    c = struct.unpack('>l', struct.pack('>f', value))[0]
    color.a = ((c & 0xff000000) >> 24) / 255
    color.b = ((c & 0x00ff0000) >> 16) / 255
    color.g = ((c & 0x0000ff00) >> 8) / 255
    color.r = (c & 0x000000ff) / 255


class PolygonSpriteBatch(PolygonBatch):
    def __init__(self, *args):
        self.mesh = None
        self.vertices = None
        self.triangles = None
        self.vertexIndex = 0
        self.triangleIndex = 0
        self.lastTexture = None
        self.invTexWidth = 0.0
        self.invTexHeight = 0.0
        self.drawing = False

        self.transformationMatrix = Matrix4()
        self.projectionMatrix = Matrix4()
        self.combinedMatrix = Matrix4()

        self.blendingDisabled = False
        self.blendSrcFunc = GL_SRC_ALPHA
        self.blendDstFunc = GL_ONE_MINUS_SRC_ALPHA
        self.blendSrcFuncAlpha = GL_SRC_ALPHA
        self.blendDstFuncAlpha = GL_ONE_MINUS_SRC_ALPHA

        self.shader = None
        self.customShader = None
        self.ownsShader = False

        self.color = Color(1, 1, 1, 1)
        self.colorPacked = color_to_float_bits(Color(1, 1, 1, 1))

        self.renderCalls = 0
        self.totalRenderCalls = 0
        self.maxTrianglesInBatch = 0

        if len(args) == 0:
            args = [2000, None]
        if len(args) == 1:
            args = [args[0], args[0] * 2, None]
        if len(args) == 2:
            args = [args[0], args[0] * 2, args[1]]

        if args[0] > 32767:
            raise Exception("You cannot have more than 32767 vertices per batch!")

        self.mesh = Mesh(Mesh.VertexDataType.VertexArray, False, args[0], args[1] * 3,
                         VertexAttribute(Usage.Position, 2, ShaderProgram.POSITION_ATTRIBUTE),
                         VertexAttribute(Usage.ColorPacked, 4, ShaderProgram.COLOR_ATTRIBUTE),
                         VertexAttribute(Usage.TextureCoordinates, 2, ShaderProgram.TEXCOORD_ATTRIBUTE + "0"))

        self.vertices = [0.0 * (args[0] * VERTEX_SIZE)]
        self.triangles = [0 * (args[1] * 3)]

        if args[2] is None:
            self.shader = SpriteBatch.createDefaultShader()
            self.ownsShader = True
        else:
            self.shader = args[2]

        self.projectionMatrix.setToOrtho2D(0, 0, App.get_running_app().width, App.get_running_app().height)

    def begin(self):
        if self.drawing:
            raise Exception("PolygonSpriteBatch.end must be called before begin.")
        self.renderCalls = 0

        glDepthMask(False)
        if self.customShader is not None:
            self.customShader.begin()
        else:
            self.shader.begin()
        self.setupMatrices()

        self.drawing = True

    def end(self):
        if not self.drawing:
            raise Exception("PolygonSpriteBatch.begin must be called before end.")
        if self.vertexIndex > 0:
            self.flush()
        self.lastTexture = None
        self.drawing = False

        glDepthMask(True)
        if self.isBlendingEnabled():
            glDisable(GL_BLEND)

        if self.customShader is not None:
            self.customShader.end()
        else:
            self.shader.end()

    def setColor(self, *args):
        if len(args) == 1:
            tint = args[0]
            self.color.r = tint.r
            self.color.g = tint.g
            self.color.b = tint.b
            self.color.a = tint.a

            self.colorPacked = color_to_float_bits(tint)
        elif len(args) == 4:
            self.color.r = args[0]
            self.color.g = args[1]
            self.color.b = args[2]
            self.color.a = args[3]

    def setPackedColor(self, packedColor):
        abgr8888ToColor(self.color, packedColor)
        self.colorPacked = packedColor

    def getColor(self):
        return self.color

    def getPackedColor(self):
        return self.colorPacked

    def draw(self, texture, polygonVertices, verticesOffset, verticesCount, polygonTriangles, trianglesOffset, trianglesCount):
        if not self.drawing:
            raise Exception("PolygonSpriteBatch.begin must be called before draw.")

        if texture != self.lastTexture:
            self.switchTexture(texture)
        elif self.triangleIndex + trianglesCount > len(self.triangles) or self.vertexIndex + verticesCount > len(self.vertices):
            self.flush()

        startVertex = self.vertexIndex / VERTEX_SIZE

        for i in range(trianglesOffset, trianglesOffset + trianglesCount):
            self.triangles[self.triangleIndex] = int(polygonTriangles[i] + startVertex)
            self.triangleIndex += 1

        for x, y in range(verticesOffset, verticesOffset + verticesCount), range(self.vertexIndex, self.vertexIndex + verticesCount):
            self.vertices[x] = polygonVertices[y]
        self.vertexIndex += verticesCount

    def flush(self):
        if self.vertexIndex == 0:
            return

        self.renderCalls += 1
        self.totalRenderCalls += 1
        trianglesInBatch = self.triangleIndex
        if trianglesInBatch > self.maxTrianglesInBatch:
            self.maxTrianglesInBatch = trianglesInBatch

        self.lastTexture.bind()
        self.mesh.setVertices(self.vertices, 0, self.vertexIndex)
        self.mesh.setIndices(self.triangles, 0, trianglesInBatch)
        if self.blendingDisabled:
            glDisable(GL_BLEND)
        else:
            glEnable(GL_BLEND)
            if self.blendSrcFunc != -1:
                glBlendFuncSeparate(self.blendSrcFunc, self.blendDstFunc, self.blendSrcFuncAlpha, self.blendDstFuncAlpha)

        self.mesh.render(self.customShader if self.customShader is not None else self.shader, GL_TRIANGLES, 0, trianglesInBatch)

        self.vertexIndex = 0
        self.triangleIndex = 0

    def disableBlending(self):
        self.flush()
        self.blendingDisabled = True

    def enableBlending(self):
        self.flush()
        self.blendingDisabled = False

    def setBendFunction(self, srcFunc, dstFunc):
        self.setBlendFunctionSeparate(srcFunc, dstFunc, srcFunc, dstFunc)

    def setBlendFunctionSeparate(self, srcFuncColor, dstFuncColor, srcFuncAlpha, dstFuncAlpha):
        if self.blendSrcFunc == srcFuncColor and self.blendDstFunc == dstFuncColor and self.blendSrcFuncAlpha == srcFuncAlpha and self.blendDstFuncAlpha == dstFuncAlpha:
            return

        self.flush()
        self.blendSrcFunc = srcFuncColor
        self.blendDstFunc = dstFuncColor
        self.blendSrcFuncAlpha = srcFuncAlpha
        self.blendDstFuncAlpha = dstFuncAlpha

    def getBlendSrcFunc(self):
        return self.blendSrcFunc

    def getBlendDstFunc(self):
        return self.blendDstFunc

    def getBlendSrcFuncAlpha(self):
        return self.blendSrcFuncAlpha

    def getBlendDstFuncAlpha(self):
        return self.blendDstFuncAlpha

    def dispose(self):
        self.mesh.dispose()
        if self.ownsShader and self.shader is not None:
            self.shader.dispose()

    def getProjectionMatrix(self):
        return self.projectionMatrix

    def getTransformationMatrix(self):
        return self.transformationMatrix

    def setProjectionMatrix(self, projection):
        if self.drawing:
            self.flush()
        self.projectionMatrix.set(projection)
        if self.drawing:
            self.setupMatrices()

    def setTransformationMatrix(self, transformation):
        if self.drawing:
            self.flush()
        self.transformationMatrix.set(transformation)
        if self.drawing:
            self.setupMatrices()

    def setupMatrices(self):
        self.combinedMatrix.set(self.projectionMatrix).mul(self.transformationMatrix)
        if self.customShader is not None:
            self.customShader.setUniformMatrix('u_projTrans', self.combinedMatrix)
            self.customShader.setUniform('u_texture', 0)
        else:
            self.shader.setUniformMatrix('u_projTrans', self.combinedMatrix)
            self.shader.setUniform('u_texture', 0)

    def switchTexture(self, texture):
        self.flush()
        self.lastTexture = texture
        self.invTexWidth = 1 / texture.getWidth()
        self.invTexHeight = 1 / texture.getHeight()

    def setShader(self, shader):
        if self.drawing:
            self.flush()
            if self.customShader is not None:
                self.customShader.end()
            else:
                self.shader.end()
        self.customShader = shader
        if self.drawing:
            if self.customShader is not None:
                self.customShader.begin()
            else:
                self.shader.begin()
            self.setupMatrices()

    def getShader(self):
        if self.customShader is None:
            return self.shader
        return self.customShader

    def isBlendingEnabled(self):
        return not self.blendingDisabled

    def isDrawing(self):
        return self.drawing
