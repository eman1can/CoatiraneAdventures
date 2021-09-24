# Kivy Imports
from kivy.properties import StringProperty

from kivy.uix.relativelayout import RelativeLayout
# KV Import
from loading.kv_loader import load_kv

load_kv(__name__)


class StatInfoBox(RelativeLayout):
    char_flag = StringProperty('adventurer')
    type_flag = StringProperty('physical')
    element_flag = StringProperty('wind')

    overlay_bar_source = StringProperty('screens/stats/overlay_bar.png')

    char_display_name = StringProperty('')
    char_name = StringProperty('')
    skills_switch_text = StringProperty('')

    def __init__(self, **kwargs):
        self.register_event_type('on_skills_switch')
        super().__init__(**kwargs)

    def on_skills_switch(self):
        pass
