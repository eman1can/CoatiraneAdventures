from kivy.properties import ObjectProperty, BooleanProperty, ListProperty
from kivy.uix.screenmanager import Screen, FadeTransition
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader

from src.modules.HTButton import HTButton
from src.modules.NoRecruit import NoRecruitWidget

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

        self.background = Image(source="../res/screens/backgrounds/background.png", allow_stretch=True)

        self.image = self.character.get_full_image(False)
        self.full_name = Label(text="[b]" + self.character.get_name() + "[/b]", markup=True, color=(1, 1, 1, 1), font_name="../res/fnt/Precious.ttf", size_hint=(None, None), outline_width=2, outline_color=(0, 0, 0, 1))
        self.display_name = Label(text="[b]" + self.character.get_display_name() + "[/b]", markup=True, color=(1, 1, 1, 1), font_name="../res/fnt/Precious.ttf", size_hint=(None, None), outline_width=2, outline_color=(0, 0, 0, 1))

        self.char_type_flag = Image(source="../res/screens/recruit/char_type_flag.png", allow_stretch=True, size_hint=(None, None))
        if self.character.is_support():
            text = "Supporter"
        else:
            text = "Adventurer"
        self.char_type_flag_label = Label(text=text, color=(1, 1, 1, 1), font_name="../res/fnt/Gabriola.ttf", size_hint=(None, None))
        self.type_flag = Image(source="../res/screens/recruit/" + self.character.get_type().lower() + "_flag.png", allow_stretch=True, size_hint=(None, None))
        self.type_flag_label = Label(text=self.character.get_type().capitalize() + " Type", color=(1, 1, 1, 1), font_name="../res/fnt/Gabriola.ttf", size_hint=(None, None))

        self.element_flag_background = Image(source="../res/screens/attribute/" + self.character.get_element().lower() + "_flag.png", allow_stretch=True, size_hint=(None, None))
        self.element_flag_label = Label(text=self.character.get_element().capitalize(), color=(0, 0, 0, 1), font_name="../res/fnt/Gabriola.ttf", size_hint=(None, None))
        self.element_flag_image = Image(source="../res/screens/attribute/" + self.character.get_element().lower() + ".png", allow_stretch=True, size_hint=(None, None))

        self.roll_again = HTButton(path='../res/screens/buttons/recruit_button', size_hint=(None, None), collide_image="../res/screens/buttons/largebutton.collision.png", text="Roll Again", font_name='../res/fnt/Precious.ttf', label_color=(1, 1, 1, 1), on_release=self.on_roll_again)
        self.confirm = HTButton(path='../res/screens/buttons/recruit_button_confirm', size_hint=(None, None), collide_image="../res/screens/buttons/largebutton.collision.png", text="Confirm", font_name='../res/fnt/Precious.ttf', label_color=(1, 1, 1, 1), on_release=self.on_confirm)
        self.cancel = HTButton(path='../res/screens/buttons/recruit_button_cancel', size_hint=(None, None), collide_image="../res/screens/buttons/largebutton.collision.png", text="Cancel", font_name='../res/fnt/Precious.ttf', label_color=(1, 1, 1, 1), on_release=self.on_cancel)
        self.character_attribute = HTButton(path='../res/screens/buttons/character_attribute', size_hint=(None, None), collide_image="../res/screens/buttons/largebutton.collision.png", text="Attributes", font_name='../res/fnt/Precious.ttf', label_color=(1, 1, 1, 1), on_release=self.on_char_attribute)

        self.no_recruits = NoRecruitWidget()

        self.sound = SoundLoader.load('../res/snd/recruit.wav')

        self.add_widget(self.background)
        self.add_widget(self.image)
        self.add_widget(self.full_name)
        self.add_widget(self.display_name)
        self.add_widget(self.char_type_flag)
        self.add_widget(self.char_type_flag_label)
        self.add_widget(self.type_flag)
        self.add_widget(self.type_flag_label)
        self.add_widget(self.element_flag_background)
        self.add_widget(self.element_flag_label)
        self.add_widget(self.element_flag_image)
        self.add_widget(self.roll_again)
        self.add_widget(self.confirm)
        self.add_widget(self.cancel)
        self.add_widget(self.character_attribute)
        self.initialized = True

    def on_size(self, instance, size):
        if not self.initialized or self._size == size:
            return
        self._size = size.copy()

        ratio = 150 / 575

        self.background.size = self.size
        self.no_recruits.size = self.size

        self.full_name.font_size = self.height * 0.125
        self.full_name.texture_update()
        self.full_name.size = self.full_name.texture_size
        self.full_name.pos = self.display_name.width / 4, self.height - (self.full_name.height * 1.25)

        self.display_name.font_size = self.height * 0.075
        self.display_name.texture_update()
        self.display_name.size = self.display_name.texture_size
        self.display_name.pos = self.display_name.width / 4, self.height - (self.display_name.height * 1.25 + self.full_name.height)

        self.image.size = (self.display_name.y * self.image.image_ratio, self.display_name.y)
        # self.image.pos = (-(self.width - self.image.image_ratio * self.height) / 2, 0)

        self.char_type_flag.size = self.width * 0.275, self.width * 0.33 * ratio
        self.char_type_flag.pos = self.width - self.char_type_flag.width, self.height - self.char_type_flag.height * 1.25
        self.char_type_flag_label.font_size = self.width * 0.30 * ratio * 0.55
        self.char_type_flag_label.size = self.width * 0.275 * 0.83, self.width * 0.33 * ratio * 0.85
        self.char_type_flag_label.pos = self.width - self.char_type_flag_label.width, self.height - self.char_type_flag.height * 1.25 + self.char_type_flag.height * 0.15

        self.type_flag.size = self.width * 0.275, self.width * 0.33 * ratio
        self.type_flag.pos = self.width - self.type_flag.width, self.char_type_flag.y - self.type_flag.height * 1.25
        self.type_flag_label.font_size = self.width * 0.30 * ratio * 0.55
        self.type_flag_label.size = self.width * 0.275 * 0.83, self.width * 0.33 * ratio * 0.85
        self.type_flag_label.pos = self.width - self.type_flag_label.width, self.char_type_flag.y - self.type_flag.height * 1.25 + self.type_flag.height * 0.15

        element_flag_size = (self.height - self.type_flag.y) * 150 / 400, self.height - self.type_flag.y
        element_flag_pos = self.type_flag.x - element_flag_size[0] * 1.5, self.type_flag.y
        self.element_flag_background.size = element_flag_size
        self.element_flag_background.pos = element_flag_pos
        self.element_flag_label.font_size = element_flag_size[1] * 0.1
        self.element_flag_label.size = element_flag_size[0], element_flag_size[1] * 0.6
        self.element_flag_label.pos = element_flag_pos[0], element_flag_pos[1] + element_flag_size[1] * 0.4
        self.element_flag_image.size = element_flag_size[0] * 0.3, element_flag_size[0] * 0.3
        self.element_flag_image.pos = element_flag_pos[0] + element_flag_size[0] * 0.35, element_flag_pos[1] + element_flag_size[0] * 0.65

        button_size = self.type_flag.y * 0.2 * 1016 / 716, self.type_flag.y * 0.2
        self.roll_again.size = button_size
        self.roll_again.pos = self.width - button_size[0] * 1.25, button_size[1] * 0.2 + button_size[1] * 3
        self.roll_again.font_size = button_size[1] * 0.1875
        self.roll_again.label_padding = [0, button_size[1] * 0.4, 0, 0]

        self.confirm.size = button_size
        self.confirm.pos = self.width - button_size[0] * 1.25, button_size[1] * 0.15 + button_size[1] * 2
        self.confirm.font_size = button_size[1] * 0.1875
        self.confirm.label_padding = [0, button_size[1] * 0.4, 0, 0]

        self.cancel.size = button_size
        self.cancel.pos = self.width - button_size[0] * 1.25, button_size[1] * 0.1 + button_size[1]
        self.cancel.font_size = button_size[1] * 0.1875
        self.cancel.label_padding = [0, button_size[1] * 0.4, 0, 0]

        self.character_attribute.size = button_size
        self.character_attribute.pos = self.width - button_size[0] * 1.25, button_size[1] * 0.05
        self.character_attribute.font_size = button_size[1] * 0.1875
        self.character_attribute.label_padding = [0, button_size[1] * 0.4, 0, 0]

    def on_roll_again(self, instance):
        if len(self.main_screen.characters) == len(self.main_screen.obtained_characters) + len(self.viewed_characters):
            self.add_widget(self.no_recruits)
        else:
            unobtained_characters = [char for char in self.main_screen.characters if char.index not in self.main_screen.obtained_characters and char not in self.viewed_characters]
            index = random.randint(0, len(unobtained_characters) - 1)
            self.viewed_characters.append(unobtained_characters[index])
            self.main_screen.create_screen('recruit', unobtained_characters[index], self.viewed_characters)
            self.sound.play()
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

    def on_char_attribute(self, instance):
        pass