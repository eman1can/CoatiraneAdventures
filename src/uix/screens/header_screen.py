from kivy.clock import Clock

from loading.kv_loader import load_kv
from uix.modules.headers import time_header
from uix.modules.screen import Screen

load_kv(__name__)


class HeaderScreen(Screen):
    def on_enter(self):
        Clock.schedule_interval(self.update_time_header, 5)

    def on_leave(self):
        Clock.unschedule(self.update_time_header)

    def update_time_header(self, dt):
        self.ids.time_header.text = time_header()
