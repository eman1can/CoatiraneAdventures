# Internal Imports
from .utils.BinaryFile import BinaryReader

# External Imports
import re


class Format:
    class Constant:
        HEADER_SIZE = 332
        FORMAT_VERSION_0 = 0x14
        FORMAT_VERSION_1 = 0x12
        FORMAT_VERSION_2 = 0x11
        FORMAT_VERSION_141211 = 0x141211

        HEADER_SIZE_COMPAT0 = 324
        FORMAT_VERSION_COMPAT0_0 = 0x12
        FORMAT_VERSION_COMPAT0_1 = 0x10
        FORMAT_VERSION_COMPAT0_2 = 0x10

        HEADER_SIZE_COMPAT1 = 324
        FORMAT_VERSION_COMPAT1_0 = 0x13
        FORMAT_VERSION_COMPAT1_1 = 0x12
        FORMAT_VERSION_COMPAT1_2 = 0x11

        FORMAT_TYPE = 0

        OPTION_OFFSET = 7

        OPTION_USE_SCRIPT = (1 << 0)
        OPTION_USE_TEXTUREATLAS = (1 << 1)
        OPTION_COMPRESSED = (1 << 2)
        OPTION_USE_LUASCRIPT = (1 << 3)

        MATRIX_FLAG = (1 << 31)
        MATRIX_FLAG_MASK = (1 << 31)
        COLORTRANSFORM_FLAG = (1 << 31)

        TEXTUREFORMAT_NORMAL = 0
        TEXTUREFORMAT_PREMULTIPLIEDALPHA = 1

        BLEND_MODE_NORMAL = 0
        BLEND_MODE_ADD = 1
        BLEND_MODE_LAYER = 2
        BLEND_MODE_ERASE = 3
        BLEND_MODE_MASK = 4
        BLEND_MODE_MULTIPLY = 5
        BLEND_MODE_SCREEN = 6
        BLEND_MODE_SUBTRACT = 7

    class StringBase:
        stringId = 0

    class Texture:
        stringId = 0
        format = 0
        width = 0
        height = 0
        scale = 0
        filename = None

        def __init__(self, *args):
            if len(args) == 1:
                if isinstance(args[0], BinaryReader):
                    br = args[0]
                    self.stringId = br.ReadInt32()
                    self.format = br.ReadInt32()
                    self.width = br.ReadInt32()
                    self.height = br.ReadInt32()
                    self.scale = br.ReadSingle()

        def SetFilename(self, data):
            self.filename = re.sub(r"\\.[^\\.]*$", "", data.strings[self.stringId])

    class TextureReplacement(Texture):
        def __init__(self, fname, fmt, w, h, s):
            super().__init__()
            self.filename = fname
            self.format = int(fmt)
            self.width = w
            self.height = h
            self.scale = s

    class TextureFragment:
        stringId = 0
        textureId = 0
        rotated = 0
        x = 0
        y = 0
        u = 0
        v = 0
        w = 0
        h = 0
        ow = 0
        oh = 0
        filename = None

        def __init__(self, *args):
            if len(args) > 0:
                if isinstance(args[0], BinaryReader):
                    br, withOriginalWH = args[0], args[1]
                    self.stringId = br.ReadInt32()
                    self.textureId = br.ReadInt32()
                    self.rotated = br.ReadInt32()
                    self.x = br.ReadInt32()
                    self.y = br.ReadInt32()
                    self.u = br.ReadInt32()
                    self.v = br.ReadInt32()
                    self.w = br.ReadInt32()
                    self.h = br.ReadInt32()
                    if withOriginalWH:
                        self.ow = br.ReadInt32()
                        self.oh = br.ReadInt32()
                    else:
                        self.ow = self.w
                        self.oh = self.h

        def SetFilename(self, data):
            self.filename = re.sub(r'\\.[^\\.]*$', "", data.strings[self.stringId])

    class TextureFragmentReplacement(TextureFragment):
        def __init__(self, fname, texId, rot, tx, ty, tu, tv, tw, th, tow, toh):
            super().__init__()
            self.filename = fname
            self.textureId = texId
            self.rotated = rot
            self.x = tx
            self.y = ty
            self.u = tu
            self.v = tv
            self.w = tw
            self.h = th
            self.ow = tow
            self.oh = toh

    class Bitmap:
        matrixId = 0
        textureFragmentId = 0

        def __init__(self, *args):
            if len(args) == 1:
                if isinstance(args[0], BinaryReader):
                    self.matrixId = args[0].ReadInt32()
                    self.textureFragmentId = args[0].ReadInt32()

    class BitmapEx:
        matrixId = 0
        textureFragmentId = 0
        attribute = 0
        u = 0.0
        v = 0.0
        w = 0.0
        h = 0.0

        def __init__(self, *args):
            if len(args) == 1:
                if isinstance(args[0], BinaryReader):
                    br = args[0]
                    self.matrixId = br.ReadInt32()
                    self.textureFragmentId = br.ReadInt32()
                    self.attribute = br.ReadInt32()
                    self.u = br.ReadSingle()
                    self.v = br.ReadSingle()
                    self.w = br.ReadSingle()
                    self.h = br.ReadSingle()

        class Attribute:
            REPEAT_S = (1 << 0)
            REPEAT_T = (1 << 1)

    class Font:
        stringId = 0
        letterspacing = 0.0

        def __init__(self, *args):
            if len(args) == 1:
                if isinstance(args[0], BinaryReader):
                    self.stringId = args[0].ReadInt32()
                    self.letterspacing = args[0].ReadSingle()

    class TextProperty:
        maxLength = 0
        fontIf = 0
        fontHeight = 0
        align = 0
        leftMargin = 0
        rightMargin = 0
        letterSpacing = 0.0
        leading = 0
        strokeColorId = 0
        strokeWidth = 0
        shadowColorId = 0
        shadowOffsetX = 0
        shadowOffsetY = 0
        shadowBlur = 0

        def __init__(self, *args):
            if len(args) == 1:
                if isinstance(args[0], BinaryReader):
                    br = args[0]
                    self.maxLength = br.ReadInt32()
                    self.fontId = br.ReadInt32()
                    self.fontHeight = br.ReadInt32()
                    self.align = br.ReadInt32()
                    self.leftMargin = br.ReadInt32()
                    self.rightMargin = br.ReadInt32()
                    self.letterSpacing = br.ReadSingle()
                    self.leading = br.ReadInt32()
                    self.strokeColorId = br.ReadInt32()
                    self.strokeWidth = br.ReadInt32()
                    self.shadowColorId = br.ReadInt32()
                    self.shadowOffsetX = br.ReadInt32()
                    self.shadowOffsetY = br.ReadInt32()
                    self.shadowBlur = br.ReadInt32()

        class Align:
            LEFT = 0
            RIGHT = 1
            CENTER = 2
            ALIGN_MASK = 0x3
            VERTICAL_BOTTOM = (1 << 2)
            VERTICAL_MIDDLE = (2 << 2)
            VERTICAL_MASK = 0xc

    class Text:
        matrixId = 0
        nameStringId = 0
        textPropertyId = 0
        stringId = 0
        colorId = 0
        width = 0
        height = 0

        def __init__(self, *args):
            if len(args) == 1:
                if isinstance(args[0], BinaryReader):
                    br = args[0]
                    self.matrixId = br.ReadInt32()
                    self.nameStringId = br.ReadInt32()
                    self.textPropertyId = br.ReadInt32()
                    self.stringId = br.ReadInt32()
                    self.colorId = br.ReadInt32()
                    self.width = br.ReadInt32()
                    self.height = br.ReadInt32()

    class ParticleData:
        stringId = 0

        def __init__(self, *args):
            if len(args) == 1:
                if isinstance(args[0], BinaryReader):
                    self.stringId = args[0].ReadInt32()

    class Particle:
        matrixId = 0
        colorTransformId = 0
        particleDataid = 0
        matrixLetter = 1

        def __init__(self, *args):
            if len(args) == 1:
                if isinstance(args[0], BinaryReader):
                    self.matrixId = args[0].ReadInt32()
                    self.colorTransformId = args[0].ReadInt32()
                    self.particleDataId = args[0].ReadInt32()

    class ProgramObject(StringBase):
        width = 0
        height = 0
        matrixId = 0
        colorTransformId = 0

        def __init__(self, *args):
            if len(args) == 1:
                if isinstance(args[0], BinaryReader):
                    self.stringId = args[0].ReadInt32()
                    self.width = args[0].ReadInt32()
                    self.height = args[0].ReadInt32()
                    self.matrixId = args[0].ReadInt32()
                    self.colorTransformId = args[0].ReadInt32()

    class GraphicObject:
        graphicObjectType = 0
        graphicObjectId = 0

        def __init__(self, *args):
            if len(args) == 1:
                if isinstance(args[0], BinaryReader):
                    self.graphicObjectType = args[0].ReadInt32()
                    self.graphicObjectId = args[0].ReadInt32()

        class Type:
            BITMAP = 0
            BITMAPEX = 1
            TEXT = 2
            GRAPHIC_OBJECT_MAX = 3

    class Graphic:
        graphicObjectId = 0
        graphicObjects = 0

        def __init__(self, *args):
            if len(args) == 1:
                if isinstance(args[0], BinaryReader):
                    self.graphicObjectId = args[0].ReadInt32()
                    self.graphicObjects = args[0].ReadInt32()

    class Object:
        objectType = 0
        objectId = 0

        def __init__(self, *args):
            if len(args) == 1:
                if isinstance(args[0], BinaryReader):
                    self.objectType = args[0].ReadInt32()
                    self.objectId = args[0].ReadInt32()

        class Type:
            BUTTON = 0
            GRAPHIC = 1
            MOVIE = 2
            BITMAP = 3
            BITMAPEX = 4
            TEXT = 5
            PARTICLE = 6
            PROGRAMOBJECT = 7
            ATTACHEDMOVIE = 8
            OBJECT_MAX = 9

    class Animation:
        animationOffset = 0
        animationLength = 0

        def __init__(self, *args):
            if len(args) == 1:
                if isinstance(args[0], BinaryReader):
                    self.animationOffset = args[0].ReadInt32()
                    self.animationLength = args[0].ReadInt32()

    class ButtonCondition:
        condition = 0
        keyCode = 0
        animationId = 0

        def __init__(self, *args):
            if len(args) == 1:
                if isinstance(args[0], BinaryReader):
                    self.condition = args[0].ReadInt32()
                    self.keyCode = args[0].ReadInt32()
                    self.animationId = args[0].ReadInt32()

        class Condition:
            ROLLOVER = (1 << 0)
            ROLLOUT = (1 << 1)
            PRESS = (1 << 2)
            RELEASE = (1 << 3)
            DRAGOUT = (1 << 4)
            DRAGOVER = (1 << 5)
            RELEASEOUTSIDE = (1 << 6)
            KEYPRESS = (1 << 7)

    class Button:
        width = 0
        height = 0
        matrixId = 0
        colorTransformId = 0
        conditionId = 0
        conditions = 0

        def __init__(self, *args):
            if len(args) == 1:
                if isinstance(args[0], BinaryReader):
                    self.width = args[0].ReadInt32()
                    self.height = args[0].ReadInt32()
                    self.matrixId = args[0].ReadInt32()
                    self.colorTransformId = args[0].ReadInt32()
                    self.conditionId = args[0].ReadInt32()
                    self.conditions = args[0].ReadInt32()

    class Label(StringBase):
        frameNo = 0

        def __init__(self, *args):
            if len(args) == 1:
                if isinstance(args[0], BinaryReader):
                    self.stringId = args[0].ReadInt32()
                    self.frameNo = args[0].ReadInt32()

    class InstanceName(StringBase):
        def __init__(self, *args):
            if len(args) == 1:
                if isinstance(args[0], BinaryReader):
                    self.stringId = args[0].ReadInt32()

    class Event(StringBase):
        def __init__(self, *args):
            if len(args) == 1:
                if isinstance(args[0], BinaryReader):
                    self.stringId = args[0].ReadInt32()

    class String:
        stringOffset = 0
        stringLength = 0

        def __init__(self, *args):
            if len(args) == 1:
                if isinstance(args[0], BinaryReader):
                    self.stringOffset = args[0].ReadInt32()
                    self.stringLength = args[0].ReadInt32()

    class Place:
        depth = 0
        objectId = 0
        instanceId = 0
        matrixId = 0
        blendMode = 0

        def __init__(self, *args):
            if len(args) == 1:
                if isinstance(args[0], BinaryReader):
                    self.depth = args[0].ReadInt32()
                    self.objectId = args[0].ReadInt32()
                    self.instacneId = args[0].ReadInt32()
                    self.matrixId = args[0].ReadInt32()
                    self.blendMode = self.depth >> 24
                    self.depth &= 0xffffff

    class ControlMoveM:
        placeId = 0
        matrixId = 0

        def __init__(self, *args):
            if len(args) == 1:
                if isinstance(args[0], BinaryReader):
                    self.placeId = args[0].ReadInt32()
                    self.matrixId = args[0].ReadInt32()

    class ControlMoveC:
        placeId = 0
        colorTransformId = 0

        def __init__(self, *args):
            if len(args) == 1:
                if isinstance(args[0], BinaryReader):
                    self.placeId = args[0].ReadInt32()
                    self.colorTransformId = args[0].ReadInt32()

    class ControlMoveMC:
        placeId = 0
        matrixId = 0
        colorTransformId = 0

        def __init__(self, *args):
            if len(args) == 1:
                if isinstance(args[0], BinaryReader):
                    self.placeId = args[0].ReadInt32()
                    self.matrixId = args[0].ReadInt32()
                    self.colorTransformId = args[0].ReadInt32()

    class ControlMoveMCB:
        placeId = 0
        matrixId = 0
        colorTransformId = 0
        blendMode = 0

        def __init__(self, *args):
            if len(args) == 1:
                if isinstance(args[0], BinaryReader):
                    self.placeId = args[0].ReadInt32()
                    self.matrixId = args[0].ReadInt32()
                    self.colorTransformId = args[0].ReadInt32()
                    self.blendMode = args[0].ReadInt32()

    class Control:
        controlType = 0
        controlId = 0

        def __init__(self, *args):
            if len(args) == 1:
                if isinstance(args[0], BinaryReader):
                    self.controlType = args[0].ReadInt32()
                    self.controlId = args[0].ReadInt32()

        class Type:
            MOVE = 0
            MOVEM = 1
            MOVEC = 2
            MOVEMC = 3
            ANIMATION = 4
            MOVEMCB = 5
            CONTROL_MAX = 6

    class Frame:
        controlOffset = 0
        controls = 0

        def __init__(self, *args):
            if len(args) == 1:
                if isinstance(args[0], BinaryReader):
                    self.controlOffset = args[0].ReadInt32()
                    self.controls = args[0].ReadInt32()

    class MovieClipEvent:
        clipEvent = 0
        animationid = 0

        def __init__(self, *args):
            if len(args) == 1:
                if isinstance(args[0], BinaryReader):
                    self.clipEvent = args[0].ReadInt32()
                    self.animationId = args[0].ReadInt32()

        class ClipEvent:
            LOAD = (1 << 0)
            UNLOAD = (1 << 1)
            ENTERFRAME = (1 << 2)

    class Movie:
        depths = 0
        labelOffset = 0
        labels = 0
        frameOffset = 0
        frames = 0
        clipEventId = 0
        clipEvents = 0

        def __init__(self, *args):
            if len(args) == 1:
                if isinstance(args[0], BinaryReader):
                    self.depths = args[0].ReadInt32()
                    self.labelOffset = args[0].ReadInt32()
                    self.labels = args[0].ReadInt32()
                    self.framesOffset = args[0].ReadInt32()
                    self.frames = args[0].ReadInt32()
                    self.clipEventId = args[0].ReadInt32()
                    self.clipEvents = args[0].ReadInt32()

    class MovieLinkage(StringBase):
        movieId = 0

        def __init__(self, *args):
            if len(args) == 1:
                if isinstance(args[0], BinaryReader):
                    self.stringId = args[0].ReadInt32()
                    self.movieId = args[0].ReadInt32()

    class ItemArray:
        offset = 0
        length = 0

        def __init__(self, *args):
            if len(args) == 1:
                if isinstance(args[0], BinaryReader):
                    self.offset = args[0].ReadInt32()
                    self.length = args[0].ReadInt32()

    class Header:
        id0 = 0000
        id1 = 0000
        id2 = 0000
        id3 = 0000
        formatVersion0 = 0000
        formatVersion1 = 0000
        formatVersion2 = 0000
        formatVersion = 0000
        option = 0000
        width = 0
        height = 0
        frameRate = 0
        rootMovieId = 0
        nameStringId = 0
        backgroundColor = 0
        stringBytes = None
        animationBytes = None
        translate = None
        matrix = None
        color = None
        alphaTransform = None
        colorTransform = None
        objectData = None
        texture = None
        textureFragment = None
        bitmap = None
        bitmapEx = None
        font = None
        textProperty = None
        text = None
        particleData = None
        particle = None
        programObject = None
        graphicObject = None
        graphic = None
        animation = None
        buttonCondition = None
        button = None
        label = None
        instanceName = None
        eventData = None
        place = None
        controlMoveM = None
        controlMoveC = None
        controlMoveMC = None
        controlMoveMCB = None
        control = None
        frame = None
        movieClipEvent = None
        movie = None
        movieLinkage = None
        stringData = None
        lwfLength = 0

        def __init__(self, *args):
            if len(args) == 1:
                if isinstance(args[0], BinaryReader):
                    br = args[0]
                    self.id0 = br.ReadByte()
                    self.id1 = br.ReadByte()
                    self.id2 = br.ReadByte()
                    self.id3 = br.ReadByte()
                    self.formatVersion0 = br.ReadByte()
                    self.formatVersion1 = br.ReadByte()
                    self.formatVersion2 = br.ReadByte()
                    self.formatVersion = (self.formatVersion0 << 16) | (self.formatVersion1 << 8) | self.formatVersion2
                    self.option = br.ReadByte()
                    self.width = br.ReadInt32()
                    self.height = br.ReadInt32()
                    self.frameRate = br.ReadInt32()
                    self.rootMovieId = br.ReadInt32()
                    self.nameStringId = br.ReadInt32()
                    self.backgroundColor = br.ReadInt32()
                    self.stringBytes = Format.ItemArray(br)
                    self.animationBytes = Format.ItemArray(br)
                    self.translate = Format.ItemArray(br)
                    self.matrix = Format.ItemArray(br)
                    self.color = Format.ItemArray(br)
                    self.alphaTransform = Format.ItemArray(br)
                    self.colorTransform = Format.ItemArray(br)
                    self.objectData = Format.ItemArray(br)
                    self.texture = Format.ItemArray(br)
                    self.textureFragment = Format.ItemArray(br)
                    self.bitmap = Format.ItemArray(br)
                    self.bitmapEx = Format.ItemArray(br)
                    self.font = Format.ItemArray(br)
                    self.textProperty = Format.ItemArray(br)
                    self.text = Format.ItemArray(br)
                    self.particleData = Format.ItemArray(br)
                    self.particle = Format.ItemArray(br)
                    self.programObject = Format.ItemArray(br)
                    self.graphicObject = Format.ItemArray(br)
                    self.graphic = Format.ItemArray(br)
                    self.animation = Format.ItemArray(br)
                    self.buttonCondition = Format.ItemArray(br)
                    self.button = Format.ItemArray(br)
                    self.label = Format.ItemArray(br)
                    self.instanceName = Format.ItemArray(br)
                    self.eventData = Format.ItemArray(br)
                    self.place = Format.ItemArray(br)
                    self.controlMoveM = Format.ItemArray(br)
                    self.controlMoveC = Format.ItemArray(br)
                    self.controlMoveMC = Format.ItemArray(br)
                    if self.formatVersion >= int(Format.Constant.FORMAT_VERSION_141211):
                        self.controlMoveMCB = Format.ItemArray(br)
                    else:
                        self.controlMoveMCB = Format.ItemArray()
                    self.control = Format.ItemArray(br)
                    self.frame = Format.ItemArray(br)
                    self.movieClipEvent = Format.ItemArray(br)
                    self.movie = Format.ItemArray(br)
                    self.movieLinkage = Format.ItemArray(br)
                    self.stringData = Format.ItemArray(br)
                    self.lwfLength = br.ReadInt32()
