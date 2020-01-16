from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import SlideTransition, RiseInTransition
from src.modules.HTButton import HTButton
from src.modules.Screens.RecruitPreview import RecruitPreview
import random


class TavernMain(Screen):
    def __init__(self, main_screen, **kwargs):
        self.initalized = False
        super().__init__(**kwargs)
        self.name = 'tavern_main'

        self.main_screen = main_screen

        self.unlocked = True
        self._size = (0, 0)

        self.background = Image(allow_stretch=True, keep_ratio=True, source='../res/screens/backgrounds/collage.png')
        self.lock = Image(allow_stretch=True, keep_ratio=True, source='../res/screens/backgrounds/locked.png')
        self.title = Label(text="[b]Recruitment[/b]", markup=True, color=(1, 1, 1, 1), size_hint=(None, None), font_name='../res/fnt/Precious.ttf')

        self.recruit_button = HTButton(path='../res/screens/buttons/recruitButton', size_hint=(None, None), collide_image="../res/screens/buttons/largebutton.collision.png", on_touch_down=self.onRecruit)
        self.back_button = HTButton(path='../res/screens/buttons/back', size_hint=(None, None), on_touch_down=self.on_back_press)

        self.add_widget(self.background)
        self.add_widget(self.title)
        self.add_widget(self.recruit_button)
        self.add_widget(self.lock)
        self.add_widget(self.back_button)
        self.initalized = True

    def on_size(self, instance, size):
        if not self.initalized or self._size == size:
            return
        self._size = size.copy()

        self.background.size = self.size
        self.lock.size = self.size

        self.title.font_size = self.width * 0.15
        self.title.texture_update()
        self.title.size = self.title.texture_size
        self.title.pos = self.width * 0.1, self.height * 0.95 - self.title.height

        self.recruit_button.size = self.height * 0.15 * 1016 / 716, self.height * 0.15
        self.recruit_button.pos = self.width * 0.5 - self.recruit_button.width * 0.5, self.height * 0.1

        self.back_button.size = self.width * .05, self.width * .05
        self.back_button.pos = 0, self.height - self.back_button.height

    def reload(self):
        pass

    def onRecruit(self, instance, touch):
        if instance.collide_point(*touch.pos):
            if self.unlocked:
                notobtained = False
                while not notobtained:
                    index = random.randint(0, len(self.main_screen.characters) - 1)
                    notobtained = index not in self.main_screen.obtained_characters
                screen = RecruitPreview(self.main_screen, self.main_screen.characters[index], size=self.size)
                self.main_screen.display_screen(screen, True, True)

    def check_unlock(self):
        self.unlocked = self.main_screen.tavern_unlocked
        if self.unlocked:
            self.remove_widget(self.lock)

    def on_back_press(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.main_screen.display_screen(None, False, False)
