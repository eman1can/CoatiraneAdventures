# Kivy Imports
from kivy.properties import ListProperty, NumericProperty

from kivy.uix.buttonversions import PPCHoverPathToggleButton
from kivy.uix.relativelayout import RelativeLayout
# KV Import
from kivy.uix.togglebutton import ToggleButton
from loading.kv_loader import load_kv

load_kv(__name__)


class PartyIndexerButton(PPCHoverPathToggleButton):
    index = NumericProperty(0)


class PartyIndexer(RelativeLayout):
    count = NumericProperty(10)
    index = NumericProperty(0)

    def __init__(self, **kwargs):
        self.register_event_type('on_button')
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        for index in range(self.count):
            button = PartyIndexerButton(index=index, pos_hint={'center_x': (index + 0.5) * (1 / self.count)})
            self.ids[str(index)] = button
            self.add_widget(button)
        self.ids[str(self.index)].state = 'down'

    def on_button(self, index):
        pass

    def select_index(self, index):
        self.ids[str(self.index)].state = 'normal'
        self.index = index
        self.ids[str(index)].state = 'down'
