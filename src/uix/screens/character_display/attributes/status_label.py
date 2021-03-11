# Kivy Imports
from kivy.properties import ListProperty, NumericProperty, StringProperty

from kivy.uix.relativelayout import RelativeLayout
# KV Import
from loading.kv_loader import load_kv

load_kv(__name__)


class AttackLabel(RelativeLayout):
    padding = ListProperty([0, 0, 0, 0, 0, 0, 0, 0])

    title = StringProperty('')
    title_font_size = NumericProperty(0.00)

    body = StringProperty('')
    body_font_size = NumericProperty(0.00)

    cost = StringProperty('')
    cost_font_size = NumericProperty(0.00)

    type_source = StringProperty('')


class ComboAttackLabel(RelativeLayout):
    pass


class SkillLabel(RelativeLayout):
    padding = ListProperty([0, 0, 0, 0, 0, 0, 0, 0])

    title = StringProperty('')
    title_font_size = NumericProperty(0.00)

    body = StringProperty('')
    body_font_size = NumericProperty(0.00)
