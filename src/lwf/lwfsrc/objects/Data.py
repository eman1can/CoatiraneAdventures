# Internal Imports
from ..utils.Type import Matrix, Translate, Color, ColorTransform, AlphaTransform, Dict
from ..utils.BinaryFile import BinaryReader
from ..utils.Animation import *
from ..Format import Format


class Data:
    header = None
    translates = None
    matrices = None
    color = None
    alphaTransforms = None
    colorTransforms = None
    objects = None
    textures = None
    textureFragments = None
    bitmaps = None
    bitmapExs = None
    fonts = None
    textProperties = None
    texts = None
    particleDatas = None
    particles = None
    programObjects = None
    graphicObjects = None
    graphics = None
    animations = None
    buttonConditions = None
    buttons = None
    labels = None
    instanceNames = None
    events = None
    places = None
    controlMoveMs = None
    controlMoveCs = None
    controlMoveMCs = None
    controlMoveMCBs = None
    controls = None
    frames = None
    moveClipEvents = None
    movies = None
    movieLinkages = None
    strings = None

    stringMap = None
    instanceNameMap = None
    eventMap = None
    movieLinkageMap = None
    movieLinkageNameMap = None
    programObjectMap = None
    labelMap = None
    bitmapMap = None

    def __init__(self, byteArray):
        # bytes is a "bytes array"
        if len(byteArray) < int(Format.Constant.HEADER_SIZE_COMPAT0):
            return
        br = BinaryReader(byteArray)

        self.header = Format.Header(br)
        if not self.Check():
            return

        stringByteData = br.ReadBytes(int(self.header.stringBytes.length))
        animationByteData = br.ReadBytes(int(self.header.animationBytes.length))

        self.translates = [Translate(br) for _ in range(self.header.translate.length)]
        self.matrices = [Matrix(br) for _ in range(self.header.matrix.length)]
        self.colors = [Color(br) for _ in range(self.header.color.length)]
        self.alphaTransforms = [AlphaTransform(br) for _ in range(self.header.alphaTransform.length)]
        self.colorTransforms = [ColorTransform(br) for _ in range(self.header.colorTransform.length)]
        self.objects = [Format.Object(br) for _ in range(self.header.objectData.length)]
        self.textures = [Format.Texture(br) for _ in range(self.header.texture.length)]
        self.textureFragments = [
            Format.TextureFragment(br, self.header.formatVersion >= int(Format.Constant.FORMAT_VERSION_141211.value))
            for _ in range(self.header.textureFragment.length)]
        self.bitmaps = [Format.Bitmap(br) for _ in range(self.header.bitmap.length)]
        self.bitmapExs = [Format.BitmapEx(br) for _ in range(self.header.bitmapEx.length)]
        self.fonts = [Format.Font(br) for _ in range(self.header.font.length)]
        self.textProperties = [Format.TextProperty(br) for _ in range(self.header.textProperty.length)]
        self.texts = [Format.Text(br) for _ in range(self.header.text.length)]
        self.particleDatas = [Format.ParticleData(br) for _ in range(self.header.particleData.length)]
        self.particles = [Format.Particle(br) for _ in range(self.header.particle.length)]
        self.programObjects = [Format.ProgramObject(br) for _ in range(self.header.programObject.length)]
        self.graphicObjects = [Format.GraphicObject(br) for _ in range(self.header.graphicObject.length)]
        self.graphics = [Format.Graphic(br) for _ in range(self.header.graphic.length)]
        animationData = [Format.Animation(br) for _ in range(self.header.animation.length)]
        self.buttonConditions = [Format.ButtonCondition(br) for _ in range(self.header.buttonCondition.length)]
        self.buttons = [Format.Button(br) for _ in range(self.header.button.length)]
        self.labels = [Format.Label(br) for _ in range(self.header.label.length)]
        self.instanceNames = [Format.InstanceName(br) for _ in range(self.header.instanceName.length)]
        self.events = [Format.Event(br) for _ in range(self.header.eventData.length)]
        self.places = [Format.Place(br) for _ in range(self.header.place.length)]
        self.controlMoveMs = [Format.ControlMoveM(br) for _ in range(self.header.controlMoveM.length)]
        self.controlMoveCs = [Format.ControlMoveC(br) for _ in range(self.header.controlMoveC.length)]
        self.controlMoveMCs = [Format.ControlMoveMC(br) for _ in range(self.header.controlMoveMC.length)]
        self.controlMoveMCBs = [Format.ControlMoveMCB(br) for _ in range(self.header.controlMoveMCB.length)]
        self.controls = [Format.Control(br) for _ in range(self.header.control.length)]
        self.frames = [Format.Frame(br) for _ in range(self.header.frame.length)]
        self.movieClipEvents = [Format.MovieClipEvent(br) for _ in range(self.header.movieClipEvent.length)]
        self.movies = [Format.Movie(br) for _ in range(self.header.movie.length)]
        self.movieLinkages = [Format.MovieLinkage(br) for _ in range(self.header.movieLinkage.length)]
        stringData = [Format.String(br) for _ in range(self.header.stringData.length)]

        self.animations = [[] for _ in range(len(animationData))]
        for i in range(0, len(animationData)):
            self.animations[i] = self.ReadAnimation(animationByteData, int(animationData[i].animationOffset),
                                                    int(animationData[i].animationLength))
        self.strings = [None for _ in range(len(stringData))]
        for i in range(0, len(stringData)):
            self.strings[i] = stringByteData[int(stringData[i].stringOffset):int(stringData[i].stringOffset) + int(
                stringData[i].stringLength)].decode("utf-8")

        self.stringMap = Dict()
        for i in range(0, len(self.strings)):
            self.stringMap[self.strings[i]] = i

        self.instanceNameMap = Dict()
        for i in range(0, len(self.instanceNames)):
            self.instanceNameMap[self.instanceNames[i].stringId] = i

        self.eventMap = Dict()
        for i in range(0, len(self.events)):
            self.eventMap[self.events[i].stringId] = i

        self.movieLinkageMap = Dict()
        self.movieLinkageNameMap = Dict()
        for i in range(0, len(self.movieLinkages)):
            self.movieLinkageMap[self.movieLinkages[i].stringId] = i
            self.movieLinkageNameMap[self.movieLinkages[i].movieId] = self.movieLinkages[i].stringId

        self.programObjectMap = Dict()
        for i in range(0, len(self.programObjects)):
            self.programObjectMap[self.programObjects[i].stringId] = i

        self.labelMap = [{} for _ in range(len(self.movies))]
        for i in range(0, len(self.movies)):
            m = self.movies[i]
            o = m.labelOffset
            labelMap = Dict()
            for j in range(0, m.labels):
                label = self.labels[o + j]
                labelMap[label.stringId] = label.frameNo
            self.labelMap[i] = labelMap

        for i in range(0, len(self.textures)):
            self.textures[i].SetFilename(self)

        self.bitmapMap = Dict()
        bitmapList = self.bitmaps.copy()
        for i in range(0, len(self.textureFragments)):
            print("Makign me some bitmaps bro")
            self.textureFragments[i].SetFilename(self)
            self.bitmapMap[self.textureFragments[i].filename] = len(bitmapList)
            bitmap = Format.Bitmap()
            bitmap.matrixId, bitmap.textureFragmentId = 0, i
            bitmapList.append(bitmap)
        self.bitmaps = bitmapList

    @property
    def name(self):
        return self.strings[self.header.nameStringId]

    @property
    def useScript(self):
        return self.header.option & int(Format.Constant.OPTION_USE_LUASCRIPT.value) != 0

    @property
    def useTextureAtlas(self):
        return self.header.option & int(Format.Constant.OPTION_USE_TEXTUREATLAS.value)

    def Check(self):
        v0 = self.header.formatVersion0
        v1 = self.header.formatVersion1
        v2 = self.header.formatVersion2
        if self.header is not None and \
                self.header.id0 == ord('L') and \
                self.header.id1 == ord('W') and \
                self.header.id2 == ord('F') and \
                bytes([self.header.id3]) == bytes([Format.Constant.FORMAT_TYPE.value]) and \
                ((
                         bytes([v0]) == bytes([Format.Constant.FORMAT_VERSION_0.value]) and
                         bytes([v1]) == bytes([Format.Constant.FORMAT_VERSION_1.value]) and
                         bytes([v2]) == bytes([Format.Constant.FORMAT_VERSION_2.value])
                 ) or (
                        bytes([v0]) == bytes([Format.Constant.FORMAT_VERSION_COMPAT0_0.value]) and
                        bytes([v1]) == bytes([Format.Constant.FORMAT_VERSION_COMPAT0_1.value]) and
                        bytes([v2]) == bytes([Format.Constant.FORMAT_VERSION_COMPAT0_2.value])
                 ) or (
                        bytes([v0]) == bytes([Format.Constant.FORMAT_VERSION_COMPAT1_0.value]) and
                        bytes([v1]) == bytes([Format.Constant.FORMAT_VERSION_COMPAT1_1.value]) and
                        bytes([v2]) == bytes([Format.Constant.FORMAT_VERSION_COMPAT1_2.value])
                 )) and (self.header.option & int(Format.Constant.OPTION_COMPRESSED.value) is 0):
            return True
        return False

    def ReplaceTexture(self, index, textureReplacement):
        if index < 0 or index >= len(self.textures):
            return False

        self.textures[index] = textureReplacement
        return True

    def ReplaceTextureFragment(self, index, textureFragmentReplacement):
        if index < 0 or index >= len(self.textureFragments):
            return False

        self.textureFragments[index] = textureFragmentReplacement
        return True

    # lwf_loader --------------------------------------------------------------------------------
    @staticmethod
    def ReadAnimation(byteArray: list, offset: int, length: int) -> list:
        br = BinaryReader(byteArray[offset:offset + length])
        array = []
        while True:
            code = br.ReadByte()
            array.append(int(code))

            if code == PLAY or code == STOP or code == NEXTFRAME \
                    or code == PREVFRAME:
                pass
            elif code == GOTOFRAME or code == GOTOLABEL or code == EVENT \
                    or code == CALL:
                array.append(br.ReadInt32())
            elif code == SETTARGET:
                count = br.ReadInt32()
                array.append(count)
                for i in range(0, int(count)):
                    target = br.ReadInt32()
                    array.append(target)
            elif code == END:
                for i in range(0, len(array)):
                    array[i] = int(array[i])
                return array
