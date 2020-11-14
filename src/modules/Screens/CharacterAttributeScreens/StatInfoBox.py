from kivy.properties import StringProperty
from src.modules.KivyBase.Hoverable import RelativeLayoutBase as RelativeLayout


class StatInfoBox(RelativeLayout):
    flag_source = StringProperty("../res/screens/attribute/char_type_flag.png")
    type_flag_source = StringProperty('')
    element_flag_source = StringProperty('')
    element_flag_image_source = StringProperty('')
    overlay_bar_source = StringProperty("../res/screens/stats/overlay_bar.png")

    char_type = StringProperty('')
    char_stype = StringProperty('')
    char_element = StringProperty('')
    char_display_name = StringProperty('')
    char_name = StringProperty('')
    skills_switch_text = StringProperty('')

    def __init__(self, **kwargs):
        self.register_event_type('on_skills_switch')
        super().__init__(**kwargs)

    def on_skills_switch(self):
        pass
