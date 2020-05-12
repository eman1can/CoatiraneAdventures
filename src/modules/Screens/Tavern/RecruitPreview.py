from kivy.app import App
import random

from kivy.core.audio import SoundLoader
from kivy.properties import ObjectProperty, ListProperty, StringProperty, BooleanProperty
from kivy.uix.screenmanager import FadeTransition, SwapTransition

from src.modules.KivyBase.Hoverable import ScreenBase as Screen
from src.modules.Screens.Tavern.NoRecruit import NoRecruitWidget
from src.modules.Screens.Tavern.modals import TMCancelWidget, TMConfirmWidget, TMRollWidget


class RecruitPreview(Screen):
    character = ObjectProperty(None)
    viewed_characters = ListProperty([])

    character_image_source = StringProperty('')
    char_type_flag_source = StringProperty('../res/screens/recruit/char_type_flag.png')
    type_flag_source = StringProperty('')
    element_flag_background_source = StringProperty('')
    element_flag_symbol_source = StringProperty('')

    modal_open = BooleanProperty(False)

    def __init__(self, **kwargs):
        self.sound = SoundLoader.load('../res/snd/recruit.wav')
        self.root = App.get_running_app().main
        self.no_recruits = NoRecruitWidget()
        self.cancel_modal = TMCancelWidget()
        self.confirm_modal = TMConfirmWidget()
        self.rollagain_modal = TMRollWidget()
        super().__init__(**kwargs)
        self.cancel_modal.bind(on_confirm=self.do_cancel)
        self.cancel_modal.bind(on_dismiss=self.dismiss_modal)
        self.confirm_modal.bind(on_confirm=self.do_confirm)
        self.confirm_modal.bind(on_dismiss=self.dismiss_modal)
        self.rollagain_modal.bind(on_confirm=self.do_roll_again)
        self.rollagain_modal.bind(on_dismiss=self.dismiss_modal)
        self.no_recruits.bind(on_dismiss=self.dismiss_modal)

    def on_touch_hover(self, touch):
        if self.modal_open:
            return False
        return self.dispatch_to_relative_children(touch)

    def dismiss_modal(self, *args):
        self.modal_open = False

    def on_character(self, *args):
        self.type_flag_source = "../res/screens/recruit/" + self.character.get_type().lower() + "_flag.png"
        self.element_flag_background_source = "../res/screens/attribute/" + self.character.get_element().lower() + "_flag.png"
        self.element_flag_symbol_source = "../res/screens/attribute/" + self.character.get_element().lower() + ".png"
        self.character_image_source = self.character.full_image_source

    def on_roll_again(self, *args):
        self.modal_open = True
        self.rollagain_modal.open()

    def do_roll_again(self, *args):
        if len(self.root.characters) == len(self.root.obtained_characters) + len(self.viewed_characters):
            self.modal_open = True
            self.no_recruits.open()
        else:
            self.root.transition = SwapTransition(duration=2)
            unobtained_characters = [char for char in self.root.characters if char.index not in self.root.obtained_characters and char not in self.viewed_characters]
            index = random.randint(0, len(unobtained_characters) - 1)
            self.viewed_characters.append(unobtained_characters[index])
            self.root.create_screen('recruit', unobtained_characters[index], self.viewed_characters)
            self.sound.play()
            self.root.display_screen('recruit_' + unobtained_characters[index].get_id(), True, False)

    def on_confirm(self, *args):
        self.modal_open = True
        self.confirm_modal.open()

    def do_confirm(self, *args):
        self.root.obtained_characters.append(self.character.get_index())
        if self.character.is_support():
            self.root.obtained_characters_s.append(self.character.get_index())
        else:
            self.root.obtained_characters_a.append(self.character.get_index())
        self.root.transition = FadeTransition(duration=0.25)
        self.root.display_screen(None, False, False)

    def on_cancel(self, *args):
        self.modal_open = True
        self.cancel_modal.open()

    def do_cancel(self, *args):
        self.root.transition = FadeTransition(duration=0.25)
        self.root.display_screen(None, False, False)

    def on_char_attribute(self):
        self.root.transition = FadeTransition(duration=0.25)
        screen, made = self.root.create_screen('char_attr', self.character)
        self.root.display_screen(screen, True, True)