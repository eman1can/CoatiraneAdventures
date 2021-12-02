# UIX Imports
# KV Import
from os.path import exists

from kivy.properties import BooleanProperty, NumericProperty

from game.save_load import SAVE_SLOT_1
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.relativelayout import RelativeLayout
from loading.kv_loader import load_kv
from uix.modules.screen import Screen

load_kv(__name__)


class StartGame(Screen):
    continue_enabled = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if exists(SAVE_SLOT_1):
            self.continue_enabled = True

    def on_start_game(self, load_type):
        if load_type == 'new_game':
            self.manager.display_screen('save_select', True, True, True)
        else:
            self.manager.display_screen('save_select', True, True, False)

    def on_exit_game(self):
        self.manager.app.exit_game()


class BossWarning(RelativeLayout):


    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        # Clock.schedule_once(self.start_animation, 1)

    def start_boss_warning_animation(self, dt):
        Clock.schedule_interval(self.update, 1 / 30)
        anim = Animation(fade_interval=0.25, duration=5, t='in_quad') + Animation(fade_interval=1, duration=5, t='in_quad')
        anim.start(self)

    def stop_animation(self, dt):
        Clock.unschedule(self.update)

    def update(self, dt):
        self._fade_time = min(self._fade_time + dt, self.fade_interval)
        fade_percent = self._fade_time / self.fade_interval
        if self._fade_in:
            self.opacity = 1 * fade_percent
        else:
            self.opacity = 1 - 1 * fade_percent
        if self._fade_in and self.opacity >= 1:
            self._fade_in = False
        elif not self._fade_in and self.opacity <= 0:
            self._fade_in = True
        else:
            return
        self._fade_time = 0
