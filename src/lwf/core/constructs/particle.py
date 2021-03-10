__all__ = ('Particle',)

from .object import Object
from ..format import Object as ObjectType


class Particle(Object):
    def __init__(self, lwf, p, obj_id):
        super().__init__(lwf, p, ObjectType.PARTICLE, obj_id)

        self.data_matrix_id = lwf.data.particles[obj_id].matrix_id
        self.renderer = lwf.renderer_factory.construct_particle(lwf, obj_id, self)

    def update(self, m, c):
        super().update(m, c)
        if self.renderer:
            self.renderer.update(self.matrix, self.color_transform)
