# External Imports
from kivy.uix.image import Image


class CustomImage:

    def __init__(self):
        self.data = None

    @staticmethod
    def load_image(cache, RCache, settings, texture, image, source, data):
        image.data = Image(source=source)
        cache[texture.filename] = image.data
        if texture.filename in settings['_alphaMap']:
            d = ['_alphaMap'][texture.filename]

            jpg = d[0]
            alpha = d[1]
            jpgImg = cache[jpg.filename]
            alphaImg = cache[alpha.filename]
            if jpgImg and alphaImg:
                (canvas, ctx) = RCache.createCanvas(jpgImg.width, jpgImg.height)
                ctx.drawImage(jpgImg, 0, 0, jpgImg.width, jpgImg.height, 0, 0, jpgImg.width, jpgImg.height)
                ctx.globalCompositeOperation = "destination-in"
                ctx.drawImage(alphaImg, 0, 0, alphaImg.width, alphaImg.height, 0, 0, jpgImg.width,
                              jpgImg.height)
                ctx.globalCompositeOperation = "source-over"
                del cache[jpg.filename]
                del cache[alpha.filename]
                cache[jpg.filename] = canvas
                RCache.generateImages(settings, cache, jpg, canvas)
            else:
                RCache.generateImages(settings, cache, texture, image.data)

            image = image.onload = image.onabort = image.onerror = None
            RCache.loadImagesCallback(settings, cache, data)

