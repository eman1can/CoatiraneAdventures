# Internal Imports
from .utils.CustomCanvas import CustomCanvas
from .utils.Utility import Utility
from .utils.Type import Matrix

from .Renderer import BitmapContext, TextContext, DomElementRenderer, BitmapRenderer
from .Format import Format
from .LWF import LWF

# External Imports
from kivy.uix.widget import Widget
import re


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

