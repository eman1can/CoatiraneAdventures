from kivy.app import App
from kivy.core.image import Image
from kivy.properties import StringProperty, ObjectProperty
from src.modules.KivyBase.Hoverable import ScreenH as Screen

# THESE IMPORTS ARE REQUIRED! Otherwise the kivy factory will not recognize them!
from src.modules.Screens.CharacterAttributeScreens.EquipmentSlot import EquipmentSlot
from src.modules.Screens.CharacterAttributeScreens.AbilityStatBox import AbilityStatBox
from src.modules.Screens.CharacterAttributeScreens.StatBox import StatBox
from src.modules.Screens.CharacterAttributeScreens.StatusBoard import StatusBoardManager


class CharacterAttributeScreen(Screen):
    preview = ObjectProperty(None, allownone=True)
    char = ObjectProperty(None, allownone=True)

    background_texture = ObjectProperty(None)
    char_image_source = StringProperty('')
    overlay_background_source = StringProperty("../res/screens/attribute/stat_background.png")
    overlay_source = StringProperty("../res/screens/attribute/stat_background_overlay.png")
    flag_source = StringProperty("../res/screens/attribute/char_type_flag.png")
    type_flag_source = StringProperty('')
    element_flag_source = StringProperty('')
    element_flag_image_source = StringProperty('')
    overlay_bar_source = StringProperty("../res/screens/stats/overlay_bar.png")
    neat_stat_overlay_source = StringProperty("../res/screens/attribute/stat_overlay.png")

    def __init__(self, **kwargs):
        #Overlay's and backgrounds
        self.background_texture = Image("../res/screens/backgrounds/background.png").texture
        super().__init__(**kwargs)

        self.char_image_source = self.char.full_image_source
        self.type_flag_source = "../res/screens/recruit/" + str(self.char.get_type()).lower() + "_flag.png"
        self.element_flag_source = "../res/screens/attribute/" + self.char.get_element().lower() + "_flag.png"
        self.element_flag_image_source = "../res/screens/attribute/" + self.char.get_element().lower() + ".png"

    def on_mouse_pos(self, hover):
        if self.ids.image_preview.dispatch('on_mouse_pos', hover):
            return True
        if self.ids.change_equip.dispatch('on_mouse_pos', hover):
            return True
        if self.ids.status_board.dispatch('on_mouse_pos', hover):
            return True
        return False

    def reload(self):
        pass

    def on_image_preview(self):
        pass

    def on_status_board(self):
        self.ids.status_board_screen.size = self.size
        App.get_running_app().main.display_screen(self.ids.status_board_screen, True, True)

    def on_change_equip(self):
        pass

    def on_back_press(self):
        root = App.get_running_app().main
        if root is not None:
            root.display_screen(None, False, False)
