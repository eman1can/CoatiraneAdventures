from src.modules.KivyBase.Hoverable import ScreenH as Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.app import App


class EquipmentChange(Screen):
    char = ObjectProperty()

    weapon = ObjectProperty(None, allownone=True)
    helmet = ObjectProperty(None, allownone=True)
    chest = ObjectProperty(None, allownone=True)
    grieves = ObjectProperty(None, allownone=True)
    boots = ObjectProperty(None, allownone=True)
    vambraces = ObjectProperty(None, allownone=True)
    gloves = ObjectProperty(None, allownone=True)
    necklace = ObjectProperty(None, allownone=True)
    ring = ObjectProperty(None, allownone=True)

    background_source = StringProperty("../res/screens/backgrounds/background.png")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_back_press(self):
        root = App.get_running_app().main
        if root is not None:
            root.display_screen(None, False, False)

