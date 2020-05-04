import random
from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import SwapTransition

from src.modules.KivyBase.Hoverable import ScreenBase as Screen
from src.modules.NoRecruit import NoRecruitWidget


class TavernMain(Screen):
    background_texture = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        self.sound = SoundLoader.load('../res/snd/recruit.wav')
        self.no_recruits = NoRecruitWidget()
        super().__init__(**kwargs)

    def on_recruit(self):
        root = App.get_running_app().main
        if len(root.obtained_characters) == len(root.characters):
            self.no_recruits.open()
        else:
            unobtained_characters = [char for char in root.characters if char.index not in root.obtained_characters]
            index = random.randint(0, len(unobtained_characters) - 1)
            viewed_characters = [unobtained_characters[index]]
            root.create_screen('recruit', unobtained_characters[index], viewed_characters)
            root.transition = SwapTransition(duration=2)
            self.sound.play()
            root.display_screen('recruit_' + unobtained_characters[index].get_id(), True, True)
