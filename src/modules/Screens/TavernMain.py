from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import SlideTransition, RiseInTransition
from src.modules.HTButton import HTButton
from src.modules.Screens.RecruitPreview import RecruitPreview

import random

class TavernMain(Screen):

    def __init__(self, main_screen, **kwargs):
        self.main_screen = main_screen
        super().__init__(**kwargs)
        size = (main_screen.width, main_screen.height)
        self.bg = Image(size=size, pos=(0, 0), allow_stretch=True, keep_ratio=True,
                        source='../res/screens/backgrounds/collage.png')
        self.title = Label(text="[b]Recruitment[/b]", markup=True, font_size=175, color=(1, 1, 1, 1),
                           pos=(650, main_screen.height - 200), size=(200, 50), size_hint=(None, None))
        self.recruitButton = HTButton(path='../res/screens/buttons/recruitButton', collide_image="../res/screens/buttons/largebutton.collision.png", size=(270, 180),
                                      pos=(main_screen.width / 2 - 270 / 2, 100), on_touch_down=self.onRecruit)
        self.lock = Image(size=size, pos=(0, 0), allow_stretch=True, keep_ratio=True,
                          source='../res/screens/backgrounds/locked.png')
        # print("Locking")
        self.locked = True
        self.disabled = False
        self.screen_size = 3840
        self.back_button = HTButton(size=(256 * size[0] / self.screen_size, 256 * size[0] / self.screen_size), pos=(0, size[1] - (256 * size[0] / self.screen_size)), path='../res/screens/buttons/back', on_touch_up=self.on_back_press)

        self.add_widget(self.bg)
        self.add_widget(self.title)
        self.add_widget(self.recruitButton)
        self.add_widget(self.lock)
        self.add_widget(self.back_button)
        self.size = size

    def on_size(self, instance, size):
        self.title.font_size = size[0] / 7.2
        self.title.pos = size[0] / 3, size[1] / 1.14
        self.recruitButton.size = size[1] / 4, size[1] / 6
        self.recruitButton.pos = size[0] / 2 - self.recruitButton.width / 2, size[1] / 10.8
        self.back_button.size = (256 * size[0] / self.screen_size, 256 * size[0] / self.screen_size)
        self.back_button.pos = (0, size[1] - self.back_button.height)

    def reload(self):
        pass

    def onRecruit(self, instance, touch):
        if instance.collide_point(*touch.pos):
            if self.unlocked:
                if not self.disabled:

                    # print("Recruit")
                    notobtained = False
                    while not notobtained:
                        index = random.randint(0, len(self.main_screen.characters) - 1)
                        print(str(index))
                        print(str(self.main_screen.obtained_characters))
                        notobtained = index not in self.main_screen.obtained_characters
                    print(str(self.main_screen.characters[index].get_name()))
                    preview = RecruitPreview(self.main_screen, self.main_screen.characters[index])
                    self.main_screen.transition = RiseInTransition(duration=.3)
                    self.main_screen.display_screen(preview, True, True)

    def check_unlock(self):
        print(str(self.main_screen.tavern_unlocked))
        self.unlocked = self.main_screen.tavern_unlocked
        if self.unlocked:
            print("unlocking")
            self.remove_widget(self.lock)

    def on_back_press(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.main_screen.transition = SlideTransition()
            self.main_screen.display_screen(None, False, False)
