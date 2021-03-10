# UIX Imports
from game.save_load import create_new_save
from uix.modules.screen import Screen

# KV Import
from loading.kv_loader import load_kv
load_kv(__name__)


class SelectScreen(Screen):
    def __init__(self, save_slot, name, gender, symbol_id, domain, **kwargs):
        self.save_slot = save_slot
        self.god_name = name
        self.gender = gender
        self.symbol_id = symbol_id
        self.domain = domain
        super().__init__(**kwargs)

    def choose_character(self, choice):
        create_new_save(self.save_slot, self.god_name, self.gender, self.symbol_id, self.domain, choice)
        self.manager.app.start_loading(self.save_slot)
