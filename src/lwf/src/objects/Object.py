# Internal Imports
from ..utils.Type import Matrix, ColorTransform
from ..utils.Constants import INT32_MINVALUE
from ..utils.Utility import Utility

from ..Format import Format


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
