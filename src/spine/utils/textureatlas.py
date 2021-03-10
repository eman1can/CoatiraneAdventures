from src.spine.utils.filehandle import FileHandle
from kivy.graphics.texture import Texture, TextureRegion
from kivy.core.image import Image


class Page:

    def __init__(self, file, width, height, useMipMaps, format, minFilter, magFilter, uWrap, vWrap):

        self.textureFile = None
        self.texture = None
        self.width = 0.0
        self.height = 0.0
        self.useMipMaps = False
        self.format = None
        self.minFilter = None
        self.magFilter = None
        self.uWrap = None
        self.vWrap = None

        self.width = width
        self.height = height
        self.textureFile = file
        self.useMipMaps = useMipMaps
        self.format = format
        self.minFilter = minFilter
        self.magFilter = magFilter
        self.uWrap = uWrap
        self.vWrap = vWrap


class Region:

    def __init__(self):
        self.page = None
        self.index = 0
        self.name = None
        self.offsetX = 0.0
        self.offsetY = 0.0
        self.originalWidth = 0
        self.originalHeight = 0
        self.rotate = False
        self.degrees = 0.0
        self.left = 0
        self.top = 0
        self.width = 0
        self.height = 0
        self.flip = False
        self.splits = None
        self.pads = None

    def __lt__(self, other):
        return False


class GdxTextureRegion:

    def __init__(self, *args, **kwargs):

        self.texture = None
        self.u = 0.0
        self.v = 0.0
        self.u2 = 0.0
        self.v2 = 0.0
        self.regionWidth = 0
        self.regionHeight = 0
        self.valid = False
        self.texRegion = None

        if len(args) == 1:
            if isinstance(args[0], GdxTextureRegion):
                self.setRegion(args[0])
            else:
                if args[0] is None:
                    raise Exception("Texture cannot be None")
                self.texture = args[0]
                self.setRegion(0, 0, args[0].width, args[0].height)
        elif len(args) == 3:
            texture, width, height = args[0], args[1], args[2]
            self.texture = texture
            self.setRegion(0, 0, width, height)
        elif len(args) == 5:
            if isinstance(args[0], GdxTextureRegion):
                self.setRegion(args[0], args[1], args[2], args[3], args[4])
            else:
                self.texture = args[0]
                self.setRegion(args[1], args[2], args[3], args[4])
        self.valid = False

    def setRegion(self, *args):
        if len(args) == 1:
            if isinstance(args[0], GdxTextureRegion):
                self.texture = args[0].texture
                self.setRegion(args[0].u, args[0].v, args[0].u2, args[0].v2)
            else:
                self.texture = args[0]
                self.setRegion(0, 0, args[0].width, args[0].height)
        elif len(args) == 4:
            if isinstance(args[0], int):
                invTexWidth = 1 / self.texture.width
                invTexHeight = 1 / self.texture.height
                self.setRegion(args[0] * invTexWidth, args[1] * invTexHeight, (args[0] + args[2]) * invTexWidth, (args[1] + args[3]) * invTexHeight)
                self.regionWidth = abs(args[2])
                self.regionHeight = abs(args[3])
            else:
                texWidth, texHeight = self.texture.width, self.texture.height
                u, v, u2, v2 = args[0], args[1], args[2], args[3]
                self.regionWidth = round(abs(u2 - u) * texWidth)
                self.regionHeight = round(abs(v2 - v) * texHeight)

                if self.regionWidth == 1 and self.regionHeight == 1:
                    adjustX = 0.25 / texWidth
                    u += adjustX
                    u2 -= adjustX
                    adjustY = 0.25 / texHeight
                    v += adjustY
                    v2 -= adjustY
                self.u = u
                self.v = v
                self.u2 = u2
                self.v2 = v2
        elif len(args) == 5:
            self.texture = args[0].texture
            self.setRegion(args[0].getRegionX() + args[1], args[0].getRegionY() + args[2], args[3], args[4])
        self.valid = False

    def getTexture(self):
        # return self.texture
        # if not self.valid:
        #     self.valid = True
        width, height = self.getRegionWidth(), self.getRegionHeight()
        x, y = self.getRegionX(), self.texture.height - self.getRegionY() - height
        self.texRegion = self.texture.get_region(x, y, width, height)
        #     self.texRegion = TextureRegion(self.getRegionX(), self.getRegionY(), self.getRegionWidth(), self.getRegionHeight(), self.texture)
        return self.texRegion

    def setTexture(self, texture):
        self.texture = texture
        self.valid = False

    def getU(self):
        return self.u

    def setU(self, u):
        self.u = u
        self.regionWidth = round(abs(self.u2 - self.u) * self.texture.width)
        self.valid = False

    def getV(self):
        return self.v

    def setV(self, v):
        self.v = v
        self.regionHeight = round(abs(self.v2 - self.v) * self.texture.height)
        self.valid = False

    def getU2(self):
        return self.u2

    def setU2(self, u2):
        self.u2 = u2
        self.regionWidth = round(abs(self.u2 - self.u) * self.texture.width)
        self.valid = False

    def getV2(self):
        return self.v2

    def setV2(self, v2):
        self.v2 = v2
        self.regionHeight = round(abs(self.v2 - self.v) * self.texture.height)
        self.valid = False

    def getRegionX(self):
        return round(self.u * self.texture.width)

    def setRegionX(self, x):
        self.setU(x / float(self.texture.width))

    def getRegionY(self):
        return round(self.v * self.texture.height)

    def setRegionY(self, y):
        self.setV(y / float(self.texture.height))

    def getRegionWidth(self):
        return self.regionWidth

    def setRegionWidth(self, width):
        if self.isFlipX():
            self.setU(self.u2 + width / float(self.texture.width))
        else:
            self.setU2(self.u + width / float(self.texture.width))

    def getRegionHeight(self):
        return self.regionHeight

    def setRegionHeight(self, height):
        if self.isFlipY():
            self.setV(self.v2 + height / float(self.texture.height))
        else:
            self.setV2(self.v + height / float(self.texture.height))

    def flip(self, x, y):
        if x:
            temp = self.u
            self.u = self.u2
            self.u2 = temp
            self.valid = False
        if y:
            temp = self.v
            self.v = self.v2
            self.v2 = temp
            self.valid = False

    def isFlipX(self):
        return self.u > self.u2

    def isFlipY(self):
        return self.v > self.v2


class TextureAtlas:

    def __init__(self, *args):

        self.rtuple = [None, None, None, None]
        self.textures = []
        self.regions = []

        if len(args) == 1:
            if isinstance(args[0], TextureAtlasData):
                if args[0] != None:
                    self.load(args[0])

    def load(self, data):
        pageToTexture = {}
        for page in data.pages:
            if page.texture is None:
                # texture = Texture.create(size=(page.width, page.height), colorfmt=page.format, bufferfmt=u'byte', mipmap=page.useMipMaps)
                texture = self.load_texture(page.textureFile.full_path())
                texture.min_filter = page.minFilter
                texture.mag_filter = page.magFilter
                texture.wrap = page.uWrap
                # texture.add_reload_observer(lambda texture: self.load_texture(texture, page.textureFile.full_path()))
                self.textures.append(texture)
                pageToTexture[page] = texture
            else:
                self.textures.append(page.texture)
                pageToTexture[page] = page.texture
        for region in data.regions:
            width = region.width
            height = region.height
            # atlasRegion = SpineRegion(region.name, pageToTexture[region.page], region.rotate, region.left, region.top, region.width, region.height)
            atlasRegion = AtlasRegion(pageToTexture[region.page], region.left, region.top, height if region.rotate else width, width if region.rotate else height)
            atlasRegion.index = region.index
            atlasRegion.name = region.name
            atlasRegion.offsetX = region.offsetX
            atlasRegion.offsetY = region.offsetY
            atlasRegion.originalHeight = region.originalHeight
            atlasRegion.originalWidth = region.originalWidth
            atlasRegion.rotate = region.rotate
            atlasRegion.degrees = region.degrees
            atlasRegion.splits = region.splits
            atlasRegion.pads = region.pads
            if region.flip:
                atlasRegion.flip(False, True)
            self.regions.append(atlasRegion)

    def load_texture(self, name):
        return Image(name).texture
        # texture.blit_buffer(image.texture.pixels, colorfmt='rgba')

    def addRegion(self, *args):
        if len(args) == 6:
            name, texture, x, y, width, height = args[0], args[1], int(args[2]), int(args[3]), int(args[4]), int(args[5])
            region = AtlasRegion(texture, x, y, width, height)
            self.textures.append(texture)
        else:
            name, textureRegion = args[0], args[1]
            self.textures.append(textureRegion.texture)
            region = AtlasRegion(textureRegion)
        region.name = name
        region.index = -1
        self.regions.append(region)
        return region

    def getRegions(self):
        return self.regions

    def findRegion(self, *args):
        if len(args) == 1:
            name = args[0]
            for region in self.regions:
                if region.name == name:
                    return region
        else:
            name, index = args
            for region in self.regions:
                if region.name == name and region.index == index:
                    return region
        return None

    def readValue(self, reader):
        line = reader.readline()
        try:
            colon = line.index(':')
        except ValueError:
            raise Exception(f"invalid line: {line}")
        return line[colon + 1:].strip()

    def readTuple(self, reader):
        line = reader.readline()
        try:
            colon = line.index(':')
        except ValueError:
            raise Exception(f"Invalid Line: {line}")
        i, lastMatch = 0, colon + 1
        while i < 3:
            try:
                comma = line.index(',', lastMatch)
            except ValueError:
                break
            self.rtuple[i] = line[lastMatch:comma].strip()
            lastMatch = comma + 1
            i += 1
        self.rtuple[i] = line[lastMatch:].strip()
        return i + 1


class AtlasRegion(GdxTextureRegion):

    def __init__(self, *args):

        self.page = None
        self.index = 0
        self.name = None
        self.offsetX = 0.0
        self.offsetY = 0.0
        self.originalWidth = 0
        self.originalHeight = 0
        self.rotate = False
        self.degrees = 0.0
        self.left = 0
        self.top = 0
        self.width = 0
        self.height = 0
        self.splits = None
        self.pads = None

        self.packedWidth = 0
        self.packedHeight = 0

        if len(args) == 1:
            region = args[0]
            self.setRegion(region)
            if isinstance(region, AtlasRegion):
                self.index = region.index
                self.name = region.name
                self.offsetX = region.offsetX
                self.offsetY = region.offsetY
                self.packedWidth = region.packedWidth
                self.packedHeight = region.packedHeight
                self.originalWidth = region.originalWidth
                self.originalHeight = region.originalHeight
                self.rotate = region.rotate
                self.degrees = region.degrees
                self.splits = region.splits
            else:
                self.packedWidth = int(region.getRegionWidth())
                self.packedHeight = int(region.getRegionHeight())
                self.originalWidth = self.packedWidth
                self.originalHeight = self.packedHeight
        elif len(args) == 5:
            texture, x, y, width, height = args[0], args[1], args[2], args[3], args[4]
            super().__init__(texture, x, y, width, height)
            self.originalWidth = int(width)
            self.originalHeight = int(height)
            self.packedWidth = int(width)
            self.packedHeight = int(height)

    def flip(self, x, y):
        super().flip(x, y)
        if x:
            self.offsetX = self.originalWidth - self.offsetX - self.getRotatedPackedWidth()
        if y:
            self.offsetY = self.originalHeight - self.offsetY - self.getRotatedPackedHeight()

    def getRotatedPackedWidth(self):
        if self.rotate:
            return self.packedHeight
        return self.packedWidth

    def getRotatedPackedHeight(self):
        if self.rotate:
            return self.packedWidth
        return self.packedHeight

    def __str__(self):
        return self.name


class TextureAtlasData:

    def __init__(self, packFile: FileHandle, imagesDir: FileHandle, flip, atlas):

        self.pages = []
        self.regions = []

        reader = open(packFile.full_path(), 'r', 64)
        try:
            page = None
            while True:
                line = reader.readline()
                if len(line) != 0 and len(line.strip()) == 0:
                    page = None
                elif len(line) == 0:
                    break
                elif page is None:
                    file = imagesDir.child(line)
                    width, height = 0, 0
                    if atlas.readTuple(reader) == 2:
                        width = int(atlas.rtuple[0])
                        height = int(atlas.rtuple[1])
                        atlas.readTuple(reader)
                    format = atlas.rtuple[0]
                    if format == 'Alpha' or format == 'Intensity':
                        format = u'luminance'
                    elif format == 'LuminanceAlpha':
                        format = u'luminance_alpha'
                    elif format == 'RGB565' or format == 'RGB888':
                        format = u'rgb'
                    elif format == 'RGBA4444' or format == 'RGBA8888':
                        format = u'rgba'
                    else:
                        raise Exception("Invalid Texture Format!")

                    atlas.readTuple(reader)
                    min = atlas.rtuple[0]
                    if min == 'Linear' or min == 'Nearest':
                        min = str(min).lower()
                    else:
                        raise Exception("Invalid min filter value")

                    mag = atlas.rtuple[1]
                    mipmap = True
                    if mag == 'Linear' or mag == 'Nearest':
                        mag = str(mag).lower()
                        mipmap = False
                    elif mag == 'LinearMipMapLinear':
                        mag = 'linear_mipmap_linear'
                    elif mag == 'LinearMipMapNearest':
                        mag = 'linear_mipmap_nearest'
                    elif mag == 'NearestMipMapNearest':
                        mag = 'nearest_mipmap_nearest'
                    elif mag == 'NearestMipMapLinear':
                        mag = 'nearest_mipmap_linear'
                    else:
                        raise Exception("Invalid max filter value")

                    direction = atlas.readValue(reader)
                    repeatX = 'clamp_to_edge'
                    repeatY = 'clamp_to_edge'
                    if direction == 'x':
                        repeatX = 'repeat'
                    elif direction == 'y':
                        repeatY = 'repeat'
                    elif direction == 'xy':
                        repeatX = 'repeat'
                        repeatY = 'repeat'

                    page = Page(file, width, height, mipmap, format, min, mag, repeatX, repeatY)
                    self.pages.append(page)
                else:
                    rotateValue = atlas.readValue(reader)
                    if str(rotateValue).lower() == "true":
                        degrees = 90
                    elif str(rotateValue).lower() == "false":
                        degrees = 0
                    else:
                        degrees = int(rotateValue)

                    atlas.readTuple(reader)
                    left = int(atlas.rtuple[0])
                    top = int(atlas.rtuple[1])

                    atlas.readTuple(reader)
                    width = int(atlas.rtuple[0])
                    height = int(atlas.rtuple[1])

                    region = Region()
                    region.page = page
                    region.left = left
                    region.top = top
                    region.width = width
                    region.height = height
                    region.name = line.strip()
                    region.rotate = degrees == 90
                    region.degrees = degrees

                    if atlas.readTuple(reader) == 4:
                        region.splits = [int(atlas.rtuple[0]), int(atlas.rtuple[1]), int(atlas.rtuple[2]), int(atlas.rtuple[3])]
                        if atlas.readTuple(reader) == 4:
                            region.pads = [int(atlas.rtuple[0]), int(atlas.rtuple[1]), int(atlas.rtuple[2]), int(atlas.rtuple[3])]
                            atlas.readTuple(reader)

                    region.originalWidth = int(atlas.rtuple[0])
                    region.originalHeight = int(atlas.rtuple[1])

                    atlas.readTuple(reader)
                    region.offsetX = int(atlas.rtuple[0])
                    region.offsetY = int(atlas.rtuple[1])

                    region.index = int(atlas.readValue(reader))

                    if flip:
                        region.flip = True

                    self.regions.append(region)

        except IOError as e:
            raise Exception(f"Error reading pack file {packFile.full_path()}, {e}")
        finally:
            reader.close()

        region_values = []
        for region in self.regions:
            region_values.append(region.index)

        self.regions = [region for _, region in sorted(zip(region_values, self.regions))]

    def get_pages(self):
        return self.pages

    def get_regions(self):
        return self.regions
