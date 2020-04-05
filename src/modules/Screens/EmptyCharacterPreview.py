from kivy.input.providers.wm_touch import WM_MotionEvent
from kivy.properties import ObjectProperty, BooleanProperty

from src.modules.KivyBase.Hoverable import ScreenH as Screen


class EmptyCharacterPreviewScreen(Screen):
    preview = ObjectProperty(None)
    locked = BooleanProperty(False)
    do_hover = BooleanProperty(True)

    def __init__(self, **kwargs):
        self._touch = None
        super().__init__(**kwargs)

    def is_valid_touch(self):
        return self.preview.portfolio.is_current()

    def on_mouse_pos(self, hover):
        if not self.collide_point(*hover.pos):
            return False
        if not self.do_hover:
            return False
        if self.ids.button.dispatch('on_mouse_pos', hover):
            return True

    def update_lock(self, locked):
        self.locked = locked
        if self.locked:
            self.ids.lock.opacity = 1
        else:
            self.ids.lock.opacity = 0

    def on_button_touch_down(self, instance, touch):
        if instance.collide_point(*touch.pos):
            if not self.locked:
                touch.grab(self)

    def on_button_touch_up(self, instance, touch):
        if touch.grab_current == self and not self.locked:
            touch.ungrab(self)
            if self.is_valid_touch():
                if isinstance(touch, WM_MotionEvent):
                    touch.button = 'left'
                if touch.button != 'left' or self.preview.is_disabled:
                    return True
                self.preview.show_select_screen(self, False)
                return True
