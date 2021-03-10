# Project Imports
from refs import Refs

# UIX Imports
from uix.modules.screen import Screen

# Standard Library Imports
import random

# Kivy Imports
from kivy.core.audio import SoundLoader
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import SwapTransition

# KV Import
from loading.kv_loader import load_kv
load_kv(__name__)


class TavernMain(Screen):
    background_texture = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        self.sound = SoundLoader.load('../res/snd/recruit.wav')
        self.sound.seek(0)
        super().__init__(**kwargs)

    def on_recruit(self, *args):
        Refs.gp.display_popup(self, 'tm_roll', show_warning=False, on_confirm=self.do_recruit)

    def do_recruit(self, *args):
        characters = Refs.gc.get_characters()
        obtained_characters = Refs.gc.get_all_obtained_character_indexes()

        if len(obtained_characters) == len(characters):
            Refs.gp.display_popup(self, 'tm_no_recruit')
        else:
            unobtained_characters = [char for char in characters if char.index not in obtained_characters]
            index = random.randint(0, len(unobtained_characters) - 1)
            viewed_characters = [unobtained_characters[index]]
            Refs.gs.transition = SwapTransition(duration=2)
            self.sound.play()
            Refs.gs.display_screen('recruit_' + unobtained_characters[index].get_id(), True, True, unobtained_characters[index], viewed_characters)
