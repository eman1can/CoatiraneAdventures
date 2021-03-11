# UIX Imports
# Kivy Imports
from kivy.properties import BooleanProperty, ObjectProperty

# KV Import
from loading.kv_loader import load_kv
from uix.modules.screen import Screen

load_kv(__name__)


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

    def on_button(self, *args):
        if self.locked:
            return
        if self.preview.is_disabled:
            return
        if not self.is_valid_touch():
            return
        self.preview.show_select_screen(self, False)
