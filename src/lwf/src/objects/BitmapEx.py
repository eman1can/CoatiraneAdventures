class BitmapEx(Object):
    def __init__(self, lwf, parent, objId):
        super().__init__(lwf, parent, Format.Object.Type.BITMAPEX, objId)
        self.m_dataMatrixId = lwf.data.bitmapExs[objId].matrixId
        self.m_renderer = lwf.rendererFactory.ConstructBitmapEx(lwf, objId, self)
