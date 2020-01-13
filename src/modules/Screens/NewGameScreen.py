from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from src.modules.CustomHoverableButton import CustomHoverableButton

class NewGameScreen(Screen):

    def __init__(self, main_screen, **kwargs):
        super(NewGameScreen, self).__init__(**kwargs)
        self.id = 'new_game'
        self.name = 'new_game'
        self.main_screen = main_screen
        self.bind(size=self.on_size)
        self.background = Image(source='../res/screens/backgrounds/newgamebackground.png', keep_ratio=False, allow_stretch=True,
                                size_hint=(None, None))
        self.newgame = CustomHoverableButton(size=(750, 350), pos=(100, 100), path='../res/screens/buttons/newgame')
        self.newgame.bind(on_touch_down=self.on_new_game)
        self.loadgame = CustomHoverableButton(size=(750, 350), pos=(800, 100),  path='../res/screens/buttons/loadgame', background_disabled_normal=True)
        self.title = Image(source='../res/screens/backgrounds/Title.png', keep_ratio=True, allow_stretch=True, size_hint=(None, None))

        self.loadgame.disabled = True
        self.add_widget(self.background)
        self.add_widget(self.newgame)
        self.add_widget(self.loadgame)
        self.add_widget(self.title)

    def on_new_game(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.main_screen.create_screen('select')

    def on_load_game(self, *args):
        pass

    def on_size(self, *args):
        self.background.size = self.width, self.height
        self.newgame.size = self.width / 3, self.height / 3.25
        self.newgame.pos = (self.width / 2) - self.newgame.width - self.width / 12, self.height * .12
        self.loadgame.size = self.width / 3, self.height / 3.25
        self.loadgame.pos = (self.width / 2) + self.width / 12, self.height * .12
        self.title.size = self.width / 1.5, self.height / 2.14
        self.title.pos = self.width * .05, self.height * .43
