# Project Imports
from kivy.uix.buttonversions import HoverPathButton

from game.save_load import SAVE_SLOT_1, SAVE_SLOT_2, SAVE_SLOT_3, load_save_info
from refs import Refs

# UIX Imports
from uix.modules.screen import Screen

# Standard Library Imports
from os.path import exists

# Kivy Imports
from kivy.properties import StringProperty

# KV Import
from loading.kv_loader import load_kv
load_kv(__name__)


class SelectSaveScreen(Screen):
    def __init__(self, **kwargs):
        self.saves = [False, False, False]
        super(SelectSaveScreen, self).__init__(**kwargs)

    def on_pre_enter(self, *args):
        # Load saves to slots
        Refs.log('Check Saves')
        for save_slot in range(1, 4):
            Refs.log('Check save slot 1')
            info = load_save_info(save_slot)
            if info is not None:
                self.saves[0] = True
                self.ids[f'save_slot_{save_slot}'].has_game = True
                self.ids[f'save_slot_{save_slot}'].put_save_info(info)
        # if exists(SAVE_SLOT_1):
        #     self.ids.save_slot_1.load_save_info(1)
        #     self.saves[0] = True
        # if exists(SAVE_SLOT_2):
        #     Refs.log('Load save slot 2')
        #     self.ids.save_slot_2.load_save_info(2)
        #     self.saves[1] = True
        # if exists(SAVE_SLOT_3):
        #     Refs.log('Load save slot 3')
        #     self.ids.save_slot_3.load_save_info(3)
        #     self.saves[2] = True

    def load_save(self, save_num):
        if self.saves[save_num - 1]:
            #TODO: Tell the loader which save to load
            #TODO: Add Save & New Game chunk into loader
            self.manager.app.start_loading(save_num)
        else:
            Refs.gs.display_screen('intro_start', True, True, save_num)

    def start_game(self):
        if self.has_game:
            # Load the game from disk
            pass
        else:
            # Go through game creation
            pass


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
        self.ids.symbol.source = 'family/symbols/' + info.get('symbol')[-1] + '.png'
        self.ids.name.text = info.get('save_name')
        self.ids.domain_name.text = info.get('domain')
        self.ids.rank.text = f"Family Renown - {info.get('rank')}"
        self.ids.varenth.text = f"Varenth - {info.get('varenth')}"
        self.ids.chars.text = f"Chars Obtained - {info.get('chars_collected')}"
        self.ids.quests.text = f"Quests Finished - {info.get('quests')}"
        self.ids.floor.text = f"Lowest Floor - {info.get('lowest_floor')}"
        self.ids.score.text = f"Total Score - {info.get('total_character_score')}"
        self.ids.skill.text = f"Skill Level - {info.get('skill_level')}"


