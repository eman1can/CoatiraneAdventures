# Project Imports
# Standard Library Imports
import random

from kivy.properties import ObjectProperty

# Kivy Imports
from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import FadeTransition, SwapTransition
# KV Import
from loading.kv_loader import load_kv
from refs import Refs
# UIX Imports
from uix.modules.screen import Screen

load_kv(__name__)


class RecruitPreview(Screen):
    character = ObjectProperty(None)

    def __init__(self, character, viewed_characters, **kwargs):
        self.sound = SoundLoader.load('snd/recruit.wav')
        self.sound.seek(0)
        self.viewed_characters = viewed_characters
        self.character = character
        super().__init__(**kwargs)
        self.name = 'recruit_' + character.get_id()
        self.ids.char_image.source = self.character.full_image_source
        self.ids.char_type_flag.source = 'screens/recruit/char_type_flag.png'
        self.ids.type_flag.source = f'screens/recruit/{self.character.get_type().lower()}_flag.png'
        self.ids.element_flag_background.source = f'screens/attributes/{self.character.get_element().lower()}_flag.png'
        self.ids.element_flag_symbol.source = f'screens/attributes/{self.character.get_element().lower()}.png'

    def on_roll_again(self, *args):
        Refs.gp.display_popup(self, 'tm_roll', show_warning=False, on_confirm=self.do_roll_again)

    def do_roll_again(self, *args):
        char_list = Refs.gc.get_characters()
        obtained_chars = Refs.gc.get_all_obtained_character_indexes()
        if len(char_list) == len(obtained_chars) + len(self.viewed_characters):
            Refs.gp.display_popup(self, 'tm_no_recruit')
        else:
            Refs.gs.transition = SwapTransition(duration=2)
            unobtained_characters = [char for char in char_list if char.index not in obtained_chars and char not in self.viewed_characters]
            index = random.randint(0, len(unobtained_characters) - 1)
            self.viewed_characters.append(unobtained_characters[index])
            self.sound.play()
            Refs.gs.display_screen('recruit_' + unobtained_characters[index].get_id(), True, False, unobtained_characters[index], self.viewed_characters)

    def on_confirm(self, *args):
        Refs.gp.display_popup(self, 'tm_confirm', on_confirm=self.do_confirm)

    def do_confirm(self, *args):
        Refs.gc.obtain_character(self.character.get_index(), self.character.is_support())
        Refs.gs.transition = FadeTransition(duration=0.25)
        Refs.gs.display_screen(None, False, False)

    def on_cancel(self, *args):
        Refs.gp.display_popup(self, 'tm_cancel', on_confirm=self.do_cancel)

    def do_cancel(self, *args):
        Refs.gs.transition = FadeTransition(duration=0.25)
        Refs.gs.display_screen(None, False, False)

    def on_char_attribute(self):
        Refs.gs.transition = FadeTransition(duration=0.25)
        Refs.gs.display_screen('char_attr_' + self.character.get_id(), True, True, self.character, None)
