# Project Imports
from refs import Refs

# UIX Imports
from uix.modules.screen import Screen

# Kivy Imports
from kivy.properties import StringProperty

# Standard Library Imports
import random

# KV Import
from loading.kv_loader import load_kv
load_kv(__name__)


class DungeonResult(Screen):
    win_message = StringProperty('')
    image_source = StringProperty('')

    def __init__(self, characters, floor_num, **kwargs):
        self.dungeon_config = {}
        super().__init__(**kwargs)
        self.win_message = 'Floor ' + str(floor_num) + ' - Victory'
        character = characters[random.randrange(0, len(characters))]
        self.image_source = character.full_image_source
        self.floor_num = floor_num

    def goto_dungeon_main(self):
        Refs.gs.get_screen('dungeon_main').dungeon_config = {}
        Refs.gs.display_screen('dungeon_main', True, True)
