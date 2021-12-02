class ImageUtils:
    @staticmethod
    def add_border(pixels, width, height, border_size):
        for x in range(width):
            for y in range(height):
                if border_size <= x < width - border_size and border_size <= y < height - border_size:
                    continue
                index = (y * width + x) * 4
                pixels[index + 0] = 0
                pixels[index + 1] = 0
                pixels[index + 2] = 0
                pixels[index + 3] = 255
        return pixels
