# UIX Imports
from uix.modules.screen import Screen

# KV Import
from loading.kv_loader import load_kv
load_kv(__name__)


class NewGameScreen(Screen):
    def on_start_game(self):
        self.manager.display_screen('select_save', True, True)

    def on_exit_game(self):
        self.manager.app.exit_game()
