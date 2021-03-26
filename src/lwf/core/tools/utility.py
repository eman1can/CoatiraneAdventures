__all__ = ('Utility',)

from math import atan2, pi, sqrt

from ..format import Constant
from ..type import ColorTransform, Matrix


class Utility:
    @staticmethod
    def calc_matrix_to_point(sx, sy, m):
        dx = m.scale_x * sx + m.skew_0 * sy + m.translate_x
        dy = m.skew_1 * sx + m.scale_y * sy + m.translate_y
        return dx, dy

    @staticmethod
    def get_matrix_determinant(matrix):
        return matrix.scale_x * matrix.scale_y - matrix.skew_0 * matrix.skew_1 < 0

    @staticmethod
    def sync_matrix(movie):
        matrix_id = movie.matrix_id
        scale_x = 1
        scale_y = 1
        rotation = 0
        matrix = Matrix()
        if (matrix_id & Constant.MATRIX_FLAG) == 0:
            translate = movie.lwf.data.translates[matrix_id]
            matrix.set(scale_x, scale_y, 0, 0, translate.translate_x, translate.translate_y)
        else:
            matrix_id &= ~-Constant.MATRIX_FLAG_MASK
            matrix.set(movie.lwf.data.matrices[matrix_id])
            md = bool(Utility.get_matrix_determinant(matrix))
            scale_x = sqrt(matrix.scale_x * matrix.scale_x + matrix.skew_1 * matrix.skew_1)
            if md:
                scale_x = -scale_x
            scale_y = sqrt(matrix.scale_y * matrix.scale_y + matrix.skew_0 * matrix.skew_0)
            if md:
                rotation = atan2(matrix.skew_1, -matrix.scale_x)
            else:
                rotation = atan2(matrix.skew_1, matrix.scale_x)
            rotation = rotation / pi * 180.0
        movie.set_matrix(matrix, scale_x, scale_y, rotation)

    @staticmethod
    def get_x(movie):
        matrix_id = movie.matrix_id
        if (matrix_id & Constant.MATRIX_FLAG) == 0:
            translate = movie.lwf.data.translates[matrix_id]
            return translate.translate_x
        else:
            matrix_id &= ~-Constant.MATRIX_FLAG_MASK
            matrix = movie.lwf.data.matrices[matrix_id]
            return matrix.translate_x

    @staticmethod
    def get_y(movie):
        matrix_id = movie.matrix_id
        if (matrix_id & Constant.MATRIX_FLAG) == 0:
            translate = movie.lwf.data.translates[matrix_id]
            return translate.translate_y
        else:
            matrix_id &= ~-Constant.MATRIX_FLAG_MASK
            matrix = movie.lwf.data.matrices[matrix_id]
            return matrix.translate_y

    @staticmethod
    def get_scale_x(movie):
        matrix_id = movie.matrix_id
        if (matrix_id & Constant.MATRIX_FLAG) == 0:
            return 1
        else:
            matrix_id &= ~-Constant.MATRIX_FLAG_MASK
            matrix = movie.lwf.data.matrices[matrix_id]
            md = bool(Utility.get_matrix_determinant(matrix))
            scale_x = sqrt(matrix.scale_x * matrix.scale_x + matrix.skew_1 * matrix.skew_1)
            if md:
                scale_x = -scale_x
            return scale_x

    @staticmethod
    def get_scale_y(movie):
        matrix_id = movie.matrix_id
        if (matrix_id & Constant.MATRIX_FLAG) == 0:
            return 1
        else:
            matrix_id &= ~-Constant.MATRIX_FLAG_MASK
            matrix = movie.lwf.data.matrices[matrix_id]
            scale_y = sqrt(matrix.scale_y * matrix.scale_y + matrix.skew_0 * matrix.skew_0)
            return scale_y

    @staticmethod
    def get_rotation(movie):
        matrix_id = movie.matrix_id
        if (matrix_id & Constant.MATRIX_FLAG) == 0:
            return 0
        else:
            matrix_id &= ~-Constant.MATRIX_FLAG_MASK
            matrix = movie.lwf.data.matrices[matrix_id]
            md = bool(Utility.get_matrix_determinant(matrix))
            if md:
                rotation = atan2(matrix.skew_1, -matrix.scale_x)
            else:
                rotation = atan2(matrix.skew_1, matrix.scale_x)
            rotation = rotation / pi * 180.0
            return rotation

    @staticmethod
    def sync_color_transform(movie):
        color_transform_id = movie.color_transform_id
        if (color_transform_id & Constant.COLOR_TRANSFORM_FLAG) == 0:
            alpha_transform = movie.lwf.data.alpha_transforms[color_transform_id]
            color_transform = ColorTransform(1, 1, 1, alpha_transform.alpha)
            movie.set_color_transform(color_transform)
        else:
            color_transform_id &= ~-Constant.COLOR_TRANSFORM_FLAG
            movie.set_color_transform(movie.lwf.data.color_transforms[color_transform_id])

    @staticmethod
    def get_alpha(movie):
        color_transform_id = movie.color_transform_id
        if (color_transform_id & Constant.COLOR_TRANSFORM_FLAG) == 0:
            alpha_transform = movie.lwf.data.alpha_transforms[color_transform_id]
            return alpha_transform.alpha
        else:
            color_transform_id &= ~-Constant.COLOR_TRANSFORM_FLAG
            color_transform = movie.lwf.data.color_transforms[color_transform_id]
            return color_transform.multi.alpha

    @staticmethod
    def get_red(movie):
        color_transform_id = movie.color_transform_id
        if (color_transform_id & Constant.COLOR_TRANSFORM_FLAG) == 0:
            return 1
        else:
            color_transform_id &= ~-Constant.COLOR_TRANSFORM_FLAG
            color_transform = movie.lwf.data.color_transforms[color_transform_id]
        return color_transform.multi.red

    @staticmethod
    def get_green(movie):
        color_transform_id = movie.color_transform_id
        if (color_transform_id & Constant.COLOR_TRANSFORM_FLAG) == 0:
            return 1
        else:
            color_transform_id &= ~-Constant.COLOR_TRANSFORM_FLAG
            color_transform = movie.lwf.data.color_transforms[color_transform_id]
        return color_transform.multi.green

    @staticmethod
    def get_blue(movie):
        color_transform_id = movie.color_transform_id
        if (color_transform_id & Constant.COLOR_TRANSFORM_FLAG) == 0:
            return 1
        else:
            color_transform_id &= ~-Constant.COLOR_TRANSFORM_FLAG
            color_transform = movie.lwf.data.color_transforms[color_transform_id]
        return color_transform.multi.blue

    @staticmethod
    def calc_matrix(*args):
        if isinstance(args[0], Matrix):
            dst, src_0, src_1 = args
            dst.scale_x = src_0.scale_x * src_1.scale_x + src_0.skew_0 * src_1.skew_1
            dst.skew_0 = src_0.scale_x * src_1.skew_0 + src_0.skew_0 * src_1.scale_y
            dst.translate_x = src_0.scale_x * src_1.translate_x + src_0.skew_0 * src_1.translate_y + src_0.translate_x
            dst.skew_1 = src_0.skew_1 * src_1.scale_x + src_0.scale_y * src_1.skew_1
            dst.scale_y = src_0.skew_1 * src_1.skew_0 + src_0.scale_y * src_1.scale_y
            dst.translate_y = src_0.skew_1 * src_1.translate_x + src_0.scale_y * src_1.translate_y + src_0.translate_y
            return dst
        else:
            lwf, dst, src_0, src_1_id = args
            if src_1_id == 0:
                dst.set(src_0)
            elif (src_1_id & Constant.MATRIX_FLAG) == 0:
                translate = lwf.data.translates[src_1_id]
                dst.scale_x = src_0.scale_x
                dst.skew_0 = src_0.skew_0
                dst.translate_x = src_0.scale_x * translate.translate_x + src_0.skew_0 * translate.translate_y + src_0.translate_x
                dst.skew_1 = src_0.skew_1
                dst.scale_y = src_0.scale_y
                dst.translate_y = src_0.skew_1 * translate.translate_x + src_0.scale_y * translate.translate_y + src_0.translate_y
            else:
                matrix_id = src_1_id & ~-Constant.MATRIX_FLAG_MASK
                src_1 = lwf.data.matrices[matrix_id]
                Utility.calc_matrix(dst, src_0, src_1)
            return dst

    @staticmethod
    def copy_matrix(dst, src):
        if src is None:
            dst.clear()
        else:
            dst.set(src)
        return dst

    @staticmethod
    def invert_matrix(dst, src):
        dt = src.scale_x * src.scale_y - src.skew_0 * src.skew_1
        if dt != 0.0:
            dst.scale_x = src.scale_y / dt
            dst.skew_0 = -src.skew_0 / dt
            dst.translate_x = (src.skew_0 * src.translate_y - src.translate_x * src.scale_y) / dt
            dst.skew_1 = -src.skew_1 / dt
            dst.scale_y = src.scale_x / dt
            dst.translate_y = (src.translate_x * src.skew_1 - src.scale_x * src.translate_y) / dt
        else:
            dst.clear()

    @staticmethod
    def calc_color_transform(*args):
        if isinstance(args[0], ColorTransform):
            dst, src_0, src_1 = args
            dst.multi.red = src_0.multi.red * src_1.multi.red
            dst.multi.green = src_0.multi.green * src_1.multi.green
            dst.multi.blue = src_0.multi.blue * src_1.multi.blue
            dst.multi.alpha = src_0.multi.alpha * src_1.multi.alpha
            dst.add.red = src_0.add.red * src_1.multi.red + src_1.add.red
            dst.add.green = src_0.add.green * src_1.multi.green + src_1.add.green
            dst.add.blue = src_0.add.blue * src_1.multi.blue + src_1.add.blue
            dst.add.alpha = src_0.add.alpha * src_1.multi.alpha + src_1.add.alpha
            return dst
        else:
            lwf, dst, src_0, src_1_Id = args
            if src_1_Id == 0:
                dst.set(src_0)
            elif (src_1_Id & Constant.COLOR_TRANSFORM_FLAG) == 0:
                alpha_transform = lwf.data.alpha_transforms[src_1_Id]
                dst.multi.red = src_0.multi.red
                dst.multi.green = src_0.multi.green
                dst.multi.blue = src_0.multi.blue
                dst.multi.alpha = src_0.multi.alpha * alpha_transform.alpha
                dst.add.set(src_0.add)
            else:
                color_transform_id = src_1_Id & ~Constant.COLOR_TRANSFORM_FLAG
                src_1 = lwf.data.color_transforms[color_transform_id]
                Utility.calc_color_transform(dst, src_0, src_1)
            return dst

    @staticmethod
    def copy_color_transform(dst, src):
        if src is None:
            dst.clear()
        else:
            dst.set(src)
        return dst

    @staticmethod
    def calc_color(dst, c, t):
        dst.red = c.red * t.multi.red + t.add.red
        dst.green = c.green * t.multi.green + t.add.green
        dst.blue = c.blue * t.multi.blue + t.add.blue
        dst.alpha = c.alpha * t.multi.alpha + t.add.alpha

    # @staticmethod
    # def RotateMatrix(dst, src, scale, offsetX, offsetY):
    #     offsetX *= scale
    #     offsetY *= scale
    #     dst.scaleX = -src.skew0 * scale
    #     dst.skew0 = src.scaleX * scale
    #     dst.translateX = src.scaleX * offsetX + src.skew0 * offsetY + src.translateX
    #     dst.skew1 = -src.scaleY * scale
    #     dst.scaleY = src.skew1 * scale
    #     dst.translateY = src.skew1 * offsetX + src.scaleY * offsetY + src.translateY
    #     return dst
    #
    # @staticmethod
    # def ScaleMatrix(dst, src, scale, offsetX, offsetY):
    #     offsetX *= scale
    #     offsetY *= scale
    #     dst.scaleX = src.scaleX * scale
    #     dst.skew0 = src.skew0 * scale
    #     dst.translateX = src.scaleX * offsetX + src.skew0 * offsetY + src.translateX
    #     dst.skew1 = src.skew1 * scale
    #     dst.scaleY = src.scaleY * scale
    #     dst.translateY = src.skew1 * offsetX + src.scaleY * offsetY + src.translateY
    #
    # @staticmethod
    # def FitForHeight(lwf, stageWidth, stageHeight):
    #     Utility.ScaleForHeight(lwf, stageWidth, stageHeight)
    #     offsetX = (stageWidth - lwf.width * lwf.scaleByStage) / 2.0
    #     offsetY = -stageHeight
    #     lwf.lwfproperty.Move(offsetX, offsetY)
    #
    # @staticmethod
    # def FitForWidth(lwf, stageWidth, stageHeight):
    #     Utility.ScaleForWidth(lwf, stageWidth, stageHeight)
    #     offsetX = (stageWidth - lwf.width * lwf.scaleByStage) / 2.0
    #     offsetY = -stageHeight + (stageHeight - lwf.height * lwf.scaleByStage) / 2.0
    #     lwf.lwfproperty.Move(offsetX, offsetY)
    #
    # @staticmethod
    # def ScaleForHeight(lwf, stageWidth, stageHeight):
    #     scale = stageHeight / lwf.height
    #     lwf.scaleByStage = scale
    #     lwf.lwfproperty.Scale(scale, scale)
    #
    # @staticmethod
    # def ScaleForWidth(lwf, stageWidth, stageHeight):
    #     scale = stageWidth / lwf.width
    #     lwf.scaleByStage = scale
    #     lwf.lwfproperty.Scale(scale, scale)
