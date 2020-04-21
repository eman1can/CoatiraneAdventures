from src.modules.KivyBase.Hoverable import ScreenH as Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.app import App


class ImagePreview(Screen):
    char = ObjectProperty(None)
    background_source = StringProperty("../res/screens/backgrounds/background.png")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_back_press(self):
        root = App.get_running_app().main
        if root is not None:
            root.display_screen(None, False, False)