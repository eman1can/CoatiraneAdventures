# Relative Layouts
from kivy.properties import BooleanProperty, ListProperty, NumericProperty, ObjectProperty, StringProperty

from kivy.uix.relativelayout import RelativeLayout
# KV Import
from loading.kv_loader import load_kv

load_kv(__name__)


class AbilityStatBox(RelativeLayout):

    color = ListProperty([0, 0, 0, 1])
    font = StringProperty('')

    char = ObjectProperty(None)
    rank = BooleanProperty(False)

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
        self.background_source = 'screens/attributes/ability_overlay.png'
        super().__init__(**kwargs)

    def on_char(self, *args):
        self.reload()

    def on_rank(self, *args):
        self.reload()

    def reload(self):
        if self.char is None:
            return
        if not self.rank:
            self.strength = self.char.get_strength()
            self.strength_path = self.char.get_strength_rank_image()
            self.magic = self.char.get_magic()
            self.magic_path = self.char.get_magic_rank_image()
            self.endurance = self.char.get_endurance()
            self.endurance_path = self.char.get_endurance_rank_image()
            self.dexterity = self.char.get_dexterity()
            self.dexterity_path = self.char.get_dexterity_rank_image()
            self.agility = self.char.get_agility()
            self.agility_path = self.char.get_agility_rank_image()
        else:
            self.strength = self.char.get_strength(self.char.get_current_rank())
            self.strength_path = self.char.get_strength_rank_image(self.char.get_current_rank())
            self.magic = self.char.get_magic(self.char.get_current_rank())
            self.magic_path = self.char.get_magic_rank_image(self.char.get_current_rank())
            self.endurance = self.char.get_endurance(self.char.get_current_rank())
            self.endurance_path = self.char.get_endurance_rank_image(self.char.get_current_rank())
            self.dexterity = self.char.get_dexterity(self.char.get_current_rank())
            self.dexterity_path = self.char.get_dexterity_rank_image(self.char.get_current_rank())
            self.agility = self.char.get_agility(self.char.get_current_rank())
            self.agility_path = self.char.get_agility_rank_image(self.char.get_current_rank())
