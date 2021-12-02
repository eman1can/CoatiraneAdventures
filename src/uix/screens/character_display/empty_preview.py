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

    displayed = BooleanProperty(False)
    support_displayed = BooleanProperty(False)

    def __init__(self, **kwargs):
        self.register_event_type('on_select')
        super().__init__(**kwargs)
        self.on_displayed()

    def __eq__(self, other):
        if other is None:
            return False
        if isinstance(other, str):
            return self.name == other
        if isinstance(other, Screen):
            return self.name == other.name
        return False

    def on_button(self, *args):
        if self.locked or self.disabled:
            return
        self.dispatch('on_select', False)

    def on_select(self, is_support):
        pass

    def close_hints(self):
        pass

    def on_locked(self, *args):
        self.update_visible()

    def on_displayed(self, *args):
        self.update_visible()

    def update_visible(self):
        status = self.locked or not self.displayed
        self.opacity = 1 - int(status)
        self.disabled = status
