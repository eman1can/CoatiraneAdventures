from kivy.app import App
from kivy.core.image import Image
from kivy.properties import StringProperty, ObjectProperty
from src.modules.KivyBase.Hoverable import ScreenH as Screen


class CharacterAttributeScreen(Screen):
    preview = ObjectProperty(None, allownone=True)
    char = ObjectProperty(None, allownone=True)

    background_texture = ObjectProperty(None)
    overlay_background_source = StringProperty("../res/screens/attribute/stat_background.png")
    overlay_source = StringProperty("../res/screens/attribute/stat_background_overlay.png")
    flag_source = StringProperty("../res/screens/attribute/char_type_flag.png")
    overlay_bar_source = StringProperty("../res/screens/stats/overlay_bar.png")
    neat_stat_overlay_source = StringProperty("../res/screens/attribute/stat_overlay.png")
    skills_switch_text = StringProperty('Skills')

    def __init__(self, **kwargs):
        #Overlay's and backgrounds
        self.background_texture = Image("../res/screens/backgrounds/background.png").texture
        super().__init__(**kwargs)

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

    def on_leave(self, *args):
        if self.skills_switch_text == 'Status':
            self.on_skills_switch()

    def on_status_board(self):
        screen, made = App.get_running_app().main.create_screen('status_board_' + self.char.get_name(), self.char)
        App.get_running_app().main.display_screen(screen, True, True)

    def on_skills_switch(self):
        if self.skills_switch_text == 'Skills':
            self.skills_switch_text = 'Status'
        else:
            self.skills_switch_text = 'Skills'
        self.ids.normal_layout.opacity = int(not bool(int(self.ids.normal_layout.opacity)))
        self.ids.skill_layout.opacity = int(not bool(int(self.ids.skill_layout.opacity)))
        self.ids.skillslist.scroll_y = 1
        self.ids.skillslist.update_from_scroll()

    def on_change_equip(self):
        pass

    def on_back_press(self):
        root = App.get_running_app().main
        if root is not None:
            root.display_screen(None, False, False)
