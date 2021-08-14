__all__ = ('Text',)

from .object import Object
from ..format.object import Object as ObjectType


class Text(Object):
    def __init__(self, lwf, p, obj_id, inst_id=-1):
        self.name = None
        self.set_text_renderer = False

        super().__init__(lwf, p, ObjectType.TEXT, obj_id)

        text = lwf.data.texts[obj_id]
        self.data_matrix_id = text.matrix_id

        if text.name_string_id != -1:
            self.name = lwf.data.strings[text.name_string_id]
        else:
            if 0 <= inst_id < len(lwf.data.instance_names):
                string_id = lwf.get_instance_name_string_id(inst_id)
                if string_id != -1:
                    self.name = lwf.data.strings[string_id]

        text_renderer = lwf.renderer_factory.construct_text(lwf, obj_id, self)
        if text_renderer:
            t = None
            if text.string_id != -1:
                t = lwf.data.strings[text.string_id]

            if text.name_string_id == -1 and self.name is None:
                if text.string_id != -1:
                    text_renderer.set_text(t)
            else:
                lwf.set_text_renderer(p.get_full_name(), self.name, t, text_renderer)
                self.set_text_renderer = True

        self.renderer = text_renderer

    def destroy(self):
        if self.set_text_renderer:
            full_name = self.parent.get_full_name()
            if full_name:
                self.lwf.clear_text_renderer(full_name + '.' + self.name)
            self.lwf.clear_text_renderer(self.name)
        super().destroy()