from src.modules.KivyBase.Hoverable import RelativeLayoutH as RelativeLayout
from kivy.properties import StringProperty, NumericProperty, ListProperty

class AttackLabel(RelativeLayout):
    padding = ListProperty([0, 0, 0, 0, 0, 0, 0, 0])

    title = StringProperty('')
    title_font_size = NumericProperty(0.00)

    body = StringProperty('')
    body_font_size = NumericProperty(0.00)

    cost = StringProperty('')
    cost_font_size = NumericProperty(0.00)

    type_source = StringProperty('')



    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ComboAttackLabel(RelativeLayout):
    pass


class SkillLabel(RelativeLayout):
    padding = ListProperty([0, 0, 0, 0, 0, 0, 0, 0])

    title = StringProperty('')
    title_font_size = NumericProperty(0.00)

    body = StringProperty('')
    body_font_size = NumericProperty(0.00)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)