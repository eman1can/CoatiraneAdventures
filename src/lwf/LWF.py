"""
    Copyright (C) 2012 GREE, Inc.

    This software is provided 'as-is', without any express or implied
    warranty.  In no event will the authors be held liable for any damages
    arising from the use of this software.

    Permission is granted to anyone to use this software for any purpose,
    including commercial applications, and to alter it and redistribute it
    freely, subject to the following restrictions:
    1. The origin of this software must not be misrepresented; you must not
        claim that you wrote the original software. If you use this software
        in a product, an acknowledgment in the product documentation would be
        appreciated but is not required.
    2. Altered source versions must be plainly marked as such, and must not be
        misrepresented as being the original software.
    3. This notice may not be removed or altered from any source distribution.
-------------------------------------------------------------------------------

Code Altered By Ethan Wolfe @ 2019
Description:
A purely Python implementation of GREE's Lwf C# Library implementation for use in Coatirane Adventures Game

Added:
lwf_core       - Go Over Again
lwf_animation
lwf_bitmap
lwf_bitmapEx
lwf_button
lwf_bitmapClip
lwf_object
lwf_IObject
lwf_type
lwf_utility
lwf_text
lwf_format
lwf_coredata
lwf_eventmovie
lwf_movie
lwf_property
lwf_graphic
lwf_particle
lwf_programobj
lwf_eventbutton
lwf_coreop
lwf_data
lwf_renderer
lwf_lwfcontainer
lwf_movieprop
lwf_movieop
lwf_movieat

"""

# import statements
from enum import Enum
from datetime import datetime
from typing import List

from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics.texture import Texture
from itertools import chain
from kivy.graphics import Color as KivyColor
from kivy.graphics import PushMatrix, PopMatrix, InstructionGroup, Scale, Translate, Rectangle
from lzma import LZMADecompressor

from sortedcontainers import SortedDict
from struct import unpack
import math
import re

# Constant Variables
INT32_MINVALUE = -2147483648
SINGLE_MINVALUE = -3.402823E+38
FLOAT_MAXVALUE = 3.402823E+38
FLOAT_MINVALUE = -3.402823E+38


# Pre Classes ------------------------------------------------------------
class BoundingRect:
    left = 0
    top = 0
    right = 0
    bottom = 0
    x = 0
    y = 0
    width = 0
    height = 0

# lwf_loader -----------------------------------------------------------------
class BinaryReader:
    def __init__(self, bytesArray):
        self.byteArray = bytesArray
        self.pos = 0

    def ReadByte(self):
        byte = self.byteArray[self.pos]
        self.pos += 1
        return byte

    def ReadBytes(self, length):
        startPos = self.pos
        endPos = self.pos + length
        self.pos += length
        return self.byteArray[startPos:endPos]


    def ReadChar(self):
        return self.unpack('b')

    def ReadUChar(self):
        return self.unpack('B')

    def ReadBool(self):
        return self.unpack('?')

    def ReadInt16(self):
        return self.unpack('h', 2)

    def ReadUInt16(self):
        return self.unpack('H', 2)

    def ReadInt32(self):
        return self.unpack('i', 4)

    def ReadUInt32(self):
        return self.unpack('I', 4)

    def ReadInt64(self):
        return self.unpack('q', 8)

    def ReadUInt64(self):
        return self.unpack('Q', 8)

    def ReadSingle(self):
        return self.unpack('f', 4)

    def ReadDouble(self):
        return self.unpack('d', 8)

    def unpack(self, fmt, length=1):
        return unpack(fmt, self.ReadBytes(length))[0]



class Loader:
    @staticmethod
    def load(d):
        if not d or not isinstance(d, bytes):
            return
        print("Loading Data!")
        print(d)
        return Data(d)

    @staticmethod
    def loadArray(d):
        Loader.load(d)


# ------------------------ lwf_data ------------------------------------------

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
        if len(byteArray) < int(Format.Constant.HEADER_SIZE_COMPAT0.value):
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

            if code is Animation.PLAY.value or code is Animation.STOP.value or code is Animation.NEXTFRAME.value \
                    or code is Animation.PREVFRAME.value:
                pass
            elif code is Animation.GOTOFRAME.value or code is Animation.GOTOLABEL.value or code is Animation.EVENT.value \
                    or code is Animation.CALL.value:
                array.append(br.ReadInt32())
            elif code is Animation.SETTARGET.value:
                count = br.ReadInt32()
                array.append(count)
                for i in range(0, int(count)):
                    target = br.ReadInt32()
                    array.append(target)
            elif code is Animation.END.value:
                for i in range(0, len(array)):
                    array[i] = int(array[i])
                return array


# ------------------------ lwf_core   ----------------------------------------

class TextDictionaryItem:
    text = None
    renderer = None

    def __init__(self, *args):
        self.text = args[0]
        self.renderer = args[1] if len(args) is 2 else None


# ------------------------- lwf_movie -------------------------------------

class LabelData:
    frame = 0
    name = 0


# ------------------------ lwf_format ------------------------------------

class Format:
    class Constant(Enum):
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
        MATRIX_FLAG_MASK = MATRIX_FLAG
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

        class Attribute(Enum):
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

        class Align(Enum):
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

        class Type(Enum):
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

        class Type(Enum):
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

        class Condition(Enum):
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

        class Type(Enum):
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

        class ClipEvent(Enum):
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
                    if self.formatVersion >= int(Format.Constant.FORMAT_VERSION_141211.value):
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


# ------------------------ lwf_type --------------------------------------

class Point:
    x = 0.0
    y = 0.0

    def __init__(self, px=0, py=0):
        self.x = px
        self.y = py


class Translate:
    translateX = 0.0
    translateY = 0.0

    def __init__(self, *args):
        if len(args) == 1:
            if isinstance(args[0], BinaryReader):
                br = args[0]
                self.translateX = br.ReadSingle()
                self.translateY = br.ReadSingle()
        else:
            self.translateX = 0.0
            self.translateY = 0.0


class Matrix:
    scaleX = 0.0
    scaleY = 0.0
    skew0 = 0.0
    skew1 = 0.0
    translateX = 0.0
    translateY = 0.0

    def __init__(self, *args):
        if len(args) is 0:
            self.Clear()
        elif len(args) is 1:
            if isinstance(args[0], BinaryReader):
                br = args[0]
                self.scaleX = br.ReadSingle()
                self.scaleY = br.ReadSingle()
                self.skew0 = br.ReadSingle()
                self.skew1 = br.ReadSingle()
                self.translateX = br.ReadSingle()
                self.translateY = br.ReadSingle()
            else:
                self.Set(args[0])
        else:
            self.scaleX, self.scaleY, self.skew0, self.skew1, self.translateX, self.translateY = args[0:6]

    def Clear(self):
        self.scaleX = 1
        self.scaleY = 1
        self.skew0 = 0
        self.skew1 = 0
        self.translateX = 0
        self.translateY = 0

    def Set(self, m):
        self.scaleX = m.scaleX
        self.scaleY = m.scaleY
        self.skew0 = m.skew0
        self.skew1 = m.skew1
        self.translateX = m.translateX
        self.translateY = m.translateY
        return self

    def SetWithComparing(self, m):
        if m is None:
            return False
        sX = m.scaleX
        sY = m.scaleY
        s0 = m.skew0
        s1 = m.skew1
        tX = m.translateX
        tY = m.translateY
        changed = False
        if self.scaleX is not sX:
            self.scaleX = sX
            changed = True
        if self.scaleY is not sY:
            self.scaleY = sY
            changed = True
        if self.skew0 is not s0:
            self.skew0 = s0
            changed = True
        if self.skew1 is not s1:
            self.skew1 = s1
            changed = True
        if self.translateX is not tX:
            self.translateX = tX
            changed = True
        if self.translateY is not tY:
            self.translateY = tY
            changed = True
        return changed


class Color:
    red = 0
    green = 0
    blue = 0
    alpha = 0

    def __init__(self, *args):
        if len(args) > 0:
            if isinstance(args[0], BinaryReader):
                br = args[0]
                self.red = br.ReadSingle()
                self.green = br.ReadSingle()
                self.blue = br.ReadSingle()
                self.alpha = br.ReadSingle()
            else:
                self.Set(args[0], args[1], args[2], args[3])

    def Set(self, r, g, b, a):
        self.red, self.green, self.blue, self.alpha = r, g, b, a

    def Equals(self, c):
        return self.red == c.red and self.green == c.green and self.blue == c.blue and self.alpha == c.alpha


class AlphaTransform:
    alpha = 0

    def __init__(self, *args):
        if len(args) is 0:
            self.alpha = 1
        else:
            if isinstance(args[0], BinaryReader):
                br = args[0]
                self.alpha = br.ReadSingle()
            else:
                self.alpha = args[0]


class ColorTransform:
    multi = None
    add = None

    def __init__(self, *args):
        if len(args) is 1:
            if isinstance(args[0], BinaryReader):
                br = args[0]
                self.multi = Color(br)
                self.add = Color(br)
            else:
                self.multi = Color()
                self.add = Color()
                self.Set(args[0])
        elif len(args) == 8:
            self.multi = Color(args[0], args[1], args[2], args[3])
            self.add = Color(args[4], args[5], args[6], args[7])
        else:
            self.multi = Color(1, 1, 1, 1)
            self.add = Color(0, 0, 0, 0)

    def Clear(self):
        self.multi.Set(1, 1, 1, 1)
        self.add.Set(0, 0, 0, 0)

    def Set(self, c):
        self.multi.Set(c.multi.red, c.multi.green, c.multi.blue, c.multi.alpha)
        self.add.Set(c.add.red, c.add.green, c.add.blue, c.add.alpha)

    def SetWithComparing(self, c):
        if c is None:
            return False
        cm = c.multi
        red = cm.red
        blue = cm.blue
        green = cm.green
        alpha = cm.alpha
        changed = False
        m = self.multi
        if m.red is not red:
            m.red = red
            changed = True
        if m.green is not green:
            m.green = green
            changed = True
        if m.blue is not blue:
            m.blue = blue
            changed = True
        if m.alpha is not alpha:
            m.alpha = alpha
            changed = True

        ca = c.add
        red = ca.red
        green = ca.green
        blue = ca.blue
        alpha = ca.alpha
        a = self.add
        if a.red is not red:
            a.red = red
            changed = True
        if a.green is not green:
            a.green = green
            changed = True
        if a.blue is not blue:
            a.blue = blue
            changed = True
        if a.alpha is not alpha:
            a.alpha = alpha
            changed = True

        return changed


class Bounds:
    xMin: float = 0.0
    xMax: float = 0.0
    yMin: float = 0.0
    yMax: float = 0.0

    def __init__(self, pxMin: float = 0.0, pxMax=0.0, pyMin: float = 0.0, pyMax: float = 0.0):
        self.xMin = pxMin
        self.xMax = pxMax
        self.yMin = pyMin
        self.yMax = pyMax


# -----------------------  lwf_utility -----------------------------------

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


# lwf_animation ----------------------------------------------------------

class Animation(Enum):
    END = 0
    PLAY = 1
    STOP = 2
    NEXTFRAME = 3
    PREVFRAME = 4
    GOTOFRAME = 5  # FRAMENO(4bytes)
    GOTOLABEL = 6  # LABELID(4bytes)
    SETTARGET = 7  # COUNT(1byte) INSTANCEID(4bytes)
    # SETTARGET 0           :myself
    # SETTARGET 1 ROOT      :root
    # SETTARGET 1 PARENT    :parent
    # SETTARGET 1 ID        :child
    # SETTARGET 2 PARENT ID :sibling
    # SETTARGET 2 ROOT ID   :root/child
    EVENT = 8
    CALL = 9
    INSTANCE_TARGET_ROOT = -1
    INSTANCE_TARGET_PARENT = -2


# lwf_object -------------------------------------------------------------

class Object:
    m_lwf = None
    m_parent = None
    m_type = None
    m_execCount = 0
    m_objectId = 0
    m_matrixId = 0
    m_colorTransformId = 0
    m_matrix = None
    m_dataMatrixId = 0
    m_colorTransform = None
    m_renderer = None
    m_matrixIdChanged = False
    m_colorTransformIdChanged = False
    m_updated = False

    def __init__(self, *args):
        if len(args) > 0:
            lwf, parent, otype, objId = args[0:4]
            self.m_lwf = lwf
            self.m_parent = parent
            self.m_type = otype
            self.m_objectId = objId
            self.m_matrixId = -1
            self.m_colorTransformId = -1
            self.m_matrixIdChanged = True
            self.m_colorTransformIdChanged = True
            self.m_matrix = Matrix(0, 0, 0, 0, 0, 0)
            self.m_colorTransform = ColorTransform(0, 0, 0, 0)
            self.m_execCount = 0
            self.m_updated = False

    # getters and setters
    @property
    def lwf(self):
        return self.m_lwf

    @property
    def parent(self):
        return self.m_parent

    @property
    def type(self):
        return self.m_type

    @property
    def objectId(self):
        return self.m_objectId

    @property
    def matrixId(self):
        return self.m_matrixId

    @property
    def colorTransformId(self):
        return self.m_colorTransformId

    @property
    def matrix(self):
        return self.m_matrix

    @property
    def colorTransform(self):
        return self.m_colorTransform

    @property
    def matrixIdChanged(self):
        return self.m_matrixIdChanged

    @matrixIdChanged.setter
    def matrixIdChanged(self, value):
        self.m_matrixIdChanged = value

    @property
    def colorTransformIdChanged(self):
        return self.m_colorTransformIdChanged

    @colorTransformIdChanged.setter
    def colorTransformIdChanged(self, value):
        self.m_colorTransformIdChanged = value

    @property
    def updated(self):
        return self.m_updated

    @property
    def execCount(self):
        return self.m_execCount

    @execCount.setter
    def execCount(self, value):
        self.m_execCount = value

    def Exec(self, matrixId=0, colorTransformId=0):
        if self.m_matrixId is not matrixId:
            self.m_matrixIdChanged = True
            self.m_matrixId = matrixId
        if self.m_colorTransformId is not colorTransformId:
            self.m_colorTransformIdChanged = True
            self.m_colorTransformId = colorTransformId

    def Update(self, m, c):
        self.m_updated = True
        if m is not None:
            Utility.CalcMatrix(self.m_lwf, self.m_matrix, m, self.m_dataMatrixId)
            self.m_matrixIdChanged = True
        if c is not None:
            Utility.CopyColorTransform(self.m_colorTransform, c)
            self.m_colorTransformIdChanged = True
        self.m_lwf.RenderObject()

    def Render(self, v, rOffset):
        if self.m_renderer is not None:
            rIndex = self.m_lwf.renderingIndex
            rIndexOffsetted = self.m_lwf.renderingIndexOffsetted
            rCount = self.m_lwf.renderingCount
            if rOffset != INT32_MINVALUE:
                rIndex = rIndexOffsetted - rOffset + rCount
            self.m_renderer.Render(self.m_matrix, self.m_colorTransform, rIndex, rCount, v)
        self.m_lwf.RenderObject()

    def Inspect(self, inspector, hierarchy, depth, rOffset):
        rIndex = self.m_lwf.renderingIndex
        rIndexOffsetted = self.m_lwf.renderingIdexOfsetted
        rCount = self.m_lwf.renderingCount
        if rOffset != INT32_MINVALUE:
            rIndex = rIndexOffsetted + rOffset + rCount
        inspector(self, hierarchy, depth, rIndex)
        self.m_lwf.RenderObject()

    def Destroy(self):
        if self.m_renderer is not None:
            self.m_renderer.Destruct()
            self.m_renderer = None

    def IsButton(self):
        return True if self.m_type == Format.Object.Type.BUTTON else False

    def IsMovie(self):
        return True if self.m_type == Format.Object.Type.MOVIE or self.m_type == Format.Object.Type.ATTACHEDMOVIE \
            else False

    def IsParticle(self):
        return True if self.m_type == Format.Object.Type.PARTICLE else False

    def IsProgramObject(self):
        return True if self.m_type == Format.Object.Type.PROGRAMOBJECT else False

    def IsText(self):
        return True if self.m_type == Format.Object.Type.TEXT else False

    def IsBitmapClip(self):
        return False


# lwf_iobject ------------------------------------------------------------

class IObject(Object):
    m_instanceId = 0
    m_iObjectId = 0
    m_name = None
    m_prevInstance = None
    m_nextInstance = None
    m_linkInstance = None
    m_alive = False

    def __init__(self, *args):
        if len(args) > 0:
            lwf, parent, otype, objId, instId = args[0:5]
            super().__init__(lwf, parent, otype, objId)
            self.m_alive = True

            self.m_instanceId = -1 if instId >= len(lwf.data.instanceNames) else instId
            print(lwf.data.instanceNames[0].stringId)
            self.m_iObjectId = lwf.GetIObjectOffset()

            if self.m_instanceId >= 0:
                stringId = lwf.GetInstanceNameStringId(self.m_instanceId)
                self.m_name = None if stringId == -1 else lwf.data.strings[stringId]

                print(self.m_lwf.m_instances)
                head = self.m_lwf.GetInstance(self.m_instanceId)
                if head is not None:
                    head.m_prevInstance = self
                self.m_nextInstance = head
                self.m_lwf.SetInstance(self.m_instanceId, self)

    @property
    def nextInstance(self):
        return self.m_nextInstance

    @property
    def linkInstance(self):
        return self.m_linkInstance

    @linkInstance.setter
    def linkInstance(self, value):
        self.m_linkInstance = value

    @property
    def instanceId(self):
        return self.m_instanceId

    @property
    def iObjectId(self):
        return self.m_iObjectId

    @property
    def name(self):
        return self.m_name

    def Destroy(self):
        if self.m_type is not Format.Object.Type.ATTACHEDMOVIE and self.m_instanceId >= 0:
            head = self.m_lwf.GetInstance(self.m_instanceId)
            if head is self:
                self.m_lwf.SetInstance(self.m_instanceId, self.m_nextInstance)
            if self.m_nextInstance is not None:
                self.m_nextInstance.m_prevInstance = self.m_prevInstance
            if self.m_prevInstance is not None:
                self.m_prevInstance.m_nextInstance = self.m_nextInstance

        super().Destroy()
        self.m_alive = False

    def LinkButton(self):
        pass

    def GetFullName(self):
        o = self
        fullPath = ""
        splitter = ""
        while o is not None:
            if o.name is None:
                return None
            fullPath = o.name + splitter + fullPath
            splitter = "."
            o = o.parent


# lwf_renderer -----------------------------------------------------------

class Renderer:
    m_lwf = None

    @property
    def lwf(self):
        return self.m_lwf

    def __init__(self, lwf):
        self.m_lwf = lwf

    def Destruct(self):
        pass

    def Update(self, matrix, colorTransform):
        pass

    def Render(self, matrix, colorTransform, renderingIndex, renderingCount, visible):
        pass


class TextRenderer(Renderer):
    def __init__(self, lwf):
        super().__init__(lwf)

    def SetText(self, text):
        pass


class IRendererFactory:
    def ConstructBitmap(self, lwf, objId, bitmap):
        pass

    def ConstructBitmapEx(self, lwf, objId, bitmapEx):
        pass

    def ConstructText(self, lwf, objId, text):
        pass

    def ConstructParticle(self, lwf, objId, particle):
        pass

    def Init(self, lwf):
        pass

    def BeginRender(self, lwf):
        pass

    def EndRender(self, lwf):
        pass

    def Destruct(self, lwf):
        pass

    def SetBlendMode(self, blendMode):
        pass

    def SetMaskMode(self, maskMode):
        pass


class NullRendererFactory(IRendererFactory):
    def ConstructBitmap(self, lwf, objId, bitmap):
        return None

    def ConstructBitmapEx(self, lwf, objId, bitmapEx):
        return None

    def ConstructText(self, lwf, objId, text):
        return None

    def ConstructParticle(self, lwf, objId, particle):
        return None

    def Init(self, lwf):
        pass

    def BeginRender(self, lwf):
        pass

    def EndRender(self, lwf):
        pass

    def Destruct(self, lwf):
        pass

    def SetBlendMode(self, blendMode):
        pass

    def SetMaskMode(self, maskMode):
        pass


# lwf_eventmovie ---------------------------------------------------------

class Dictionary:
    data = {}

    def __init__(self, *args):
        if len(args) > 0:
            assert isinstance(args[0], Dictionary)
            self.data = args[0].copy()

    def __len__(self):
        return len(self.data)

    def get(self, key):
        return self.data[key]

    def set(self, key, value):
        self.data[key] = value

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def copy(self):
        return self.data.copy()

    def contains(self, item):
        return self.data.contains(item)

    def __delete__(self, instance):
        del self.data

    def remove(self, key):
        del self.data[key]

    def clear(self):
        self.data = {}

    def items(self):
        return self.data.items()

    def values(self):
        return self.data.values()

    def keys(self):
        return self.data.keys()

    def TryGetValue(self, key):
        if key in self.data:
            return True, self.data[key]
        else:
            return False, None

    def __iter__(self):
        self.posistion = 0
        return self

    def __next__(self):
        self.posistion += 1
        return self.posistion < len(self.data.keys())

    def current(self):
        return self.data.keys[self.posistion]


class Dict(dict):
    def __init__(self):
        super().__init__()
    def TryGetValue(self, key):
        if key in self.keys():
            return True, self[key]
        else:
            return False, None


class MovieEventHandlerDictionary(Dictionary):
    pass


class MovieEventHandlers:
    load = None
    postLoad = None
    unload = None
    enterFrame = None
    update = None
    render = None
    empty = False

    class Type(Enum):
        LOAD = 0
        POSTLOAD = 1
        UNLOAD = 2
        ENTERFRAME = 3
        UPDATE = 4
        RENDER = 5

    def __init__(self):
        self.load = MovieEventHandlerDictionary()
        self.postLoad = MovieEventHandlerDictionary()
        self.unload = MovieEventHandlerDictionary()
        self.enterFrame = MovieEventHandlerDictionary()
        self.update = MovieEventHandlerDictionary()
        self.render = MovieEventHandlerDictionary()
        self.empty = True

    def Clear(self, *args):
        if len(args) is 0:
            self.load.clear()
            self.postLoad.clear()
            self.unload.clear()
            self.enterFrame.clear()
            self.update.clear()
            self.render.clear()
            self.empty = True
        else:
            if args[0] == self.Type.LOAD.value:
                self.load.clear()
            elif args[0] == self.Type.POSTLOAD.value:
                self.postLoad.clear()
            elif args[0] == self.Type.UNLOAD.value:
                self.unload.clear()
            elif args[0] == self.Type.ENTERFRAME.value:
                self.enterFrame.clear()
            elif args[0] == self.Type.UPDATE.value:
                self.update.clear()
            elif args[0] == self.Type.RENDER.value:
                self.render.clear()
            self.UpdateEmpty()

    def Add(self, arg0, load=None, p=None, u=None, e=None, up=None, r=None):
        if not isinstance(arg0, int):
            handlers = arg0
            if handlers is None:
                return

            print(handlers.load)
            for hk, hv in handlers.load.items():
                self.load[hk] = hv
            for hk, hv in handlers.postLoad.items():
                self.postLoad[hk] = hv
            for hk, hv in handlers.unload.items():
                self.unload[hk] = hv
            for hk, hv in handlers.enterFrame.items():
                self.enterFrame[hk] = hv
            for hk, hv in handlers.update.items():
                self.update[hk] = hv
            for hk, hv in handlers.render.items():
                self.render[hk] = hv
            self.UpdateEmpty()
        else:
            key = arg0
            if load is not None:
                self.load[key] = load
            if p is not None:
                self.load[key] = p
            if u is not None:
                self.load[key] = u
            if e is not None:
                self.load[key] = e
            if up is not None:
                self.load[key] = up
            if r is not None:
                self.load[key] = r
            self.UpdateEmpty()

    def Remove(self, key):
        self.load.remove(key)
        self.postLoad.remove(key)
        self.unload.remove(key)
        self.enterFrame.remove(key)
        self.update.remove(key)
        self.render.remove(key)
        self.UpdateEmpty()

    def Call(self, htype, target):
        dictionary = None
        if htype == self.Type.LOAD.value:
            dictionary = self.load
        elif htype == self.Type.POSTLOAD.value:
            dictionary = self.postLoad
        elif htype == self.Type.UNLOAD.value:
            dictionary = self.unload
        elif htype == self.Type.ENTERFRAME.value:
            dictionary = self.enterFrame
        elif htype == self.Type.UPDATE.value:
            dictionary = self.update
        elif htype == self.Type.RENDER.value:
            dictionary = self.render
        if dictionary is not None:
            dictionary = MovieEventHandlerDictionary(dictionary)
            for h in dictionary.values():
                h(target)

    def UpdateEmpty(self):
        self.empty = True
        if len(self.load) > 0:
            self.empty = False
            return
        if len(self.postLoad) > 0:
            self.empty = False
            return
        if len(self.unload) > 0:
            self.empty = False
            return
        if len(self.enterFrame) > 0:
            self.empty = False
            return
        if len(self.update) > 0:
            self.empty = False
            return
        if len(self.render) > 0:
            self.empty = False
            return

    def Empty(self):
        return self.empty


# ------------------------ lwf_movie  -------------------------------------

class Action:
    def __init__(self):
        self.value = None

    def __set__(self, instance, value):
        self.value = value

    def __get__(self, instance, owner):
        return self.value

    def __delete__(self, instance):
        del self.value


class SortedList(list):

    def Sort(self, comparison, left=0, r=0):
        if r is 0:
            r = len(self) - 1
        if left >= r:
            return

        pivot = self[r]
        cnt = left
        for i in range(left, r + 1):
            if comparison(self[i], pivot):
                self[cnt], self[i] = self[i], self[cnt]
                cnt += 1
        self.Sort(comparison, left, cnt - 2)
        self.Sort(comparison, cnt, r)


class EventHandler(Action):
    pass


class MovieEventHandler(Action):
    pass


class CurrentLabels(SortedList):
    pass


class CurrentLabelCache(Dictionary):
    pass


class Texts(Dictionary):
    pass


class EventHandlerDictionary(Dictionary):
    pass


class EventHandlers(Dictionary):
    pass


class CalculateBoundsCallbacks(SortedList):
    pass


# lwf_movieat ------------------------------------------------------------

class SortedDictionary(SortedDict):
    def TryGetValue(self, key):
        if key in self:
            return True, self[key]
        else:
            return False, None

    def __iter__(self):
        self.position = 0
        return self

    def __next__(self):
        self.position += 1
        return self.position < len(self.keys())

    def current(self):
        return self.keys()[self.position]

    def remove(self, key):
        self._list_remove(key)


class AttachedMovies(Dictionary):
    pass


class AttachedMovieList(SortedDictionary):
    pass


class AttachedMovieDescendingList(SortedDictionary):
    def __iter__(self):
        self.position = len(self.keys()) - 1
        return self

    def __next__(self):
        self.position -= 1
        return self.position < len(self.keys())

    def current(self):
        return self.keys()[self.position]


class AttachedLWFs(Dictionary):
    pass


class AttachedLWFList(SortedDictionary):
    pass


class AttachedLWFDescendingList(SortedDictionary):
    def __iter__(self):
        self.position = len(self.keys()) - 1
        return self

    def __next__(self):
        self.position -= 1
        return self.position < len(self.keys())

    def current(self):
        return self.keys()[self.position]


class DetachDict(Dictionary):
    pass


class BitmapClips(SortedDictionary):
    pass


# ----------------------- lwf_button -------------------------------------

class ButtonEventHandler(Action):
    pass


class ButtonKeyPressHandler(Action):
    pass


class ButtonEventHandlerDictionary(Dictionary):
    pass


class ButtonKeyPressHandlerDictionary(Dictionary):
    pass


# lwf_event ---------------------------------------------------------------

class GenericEventHandlerDictionary(Dictionary):
    pass


class MovieEventHandlersDictionary(Dictionary):
    pass


class ButtonEventHandlersDictionary(Dictionary):
    pass


# ----------------------- lwf_eventbutton ---------------------------------

class ButtonEventHandlers:
    class Type(Enum):
        LOAD = 0
        UNLOAD = 1
        ENTERFRAME = 2
        UPDATE = 3
        RENDER = 4
        PRESS = 5
        RELEASE = 6
        ROLLOVER = 7
        KEYPRESS = 8

    load = None
    unload = None
    enterFrame = None
    update = None
    render = None
    press = None
    release = None
    rollOver = None
    rollOut = None
    keyPress = None

    def __init__(self):
        self.load = ButtonEventHandlerDictionary()
        self.unload = ButtonEventHandlerDictionary()
        self.enterFrame = ButtonEventHandlerDictionary()
        self.update = ButtonEventHandlerDictionary()
        self.render = ButtonEventHandlerDictionary()
        self.press = ButtonEventHandlerDictionary()
        self.release = ButtonEventHandlerDictionary()
        self.rollOver = ButtonEventHandlerDictionary()
        self.rollOut = ButtonEventHandlerDictionary()
        self.keyPress = ButtonKeyPressHandlerDictionary()

    def Clear(self, *args):
        if len(args) is 0:
            self.load.clear()
            self.unload.clear()
            self.enterFrame.clear()
            self.update.clear()
            self.render.clear()
            self.press.clear()
            self.release.clear()
            self.rollOver.clear()
            self.rollOut.clear()
            self.keyPress.clear()
        else:
            if args[0] == ButtonEventHandlers.Type.LOAD.value:
                self.load.clear()
            elif args[0] == ButtonEventHandlers.Type.UNLOAD.value:
                self.unload.clear()
            elif args[0] == ButtonEventHandlers.Type.RENDER.value:
                self.render.clear()
            elif args[0] == ButtonEventHandlers.Type.PRESS.value:
                self.press.clear()
            elif args[0] == ButtonEventHandlers.Type.RELEASE.value:
                self.release.clear()
            elif args[0] == ButtonEventHandlers.Type.ROLLOVER.value:
                self.rollOver.clear()
            elif args[0] == ButtonEventHandlers.Type.ROLLOUT.value:
                self.rollOut.clear()
            elif args[0] == ButtonEventHandlers.Type.KEYPRESS.value:
                self.keyPress.clear()

    def Add(self, arg, load=None, u=None, e=None, up=None, r=None, p=None, rl=None, rOver=None, rOut=None, k=None):
        if not isinstance(arg, int):
            handlers = arg
            if handlers is None:
                return

            for hk, hv in handlers.load:
                self.load.set(hk, hv)
            for hk, hv in handlers.unload:
                self.unload.set(hk, hv)
            for hk, hv in handlers.enterFrame:
                self.enterFrame.set(hk, hv)
            for hk, hv in handlers.update:
                self.update.set(hk, hv)
            for hk, hv in handlers.render:
                self.render.set(hk, hv)
            for hk, hv in handlers.press:
                self.press.set(hk, hv)
            for hk, hv in handlers.release:
                self.release.set(hk, hv)
            for hk, hv in handlers.rollOver:
                self.rollOver.set(hk, hv)
            for hk, hv in handlers.rollOut:
                self.rollOut.set(hk, hv)
            for hk, hv in handlers.keyPress:
                self.keyPress.set(hk, hv)
        else:
            key = arg
            if load is not None:
                self.load.set(key, load)
            if u is not None:
                self.unload.set(key, u)
            if e is not None:
                self.enterFrame.set(key, e)
            if up is not None:
                self.update.set(key, up)
            if r is not None:
                self.render.set(key, r)
            if p is not None:
                self.press.set(key, p)
            if rl is not None:
                self.release.set(key, rl)
            if rOver is not None:
                self.rollOver.set(key, rOver)
            if rOut is not None:
                self.rollOut.set(key, rOut)
            if k is not None:
                self.keyPress.set(key, k)

    def Remove(self, key):
        self.load.remove(key)
        self.unload.remove(key)
        self.enterFrame.remove(key)
        self.update.remove(key)
        self.render.remove(key)
        self.press.remove(key)
        self.release.remove(key)
        self.rollOver.remove(key)
        self.rollOut.remove(key)
        self.keyPress.remove(key)

    def Call(self, buttonType, target):
        dictionary = None
        if buttonType == ButtonEventHandlers.Type.LOAD.value:
            dictionary = self.load
        elif buttonType == ButtonEventHandlers.Type.UNLOAD.value:
            dictionary = self.unload
        elif buttonType == ButtonEventHandlers.Type.RENDER.value:
            dictionary = self.render
        elif buttonType == ButtonEventHandlers.Type.PRESS.value:
            dictionary = self.press
        elif buttonType == ButtonEventHandlers.Type.RELEASE.value:
            dictionary = self.release
        elif buttonType == ButtonEventHandlers.Type.ROLLOVER.value:
            dictionary = self.rollOver
        elif buttonType == ButtonEventHandlers.Type.ROLLOUT.value:
            dictionary = self.rollOut
        if dictionary is not None:
            dictionary = ButtonEventHandlerDictionary(dictionary)
            for k, v in dictionary.items():
                v(target)

    def CallKEYPRESS(self, target, code):
        dictionary = ButtonKeyPressHandlerDictionary(self.keyPress)
        for k, v in dictionary.items():
            v(target, code)


# ----------------------- lwf_property ------------------------------------

class Property:
    m_lwf = None
    m_matrix = None
    m_colorTransform = None
    m_scaleX = 1.0
    m_scaleY = 1.0
    m_rotation = 0.0
    m_renderingOffset = 0
    m_hasMatrix = False
    m_hasColorTransform = False

    def __init__(self, lwf):
        self.m_lwf = lwf
        self.m_matrix = Matrix()
        self.m_colorTransform = ColorTransform()
        self.ClearRenderingOffset()

    @property
    def matrix(self):
        return self.m_matrix

    @property
    def colorTransform(self):
        return self.m_colorTransform

    @property
    def renderingOffset(self):
        return self.m_renderingOffset

    @property
    def hasMatrix(self):
        return self.m_hasMatrix

    @property
    def hasColorTransform(self):
        return self.m_hasColorTransform

    @property
    def hasRenderingOffset(self):
        return self.m_renderingOffset != INT32_MINVALUE

    def Clear(self):
        self.m_scaleX = 1
        self.m_scaleY = 1
        self.m_rotation = 0
        self.m_matrix.Clear()
        self.m_colorTransform.Clear()
        if self.m_hasMatrix and self.m_hasColorTransform:
            self.m_lwf.SetPropertyDirty()
            self.m_hasMatrix = False
            self.m_hasColorTransform = False
        self.ClearRenderingOffset()

    def Move(self, x, y):
        self.m_matrix.translateX += x
        self.m_matrix.translateY += y
        self.m_hasMatrix = True
        self.m_lwf.SetPropertyDirty()

    def MoveTo(self, x, y):
        self.m_matrix.translateX = x
        self.m_matrix.translateY = y
        self.m_hasMatrix = True
        self.m_lwf.SetPropertyDirty()

    def Rotate(self, degree):
        self.RotateTo(self.m_rotation + degree)

    def RotateTo(self, degree):
        self.m_rotation = degree
        self.SetScaleAndRotation()

    def Scale(self, x, y):
        self.m_scaleX *= x
        self.m_scaleY *= y
        self.SetScaleAndRotation()

    def ScaleTo(self, x, y):
        self.m_scaleX = x
        self.m_scaleY = y
        self.SetScaleAndRotation()

    def SetScaleAndRotation(self):
        radian = self.m_rotation * math.pi / 180.0
        c = math.cos(radian)
        s = math.sin(radian)
        self.m_matrix.scaleX = self.m_scaleX * c
        self.m_matrix.skew0 = self.m_scaleY * -s
        self.m_matrix.skew1 = self.m_scaleX * s
        self.m_matrix.scaleY = self.m_scaleY * c
        self.m_hasMatrix = True
        self.m_lwf.SetPropertyDirty()

    def SetMatrix(self, m, sX=1, sY=1, r=0):
        self.m_matrix.Set(m)
        self.m_scaleX = sX
        self.m_scaleY = sY
        self.m_rotation = r
        self.m_hasMatrix = True
        self.m_lwf.SetPropertyDirty()

    def SetAlpha(self, alpha):
        self.m_colorTransform.multi.alpha = alpha
        self.m_hasColorTransform = True
        self.m_lwf.SetPropertyDirty()

    def SetRed(self, red):
        self.m_colorTransform.multi.red = red
        self.m_hasColorTransform = True
        self.m_lwf.SetPropertyDirty()

    def SetGreen(self, green):
        self.m_colorTransform.multi.green = green
        self.m_hasColorTransform = True
        self.m_lwf.SetPropertyDirty()

    def SetBlue(self, blue):
        self.m_colorTransform.multi.blue = blue
        self.m_hasColorTransform = True
        self.m_lwf.SetPropertyDirty()

    def SetColorTransform(self, c):
        self.m_colorTransform.Set(c)
        self.m_hasColorTransform = True
        self.m_lwf.SetPropertyDirty()

    def SetRenderingOffset(self, rOffset):
        self.m_renderingOffset = rOffset

    def ClearRenderingOffset(self):
        self.m_renderingOffset = INT32_MINVALUE


# lwf_graphic -------------------------------------------------------------

class Graphic(Object):
    m_displayList = None

    def __init__(self, lwf, parent, objId):
        super().__init__(lwf, parent, Format.Object.Type.GRAPHIC, objId)
        data = lwf.data.graphics[objId]
        n = data.graphicObjects
        self.m_displayList = [Object() for _ in range(0, n)]
        graphicObjects = lwf.data.graphicObjects
        for i in range(0, n):
            gobj = graphicObjects[data.graphicObjectId + i]
            obj = None
            graphicObjectId = gobj.graphicObjectId

            if graphicObjectId is -1:
                continue
            if gobj.graphicObjectType == Format.Object.Type.BITMAP.value:
                obj = Bitmap(lwf, parent, graphicObjectId)
            elif gobj.graphicObjectType == Format.Object.Type.BITMAPEX.value:
                obj = BitmapEx(lwf, parent, graphicObjectId)
            elif gobj.graphicObjectType == Format.Object.Type.TEXT.value:
                obj = Text(lwf, parent, graphicObjectId)

            obj.Exec()
            self.m_displayList[i] = obj

    @property
    def displayList(self):
        return self.m_displayList

    def Update(self, m, c):
        n = len(self.m_displayList)
        for i in range(0, n):
            self.m_displayList[i].Update(m, c)

    def Render(self, v, rOffset):
        if not v:
            return
        n = len(self.m_displayList)
        for i in range(0, n):
            self.m_displayList[i].Render(v, rOffset)

    def Destroy(self):
        n = len(self.m_displayList)
        for i in range(0, n):
            self.m_displayList[i].Destroy()
        self.m_displayList = None


# lwf_particle ------------------------------------------------------------

class Particle(Object):
    def __init__(self, lwf, parent, objId):
        super().__init__(lwf, parent, Format.Object.Type.PARTICLE, objId)
        self.m_dataMatrixId = lwf.data.particles[objId].matrixId
        self.m_renderer = lwf.rendererFactory.ConstructParticle(lwf, objId, self)

    def Update(self, m, c):
        super().Update(m, c)
        if self.m_renderer is not None:
            self.m_renderer.Update(self.m_matrix, self.m_colorTransform)


# lwf_programobject -------------------------------------------------------

class ProgramObject(Object):
    def __init__(self, lwf, parent, objId):
        super().__init__(lwf, parent, Format.Object.Type.PROGRAMOBJECT, objId)
        data = lwf.data.programObjects[objId]
        self.m_matrixId = data.matrixId
        ctor = lwf.GetProgramObjectConstructor(objId)
        if ctor is not None:
            self.m_renderer = ctor(self, objId, data.width, data.height)

    def Update(self, m, c):
        super().Update(m, c)
        if self.m_renderer is not None:
            self.m_renderer.Update(self.m_matrix, self.m_colorTransform)


# lwf_movie ---------------------------------------------------------------

class Movie(IObject):
    m_data = 0
    m_instanceHead = None
    m_instanceTail = None
    m_displayList: List[(Object or None)] = None
    m_eventHandlers = None
    m_handler = None
    m_calculateBoundsCallbacks = None
    m_attachedMovies = None
    m_attachedMovieList = None
    m_attachedMovieDescendingList = None
    m_detachedMovies = None
    m_attachedLWFs = None
    m_attachedLWFList = None
    m_attachedLWFDescendingList = None
    m_detachedLWFs = None
    m_texts = None
    m_bitmapClips = None
    m_bounds = None
    m_currentBounds = None
    m_attachName = None
    m_totalFrames = 0
    m_currentFrameInternal = 0
    m_currentFrameCurrent = 0
    m_execedFrame = 0
    m_animationPlayedFrame = 0
    m_depth = 0
    m_lastControlOffset = 0
    m_lastControls = 0
    m_lastControlAnimationOffset = 0
    m_movieExecCount = 0
    m_postExecCount = 0
    m_blendMode = 0
    m_active = 0
    m_visible = 0
    m_playing = 0
    m_jumped = 0
    m_overriding = 0
    m_hasButton = 0
    m_postLoaded = 0
    m_lastHasButton = 0
    m_skipped = 0
    m_attachMovieExeced = 0
    m_attachMoviePostExeced = 0
    m_needsUpdateAttachedLWFs = 0
    m_requestedCalculateBounds = 0
    m_matrix0 = None
    m_matrix1 = None
    m_matrixForAttachedLWFs = None
    m_colorTransform0 = None
    m_colorTransform1 = None
    m_colorTransformForAttachedLWFs = None
    m_currentLabelsCache = None
    m_currentLabelCache = None
    m_property = None

    def __init__(self, lwf, parent, objId, instId, matrixId=0, colorTransformId=0, attached=False, handler=None,
                 n=None):
        super().__init__(lwf, parent, Format.Object.Type.ATTACHEDMOVIE if attached else Format.Object.Type.MOVIE, objId, instId)
        self.m_data = lwf.data.movies[objId]
        self.m_matrixId = matrixId
        self.m_colorTransformId = colorTransformId
        self.m_totalFrames = self.m_data.frames
        if not (n is None or n is ""):
            self.m_name = n
        self.m_currentFrameInternal = -1
        self.m_execedFrame = -1
        self.m_animationPlayedFrame = -1
        self.m_lastControlOffset = -1
        self.m_lastControls = -1
        self.m_lastHasButton = False
        self.m_lastControlAnimationOffset = -1
        self.m_skipped = False
        self.m_postLoaded = False
        self.m_active = True
        self.m_visible = True
        self.m_playing = True
        self.m_jumped = False
        self.m_overriding = False
        self.m_attachMovieExeced = False
        self.m_attachMoviePostExeced = False
        self.m_movieExecCount = -1
        self.m_postExecCount = -1
        self.m_blendMode = int(Format.Constant.BLEND_MODE_NORMAL.value)
        self.m_requestedCalculateBounds = False
        self.m_calculateBoundsCallbacks = CalculateBoundsCallbacks()

        self.m_property = Property(lwf)

        self.m_matrix0 = Matrix()
        self.m_matrix1 = Matrix()
        self.m_matrixForAttachedLWFs = Matrix()
        self.m_colorTransform0 = ColorTransform()
        self.m_colorTransform1 = ColorTransform()
        self.m_colorTransformForAttachedLWFs = ColorTransform()

        self.m_displayList = [None for _ in range(self.m_data.depths)]

        self.m_eventHandlers = EventHandlers()
        self.m_handler = MovieEventHandlers()
        self.m_handler.Add(lwf.GetMovieEventHandlers(self))
        self.m_handler.Add(handler)

        self.PlayAnimation(Format.MovieClipEvent.ClipEvent.LOAD)
        if not self.m_handler.Empty():
            self.m_handler.Call(MovieEventHandlers.Type.LOAD, self)

        lwf.ExecMovieCommand()

    @property
    def data(self):
        return self.m_data

    @property
    def attachName(self):
        return self.m_attachName

    @attachName.setter
    def attachName(self, value):
        self.m_attachName = value

    @property
    def depth(self):
        return self.m_depth

    @depth.setter
    def depth(self, value):
        self.m_depth = value

    @property
    def blendMode(self):
        return self.m_blendMode

    @blendMode.setter
    def blendMode(self, value):
        self.m_blendMode = value

    @property
    def currentFrame(self):
        return self.m_currentFrameInternal + 1

    @property
    def totalFrames(self):
        return self.m_totalFrames

    @property
    def playing(self):
        return self.m_playing

    @property
    def visible(self):
        return self.m_visible

    @property
    def hasButton(self):
        return self.m_totalFrames

    def SetHandlers(self, handler):
        self.m_handler.Clear()
        self.m_handler.Add(handler)

    def GlobalToLocal(self, point):
        invert = Matrix()
        if self.m_property.hasMatrix:
            m = Matrix()
            m = Utility.CalcMatrix(m, self.m_matrix, self.m_property.matrix)
        else:
            m = self.m_matrix
        Utility.InvertMatrix(invert, m)
        px, py = Utility.CalcMatrixToPoint(point.x, point.y, invert)
        return Point(px, py)

    def LocalToGlobal(self, point):
        if self.m_property.hasMatrix:
            m = Matrix()
            m = Utility.CalcMatrix(m, self.m_matrix, self.m_property.matrix)
        else:
            m = self.m_matrix
        px, py = Utility.CalcMatrixToPoint(point.x, point.y, m)
        return Point(px, py)

    def ExecObject(self, dlDepth, objId, matrixId, colorTransformId, instId, dlBlendMode, updateBlendMode=False):
        print("Update Movie Object")
        if objId is -1:
            return
        data = self.m_lwf.data
        dataObject = data.objects[objId]
        dataObjectId = dataObject.objectId
        obj = self.m_displayList[dlDepth]
        if obj is not None and (obj.type != dataObject.objectType or obj.objectId != dataObjectId or (
                obj.IsMovie() and obj.instanceId != instId)):
            if self.m_texts is not None and obj.IsText():
                self.EraseText(obj.objectId)
            obj.Destroy()
            obj = None
        if obj is None:
            if dataObject.objectType == Format.Object.Type.BUTTON.value:
                obj = Button(self.m_lwf, self, dataObjectId, instId, matrixId, colorTransformId)
            elif dataObject.objectType == Format.Object.Type.GRAPHIC.value:
                obj = Graphic(self.m_lwf, self, dataObjectId)
            elif dataObject.objectType == Format.Object.Type.MOVIE.value:
                obj = Movie(self.m_lwf, self, dataObjectId, instId, matrixId, colorTransformId)
                obj.blendMode = dlBlendMode
            elif dataObject.objectType == Format.Object.Type.BITMAP.value:
                obj = Bitmap(self.m_lwf, self, dataObjectId)
            elif dataObject.objectType == Format.Object.Type.BITMAPEX.value:
                obj = BitmapEx(self.m_lwf, self, dataObjectId)
            elif dataObject.objectType == Format.Object.Type.TEXT.value:
                obj = Text(self.m_lwf, self, dataObjectId, instId)
            elif dataObject.objectType == Format.Object.Type.PARTICLE.value:
                obj = Particle(self.m_lwf, self, dataObjectId)
            elif dataObject.objectType == Format.Object.Type.PROGRAMOBJECT.value:
                obj = ProgramObject(self.m_lwf, self, dataObjectId)
        if obj.IsMovie() and updateBlendMode:
            obj.blendMode = dlBlendMode
        if obj.IsMovie() or obj.IsButton():
            instance = obj
            instance.linkInstance = None
            if self.m_instanceHead is None:
                self.m_instanceHead = instance
            else:
                self.m_instanceTail.linkInstance = instance
            self.m_instanceTail = instance
            if obj.IsButton():
                self.m_hasButton = True
        if self.m_texts is not None and obj.IsText():
            self.InsertText(obj.objectId)
        self.m_displayList[dlDepth] = obj
        obj.execCount = self.m_movieExecCount
        obj.Exec(matrixId, colorTransformId)

    def Override(self, overriding):
        self.m_overriding = overriding

    def Exec(self, matrixId=0, colorTransformId=0):
        print("Movie Update")
        self.m_attachMovieExeced = False
        self.m_attachMoviePostExeced = False
        super().Exec(matrixId, colorTransformId)

    def PostExec(self, progressing):
        print("Movie Post Exec")
        self.m_hasButton = False
        if not self.m_active:
            return

        self.m_execedFrame = -1
        postExeced = self.m_postExecCount == self.m_lwf.execCount
        if progressing and self.m_playing and not self.m_jumped and not postExeced:
            self.m_currentFrameInternal += 1
        while True:
            if self.m_currentFrameInternal < 0 or self.m_currentFrameInternal >= self.m_totalFrames:
                self.m_currentFrameInternal = 0
            if self.m_currentFrameInternal == self.m_execedFrame:
                break
            self.m_currentFrameCurrent = self.m_currentFrameInternal
            self.m_execedFrame = self.m_currentFrameCurrent
            data = self.m_lwf.data
            frame = data.frames[self.m_data.frameOffset + self.m_currentFrameCurrent]
            print("Got a frame?", frame.controls, frame.controlOffset)
            if self.m_lastControlOffset == frame.controlOffset and self.m_lastControls == frame.controls:
                controlAnimationOffset = self.m_lastControlAnimationOffset
                if self.m_skipped:
                    instance = self.m_instanceHead
                    while instance is not None:
                        if instance.IsMovie():
                            movie = instance
                            movie.m_attachMovieExeced = False
                            movie.m_attachMoviePostExeced = False
                        elif instance.IsButton():
                            instance.EnterFrame()
                        instance = instance.linkInstance
                    self.m_hasButton = self.m_lastHasButton
                else:
                    for dlDepth in range(0, self.m_data.depths):
                        obj = self.m_displayList[dlDepth]
                        if obj is not None:
                            if not postExeced:
                                obj.matrixIdChanged = False
                                obj.colorTransformIdChanged = False
                            if obj.IsMovie():
                                movie = obj
                                movie.m_attachMovieExeced = False
                                movie.m_attachMoviePostExeced = False
                            elif obj.IsButton():
                                obj: Button
                                obj.EnterFrame()
                                self.m_hasButton = True
                    self.m_lastHasButton = self.m_hasButton
                    self.m_skipped = True
            else:
                self.m_movieExecCount += 1
                self.m_instanceHead = None
                self.m_instanceTail = None
                self.m_lastControlOffset = frame.controlOffset
                self.m_lastControls = frame.controls
                controlAnimationOffset = -1
                for i in range(0, frame.controls):
                    control = data.controls[frame.controlOffset + i]
                    if control.controlType == Format.Control.Type.MOVE.value:
                        p = data.places[control.controlId]
                        self.ExecObject(p.depth, p.objectId, p.matrixId, 0, p.instanceId, p.blendMode)
                    elif control.controlType == Format.Control.Type.MOVEM.value:
                        ctrl = data.controlMoveMs[control.controlId]
                        p = data.places[ctrl.placeId]
                        self.ExecObject(p.depth, p.objectId, ctrl.matrixId, 0, p.instanceId, p.blendMode)
                    elif control.controlType == Format.Control.Type.MOVEC.value:
                        ctrl = data.controlMoveCs[control.controlId]
                        p = data.places[ctrl.placeId]
                        self.ExecObject(p.depth, p.objectId, ctrl.matrixId, ctrl.colorTransformId, p.instanceId,
                                        p.blendMode)
                    elif control.controlType == Format.Control.Type.MOVEMC.value:
                        ctrl = data.controlMoveMCs[control.controlId]
                        p = data.places[ctrl.placeId]
                        self.ExecObject(p.depth, p.objectId, ctrl.matrixId, ctrl.colorTransformId, p.instanceId,
                                        p.blendMode)
                    elif control.controlType == Format.Control.Type.MOVEMCB.value:
                        ctrl = data.controlMoveMCBs[control.controlId]
                        p = data.places[ctrl.placeId]
                        self.ExecObject(p.depth, p.objectId, ctrl.matrixId, ctrl.colorTransformId, p.instanceId,
                                        ctrl.blendMode, True)
                    elif control.controlType == Format.Control.Type.ANIMATION.value:
                        if controlAnimationOffset == -1:
                            controlAnimationOffset = i
                self.m_lastControlAnimationOffset = controlAnimationOffset
                self.m_lastHasButton = self.m_hasButton

                for dlDepth in range(0, self.m_data.depths):
                    obj = self.m_displayList[dlDepth]
                    if obj is not None and obj.execCount is not self.m_movieExecCount:
                        if self.m_texts is not None and obj.IsText():
                            self.EraseText(obj.objectId)
                        obj.Destroy()
                        self.m_displayList[dlDepth] = None
            self.m_attachMovieExeced = True
            if self.m_attachedMovies is not None:
                for movie in self.m_attachedMovieList.values():
                    if movie is not None:
                        movie.Exec()

            instance = self.m_instanceHead
            while instance is not None:
                if instance.IsMovie():
                    movie = instance
                    movie.PostExec(progressing)
                    if not self.m_hasButton and movie.m_hasButton:
                        self.m_hasButton = True
                instance = instance.linkInstance

            self.m_attachMoviePostExeced = True
            if self.m_attachedMovies is not None:
                for attachName, v in self.m_detachedMovies:
                    boolean, movie = self.m_attachedMovies.TryGetValue(attachName)
                    if boolean:
                        self.DeleteAttachedMovie(self, movie, True, False)
                self.m_detachedMovies.clear()
                for movie in self.m_attachedMovieList.values():
                    if movie is not None:
                        movie.PostExec(progressing)
                        if not self.m_hasButton and movie.m_hasButton:
                            self.m_hasButton = True
            if self.m_attachedLWFs is not None:
                self.m_hasButton = True
            if not self.m_postLoaded:
                self.m_postLoaded = True
                if not self.m_handler.Empty():
                    self.m_handler.Call(MovieEventHandlers.Type.POSTLOAD, self)
            if controlAnimationOffset is not -1 and self.m_execedFrame == self.m_currentFrameInternal:
                animationPlayed = self.m_animationPlayedFrame == self.m_currentFrameCurrent and not self.m_jumped
                if not animationPlayed:
                    for i in range(controlAnimationOffset, frame.controls):
                        control = data.controls[frame.controlOffset + i]
                        self.m_lwf.PlayAnimation(control.controlId, self)
            self.m_animationPlayedFrame = self.m_currentFrameCurrent
            if self.m_currentFrameCurrent == self.m_currentFrameInternal:
                self.m_jumped = False

        self.PlayAnimation(Format.MovieClipEvent.ClipEvent.ENTERFRAME)
        if not self.m_handler.Empty():
            self.m_handler.Call(MovieEventHandlers.Type.ENTERFRAME, self)
            self.m_postExecCount = self.m_lwf.execCount

    def ExecAttachedLWF(self, tick, currentProgress):
        hasButton = False
        instance = self.m_instanceHead
        while instance is not None:
            if instance.IsMovie():
                hasButton |= instance.ExecAttachedLWF(tick, currentProgress)
            instance = instance.linkInstance

        if self.m_attachedMovies is not None:
            for movie in self.m_attachedMovieList.values():
                if movie is not None:
                    hasButton |= movie.ExecAttachedLWF(tick, currentProgress)
        if self.m_attachedLWFs is not None:
            for attachName, v in self.m_detachedLWFs:
                boolean, lwfContainer = self.m_attachedLWFs.TryGetValue(attachName)
                if boolean:
                    self.DeleteAttachedLWF(self, lwfContainer, True, False)
            self.m_detachedLWFs.clear()
            for lwfContainer in self.m_attachedLWFList.values():
                child = lwfContainer.child
                if child.tick == self.m_lwf.tick:
                    child.progress = currentProgress
                self.m_lwf.RenderObject(child.ExecInternal(tick))
                hasButton |= child.rootMovie.hasButton
        return hasButton

    def UpdateObject(self, obj, m, c, matrixChanged, colorTransformChanged):
        if obj.IsMovie() and obj.m_property.hasMatrix:
            objm = m
        elif matrixChanged or not obj.updated or obj.matrixIdChanged:
            objm = Utility.CalcMatrix(self.m_lwf, self.m_matrix1, m, obj.matrixId)
        else:
            objm = None
        if obj.IsMovie() and obj.m_property.hasColorTransform():
            objc = c
        elif colorTransformChanged or not obj.updated or obj.colorTransformIdChanged:
            objc = Utility.CalcColorTransform(self.m_lwf, self.m_colorTransform1, c, obj.colorTransformId)
        else:
            objc = None
        obj.Update(objm, objc)

    def Update(self, m, c):
        if not self.m_active:
            return

        if self.m_overriding:
            matrixChanged = True
            colorTransformChanged = True
        else:
            matrixChanged = self.m_matrix.SetWithComparing(m)
            colorTransformChanged = self.m_colorTransform.SetWithComparing(c)

        if self.m_property.hasMatrix:
            matrixChanged = True
            m = Utility.CalcMatrix(self.m_matrix0, self.m_matrix, self.m_property.matrix)
        else:
            m = self.m_matrix

        if self.m_property.hasColorTransform:
            colorTransformChanged = True
            c = Utility.CalcColorTransform(self.m_colorTransform0, self.m_colorTransform,
                                           self.m_property.colorTransform)
        else:
            c = self.m_colorTransform

        if self.m_attachedLWFs is not None:
            self.m_needsUpdateAttachedLWFs = False
            self.m_needsUpdateAttachedLWFs |= self.m_matrixForAttachedLWFs.SetWithComparing(m)
            self.m_needsUpdateAttachedLWFs |= self.m_colorTransformForAttachedLWFs.SetWithComparing(c)

        for dlDepth in range(0, self.m_data.depths):
            obj = self.m_displayList[dlDepth]
            if obj is not None:
                self.UpdateObject(obj, m, c, matrixChanged, colorTransformChanged)

        if self.m_bitmapClips is not None:
            for bitmapClip in self.m_bitmapClips.values():
                if bitmapClip is not None:
                    bitmapClip.Update(m, c)

        if self.m_attachedMovies is not None:
            for movie in self.m_attachedMovieList.values():
                if movie is not None:
                    self.UpdateObject(movie, m, c, matrixChanged, colorTransformChanged)

    def PostUpdate(self):
        instance = self.m_instanceHead
        while instance is not None:
            if instance.IsMovie():
                instance.PostUpdate()
            instance = instance.linkInstance
        if self.m_attachedMovies is not None:
            for movie in self.m_attachedMovieList.values():
                if movie is not None:
                    movie.PostUpdate()

        if self.m_requestedCalculateBounds:
            self.m_currentBounds = Bounds(FLOAT_MAXVALUE, FLOAT_MINVALUE, FLOAT_MAXVALUE, FLOAT_MINVALUE)
            self.Inspect((lambda o, hy, d, r: self.CalculateBounds(o)), 0, 0, 0)
            if self.lwf.lwfproperty.hasMatrix:
                invert = Matrix()
                Utility.InvertMatrix(invert, self.lwf.lwfproperty.matrix)
                x, y = Utility.CalcMatrixToPoint(self.m_currentBounds.xMin, self.m_currentBounds.yMin, invert)
                self.m_currentBounds.xMin = x
                self.m_currentBounds.yMin = y
                x, y = Utility.CalcMatrixToPoint(self.m_currentBounds.xMax, self.m_currentBounds.yMax, invert)
                self.m_currentBounds.xMax = x
                self.m_currentBounds.yMax = y
            self.m_bounds = self.m_currentBounds
            self.m_currentBounds = None
            self.m_requestedCalculateBounds = False
            if len(self.m_calculateBoundsCallbacks) is not 0:
                for h in self.m_calculateBoundsCallbacks:
                    h(self)
                self.m_calculateBoundsCallbacks.clear()

        if not self.m_handler.Empty():
            self.m_handler.Call(MovieEventHandlers.Type.UPDATE, self)

    def UpdateAttachedLWF(self):
        instance = self.m_instanceHead
        while instance is not None:
            if instance.IsMovie():
                instance.UpdateAttachedLWF()
            instance = instance.linkInstance

        if self.m_attachedMovies is not None:
            for movie in self.m_attachedMovieList.values():
                if movie is not None:
                    movie.updateAttachedLWF()

        if self.m_attachedLWFs is not None:
            for lwfContainer in self.m_attachedLWFList.values():
                if lwfContainer is None:
                    continue
                child = lwfContainer.child
                needsUpdateAttachedLWFs = child.needsUpdate or self.m_needsUpdateAttachedLWFs
                if needsUpdateAttachedLWFs:
                    child.Update(self.m_matrixForAttachedLWFs, self.m_colorTransformForAttachedLWFs)
                if child.isLWFAttached:
                    child.rootMovie.UpdateAttachedLWF()
                if needsUpdateAttachedLWFs:
                    child.rootMovie.PostUpdate()

    def CalculateBounds(self, o):
        if o.type == Format.Object.Type.GRAPHIC.value:
            for obj in o.displayList:
                self.CalculateBounds(obj)
        elif o.type == Format.Object.Type.BITMAP.value or o.type == Format.Object.Type.BITMAPEX.value:
            tfId = -1
            if o.type == Format.Object.Type.BITMAP.value:
                if o.objectId < len(o.lwf.data.bitmaps):
                    tfId = o.lwf.data.bitmaps[o.objectId].textureFragmentId
            else:
                if o.objectId < len(o.lwf.data.bitmapExs):
                    tfId = o.lwf.data.bitmapExs[o.objectId].textureFragmentId
            if tfId >= 0:
                tf = o.lwf.data.textureFragments[tfId]
                self.UpdateBounds(o.matrix, tf.x, tf.x + tf.w, tf.y, tf.y + tf.h)
        elif o.type == Format.Object.Type.BUTTON.value:
            self.UpdateBounds(o.matrix, 0, o.width, 0, o.height)
        elif o.type == Format.Object.Type.TEXT.value:
            text = o.lwf.data.texts[o.objectId]
            self.UpdateBounds(o.matrix, 0, text.width, 0, text.height)
        elif o.type == Format.Object.Type.PROGRAMOBJECT.value:
            pobj = o.lwf.data.programObjects[o.objectId]
            self.UpdateBounds(o.matrix, 0, pobj.width, 0, pobj.height)

    def UpdateBounds(self, m, *args):
        if len(args) == 4:  # type 1
            self.UpdateBounds(m, args[0], args[2])  # xMin, yMin
            self.UpdateBounds(m, args[0], args[3])  # xMin, yMax
            self.UpdateBounds(m, args[1], args[2])  # xMax, yMin
            self.UpdateBounds(m, args[1], args[3])  # xMax, yMax
        elif len(args) == 2:  # type 2
            x, y = Utility.CalcMatrixToPoint(args[0], args[1], m)
            if x < self.m_currentBounds.xMin:
                self.m_currentBounds.xMin = x
            elif x > self.m_currentBounds.xMax:
                self.m_currentBounds.xMax = x
            if y < self.m_currentBounds.yMin:
                self.m_currentBounds.yMin = y
            elif y > self.m_currentBounds.yMax:
                self.m_currentBounds.yMax = y

    def LinkButton(self):
        if not self.m_visible or not self.m_active or not self.m_hasButton:
            return
        for dlDepth in range(0, self.m_data.depths):
            obj = self.m_displayList[dlDepth]
            if obj is not None:
                if obj.IsButton():
                    obj.LinkButton()
                elif obj.IsMovie():
                    if obj.m_hasButton:
                        obj.LinkButton()
        if self.m_attachedMovies is not None:
            for movie in self.m_attachedMovieList.values():
                if movie is not None and movie.m_hasButton:
                    movie.linkButton()

        if self.m_attachedLWFs is not None:
            for lwfContainer in self.m_attachedLWFList.values():
                if lwfContainer is not None:
                    lwfContainer.LinkButton()

    def Render(self, v, rOffset):
        print("render")
        if not self.m_visible or not self.m_active:
            v = False

        useBlendMode = False
        useMaskMode = False
        if self.m_blendMode is not int(Format.Constant.BLEND_MODE_NORMAL.value):
            if self.m_blendMode is int(Format.Constant.BLEND_MODE_ADD.value) \
                    or self.m_blendMode is int(Format.Constant.BLEND_MODE_MULTIPLY.value) \
                    or self.m_blendMode is int(Format.Constant.BLEND_MODE_SCREEN.value) \
                    or self.m_blendMode is int(Format.Constant.BLEND_MODE_SUBTRACT.value):
                self.m_lwf.BeginBlendMode(self.m_blendMode)
                useBlendMode = True
            elif self.m_blendMode is int(Format.Constant.BLEND_MODE_ERASE.value) \
                    or self.m_blendMode is int(Format.Constant.BLEND_MODE_LAYER.value) \
                    or self.m_blendMode is int(Format.Constant.BLEND_MODE_MASK.value):
                self.m_lwf.BeginMaskMode(self.m_blendMode)
                useMaskMode = True

        if v and not self.m_handler.Empty():
            self.m_handler.Call(MovieEventHandlers.Type.RENDER, self)

        if self.m_property.hasRenderingOffset:
            self.m_lwf.RenderOffset()
            rOffset = self.m_property.renderingOffset

        if rOffset is INT32_MINVALUE:
            self.m_lwf.ClearRenderOffset()

        for dlDepth in range(0, self.m_data.depths):
            obj = self.m_displayList[dlDepth]
            if obj is not None:
                print("Render Object")
                obj.Render(v, rOffset)

        if self.m_bitmapClips is not None:
            for bitmapClip in self.m_bitmapClips.values():
                if bitmapClip is not None:
                    bitmapClip.Render(v and bitmapClip.visible, rOffset)

        if self.m_attachedMovies is not None:
            for movie in self.m_attachedMovieList.values():
                if movie is not None:
                    movie.Render(v, rOffset)

        if self.m_attachedLWFs is not None:
            for lwfContainer in self.m_attachedMovieList.values():
                if lwfContainer is not None:
                    child = lwfContainer.child
                    child.SetAttachVisible(v)
                    self.m_lwf.RenderObject(child.Render(self.m_lwf.renderingIndex, self.m_lwf.renderingCount, rOffset))

        if useBlendMode:
            self.m_lwf.EndBlendMode()
        if useMaskMode:
            self.m_lwf.EndMaskMode()

    def Inspect(self, inspector, hierarchy, inspectDepth, rOffset):
        if self.m_property.hasRenderingOffset:
            self.m_lwf.RenderOffset()
            rOffset = self.m_property.renderingOffset
        if rOffset is INT32_MINVALUE:
            self.m_lwf.ClearRenderOffset()

        inspector(self, hierarchy, inspectDepth, rOffset)

        hierarchy += 1

        d = 0
        for d in range(0, self.m_data.depths):
            obj = self.m_displayList[d]
            if obj is not None:
                obj.Inspect(inspector, hierarchy, d, rOffset)
        if self.m_bitmapClips is not None:
            for bitmapClip in self.m_bitmapClips.values():
                if bitmapClip is not None:
                    bitmapClip.Inspect(inspector, hierarchy, d, rOffset)
                    d += 1
        if self.m_attachedMovies is not None:
            for movie in self.m_attachedMovieList.values():
                if movie is not None:
                    movie.Inspect(inspector, hierarchy, d, rOffset)
                    d += 1

        if self.m_attachedLWFs is not None:
            for lwfContainer in self.m_attachedLWFList.values():
                if lwfContainer is not None:
                    child = lwfContainer.child
                    self.m_lwf.RenderObject(child.Inspect(inspector, hierarchy, d, rOffset))
                    d += 1

    def Destroy(self):
        for dlDepth in range(0, self.m_data.depths):
            obj = self.m_displayList[dlDepth]
            if obj is not None:
                obj.Destroy()

        if self.m_bitmapClips is not None:
            for k, v in self.m_bitmapClips:
                if v is not None:
                    v.Destroy()
            self.m_bitmapClips = None

        if self.m_attachedMovies is not None:
            for k, v in self.m_attachedMovies:
                v.Destroy()
            self.m_attachedMovies = None
            self.m_detachedMovies = None
            self.m_attachedMovieList = None

        if self.m_attachedLWFs is not None:
            for k, v in self.m_attachedLWFs:
                if v.child.detachHandler is not None:
                    v.detachHandler(v.child)
            self.m_attachedLWFs = None
            self.m_detachedLWFs = None
            self.m_attachedLWFList = None

        self.PlayAnimation(Format.MovieClipEvent.ClipEvent.UNLOAD)
        if not self.m_handler.Empty():
            self.m_handler.Call(MovieEventHandlers.Type.UNLOAD, self)

        self.m_displayList = None
        self.m_property = None
        super().Destroy()

    def PlayAnimation(self, clipEvent):
        clipEvents = self.m_lwf.data.movieClipEvents
        for i in range(0, self.m_data.clipEvents):
            c = clipEvents[self.m_data.clipEventId + i]
            if (c.clipEvent & int(clipEvent)) != 0:
                self.m_lwf.PlayAnimation(c.animationId, self)

    def SearchFrame(self, arg):
        return self.m_lwf.SearchFrame(self, arg)

    def SearchMovieInstance(self, arg, recursive=True):
        if isinstance(arg, int):
            stringId = arg
            if stringId is -1:
                return None
            instance = self.m_instanceHead
            while instance is not None:
                if instance.IsMovie() and self.m_lwf.GetInstanceNameStringId(instance.instanceId) == stringId:
                    return instance
                elif recursive and instance.IsMovie():
                    i = instance.SearchMovieInstance(stringId, recursive)
                    if i is not None:
                        return i
                instance = instance.linkInstance
        else:
            instanceName = arg
            stringId = self.m_lwf.GetStringId(instanceName)
            if stringId is not -1:
                return self.SearchMovieInstance(stringId, recursive)

            if self.m_attachedMovies is not None:
                for movie in self.m_attachedMovieList.values():
                    if movie is not None:
                        if movie.attachName is instanceName:
                            return movie
                        elif recursive:
                            descendant = movie.SearchMovieInstance(instanceName, recursive)
                            if descendant is not None:
                                return descendant
            if self.m_attachedLWFs is not None:
                for lwfContainer in self.m_attachedLWFList.values():
                    if lwfContainer is not None:
                        child = lwfContainer.child
                        if child.attachName == instanceName:
                            return child.rootMovie
                        elif recursive:
                            descendant = child.rootMovie.SearchMovieInstance(instanceName, recursive)
                            if descendant is not None:
                                return descendant
        return None

    def __getitem__(self, instanceName):
        return self.SearchMovieInstance(instanceName, False)

    def SearchMovieInstanceByInstanceId(self, instId, recursive):
        instance = self.m_instanceHead
        while instance is not None:
            if instance.IsMovie() and instance.instanceId == instId:
                return instance
            elif recursive and instance.IsMovie():
                i = instance.SearchMovieInstanceByInstanceId(instId, recursive)
                if i is not None:
                    return i
            instance = instance.linkInstance
        return None

    def SearchButtonInstance(self, arg, recursive=True):
        if isinstance(arg, int):
            stringId = arg
            if stringId is -1:
                return None
            instance = self.m_instanceHead
            while instance is not None:
                if instance.IsButton() and self.m_lwf.GetInstanceNameStringId(instance.instanceId) == stringId:
                    return instance
                elif recursive and instance.IsMovie():
                    i = instance.SearchButtonInstance(stringId, recursive)
                    if i is not None:
                        return i
                instance = instance.linkInstance
        else:
            instanceName = arg
            stringId = self.m_lwf.GetStringId(instanceName)
            if stringId is not -1:
                return self.SearchButtonInstance(stringId, recursive)

            if self.m_attachedMovies is not None and recursive:
                for movie in self.m_attachedMovieList.values():
                    if movie is not None:
                        button = movie.SearchButtonInstance(instanceName, recursive)
                        if button is not None:
                            return button
            if self.m_attachedLWFs is not None:
                for lwfContainer in self.m_attachedLWFList.values():
                    if lwfContainer is not None:
                        child = lwfContainer.child
                        button = child.rootMovie.SearchButtonInstance(instanceName, recursive)
                        if button is not None:
                            return button
        return None

    def SearchButtonInstanceByInstanceId(self, instId, recursive):
        instance = self.m_instanceHead
        while instance is not None:
            if instance.IsButton() and instance.instanceId == instId:
                return instance
            elif recursive and instance.IsMovie():
                i = instance.SearchButtonInstanceByInstanceId(instId, recursive)
                if i is not None:
                    return i
            instance = instance.linkInstance
        return None

    def InsertText(self, objId):
        text = self.lwf.data.texts[objId]
        if text.nameStringId is not -1:
            self.m_texts[self.lwf.data.srings[text.nameStringId]] = True

    def EraseText(self, objId):
        text = self.lwf.data.texts[objId]
        if text.nameStringId is not -1:
            self.m_texts.remove(self.lwf.data.strings[text.nameStringId])

    def SearchText(self, textName):
        if self.m_texts is not None:
            self.m_texts = Texts()
            for dlDepth in range(0, self.data.depths):
                obj = self.m_displayList[dlDepth]
                if obj is not None and obj.IsText():
                    self.InsertText(obj.objectId)

        boolean, v = self.m_texts.TryGetValue(textName)
        if boolean:
            return True
        return False

    def AddEventHandler(self, eventName, handler):
        if isinstance(handler, MovieEventHandler):
            eventId = self.m_lwf.GetEventOffset()
            if eventName is "load":
                self.m_handler.Add(eventId, load=handler)
                return eventId
            elif eventName is "postLoad":
                self.m_handler.Add(eventId, p=handler)
                return eventId
            elif eventName is "unload":
                self.m_handler.Add(eventId, u=handler)
                return eventId
            elif eventName is "enterFrame":
                self.m_handler.Add(eventId, e=handler)
                return eventId
            elif eventName is "update":
                self.m_handler.Add(eventId, up=handler)
                return eventId
            elif eventName is "render":
                self.m_handler.Add(eventId, r=handler)
                return eventId
            else:
                return -1
        else:
            eventId = self.m_lwf.GetEventOffset()
            boolean, dictionary = self.m_eventHandlers.TryGetValue(eventName)
            if not boolean:
                dictionary = EventHandlerDictionary()
                self.m_eventHandlers[eventName] = dictionary
            dictionary.Add(eventId, handler)
            return eventId

    def RemoveEventHandler(self, eventName, buttonId):
        if eventName is "load" or \
                eventName is "postLoad" or \
                eventName is "unload" or \
                eventName is "enterFrame" or \
                eventName is "update" or \
                eventName is "render":
            self.m_handler.Remove(buttonId)
        else:
            boolean, dictionary = self.m_eventHandlers.TryGetValue(eventName)
            if boolean:
                dictionary.Remove(buttonId)

    def ClearEventHandler(self, eventName):
        if eventName is "load":
            self.m_handler.Clear(MovieEventHandlers.Type.LOAD)
        elif eventName is "postLoad":
            self.m_handler.Clear(MovieEventHandlers.Type.POSTLOAD)
        elif eventName is "unload":
            self.m_handler.Clear(MovieEventHandlers.Type.UNLOAD)
        elif eventName is "enterframe":
            self.m_handler.Clear(MovieEventHandlers.Type.ENTERFRAME)
        elif eventName is "update":
            self.m_handler.Clear(MovieEventHandlers.Type.UPDATE)
        elif eventName is "render":
            self.m_handler.Clear(MovieEventHandlers.Type.RENDER)
        else:
            self.m_eventHandlers.remove(eventName)

    def SetEventHandler(self, eventName, eventHandler):
        self.ClearEventHandler(eventName)
        return self.AddEventHandler(eventName, eventHandler)

    def DispatchEvent(self, eventName):
        if eventName is "load":
            self.m_handler.Call(MovieEventHandlers.Type.LOAD, self)
        elif eventName is "postLoad":
            self.m_handler.Call(MovieEventHandlers.Type.POSTLOAD, self)
        elif eventName is "unload":
            self.m_handler.Call(MovieEventHandlers.Type.UNLOAD, self)
        elif eventName is "enterframe":
            self.m_handler.Call(MovieEventHandlers.Type.ENTERFRAME, self)
        elif eventName is "update":
            self.m_handler.Call(MovieEventHandlers.Type.UPDATE, self)
        elif eventName is "render":
            self.m_handler.Call(MovieEventHandlers.Type.RENDER, self)
        else:
            boolean, dictionary = self.m_eventHandlers.TryGetValue(eventName)
            if boolean:
                dictionary = EventHandlerDictionary(dictionary)
                for k, v in dictionary.items():
                    v()

    def RequestCalculateBounds(self, callback=None):
        self.m_requestedCalculateBounds = True
        self.m_calculateBoundsCallbacks.append(callback)
        self.m_bounds = None
        return

    def GetBounds(self):
        return self.m_bounds

    def CacheCurrentLabels(self):
        if self.m_currentLabelsCache is not None:
            return
        self.m_currentLabelsCache = CurrentLabels()
        labels = self.m_lwf.GetMovieLabels(self)
        if labels is None:
            return

        for k, v in labels:
            labelData = LabelData()
            labelData.frame = v + 1
            labelData.name = self.m_lwf.data.strings[k]
            self.m_currentLabelsCache.append(labelData)

        def anon(a, b):
            return a.frame - b.frame

        self.m_currentLabelsCache.Sort(anon)

    def GetCurrentLabel(self):
        self.CacheCurrentLabels()

        if len(self.m_currentLabelsCache) == 0:
            return None

        currentFrameTmp = self.currentFrame
        if currentFrameTmp < 1:
            currentFrameTmp = 1

        if self.m_currentLabelCache is None:
            self.m_currentLabelCache = CurrentLabelCache()

        boolean, labelName = self.m_currentLabelCache.TryGetValue(currentFrameTmp)
        if not boolean:
            firstLabel = self.m_currentLabelsCache[0]
            lastLabel = self.m_currentLabelsCache[len(self.m_currentLabelsCache) - 1]
            if currentFrameTmp < firstLabel.frame:
                labelName = ""
            elif currentFrameTmp == firstLabel.frame:
                labelName = firstLabel.name
            elif currentFrameTmp >= lastLabel.frame:
                labelName = lastLabel.name
            else:
                left = 0
                ln = self.m_currentLabelsCache[left].frame
                r = len(self.m_currentLabelsCache) - 1
                rn = self.m_currentLabelsCache[r].frame
                while True:
                    if (left == r) or (r - left == 1):
                        if currentFrameTmp < ln:
                            labelName = ""
                        elif currentFrameTmp == rn:
                            labelName = self.m_currentLabelsCache[r].name
                        else:
                            labelName = self.m_currentLabelsCache[left].name
                        break
                    n = int(math.floor((r - left) / 2.0) + left)
                    nn = self.m_currentLabelsCache[n].frame
                    if currentFrameTmp < nn:
                        r = n
                        rn = nn
                    elif currentFrameTmp > nn:
                        left = n
                        ln = nn
                    else:
                        labelName = self.m_currentLabelsCache[n].name
                        break
        return None if (labelName is "" or labelName is None) else labelName

    def GetCurrentLabels(self):
        self.CacheCurrentLabels()
        return self.m_currentLabelsCache

    # lwf_movieprop -----------------------------------------------------------

    @property
    def x(self):
        if self.m_property.hasMatrix:
            return self.m_property.matrix.translateX
        else:
            return Utility.GetX(self)

    @x.setter
    def x(self, value):
        if not self.m_property.hasMatrix:
            Utility.SyncMatrix(self)
        self.m_property.MoveTo(value, self.m_property.matrix.translateY)

    @property
    def y(self):
        if self.m_property.hasMatrix:
            return self.m_property.matrix.translateY
        else:
            return Utility.GetY(self)

    @y.setter
    def y(self, value):
        if not self.m_property.hasMatrix:
            Utility.SyncMatrix(self)
        self.m_property.MoveTo(self.m_property.matrix.translateX, value)

    @property
    def scaleX(self):
        if self.m_property.hasMatrix:
            return self.m_property.m_scaleX
        else:
            return Utility.GetScaleX(self)

    @scaleX.setter
    def scaleX(self, value):
        if not self.m_property.hasMatrix:
            Utility.SyncMatrix(self)
        self.m_property.ScaleTo(value, self.m_property.m_scaleY)

    @property
    def scaleY(self):
        if self.m_property.hasMatrix:
            return self.m_property.m_scaleY
        else:
            return Utility.GetScaleY(self)

    @scaleY.setter
    def scaleY(self, value):
        if not self.m_property.hasMatrix:
            Utility.SyncMatrix(self)
        self.m_property.ScaleTo(self.m_property.m_scaleX, value)

    @property
    def rotation(self):
        if self.m_property.hasMatrix:
            return self.m_property.m_rotation
        else:
            return Utility.GetRotation(self)

    @rotation.setter
    def rotation(self, value):
        if not self.m_property.hasMatrix:
            Utility.SyncMatrix(self)
        self.m_property.RotateTo(value)

    @property
    def alpha(self):
        if self.m_property.hasColorTransform:
            return self.m_property.colorTransform.multi.alpha
        else:
            return Utility.GetAlpha(self)

    @alpha.setter
    def alpha(self, value):
        if not self.m_property.hasColorTransform:
            Utility.SyncColorTransform(self)
        self.m_property.SetAlpha(value)

    @property
    def red(self):
        if self.m_property.hasColorTransform:
            return self.m_property.colorTransform.multi.red
        else:
            return Utility.GetRed(self)

    @red.setter
    def red(self, value):
        if not self.m_property.hasColorTransform:
            Utility.SyncColorTransform(self)
        self.m_property.SetAlpha(value)

    @property
    def green(self):
        if self.m_property.hasColorTransform:
            return self.m_property.colorTransform.multi.green
        else:
            return Utility.GetGreen(self)

    @green.setter
    def green(self, value):
        if not self.m_property.hasColorTransform:
            Utility.SyncColorTransform(self)
        self.m_property.SetAlpha(value)

    @property
    def blue(self):
        if self.m_property.hasColorTransform:
            return self.m_property.colorTransform.multi.blue
        else:
            return Utility.GetBlue(self)

    @blue.setter
    def blue(self, value):
        if not self.m_property.hasColorTransform:
            Utility.SyncColorTransform(self)
        self.m_property.SetAlpha(value)

    # lwf_movieop -------------------------------------------------------------

    def Play(self):
        self.m_playing = True
        return self

    def Stop(self):
        self.m_playing = False
        return self

    def NextFrame(self):
        self.m_jumped = True
        self.Stop()
        self.m_currentFrameInternal += 1
        return self

    def PrevFrame(self):
        self.m_jumped = True
        self.Stop()
        self.m_currentFrameInternal -= 1
        return self

    def GotoFrame(self, frameNo):
        self.GotoFrameInternal(frameNo - 1)
        return self

    def GotoFrameInternal(self, frameNo):
        self.m_jumped = True
        self.Stop()
        self.m_currentFrameInternal = frameNo
        return self

    def SetVisible(self, visible):
        self.m_visible = visible
        self.m_lwf.SetPropertyDirty()
        return self

    def GotoLabel(self, arg):
        if isinstance(arg, int):
            self.GotoFrame(self.m_lwf.SearchFrame(self, arg))
        else:
            self.GotoLabel(self.m_lwf.GetStringId(arg))
        return self

    def GotoAndStop(self, arg):
        if isinstance(arg, int):
            self.GotoFrame(arg)
        else:
            self.GotoFrame(self.m_lwf.SearchFrame(self, self.m_lwf.GetStringId(arg)))
        self.Stop()
        return self

    def GotoAndPlay(self, arg):
        if isinstance(arg, int):
            self.GotoFrame(arg)
        else:
            self.GotoFrame(self.m_lwf.SearchFrame(self, self.m_lwf.GetStringId(arg)))
        self.Play()
        return self

    def Move(self, vx, vy):
        if not self.m_property.hasMatrix:
            Utility.SyncMatrix(self)
        self.m_property.Move(vx, vy)
        return self

    def MoveTo(self, vx, vy):
        if not self.m_property.hasMatrix:
            Utility.SyncMatrix(self)
        self.m_property.MoveTo(vx, vy)
        return self

    def Rotate(self, degree):
        if not self.m_property.hasMatrix:
            Utility.SyncMatrix(self)
        self.m_property.Rotate(degree)
        return self

    def RotateTo(self, degree):
        if not self.m_property.hasMatrix:
            Utility.SyncMatrix(self)
        self.m_property.RotateTo(degree)
        return self

    def Scale(self, vx, vy):
        if not self.m_property.hasMatrix:
            Utility.SyncMatrix(self)
        self.m_property.Scale(vx, vy)
        return self

    def ScaleTo(self, vx, vy):
        if not self.m_property.hasMatrix:
            Utility.SyncMatrix(self)
        self.m_property.ScaleTo(vx, vy)
        return self

    def SetMatrix(self, m, sx=1, sy=1, r=0):
        self.m_property.SetMatrix(m, sx, sy, r)
        return self

    def SetAlpha(self, v):
        if not self.m_property.hasColorTransform:
            Utility.SyncColorTransform(self)
        self.m_property.SetAlpha(v)
        return self

    def SetColorTransform(self, c):
        self.m_property.SetColorTransform(c)
        return self

    def SetRenderingOffset(self, rOffset):
        self.m_property.SetRenderingOffset(rOffset)
        return self

    # lwf_movieat -------------------------------------------------------------

    def ReorderAttachedMovieList(self, reorder, index, movie):
        self.m_attachedMovieList = AttachedMovieList(self.m_attachedMovieList)
        self.m_attachedMovieList[index] = movie
        self.m_attachedMovieDescendingList[index] = index
        if reorder:
            mlist = self.m_attachedMovieList
            self.m_attachedMovieList = AttachedMovieList()
            self.m_attachedMovieDescendingList = AttachedMovieDescendingList()
            i = 0
            for m in mlist.values():
                m.depth = i
                self.m_attachedMovieList[i] = m
                self.m_attachedMovieDescendingList[i] = i
                i += 1

    @staticmethod
    def DeleteAttachedMovie(parent, movie, destroy=True, deleteFromDetachedMovies=True):
        attachName = movie.attachName
        attachDepth = movie.depth
        parent.m_attachedMovies.remove(attachName)
        parent.m_attachedMovieList.remove(attachDepth)
        parent.m_attachedMovieDescendingList.remove(attachDepth)
        if deleteFromDetachedMovies:
            parent.m_detachedMovies.remove(attachName)
        if destroy:
            movie.Destroy()

    def AttachMovieInternal(self, movie, attachName, attachDepth=-1, reorder=False):
        if self.m_attachedMovies is None:
            self.m_attachedMovies = AttachedMovies()
            self.m_detachedMovies = DetachDict()
            self.m_attachedMovieList = AttachedMovieList()
            self.m_attachedMovieDescendingList = AttachedMovieDescendingList()

        boolean, attachedMovie = self.m_attachedMovies.TryGetValue(attachName)
        if boolean:
            self.DeleteAttachedMovie(self, attachedMovie)

        if not reorder and attachDepth >= 0:
            boolean, attachedMovie = self.m_attachedMovieList.TryGetValue(attachDepth)
            if boolean:
                self.DeleteAttachedMovie(self, attachedMovie)

        movie.m_attachName = attachName
        if attachDepth >= 0:
            movie.depth = attachDepth
        else:
            e = iter(self.m_attachedMovieDescendingList)
            if next(e):
                e: SortedDictionary
                movie.depth = e.current() + 1
            else:
                movie.depth = 0
        self.m_attachedMovies[attachName] = movie
        self.ReorderAttachedMovieList(reorder, movie.depth, movie)

        return movie

    def AttachMovie(self, arg, attachName, attachDepth=-1, reorder=False,
                    load=None, postLoad=None, unload=None, enterFrame=None, update=None, render=None):
        if not isinstance(arg, Movie):
            linkageName = arg
            movieId = self.m_lwf.SearchMovieLinkage(self.m_lwf.GetStringId(linkageName))
            if movieId is -1:
                return None

            handlers = MovieEventHandlers()
            handlers.Add(self.m_lwf.GetEventOffset(), load, postLoad, unload, enterFrame, update, render)
            movie = Movie(self.m_lwf, self, movieId, -1, 0, 0, True, handlers, attachName)
            if self.m_attachMovieExeced:
                movie.Exec()
            if self.m_attachMoviePostExeced:
                movie.PostExec(True)

            return self.AttachMovieInternal(movie, attachName, attachDepth, reorder)
        else:
            movie = arg
            self.DeleteAttachedMovie(movie.parent, movie, False)
            handlers = MovieEventHandlers()
            handlers.Add(self.m_lwf.GetEventOffset(), load, postLoad, unload, enterFrame, update, render)
            movie.SetHandlers(handlers)

            movie.m_name = attachName
            return self.AttachMovieInternal(movie, attachName, attachDepth, reorder)

    def AttachEmptyMovie(self, attachName, attachDepth=-1, reorder=False, load=None, postLoad=None, unload=None,
                         enterFrame=None, update=None, render=None):
        return self.AttachMovie("_empty", attachName, attachDepth, reorder, load, postLoad, unload, enterFrame, update,
                                render)

    def SwapAttachedMovieDepth(self, depth0, depth1):
        if self.m_attachedMovies is None:
            return

        boolean, attachedMovie0 = self.m_attachedMovieList.TryGetValue(depth0)
        boolean, attachedMovie1 = self.m_attachedMovieList.TryGetValue(depth1)

        if attachedMovie0 is not None:
            attachedMovie0.depth = depth1

        if attachedMovie1 is not None:
            attachedMovie1.depth = depth0
        self.m_attachedMovieList[depth0] = attachedMovie1
        self.m_attachedMovieList[depth1] = attachedMovie0

    def GetAttachedMovie(self, arg):
        if self.m_attachedMovies is not None:
            boolean, movie = self.m_attachedMovieList.TryGetValue(arg)
            if boolean:
                return movie

    def SearchAttachedMovie(self, attachName, recursive=True):
        movie = self.GetAttachedMovie(attachName)
        if movie is not None:
            return movie

        if not recursive:
            return None

        instance = self.m_instanceHead
        while instance is not None:
            if instance.IsMovie():
                i = instance.SearchAttachedMovie(attachName, recursive)
                if i is not None:
                    return i
            instance = instance.linkInstance
        return None

    def DetachMovie(self, arg):
        if isinstance(arg, int):
            if self.m_detachedMovies is not None:
                boolean, movie = self.m_attachedMovieList.TryGetValue(arg)
                if boolean:
                    self.m_detachedMovies[movie.attachName] = True
        elif isinstance(arg, Movie):
            if self.m_detachedMovies is not None and arg is not None and arg.attachName is not None:
                self.m_detachedMovies[arg.attachName] = True
        else:
            if self.m_detachedMovies is not None:
                self.m_detachedMovies[arg] = True

    def DetachFromParent(self):
        if self.m_type != Format.Object.Type.ATTACHEDMOVIE.value:
            return

        self.m_active = False
        if self.m_parent is not None:
            self.m_parent.DetachMovie(self)

    def ReorderAttachedLWFLList(self, reorder, index, lwfContainer):
        self.m_attachedLWFList = AttachedLWFList(self.m_attachedLWFList)
        self.m_attachedLWFList[index] = lwfContainer
        self.m_attachedLWFDescendingList[index] = index
        if reorder:
            llist = self.m_attachedLWFList
            self.m_attachedLWFList = AttachedLWFList()
            self.m_attachedLWFDescendingList = AttachedLWFDescendingList()
            i = 0
            for l in llist.values():
                l.child.depth = i
                self.m_attachedLWFList[i] = l
                self.m_attachedLWFDescendingList[i] = i
                i += 1

    @staticmethod
    def DeleteAttachedLWF(parent, lwfContainer, destroy=True, deleteFromDetachedLWFs=True):
        attachName = lwfContainer.child.attachName
        attachDepth = lwfContainer.child.depth
        parent.m_attachedLWFs.remove(attachName)
        parent.m_attachedLWFList.remove(attachDepth)
        parent.m_attachedLWFDescendingList.remove(attachDepth)
        if deleteFromDetachedLWFs:
            parent.m_detachedLWFs.remove(attachName)
        if destroy:
            if lwfContainer.child.detachHandler is not None:
                lwfContainer.child.detachHandler(lwfContainer.child)
                lwfContainer.child.parent = None
                lwfContainer.detachHandler = None
                lwfContainer.child.attachName = None
                lwfContainer.child.depth = -1
            else:
                lwfContainer.child.Destroy()
            lwfContainer.Destroy()

    def AttachLWF(self, arg0, attachName, attachDepth=-1, reorder=False, arg1=None):
        if not isinstance(arg0, LWF):
            path = arg0
            texturePrefix = arg1
            if self.m_lwf.lwfLoader is None:
                return None

            child = self.m_lwf.lwfLoader(path, texturePrefix)
            if child is None:
                return None

            self.AttachLWF(child, attachName, attachDepth, reorder, lambda l: l.Destroy())
            return child
        else:
            child = arg0
            detachHandler = arg1

            if self.m_attachedLWFs is None:
                self.m_attachedLWFs = AttachedLWFs()
                self.m_detachedLWFs = DetachDict()
                self.m_attachedLWFList = AttachedLWFList()
                self.m_attachedLWFDescendingList = AttachedMovieDescendingList()

            if child.parent is not None:
                boolean, lwfContainer = child.parent.m_attachedLwfs.TryGetValue(child.attachName)
                self.DeleteAttachedLWF(child.parent, lwfContainer, False)
            boolean, lwfContainer = self.m_attachedLWFs.TryGetValue(attachName)
            if boolean:
                self.DeleteAttachedLWF(self, lwfContainer)

            if not reorder and attachDepth >= 0:
                boolean, lwfContainer = self.m_attachedLWFList.TryGetValue(attachDepth)
                if boolean:
                    self.DeleteAttachedLWF(self, lwfContainer)

            lwfContainer = LWFContainer(self, child)

            if child.interactive is True:
                self.m_lwf.SetInteractive()
            child.parent = self
            child.SetRoot(self.m_lwf.__root)
            child.detachHandler = detachHandler
            child.attachname = attachName
            if attachDepth >= 0:
                child.depth = attachDepth
            else:
                e = iter(self.m_attachedLWFDescendingList)
                if next(e):
                    e: SortedDictionary
                    child.depth = e.current() + 1
                else:
                    child.depth = 0
            self.m_attachedLWFs[attachName] = lwfContainer
            self.ReorderAttachedLWFLList(reorder, child.depth, lwfContainer)

            self.m_lwf.SetLWFAttached()

            return

    def SwapAttachedLWFDepth(self, depth0, depth1):
        if self.m_attachedLWFs is None:
            return

        boolean, attachedLWF0 = self.m_attachedLWFList.TryGetValue(depth0)
        boolean, attachedLWF1 = self.m_attachedLWFList.TryGetValue(depth1)
        if attachedLWF0 is not None:
            attachedLWF0.child.depth = depth1
        if attachedLWF1 is not None:
            attachedLWF1.child.depth = depth0
        self.m_attachedLWFList[depth0] = attachedLWF1
        self.m_attachedLWFList[depth1] = attachedLWF0

    def GetAttachedLWF(self, arg):
        if self.m_attachedLWFs is not None:
            boolean, lwfContainer = self.m_attachedLWFList.TryGetValue(arg)
            if boolean:
                return lwfContainer.child
        return None

    def SearchAttachedLWF(self, attachName, recursive=True):
        attachedLWF = self.GetAttachedLWF(attachName)
        if attachedLWF is not None:
            return attachedLWF

        if not recursive:
            return None

        instance = self.m_instanceHead
        while instance is not None:
            if instance.IsMovie():
                i = instance.SearchAttachedLWF(attachName, recursive)
                if i is not None:
                    return i
            instance = instance.linkInstance
        return None

    def DetachLWF(self, arg):
        if isinstance(arg, int):
            if self.m_detachedLWFs is not None:
                boolean, lwfContainer = self.m_attachedLWFList.TryGetValue(arg)
                if boolean:
                    self.m_detachedLWFs[lwfContainer.child.attachName] = True
        elif isinstance(arg, LWF):
            if self.m_detachedLWFs is not None and arg is not None and arg.attachName is not None:
                self.m_detachedLWFs[arg.attachName] = True
        else:
            if self.m_detachedLWFs is not None:
                self.m_detachedLWFs[arg] = True

    def DetachAllLWFs(self):
        if self.m_detachedLWFs is not None:
            for lwfContainer in self.m_attachedLWFs.values():
                self.m_detachedLWFs[lwfContainer.child.attachName] = True

    def RemoveMovieClup(self):
        if self.m_type == Format.Object.Type.ATTACHEDMOVIE.value:
            self.DetachFromParent()
        elif self.m_lwf.attachName is not None and self.m_lwf.parent is not None:
            self.m_lwf.parent.DetachLWF(self.m_lwf.attachName)

    def AttachBitmap(self, linkageName, depth):
        boolean, bitmapId = self.m_lwf.data.bitmapMap.TryGetValue(linkageName)
        if not boolean:
            return None
        bitmap = BitmapClip(self.m_lwf, self, bitmapId)
        if self.m_bitmapClips is not None:
            self.DetachBitmap(depth)
        else:
            self.m_bitmapClips = BitmapClips()
        self.m_bitmapClips[depth] = bitmap
        bitmap.depth = depth
        bitmap.name = linkageName
        return bitmap

    def GetAttachedBitMaps(self):
        return self.m_bitmapClips

    def GetAttachedBitmap(self, depth):
        if self.m_bitmapClips is None:
            return None
        boolean, bitmap = self.m_bitmapClips.TryGetValue(depth)
        return bitmap

    def SwapAttachedBitmapDepth(self, depth0, depth1):
        if self.m_bitmapClips is None:
            return

        boolean, bitmapClip0 = self.m_bitmapClips.TryGetValue(depth0)
        boolean, bitmapClip1 = self.m_bitmapClips.TryGetValue(depth1)
        if bitmapClip0 is not None:
            bitmapClip0.depth = depth1
            self.m_bitmapClips[depth1] = bitmapClip0
        else:
            self.m_bitmapClips.remove(depth1)
        if bitmapClip1 is not None:
            bitmapClip1.depth = depth0
            self.m_bitmapClips[depth0] = bitmapClip1
        else:
            self.m_bitmapClips.remove(depth0)

    def DetachBitmap(self, depth):
        if self.m_bitmapClips is None:
            return
        boolean, bitmapClip = self.m_bitmapClips.TryGetValue(depth)
        if not boolean:
            return
        bitmapClip.Destroy()
        self.m_bitmapClips.remove(depth)


# lwf_core ----------------------------------------------------------------

class MovieCommand(Action):
    pass


class MovieCommands(Dictionary):
    pass


class DetachHandler(Action):
    pass


class Inspector(Action):
    pass


class AllowButtonList(Dictionary):
    pass


class DenyButtonList(Dictionary):
    pass


class ExecHandler(Action):
    pass


class ExecHandlerList(List):
    pass


class TextDictionary(Dictionary):
    pass


class BlendModes(List):
    pass


class MaskModes(List):
    pass


class ProgramObjectConstructor(Action):
    pass


# ------------------------  lwf_coreop ------------------------------------

class HandlerWrapper:
    id = 0


# -----------------------  lwf_text  -------------------------------------

class Text(Object):
    m_name = None

    def __init__(self, lwf, p, objId, instId=-1):
        super().__init__(lwf, p, Format.Object.Type.TEXT, objId)
        text = lwf.data.texts[objId]
        self.m_dataMatrixId = text.matrixId

        if text.nameStringId is not -1:
            self.m_name = lwf.data.strings[text.nameStringId]
        else:
            if 0 <= instId < len(lwf.data.instanceNames):
                stringId = lwf.GetInstanceNameStringId(instId)
                if stringId is not -1:
                    self.m_name = lwf.data.strings[stringId]

        textRenderer = lwf.rendererFactory.ConstructText(lwf, objId, self)
        t = None
        if text.stringId is not -1:
            t = lwf.data.strings[text.stringId]

        if text.nameStringId is -1 and (self.name is None or self.name is ""):
            if text.stringId is not -1:
                textRenderer.SetText(t)
        else:
            lwf.SetTextRenderer(p.GetFullName(), self.name, t, textRenderer)

        self.m_renderer = textRenderer

    @property
    def name(self):
        return self.m_name


# -----------------------   lwf_bitmap -----------------------------------

class Bitmap(Object):
    def __init__(self, lwf, parent, objId):
        super().__init__(lwf, parent, Format.Object.Type.BITMAP, objId)
        self.m_dataMatrixId = lwf.data.bitmaps[objId].matrixId
        self.m_renderer = lwf.rendererFactory.ConstructBitmap(lwf, objId, self)


# -----------------------   lwf_bitmapex ---------------------------------

class BitmapEx(Object):
    def __init__(self, lwf, parent, objId):
        super().__init__(lwf, parent, Format.Object.Type.BITMAPEX, objId)
        self.m_dataMatrixId = lwf.data.bitmapExs[objId].matrixId
        self.m_renderer = lwf.rendererFactory.ConstructBitmapEx(lwf, objId, self)


# -----------------------   lwf_bitmapclip -------------------------------

class BitmapClip(Bitmap):
    depth = 0
    visible = False
    name = None
    width = 0.0
    height = 0.0
    regX = 0.0
    regY = 0.0
    x = 0.0
    y = 0.0
    scaleX = 0.0
    scaleY = 0.0
    rotation = 0.0
    alpha = 0.0
    offsetX = 0.0
    offsetY = 0.0
    originalWidth = 0.0
    originalHeight = 0.0

    _scaleX = 0.0
    _scaleY = 0.0
    _rotation = 0.0
    _cos = 0.0
    _sin = 0.0
    _matrix = 0.0

    def __init__(self, lwf, parent, objId):
        super().__init__(lwf, parent, objId)
        data = lwf.data.bitmaps[objId]
        fragment = lwf.data.textureFragments[data.textureFragmentId]
        texdata = lwf.data.textures[fragment.textureId]

        self.width = fragment.w / texdata.scale
        self.height = fragment.h / texdata.scale
        self.offsetX = fragment.x
        self.offsetY = fragment.y
        self.originalWidth = fragment.ow
        self.originalHeight = fragment.oh

        self.depth = -1
        self.visible = True

        self.regX = 0
        self.regY = 0
        self.x = 0
        self.y = 0
        self.scaleX = 0
        self.scaleY = 0
        self.rotation = 0
        self.alpha = 1

        self._scaleX = self.scaleX
        self._scaleY = self.scaleY
        self._rotation = self.rotation
        self._cos = 1
        self._sin = 0

        self._matrix = Matrix()

    def Exec(self, matrixId=0, colorTransformId=0):
        pass

    def Update(self, m, c):
        dirty = False
        if self.rotation is not self._rotation:
            self._rotation = self.rotation
            radian = self._rotation * math.pi / 180.0
            self._cos = math.cos(radian)
            self._sin = math.sin(radian)
            dirty = True
        if dirty or self._scaleX is not self.scaleX or self._scaleY is not self.scaleY:
            self._scaleX = self.scaleX
            self._scaleY = self.scaleY
            self._matrix.scaleX = self._scaleX * self._cos
            self._matrix.skew1 = self.scaleX * self._sin
            self._matrix.skew0 = self.scaleY * -self._sin
            self._matrix.scaleY = self.scaleY * self._cos
        self._matrix.translateX = self.x - self.regX
        self._matrix.translateY = self.y - self.regY

        self.m_matrix.scaleX = m.scaleX * self._matrix.scaleX + m.skew0 * self._matrix.skew1
        self.m_matrix.skew0 = m.scaleX * self._matrix.skew0 + m.skew0 * self._matrix.scaleY
        self.m_matrix.translateX = m.scaleX * self.x + m.skew0 * self.y + m.translateX + \
           m.scaleX * self.regX + m.skew0 * self.regY + \
           self.m_matrix.scaleX * -self.regX + self.m_matrix.skew0 * -self.regY

        self.m_matrix.skew1 = m.skew1 * self._matrix.scaleX + m.scaleY * self._matrix.skew1
        self.m_matrix.scaleY = m.skew1 * self._matrix.skew0 + m.scaleY * self._matrix.scaleY
        self.m_matrix.translateY = m.skew1 * self.x + m.scaleY * self.y + m.translateY + m.skew1 \
            * self.regX + m.scaleY * self.regY + self.m_matrix.skew1 * -self.regX + self.m_matrix.scaleY * -self.regY

        self.m_colorTransform.Set(c)
        self.m_colorTransform.multi.alpha *= self.alpha

        self.m_lwf.RenderObject()

    def DetachFromParent(self):
        if self.m_parent is not None:
            self.m_parent.DetachBitmap(self.depth)
            self.m_parent = None

    def IsBitmapClip(self):
        return True


# ----------------------- lwf_button -------------------------------------

class Button(IObject):
    m_data = None
    m_buttonLink = None
    m_handler = None
    m_invert = None
    m_hitX = 0.0
    m_hitY = 0.0

    def __init__(self, *args):
        if len(args) > 0:
            lwf, parent, objId, instId = args[0], args[1], args[2], args[3]
            matrixId = args[4] if args[4] else -1
            colorTransformId = args[5] if args[5] else -1
            super().__init__(lwf, parent, Format.Object.Type.BUTTON, objId, instId)
            self.m_matrixId = matrixId
            self.m_colorTransformId = colorTransformId

            self.m_invert = Matrix()
            self.m_hitX = INT32_MINVALUE
            self.m_hitY = INT32_MINVALUE

            if objId >= 0:
                self.m_data = lwf.data.buttons[objId]
                self.m_dataMatrixId = self.m_data.matrixId

            handler = lwf.GetButtonEventHandlers(self)
            if handler is not None:
                self.m_handler = ButtonEventHandlers()
                self.m_handler.Add(handler)
                self.m_handler.Call(ButtonEventHandlers.Type.LOAD, self)

    # Getters and setters
    @property
    def data(self):
        return self.m_data

    @property
    def width(self):
        return self.m_data.width if self.m_data is not None else 0

    @property
    def height(self):
        return self.m_data.height if self.m_data is not None else 0

    @property
    def hitX(self):
        return self.m_hitX

    @property
    def hitY(self):
        return self.m_hitY

    @property
    def buttonLink(self):
        return self.m_buttonLink

    @buttonLink.setter
    def buttonLink(self, value):
        self.m_buttonLink = value

    # main methods
    def SetHandlers(self, handler):
        if self.m_handler is None:
            self.m_handler = ButtonEventHandlers()
        else:
            self.m_handler.Clear()
        self.m_handler.Add(handler)

    def Exec(self, matrixId=0, colorTransformId=0):
        super().Exec(matrixId, colorTransformId)
        self.EnterFrame()

    def Update(self, m, c):
        super().Update(m, c)

        if self.m_handler is not None:
            self.m_handler.Call(ButtonEventHandlers.Type.UPDATE, self)

    def Render(self, v, rOffset):
        if v and self.m_handler is not None:
            self.m_handler.Call(ButtonEventHandlers.Type.RENDER, self)

    def Destroy(self):
        self.m_lwf.ClearFocus(self)
        self.m_lwf.ClearPressed(self)

        if self.m_handler is not None:
            self.m_handler.Call(ButtonEventHandlers.Type.UNLOAD, self)

        super().Destroy()

    def LinkButton(self):
        if self.m_lwf.focus == self:
            self.m_lwf.focusOnLink = True
        self.m_buttonLink = self.m_lwf.buttonHead
        self.m_lwf.buttonHead = self

    def CheckHit(self, px, py):
        Utility.InvertMatrix(self.m_invert, self.m_matrix)
        x, y = Utility.CalcMatrixToPoint(px, py, self.m_invert)
        if 0 <= x < self.m_data.width and 0 <= y < self.m_data.height:
            self.m_hitX = x
            self.m_hitY = y
            return True
        self.m_hitX = INT32_MINVALUE
        self.m_hitY = INT32_MINVALUE
        return False

    def EnterFrame(self):
        if self.m_handler is not None:
            self.m_handler.Call(ButtonEventHandlers.Type.ENTERFRAME, self)

    def RollOver(self):
        if self.m_handler is not None:
            self.m_handler.Call(ButtonEventHandlers.Type.ROLLOVER, self)

        self.PlayAnimation(Format.ButtonCondition.Condition.ROLLOVER)

    def RollOut(self):
        if self.m_handler is not None:
            self.m_handler.Call(ButtonEventHandlers.Type.ROLLOUT, self)

        self.PlayAnimation(Format.ButtonCondition.Condition.ROLLOUT)

    def Press(self):
        if self.m_handler is not None:
            self.m_handler.Call(ButtonEventHandlers.Type.PRESS, self)

        self.PlayAnimation(Format.ButtonCondition.Condition.PRESS)

    def Release(self):
        if self.m_handler is not None:
            self.m_handler.Call(ButtonEventHandlers.Type.RELEASE, self)

        self.PlayAnimation(Format.ButtonCondition.Condition.RELEASE)

    def KeyPress(self, code):
        if self.m_handler is not None:
            self.m_handler.CallKEYPRESS(self, code)

        self.PlayAnimation(Format.ButtonCondition.Condition.KEYPRESS, code)

    def PlayAnimation(self, condition, code=0):
        conditions = self.m_lwf.data.buttonConditions
        i = 0
        while i < self.m_data.conditions:
            c = conditions[self.m_data.conditionId + i]
            if (c.condition & condition) != 0 and (
                    condition != Format.ButtonCondition.Condition.KEYPRESS or c.keyCode == code):
                self.m_lwf.PlayAnimation(c.animationId, self.m_parent, self)
            i += 1

    def AddButtonEventHandler(self, eventName, handler):
        eventId = self.m_lwf.GetEventOffset()
        if eventName is "load":
            self.m_handler.Add(eventId, load=handler)
            return eventId
        elif eventName is "unload":
            self.m_handler.Add(eventId, u=handler)
            return eventId
        elif eventName is "enterFrame":
            self.m_handler.Add(eventId, e=handler)
            return eventId
        elif eventName is "update":
            self.m_handler.Add(eventId, up=handler)
            return eventId
        elif eventName is "render":
            self.m_handler.Add(eventId, r=handler)
            return eventId
        elif eventName is "press":
            self.m_handler.Add(eventId, p=handler)
            return eventId
        elif eventName is "release":
            self.m_handler.Add(eventId, rl=handler)
            return eventId
        elif eventName is "rollOver":
            self.m_handler.Add(eventId, rOver=handler)
            return eventId
        elif eventName is "rollOut":
            self.m_handler.Add(eventId, rOut=handler)
            return eventId
        else:
            return -1

    def AddButtonKeyPressHandler(self, eventName, handler):
        eventId = -1
        if eventName is "keyPress":
            eventId = self.m_lwf.GetEventOffset()
            self.m_handler.Add(eventId, k=handler)
        return eventId

    def RemoveEventHandler(self, eventName, eventId):
        if eventName is "load" \
                or eventName is "unload" \
                or eventName is "enterFrame" \
                or eventName is "update" \
                or eventName is "render" \
                or eventName is "press" \
                or eventName is "release" \
                or eventName is "rollOver" \
                or eventName is "rollOut" \
                or eventName is "keyPress":
            self.m_handler.Remove(eventId)

    def ClearEventHandler(self, eventName):
        if eventName is "load":
            self.m_handler.Clear(ButtonEventHandlers.Type.LOAD)
        elif eventName is "unload":
            self.m_handler.Clear(ButtonEventHandlers.Type.UNLOAD)
        elif eventName is "enterFrame":
            self.m_handler.Clear(ButtonEventHandlers.Type.ENTERFRAME)
        elif eventName is "update":
            self.m_handler.Clear(ButtonEventHandlers.Type.UPDATE)
        elif eventName is "render":
            self.m_handler.Clear(ButtonEventHandlers.Type.RENDER)
        elif eventName is "press":
            self.m_handler.Clear(ButtonEventHandlers.Type.PRESS)
        elif eventName is "release":
            self.m_handler.Clear(ButtonEventHandlers.Type.RELEASE)
        elif eventName is "rollOver":
            self.m_handler.Clear(ButtonEventHandlers.Type.ROLLOVER)
        elif eventName is "rollOut":
            self.m_handler.Clear(ButtonEventHandlers.Type.ROLLOUT)
        elif eventName is "keyPress":
            self.m_handler.Clear(ButtonEventHandlers.Type.KEYPRESS)


# lwf_lwfcontainer -------------------------------------------------------

class LWFContainer(Button):
    m_child = None

    def __init__(self, parent, child):
        self.m_lwf = parent.lwf
        self.m_parent = parent
        self.m_child = child

    @property
    def child(self):
        return self.m_child

    def CheckHit(self, px, py):
        button = self.m_child.InputPoint(int(px), int(py))
        return True if button is not None else False

    def RollOver(self):
        pass

    def RollOut(self):
        if self.m_child.focus is not None:
            self.m_child.RollOut()
            self.m_child.ClearFocus(self.m_child.focus)

    def Press(self):
        self.m_child.InputPress()

    def Release(self):
        self.m_child.InputRelease()

    def KeyPress(self, code):
        self.m_child.InputKeyPress(code)


# -----------------------   lwf_core ----------------------------------------

class LWF:
    class TweenMode(Enum):
        Movie = 0
        LWF = 1

    m_instanceOffset = 0
    m_iObjectOffset = 0
    ROUND_OFF_TICK_RATE = 0.05
    m_textureLoadHandler = None

    m_data = None
    m_rendererFactory = None
    m_rootMovieStringId = 0
    m_property = None
    m_rootMovie = None
    m__root = None
    m_instances = None
    m_focus = None
    m_pressed = None
    m_buttonHead = None
    m_movieCommands = None
    m_programObjectConstructors = None
    m_detachHandler = None
    m_allowButtonList = None
    m_denyButtonList = None
    m_execHandlers = None
    m_textDictionary = None
    m_blendModes = None
    m_maskModes = None
    m_frameRate = 0
    m_fastForwardTimeout = 0
    m_fastForward = False
    m_fastForwardCurrent = False
    m_frameSkip = False
    m_execLimit = 0
    m_renderingIndex = 0
    m_renderingIndexOffsetted = 0
    m_renderingCount = 0
    m_depth = 0
    m_execCount = 0
    m_updateCount = 0
    m_instanceId = 0
    m_time = 0.0
    m_progress = 0.0
    m_tick = 0.0
    m_roundOffTick = 0.0
    m_parent = None
    m_attachName = None
    m_attachVisible = False
    m_execDisabled = False
    m_executedForExecDisabled = False
    m_interceptByNotAllowOrDenyButtons = False
    m_intercepted = False
    m_propertyDirty = False
    m_focusOnLink = False
    m_needsUpdate = False
    m_needsUpdateForAttachLWF = False
    m_pointX = 0.0
    m_pointY = 0.0
    m_pressing = False
    m_matrix = None
    m_matrixIdentity = None
    m_execMatrix = None
    m_colorTransform = None
    m_colorTransformIdentity = None
    m_execColorTransform = None
    m_alive = False
    m_eventOffset = 0
    # lwf_event -----------------------------------------------------------------------------------------
    m_eventHandlers: List[(EventHandlerDictionary or None)] = None
    m_genericEventHandlerDictionary = None
    m_movieEventHandlers = None
    m_buttonEventHandlers = None
    m_movieEventHandlersByFullName = None
    m_buttonEventHandlersByFullName = None

    # lwf_core ------------------------------------------------------------------------------------------

    interactive = False
    scaleByStage = 0.0
    isLWFAttached = False
    lwfLoader = None
    lwfUnloader = None
    privateData = None
    tweenMode = None
    tweens = None
    tweenEventId = None

    def __init__(self, lwfData, r):
        print("Create a lwf!")
        self.m_data = lwfData
        self.interactive = len(self.m_data.buttonConditions) > 0
        self.m_frameRate = self.m_data.header.frameRate
        self.m_execLimit = 3
        self.m_frameSkip = False
        self.m_tick = 1.0 / self.m_frameRate
        self.m_roundOffTick = self.m_tick * self.ROUND_OFF_TICK_RATE
        self.m_attachVisible = True
        self.m_interceptByNotAllowOrDenyButtons = True
        self.m_intercepted = False
        self.scaleByStage = 1
        self.m_needsUpdate = False
        self.m_needsUpdateForAttachLWF = False
        self.m_pointX = SINGLE_MINVALUE
        self.m_pointY = SINGLE_MINVALUE
        self.m_pressing = False
        self.m_instanceOffset += 1
        self.m_instanceId = self.m_instanceOffset
        self.m_alive = True

        if not self.interactive and len(self.m_data.frames) == 1:
            self.DisableExec()
        self.m_property = Property(self)
        self.m_instances = [IObject() for _ in range(0, len(self.m_data.instanceNames))]
        print(self.m_instances)
        self.InitEvent()
        self.m_movieCommands = MovieCommands()
        self.m_programObjectConstructors = [ProgramObjectConstructor() for _ in
                                            range(0, len(self.m_data.programObjects))]
        self.m_textDictionary = TextDictionary()

        self.m_matrix = Matrix()
        self.m_matrixIdentity = Matrix()
        self.m_execMatrix = Matrix()
        self.m_colorTransform = ColorTransform()
        self.m_ColorTransFormIdentity = ColorTransform()
        self.m_execColorTransform = ColorTransform()
        self.m_blendModes = BlendModes()
        self.m_maskModes = MaskModes()

        self.Init()

        self.SetRendererFactory(r)

    # getters and setters
    @property
    def data(self):
        return self.m_data

    # @property
    # def interactive(self):
    #     return self.m_interactive
    #
    # @interactive.setter
    # def interactive(self, value):
    #     self.m_interactive = value

    # @property
    # def scaleByStage(self):
    #     return self.m_scaleByStage
    #
    # @scaleByStage.setter
    # def scaleByStage(self, value):
    #     self.m_scaleByStage = value


    @property
    def isExecDisabled(self):
        return self.m_execDisabled

    @property
    def attachVisible(self):
        return self.m_attachVisible

    @property
    def isPropertyDirty(self):
        return self.m_propertyDirty

    # @property
    # def isLWFAttached(self):
    #     return self.b_isLWFAttached
    #
    # @isLWFAttached.setter
    # def isLWFAttached(self, value):
    #     self.b_isLWFAttached = value

    # @property
    # def lwfLoader(self):
    #     return self.b_lwfLoader
    #
    # @lwfLoader.setter
    # def lwfLoader(self, value):
    #     self.b_lwfLoader = value

    # @property
    # def lwfUnloader(self):
    #     return self.b_lwfUnloader
    #
    # @lwfUnloader.setter
    # def lwfUnloader(self, value):
    #     self.b_lwfUnloader = value

    # @property
    # def privateData(self):
    #     return self.b_privateData
    #
    # @privateData.setter
    # def privateData(self, value):
    #     self.b_privateData = value

    # @property
    # def tweenMode(self):
    #     return self.b_tweenMode
    #
    # @tweenMode.setter
    # def tweenMode(self, value):
    #     self.b_tweenMode = value

    # @property
    # def tweens(self):
    #     return self.b_tweens
    #
    # @tweens.setter
    # def tweens(self, value):
    #     self.b_tweens = value

    # @property
    # def tweenEventId(self):
    #     return self.b_tweenEventId
    #
    # @tweenEventId.setter
    # def tweenEventId(self, value):
    #     self.b_tweenEventId = value

    @property
    def rendererFactory(self):
        return self.m_rendererFactory

    @property
    def lwfproperty(self):
        return self.m_property

    @property
    def rootMovie(self):
        return self.m_rootMovie

    @property
    def __root(self):
        return self.m__root

    @property
    def focus(self):
        return self.m_focus

    @property
    def pressed(self):
        return self.m_pressed

    @property
    def buttonHead(self):
        return self.m_buttonHead

    @buttonHead.setter
    def buttonHead(self, value):
        self.m_buttonHead = value

    @property
    def needsUpdate(self):
        return self.m_needsUpdate

    @property
    def needsUpdateForAttachLWF(self):
        return self.m_needsUpdateForAttachLWF

    @property
    def pointX(self):
        return self.m_pointX

    @property
    def pointY(self):
        return self.m_pointY

    @property
    def pressing(self):
        return self.m_pressing

    @property
    def frameRate(self):
        return self.m_frameRate

    @property
    def renderingIndex(self):
        return self.m_renderingIndex

    @property
    def renderingIndexOffsetted(self):
        return self.m_renderingIndexOffsetted

    @property
    def renderingCount(self):
        return self.m_renderingCount

    @property
    def execCount(self):
        return self.m_execCount

    @property
    def updateCount(self):
        return self.m_updateCount

    @property
    def instanceId(self):
        return self.m_instanceId

    @property
    def width(self):
        return self.m_data.header.width

    @property
    def height(self):
        return self.m_data.header.height

    @property
    def time(self):
        return self.m_time

    @property
    def progress(self):
        return self.m_progress

    @progress.setter
    def progress(self, value):
        self.m_progress = value

    @property
    def tick(self):
        return self.m_tick

    @property
    def alive(self):
        return self.m_alive

    @property
    def focusOnLink(self):
        return self.m_focusOnLink

    @focusOnLink.setter
    def focusOnLink(self, value):
        self.m_focusOnLink = value

    @property
    def parent(self):
        return self.m_parent

    @parent.setter
    def parent(self, value):
        self.m_parent = value

    @property
    def name(self):
        return self.m_data.strings[self.m_data.header.nameStringId]

    @property
    def attachName(self):
        return self.m_attachName

    @attachName.setter
    def attachName(self, value):
        self.m_attachName = value

    @property
    def depth(self):
        return self.m_depth

    @depth.setter
    def depth(self, value):
        self.m_depth = value

    @property
    def detachHandler(self):
        return self.m_detachHandler

    @detachHandler.setter
    def detachHandler(self, value):
        self.m_detachHandler = value

    @property
    def interceptByNotAllowOrDenyButtons(self):
        return self.m_interceptByNotAllowOrDenyButtons

    @interceptByNotAllowOrDenyButtons.setter
    def interceptByNotAllowOrDenyButtons(self, value):
        self.m_interceptByNotAllowOrDenyButtons = value

    @property
    def intercepted(self):
        return self.interactive and self.m_intercepted

    # main methods

    def SetRendererFactory(self, rendererFactory=None):
        if rendererFactory is None:
            rendererFactory = NullRendererFactory()
        self.m_rendererFactory = rendererFactory
        self.m_rendererFactory.init(self)

    def SetFrameRate(self, f):
        if f == 0:
            return
        self.m_frameRate = f
        self.m_tick = 1 / self.m_frameRate

    def SetPreferredFrameRate(self, f, execLimit=2):
        if f == 0:
            return
        self.m_execLimit = math.ceil(self.m_frameRate / f) + execLimit

    def FitForHeight(self, stageHeight):
        Utility.FitForHeight(self, stageHeight)

    def FitForWidth(self, stageWidth):
        Utility.FitForWidth(self, stageWidth)

    def ScaleFroheight(self, stageHeight):
        Utility.ScaleForHeight(self, stageHeight)

    def ScaleForWidth(self, stageWidth):
        Utility.ScaleForWidth(self, stageWidth)

    def RenderOffset(self):
        self.m_renderingIndexOffsetted = 0

    def ClearRenderOffset(self):
        self.m_renderingIndexOffsetted = self.m_renderingIndex

    def RenderObject(self, count=1):
        self.m_renderingIndex += count
        self.m_renderingIndexOffsetted += count
        return self.m_renderingIndex

    def BeginBlendMode(self, blendMode):
        self.m_blendModes.append(blendMode)
        self.m_rendererFactory.SetBlendMode(blendMode)

    def EndBlendMode(self):
        self.m_blendModes.remove(len(self.m_blendModes) - 1)
        self.m_rendererFactory.SetBlendMode(self.m_blendModes[len(self.m_blendModes) - 1] if len(self.m_blendModes) > 0
                                            else Format.Constant.BLEND_MODE_NORMAL.value)

    def BeginMaskMode(self, maskMode):
        self.m_maskModes.append(maskMode)
        self.m_rendererFactory.SetMaskMode(maskMode)

    def EndMaskMode(self):
        self.m_maskModes.remove(len(self.m_maskModes) - 1)
        self.m_rendererFactory.SetMaskMode(self.m_maskModes[len(self.m_maskModes) - 1] if len(self.m_maskModes) > 0
                                           else Format.Constant.BLEND_MODE_NORMAL.value)

    def SetAttachVisible(self, visible):
        self.m_attachVisible = visible

    def ClearFocus(self, button):
        if self.m_focus == button:
            self.m_focus = None

    def ClearPressed(self, button):
        if self.m_pressed == button:
            self.m_pressed = None

    def ClearIntercepted(self):
        self.m_intercepted = False

    def Init(self):
        self.m_time = 0
        self.m_progress = 0

        Utility.Clear_Array(self.m_instances, 0, len(self.m_instances))
        self.m_focus = None

        self.m_movieCommands.clear()

        self.m_rootMovieStringId = self.GetStringId("_root")
        if self.m_rootMovie is not None:
            self.m_rootMovie.Destroy()
        self.m_rootMovie = Movie(self, None, self.m_data.header.rootMovieId,  self.SearchInstanceId(self.m_rootMovieStringId))
        self.m__root = self.m_rootMovie

    def SetRoot(self, root):
        self.m__root = root

    def CalcMatrix(self, matrix):
        p = self.m_property
        if p.hasMatrix:
            if matrix is not None:
                m = Utility.CalcMatrix(self.m_matrix, matrix, p.matrix)
            else:
                m = p.matrix
        else:
            m = self.m_matrixIdentity if matrix is None else matrix
        return m

    def CalcColorTransform(self, colorTransform):
        p = self.m_property
        if p.hasColorTransform:
            if colorTransform is not None:
                c = Utility.CalcColorTransform(self.m_colorTransform, colorTransform, p.colorTransform)
            else:
                c = p.colorTransform
        else:
            c = self.m_colorTransformIdentity if colorTransform is None else colorTransform
        return c

    def LinkButton(self):
        self.m_buttonHead = None
        if self.interactive and self.m_rootMovie.hasButton:
            self.m_focusOnLink = False
            self.m_rootMovie.LinkButton()
            if self.m_focus is not None and not self.m_focusOnLink:
                self.m_focus.RollOut()
                self.m_focus = None

    def ExecInternal(self, tick):
        print("Exec Internal lwf")
        if self.m_rootMovie is None:
            return 0
        execed = False
        currentProgress = self.m_progress

        if self.m_execDisabled and self.tweens is None:
            if not self.m_executedForExecDisabled:
                self.m_execCount += 1
                self.m_rootMovie.Exec()
                self.m_rootMovie.PostExec(True)
                self.m_executedForExecDisabled = True
                execed = True
        else:
            progressing = True
            if tick == 0:
                self.m_progress = self.m_tick
            elif tick < 0:
                self.m_progress = self.m_tick
                progressing = False
            else:
                if self.m_time == 0:
                    self.m_time += self.m_tick
                    self.m_progress += self.m_tick
                else:
                    self.m_time += tick
                    self.m_progress += tick

            if self.m_execHandlers is not None:
                for h in self.m_execHandlers:
                    h(self)

            execLimit = self.m_execLimit
            while self.m_progress >= self.m_tick - self.m_roundOffTick:
                execLimit -= 1
                if execLimit < 0:
                    self.m_progress = 0
                    break
                self.m_progress -= self.m_tick
                self.m_execCount += 1
                self.m_rootMovie.Exec()
                self.m_rootMovie.PostExec(progressing)
                execed = True
                if not self.m_frameSkip:
                    break
            if self.m_progress < self.m_roundOffTick:
                self.m_progress = 0

            self.LinkButton()

        if self.isLWFAttached:
            hasButton = self.m_rootMovie.ExecAttachedLWF(tick, currentProgress)
            if hasButton:
                self.LinkButton()

        self.m_needsUpdate = False
        if not self.m_fastForward:
            if execed or self.m_propertyDirty or self.m_needsUpdateForAttachLWF:
                self.m_needsUpdate = True

        if not self.m_execDisabled:
            if tick < 0:
                self.m_progress = currentProgress

        return self.m_renderingCount

    def Exec(self, tick=0, matrix=None, colorTransform=None):
        print("Exec lwf")
        needsToUpdate = False
        if matrix is not None:
            needsToUpdate |= self.m_execMatrix.SetWithComparing(matrix)
        if colorTransform is not None:
            needsToUpdate |= self.m_execColorTransform.SetWithComparing(colorTransform)
        startTime = datetime.now()
        if self.m_parent is None:
            self.m_fastForwardCurrent = self.m_fastForward
            if self.m_fastForwardCurrent:
                tick = self.m_tick
                startTime = datetime.now()

        while True:
            renderingCount = self.ExecInternal(tick)
            needsToUpdate |= self.m_needsUpdate
            if needsToUpdate:
                self.Update(matrix, colorTransform)
            if self.isLWFAttached:
                self.m_rootMovie.UpdateAttachedLWF()
            if needsToUpdate:
                self.m_rootMovie.PostUpdate()
            if self.m_fastForwardCurrent and self.m_fastForward and self.m_parent is None:
                diff = datetime.now() - startTime
                if diff >= self.m_fastForwardTimeout:
                    break
            else:
                break

        return renderingCount

    def ForceExec(self, matrix=None, colorTransform=None):
        return self.Exec(0, matrix, colorTransform)

    def ForceExecWithoutProgress(self, matrix=None, colorTransform=None):
        return self.Exec(-1, matrix, colorTransform)

    def Update(self, matrix=None, colorTransform=None):
        self.m_updateCount += 1
        m = self.CalcMatrix(matrix)
        c = self.CalcColorTransform(colorTransform)
        self.m_renderingIndex = 0
        self.m_renderingIndexOffsetted = 0
        self.m_rootMovie.Update(m, c)
        self.m_renderingCount = self.m_renderingIndex
        self.m_propertyDirty = False
        self.m_needsUpdateForAttachLWF = False

    def Render(self, rIndex=0, rCount=0, rOffset=INT32_MINVALUE):
        if self.m_rootMovie is None or self.m_fastForwardCurrent:
            return 0
        if rCount > 0:
            self.m_renderingCount = rCount
        self.m_renderingIndex = rIndex
        self.m_renderingIndexOffsetted = rIndex
        if self.m_property.hasRenderingOffset:
            self.RenderOffset()
            rOffset = self.m_property.renderingOffset
        self.m_rendererFactory.beginRender(self)
        self.m_rootMovie.Render(self.m_attachVisible, rOffset)
        self.m_rendererFactory.endRender(self)
        return self.m_renderingIndex - rIndex

    def Inspect(self, inspector, hierarchy=0, inspectDepth=0, rIndex=0, rCount=0, rOffset=-2147483648):
        if rCount > 0:
            self.m_renderingCount = rCount
        self.m_renderingIndex = rIndex
        self.m_renderingIndexOffsetted = rIndex
        if self.m_property.hasRenderingOffset:
            self.RenderOffset()
            rOffset = self.m_property.renderingOffset
        self.m_rootMovie.Inspect(inspector, hierarchy, inspectDepth, rOffset)
        return self.m_renderingIndex - rIndex

    def Destroy(self):
        self.m_rootMovie.Destroy()
        if self.m_rendererFactory is not None:
            self.m_rendererFactory.Destruct()
            self.m_rendererFactory = None
        self.m_alive = False
        if self.lwfUnloader is not None:
            self.lwfUnloader()

    def GetIObjectOffset(self):
        self.m_iObjectOffset += 1
        return self.m_iObjectOffset

    def SearchMovieInstance(self, *args):
        assert len(args) is 1
        if isinstance(args[0], int):
            stringId = args[0]
            return self.SearchMovieInstanceByInstanceId(self.SearchInstanceId(stringId))
        else:
            instanceName = args[0]
            if "." in instanceName:
                names = instanceName.split('.')
                if names[0] != self.m_data.strings[self.m_rootMovieStringId]:
                    return None

                m = self.m_rootMovie
                i = 1
                while i < len(names):
                    m = m.SearchMovieInstance(names[i], False)
                    if m is None:
                        return None
                    i += 1

                return m

            stringId = self.GetStringId(instanceName)
            if stringId == -1:
                return self.rootMovie.SearchMovieInstance(instanceName, True)
            return self.SearchMovieInstance(stringId)

    def __getitem__(self, instanceName):
        return self.SearchMovieInstance(instanceName)

    def SearchMovieInstanceByInstanceId(self, instId):
        if instId < 0 or instId >= len(self.m_instances):
            return None
        obj = self.m_instances[instId]
        while obj is not None:
            if obj.IsMovie():
                return obj
            obj = obj.nextInstance
        return None

    def SearchButtonInstance(self, *args) -> (Button or None):
        assert len(args) is 1
        if isinstance(args[0], int):
            stringId = args[0]
            return self.SearchButtonInstanceByInstanceId(self.SearchInstanceId(stringId))
        else:
            instanceName = args[0]
            if "." in instanceName:
                names = instanceName.split('.')
                if names[0] is not self.m_data.strings[self.m_rootMovieStringId]:
                    return None

                m = self.m_rootMovie
                i = 1
                while i < len(names):
                    if i is len(names) - 1:
                        return m.SearchButtonInstance(names[i], False)
                    else:
                        m = m.SearchMovieInstance(names[i], False)
                        if m is None:
                            return None
                    i += 1
                return None

            stringId = self.GetStringId(instanceName)
            if stringId is -1:
                return self.rootMovie.SearchButtonInstance(instanceName, True)

            return self.SearchButtonInstance(stringId)

    def SearchButtonInstanceByInstanceId(self, instId):
        if instId < 0 or instId >= len(self.m_instances):
            return None
        obj = self.m_instances[instId]
        while obj is not None:
            if obj.IsButton():
                return obj
            obj = obj.nextInstance
        return None

    def GetInstance(self, instId):
        print(self.m_instances)
        print(self)
        return self.m_instances[instId]

    def SetInstance(self, instId, instance):
        self.m_instances[instId] = instance

    def GetProgramObjectConstructor(self, arg):
        if isinstance(arg, int):
            programObjectId = arg
            if programObjectId < 0 or programObjectId >= len(self.m_data.programObjects):
                return None
            return self.m_programObjectConstructors[programObjectId]
        else:
            programObjectName = arg
            return self.GetProgramObjectConstructor(self.SearchProgramObjectId(programObjectName))

    def SetProgramObjectConstructor(self, arg, programObjectConstructor):
        if isinstance(arg, int):
            programObjectId = arg
            if programObjectId < 0 or programObjectId >= len(self.m_data.programObjects):
                return
            self.m_programObjectConstructors[programObjectId] = programObjectConstructor
        else:
            programObjectName = arg
            self.SetProgramObjectConstructor(self.SearchProgramObjectId(programObjectName),
                                             programObjectConstructor)

    def ExecMovieCommand(self):
        if len(self.m_movieCommands) is 0:
            return
        deletes = []
        for key, value in self.m_movieCommands.items():
            avaliable = True
            movie = self.m_rootMovie
            for name in key:
                movie = movie.SearchMovieInstance(name)
                if movie is None:
                    avaliable = False
                    break
            if avaliable:
                value(movie)
                deletes.append(key)

        for key in deletes:
            self.m_movieCommands.remove(key)

    def SetMovieCommand(self, instanceNames, cmd):
        names = []
        for name in instanceNames:
            names.append(name)
        self.m_movieCommands.set(names, cmd)
        self.ExecMovieCommand()

    def SearchAttachedMovie(self, attachName):
        return self.m_rootMovie.SearchAttachedMovie(attachName)

    def SearchAttachedLWF(self, attachName):
        return self.m_rootMovie.SearchAttachedLWF(attachName)

    def AddAllowButton(self, buttonName):
        instId = self.SearchInstanceId(self.GetStringId(buttonName))
        if instId < 0:
            return False

        if self.m_allowButtonList is None:
            self.m_allowButtonList = AllowButtonList()
        self.m_allowButtonList[instId] = True
        return True

    def RemoveAllowButton(self, buttonName):
        if self.m_allowButtonList is None:
            return False

        instId = self.SearchInstanceId(self.GetStringId(buttonName))
        if instId < 0:
            return False
        return self.m_allowButtonList.Remove(instId)

    def ClearAllowButton(self):
        self.m_allowButtonList = None

    def AddDenyButton(self, buttonName):
        instId = self.SearchInstanceId(self.GetStringId(buttonName))
        if instId < 0:
            return False
        if self.m_denyButtonList is None:
            self.m_denyButtonList = DenyButtonList()
        self.m_denyButtonList[instId] = True
        return True

    def DenyAllButtons(self):
        if self.m_denyButtonList is None:
            self.m_denyButtonList = DenyButtonList()
        instId = 0
        while instId < len(self.m_instances):
            self.m_denyButtonList[instId] = True
            instId += 1

    def RemoveDenyButton(self, buttonName):
        if self.m_denyButtonList is None:
            return False
        instId = self.SearchInstanceId(self.GetStringId(buttonName))
        if instId < 0:
            return False
        return self.m_denyButtonList.Remove(instId)

    def ClearDenyButton(self):
        self.m_denyButtonList = None

    def DisableExec(self):
        self.m_execDisabled = True
        self.m_executedForExecDisabled = False

    def EnableExec(self):
        self.m_execDisabled = False

    def SetPropertyDirty(self):
        self.m_propertyDirty = True
        if self.m_parent is not None:
            self.m_parent.lwf.SetPropertyDirty()

    def GetParent(self):
        if self.m_parent is None:
            return None

        lwfParent = self.m_parent.lwf
        while True:
            if lwfParent is None or lwfParent.m_parent is None:
                return lwfParent
            lwfParent = lwfParent.m_parent.lwf

    def SetInteractive(self):
        self.interactive = True
        if self.m_parent is not None:
            self.m_parent.lwf.SetInteractive()

    def SetFrameSkip(self, frameSkip):
        self.m_frameSkip = frameSkip
        self.m_progress = 0
        if self.m_parent is not None:
            self.m_parent.lwf.SetFrameSkip(frameSkip)

    def SetLWFAttached(self):
        self.isLWFAttached = True
        self.m_needsUpdateForAttachLWF = True
        if self.m_parent is not None:
            self.m_parent.lwf.SetLWFAttached()

    def SetFastForwardTimeout(self, fastForwardTimeout):
        self.m_fastForwardTimeout = fastForwardTimeout

    def SetFastForward(self, fastForward):
        self.m_fastForward = fastForward
        if self.m_parent is not None:
            self.m_parent.lwf.SetFastForward(fastForward)

    def AddExecHandler(self, execHandler):
        if self.m_execHandlers is None:
            self.m_execHandlers = ExecHandlerList()
        self.m_execHandlers.append(execHandler)

    def RemoveExecHandler(self, execHandler):
        if self.m_execHandlers is None:
            return
        self.m_execHandlers.RemoveAll(lambda h: h == execHandler)

    def ClearExecHandler(self):
        self.m_execHandlers = None

    def SetExecHandler(self, execHandler):
        self.ClearExecHandler()
        self.AddExecHandler(execHandler)

    def SetText(self, textName, text):
        boolean, item = self.m_textDictionary.TryGetValue(textName)
        if not boolean:
            self.m_textDictionary[textName] = TextDictionaryItem(text)
        else:
            if item.renderer is not None:
                item.renderer.SetText(text)
            item.text = text

    def GetText(self, textName):
        boolean, item = self.m_textDictionary.TryGetValue(textName)
        if boolean:
            return item.text
        return None

    def SetTextRenderer(self, fullPath, textName, text, textRenderer):
        setText = False
        fullName = fullPath + "." + textName
        boolean, item = self.m_textDictionary.TryGetValue(fullName)
        if boolean:
            item.renderer = textRenderer
            if not (item.text is None or item.text == ""):
                textRenderer.SetText(item.text)
                setText = True
        else:
            self.m_textDictionary[fullName] = TextDictionaryItem(text, textRenderer)

        boolean, item = self.m_textDictionary.TryGetValue(textName)
        if boolean:
            item.renderer = textRenderer
            if not setText and not (item.text is None or item.text == ""):
                textRenderer.SetText(item.text)
                setText = True
        else:
            self.m_textDictionary[textName] = TextDictionaryItem(text, textRenderer)

        if not setText:
            textRenderer.SetText(text)

    def ClearTextRenderer(self, textName):
        boolean, item = self.m_textDictionary.TryGetValue(textName)
        if not boolean:
            item.renderer = None

    @staticmethod
    def SetTextureLoadHandler(h):
        LWF.m_textureLoadHandler = h

    @staticmethod
    def GetTextureLoadHandler():
        return LWF.m_textureLoadHandler

    # -----------------------   lwf_animation -------------------------------

    def PlayAnimation(self, animationId, movie, button=None):
        i = 0
        animations = self.m_data.animations[animationId]
        target = movie
        while True:
            case = animations[i]
            i += 1
            if case == Animation.END.value:
                return
            elif case == Animation.PLAY.value:
                target.Play()
            elif case == Animation.STOP.value:
                target.Stop()
            elif case == Animation.NEXTFRAME.value:
                target.NextFrame()
            elif case == Animation.PREVFRAME.value:
                target.PrevFrame()
            elif case == Animation.GOTOFRAME.value:
                target.GotoFrameInternal(animations[i])
                i += 1
            elif case == Animation.GOTOLABEL.value:
                target.GotoFrame(self.SearchFrame(target, animations[i]))
                i += 1
            elif case == Animation.SETTARGET.value:
                target = movie
                count = animations[i]
                i += 1
                if count is 0:
                    break

                j = 0
                while j < count:
                    instId = animations[i]
                    i += 1
                    if instId == Animation.INSTANCE_TARGET_ROOT.value:
                        target = self.m_rootMovie
                    elif instId == Animation.INSTANCE_TARGET_PARENT.value:
                        target = target.parent
                        if target is None:
                            target = self.m_rootMovie
                    else:
                        target = target.SearchMovieInstanceByInstanceId(instId, False)
                        if target is None:
                            target = movie
                    j += 1
            elif case == Animation.EVENT.value:
                eventId = animations[i]
                i += 1
                if self.m_eventHandlers[eventId] is not None:
                    handlers = EventHandlerDictionary(self.m_eventHandlers[eventId])
                    for hk, hv in handlers:
                        hv(movie, button)
            elif case == Animation.CALL.value:
                i += 1

    # ----------------------------- lwf_coredata -----------------------------------------------

    def GetInstanceNameStringId(self, instId):
        if instId < 0 or instId >= len(self.m_data.instanceNames):
            return -1
        return self.m_data.instanceNames[instId].stringId

    def GetStringId(self, string):
        boolean, i = self.m_data.stringMap.TryGetValue(string)
        if boolean:
            return i
        else:
            return -1

    def SearchInstanceId(self, stringId):
        if stringId < 0 or stringId >= len(self.m_data.strings):
            return -1
        boolean, i = self.m_data.instanceNameMap.TryGetValue(stringId)
        if boolean:
            return i
        else:
            return -1

    def SearchFrame(self, movie, *args):
        if not isinstance(args[0], int):
            return self.SearchFrame(movie, self.GetStringId(args[0]))
        else:
            if args[0] < 0 or args[0] >= len(self.m_data.strings):
                return -1
            labelMap = self.m_data.labelMap[movie.objectId]
            boolean, frameNo = labelMap.tryGetValue(args[0])
            if boolean:
                return frameNo + 1
            else:
                return -1

    def GetMovieLabels(self, movie):
        if movie is None:
            return None
        else:
            return self.m_data.labelMap[movie.objectId]

    def SearchMovieLinkage(self, stringId):
        if stringId < 0 or stringId >= len(self.m_data.strings):
            return -1
        boolean, i = self.m_data.movieLinkageMap.TryGetValue(stringId)
        if boolean:
            return self.m_data.movieLinkages[i].movieId
        else:
            return -1

    def GetMovieLinkageName(self, movieId):
        boolean, i = self.m_data.movieLinkageNameMap.TryGetValue(movieId)
        if boolean:
            return self.m_data.strings[i]
        else:
            return None

    def SearchEventId(self, *args):
        assert len(args) is 1
        if not isinstance(args[0], int):
            return self.SearchEventId(self.GetStringId(args[0]))
        else:
            if args[0] < 0 or args[0] >= len(self.m_data.strings):
                return -1
            boolean, i = self.m_data.eventMap.TryGetValue(args[0])
            if boolean:
                return i
            else:
                return -1

    def SearchProgramObjectId(self, *args):
        assert len(args) is 1
        if not isinstance(args[0], int):
            return self.SearchProgramObjectId(self.GetStringId(args[0]))
        else:
            if args[0] < 0 or args[0] >= len(self.m_data.strings):
                return -1
            boolean, i = self.m_data.programObjectMap.TryGetValue(args[0])
            if boolean:
                return i
            else:
                return -1

    # ---------------------------- lwf_coreop --------------------------------------------

    def SetMovieLoadCommand(self, instanceName, handler):
        movie = self.SearchMovieInstance(instanceName)
        if movie is not None:
            handler(movie)
        else:
            w = HandlerWrapper()

            def handle(m):
                self.RemoveMovieEventHandler(instanceName, w.id)
                handler(m)

            h = handle
            w.id = self.AddMovieEventHandler(instanceName, load=h)

    def SetMoviePostLoadCommand(self, instanceName, handler):
        movie = self.SearchMovieInstance(instanceName)
        if movie is not None:
            handler(movie)
        else:
            w = HandlerWrapper()

            def handle(m):
                self.RemoveMovieEventHandler(instanceName, w.id)
                handler(m)

            h = handle
            w.id = self.AddMovieEventHandler(instanceName, postLoad=h)

    def PlayMovie(self, instanceName):
        self.SetMovieLoadCommand(instanceName, lambda m: m.Play())

    def StopMovie(self, instanceName):
        self.SetMovieLoadCommand(instanceName, lambda m: m.Stop())

    def NextFrameMovie(self, instanceName):
        self.SetMovieLoadCommand(instanceName, lambda m: m.NextFrame())

    def PrevFrameMovie(self, instanceName):
        self.SetMovieLoadCommand(instanceName, lambda m: m.PrevFrame())

    def SetVisibleMovie(self, instanceName, visible):
        self.SetMovieLoadCommand(instanceName, lambda m: m.SetVisible(visible))

    def GotoAndStopMovie(self, instanceName, arg):
        if not isinstance(arg, int):
            label = arg
            self.SetMovieLoadCommand(instanceName, lambda m: m.GotoAndStop(label))
        else:
            frameNo = arg
            self.SetMovieLoadCommand(instanceName, lambda m: m.GotoAndStop(frameNo))

    def GotoAndPlayMovie(self, instanceName, arg):
        if not isinstance(arg, int):
            label = arg
            self.SetMovieLoadCommand(instanceName, lambda m: m.GotoAndPlay(label))
        else:
            frameNo = arg
            self.SetMovieLoadCommand(instanceName, lambda m: m.GotoAndPlay(frameNo))

    def MoveMovie(self, instanceName, vx, vy):
        self.SetMovieLoadCommand(instanceName, lambda m: m.Move(vx, vy))

    def MoveToMovie(self, instanceName, vx, vy):
        self.SetMovieLoadCommand(instanceName, lambda m: m.MoveTo(vx, vy))

    def RotateMovie(self, instanceName, degree):
        self.SetMovieLoadCommand(instanceName, lambda m: m.Rotate(degree))

    def RotateToMovie(self, instanceName, degree):
        self.SetMovieLoadCommand(instanceName, lambda m: m.RetateTo(degree))

    def ScaleMovie(self, instanceName, vx, vy):
        self.SetMovieLoadCommand(instanceName, lambda m: m.Scale(vx, vy))

    def ScaleToMovie(self, instanceName, vx, vy):
        self.SetMovieLoadCommand(instanceName, lambda m: m.ScaleTo(vx, vy))

    def SetAlphaMovie(self, instanceName, v):
        self.SetMovieLoadCommand(instanceName, lambda m: m.SetAlpha(v))

    def SetColorTransformMovie(self, instanceName, vr, vg, vb, va, ar, ag, ab, aa):
        self.SetMovieLoadCommand(instanceName,
                                 lambda m: m.SetColorTransform(ColorTransform(vr, vg, vb, va, ar, ag, ab, aa)))

    # lwf_input --------------------------------------------------------------------
    def InputPoint(self, px, py):
        self.m_intercepted = False
        if not self.interactive:
            return None

        x, y = px, py

        self.m_pointX, self.m_pointY = x, y

        found = False
        button = self.m_buttonHead
        while button is not None:
            if button.CheckHit(x, y):
                if self.m_allowButtonList is not None:
                    boolean, v = self.m_allowButtonList.TryGetValue(button.instanceId)
                    if not boolean:
                        if self.m_interceptByNotAllowOrDenyButtons:
                            self.m_intercepted = True
                            break
                        else:
                            continue
                elif self.m_denyButtonList is not None:
                    boolean, v = self.m_denyButtonList.TryGetValue(button.instanceId)
                    if boolean:
                        if self.m_interceptByNotAllowOrDenyButtons:
                            self.m_intercepted = True
                            break
                        else:
                            continue
                found = True
                if self.m_focus is not button:
                    if self.m_focus is not None:
                        self.m_focus.RollOut()
                    self.m_focus = button
                    self.m_focus.RollOver()
                break
            button = button.buttonLink
        if not found and self.m_focus is not None:
            self.m_focus.RollOut()
            self.m_focus = None
        return self.m_focus

    def InputPress(self):
        if not self.interactive:
            return
        self.m_pressing = True
        if self.m_focus is not None:
            self.m_pressed = self.m_focus
            self.m_focus.Press()

    def InputRelease(self):
        if not self.interactive:
            return
        if self.m_focus is not None and self.m_pressed == self.m_focus:
            self.m_focus.Release()
            self.m_pressed = None

    def InputKeyPress(self, code):
        if not self.interactive:
            return

        button = self.m_buttonHead
        while button is not None:
            button.keyPress(code)
            button = button.buttonLink

    # lwf_event -------------------------------------------------------------------------

    def InitEvent(self):
        self.m_eventHandlers = [EventHandlerDictionary() for _ in range(len(self.m_data.events))]
        self.m_genericEventHandlerDictionary = GenericEventHandlerDictionary()
        self.m_movieEventHandlers = [MovieEventHandlers() for _ in range(len(self.m_instances))]
        self.m_buttonEventHandlers = [ButtonEventHandlers() for _ in range(len(self.m_instances))]

    def GetEventOffset(self):
        self.m_eventOffset += 1
        return self.m_eventOffset

    def AddEventHandler(self, arg, eventHandler):
        if isinstance(arg, int):
            if arg < 0 or arg >= len(self.m_data.events):
                return -1
            dictionary = self.m_eventHandlers[arg]
            if dictionary is None:
                dictionary = EventHandlerDictionary()
                self.m_eventHandlers[arg] = dictionary
            handlerId = self.GetEventOffset()
            dictionary.set(handlerId, eventHandler)
            return handlerId
        else:
            eventId = self.SearchEventId(arg)
            if 0 <= eventId < len(self.m_data.events):
                handlerId = self.AddEventHandler(eventId, eventHandler)
            else:
                boolean, dictionary = self.m_genericEventHandlerDictionary.TryGetValue(arg)
                if not boolean:
                    dictionary = EventHandlerDictionary()
                    self.m_genericEventHandlerDictionary[arg] = dictionary
                handlerId = self.GetEventOffset()
                dictionary.set(handlerId, eventHandler)
            return handlerId

    def RemoveEventHandler(self, arg, handlerId):
        if isinstance(arg, int):
            if arg < 0 or arg >= len(self.m_data.events):
                return
            dictionary = self.m_eventHandlers[arg]
            if dictionary is None:
                return
            dictionary.remove(handlerId)
        else:
            eventId = self.SearchEventId(arg)
            if 0 <= eventId < len(self.m_data.events):
                self.RemoveEventHandler(eventId, handlerId)
            else:
                dictionary = self.m_genericEventHandlerDictionary[arg]
                if dictionary is None:
                    return
                dictionary.remove(handlerId)

    def ClearEventHandler(self, arg):
        if isinstance(arg, int):
            if arg < 0 or arg >= len(self.m_data.events):
                return
            self.m_eventHandlers[arg] = None
        else:
            eventId = self.SearchEventId(arg)
            if 0 <= eventId < len(self.m_data.events):
                self.ClearEventHandler(eventId)
            else:
                self.m_genericEventHandlerDictionary.remove(arg)

    def SetEventHandler(self, arg, eventHandler):
        if isinstance(arg, int):
            self.ClearEventHandler(arg)
            return self.AddEventHandler(arg, eventHandler)
        else:
            return self.SetEventHandler(self.SearchEventId(arg), eventHandler)

    def DispatchEvent(self, eventName, m=None, b=None):
        if m is None:
            m = self.m_rootMovie
        eventId = self.SearchEventId(eventName)
        if 0 <= eventId < len(self.m_data.events):
            dictionary = EventHandlerDictionary(self.m_eventHandlers[eventId])
            for hk, hv in dictionary:
                hv(m, b)

    def GetMovieEventHandlers(self, m):
        if self.m_movieEventHandlersByFullName is not None:
            fullName = m.GetFullName()
            if fullName is not None:
                boolean, handlers = self.m_movieEventHandlersByFullName.TryGetValue(fullName)
                return handlers

        instId = m.instanceId
        if instId < 0 or instId >= len(self.m_instances):
            return None
        return self.m_movieEventHandlers[instId]

    def AddMovieEventHandler(self, arg, load=None, postLoad=None, unload=None, enterFrame=None, update=None,
                             render=None):
        if isinstance(arg, int):
            if arg < 0 or arg >= len(self.m_instances):
                return -1

            handlers = self.m_movieEventHandlers[arg]
            if handlers is None:
                handlers = MovieEventHandlers()
                self.m_movieEventHandlers[arg] = handlers

            handlerId = self.GetEventOffset()
            handlers.Add(handlerId, load, postLoad, unload, enterFrame, update, render)
            movie = self.SearchMovieInstanceByInstanceId(arg)
            if movie is not None:
                movie: Movie
                movie.SetHandlers(handlers)
            return handlerId
        else:
            instId = self.SearchInstanceId(self.GetStringId(arg))
            if instId >= 0:
                return self.AddMovieEventHandler(instId, load, postLoad, unload, enterFrame, update, render)

            if "." not in arg:
                return -1

            if self.m_movieEventHandlersByFullName is None:
                self.m_movieEventHandlersByFullName = MovieEventHandlersDictionary()

            boolean, handlers = self.m_movieEventHandlersByFullName.TryGetValue(arg)
            if not boolean:
                handlers = MovieEventHandlers()
                self.m_movieEventHandlersByFullName[arg] = handlers

            handlerId = self.GetEventOffset()
            handlers.Add(handlerId, load, postLoad, unload, enterFrame, update, render)

            movie = self.SearchMovieInstance(arg)
            if movie is not None:
                movie.SetHandlers(handlers)
            return handlerId

    def RemoveMovieEventHandler(self, arg, handlerId):
        if isinstance(arg, int):
            if arg < 0 or arg >= len(self.m_instances):
                return

            handlers = self.m_movieEventHandlers[arg]
            if handlers is None:
                return

            handlers.Remove(handlerId)
            movie = self.SearchMovieInstanceByInstanceId(arg)
            if movie is not None:
                movie: Movie
                movie.SetHandlers(handlers)
        else:
            instId = self.SearchInstanceId(self.GetStringId(arg))
            if instId >= 0:
                self.RemoveMovieEventHandler(instId, handlerId)
                return

            if self.m_movieEventHandlersByFullName is None:
                return

            boolean, handlers = self.m_movieEventHandlersByFullName.TryGetValue(arg)
            if not boolean:
                return

            handlers.remove(handlerId)
            movie = self.SearchMovieInstance(arg)
            if movie is not None:
                movie.SetHandlers(handlers)

    def ClearMovieEventHandler(self, arg, *args):
        if len(arg) is 0:
            if isinstance(arg, int):
                if arg < 0 or arg >= len(self.m_instances):
                    return

                handlers = self.m_movieEventHandlers[arg]
                if handlers is None:
                    return

                handlers.Clear()
                movie = self.SearchMovieInstanceByInstanceId(arg)
                if movie is not None:
                    movie: Movie
                    movie.SetHandlers(handlers)
            else:
                instId = self.SearchInstanceId(self.GetStringId(arg))

                if instId >= 0:
                    self.ClearMovieEventHandler(instId)
                    return

                if self.m_movieEventHandlersByFullName is None:
                    return

                boolean, handlers = self.m_movieEventHandlersByFullName.TryGetValue(arg)
                if not boolean:
                    return

                handlers.Clear()
                movie = self.SearchMovieInstance(arg)
                if movie is not None:
                    movie.SetHandlers(handlers)
        else:
            if isinstance(arg, int):
                if arg < 0 or arg >= len(self.m_instances):
                    return

                handlers = self.m_movieEventHandlers[arg]
                if handlers is None:
                    return

                handlers.Clear(args[0])
                movie = self.SearchMovieInstanceByInstanceId(arg)
                if movie is not None:
                    movie: Movie
                    movie.SetHandlers(handlers)
            else:
                instId = self.SearchInstanceId(self.GetStringId(arg))

                if instId >= 0:
                    self.ClearMovieEventHandler(instId, args[0])
                    return

                if self.m_movieEventHandlersByFullName is None:
                    return

                boolean, handlers = self.m_movieEventHandlersByFullName.TryGetValue(arg)
                if not boolean:
                    return

                handlers.Clear(args[0])
                movie = self.SearchMovieInstance(arg)
                if movie is not None:
                    movie.SetHandlers(handlers)

    def SetMovieEventHandler(self, arg, load=None, postLoad=None, unload=None, enterFrame=None, update=None,
                             render=None):
        self.ClearMovieEventHandler(arg)
        return self.AddMovieEventHandler(arg, load, postLoad, unload, enterFrame, update, render)

    def GetButtonEventHandlers(self, b):
        if self.m_buttonEventHandlersByFullName is not None:
            fullName = b.GetFullName()
            if fullName is not None:
                boolean, handlers = self.m_buttonEventHandlersByFullName.TryGetValue(fullName)
                if boolean:
                    return handlers

        instId = b.instanceId
        if instId < 0 or instId >= len(self.m_instances):
            return None
        return self.m_buttonEventHandlers[instId]

    def AddButtonEventHandler(self, arg, load=None, unload=None, enterFrame=None, update=None, render=None, press=None,
                              release=None, rollOver=None, rollOut=None, keyPress=None):
        self.interactive = True
        if isinstance(arg, int):
            if arg < 0 or arg >= len(self.m_instances):
                return -1
            handlers = self.m_buttonEventHandlers[arg]
            if handlers is None:
                handlers = ButtonEventHandlers()
                self.m_buttonEventHandlers[arg] = handlers

            handlerId = self.GetEventOffset()
            handlers.Add(handlerId, load, unload, enterFrame, update, render, press, release, rollOver, rollOut,
                         keyPress)

            button = self.SearchButtonInstanceByInstanceId(arg)
            if button is not None:
                button: Button
                button.SetHandlers(handlers)
            return handlerId
        else:
            instId = self.SearchInstanceId(self.GetStringId(arg))
            if instId >= 0:
                return self.AddButtonEventHandler(instId, load, unload, enterFrame, update, render, press, release,
                                                  rollOver, rollOut, keyPress)

            if "." not in arg:
                return -1

            if self.m_buttonEventHandlersByFullName is None:
                self.m_buttonEventHandlersByFullName = ButtonEventHandlersDictionary()

            boolean, handlers = self.m_buttonEventHandlersByFullName.TryGetValue(arg)
            if not boolean:
                handlers = ButtonEventHandlers()
                self.m_buttonEventHandlersByFullName[arg] = handlers

            handlerId = self.GetEventOffset()
            handlers.Add(handlerId, load, unload, enterFrame, update, render, press, release, rollOver, rollOut,
                         keyPress)

            button = self.SearchButtonInstance(arg)
            if button is not None:
                button: Button
                button.SetHandlers(handlers)
            return handlerId

    def RemoveButtonEventHandler(self, arg, handlerId):
        if isinstance(arg, int):
            if arg < 0 or arg >= len(self.m_instances):
                return

            handlers = self.m_buttonEventHandlers[arg]
            if handlers is None:
                return

            handlers.Remove(handlerId)
            button = self.SearchButtonInstanceByInstanceId(arg)
            if button is not None:
                button: Button
                button.SetHandlers(handlers)
        else:
            instId = self.SearchInstanceId(self.GetStringId(arg))
            if instId >= 0:
                self.RemoveButtonEventHandler(instId, handlerId)
                return

            if self.m_buttonEventHandlersByFullName is None:
                return

            boolean, handlers = self.m_buttonEventHandlersByFullName.TryGetValue(arg)
            if not boolean:
                return

            handlers.remove(handlerId)
            button = self.SearchButtonInstance(arg)
            if button is not None:
                button: Button
                button.SetHandlers(handlers)

    def ClearButtonEventHandler(self, arg, *args):
        if len(arg) is 0:
            if isinstance(arg, int):
                if arg < 0 or arg >= len(self.m_instances):
                    return

                handlers = self.m_buttonEventHandlers[arg]
                if handlers is None:
                    return

                handlers.Clear()
                button = self.SearchButtonInstanceByInstanceId(arg)
                if button is not None:
                    button: Button
                    button.SetHandlers(handlers)
            else:
                instId = self.SearchInstanceId(self.GetStringId(arg))

                if instId >= 0:
                    self.ClearButtonEventHandler(instId)
                    return

                if self.m_buttonEventHandlersByFullName is None:
                    return

                boolean, handlers = self.m_buttonEventHandlersByFullName.TryGetValue(arg)
                if not boolean:
                    return

                handlers.Clear()
                button = self.SearchButtonInstance(arg)
                if button is not None:
                    button.SetHandlers(handlers)
        else:
            if isinstance(arg, int):
                if arg < 0 or arg >= len(self.m_instances):
                    return

                handlers = self.m_buttonEventHandlers[arg]
                if handlers is None:
                    return

                handlers.Clear(args[0])
                button = self.SearchButtonInstanceByInstanceId(arg)
                if button is not None:
                    button: Button
                    button.SetHandlers(handlers)
            else:
                instId = self.SearchInstanceId(self.GetStringId(arg))

                if instId >= 0:
                    self.ClearButtonEventHandler(instId, args[0])
                    return

                if self.m_buttonEventHandlersByFullName is None:
                    return

                boolean, handlers = self.m_buttonEventHandlersByFullName.TryGetValue(arg)
                if not boolean:
                    return

                handlers.Clear(args[0])
                button = self.SearchButtonInstance(arg)
                if button is not None:
                    button: Button
                    button.SetHandlers(handlers)

    def SetButtonEventHandler(self, arg, load=None, unload=None, enterFrame=None, update=None,
                              render=None, press=None, release=None, rollOver=None, rollOut=None, keyPress=None):
        self.ClearButtonEventHandler(arg)
        return self.AddButtonEventHandler(arg, load, unload, enterFrame, update, render, press, release, rollOver,
                                          rollOut, keyPress)

    # class RendererFactory(IRendererFactory):
    #     def __init__(self, data, resourceCache, cache, stage, textInSubpixel, needsClear, quirkyClearRect):
    #         self.blendMode = "normal"
    #         self.maskMode = "normal"
    #         self.stage = stage
    #
    #         if stage.width == 0 and stage.height == 0:
    #             stage.width = data.header.width
    #             stage.height = data.header.height
    #
    #     def BeginRender(self, ctx):
    #         print("Pre-Render func")
    #
    #     def Render(self, ctx, cmd):
    #         print("Render me!")
    #
    #     def EndRender(self, ctx):
    #         print("Post render!")
    #
    # class ResourceCache:
    #     @staticmethod
    #     def get():
    #         return lwf.ResourceCache()
    #
    #     def __init__(self):
    #         self.cache = {}
    #         self.lwfInstanceIndex = 0
    #         self.canvasIndex = 0
    #
    #     def getRendererName(self):
    #         return "Canvas"
    #
    #     def newFactory(self, settings, cache, data):
    #         return lwf.RendererFactory(data, self, cache, settings['stage'],
    #                                settings['textInSubpixel'] if 'textInSubpixel'in settings else False,
    #                                settings['needsClear'] if 'needsClear'in settings else True,
    #                                settings['quirkyClearRect'] if 'quirkyClearRect' in settings else False)
    #
    #     def generateImages(self, settings, imageCache, texture, image):
    #         imageCache[texture.filename] = texture
    #         # super().generateImages(settings, imageCache, texture, image)
    #
    #     def LoadLWF(self, settings):
    #         lwfUrl = settings['prefix'] + settings['lwf']
    #         settings['error'] = []
    #         if lwfUrl in self.cache:
    #             return self.cache[lwfUrl]
    #         file = open(lwfUrl, 'rb').read()
    #         data = Data(file)
    #         self.cache[lwfUrl] = data
    #         settings['data'] = data
    #         onload = settings['onload']
    #         onload(settings)
    #         return

    class CustomImage:

        def __init__(self):
            self.source = ""
            self.data = None

        @staticmethod
        def load_image(cache, RCache, image, texture, url, settings, data):
            image.data = Image(source=url)

            cache[texture.filename] = image.data
            if texture.filename in settings['_alphaMap']:
                d = settings['_alphaMap'][texture.filename]
                jpg = d[0]
                alpha = d[1]
                jpgImg = cache[jpg.filename]
                alphaImg = cache[alpha.filename]
                if jpgImg and alphaImg:
                    (canvas, ctx) = RCache.createCanvas(jpgImg.width, jpgImg.height)
                    ctx.drawImage(jpgImg, 0, 0, jpgImg.width, jpgImg.height, 0, 0, jpgImg.width,
                                  jpgImg.height)
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
                RCache.loadImagesCallback(settings, cache, data)

    class CustomCanvas(Widget):
        # Every Custom Canvas will store every instruction in a InstructionGroup
        # This will allow us to pass a variety of arguments into draw Image
        def __init__(self):
            super().__init__()
            self.hasTransform = False
            self.group = InstructionGroup()
            self._group = InstructionGroup()
            self.globalCompositeOperation = "source-over"
            self.globalAlpha = 1
            self.style = {}
            self.backgroundColor = Color(0, 0, 0, 1)
            self.fillStyle = "#000000"  # can be a color #000000 or "gradient" or "pattern"

        def getContext(self):
            return self

        def setTransform(self, scaleX, skew1, skew0, scaleY, translateX, translateY):
            if skew1 != 0 or skew0 != 0:
                raise Exception("Skewing is not implemented!")
            if self.hasTransform:
                self.group.add(PopMatrix())
                self.hasTransform = False
            self.group.add(PushMatrix())
            self.hasTransform = True
            if scaleX != 1 or scaleY != 1:
                self.group.add(Scale(scaleX, scaleY, 0))
            if translateX != 0 or translateY != 0:
                self.group.add(Translate(translateX, translateY))

        def translate(self, x, y):
            if self.hasTransform:
                self.group.add(Translate(x, y))
            else:
                self.group.add(PushMatrix())
                self.hasTransform = True
                self.group.add(Translate(x, y))

        def fillRect(self, x, y, w, h):
            self.rect(x, y, w, h)

        def rect(self, x, y, w, h):  # should be the same as a fillRect
            if self.fillStyle == "pattern":
                # is an image pattern
                self.group.add(Rectangle(pos=(x, y), size=(w, h), source=self.pattern, tex_coords=self.tex_coords))
            elif self.fillStyle == "gradient":
                self.group.add(Rectangle(pos=(x, y), size=(w, h), texture=self.gradient, tex_coords=self.tex_coords))
            else:
                # is a color
                self.parseColor(self.fillStyle)
                self.group.add(Rectangle(pox=(x, y), size=(w, h)))
            self.draw()

        def clearRect(self, x, y, w, h):
            # use background color to write over
            print(self.style)

            if x <= 0 and y <= 0 and w >= self.width and h >= self.height:
                # Is a full Screen Clear, clean-up resources
                self.group = InstructionGroup()
                self._group = InstructionGroup()
                self.canvas.clear()
            self.group.add(self.backgroundColor)
            self.group.add(Rectangle(pos=(x, y), size=(w, h)))
            self.draw()

        # Removes the instructions from the buffer and adds them to the canvas
        def draw(self):
            for instruction in self.group.children:
                # We may have an extra bind texture for every InstructionGroup()
                # If it causes problems, then filter them out.
                print("Adding ", instruction, " to the canvas!")
                self.group.remove(instruction)
                self._group.add(instruction)
                self.canvas.add(instruction)

        def drawImage(self, *args):
            # img is either a canvas with instructions or a image
            if len(args) == 3:
                # img, x, y
                img = args[0]
                sx = 0
                sy = 0
                swidth = 1
                sheight = 1
                dx = args[1]
                dy = args[2]
                dwidth = img.width
                dheight = img.height
            elif len(args) == 5:
                # img, x, y, width, height
                img = args[0]
                sx = 0
                sy = 0
                swidth = 0
                sheight = 0
                dx = args[1]
                dy = args[2]
                dwidth = args[3]
                dheight = args[4]
            elif len(args) == 9:
                # img, sx, sy, sWidth, sHeight, dx, dy, dWidth, dHeight
                img = args[0]
                sx = self.normalize(args[1], img.width)
                sy = self.normalize(args[2], img.height)
                swidth = self.normalize(args[3], img.width)
                sheight = self.normalize(args[4], img.height)
                dx = args[5]
                dy = args[6]
                dwidth = args[7]
                dheight = args[8]
            else:
                raise Exception("Incorrect method call for draw image!")
            # now that we have our vars, we need to sort our composite and image types
            if isinstance(img, LWF.CustomCanvas):
                # I am not sure how to sscale these down. ???
                if sx >= 0 or sy >= 0 or swidth <= 1 or sheight <= 1:
                    raise Exception("Unsupported Canvas operation. Cannot Scale already drawn canvas instructions!")
                for instruction in LWF.CustomCanvas._group.children:
                    self.group.add(instruction)
            else:
                tex_coords = [sx, sy, sx + swidth, sy, sx + swidth, sy + sheight, sx, sy + sheight]
                # top-left, top-right, right, left
                self.group.add(
                    Rectangle(pos=(dx, dy), size=(dwidth, dheight), texture=img.texture, tex_coords=tex_coords))

            print(self.globalCompositeOperation + " was ignored!")
            # Do not currently do anything with self.globalCompositeOperation
            self.draw()

        def parseColor(self, color):
            # Once I have a base working with this method, change to use Color by default
            if re.match('#[0-9]{6}', color):
                # make a hex color to rgba
                self.group.add(KivyColor(int(color[1:3]), int(color[3:5]), int(color[5:7]), 1 * self.globalAlpha))
            elif re.match('rgb\([0-9](\.[0-9])?,[0-9](\.[0-9])?,[0-9](\.[0-9])?\)', color):
                r = re.match('[0-9](\.[0-9])?', color)
                g = re.match('[0-9](\.[0-9])?', color[len(r.string) + 1 + 4:])
                b = re.match('[0-9](\.[0-9])?', color[len(r.string) + len(g.string) + 2 + 4:])
                self.group.add(KivyColor(float(r.string), float(g.string), float(b.string), 1 * self.globalAlpha))
            elif re.match('rgba\([0-9](\.[0-9])?,[0-9](\.[0-9])?,[0-9](\.[0-9])?,[0-9](\.[0-9])?\)', color):
                r = re.match('[0-9](\.[0-9])?', color)
                g = re.match('[0-9](\.[0-9])?', color[len(r.string) + 1 + 5:])
                b = re.match('[0-9](\.[0-9])?', color[len(r.string) + len(g.string) + 2 + 5:])
                a = re.match('[0-9](\.[0-9])?', color[len(r.string) + len(g.string) + len(b.string) + 3 + 5])
                self.group.add(
                    KivyColor(float(r.string), float(g.string), float(b.string), float(a.string) * self.globalAlpha))
            else:
                raise Exception("The color/filltype is not supported/implemented!!! ", color)

        def createGradient(self, direction, *args):
            if direction == "horizontal":
                texture = Texture.create(size=(len(args), 1), colorfmt='rgba')
            elif direction == "vertical":
                texture = Texture.create(size=(len(args), 1), colorfmt='rgba')
            else:
                raise Exception("Unsupported gradient direction")
            buf = bytes([int(v * 255) for v in chain(*args)])  # flattens
            texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
            self.tex_coords = [0, 1, 1, 1, 1, 0, 0, 0]
            self.gradient = texture

        def createPattern(self, image, wrap):
            self.fillStyle = "pattern"
            image.wrap = wrap
            self.pattern = image
            self.tex_coords = [0, 1, 1, 1, 1, 0, 0, 0]

        def normalize(self, value, max):
            return value / max

    class RenderCommand:
        def __init__(self):
            self.renderCount = 0
            self.renderingIndex = 0
            self.alpha = 0
            self.blendMode = 0
            self.maskMode = 0
            self.matrix = None
            self.image = None
            self.pattern = None
            self.u = 0
            self.v = 0
            self.w = 0
            self.h = 0

    class BaseRenderCommand:
        def __init__(self):
            self.renderCount = 0
            self.renderingIndex = 0
            self.isBitmap = False
            self.renderer = None
            self.matrix = None
            self.maskMode = 0

    class BitmapContext:
        def __init__(self, factory, data, bitmapEx):
            self.factory = factory
            self.data = data
            self.fragment = self.data.textureFragments[bitmapEx.textureFragmentId]
            texture = self.data.textures[self.fragment.textureId]
            if isinstance(self.factory.cache, dict):
                self.image = self.factory.cache[texture.filename]
            else:
                self.image = self.factory.cache.cache[texture.filename]

            imageWidth = self.image.width
            withPadding = True if re.match('_withpadding', texture.filename) else False
            if withPadding:
                imageWidth -= 2
            imageScale = imageWidth / texture.width
            self.scale = 1 / (texture.scale * imageScale)

            repeat = None
            if (bitmapEx.attribute & Format.BitmapEx.Attribute.REPEAT_S.value) != 0:
                repeat = 'repeat-x'
            if (bitmapEx.attribute & Format.BitmapEx.Attribute.REPEAT_T.value) != 0:
                if repeat != None:
                    repeat = "repeat"
                else:
                    repeat = "repeat-y"
            if repeat is not None:
                # look up this function and what it does in javascript make a port
                self.pattern = self.factory.stageContext.createPattern(self.image, repeat)
            else:
                self.pattern = None

            x = self.fragment.x
            y = self.fragment.y
            u = self.fragment.u
            v = self.fragment.v
            w = self.fragment.w
            h = self.fragment.h

            if withPadding:
                x -= 1
                y -= 1
                w += 2
                h += 2

            bu = bitmapEx.u * w
            bv = bitmapEx.v * h
            bw = bitmapEx.w
            bh = bitmapEx.h

            x += bu
            y += bv
            u += bu
            v += bv
            w *= bw
            h *= bh

            self.x = round(x * imageScale)
            self.y = round(y * imageScale)
            self.u = round(u * imageScale)
            self.v = round(v * imageScale)
            if self.fragment.rotated:
                self.w = round(h * imageScale)
                self.h = round(w * imageScale)
            else:
                self.w = round(w * imageScale)
                self.h = round(h * imageScale)
            if self.u + self.w > self.image.width:
                self.w = self.image.width - self.u
            if self.v * self.h > self.image.height:
                self.h = self.image.height - self.v
            self.imageHeight = h * imageScale

    class BitmapRenderer:
        def __init__(self, context):
            self.context = context
            fragment = self.context.fragment
            self.matrix = Matrix(0, 0, 0, 0, 0, 0)
            if fragment.rotated or self.context.x != 0 or self.context.y != 0 or self.context.scale != 1:
                self.matrixForAtlas = Matrix()
            self.cmd = LWF.RenderCommand()

        def destruct(self):
            pass

        def render(self, m, c, renderingIndex, renderingCount, visible):
            if not visible or c.multi.alpha == 0:
                return

            if self.matrix.SetWithComparing(m):
                m = self.matrix
                fragment = self.context.fragment
                x = self.context.x
                y = self.context.y
                scale = self.context.scale
                if fragment.rotated:
                    m = Utility.RotateMatrix(self.matrixForAtlas, m, scale, x, y + self.context.imageHeight)
                elif scale != 1 or x != 0 or y != 0:
                    m = Utility.ScaleMatrix(self.matrixForAtlas, m, scale, x, y)
            else:
                if self.matrixForAtlas is not None:
                    m = self.matrixForAtlas
            self.alpha = c.multi.alpha

            f = self.context.factory.lwf.getRendererFactory()
            fragment = self.context.fragment
            cmd = self.cmd
            cmd.alpha = self.alpha
            cmd.blendMode = f.blendMode
            cmd.maskMode = f.maskMode
            cmd.matrix = m
            cmd.image = self.context.imageHeight
            cmd.pattern = self.context.pattern
            cmd.u = self.context.u
            cmd.v = self.context.v
            cmd.w = self.context.w
            cmd.h = self.context.h
            self.context.factory.addCommand(renderingIndex, cmd)
            return

    class TextContext:
        def __init__(self, factory, data, text):
            # not implemented. Do later.
            pass

    class TextRenderer:
        def __init__(self, lwf, context, text):
            pass  # implement later

    class DomElementRenderer:
        def __init__(self, factory, node):
            self.factory = factory
            self.node = node
            self.appended = False
            self.node.style.visibility = "hidden"
            self.matrix = Matrix(0, 0, 0, 0, 0, 0)
            self.matrixForDom = Matrix(0, 0, 0, 0, 0, 0)
            self.matrixForRender = Matrix(0, 0, 0, 0, 0, 0)
            self.alpha = -1
            self.zIndex = -1
            self.visible = False

        def destructor(self):
            if self.appended:
                self.factory.stage.parent.remove_widget(self.node)

        def destruct(self):
            if self.factory.resourceCache.constructor is LWF.BaseResourceCache:
                self.factory.destructRender(self)
            else:
                self.destructor()
            return

        def update(self, m, c):
            pass

        def render(self, m, c, renderingIndex, renderingCount, visible):
            if self.visible is visible:
                if visible is False:
                    return visible
            else:
                self.visible = visible
                if visible is False:
                    self.node.style.visibility = "hidden"
                    return
                else:
                    self.node.style.visibility = "visible"

            matrixChanged = self.matrix.SetWithComparing(m)
            if not matrixChanged and self.appended and self.alpha == c.multi.alpha and self.zIndex is renderingIndex + renderingCount:
                return

            if not self.appended:
                self.appended = True
                self.node.style.position = "absolute"
                self.node.style.webkitTransformOrigin = "0px 0px"
                self.node.style.display = "block"

            raise Exception("NOT IMPLEMENTED")

    class CanvasLoader:
        @staticmethod
        def load(d):
            if not d or not isinstance(d, bytes):
                return None
            option = d[Format.Constant.OPTION_OFFSET.value] & 0xff
            if option & Format.Constant.OPTION_COMPRESSED.value == 0:
                print("uncompressed")
                return Loader.load(d)
            # if compressed
            a = [0 for _ in range(len(d))]
            for i in range(0, len(d)):
                a[i] = d[i] & 0xff
            print("compressed")
            return Loader.loadArray(a)

        def loadArray(self, d):
            if not d:
                return None
            option = d[Format.Constant.OPTION_OFFSET.value]
            if (option & Format.Constant.OPTION_COMPRESSED.value) == 0:
                return Loader.loadArray(d)

            header = d[0:Format.Constant.HEADER_SIZE]
            compressed = d[Format.Constant.HEADER_SIZE:]
            # if compressed
            try:  # implement
                decompressed = LZMADecompressor.decompress(compressed)
            except Exception:
                return None
            d.header.append(decompressed)
            return Loader.loadArray(d)

    class BaseRendererFactory:
        def __init__(self, data, resourceCache, cache, stage, textInSubpixel, use3D, recycleTextCanvas,
                     quirkyClearRect):
            self.resourceCache = resourceCache
            self.cache = cache
            self.stage = stage
            self.texInSubpixel = textInSubpixel
            self.use3D = use3D
            self.recycleTextCanvas = recycleTextCanvas
            self.quirkyClearRect = quirkyClearRect
            self.needsRenderForInactive = True
            self.maskMode = "normal"
            self.commands = None

            self.bitmapContexts = []
            for bitmap in data.bitmaps:
                if bitmap.textureFragmentId == -1:
                    continue
                bitmapEx = Format.BitmapEx()
                bitmapEx.matrixId = bitmap.matrixId
                bitmapEx.textureFragmentId = bitmap.textureFragmentId
                bitmapEx.u = 0
                bitmapEx.v = 0
                bitmapEx.w = 1
                bitmapEx.h = 1
                bitmapEx.attribute = 0
                self.bitmapContexts.append(LWF.BitmapContext(self, data, bitmapEx))

            self.bitmapExContexts = []
            for bitmapEx in data.bitmapExs:
                if bitmapEx.textureFragmentId == -1:
                    continue
                self.bitmapExContexts.append(LWF.BitmapContext(self, data, bitmapEx))

            self.textContexts = []
            for text in data.texts:
                self.textContexts.append(LWF.TextContext(self, data, text))

            # style = self.stage.style
            (w, h) = self.getStageSize()
            if w == 0 and h == 0:
                self.stage.width = str(data.header.width)
                self.stage.height = str(data.header.height)

            self.initCommands()
            self.destructedRenderers = []

        def initCommands(self):
            if not self.commands or self.commandsCount < len(self.commands) * 0.75:
                self.commands = []
            self.commandsCount = 0
            self.subCommands = None
            return

        def isMask(self, cmd):
            if cmd.maskMode == "erase" or cmd.maskMode == "mask" or cmd.maskMode == "alpha":
                return True
            return False

        def isLayer(self, cmd):
            return cmd.maskMode == "layer"

        def addCommand(self, rIndex, cmd):
            cmd.renderCount = self.lwf.renderCount
            cmd.renderingIndex = rIndex
            if self.isMask(cmd):
                if self.subCommands:
                    self.subCommands[rIndex] = cmd
            else:
                if self.isLayer(cmd) and self.commandMaskMode != cmd.maskMode:
                    cmd.subCommands = []
                    self.subCommands = cmd.subCommands
                self.commands[rIndex] = cmd
                self.commandsCount += 1
            self.commandMaskMode = cmd.maskMode
            return

        def addCommandToParent(self, lwf):
            f = lwf.getRendererFactory()
            renderCount = lwf.renderCount
            for rIndex in range(0, len(self.commands)):
                cmd = self.commands[rIndex]
                if not cmd or cmd.renderingIndex != rIndex or cmd.renderCount != renderCount:
                    continue
                subCommands = cmd.subCommands
                cmd.subCommands = None
                f.addCommand(rIndex, cmd)
                if subCommands:
                    for srIndex in range(0, len(subCommands)):
                        scmd = subCommands[srIndex]
                        if not scmd or scmd.renderingIndex != srIndex or scmd.renderCount != renderCount:
                            continue
                        f.addCommand(srIndex, scmd)
            self.initCommands()
            return

        def destruct(self):
            if self.destructedRenderers:
                self.callRendererDestructor()
            for context in self.bitmapContexts:
                del context
            for context in self.bitmapExContexts:
                del context
            for context in self.textContexts:
                del context

        def init(self, lwf):
            self.lwf = lwf
            lwf.stage = self.stage
            lwf.resourceCache = self.resourceCache
            # if self.setupedDomElementConstructor:
            #     return
            # self.setupedDomElementConstructor = True
            for progObj in lwf.data.programObjects:
                name = lwf.data.strings[progObj.stringId]
                m = re.match('^DOM_(.*)', name)
                if m:
                    domName = m[1]

                    def do(domName):
                        def dom(lwf_, objId, w, h):
                            ctor = self.resourceCache.dolElementCOnstructor
                            if not ctor:
                                return None
                            domElement = ctor(lwf_, domName, w, h)
                            if not domElement:
                                return None
                            return LWF.DomElementRenderer(self, domElement)

                        lwf.setProgramObjectConstructor(name, dom)

                    do(domName)

        def destructRenderer(self, renderer):
            self.destructedRenderers.append(renderer)
            return

        def callRendererDestructor(self):
            for renderer in self.destructedRenderers:
                renderer.destructor()
            self.destructedRenderers = []
            return

        def beginRender(self, lwf):
            if self.destructedRenderers:
                self.callRendererDestructor()
            return

        def render(self, cmd):
            renderer = cmd.renderer
            node = renderer.node
            style = node.style
            style.zIndex = renderer.zIndex
            m = cmd.matrix

            if cmd.maskMode == "mask" or cmd.maskMode == "alpha":
                self.renderMasked = True
                style.opacity = 0
                if self.renderMaskMode != "mask" and self.renderMaskMode != "alpha":
                    if node.mask:
                        self.mask = node.mask
                        style = self.mask.style
                    else:
                        self.mask = node.mask = LWF.CustomCanvas()
                        style = self.mask.style
                        style.display = "block"
                        style.position = "absolute"
                        style.overflow = "hidden"
                        style.webkitUserSelect = "none"
                        style.webkitTransformOrigin = "0px 0px"
                        self.stage.append_widget(self.mask)
                    style.width = node.style.width
                    style.height = node.style.height
                    if not self.maskMatrix:
                        self.maskMatrix = Matrix()
                        self.maskedMatrix = Matrix()
                    Utility.InvertMatrix(self.maskMatrix, m)
                else:
                    return
            elif cmd.maskMode == "layer":
                if self.renderMasked:
                    if self.renderMaskMode != cmd.maskMode:
                        self.mask.style.zIndex = renderer.zIndex
                    if node.parent != self.mask:
                        node.parent.remove_widget(node)
                        self.mask.add_widget(node)
                    m = Utility.CalcMatrix(self.maskedMatrix, self.maskMatrix, m)
                else:
                    if node.parent != self.stage:
                        node.parent.remove_widget(node)
                        self.stage.add_widget(node)
            else:
                if node.parent != self.stage:
                    node.parent.remove_widget(node)
                    self.stage.add_widget(node)
            self.renderMaskMode = cmd.maskMode
            style.opacity = renderer.alpha
            scaleX = round(m.scaleX, 12)
            scaleY = round(m.scaleY, 12)
            skew1 = round(m.skew1, 12)
            skew0 = round(m.skew0, 12)
            translateX = round(m.translateX, 12)
            translateY = round(m.translateY, 12)
            if self.use3D:
                style.webkitTransform = "matrix3d(" + str(scaleX) + "," + str(skew1) + ",0,0," + str(skew0) + "," + str(
                    scaleY) + ",0,0,0,0,1,0," + str(translateX) + "," + str(translateY) + ",0,1)"
            else:
                style.webkitTransform = "matrix(" + str(scaleX) + "," + str(skew1) + "," + str(skew0) + "," + str(
                    scaleY) + "," + str(translateX) + "," + str(translateY)
            return

        def endRender(self, lwf):
            if lwf.parent:
                self.addCommandToParent(lwf)
                if self.destructedRenderers:
                    self.callRendererDestructor()
                return

            self.renderMaskMode = "normal"
            self.renderMasked = False
            renderCount = lwf.renderingCount
            for rIndex in range(0, len(self.commands)):
                cmd = self.commands[rIndex]
                if not cmd or cmd.renderingIndex != rIndex or cmd.renderCount != renderCount:
                    continue
                if cmd.subCommands:
                    for srIndex in range(0, len(cmd.subCommands)):
                        scmd = cmd.subCommands[srIndex]
                        if not scmd or scmd.renderingIndex != srIndex or scmd.renderCount != renderCount:
                            continue
                        self.render(scmd)
                    self.render(cmd)

                self.initCommands()

                if self.destructedRenderers:
                    self.callRendererDestructor()
                return

        def setBlendMode(self, blendMode):
            self.blendMode = blendMode

        def setMaskMode(self, maskMode):
            self.maskMode = maskMode

        def constructBitmap(self, lwf, objectId, bitmap):
            context = self.bitmapContexts[objectId]
            if context:
                return LWF.BitmapRenderer(context)
            return None

        def constructBitmapEx(self, lwf, objectId, bitmapEx):
            context = self.bitmapExContexts[objectId]
            if context:
                return LWF.BitmapRenderer(context)
            return None

        def constructText(self, lwf, objectId, text):
            context = self.textContexts[objectId]
            if context:
                return LWF.TextRenderer(lwf, context, text)

        def constructParticle(self, lwf, objectId, particle):
            ctor = self.resourceCache.particleConstructor
            particleData = lwf.data.particleDatas[particle.particleDataId]
            if ctor:
                return ctor(lwf, lwf.data.strings[particleData.stringId])
            return None

        def convertColor(self, lwf, d, c, t):
            Utility.CalcColor(d, c, t)
            d.red = round(d.red * 255)
            d.green = round(d.green * 255)
            d.blue = round(d.blue * 255)
            return

        def convertRGB(self, c):
            r = round(c.red * 255)
            g = round(c.green * 255)
            b = round(c.blue * 255)
            return "rgb(" + str(r) + "," + str(g) + "," + str(b) + ")"

        def getStageSize(self):
            r = self.getBoundingRect(self.stage)
            return (r.width, r.height)


        def getBoundingRect(self, widget):
            box = BoundingRect()
            box.width = widget.width
            box.height = widget.height
            box.x, box.y = widget.pos
            box.left = box.x
            box.top = box.y
            box.right = box.left + box.width
            box.bottom = box.top + box.height
            return box


        def fitForHeight(self, lwf):
            (w, h) = self.getStageSize()
            if h != 0 and h != lwf.data.header.height:
                lwf.fitForHeight(w, h)
            return

        def fitForWidth(self, lwf):
            (w, h) = self.getStageSize()
            if w != 0 and w != lwf.data.header.width:
                lwf.fitForWidth(w, h)
            return

        def scaleForHeight(self, lwf):
            (w, h) = self.getStageSize()
            if h != 0 and h != lwf.data.header.height:
                lwf.scaleForHeight(w, h)
            return

        def scaleForWidth(self, lwf):
            (w, h) = self.getStageSize()
            if w != 0 and w != lwf.data.header.width:
                lwf.scaleForWidth(w, h)
            return

        def parseBackgroundColor(self, v):
            if isinstance(v, float) or isinstance(v, int):
                bgColor = v
            elif isinstance(v, str):
                bgColor = int(v, 16)
            elif isinstance(v, LWF):
                lwf = v
                bgColor = lwf.data.header.backgroundColor
                bgColor |= 0xff << 24
            else:
                return 255, 255, 255, 255
            a = ((bgColor >> 24) & 0xff)
            r = ((bgColor >> 16) & 0xff)
            g = ((bgColor >> 8) & 0xff)
            b = ((bgColor >> 0) & 0xff)
            return r, g, b, a

        def setBackgroundColor(self, v):
            (r, g, b, a) = self.parseBackgroundColor(v)
            self.stage.style.backgroundColor = "rgba(" + str(r) + "," + str(g) + "," + str(b) + "," + str(a / 255) + ")"
            return

        def clearCanvasRect(self, canvas, ctx):
            ctx.clearRect(0, 0, canvas.width + 1, canvas.height + 1)
            if self.quirkyClearRect:
                canvas.width = canvas.width
            return

        def setFont(self, oldFontName, newFontName):
            oldFontName += ",sans-serif"
            newFontName += ",sans-serif"
            for context in self.textContexts:
                if context.fontName == oldFontName:
                    context.fontName = newFontName
                    context.fontChanged = True
            return

    class BaseResourceCache:
        _instance = None

        @staticmethod
        def get():
            if LWF.BaseResourceCache._instance is None:
                LWF.BaseResourceCache._instance = LWF.BaseResourceCache()
            return LWF.BaseResourceCache._instance

        def __init__(self):
            self.cache = {}
            self.lwfInstanceIndex = 0
            self.canvasIndex = 0

        def getRendererName(self):
            return "webkitCSS"

        def clear(self):
            for k, cache in self.cache:
                for kk, lwfInstance in cache.instances:
                    lwfInstance.destroy()
            self.cache = {}

        def getTextureURL(self, settings, data, texture):
            if 'imagePrefix' in settings:
                prefix = settings['imagePrefix']
            elif 'prefix' in settings:
                prefix = settings['prefix'];
            else:
                prefix = ""

            if 'imageSuffix' in settings:
                sufix = settings['imageSuffix']
            else:
                suffix = ""

            if 'imageQueryString' in settings:
                queryString = settings['imageQueryString']
            else:
                queryString = ""

            if len(queryString) > 0:
                queryString = "?" + queryString

            # imageMap = settings['imageMap']
            url = texture.filename
            # if callable(imageMap):
            #     newUrl = imageMap(settings, url)
            # if newUrl:
            #     url = newUrl
            # elif isinstance(imageMap, dict):
            #     newUrl = imageMap[url]
            #     if newUrl:
            #         url = newUrl
            if not (re.match('^/', url) or re.match('^https?://', url)):
                url = prefix + url
            url = url.replace('(\.gif|\.png|\.jpg)', suffix + "$1" + queryString)
            print("returning! ", url)
            return url

        def checkTextures(self, settings, data):
            settings['_alphaMap'] = {}
            settings['_colorMap'] = {}
            settings['_textures'] = []

            re_o = '_atlas(.*)_info_' + '([0-9])_([0-9]+)_([0-9]+)_([0-9]+)_([0-9]+)_([0-9]+)_([0-9]+)'
            re_rgb = '(.*)_rgb_([0-9a-f]{6})(.*)$'
            re_rgb10 = '(.*)_rgb_([0-9]*),([0-9]*),([0-9]*)(.*)$'
            re_rgba = '(.*)_rgba_([0-9a-f]{8})(.*)$'
            re_rgba10 = '(.*)_rgba_([0-9]*),([0-9]*),([0-9]*),([0-9]*)(.*)$'
            re_add = '(.*)_add_([0-9a-f]{6})(.*)$'
            re_add10 = '(.*)_add_([0-9]*),([0-9]*),([0-9]*)(.*)$'

            for texture in data.textures:
                orig = None
                if re.match(re_rgb, texture.filename):
                    m = re.match(re_rgb, texture.filename)
                    orig = m[1] + m[3]
                    colorOp = "rgb"
                    colorValue = m[2]
                elif re.match(re_rgb10, texture.filename):
                    m = re.match(re_rgb10, texture.filename)
                    orig = m[1] + m[5]
                    colorOp = "rgb"
                    r = hex(int(m[2], 10))[2:]
                    g = hex(int(m[3], 10))[2:]
                    b = hex(int(m[4], 10))[2:]
                    colorValue = ("0" if len(r) == 1 else "") + r + \
                                 ("0" if len(g) == 1 else "") + g + \
                                 ("0" if len(b) == 1 else "") + b
                elif re.match(re_rgba, texture.filename):
                    m = re.match(re_rgba, texture.filename)
                    orig = m[1] + m[3]
                    colorOp = "rgba"
                    colorValue = m[2]
                elif re.match(re_rgba10, texture.filename):
                    m = re.match(re_rgba10, texture.filename)
                    orig = m[1] + m[6]
                    colorOp = "rgba"
                    r = hex(int(m[2], 10))[2:]
                    g = hex(int(m[3], 10))[2:]
                    b = hex(int(m[4], 10))[2:]
                    a = hex(int(m[5], 10))[2:]
                    colorValue = ("0" if len(r) == 1 else "") + r + \
                                 ("0" if len(g) == 1 else "") + g + \
                                 ("0" if len(b) == 1 else "") + b + \
                                 ("0" if len(a) == 1 else "") + a
                elif re.match(re_add, texture.filename):
                    m = re.match(re_add, texture.filename)
                    orig = m[1] + m[3]
                    colorOp = "add"
                    colorValue = m[2]
                elif re.match(re_add10, texture.filename):
                    m = re.match(re_add10, texture.filename)
                    orig = m[1] + m[5]
                    colorOp = "add"
                    r = hex(int(m[2], 10))[2:]
                    g = hex(int(m[3], 10))[2:]
                    b = hex(int(m[4], 10))[2:]
                    colorValue = ("0" if len(r) == 1 else "") + r + \
                                 ("0" if len(g) == 1 else "") + g + \
                                 ("0" if len(b) == 1 else "") + b

                if orig:
                    ma = re.match(re_o, texture.filename)
                    if ma:
                        orig = ma[1]
                        rotated = ma[2] == "1"
                        u = int(ma[3], 10)
                        v = int(ma[4], 10)
                        w = int(ma[5], 10)
                        h = int(ma[6], 10)
                        x = int(ma[7], 10)
                        y = int(ma[8], 10)
                    else:
                        rotated = False
                        u = 0
                        v = 0
                        w = None
                        h = None
                        x = 0
                        y = 0
                    if orig not in settings['_colorMap']:
                        settings['_colorMap'][orig] = []
                        settings['_colorMap'][orig].append({
                            'filename': texture.filename,
                            'colorOp': colorOp,
                            'colorValue': colorValue,
                            'rotated': rotated,
                            'u': u,
                            'v': v,
                            'w': w,
                            'h': h,
                            'x': x,
                            'y': y
                        })
                        continue
                settings['_textures'].append(texture)
                m = re.match('^(.*)_withalpha(.*\.)jpg(.*)$', texture.filename)
                if m:
                    pngFilename = m[1] + "_alpha" + m[2] + "png" + m[3]
                    t = Format.TextureReplacement(pngFilename)
                    settings['_textures'].append(t)
                    settings['_alphaMap'][texture.filename] = [texture, t]
                    settings['_alphaMap'][t.filename] = [texture, t]
            return

        def onloaddata(self, settings, data, url):
            if not data or not data.Check():
                settings['error'].append({'url': url, 'reason': 'dataError'})
                settings['onload'](settings, None)
                return

            settings['name'] = data.name

            self.checkTextures(settings, data)

            # Assume we have no scripts
            needsToLoadScript = data.useScript #and !global['lwf]?['Script']?[data.name()]?

            self.cache[settings['lwfUrl']]['data'] = data
            settings['total'] = len(settings['_textures']) + 1
            # if needsToLoadScript:
            #   settings.total += 1
            settings['loadedCount'] = 1
            if 'onprogress' in settings:
                on_progress = settings['onprogress']
                on_progress(settings, settings['loadedCount'], settings['total'])

            # Assume that out lwfs require no scripts
            if needsToLoadScript:
                pass
            #   self.loadJs(settings, data)
            else:
                self.loadImages(settings, data)
            return

        def LoadLWF(self, settings):
            lwfUrl = settings['lwf']
            if not re.match('^/', lwfUrl):
                if 'prefix' in settings:
                    lwfUrl = settings['prefix'] + lwfUrl
            settings['lwfUrl'] = lwfUrl
            settings['error'] = []

            if lwfUrl in self.cache:
                data = self.cache[lwfUrl].data
                if data:
                    settings['name'] = data.name()
                    self.checkTextures(settings, data)
                    settings.total = len(settings._textures) + 1
                    settings.loadedCount = 1
                    if 'onprogress' in settings:
                        on_progress = settings['onprogress']
                        on_progress(settings, settings.loadedCount, settings.total)
                    self.loadImages(settings, data)
                    return
            self.cache[lwfUrl] = {}
            self.loadLWFData(settings, lwfUrl)

            # file = open(lwfUrl, "rb")
            # data = Data(file.read())
            # self.cache[lwfUrl] = data
            # settings['data'] = data
            # onload = settings['onload']
            # onload(settings)
            # return

        def dispatchOnloaddata(self, settings, url, data):
            data = LWF.CanvasLoader.load(data)
            print(data)

            self.onloaddata(settings, data, url)

        def loadLWFData(self, settings, url):
            self.dispatchOnloaddata(settings, url, open(url, 'rb').read())

        def loadImagesCallback(self, settings, imageCache, data):
            print("Images loaded callback!")
            settings['loadedCount'] += 1
            if settings['loadedCount'] is settings['total']:
                print("All images loaded!")
                del settings['_alphaMap']
                del settings['_colorMap']
                del settings['_textures']
                if len(settings['error']) > 0:
                    del self.cache[settings['lwf']]
                    on_load = settings['onload']
                    on_load(settings, None)
                else:
                    self.newLWF(settings, imageCache, data)
            else:
                print("\nNot all loaded!")
            return

        def drawImage(self, ctx, image, o, u, v, w, h):
            if o.rotates:
                m = Matrix()
                Utility.RotateMatrix(m, Matrix(), 1, 0, w)
                ctx.setTransform(m.scaleX, m.skew1, m.skew0, m.scaleY, m.translateX, m.translateY)
            else:
                ctx.setTransform(1, 0, 0, 1, 0, 0)
            ctx.drawImage(image, u, v, w, h, 0, 0, w, h)
            ctx.setTransform(1, 0, 0, 1, 0, 0)
            return

        def getCanvasName(self):
            self.canvasIndex += 1
            return "__canvas__" + str(self.canvasIndex)

        def createCanvas(self, w, h):
            name = self.getCanvasName()
            canvas = LWF.CustomCanvas()
            canvas.width = w
            canvas.height = h
            ctx = canvas.getContext()
            canvas.name = name
            return (canvas, ctx)

        def generateImages(self, settings, imageCache, texture, image):
            d = settings._colorMap[texture.filename]
            if d:
                scaleX = image.width / texture.width
                scaleY = image.height / texture.height
                for o in d:
                    u = round(o.u * scaleX)
                    v = round(o.v * scaleY)
                    w = round((o.w if o.w else texture.width) * scaleX)
                    h = round((o.h if o.h else texture.height) * scaleY)
                    if o.rotated:
                        iw = h
                        ih = w
                    else:
                        iw = w
                        ih = h
                    (canvas, ctx) = self.createCanvas(w, h)

                    if o.colorOp == "rgb":
                        ctx.fillStyle = "#" + str(o.colorValue)
                        ctx.fillRect(0, 0, w, h)
                        ctx.globalCompositeOperation = "destination-in"
                        self.drawImage(ctx, image, o, u, v, iw, ih)
                    elif o.colorOp == "rgba":
                        self.drawImage(ctx, image, o, u, v, iw, ih)
                        ctx.globalCompositeOperation = "source-atop"
                        val = o.colorValue
                        r = int(val[0:2], 16)
                        g = int(val[2:2], 16)
                        b = int(val[4:2], 16)
                        a = int(val[6:2], 16) / 255
                        ctx.fillStyle = "rgba(" + str(r) + ", " + str(g) + ", " + str(b) + ", " + str(a) + ")"
                        ctx.fillRect(0, 0, w, h)
                    elif o.colorOp == "add":
                        canvasAdd = LWF.CustomCanvas()
                        canvasAdd.width = w
                        canvasAdd.height = h
                        ctxAdd = canvasAdd.getContext()
                        ctxAdd.fillStyle = "#" + str(o.colorValue)
                        ctxAdd.fillRect(0, 0, w, h)
                        ctxAdd.globalCompositeOperation = "destination-in"
                        self.drawImage(ctxAdd, image, o, u, v, iw, ih)
                        self.drawImage(ctx, image, o, u, v, iw, ih)
                        ctx.globalCompositeOperation = "lighter"
                        ctx.drawImage(canvasAdd, 0, 0, canvasAdd.width, canvasAdd.height, 0, 0, canvasAdd.width,
                                      canvasAdd.height)
                    ctx.globalCompositeOperation = "source-over"
                    imageCache[o.filename] = canvas
            return

        def loadImages(self, settings, data):
            imageCache = {}

            if len(data.textures) == 0:
                self.newLWF(settings, imageCache, data)
                return

            for texture in settings['_textures']:
                url = self.getTextureURL(settings, data, texture)

                image = LWF.CustomImage()
                try:
                    LWF.CustomImage.load_image(imageCache, self, image, texture, url, settings, data)
                except Exception:
                    settings['error'].append({'url': url, 'reason': "error"})
                self.loadImagesCallback(settings, imageCache, data)
            print("Finished Loading images!")
            return

        def newFactory(self, settings, cache, data):

            return LWF.BaseRendererFactory(data, self, cache, settings['stage'],
                                       settings['textInSubpixel'] if 'textInSubPixel' in settings else False,
                                       settings['use3D'] if 'use3D' in settings else False,
                                       settings['recycleTextCanvas'] if 'recycleTextCanvas' in settings else False,
                                       settings['quirkyClearRect'] if 'quirkyClearRect' in settings else False)

        def onloadLWF(self, settings, lwf):
            factory = lwf.rendererFactory
            print("On Load!")
            if 'setBackgroundColor' in settings:
                factory.setBackgroundColor(settings['setBackgroundColor'])
            elif 'useBackgroundColor' in settings:
                factory.setBackgroundColor(lwf)
            if 'fitForHeight' in settings:
                factory.fitForHeight(lwf)
            elif 'fitForWidth' in settings:
                factory.fitForWidth(lwf)
            on_load = settings['onload']
            on_load(settings, lwf)
            return

        def newLWF(self, settings, imageCache, data):
            lwfUrl = settings['lwfUrl']
            cache = self.cache[lwfUrl]
            factory = self.newFactory(settings, imageCache, data)
            # ignoring scripts
            # embeddedScript = global["lwf"]?["Script"]?[data.name()] if data.useScript
            lwf = LWF(data, factory)
            if 'active' in settings:
                lwf.active = settings['active']
            lwf.url = settings['lwfUrl']
            self.lwfInstanceIndex += 1
            lwf.lwfInstanceId = self.lwfInstanceIndex
            if 'instances' not in cache:
                cache['instances'] = {}
            cache['instances'][lwf.lwfInstanceId] = lwf
            if 'parentLWF' in settings:
                parentLWF = settings['parentLWF']
                parentLWF.loadedLWFs[lwf.lwfInstanceId] = lwf
            if 'preferredFrameRate' in settings:
                if 'execLimit' in settings:
                    lwf.SetPreferredFrameRate(settings['preferredFrameRate'], settings['execLimit'])
                else:
                    lwf.SetPreferredFrameRate(settings['preferredFrameRate'])
            self.onloadLWF(settings, lwf)
            return

        def unloadLWF(self, lwf):
            cache = self.cache[lwf.url]
            if cache:
                if lwf.lwfInstanceId:
                    del cache.instances[lwf.lwfInstanceId]
                    empty = True
                    for k, v in cache.instances:
                        empty = False
                        break
                    if empty:
                        # we ignore scripts
                        #     try:
                        #         if cache.scripts:
                        #             head = document.getElementsByTagName('head')[0]
                        #             for script in cache.scripts
                        #                 head.removeChild(script)
                        #     catch e
                        del self.cache[lwf.url]
            return

        def loadLWFs(self, settingsArray, onloadall):
            loadTotal = len(settingsArray)
            loadedCount = 0
            errors = None
            for settings in settingsArray:
                onload = settings['onload']

                def do(onload):
                    def on_load(lwf):
                        if onload:
                            onload(lwf)
                        if len(settings.error) > 0:
                            if errors is not None:
                                errors = []
                            errors = errors.append(settings.error)
                        loadedCount += 1
                        if loadTotal == loadedCount:
                            onloadall(errors)

                    settings['onload'] = on_load

                do(onload)
                self.LoadLWF(settings)

        def getCache(self):
            return self.cache

        def setParticleConstructor(self, ctor):
            self.particleConstructor = ctor
            return

        # We do not use DOM elements. No need for this
        # def setDOMElementCOnstructor(self, ctor):
        #     self.domElementConstructor = ctor
        #     return

    class RendererFactory(BaseRendererFactory):
        def __init__(self, data, resourceCache, cache, stage, textInSubpixel, needsClear, quirkyClearRect):
            self.resourceCache = resourceCache
            self.cache = cache
            self.stage = stage
            self.textInSubPixel = textInSubpixel
            self.needsClear = needsClear
            self.quirkyClearRect = quirkyClearRect
            self.blendMode = "normal"
            self.maskMode = "normal"

            self.stageContext = self.stage.getContext()
            if self.stage.width == 0 and self.stage.height == 0:
                self.stage.width = data.header.width
                self.stage.height = data.header.height

            self.bitmapContexts = []
            for bitmap in data.bitmaps:
                if bitmap.textureFragmentId == -1:
                    continue
                bitmapEx = Format.BitmapEx()
                bitmapEx.matrixId = bitmap.matrixId
                bitmapEx.textureFragmentId = bitmap.textureFragmentId
                bitmapEx.u = 0
                bitmapEx.v = 0
                bitmapEx.w = 1
                bitmapEx.h = 1
                bitmapEx.attribute = 0
                self.bitmapContexts.append(LWF.BitmapContext(self, data, bitmapEx))

            self.bitmapExContexts = []
            for bitmapEx in data.bitmapExs:
                if bitmapEx.textureFragmentId == -1:
                    continue
                self.bitmapExContexts.append(LWF.BitmapContext(self, data, bitmapEx))

            self.textContexts = []
            for text in data.texts:
                self.textContexts.append(LWF.TextContext(self, data, text))

            self.initCommands()

        def destruct(self):
            for context in self.bitmapContexts:
                del context
            for context in self.bitmapExContexts:
                del context
            for context in self.textContexts:
                del context
            return

        def setBlendMode(self, blendMode):
            self.blendMode = blendMode

        def setMaskMode(self, maskMode):
            self.maskMode = maskMode

        def constructBitmap(self, lwf, objectId, bitmap):
            context = self.bitmapContexts[objectId]
            if context:
                return LWF.BitmapRenderer(context)
            return None

        def constructBitmapEx(self, lwf, objectId, bitmapEx):
            context = self.bitmapExContexts[objectId]
            if context:
                return LWF.BitmapRenderer(context)
            return None

        def constructText(self, lwf, objectId, text):
            context = self.textContexts[objectId]
            if context:
                return TextRenderer(lwf, context, text)
            return None

        def constructParticle(self, lwf, objectId, particle):
            ctor = self.resourceCache.particleConstructor
            particleData = lwf.data.particleDatas[particle.particleDataId]
            if ctor:
                return ctor(lwf, lwf.data.strings[particleData.stringId])

        def getStageSize(self):
            return (self.stage.width, self.stage.height)

        def setBackgroundColor(self, v):
            r, g, b, a = self.parseBackgroundColor(v)
            self.clearColor = "rgba(" + str(r) + "," + str(g) + "," + str(b) + "," + str(a / 255) + ")"
            return

        def resetGlobalCompositeOperation(self, ctx):
            ctx.globalCompositeOperation = "source-over"
            self.renderBlendMode = "normal"
            return

        def setGlobalCompositeOperation(self, ctx, blendMode):
            if self.renderBlendMode != blendMode:
                self.renderBlendMode = blendMode
                if self.renderBlendMode == "add":
                    ctx.globalCompositeOperation = "lighter"
                elif self.renderBlendMode == "normal":
                    ctx.globalCompositeOperation = "source-over"
            return

        def renderMask(self, blendMode):
            print("Boss! I'm rendering a mask!")
            ctx = self.maskCanvas.getContext()
            ctx.globalCompositeOperation = self.maskComposition
            self.renderBlendMode = None
            ctx.setTransform(1, 0, 0, 1, 0, 0)
            ctx.drawImage(self.layerCanvas, 0, 0, self.layerCanvas.width, self.layerCanvas.height, 0, 0,
                          self.layerCanvas.width, self.layerCanvas.height)

            ctx = self.stageContext
            self.setGlobalCompositeOperation(ctx, blendMode)
            ctx.setTransform(1, 0, 0, 1, 0, 0)
            ctx.drawImage(self.maskCanvas, 0, 0, self.maskCanvas.width, self.maskCanvas.height, 0, 0,
                          self.maskCanvas.width, self.maskCanvas.height)
            return

        def render(self, ctx, cmd):
            print("Boss! I'm rendering!")
            if self.renderMaskMode != cmd.maskMode:
                if cmd.maskMode == "erase" or cmd.maskMode == "mask" or cmd.maskMode == "alpha":
                    if self.renderMaskMode == "layer" and self.renderMasked:
                        self.renderMask(cmd.blendMode)
                    self.renderMasked = True
                    if cmd.maskMode == "erase":
                        self.maskComposition = "source-out"
                    else:
                        self.maskComposition = "source-in"
                    if not self.maskCanvas:
                        self.maskCanvas = LWF.CustomCanvas()
                        self.maskCanvas.width = self.stage.width
                        self.maskCanvas.height = self.stage.height
                        cleared = True
                    else:
                        cleared = False
                    ctx = self.maskCanvas.getContext()
                    self.resetGlobalCompositeOperation(ctx)
                    if not cleared:
                        ctx.setTransform(1, 0, 0, 1, 0, 0)
                        self.clearCanvasRect(self.stage, ctx)
                elif cmd.maskMode == "layer":
                    if self.renderMasked:
                        if not self.layerCanvas:
                            self.layerCanvas = LWF.CustomCanvas()
                            self.layerCanvas.width = self.stage.width
                            self.layerCanvas.height = self.stage.height
                            cleared = True
                        else:
                            cleared = False
                        ctx = self.layerCanvas.getContext()
                        self.resetGlobalCompositeOperation(ctx)
                        if not cleared:
                            ctx.setTransform(1, 0, 0, 1, 0, 0)
                            self.clearCanvasRect(self.stage, ctx)
                    else:
                        ctx = self.stageContext
                        self.resetGlobalCompositeOperation(ctx)
                elif cmd.maskMode == "normal":
                    ctx = self.stageContext
                    self.resetGlobalCompositeOperation(ctx)
                    if self.renderMaskMode == "layer" and self.renderMasked:
                        self.renderMask(self.renderBlendMode)
                self.renderMaskMode = cmd.maskMode
            self.setGlobalCompositeOperation(ctx, cmd.blendMode)
            if cmd.alpha != 1:
                ctx.globalAlpha = cmd.alpha
            m = cmd.matrix
            ctx.setTransform(m.scaleX, m.skew1, m.skew0, m.scaleY, m.translateX, m.translateY)
            u = cmd.u
            v = cmd.v
            w = cmd.w
            h = cmd.h
            if cmd.pattern and (w > cmd.image.width or h > cmd.image.height):
                ctx.fillStyle = cmd.pattern
                ctx.translate(-u, -v)
                ctx.rect(u, v, w, h)
            else:
                ctx.drawImage(cmd.image, u, v, w, h, 0, 0, w, h)
            if cmd.alpha != 1:
                ctx.globalAlpha = 1
            return ctx

        def endRender(self, lwf):
            print("Ending my render boss!")
            ctx = self.stageContext
            if lwf.parent:
                self.addCommandToParent(lwf)
                return

            if self.needsClear:
                ctx.setTransform(1, 0, 0, 1, 0, 0)
                if self.clearColor:
                    if self.clearColor[3] == 'a':
                        self.clearCanvasRect(self.stage, ctx)
                    ctx.fillStyle = self.clearColor
                    ctx.fillRect(0, 0, self.stage.width, self.stage.height)
                else:
                    self.clearCanvasRect(self.stage, ctx)

            ctx.globalAlpha = 1
            self.resetGlobalCompositeOperation(ctx)
            self.renderMaskMode = "normal"
            self.renderMasked = False
            renderCount = lwf.renderCount
            for rIndex in range(0, len(self.commands)):
                cmd = self.commands[rIndex]
                if not cmd or cmd.renderingIndex != rIndex or cmd.renderCount != renderCount:
                    continue
                if cmd.subCommands:
                    for srIndex in range(0, len(cmd.subCommands)):
                        scmd = cmd.subCommands[srIndex]
                        if not scmd or scmd.renderingIndex != srIndex or scmd.renderCount != renderCount:
                            continue
                        ctx = self.render(ctx, scmd)
                ctx = self.render(ctx, cmd)
            if self.renderMaskMode == "layer" and self.renderMasked:
                self.renderMask(self.renderBlendMode)
            self.initCommands()
            return

    class ResourceCache(BaseResourceCache):

        def getRendererName(self):
            return "Canvas"

        def newFactory(self, settings, cache, data):
            return LWF.RendererFactory(data, self, cache, settings['stage'],
                                       settings['textInSubpixel'] if 'textInSubpixel' in settings else False,
                                       settings['needsClear'] if 'needsClear' in settings else True,
                                       settings['quirkyClearRect'] if 'quirkyClearRect' in settings else False)

        def generateImages(self, settings, imageCache, texture, image):
            m = re.match('_withpadding', texture.filename)
            if m:
                w = image.width + 2
                h = image.height + 2
                canvas = LWF.CustomCanvas()
                canvas.width = 2
                canvas.height = h
                canvas.name = self.getCanvasName()
                ctx = canvas.getContext()
                canvas.widthPadding = True
                ctx.drawImage(image, 0, 0, image.width, image.height, 1, 1, image.width, image.height)
                imageCache[texture.filename] = canvas
            super().generateImages(settings, imageCache, texture, image)
            return



