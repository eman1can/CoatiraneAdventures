# Internal Imports
from .Object import Object
from ..Format import Format


class Bitmap(Object):
    def __init__(self, lwf, parent, objId):
        super().__init__(lwf, parent, Format.Object.Type.BITMAP, objId)
        self.m_dataMatrixId = lwf.data.bitmaps[objId].matrixId
        self.m_renderer = lwf.rendererFactory.ConstructBitmap(lwf, objId, self)
