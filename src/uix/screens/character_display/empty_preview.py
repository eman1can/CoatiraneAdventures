# UIX Imports
# Kivy Imports
from kivy.properties import BooleanProperty, ObjectProperty

# KV Import
from loading.kv_loader import load_kv
from uix.modules.screen import Screen

load_kv(__name__)


class EmptyCharacterPreviewScreen(Screen):
    locked = BooleanProperty(False)
    current = BooleanProperty(False)
    do_hover = BooleanProperty(True)

    def __init__(self, **kwargs):
        self.register_event_type('on_select')
        self.name = 'empty'
        super().__init__(**kwargs)

    def __eq__(self, other):
        if other is None:
            return False
        if isinstance(other, str):
            return self.name == other
        if isinstance(other, Screen):
            return self.name == other.name
        return False

    def update_lock(self, locked):
        self.locked = locked

    def on_button(self, *args):
        if self.locked:
            return
        # if not self.current:
        #     return
        self.dispatch('on_select', False)

    def on_select(self, is_support):
        pass

    def close_hints(self):
        pass