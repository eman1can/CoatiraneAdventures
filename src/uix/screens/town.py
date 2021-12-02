# UIX Imports
# KV Import
from kivy.properties import StringProperty
from loading.kv_loader import load_kv
from refs import Refs
from uix.modules.screen import Screen

load_kv(__name__)


class TownMain(Screen):
    profile_source = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
        self.manager.display_screen('shop_main', True, True, 'main')

    def on_quests(self):
        self.manager.display_screen('quests_main', True, True)

    def on_crafting(self):
        if not self.content.is_tavern_locked():
            self.manager.display_screen('crafting_main', True, True)

    def on_inventory(self):
        self.manager.display_screen('inventory_main', True, True)

    def on_profile(self):
        self.manager.display_screen('profile_main', True, True)

    def on_almanac(self):
        self.manager.display_screen('almanac_main', True, True)

    def on_housing(self):
        pass
