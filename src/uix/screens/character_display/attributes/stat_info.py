# Kivy Imports
from kivy.properties import StringProperty

from kivy.uix.relativelayout import RelativeLayout
# KV Import
from loading.kv_loader import load_kv

load_kv(__name__)


class StatInfoBox(RelativeLayout):
    flag_source = StringProperty('screens/attributes/char_type_flag.png')
    type_flag_source = StringProperty('')
    element_flag_source = StringProperty('')
    element_flag_image_source = StringProperty('')
    overlay_bar_source = StringProperty('screens/stats/overlay_bar.png')

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
