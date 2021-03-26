# Kivy Imports
from kivy.properties import BooleanProperty, NumericProperty, OptionProperty

from kivy.uix.relativelayout import RelativeLayout
# KV Import
from loading.kv_loader import load_kv

load_kv(__name__)


class CustomSlot(RelativeLayout):
    type = OptionProperty('strength', options=['strength', 'magic', 'endurance', 'dexterity', 'agility'])
    locked = BooleanProperty(False)
    hover = BooleanProperty(False)
    value = NumericProperty(0.0)

    def __init__(self, **kwargs):
        self.register_event_type('on_unlock')
        super().__init__(**kwargs)

    def _do_press(self):
        if not self.toggle_enabled:
            self.state = 'down'
        else:
            if self.locked:
                self.dispatch('on_unlock')

    def on_unlock(self, *args):
        pass

    def unlock_slot(self):
        self.locked = False
        self.disabled = True
