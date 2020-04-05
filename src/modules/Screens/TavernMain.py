import random
from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.core.image import Image
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import SwapTransition

from src.modules.KivyBase.Hoverable import ScreenH as Screen
from src.modules.NoRecruit import NoRecruitWidget


class TavernMain(Screen):
    main_screen = ObjectProperty(None)
    background_texture = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        self.background_texture = Image('../res/screens/backgrounds/collage.png').texture
        self.sound = SoundLoader.load('../res/snd/recruit.wav')
        self.no_recruits = NoRecruitWidget()
        super().__init__(**kwargs)

    def reload(self):
        pass

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

    def on_back_press(self):
        App.get_running_app().main.display_screen(None, False, False)
