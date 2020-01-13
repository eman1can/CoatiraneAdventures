# Internal Imports
from .utils.Type import Matrix
from .utils.Utility import Utility

from .ResourceCache import BaseResourceCache
from .Format import Format

# External Imports
import re

# Lots of code below is still experimental and may/will need to be changed
# Most code below is a direct port and doesn't port the logic, meaning it will break immediately


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
        if (bitmapEx.attribute & Format.BitmapEx.Attribute.REPEAT_S) != 0:
            repeat = 'repeat-x'
        if (bitmapEx.attribute & Format.BitmapEx.Attribute.REPEAT_T) != 0:
            if repeat is not None:
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





