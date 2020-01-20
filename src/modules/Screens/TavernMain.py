from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import SlideTransition, RiseInTransition, SwapTransition
from kivy.core.audio import SoundLoader

import random

from src.modules.HTButton import HTButton


class TavernMain(Screen):
    initialized = BooleanProperty(False)
    main_screen = ObjectProperty(None)
    unlocked = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'tavern_main'

        self._size = (0, 0)

        self.background = Image(allow_stretch=True, keep_ratio=True, source='../res/screens/backgrounds/collage.png', size_hint=(None, None))
        self.lock = Image(allow_stretch=True, keep_ratio=True, source='../res/screens/backgrounds/locked.png')
        self.title = Label(text="[b]Recruitment[/b]", markup=True, color=(1, 1, 1, 1), size_hint=(None, None), font_name='../res/fnt/Precious.ttf', outline_width=2, outline_color=(0, 0, 0, 1))

        self.recruit_button = HTButton(path='../res/screens/buttons/recruit_button', size_hint=(None, None), collide_image="../res/screens/buttons/largebutton.collision.png", text="Recruit", font_name='../res/fnt/Precious.ttf', label_color=(1, 1, 1, 1), on_release=self.on_recruit)
        self.back_button = HTButton(path='../res/screens/buttons/back', size_hint=(None, None), on_release=self.on_back_press)

        self.sound = SoundLoader.load('../res/snd/recruit.wav')

        self.add_widget(self.background)
        self.add_widget(self.title)
        self.add_widget(self.recruit_button)
        self.add_widget(self.lock)
        self.add_widget(self.back_button)
        self.initialized = True

    def on_enter(self, *args):
        if not self.unlocked:
            self.check_unlock()

    def on_size(self, instance, size):
        if not self.initialized or self._size == size:
            return
        self._size = size.copy()

        self.background.size = self.size
        self.lock.size = self.size

        self.title.font_size = self.width * 0.0725
        self.title.texture_update()
        self.title.size = self.title.texture_size
        self.title.pos = self.width * 0.2, self.height * 0.95 - self.title.height

        self.recruit_button.size = self.height * 0.15 * 1016 / 716, self.height * 0.15
        self.recruit_button.pos = self.width * 0.5 - self.recruit_button.width * 0.5, self.height * 0.1
        self.recruit_button.font_size = self.recruit_button.height * 0.1875
        self.recruit_button.label_padding = [0, self.recruit_button.height * 0.4, 0, 0]

        self.back_button.size = self.width * .05, self.width * .05
        self.back_button.pos = 0, self.height - self.back_button.height

    def reload(self):
        pass

    def on_recruit(self, instance):
        if self.unlocked:
            print(self.main_screen.obtained_characters)
            print(self.main_screen.characters)
            if self.main_screen.obtained_characters == len(self.main_screen.characters):
                print("Obtained All Characters")
            else:
                unobtained_characters = [char for char in self.main_screen.characters if char.index not in self.main_screen.obtained_characters]
                index = random.randint(0, len(unobtained_characters) - 1)
                viewed_characters = [unobtained_characters[index]]
                self.main_screen.create_screen('recruit', unobtained_characters[index], viewed_characters)
                self.main_screen.transition = SwapTransition(duration=2)
                self.sound.play()
                self.main_screen.display_screen('recruit_' + unobtained_characters[index].get_id(), True, True)

    def check_unlock(self):
        self.unlocked = self.main_screen.tavern_unlocked
        if self.unlocked:
            self.remove_widget(self.lock)

    def on_back_press(self, instance):
        self.main_screen.display_screen(None, False, False)
