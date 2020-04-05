from kivy.app import App
import random

from kivy.core.audio import SoundLoader
from kivy.core.image import Image
from kivy.properties import ObjectProperty, ListProperty, StringProperty
from kivy.uix.screenmanager import FadeTransition

from src.modules.KivyBase.Hoverable import ScreenH as Screen
from src.modules.NoRecruit import NoRecruitWidget


class RecruitPreview(Screen):
    main_screen = ObjectProperty(None)

    character = ObjectProperty(None)
    viewed_characters = ListProperty([])

    character_image_source = StringProperty('')
    background_texture = ObjectProperty(None, allownone=True)
    char_type_flag_texture = ObjectProperty(None, allownone=True)
    type_flag_texture = ObjectProperty(None, allownone=True)
    element_flag_background_texture = ObjectProperty(None, allownone=True)
    element_flag_symbol_texture = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        self.background_texture = Image("../res/screens/backgrounds/background.png").texture
        self.char_type_flag_texture = Image("../res/screens/recruit/char_type_flag.png").texture
        self.sound = SoundLoader.load('../res/snd/recruit.wav')
        self.root = App.get_running_app().main
        self.no_recruits = NoRecruitWidget()
        super().__init__(**kwargs)

    def on_character(self, *args):
        self.type_flag_texture = Image("../res/screens/recruit/" + self.character.get_type().lower() + "_flag.png").texture
        self.element_flag_background_texture = Image("../res/screens/attribute/" + self.character.get_element().lower() + "_flag.png").texture
        self.element_flag_symbol_texture = Image("../res/screens/attribute/" + self.character.get_element().lower() + ".png").texture
        self.character_image_source = self.character.full_image_source

    def on_roll_again(self):
        if len(self.root.characters) == len(self.root.obtained_characters) + len(self.viewed_characters):
            self.no_recruits.open()
        else:
            unobtained_characters = [char for char in self.root.characters if char.index not in self.root.obtained_characters and char not in self.viewed_characters]
            index = random.randint(0, len(unobtained_characters) - 1)
            self.viewed_characters.append(unobtained_characters[index])
            self.root.create_screen('recruit', unobtained_characters[index], self.viewed_characters)
            self.sound.play()
            self.root.display_screen('recruit_' + unobtained_characters[index].get_id(), True, False)

    def on_confirm(self):
        self.root.obtained_characters.append(self.character.get_index())
        if self.character.is_support():
            self.root.obtained_characters_s.append(self.character.get_index())
        else:
            self.root.obtained_characters_a.append(self.character.get_index())
        self.root.transition = FadeTransition(duration=0.25)
        self.root.display_screen(None, False, False)

    def on_cancel(self):
        self.root.transition = FadeTransition(duration=0.25)
        self.root.display_screen(None, False, False)

    def on_char_attribute(self):
        self.root.transition = FadeTransition(duration=0.25)
        next_screen = self.character.get_attr_screen()
        self.root.display_screen(next_screen, True, True)