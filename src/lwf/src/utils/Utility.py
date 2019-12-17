# Internal Imports
from .Type import ColorTransform, Matrix

from ..objects.Object import IObject

from ..Format import Format
from ..LWF import LWF

# External Imports
import math


class Utility:
    @staticmethod
    def Clear_Array(array, si, ei):
        for x in range(si, ei):
            if isinstance(array[x], IObject):
                array[x] = IObject()
            else:
                raise Exception("Not Implemented!")

    @staticmethod
    def CalcMatrixToPoint(sx, sy, m):
        dx = m.scaleX * sx + m.skew0 * sy + m.translateX
        dy = m.skew1 * sx + m.scaleY * sy + m.translateY
        return dx, dy

    @staticmethod
    def GetMatrixDeterminant(matrix):
        return matrix.scaleX & matrix.scaleY - matrix.skew0 * matrix.skew1 < 0

    @staticmethod
    def SyncMatrix(movie):
        matrixId = movie.matrixId
        scaleX = 1
        scaleY = 1
        rotation = 0
        if (matrixId & int(Format.Constant.MATRIX_FLAG.value)) == 0:
            translate = movie.lwf.data.translates[matrixId]
            matrix = Matrix(scaleX, scaleY, 0, 0, translate.translateX, translate.translateY)
        else:
            matrixId &= ~int(Format.Constant.MATRIX_FLAG_MASK.value.value)
            matrix = movie.lwf.data.matrices[matrixId]
            md = Utility.GetMatrixDeterminant(matrix)
            scaleX = float(math.sqrt(matrix.scaleX * matrix.scaleX + matrix.skew1 * matrix.skew1))
            if md:
                scaleX = -scaleX
            scaleY = float(math.sqrt(matrix.scaleY * matrix.scaleY + matrix.skew0 * matrix.skew0))
            if md:
                rotation = float(math.atan2(matrix.skew1, -matrix.scaleX))
            else:
                rotation = float(math.atan2(matrix.skew1, matrix.scaleX))
            rotation = rotation / float(math.pi) * 180.0
        movie.SetMatrix(matrix, scaleX, scaleY, rotation)

    @staticmethod
    def GetX(movie):
        matrixId = movie.matrixId
        if (matrixId & int(Format.Constant.MATRIX_FLAG.value)) == 0:
            translate = movie.lwf.data.translates[matrixId]
            return translate.translateX
        else:
            matrixId &= ~int(Format.Constant.MATRIX_FLAG_MASK.value.value)
            matrix = movie.lwf.data.matrices[matrixId]
            return matrix.translateX

    @staticmethod
    def GetY(movie):
        matrixId = movie.matrixId
        if (matrixId & int(Format.Constant.MATRIX_FLAG.value)) == 0:
            translate = movie.lwf.data.translates[matrixId]
            return translate.translateY
        else:
            matrixId &= ~int(Format.Constant.MATRIX_FLAG_MASK.value.value)
            matrix = movie.lwf.data.matrices[matrixId]
            return matrix.translateY

    @staticmethod
    def GetScaleX(movie):
        matrixId = movie.matrixId
        if (matrixId & int(Format.Constant.MATRIX_FLAG.value)) == 0:
            return 1
        else:
            matrixId &= ~int(Format.Constant.MATRIX_FLAG_MASK.value.value)
            matrix = movie.lwf.data.matrices[matrixId]
            md = Utility.GetMatrixDeterminant(matrix)
            scaleX = float(math.sqrt(matrix.scaleX * matrix.scaleX + matrix.skew1 * matrix.skew1))
            if md:
                scaleX = -scaleX
            return scaleX

    @staticmethod
    def GetScaleY(movie):
        matrixId = movie.matrixId
        if (matrixId & int(Format.Constant.MATRIX_FLAG.value)) == 0:
            return 1
        else:
            matrixId &= ~int(Format.Constant.MATRIX_FLAG_MASK.value.value)
            matrix = movie.lwf.data.matrices[matrixId]
            scaleY = float(math.sqrt(matrix.scaleY * matrix.scaleY + matrix.skew0 * matrix.skew0))
            return scaleY

    @staticmethod
    def GetRotation(movie):
        matrixId = movie.matrixId
        if (matrixId & int(Format.Constant.MATRIX_FLAG.value)) == 0:
            return 0
        else:
            matrixId &= ~int(Format.Constant.MATRIX_FLAG_MASK.value.value)
            matrix = movie.lwf.data.matrices[matrixId]
            md = Utility.GetMatrixDeterminant(matrix)
            if md:
                rotation = float(math.atan2(matrix.skew1, -matrix.scaleX))
            else:
                rotation = float(math.atan2(matrix.skew1, matrix.scaleX))
            rotation = rotation / float(math.pi) * 180.0
            return rotation

    @staticmethod
    def SyncColorTransform(movie):
        colorTransformId = movie.colorTransformId
        if (colorTransformId & int(Format.Constant.COLORTRANSFORM_FLAG.value)) == 0:
            alphaTransform = movie.lwf.data.alphaTransforms[colorTransformId]
            colorTransform = ColorTransform(1, 1, 1, alphaTransform.alpha)
        else:
            colorTransformId &= ~int(Format.Constant.COLORTRANSFORM_FLAG.value)
            colorTransform = movie.lwf.data.colorTransforms[colorTransformId]
        movie.SetColorTransform(colorTransform)

    @staticmethod
    def GetAlpha(movie):
        colorTransformId = movie.colorTransformId
        if (colorTransformId & int(Format.Constant.COLORTRANSFORM_FLAG.value)) == 0:
            alphaTransform = movie.lwf.data.alphaTransforms[colorTransformId]
            return alphaTransform.alpha
        else:
            colorTransformId &= ~int(Format.Constant.COLORTRANSFORM_FLAG.value)
            colorTransform = movie.lwf.data.colorTransforms[colorTransformId]
        return colorTransform.multi.alpha

    @staticmethod
    def GetRed(movie):
        colorTransformId = movie.colorTransformId
        if (colorTransformId & int(Format.Constant.COLORTRANSFORM_FLAG.value)) == 0:
            return 1
        else:
            colorTransformId &= ~int(Format.Constant.COLORTRANSFORM_FLAG.value)
            colorTransform = movie.lwf.data.colorTransforms[colorTransformId]
        return colorTransform.multi.red

    @staticmethod
    def GetGreen(movie):
        colorTransformId = movie.colorTransformId
        if (colorTransformId & int(Format.Constant.COLORTRANSFORM_FLAG.value)) == 0:
            return 1
        else:
            colorTransformId &= ~int(Format.Constant.COLORTRANSFORM_FLAG.value)
            colorTransform = movie.lwf.data.colorTransforms[colorTransformId]
        return colorTransform.multi.green

    @staticmethod
    def GetBlue(movie):
        colorTransformId = movie.colorTransformId
        if (colorTransformId & int(Format.Constant.COLORTRANSFORM_FLAG.value)) == 0:
            return 1
        else:
            colorTransformId &= ~int(Format.Constant.COLORTRANSFORM_FLAG.value)
            colorTransform = movie.lwf.data.colorTransforms[colorTransformId]
        return colorTransform.multi.blue

    @staticmethod
    def CalcMatrix(*args):
        assert len(args) >= 3
        if isinstance(args[0], LWF):
            lwf = args[0]
            dst = args[1]
            src0 = args[2]
            src1Id = args[3]
            if src1Id == 0:
                dst.Set(src0)
            elif (src1Id & int(Format.Constant.MATRIX_FLAG.value)) == 0:
                translate = lwf.data.translates[src1Id]
                dst.scaleX = src0.scaleX
                dst.skew0 = src0.skew0
                dst.translateX = src0.scaleX * translate.translateX + src0.skew0 * translate.translateY + \
                    src0.translateX
                dst.skew1 = src0.skew1
                dst.scaleY = src0.scaleY
                dst.translateY = src0.skew1 * translate.translateX + src0.scaleY * translate.translateY + \
                    src0.translateY
            else:
                matrixId = src1Id & ~int(Format.Constant.MATRIX_FLAG_MASK.value)
                src1 = lwf.data.matrices[matrixId]
                Utility.CalcMatrix(dst, src0, src1)
            return dst
        else:
            dst = args[0]
            src0 = args[1]
            src1 = args[2]
            dst.scaleX = \
                src0.scaleX * src1.scaleX + \
                src0.skew0 * src1.skew1
            dst.skew0 = \
                src0.scaleX * src1.skew0 + \
                src0.skew0 * src1.scaleY
            dst.translateX = \
                src0.scaleX * src1.translateX + \
                src0.skew0 * src1.translateY + \
                src0.translateX
            dst.skew1 = \
                src0.skew1 * src1.scaleX + \
                src0.scaleY * src1.skew1
            dst.scaleY = \
                src0.skew1 * src1.skew0 + \
                src0.scaleY * src1.scaleY
            dst.translateY = \
                src0.skew1 * src1.translateX + \
                src0.scaleY * src1.translateY + \
                src0.translateY
            return dst

    @staticmethod
    def RotateMatrix(dst, src, scale, offsetX, offsetY):
        offsetX *= scale
        offsetY *= scale
        dst.scaleX = -src.skew0 * scale
        dst.skew0 = src.scaleX * scale
        dst.translateX = src.scaleX * offsetX + src.skew0 * offsetY + src.translateX
        dst.skew1 = -src.scaleY * scale
        dst.scaleY = src.skew1 * scale
        dst.translateY = src.skew1 * offsetX + src.scaleY * offsetY + src.translateY
        return dst

    @staticmethod
    def ScaleMatrix(dst, src, scale, offsetX, offsetY):
        offsetX *= scale
        offsetY *= scale
        dst.scaleX = src.scaleX * scale
        dst.skew0 = src.skew0 * scale
        dst.translateX = src.scaleX * offsetX + src.skew0 * offsetY + src.translateX
        dst.skew1 = src.skew1 * scale
        dst.scaleY = src.scaleY * scale
        dst.translateY = src.skew1 * offsetX + src.scaleY * offsetY + src.translateY

    @staticmethod
    def FitForHeight(lwf, stageHeight):
        scale = stageHeight / lwf.height
        offsetX = -lwf.width / 2 * scale
        offsetY = -lwf.height / 2 * scale
        lwf.lwfproperty.Scale(scale, scale)
        lwf.lwfproperty.Move(offsetX, offsetY)

    @staticmethod
    def FitForWidth(lwf, stageWidth):
        scale = stageWidth / lwf.width
        offsetX = -lwf.width / 2 * scale
        offsetY = -lwf.height / 2 * scale
        lwf.lwfproperty.Scale(scale, scale)
        lwf.lwfproperty.Move(offsetX, offsetY)

    @staticmethod
    def ScaleForHeight(lwf, stageHeight):
        scale = stageHeight / lwf.height
        lwf.lwfproperty.Scale(scale, scale)

    @staticmethod
    def ScaleForWidth(lwf, stageWidth):
        scale = stageWidth / lwf.width
        lwf.lwfproperty.Scale(scale, scale)

    @staticmethod
    def CopyMatrix(dst, src):
        if src is None:
            dst.Clear()
        else:
            dst.Set(src)
        return dst

    @staticmethod
    def InvertMatrix(dst, src):
        dt = src.scaleX * src.scaleY - src.skew0 * src.skew1
        if dt is not 0:
            dst.scaleX = src.scaleY / dt
            dst.skew0 = -src.skew0 / dt
            dst.translateX = (src.skew0 * src.translateY - src.translateX * src.scaleY) / dt
            dst.skew1 = -src.skew1 / dt
            dst.scaleY = src.scaleX / dt
            dst.translateY = (src.translateX * src.skew1 - src.scaleX * src.translateY) / dt
        else:
            dst.Clear()

    @staticmethod
    def CalcColorTransform(*args):
        assert len(args) >= 3
        if isinstance(args[0], LWF):
            lwf = args[0]
            dst = args[1]
            src0 = args[2]
            src1Id = args[3]
            if src1Id is 0:
                dst.Set(src0)
            elif (src1Id & int(Format.Constant.COLORTRANSFORM_FLAG.value)) == 0:
                alphaTransform = lwf.data.alphaTransforms[src1Id]
                dst.multi.red = src0.multi.red
                dst.multi.green = src0.multi.green
                dst.multi.blue = src0.multi.blue
                dst.multi.alpha = src0.multi.alpha * alphaTransform.alpha
                dst.add.Set(src0.add)
            else:
                colorTransformId = src1Id & ~int(Format.Constant.COLORTRANSFORM_FLAG.value)
                src1 = lwf.data.colorTransforms[colorTransformId]
                Utility.CalcColorTransform(dst, src0, src1)
            return dst
        else:
            dst = args[0]
            src0 = args[1]
            src1 = args[2]
            dst.multi.red = src0.multi.red * src1.multi.red
            dst.multi.green = src0.multi.green * src1.multi.green
            dst.multi.blue = src0.multi.blue * src1.multi.blue
            dst.multi.alpha = src0.multi.alpha * src1.multi.alpha
            dst.add.red = src0.add.red * src1.multi.red + src1.add.red
            dst.add.green = src0.add.green * src1.multi.green + src1.add.green
            dst.add.blue = src0.add.blue * src1.multi.blue + src1.add.blue
            dst.add.alpha = src0.add.alpha * src1.multi.alpha + src1.add.alpha
            return dst

    @staticmethod
    def CopyColorTransform(dst, src):
        if src is None:
            dst.Clear()
        else:
            dst.Set(src)
        return dst

    @staticmethod
    def CalcColor(dst, c, t):
            dst.red = c.red * t.multi.red + t.add.red
            dst.green = c.green * t.multi.green + t.add.green
            dst.blue = c.blue * t.multi.blue + t.add.blue
            dst.alpha = c.alpha * t.multi.alpha + t.add.alpha