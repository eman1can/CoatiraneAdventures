import random
from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.screenmanager import SwapTransition

from src.modules.KivyBase.Hoverable import ScreenBase as Screen
from src.modules.Screens.Tavern.NoRecruit import NoRecruitWidget
from src.modules.Screens.Tavern.modals import TMRollWidget


class TavernMain(Screen):
    background_texture = ObjectProperty(None, allownone=True)

    modal_open = BooleanProperty(False)

    def __init__(self, **kwargs):
        self.sound = SoundLoader.load('../res/snd/recruit.wav')
        self.no_recruits = NoRecruitWidget()
        self.roll_modal = TMRollWidget()
        self.roll_modal.show_warning = False
        super().__init__(**kwargs)
        self.roll_modal.bind(on_confirm=self.do_recruit)
        self.roll_modal.bind(on_dismiss=self.dismiss_modal)

    def on_touch_hover(self, touch):
        if self.modal_open:
            return False
        return self.dispatch_to_relative_children(touch)

    def dismiss_modal(self, *args):
        self.modal_open = False

    def on_recruit(self, *args):
        self.modal_open = True
        self.roll_modal.open()

    def do_recruit(self, *args):
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
