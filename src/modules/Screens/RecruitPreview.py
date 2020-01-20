from kivy.properties import ObjectProperty, BooleanProperty, ListProperty
from kivy.uix.screenmanager import Screen, FadeTransition
from kivy.uix.image import Image
from kivy.uix.label import Label

from src.modules.HTButton import HTButton

import random

class RecruitPreview(Screen):
    initialized = BooleanProperty(False)
    main_screen = ObjectProperty(None)

    character = ObjectProperty(None)
    viewed_characters = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'recruit_' + self.character.get_id()

        self._size = (0, 0)

        self.background = Image(source="../res/screens/backgrounds/recruit_background.png", allow_stretch=True)

        self.image = self.character.get_full_image(False)
        self.display_name = Label(text="[b]" + self.character.get_name() + "[/b]", markup=True, color=(1, 1, 1, 1), font_name="../res/fnt/Precious.ttf")
        self.name = Label(text="[b]" + self.character.get_name() + "[/b]", markup=True, color=(1, 1, 1, 1), font_name="../res/fnt/Precious.ttf")
        self.flag = Image(source="../res/screens/recruit/flag_" + self.character.get_type.lower() + ".png", allow_stretch=True)
        self.roll_again = HTButton(path='../res/screens/buttons/RecruitButtonRollAgain', collide_image="../res/screens/buttons/largebutton.collision.png", size_hint=(None, None), on_release=self.on_roll_again)
        self.confirm = HTButton(path='../res/screens/buttons/RecruitButtonConfirm', collide_image="../res/screens/buttons/largebutton.collision.png", size_hint=(None, None), on_release=self.on_confirm)
        self.cancel = HTButton(path='../res/screens/buttons/RecruitButtonCancel', collide_image="../res/screens/buttons/largebutton.collision.png", size_hint=(None, None), on_release=self.on_cancel)

        self.add_widget(self.title)
        self.add_widget(self.image)
        self.add_widget(self.flag)
        self.add_widget(self.roll_again)
        self.add_widget(self.confirm)
        self.add_widget(self.cancel)
        self.initialized = True

    def on_size(self, instance, size):
        if not self.initialized or self._size == size:
            return
        self._size = size.copy()

        self.display_name.font_size = self.height * 0.075
        self.display_name.texture_update()
        self.display_name.size = self.display_name.texture_size
        self.display_name.pos = self.display_name.width / 4, self.height - self.display_name.height * 1.25

        self.name.font_size = self.height * 0.15
        self.name.texture_update()
        self.name.size = self.name.texture_size
        self.name.pos = self.display_name.width / 4, self.height - self.display_name.height * 1.25 - self.name.height * 1.25


        self.image.size = size
        self.image.pos = (0, 0)

        button_size = self.height * 0.175 * 1016 / 716, self.height * 0.175
        self.roll_again.size = button_size
        self.roll_again.pos = self.width / 2 - button_size[0] * 1.75, button_size[1] * 0.25
        self.confirm.size = button_size
        self.confirm.pos = self.width / 2 - button_size[0] * 0.5, button_size[1] * 0.25
        self.cancel.size = button_size
        self.cancel.pos = self.width / 2 + button_size[0] * .75, button_size[1] * 0.25

    def on_roll_again(self, instance):
        if len(self.main_screen.characters) == len(self.main_screen.obtained_characters) + len(self.viewed_characters):
            print("No more characters")
        else:
            unobtained_characters = [char for char in self.main_screen.characters if char.index not in self.main_screen.obtained_characters and char not in self.viewed_characters]
            print("unobtained chars", unobtained_characters)
            index = random.randint(0, len(unobtained_characters) - 1)
            print(index)
            print(unobtained_characters[index].get_display_name())
            self.viewed_characters.append(unobtained_characters[index])
            self.main_screen.create_screen('recruit', unobtained_characters[index], self.viewed_characters)
            self.main_screen.display_screen('recruit_' + unobtained_characters[index].get_id(), True, False)

    def on_confirm(self, instance):
        self.main_screen.obtained_characters.append(self.character.get_index())
        if self.character.is_support():
            self.main_screen.obtained_characters_s.append(self.character.get_index())
        else:
            self.main_screen.obtained_characters_a.append(self.character.get_index())
        self.main_screen.transition = FadeTransition(duration=0.25)
        self.main_screen.display_screen(None, False, False)

    def on_cancel(self, instance):
        self.main_screen.transition = FadeTransition(duration=0.25)
        self.main_screen.display_screen(None, False, False)