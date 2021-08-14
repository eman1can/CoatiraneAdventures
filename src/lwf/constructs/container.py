__all__ = ('LWFContainer',)

from .button import Button


class LWFContainer(Button):
    def __init__(self, p, c):
        super().__init__()

        self.lwf = p.lwf
        self.parent = p
        self.child = c

        self.alive = True
        self.instance_id = -1
        self.i_object_id = self.lwf.get_i_object_offset()

        self.prev_instance = None
        self.next_instance = None
        self.link_instance = None

    def check_hit(self, px, py):
        button = self.child.input_point(px, py)
        return button is not None

    def roll_over(self):
        pass

    def roll_out(self):
        if self.child.focus:
            self.child.focus.roll_out()
            self.child.clear_focus(self.child.focus)

    def press(self):
        self.child.input_press()

    def release(self):
        self.child.input_release()

    def key_press(self, code):
        self.child.input_key_press(code)
