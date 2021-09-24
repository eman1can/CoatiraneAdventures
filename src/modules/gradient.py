from itertools import chain

from kivy.graphics.texture import Texture


class Gradient:
    @staticmethod
    def interpolate(size, max_size, colors):
        section = int(max_size / (len(colors) - 1))
        output = []
        for index in range(len(colors) - 1):
            output += Gradient.interpolate_two(max(min(size - (section * index), section), 0), section, *colors[index], *colors[index + 1])
        return output

    @staticmethod
    def interpolate_two(size, max_size, r, g, b, a, re, ge, be, ae):
        ra = [r + (re - r) * x / max_size for x in range(size)]
        ga = [g + (ge - g) * x / max_size for x in range(size)]
        ba = [b + (be - b) * x / max_size for x in range(size)]
        aa = [a + (ae - a) * x / max_size for x in range(size)]
        return [v for v in chain(*[[ra[x], ga[x], ba[x], aa[x]] for x in range(size)])]

    @staticmethod
    def create_texture(gradient, width, height):
        texture = Texture.create(size=(width, height), colorfmt='rgba')
        buf = bytes([int(v) for v in gradient])  # flattens
        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        return texture

    @staticmethod
    def horizontal(width, max_width, height, *colors):
        if width <= 0 or height <= 0:
            return None

        width, max_width, height = int(width), int(max_width), int(height)

        gradient = Gradient.interpolate(width, max_width, colors) * height

        return Gradient.create_texture(gradient, width, height)

    @staticmethod
    def vertical(width, height, max_height, *colors):
        if width <= 0 or height <= 0:
            return None

        width, height, max_height = int(width), int(height), int(max_height)

        gradient_horizontal = Gradient.interpolate(height, max_height, colors)

        gradient = []
        for x in range(0, len(gradient_horizontal), 4):
            gradient += gradient_horizontal[x:x + 4] * width

        return Gradient.create_texture(gradient, width, height)

    @staticmethod
    def vertical_center(width, height, max_height, color1, color2, edge=0.5):
        if width <= 0 or height <= 0:
            return None

        width, height, max_height = int(width), int(height), int(max_height)

        gradient_first = Gradient.interpolate_two(int(height * edge), int(max_height * edge), *color2, *color1)
        gradient_second = Gradient.interpolate_two(int(height * edge), int(max_height * edge), *color1, *color2)

        gradient = []
        for x in range(0, len(gradient_first), 4):
            gradient += gradient_first[x:x + 4] * width
        for _ in range(int(height * (1 - edge * 2))):
            gradient += color1 * width
        for x in range(0, len(gradient_second), 4):
            gradient += gradient_second[x:x + 4] * width

        return Gradient.create_texture(gradient, width, height)

    # @staticmethod
    # def diagonal(*args):
    #     return Gradient.create_texture(gradient, width, height)