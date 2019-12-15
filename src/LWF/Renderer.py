from src.LWF.lwf import Data, LWF, IRendererFactory,Format, Color, Utility, Matrix

from kivy.graphics.instructions import Canvas



from kivy.graphics import Color as KivyColor
from kivy.core.window import Window
import os

from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics.texture import Texture
from itertools import chain
from kivy.graphics import PushMatrix, PopMatrix, InstructionGroup, Scale, Translate, Rectangle
from lzma import LZMADecompressor
import re


class CustomImage:
    src = None
    def __init__(self):
        self.source = ""
        self.onerror = None
        self.onload = None

    @src.setter
    def src(self, newSrc):
        self.source = newSrc
        self.load_image()

    def load_image(self):
        try:
            self.data = Image(source=self.source)
        except Exception:
            if self.onerror is not None:
                self.onerror()
        if self.onload is not None:
            self.onload()


class CustomCanvas(Widget):
    #Every Custom Canvas will store every instruction in a InstructionGroup
    #This will allow us to pass a variety of arguments into draw Image
    def __init__(self):
        super().__init__()
        self.hasTransform = False
        self.group = InstructionGroup()
        self._group = InstructionGroup()
        self.globalCompositeOperation = "source-over"
        self.globalAlpha = 1
        self.style = {}
        self.backgroundColor = Color(0, 0, 0, 1)
        self.fillStyle = "#000000" #can be a color #000000 or "gradient" or "pattern"

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

    def rect(self, x, y, w, h): #should be the same as a fillRect
        if self.fillStyle == "pattern":
            #is an image pattern
            self.group.add(Rectangle(pos=(x, y), size=(w, h), source=self.pattern, tex_coords=self.tex_coords))
        elif self.fillStyle == "gradient":
            self.group.add(Rectangle(pos=(x, y), size=(w, h), texture=self.gradient, tex_coords=self.tex_coords))
        else:
            #is a color
            self.parseColor(self.fillStyle)
            self.group.add(Rectangle(pox=(x, y), size=(w, h)))
        self.draw()

    def clearRect(self, x, y, w, h):
        # use background color to write over
        print(self.style)

        if x <= 0 and y <= 0 and w >= self.width and h >= self.height:
            #Is a full Screen Clear, clean-up resources
            self.group = InstructionGroup()
            self._group = InstructionGroup()
            self.canvas.clear()
        self.group.add(self.backgroundColor)
        self.group.add(Rectangle(pos=(x, y), size=(w, h)))
        self.draw()

    #Removes the instructions from the buffer and adds them to the canvas
    def draw(self):
        for instruction in self.group.children:
            #We may have an extra bind texture for every InstructionGroup()
            #If it causes problems, then filter them out.
            print("Adding ", instruction, " to the canvas!")
            self.group.remove(instruction)
            self._group.add(instruction)
            self.canvas.add(instruction)

    def drawImage(self, *args):
        # img is either a canvas with instructions or a image
        if len(args) == 3:
            #img, x, y
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
            #img, x, y, width, height
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
            #img, sx, sy, sWidth, sHeight, dx, dy, dWidth, dHeight
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
        #now that we have our vars, we need to sort our composite and image types
        if isinstance(img, CustomCanvas):
            #I am not sure how to sscale these down. ???
            if sx >= 0 or sy >= 0 or swidth <= 1 or sheight <= 1:
                raise Exception("Unsupported Canvas operation. Cannot Scale already drawn canvas instructions!")
            for instruction in CustomCanvas._group.children:
                self.group.add(instruction)
        else:
            tex_coords = [sx, sy, sx+swidth, sy, sx+swidth, sy+sheight, sx, sy+sheight]
            #top-left, top-right, right, left
            self.group.add(Rectangle(pos=(dx, dy), size=(dwidth, dheight), texture=img.texture, tex_coords=tex_coords))

        print(self.globalCompositeOperation + " was ignored!")
        #Do not currently do anything with self.globalCompositeOperation
        self.draw()

    def parseColor(self, color):
        #Once I have a base working with this method, change to use Color by default
        if re.match('#[0-9]{6}', color):
            #make a hex color to rgba
            self.group.add(Color(int(color[1:3]), int(color[3:5]), int(color[5:7]), 1  * self.globalAlpha))
        elif re.match('rgb\([0-9](\.[0-9])?,[0-9](\.[0-9])?,[0-9](\.[0-9])?\)', color):
            r = re.match('[0-9](\.[0-9])?', color)
            g = re.match('[0-9](\.[0-9])?', color[len(r.string)+1+4:])
            b = re.match('[0-9](\.[0-9])?', color[len(r.string)+len(g.string)+2+4:])
            self.group.add(Color(float(r.string), float(g.string), float(b.string), 1  * self.globalAlpha))
        elif re.match('rgba\([0-9](\.[0-9])?,[0-9](\.[0-9])?,[0-9](\.[0-9])?,[0-9](\.[0-9])?\)', color):
            r = re.match('[0-9](\.[0-9])?', color)
            g = re.match('[0-9](\.[0-9])?', color[len(r.string) + 1 + 5:])
            b = re.match('[0-9](\.[0-9])?', color[len(r.string) + len(g.string) + 2 + 5:])
            a = re.match('[0-9](\.[0-9])?', color[len(r.string) + len(g.string) + len(b.string) + 3 + 5])
            self.group.add(Color(float(r.string), float(g.string), float(b.string), float(a.string) * self.globalAlpha))
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
        self.image = self.factory.cache[texture.filename]
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
            #look up this function and what it does in javascript make a port
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
        self.cmd = RenderCommand()

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
        #not implemented. Do later.
        pass


class TextRenderer:
    def __init__(self, lwf, context, text):
        pass #implement later


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
        if self.factory.resourceCache.constructor is BaseResourceCache:
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
        if not d or not isinstance(d, str):
            return None
        option = d[Format.Constant.OPTION_OFFSET.value] & 0xff
        if option & Format.Constant.OPTION_COMPRESSED == 0:
            return Loader.load(d)
        #if compressed
        a = [0 for _ in range(len(d))]
        for i in range(0, len(d)):
            a[i] = d[i] & 0xff
        return Loader.loadArray(a)

    def loadArray(self, d):
        if not d:
            return None
        option = d[Format.Constant.OPTION_OFFSET.value]
        if (option & Format.Constant.OPTION_COMPRESSED.value) == 0:
            return Loader.loadArray(d)

        header = d[0:Format.Constant.HEADER_SIZE]
        compressed = d[Format.Constant.HEADER_SIZE:]
        #if compressed
        try:#implement
            decompressed = LZMADecompressor.decompress(compressed)
        except Exception:
            return None
        d.header.append(decompressed)
        return Loader.loadArray(d)


class BaseRendererFactory:
    def __init__(self, data, resourceCache, cache, stage, textInSubpixel, use3D, recycleTextCanvas, quirkyClearRect):
        self.resourceCache = resourceCache
        self.cache = cache
        self.stage = stage
        self.texInSubpixel = textInSubpixel
        self.use3D = use3D
        self.recycleTExtCanvas = recycleTextCanvas
        self.quirkyClearRect = quirkyClearRect
        self.needsRenderForInactive = True
        self.maskMode = "normal"

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
            self.bitmapContexts.append(BitmapContext(self, data, bitmapEx))

        self.bitmapExContexts = []
        for bitmapEx in data.bitmapExs:
            if bitmapEx.textureFragmentId == -1:
                continue
            self.bitmapExContexts.append(BitmapContext(self, data, bitmapEx))

        self.textContexts = []
        for text in data.texts:
            self.textContexts.append(TextContext(self, data, text))

        style = self.stage.style
        (w, h) = self.getStageSize()
        if w == 0 and h == 0:
            style.width = str(data.header.width) + "px"
            style.height = str(data.header.height) + "px"

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
        if self.setupedDomElementConstructor:
            return
        self.setupedDomElementConstructor = True
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
                        return DomElementRenderer(self, domElement)
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
        print("render")
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
                    self.mask = node.mask = Widget()
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
            style.webkitTransform = "matrix3d(" + str(scaleX) + "," + str(skew1) + ",0,0," + str(skew0) + "," + str(scaleY) + ",0,0,0,0,1,0," + str(translateX) + "," + str(translateY) + ",0,1)"
        else:
            style.webkitTransform = "matrix(" + str(scaleX) + "," + str(skew1) + "," + str(skew0) + "," + str(scaleY) + "," + str(translateX) + "," + str(translateY)
        return

    def endRender(self, lwf):
        if lwf.parent:
            self.addCommandToParent(lwf)
            if self.destructedRenderers:
                self.callRendererDestructor()
            return

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
            return BitmapRenderer(context)
        return None

    def constructBitmapEx(self, lwf, objectId, bitmapEx):
        context = self.bitmapExContexts[objectId]
        if context:
            return BitmapRenderer(context)
        return None

    def constructText(self, lwf, objectId, text):
        context = self.textContexts[objectId]
        if context:
            return TextRenderer(lwf, context, text)

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
        r = self.stage.getCoundingClientRect()
        return (r.width, r.height)

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
        settings._alphaMap = {}
        settings._colorMap = {}
        settings._textures = []

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
                if orig not in settings._colorMap:
                    settings._colorMap[orig] = []
                    settings._colorMap[orig].append({
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
                settings._textures.append(texture)
                m = re.match('^(.*)_withalpha(.*\.)jpg(.*)$', texture.filename)
                if m:
                    pngFilename = m[1] + "_alpha" + m[2] + "png" + m[3]
                    t = Format.TextureReplacement(pngFilename)
                    settings._textures.append(t)
                    settings._alphaMap[texture.filename] = [texture, t]
                    settings._alphaMap[t.filename] = [texture, t]
        return

    def onloaddata(self, settings, data, url):
        if not data and data.check():
            settings.error.append({'url': url, 'reason': 'dataError'})
            settings['onload'](settings, None)
            return

        settings['name'] = data.name()

        self.checkTextures(settings, data)

        #Assume we have no scripts
        needsToLoadScript = data.useScript #and !global['LWF]?['Script']?[data.name()]?

        self.cache[settings['lwfUrl']].data = data
        settings.total = len(settings._textures) + 1
        # if needsToLoadScript:
        #   settings.total += 1
        settings.loadedCount = 1
        if 'onprogress' in settings:
            on_progress = settings['onprogress']
            on_progress(settings, settings.loadedCount, settings.total)

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

        # data = Data(file)
        # self.cache[lwfUrl] = data
        # settings['data'] = data
        # onload = settings['onload']
        # onload(settings)
        # return

    def dispatchOnloaddata(self, settings, url, data):
        data = CanvasLoader.load(data.data)
        print(data)

        self.onloaddata(settings, data, url)

    def loadLWFData(self, settings, url):
        self.dispatchOnloaddata(settings, url, open(url, 'rb').read())

    def loadImagesCallback(self, settings, imageCache, data):
        settings.loadedCount += 1
        if 'onprogress' in settings:
            on_progress = settings['onprogress']
            on_progress(settings, settings.loadedCount, settings.total)
        if settings.loadedCount is settings.total:
            del settings._alphaMap
            del settings._colorMap
            del settings._textures
            if len(settings.error) > 0:
                del self.cache[settings['lwf']]
                on_load = settings['onload']
                on_load(settings, None)
            else:
                self.newLWF(settings, imageCache, data)
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
        canvas = CustomCanvas()
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
                    canvasAdd = CustomCanvas()
                    canvasAdd.width = w
                    canvasAdd.height = h
                    ctxAdd = canvasAdd.getContext()
                    ctxAdd.fillStyle = "#" + str(o.colorValue)
                    ctxAdd.fillRect(0, 0, w, h)
                    ctxAdd.globalCompositeOperation = "destination-in"
                    self.drawImage(ctxAdd, image, o, u, v, iw, ih)
                    self.drawImage(ctx, image, o, u, v, iw, ih)
                    ctx.globalCompositeOperation = "lighter"
                    ctx.drawImage(canvasAdd, 0, 0, canvasAdd.width, canvasAdd.height, 0, 0, canvasAdd.width, canvasAdd.height)
                ctx.globalCompositeOperation = "source-over"
                imageCache[o.filename] = canvas
        return

    def loadImages(self, settings, data):
        imageCache = {}

        if len(data.textures) == 0:
            self.newLWF(settings, imageCache, data)
            return

        for texture in settings._textures:
            url = self.getTextureURL(settings, data, texture)
            def do(texture, url):
                image = CustomImage()
                def onabort():
                    settings.error.append({'url':url, 'reason':"abort"})
                    image = image.onload = image.onabort = image.onerror = None
                    self.loadImagesCallback(settings, imageCache, data)
                image.onabort = onabort
                def onerror():
                    settings.error.append({'url': url, 'reason': "error"})
                    image = image.onload = image.onabort = image.onerror = None
                    self.loadImagesCallback(settings, imageCache, data)
                image.onerror = onerror
                def onload():
                    imageCache[texture.filename] = image.data
                    d = settings._alphaMap[texture.filename]
                    if d:
                        jpg = d[0]
                        alpha = d[1]
                        jpgImg = imageCache[jpg.filename]
                        alphaImg = imageCache[alpha.filename]
                        if jpgImg and alphaImg:
                            (canvas, ctx) = self.createCanvas(jpgImg.width, jpgImg.height)
                            ctx.drawImage(jpgImg, 0, 0, jpgImg.width, jpgImg.height, 0, 0, jpgImg.width, jpgImg.height)
                            ctx.globalCompositeOperation = "destination-in"
                            ctx.drawImage(alphaImg, 0, 0, alphaImg.width, alphaImg.height, 0, 0, jpgImg.width, jpgImg.height)
                            ctx.globalCompositeOperation = "source-over"
                            del imageCache[jpg.filename]
                            del imageCache[alpha.filename]
                            imageCache[jpg.filename] = canvas
                            self.generateImages(settings, imageCache, jpg, canvas)
                        else:
                            self.generateImages(settings, imageCache, texture, image.data)

                        image = image.onload = image.onabort = image.onerror = None
                        self.loadImagesCallback(settings, imageCache, data)
                image.onload = onload
                image.src = url
            do(texture, url)
        return

    def newFactory(self, settings, cache, data):
        return BaseRendererFactory(data, self, cache, settings['stage'],
                                   settings['textInSubpixel'] if 'textInSubPixel' in settings else False,
                                   settings['use3D'] if 'use3D' in settings else False,
                                   settings['recycleTextCanvas'] if 'recycleTextCanvas' in settings else False,
                                   settings['quirkyClearRect'] if 'quirkyClearRect' in settings else False)

    def onloadLWF(self, settings, lwf):
        factory = lwf.rendererFactory
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

    def newLWF(self, settings, imageCache, data):
        lwfUrl = settings['lwfUrl']
        cache = self.cache['lwfUrl']
        factory = self.newFactory(settings, imageCache, data)
        #ignoring scripts
        #embeddedScript = global["LWF"]?["Script"]?[data.name()] if data.useScript
        lwf = LWF(data, factory)
        if 'active' in settings:
            lwf.active = settings['active']
        lwf.url = settings['lwfUrl']
        self.lwfInstanceIndex += 1
        lwf.lwfInstanceId = self.lwfInstanceIndex
        if cache.instances is None:
            cache.instances = {}
        cache.instances[lwf.lwfInstanceId] = lwf
        parentLWF = settings['parentLWF']
        if parentLWF:
            parentLWF.loadedLWFs[lwf.lwfInstanceId] = lwf
        if 'preferredFrameRate' in settings:
            pass
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
            self.bitmapContexts.append(BitmapContext(self, data, bitmapEx))

        self.bitmapExContexts = []
        for bitmapEx in data.bitmapExs:
            if bitmapEx.textureFragmentId == -1:
                continue
            self.bitmapExContexts.append(BitmapContext(self, data, bitmapEx))

        self.textContexts = []
        for text in data.texts:
            self.textContexts.append(TextContext(self, data, text))

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
            return BitmapRenderer(context)
        return None

    def constructBitmapEx(self, lwf, objectId, bitmapEx):
        context = self.bitmapExContexts[objectId]
        if context:
            return BitmapRenderer(context)
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
        ctx.drawImage(self.layerCanvas, 0, 0, self.layerCanvas.width, self.layerCanvas.height, 0, 0, self.layerCanvas.width, self.layerCanvas.height)

        ctx = self.stageContext
        self.setGlobalCompositeOperation(ctx, blendMode)
        ctx.setTransform(1, 0, 0, 1, 0, 0)
        ctx.drawImage(self.maskCanvas, 0, 0, self.maskCanvas.width, self.maskCanvas.height, 0, 0, self.maskCanvas.width, self.maskCanvas.height)
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
                    self.maskCanvas = CustomCanvas()
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
                        self.layerCanvas = CustomCanvas()
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
            canvas = CustomCanvas()
            canvas.width = 2
            canvas.height = h
            canvas.name = self.getCanvasName()
            ctx = canvas.getContext()
            canvas.widthPadding = True
            ctx.drawImage(image, 0, 0, image.width, image.height, 1, 1, image.width, image.height)
            imageCache[texture.filename] = canvas
        super().generateImages(settings, imageCache, texture, image)
        return
