from kivy.properties import ObjectProperty, BooleanProperty

from src.modules.KivyBase.Hoverable import ScreenBase as Screen


class EmptyCharacterPreviewScreen(Screen):
    preview = ObjectProperty(None)
    locked = BooleanProperty(False)
    do_hover = BooleanProperty(True)

    def is_valid_touch(self):
        return self.preview.portfolio.is_current()

    def update_lock(self, locked):
        self.locked = locked
        if self.locked:
            self.ids.lock.opacity = 1
        else:
            self.ids.lock.opacity = 0

    def on_button_touch_down(self, instance, touch):
        if not instance.collide_point(*touch.pos):
            return False
        if self.locked:
            return False
        touch.grab(self)
        return True

    def on_button_touch_up(self, instance, touch):
        if touch.grab_current is None:
            return False
        if touch.grab_current != self:
            return False
        if self.preview.is_disabled:
            return False
        if self.locked:
            return False
        if self.is_valid_touch():
            if touch.is_touch:
                touch.button = 'left'
            if touch.button == 'left':
                self.preview.show_select_screen(self, False)
                return True
        return False
