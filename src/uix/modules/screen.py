# Kivy Imports
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty

from kivy.clock import Clock
from kivy.uix.screenmanager import Screen as ScreenBase
# KV Import
from loading.kv_loader import load_kv
from refs import Refs

load_kv(__name__)


class Screen(ScreenBase):
    background_source = StringProperty('background.png')
    background = BooleanProperty(True)

    title_source = StringProperty('')

    title_hidden = BooleanProperty(False)
    back_hidden = BooleanProperty(False)
    back_enabled = BooleanProperty(True)
    home_hidden = BooleanProperty(False)
    home_enabled = BooleanProperty(True)

    content = ObjectProperty(None)

    def __init__(self, **kwargs):
        self.content = Refs.gc
        super().__init__(**kwargs)

    def reload(self, *args, **kwargs):
        pass

    def on_back_press(self):
        self.manager.display_screen(None, False, False)

    def on_home_press(self):
        self.manager.display_screen('town_main', True, False)


