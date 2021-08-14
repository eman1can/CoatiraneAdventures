# UIX Imports
# KV Import
from kivy.clock import Clock
from loading.kv_loader import load_kv
from refs import Refs
from uix.modules.headers import time_header
from uix.modules.screen import Screen

load_kv(__name__)


class TownMain(Screen):
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)

        # self.sound = SoundLoader.load('res/town.mp3')
        # self.sound.loop = True

    def on_pre_enter(self, *args):
        self.check_locks()

    def on_enter(self):
        Clock.schedule_interval(self.update_time_header, 5)
        # if self.sound:
        #     self.sound.play()

    def on_leave(self):
        Clock.unschedule(self.update_time_header)
        # if self.sound:
        #     self.sound.stop()

    def update_time_header(self, dt):
        self.ids.time_header.text = time_header()

    def on_dungeon(self):
        self.manager.display_screen('dungeon_main', True, True)

    def on_inventory(self):
        self.manager.display_screen('inventory_main', True, True)

    def on_tavern(self):
        if not self.content.is_tavern_locked():
            self.manager.display_screen('tavern_main', True, True)

    def on_crafting(self):
        if not self.content.is_tavern_locked():
            self.manager.display_screen('crafting_main', True, True)

    def check_locks(self):
        self.ids.tavern_lock.opacity = int(self.content.is_tavern_locked())
        self.ids.crafting_lock.opacity = int(self.content.is_tavern_locked())
