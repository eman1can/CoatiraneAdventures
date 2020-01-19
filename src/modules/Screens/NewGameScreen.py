from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image

from src.modules.HTButton import HTButton


class NewGameScreen(Screen):
    initialized = BooleanProperty(False)
    main_screen = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(NewGameScreen, self).__init__(**kwargs)

        self.name = 'new_game'

        self._size = (0, 0)

        self.background = Image(source='../res/screens/backgrounds/newgamebackground.png', allow_stretch=True)
        self.title = Image(source='../res/screens/backgrounds/Title.png', allow_stretch=True, size_hint=(None, None))

        self.new_game = HTButton(size_hint=(None, None), path='../res/screens/buttons/newgame', on_release=self.on_new_game)
        self.load_game = HTButton(size_hint=(None, None), path='../res/screens/buttons/loadgame', on_release=self.on_load_game)

        self.add_widget(self.background)
        self.add_widget(self.new_game)
        self.add_widget(self.load_game)
        self.add_widget(self.title)
        self.initialized = True

    def on_new_game(self, instance):
        self.main_screen.display_screen('select_screen', True, False)

    def on_load_game(self, instance):
        pass

    def on_size(self, instance, size):
        if not self.initialized or self._size == size:
            return
        self._size = size.copy()

        self.title.size = self.width / 1.5, self.height / 2.14
        self.title.pos = self.width * .05, self.height * .43

        self.new_game.size = self.width / 3, self.height / 3.25
        self.new_game.pos = (self.width / 2) - self.new_game.width - self.width / 12, self.height * .12

        self.load_game.size = self.width / 3, self.height / 3.25
        self.load_game.pos = (self.width / 2) + self.width / 12, self.height * .12
