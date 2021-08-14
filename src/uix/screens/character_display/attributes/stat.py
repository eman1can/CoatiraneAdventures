# Kivy Imports
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, StringProperty

from kivy.uix.relativelayout import RelativeLayout
# KV Import
from loading.kv_loader import load_kv

load_kv(__name__)


class StatBox(RelativeLayout):
    color = ListProperty([0, 0, 0, 1])
    number_color = ListProperty([0, 0, 0, 1])
    font = StringProperty('')

    char = ObjectProperty(None)

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
        self.stat_bar_source = 'stat_bar.png'
        self.health_source = 'icons/Hea.png'
        self.mana_source = 'icons/Mna.png'
        self.phy_attack_source = 'icons/PAtk.png'
        self.mag_attack_source = 'icons/MAtk.png'
        self.defense_source = 'icons/Def.png'
        super().__init__(**kwargs)

    def on_char(self, *args):
        self.reload()

    def reload(self):
        if self.char is None:
            return
        self.health = self.char.get_health()
        self.mana = self.char.get_mana()
        self.phy_attack = self.char.get_physical_attack()
        self.mag_attack = self.char.get_magical_attack()
        self.defense = self.char.get_defense()
