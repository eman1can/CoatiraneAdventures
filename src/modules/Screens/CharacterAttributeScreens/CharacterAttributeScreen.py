from kivy.app import App
from kivy.properties import StringProperty, ObjectProperty
from src.modules.KivyBase.Hoverable import ScreenBase as Screen


class CharacterAttributeScreen(Screen):
    preview = ObjectProperty(None, allownone=True)
    char = ObjectProperty(None, allownone=True)

    overlay_background_source = StringProperty("../res/screens/attribute/stat_background.png")
    overlay_source = StringProperty("../res/screens/attribute/stat_background_overlay.png")
    flag_source = StringProperty("../res/screens/attribute/char_type_flag.png")
    overlay_bar_source = StringProperty("../res/screens/stats/overlay_bar.png")
    neat_stat_overlay_source = StringProperty("../res/screens/attribute/stat_overlay.png")
    skills_switch_text = StringProperty('Skills')

    def on_touch_hover(self, touch):
        if self.ids.image_preview.dispatch('on_touch_hover', touch):
            return True
        if self.ids.change_equip.dispatch('on_touch_hover', touch):
            return True
        if self.ids.status_board.dispatch('on_touch_hover', touch):
            return True
        return False

    def on_image_preview(self):
        screen, made = App.get_running_app().main.create_screen('image_preview_' + self.char.get_name(), self.char)
        App.get_running_app().main.display_screen(screen, True, True)

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
        screen, made = App.get_running_app().main.create_screen('equipment_change_' + self.char.get_name(), self.char)
        App.get_running_app().main.display_screen(screen, True, True)
