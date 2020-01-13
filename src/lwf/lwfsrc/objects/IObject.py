# Internal Imports
from .Object import Object

from ..Format import Format

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

    @staticmethod
    def Clear_Array(array, si, ei):
        for x in range(si, ei):
            if isinstance(array[x], IObject):
                array[x] = IObject()
            else:
                raise Exception("Not Implemented!")
