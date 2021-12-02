# Project Imports
# Kivy Imports
from kivy.properties import StringProperty

from game.save_load import load_save_info, delete_save
from kivy.uix.buttonversions import HoverPathButton
# KV Import
from loading.kv_loader import load_kv
from refs import Refs
# UIX Imports
from uix.modules.screen import Screen

# Standard Library Imports
load_kv(__name__)


class SaveSelect(Screen):
    def __init__(self, is_new_game, **kwargs):
        self.is_new_game = is_new_game
        self.saves = [False, False, False]
        super(SaveSelect, self).__init__(**kwargs)

    def reload(self, is_new_game=True):
        self.is_new_game = is_new_game
        self.saves = [False, False, False]
        Refs.log(f'Reload: {is_new_game}')

    def on_pre_enter(self, *args):
        # Load saves to slots
        Refs.log(f'Check Saves - {self.is_new_game}')

        # On new game, set all but top empty slot to disabled
        # On load game, set only loaded to disabled

        found_empty = True
        for save_slot in range(1, 4):
            Refs.log(f'Check save slot {save_slot}')
            info = load_save_info(save_slot)

            if info is not None:
                self.saves[0] = True
                self.ids[f'save_slot_{save_slot}'].has_game = True
                self.ids[f'save_slot_{save_slot}'].put_save_info(info)
                self.ids[f'save_trash_{save_slot}'].disabled = False
                self.ids[f'save_trash_{save_slot}'].opacity = 1
                self.set_save(save_slot, True)
            else:
                self.ids[f'save_trash_{save_slot}'].disabled = True
                self.ids[f'save_trash_{save_slot}'].opacity = 0
                if self.is_new_game and found_empty:
                    self.set_save(save_slot, True)
                    found_empty = False

                else:
                    self.set_save(save_slot, False)

    def set_save(self, save_slot, enabled):
        self.ids[f'save_slot_{save_slot}'].disabled = not enabled
        self.ids[f'save_slot_{save_slot}'].opacity = 1 if enabled else 0

    def load_save(self, save_num):
        if self.is_new_game:
            self.manager.display_screen('intro_start', True, True, save_num)
        else:
            self.manager.app.start_loading(save_num, 'town_main')
        self.ids.save_slot_1.disabled = True
        self.ids.save_slot_2.disabled = True
        self.ids.save_slot_3.disabled = True

    def delete_save(self, save_num):
        Refs.gp.display_popup(self, 'confirm', title_text='Are you sure?', description_text='This action is irreversible', on_confirm=lambda instance, num=save_num: self.do_delete_save(num))

    def do_delete_save(self, save_num):
        delete_save(save_num)
        self.on_pre_enter()


class SaveSlot(HoverPathButton):
    title = StringProperty('')

    def __init__(self, **kwargs):
        self.has_game = False
        super().__init__(**kwargs)

    def put_save_info(self, info):
        self.ids.version.text = f"Version - {info.get('game_version')}"
        self.ids.time.text = info.get('last_save_time')
        self.ids.gender_symbol.source = 'family/' + info.get('gender') + '.png'
        self.ids.domain_symbol.source = 'family/domains/' + info.get('domain') + '.png'
        self.ids.symbol.source = 'family/symbols/' + info.get('symbol').split('_')[1] + '.png'
        self.ids.name.text = info.get('save_name')
        self.ids.domain_name.text = info.get('domain')
        self.ids.rank.text = f"Family Renown - {info.get('rank')}"
        self.ids.varenth.text = f"Varenth - {info.get('varenth')}"
        self.ids.chars.text = f"Chars Obtained - {info.get('chars_collected')}"
        self.ids.quests.text = f"Quests Finished - {info.get('quests')}"
        self.ids.floor.text = f"Lowest Floor - {info.get('lowest_floor')}"
        self.ids.score.text = f"Total Score - {info.get('total_character_score')}"
        self.ids.skill.text = f"Skill Level - {info.get('skill_level')}"
