from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.properties import NumericProperty
from kivy.graphics import Color, Rectangle
from src.modules.HTButton import HTButton

class SelectScreen(Screen):
    font_size = NumericProperty(150)
    font_size2 = NumericProperty(75)
    title_x = NumericProperty(500)

    def __init__(self, main_screen, **kwargs):
        self.initalized = False
        super(SelectScreen, self).__init__(**kwargs)
        self.main_screen = main_screen
        self.name = 'select_screen'

        self.title = Label(text="Select a Character!", font_size=self.main_screen.width * .075, size_hint=(None, None), color=(.8, .8, .8, 1), font_name='../res/fnt/Precious.ttf')
        self.title._label.refresh()
        self.title.size = self.title._label.texture.size
        self.title.pos = (self.main_screen.width - self.title.width) / 2, self.main_screen.height * .85 - self.title.height / 2

        button_size = self.main_screen.width * .25, self.main_screen.width * .25
        button_pos = self.main_screen.width * .5 / 3, (self.main_screen.height - self.main_screen.width * .25) / 2
        self.newgamebell = HTButton(size=button_size, pos=button_pos, size_hint=(None, None), path='../res/screens/buttons/newgame.bell')
        self.newgamebell.bind(on_touch_down=lambda instance, touch: self.chooseCharacter(instance, touch, 'hero_bell'))
        self.newgameais = HTButton(size=button_size, pos=(button_pos[0] * 2 + button_size[0], button_pos[1]), size_hint=(None, None), path='../res/screens/buttons/newgame.ais')
        self.newgameais.bind(on_touch_down=lambda instance, touch: (self.chooseCharacter(instance, touch, 'badass_ais')))

        self.newgamebell_label = Label(text="Rabbit Foot", font_size=self.main_screen.width * .05, size_hint=(None, None), color=(1, 1, 1, 1), font_name='../res/fnt/Precious.ttf')
        self.newgamebell_label._label.refresh()
        self.newgamebell_label.size = self.newgamebell_label._label.texture.size
        self.newgamebell_label.pos = self.main_screen.width * .5 / 3 * 2 + button_size[0] + (self.main_screen.width * .25 - self.newgamebell_label.width) / 2, (self.main_screen.height - self.main_screen.width * .25) / 2 - self.newgamebell_label.height * 1.75

        self.newgameais_label = Label(text="Battle Princess", font_size=self.main_screen.width * .05, size_hint=(None, None), color=(1, 1, 1, 1), font_name='../res/fnt/Precious.ttf')
        self.newgameais_label._label.refresh()
        self.newgameais_label.size = self.newgameais_label._label.texture.size
        self.newgameais_label.pos = self.main_screen.width * .5 / 3 + (self.main_screen.width * .25 - self.newgameais_label.width) / 2, (self.main_screen.height - self.main_screen.width * .25) / 2 - self.newgameais_label.height * 1.75

        self.add_widget(self.title)
        self.add_widget(self.newgamebell)
        self.add_widget(self.newgameais)
        self.add_widget(self.newgamebell_label)
        self.add_widget(self.newgameais_label)
        self.initalized = True

    def chooseCharacter(self, instance, touch, choice):
        if instance.collide_point(*touch.pos):
            print('Chosen Character: %s, adding to char Array.' % choice)
            self.bind(size=self.on_size)
            for x in self.main_screen.characters:
                if x.get_index() > 2 and x.get_id() != 'enticing_misha':
                    self.main_screen.obtained_characters.append(x.get_index())
                    if x.is_support():
                        self.main_screen.obtained_characters_s.append(x.get_index())
                    else:
                        self.main_screen.obtained_characters_a.append(x.get_index())
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
                    self.main_screen.create_screen('town')
                    return True

    def on_size(self, *args):
        if not self.initalized:
            return
        self.title.font_size = self.main_screen.width * .075
        self.title._label.refresh()
        self.title.size = self.title._label.texture.size
        self.title.pos = (self.main_screen.width - self.title.width) / 2, self.main_screen.height * .85 - self.title.height / 2

        button_size = self.main_screen.width * .25, self.main_screen.width * .25
        button_pos = self.main_screen.width * .5 / 3, (self.main_screen.height - self.main_screen.width * .25) / 2
        self.newgameais.size = button_size
        self.newgameais.pos = button_pos
        self.newgamebell.size = button_size
        self.newgamebell.pos = button_pos[0] * 2 + button_size[0], button_pos[1]

        self.newgamebell_label.font_size = self.main_screen.width * .05
        self.newgamebell_label._label.refresh()
        self.newgamebell_label.size = self.newgamebell_label._label.texture.size
        self.newgamebell_label.pos = self.main_screen.width * .5 / 3 * 2 + button_size[0] + (self.main_screen.width * .25 - self.newgamebell_label.width) / 2, (self.main_screen.height - self.main_screen.width * .25) / 2 - self.newgamebell_label.height * 1.75

        self.newgameais_label.font_size = self.main_screen.width * .05
        self.newgameais_label._label.refresh()
        self.newgameais_label.size = self.newgameais_label._label.texture.size
        self.newgameais_label.pos = self.main_screen.width * .5 / 3 + (self.main_screen.width * .25 - self.newgameais_label.width) / 2, (self.main_screen.height - self.main_screen.width * .25) / 2 - self.newgameais_label.height * 1.75
