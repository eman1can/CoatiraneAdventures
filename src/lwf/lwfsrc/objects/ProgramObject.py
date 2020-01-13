# Internal Imports
from ..utils.Type import Action

from ..objects.Object import Object

from ..Format import Format


class ProgramObjectConstructor(Action):
    pass


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
