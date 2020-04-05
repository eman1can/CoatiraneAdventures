from kivy.properties import StringProperty, ListProperty, NumericProperty
from src.modules.KivyBase.Hoverable import RelativeLayoutH as RelativeLayout


class StatBox(RelativeLayout):
    color = ListProperty([0, 0, 0, 1])
    number_color = ListProperty([0, 0, 0, 1])
    font = StringProperty('')

    health = NumericProperty(0.0)
    mana = NumericProperty(0.0)
    phy_attack = NumericProperty(0.0)
    mag_attack = NumericProperty(0.0)
    defense = NumericProperty(0.0)

    stat_bar_source = StringProperty('')
    health_source = StringProperty('')
    mana_source = StringProperty('')
    phy_attack_source = StringProperty('')
    mag_attack_source = StringProperty('')
    defense_source = StringProperty('')

    def __init__(self, **kwargs):
        self.stat_bar_source = "../res/screens/attribute/stat_bar.png"
        self.health_source = "../res/screens/stats/Health.png"
        self.mana_source = "../res/screens/stats/Mana.png"
        self.phy_attack_source = "../res/screens/stats/PhysicalAttack.png"
        self.mag_attack_source = "../res/screens/stats/MagicalAttack.png"
        self.defense_source = "../res/screens/stats/Defense.png"
        super().__init__(**kwargs)
