# UIX Imports
# KV Import
from kivy.clock import Clock
from kivy.properties import StringProperty
from loading.kv_loader import load_kv
from refs import Refs
from uix.modules.headers import time_header
from uix.modules.screen import Screen

load_kv(__name__)


class TownMain(Screen):
    profile_source = StringProperty('')

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)

        # self.sound = SoundLoader.load('res/town.mp3')
        # self.sound.loop = True

    def on_kv_post(self, base_widget):
        symbol = Refs.gc.get_symbol().split('_')[1]
        self.profile_source = f'family/symbols/{symbol}_white.png'
        days_until_due = Refs.gc.get_housing().get_bill_due()
        if days_until_due < 0:
            self.ids.housing_warning.opacity = 1
            self.ids.warning_label.text = 'Your housing bill is overdue!'
        elif days_until_due < 5:
            self.ids.housing_warning.opacity = 1
            self.ids.warning_label.text = f'Your housing bill is due in {days_until_due} days!'
        else:
            self.ids.housing_warning.opacity = 0

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

    def check_locks(self):
        self.ids.tavern_lock.opacity = int(self.content.is_tavern_locked())
        self.ids.crafting_lock.opacity = int(self.content.is_tavern_locked())

    def on_save_game(self):
        Refs.gc.save_game()

    def on_exit_game(self):
        Refs.app.reset_loader()
        Refs.gc.save_game(lambda: Refs.gs.display_screen('start_game', True, False))

    def on_dungeon(self):
        self.manager.display_screen('dungeon_main', True, True)

    def on_tavern(self):
        if not self.content.is_tavern_locked():
            self.manager.display_screen('tavern_main', True, True)

    def on_shop(self):
        pass

    def on_quests(self):
        pass

    def on_crafting(self):
        if not self.content.is_tavern_locked():
            self.manager.display_screen('crafting_main', True, True)

    def on_inventory(self):
        self.manager.display_screen('inventory_main', True, True)

    def on_profile(self):
        self.manager.display_screen('profile_main', True, True)

    def on_almanac(self):
        pass

    def on_housing(self):
        pass
