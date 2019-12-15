from src.LWF import Renderer
from src.LWF.Renderer import ResourceCache
from src.LWF.lwf import Format, LWF

class Factory(Renderer.Factory):
    m_bitmapContexts = None
    m_bitmapExContexts = None

    def __init__(self, d, canvas, zOff, zR, rQOff, sLayerName=None, sOrder=0, uAC=False, texturePrfx="", fontPrfx="",
                 textureLdr=None,textureUnldr=None,shaderName="LWF"):
        super().__init__(d, canvas, zOff, zR, rQOff, sLayerName, sOrder, uAC,
                         texturePrfx, fontPrfx, textureLdr, textureUnldr, shaderName)
        self.CreateBitmapContexts()
        self.CreateTextContexts()

    def Destruct(self):
        self.DestructBitmapContexts()
        self.DestructTextContexts()

        super().Destruct()

    def ConstructBitmap(self, lwf, objectId, bitmap):
        return self.BitMapRenderer(lwf, self.m_bitmapContexts[objectId])

    def ConstructBitmapEx(self, lwf, objectId, bitmapEx):
        return self.BitMapRenderer(lwf, self.m_bitmapExContexts[objectId])

    def ConstructText(self, lwf, objectId, text):
        return self.TextRenderer(lwf, self.m_textContexts[objectId])

    def CreateBitmapContexts(self):
        self.m_bitmapContexts = [BitmapContext() for _ in range(len(self.data.bitmaps))]
        for i in range(0, len(self.data.bitmaps)):
            bitmap = self.data.bitmaps[i]
            if bitmap.textureFragmentId == -1:
                continue
            bitmapExId = -i - 1
            bitmapEx = Format.BitmapEx()
            bitmapEx.matrixId = bitmap.matrixId
            bitmapEx.textureFragmentId = bitmap.textureFragmentId
            bitmapEx.u = 0
            bitmapEx.v = 0
            bitmapEx.w = 1
            bitmapEx.h = 1
            self.m_bitmapContexts[i] = BitmapContext(self, self.data, bitmapEx, bitmapExId)

        self.m_bitmapExContexts = [BitmapContext() for _ in range(len(self.data.bitmapExs))]
        for i in range(0, len(self.data.bitmapExs)):
            bitmapEx = self.data.bitmapExs[i]
            if bitmapEx.textureFragmentId == -1:
                continue
            self.m_bitmapExContexts[i] = BitmapContext(self, self.data, bitmapEx, i)

    def DestructBitmapContexts(self):
        for i in range(0, len(self.m_bitmapContexts)):
            if self.m_bitmapContexts[i] is not None:
                self.m_bitmapContexts[i].Destruct()
        for i in range(0, len(self.m_bitmapExContexts)):
            if self.m_bitmapExContexts[i] is not None:
                self.m_bitmapExContexts[i].Destruct()


class BitmapContext:
    m_factory = None
    m_material = None
    m_mesh = None
    m_data = None
    m_height = 0.0
    m_textureName = None
    m_bitmapExId = 0
    m_premultipliesAlpha = False

    @property
    def factory(self):
        return self.m_factory

    @@property
    def material(self):
        return self.m_material

    @property
    def mesh(self):
        return self.m_mesh

    @property
    def data(self):
        return self.m_data

    @property
    def textureName(self):
        return self.m_textureName

    @property
    def height(self):
        return self.m_height

    @property
    def bitmapExId(self):
        return self.m_bitmapExId

    @property
    def premultipliedAlpha(self):
        return self.m_premultipliesAlpha

    def __init__(self, f, d, bitmapEx, bId):
        self.m_factory = f
        self.m_data = d
        self.m_bitmapExId = bId

        fragment = self.data.textureFragments[bitmapEx.textureFragmentId]
        texture = self.data.textures[fragment.textureId]

        self.m_textureName = self.factory.texturePrefix + texture.filename
        if LWF.GetTextureLoadHandler() is not None:
            self.m_textureName =  LWF.GetTextureLoadHandler()(self.m_textureName, self.factory.texturePrefix, texture.filename)

        self.m_premultipliesAlpha = texture.format == int(Format.Constant.TEXTUREFORMAT_PREMULTIPLIEDALPHA.value)
        self.m_material = ResourceCache.SharedInstance().LoadTexture(self.data.name, self.m_textureName, texture.format, self.factory.useAdditionalCOlor, self.factory.textureLoader, self.factory.texureUnloader, self.factory.shaderName)

