__all__ = ('IObject',)

from .object import Object
from ..format.object import Object as ObjectType


class IObject(Object):
    def __init__(self, *args):
        self.alive = False
        self.instance_id = 0
        self.i_object_id = 0
        self.name = None
        self.prev_instance = None
        self.next_instance = None
        self.link_instance = None

        if len(args) > 0:
            lwf, p, t, obj_id, inst_id = args
            super().__init__(lwf, p, t, obj_id)

            self.alive = True
            self.instance_id = -1 if inst_id >= len(lwf.data.instance_names) else inst_id
            self.i_object_id = lwf.get_i_object_offset()

            self.prev_instance = 0
            self.next_instance = 0
            self.link_instance = 0

            if self.instance_id >= 0:
                string_id = lwf.get_instance_name_string_id(self.instance_id)
                if string_id != -1:
                    self.name = lwf.data.strings[string_id]

                head = lwf.get_instance(self.instance_id)
                if head:
                    head.prev_instance = self
                self.next_instance = head
                lwf.set_instance(self.instance_id, self)
        else:
            super().__init__()

    def destroy(self):
        if self.type is not ObjectType.ATTACHED_MOVIE and self.instance_id >= 0:
            head = self.lwf.get_instance(self.instance_id)
            if head == self:
                self.lwf.set_instance(self.instance_id, self.next_instance)
            if self.next_instance:
                self.next_instance.prev_instance = self.prev_instance
            if self.prev_instance is not None:
                self.prev_instance.next_instance = self.next_instance

        super().destroy()
        self.alive = False

    def link_button(self):
        pass

    def get_full_name(self):
        full_path = ""
        splitter = ""
        o = self
        while o:
            if o.name is None:
                return ""
            full_path = o.name + splitter + full_path
            if splitter == "":
                splitter = "."
            o = o.parent
        return full_path
