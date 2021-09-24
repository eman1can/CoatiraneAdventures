from loading.family import load_domains
# KV Import
from loading.kv_loader import load_kv
from refs import Refs
from uix.modules.screen import Screen

load_kv(__name__)


class IntroDomain(Screen):
    def __init__(self, save_slot, name, gender, symbol_id, **kwargs):
        self.save_slot = save_slot
        self.god_name = name
        self.gender = gender
        self.symbol_id = symbol_id
        super().__init__(**kwargs)
        data = []
        domains = load_domains(Refs.gc.get_program_type())
        for domain in domains:
            data.append({'opacity': 0.5, 'domain': domain})
        data[0]['opacity'] = 1
        self.ids.domain_wheel.data = data
        self.ids.large_display.domain = data[0]['domain']

    def goto_next(self):
        Refs.gs.display_screen('intro_select', True, True, self.save_slot, self.god_name, self.gender, self.symbol_id, self.ids.domain_wheel.widgets[0].domain.get_title())
