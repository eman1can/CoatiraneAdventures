from kivy.app import App
from kivy.core.image import Image
from kivy.properties import ObjectProperty

from src.modules.KivyBase.Hoverable import ScreenBase as Screen


class NewGameScreen(Screen):
    title_texture = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        self.title_texture = Image('../res/screens/backgrounds/Title.png').texture
        super(NewGameScreen, self).__init__(**kwargs)

    def on_new_game(self):
        App.get_running_app().main.display_screen('select_screen', True, False)

    def on_load_game(self):
        pass
