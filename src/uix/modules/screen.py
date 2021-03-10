# Kivy Imports
from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty
from kivy.uix.screenmanager import Screen as ScreenBase

# KV Import
from loading.kv_loader import load_kv
load_kv(__name__)


class Screen(ScreenBase):
    background_source = StringProperty('backgrounds/background.png')
    background = BooleanProperty(True)

    content = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.initialize_data, 0)

    def initialize_data(self, dt):
        pass

    def reload(self, *args):
        pass

    def on_back_press(self):
        self.manager.display_screen(None, False, False)

    def on_home_press(self):
        self.manager.display_screen('town_main', False, False)

    def on_manager(self, instance, manager):
        if self.manager is None:
            return
        self.content = self.manager.app.get_content()
