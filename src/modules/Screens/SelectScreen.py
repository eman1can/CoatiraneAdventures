from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty

from src.modules.CustomHoverableButton import CustomHoverableButton

class SelectScreen(Screen):
    font_size = NumericProperty(150)
    font_size2 = NumericProperty(75)
    title_x = NumericProperty(500)

    def __init__(self, main_screen, **kwargs):
        super(SelectScreen, self).__init__(**kwargs)
        self.main_screen = main_screen
        self.id = 'select_screen'
        self.name = 'select_screen'
        self.newgamebell = CustomHoverableButton(size=(600, 600), pos=(200, 200), path='../res/screens/buttons/newgame.bell')
        self.newgamebell.bind(on_touch_down=lambda instance, touch: self.chooseCharacter(instance, touch, 'hero_bell'))
        self.newgameais = CustomHoverableButton(size=(600, 600), pos=(200, 200), path='../res/screens/buttons/newgame.ais')
        self.newgameais.bind(on_touch_down=lambda instance, touch: (self.chooseCharacter(instance, touch, 'badass_ais')))
        self.add_widget(self.newgamebell)
        self.add_widget(self.newgameais)

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
        self.font_size = self.height / 9.6
        self.font_size2 = self.height / 19.2
        self.newgameais.size = self.height / 2.22, self.height / 2.22
        self.newgameais.pos = self.width / 3 - self.newgameais.width / 2, self.height * 2 / 8
        self.newgamebell.size = self.height / 2.22, self.height / 2.22
        self.newgamebell.pos = self.width * 2 / 3 - self.newgameais.width / 2, self.height * 2 / 8
        self.title_x = self.width / 4

        # Name, ID, Health, Defense, Physical Attack, magical Attack, Mana, Strength, Magic, Endurance, Agility, Dexterity, Slide Image, Square Image, Full Image

        # Lena | fanciful_lena
        # Min: H 110 M 0 Str 20 Mag 0 End 14 Agi 15 Dex 16 | MAtk 10 PAtk 20 Defense 14
        # Max: H 3432 M 0 Str 1220 Mag 0 End 414 Agi 512 Dex 467 | MAtk 315 PAtk 1220 Defense 414
        # Physical Type
        # Base: Foe: Lo Physical Attack w/ 5% stun
        # 1) Foes: Mid Physical Attack && Foes: Str -10%
        # 2) Foes: High Physical Attack w/ temp Str Boost
        # 3) Allies: Str +50% && Self Str +75% for 2 turns
        # Special: Ultra Physical Attack with temp Str Boost && Allies +10% to health of damage
        # For Each Rank -> I to S
        # For Each  Rank -> Level 0 -> 50
        # For each Rank, Attribute star w/ unlocks by Gems
        # For Each Rank, you choose an ability
