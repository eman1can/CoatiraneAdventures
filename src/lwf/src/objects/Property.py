# Internal Imports
from ..utils.Type import Matrix, ColorTransform
from ..utils.Constants import INT32_MINVALUE

# External imports
import math


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
