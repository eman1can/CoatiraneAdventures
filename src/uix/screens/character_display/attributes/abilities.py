# Kivy Imports
from kivy.properties import BooleanProperty, NumericProperty, StringProperty

from kivy.uix.relativelayout import RelativeLayout
# KV Import
from loading.kv_loader import load_kv

load_kv(__name__)


class ASBox(RelativeLayout):
    locked = BooleanProperty(True)
    unlocked = BooleanProperty(False)
    body = StringProperty('')

    def __init__(self, **kwargs):
        self.register_event_type('on_touch')
        super().__init__(**kwargs)

    def on_touch(self, *args):
        pass


class AbilityBox(ASBox):
    set = BooleanProperty(False)
    name = StringProperty('')


class AbilityChoice(RelativeLayout):
    choice_id = NumericProperty(0.0)
    title = StringProperty('')
    body = StringProperty('')

    def __init__(self, ability, **kwargs):
        self.register_event_type('on_choice')
        super().__init__(**kwargs)
        self.title = ability.name
        self.body = ability.description

    def on_choice(self, choice_id):
        pass


class SkillBox(ASBox):
    name = StringProperty('')
