from kivy.properties import StringProperty, ListProperty, NumericProperty
from src.modules.KivyBase.Hoverable import RelativeLayoutH as RelativeLayout


class AbilityStatBox(RelativeLayout):

    color = ListProperty([0, 0, 0, 1])
    font = StringProperty('')

    strength = NumericProperty(0.0)
    strength_path = StringProperty('')
    magic = NumericProperty(0.0)
    magic_path = StringProperty('')
    endurance = NumericProperty(0.0)
    endurance_path = StringProperty('')
    dexterity = NumericProperty(0.0)
    dexterity_path = StringProperty('')
    agility = NumericProperty(0.0)
    agility_path = StringProperty('')

    background_source = StringProperty('')

    def __init__(self, **kwargs):
        self.background_source = "../res/screens/attribute/ability_overlay.png"
        super().__init__(**kwargs)
