__all__ = ('Button',)

from .button_event_handlers import ButtonEventHandlers
from .iobject import IObject
from ..format.button import ButtonCondition as BC
from ..format.object import Object as ObjectType
from ..tools.utility import Utility
from ..type import Matrix


class Button(IObject):
    def __init__(self, *args):
        self.data = None
        self.button_link = None
        self.hit_x = 0.0
        self.hit_y = 0.0
        self.width = 0.0
        self.height = 0.0

        self._m_invert = Matrix()
        self._handler = ButtonEventHandlers()

        if len(args) > 0:
            l, p, obj_id, inst_id, m_id, c_id = args
            super().__init__(l, p, ObjectType.BUTTON, obj_id, inst_id)

            self.matrix_id = m_id
            self.color_transform_id = c_id

            self.hit_x = -2147483648
            self.hit_y = -2147483648

            if obj_id >= 0:
                self.data = self.lwf.data.buttons[obj_id]
                self.data_matrix_id = self.data.matrix_id
                self.width = self.data.width
                self.height = self.data.height
            else:
                self.data = None
                self.width = 0
                self.height = 0

            self.button_link = None

            self._handler.add(self.lwf.get_button_event_handlers(self))
            if not self._handler.empty():
                self._handler.call(ButtonEventHandlers.LOAD, self)

    def add_handlers(self, h):
        self._handler.add(h)

    def exec(self, m_id=0, c_id=0):
        super().exec(m_id, c_id)
        self.enter_frame()

    def update(self, m, c):
        super().update(m, c)

        if not self._handler.empty():
            self._handler.call(ButtonEventHandlers.UPDATE, self)

    def render(self, v, r_offset):
        if v and not self._handler.empty():
            self._handler.call(ButtonEventHandlers.RENDER, self)

    def destroy(self):
        self.lwf.clear_focus(self)
        self.lwf.clear_pressed(self)

        if not self._handler.empty():
            self._handler.call(ButtonEventHandlers.UNLOAD, self)

        super().destroy()

    def link_button(self):
        if self.lwf.focus == self:
            self.lwf.focus_on_link = True
        self.button_link = self.lwf.button_head
        self.lwf.button_head = self

    def check_hit(self, px, py):
        Utility.invert_matrix(self._m_invert, self.matrix)
        x, y = Utility.calc_matrix_to_point(px, py, self._m_invert)
        if 0.0 <= x < self.data.width and 0.0 <= y < self.data.height:
            self.hit_x = x
            self.hit_y = y
            return True
        self.hit_x = -2147483648
        self.hit_y = -2147483648
        return False

    def enter_frame(self):
        if not self._handler.empty():
            self._handler.call(ButtonEventHandlers.ENTER_FRAME, self)

    def roll_over(self):
        if not self._handler.empty():
            self._handler.call(ButtonEventHandlers.ROLL_OVER, self)

        self.play_animation(BC.Condition.ROLL_OVER)

    def roll_out(self):
        if not self._handler.empty():
            self._handler.call(ButtonEventHandlers.ROLL_OUT, self)

        self.play_animation(BC.Condition.ROLL_OUT)

    def press(self):
        if not self._handler.empty():
            self._handler.call(ButtonEventHandlers.PRESS, self)

        self.play_animation(BC.Condition.PRESS)

    def release(self):
        if not self._handler.empty():
            self._handler.call(ButtonEventHandlers.RELEASE, self)

        self.play_animation(BC.Condition.RELEASE)

    def key_press(self, code):
        if not self._handler.empty():
            self._handler.call_key_press(self, code)

        self.play_animation(BC.Condition.KEY_PRESS, code)

    def play_animation(self, condition, code=0):
        if not self.data:
            return

        for i in range(0, self.data.conditions):
            c = self.data.conditions[self.data.condition_id + i]
            if (c.condition & condition) != 0 and (condition != BC.Condition.KEY_PRESS or c.key_code == code):
                self.lwf._play_animation(c.animation_id, self.parent, self)

    def add_event_handler(self, event_name, event_handler):
        event_id = self.lwf.get_event_offset()
        if self._handler.add(event_id, event_name, event_handler):
            return event_id
        return -1

    def remove_event_handler(self, event_name, event_id):
        self._handler.remove(event_id)

    def remove_button_event_handler(self, event_id):
        self._handler.remove(event_id)

    def clear_event_handler(self, event_name):
        self._handler.clear(event_name)

    def clear_button_event_handler(self):
        self._handler.clear()

    def clear_all_event_handler(self):
        self._handler.clear()

    def set_event_handler(self, event_name, event_handler):
        self.clear_event_handler(event_name)
        return self.add_event_handler(event_name, event_handler)
