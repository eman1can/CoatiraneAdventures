# Internal Imports
from .Bitmap import Bitmap
from .BitmapEx import BitmapEx
from .Object import Object
from .Text import Text
from ..Format import Format


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
