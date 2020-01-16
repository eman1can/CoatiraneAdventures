from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.image import Image

from src.modules.HTButton import HTButton


class SelectScreen(Screen):
    def __init__(self, main_screen, **kwargs):
        self.initalized = False
        super(SelectScreen, self).__init__(**kwargs)

        self.name = 'select_screen'
        self.main_screen = main_screen

        self._size = (0, 0)

        self.background = Image(source='../res/screens/backgrounds/background.png', allow_stretch=True)

        self.title = Label(text="Select a Character!", size_hint=(None, None), color=(.8, .8, .8, 1), font_name='../res/fnt/Precious.ttf', outline_width=1, outline_color=(0, 0, 0, .75))

        self.new_game_bell = HTButton(size_hint=(None, None), path='../res/screens/buttons/newgame.bell', on_touch_down=lambda instance, touch: self.choose_character(instance, touch, 'hero_bell'))
        self.new_game_ais = HTButton(size_hint=(None, None), path='../res/screens/buttons/newgame.ais', on_touch_down=lambda instance, touch: (self.choose_character(instance, touch, 'badass_ais')))

        self.new_game_bell_label = Label(text="Rabbit Foot", size_hint=(None, None), font_name='../res/fnt/Precious.ttf', outline_width=0.25, outline_color=(1, 0, 0, .75))
        self.new_game_ais_label = Label(text="Battle Princess", size_hint=(None, None), font_name='../res/fnt/Precious.ttf', outline_width=0.25, outline_color=(0, 0, 1, .75))

        self.add_widget(self.background)
        self.add_widget(self.title)
        self.add_widget(self.new_game_bell)
        self.add_widget(self.new_game_ais)
        self.add_widget(self.new_game_bell_label)
        self.add_widget(self.new_game_ais_label)
        self.initalized = True

    def choose_character(self, instance, touch, choice):
        if instance.collide_point(*touch.pos):
            print('Chosen Character: %s, adding to char Array.' % choice)
            # for x in self.main_screen.characters:
            #     if x.get_index() > 2 and x.get_id() != 'enticing_misha':
            #         self.main_screen.obtained_characters.append(x.get_index())
            #         if x.is_support():
            #             self.main_screen.obtained_characters_s.append(x.get_index())
            #         else:
            #             self.main_screen.obtained_characters_a.append(x.get_index())
            char = support = False
            for x in self.main_screen.characters:
                id = x.get_id()
                if id == choice:
                    x.first = True
                    self.main_screen.obtained_characters.append(x.get_index())
                    self.main_screen.obtained_characters_a.append(x.get_index())
                    char = True
                if id == 'enticing_misha':
                    self.main_screen.obtained_characters.append(x.get_index())
                    self.main_screen.obtained_characters_s.append(x.get_index())
                    support = True
                if char and support:
                    self.main_screen.display_screen('town_screen', True, False)
                    return

    def on_size(self, instance, size):
        if not self.initalized or self._size == size:
            return
        self._size = size.copy()

        self.title.font_size = self.main_screen.width * 0.075
        self.title.texture_update()
        self.title.size = self.title.texture_size
        self.title.pos = (self.main_screen.width - self.title.width) / 2, self.main_screen.height * 0.85 - self.title.height / 2

        button_size = self.main_screen.width * 0.25, self.main_screen.width * 0.25
        button_pos = self.main_screen.width * 0.5 / 3, (self.main_screen.height - self.main_screen.width * 0.25) / 2
        self.new_game_ais.size = button_size
        self.new_game_ais.pos = button_pos
        self.new_game_bell.size = button_size
        self.new_game_bell.pos = button_pos[0] * 2 + button_size[0], button_pos[1]

        self.new_game_bell_label.font_size = self.main_screen.width * 0.05
        self.new_game_bell_label.texture_update()
        self.new_game_bell_label.size = self.new_game_bell_label.texture_size
        self.new_game_bell_label.pos = self.main_screen.width / 3 + button_size[0] + (self.main_screen.width * 0.25 - self.new_game_bell_label.width) / 2, (self.main_screen.height - self.main_screen.width * 0.25) / 2 - self.new_game_bell_label.height * 1.75

        self.new_game_ais_label.font_size = self.main_screen.width * 0.05
        self.new_game_ais_label.texture_update()
        self.new_game_ais_label.size = self.new_game_ais_label.texture_size
        self.new_game_ais_label.pos = self.main_screen.width * 0.5 / 3 + (self.main_screen.width * 0.25 - self.new_game_ais_label.width) / 2, (self.main_screen.height - self.main_screen.width * 0.25) / 2 - self.new_game_ais_label.height * 1.75
