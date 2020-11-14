# Internal Imports
from ..Format import Format
from ..objects.Object import Object


class Particle(Object):
    def __init__(self, lwf, parent, objId):
        super().__init__(lwf, parent, Format.Object.Type.PARTICLE, objId)
        self.m_dataMatrixId = lwf.data.particles[objId].matrixId
        self.m_renderer = lwf.rendererFactory.ConstructParticle(lwf, objId, self)

    def Update(self, m, c):
        super().Update(m, c)
        if self.m_renderer is not None:
            self.m_renderer.Update(self.m_matrix, self.m_colorTransform)
