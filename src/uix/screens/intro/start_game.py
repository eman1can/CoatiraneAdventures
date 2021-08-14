# UIX Imports
# KV Import
from os.path import exists

from kivy.properties import BooleanProperty

from game.save_load import SAVE_SLOT_1
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
