__all__ = ('ProgramObject',)

from .object import Object
from ..format.object_data import PROGRAM_OBJECT


class ProgramObject(Object):
    def __init__(self, lwf, p, obj_id):
        super().__init__(lwf, p, PROGRAM_OBJECT, obj_id)

        data = lwf.data.program_objects[obj_id]
        self.data_matrix_id = data.matrix_id

        ctor = lwf.get_program_object_constructor(obj_id)
        if ctor:
            self.renderer = ctor(self, obj_id, data.width, data.height)

    def update(self, m, c):
        super().update(m, c)
        if self.renderer:
            self.renderer.update(self.matrix, self.color_transform)
