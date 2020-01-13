from kivy.uix.screenmanager import Screen, RiseInTransition
from kivy.uix.image import Image
from kivy.uix.label import Label

from src.modules.CustomHoverableButton import CustomHoverableButton

import random

class RecruitPreview(Screen):

    def __init__(self, main_screen, char, **kwargs):
        self.main_screen = main_screen
        super().__init__(**kwargs, name='RecruitPreview_%s' % char.get_id(), id='RecruitPreview')
        self.image = char.get_full_image(False)
        self.image.size = (self.main_screen.height * 2 / 3, self.main_screen.height * 2 / 3)
        self.image.pos = (0, 0)
        self.add_widget(self.image)
        self.title = Label(text="[b]" + char.get_name() + "[/b]", markup=True, color=(1, 1, 1, 1), size=(200, 50),
                           font_size=80, pos=((self.main_screen.width - (self.main_screen.height * 2 / 3)) / 2, self.main_screen.height - 100))
        self.add_widget(self.title)
        self.rollAgainButton = CustomHoverableButton(path='../res/screens/buttons/RecruitButtonRollAgain', collision="../res/screens/buttons/largebutton.collision.png", size=(270, 180),
                                            pos=(200 - 135, self.main_screen.height / 2), on_touch_down=self.onRollAgain)
        self.confirmButton = CustomHoverableButton(path='../res/screens/buttons/RecruitButtonConfirm', collision="../res/screens/buttons/largebutton.collision.png", size=(270, 180),
                                          pos=(self.main_screen.width - 200 - 135, self.main_screen.height / 2), on_touch_down=self.onConfirm)
        self.cancelButton = CustomHoverableButton(path='../res/screens/buttons/RecruitButtonCancel', collision="../res/screens/buttons/largebutton.collision.png", size=(270, 180),
                                         pos=(self.main_screen.width - 200 - 135, self.main_screen.height / 2 - 200), on_touch_down=self.onCancel)
        self.add_widget(self.rollAgainButton)
        self.add_widget(self.confirmButton)
        self.add_widget(self.cancelButton)
        self.char = char

    def on_size(self, *args):
        self.rollAgainButton.size = self.height / 4, self.height / 6
        self.rollAgainButton.pos = self.height / 5.4 - self.rollAgainButton.width / 2, self.height / 2 - self.rollAgainButton.height / 2
        self.confirmButton.size = self.height / 4, self.height / 6
        self.confirmButton.pos = self.width - self.height / 5.4 - self.confirmButton.width / 2, self.height / 2
        self.cancelButton.size = self.height / 4, self.height / 6
        self.cancelButton.pos = self.width - self.height / 5.4 - self.cancelButton.width / 2, self.height / 2 - self.rollAgainButton.height

    def onRollAgain(self, instance, touch):
        if instance.collide_point(*touch.pos):
            notobtained = False
            while not notobtained:
                index = random.randint(0, len(self.main_screen.characters) - 1)
                print(str(index))
                print(str(self.main_screen.obtained_characters))
                notobtained = index not in self.main_screen.obtained_characters
            print(str(self.main_screen.characters[index].get_name()))
            preview = RecruitPreview(self.main_screen, self.main_screen.characters[index])
            self.main_screen.transition = RiseInTransition(duration=.3)
            self.main_screen.display_screen(preview, True, False)

    def onConfirm(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.main_screen.obtained_characters.append(self.char.get_index())
            if self.char.is_support():
                self.main_screen.obtained_characters_s.append(self.char.get_index())
            else:
                self.main_screen.obtained_characters_a.append(self.char.get_index())
            self.main_screen.display_screen(None, False, False)

    def onCancel(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.main_screen.display_screen(None, False, False)