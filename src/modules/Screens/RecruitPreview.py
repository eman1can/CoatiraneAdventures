from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.label import Label

from src.modules.HTButton import HTButton

import random

class RecruitPreview(Screen):
    initialized = BooleanProperty(False)
    main_screen = ObjectProperty(None)

    def __init__(self, char, **kwargs):
        super().__init__(**kwargs)
        self.name = 'recruit_' + char.get_name()

        self.char = char

        self._size = (0, 0)

        self.background = Image(source="../res/screens/backgrounds/recruit_background.png", allow_stretch=True)

        self.image = char.get_full_image(False)
        self.title = Label(text="[b]" + char.get_name() + "[/b]", markup=True, color=(1, 1, 1, 1), font_name="../res/fnt/Precious.ttf")
        self.roll_again = HTButton(path='../res/screens/buttons/RecruitButtonRollAgain', collide_image="../res/screens/buttons/largebutton.collision.png", size_hint=(None, None), on_touch_down=self.on_roll_again)
        self.confirm = HTButton(path='../res/screens/buttons/RecruitButtonConfirm', collide_image="../res/screens/buttons/largebutton.collision.png", size_hint=(None, None), on_touch_down=self.on_confirm)
        self.cancel = HTButton(path='../res/screens/buttons/RecruitButtonCancel', collide_image="../res/screens/buttons/largebutton.collision.png", size_hint=(None, None), on_touch_down=self.on_cancel)

        self.add_widget(self.title)
        self.add_widget(self.image)
        self.add_widget(self.roll_again)
        self.add_widget(self.confirm)
        self.add_widget(self.cancel)
        self.initialized = True

    def on_size(self, instance, size):
        if not self.initialized or self._size == size:
            return
        self._size = size.copy()

        self.title.font_size = self.height * 0.15
        self.title.texture_update()
        self.title.size = self.title.texture_size
        self.title.pos = self.width / 2 - self.title.width / 2, self.height * 0.9

        self.image.size = size
        self.image.pos = (0, 0)

        button_size = self.height * 0.25 * 1016 / 716, self.height * 0.25
        self.roll_again.size = button_size
        self.roll_again.pos = self.width / 2 - button_size[0] * 1.75, button_size[1] * 0.25
        self.confirm.size = button_size
        self.confirm.pos = self.width / 2 - button_size[0] * 0.5, button_size[1] * 0.25
        self.cancel.size = button_size
        self.cancel.pos = self.width / 2 + button_size[0] * .75, button_size[1] * 0.25

    def on_roll_again(self, instance, touch):
        if instance.collide_point(*touch.pos):
            not_obtained = False
            while not not_obtained:
                index = random.randint(0, len(self.main_screen.characters) - 1)
                not_obtained = index not in self.main_screen.obtained_characters
            preview = RecruitPreview(self.main_screen, self.main_screen.characters[index])
            preview.size = self.size
            self.main_screen.display_screen(preview, True, False)

    def on_confirm(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.main_screen.obtained_characters.append(self.char.get_index())
            if self.char.is_support():
                self.main_screen.obtained_characters_s.append(self.char.get_index())
            else:
                self.main_screen.obtained_characters_a.append(self.char.get_index())
            self.main_screen.display_screen(None, False, False)

    def on_cancel(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.main_screen.display_screen(None, False, False)