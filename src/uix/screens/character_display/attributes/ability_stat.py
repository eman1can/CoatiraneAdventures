# Relative Layouts
from kivy.properties import BooleanProperty, ListProperty, NumericProperty, ObjectProperty, StringProperty

from kivy.uix.relativelayout import RelativeLayout
# KV Import
from loading.kv_loader import load_kv
from refs import Refs

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
        self.background_source = 'ability_overlay.png'
        super().__init__(**kwargs)

    def on_char(self, *args):
        self.reload()

    def on_rank(self, *args):
        self.reload()

    def reload(self):
        if self.char == -1:
            return
        char = Refs.gc.get_char_by_index(self.char)
        if not self.rank:
            self.strength = char.get_strength()
            self.strength_path = char.get_strength_rank_image()
            self.magic = char.get_magic()
            self.magic_path = char.get_magic_rank_image()
            self.endurance = char.get_endurance()
            self.endurance_path = char.get_endurance_rank_image()
            self.dexterity = char.get_dexterity()
            self.dexterity_path = char.get_dexterity_rank_image()
            self.agility = char.get_agility()
            self.agility_path = char.get_agility_rank_image()
        else:
            self.strength = char.get_strength(char.get_current_rank())
            self.strength_path = char.get_strength_rank_image(char.get_current_rank())
            self.magic = char.get_magic(char.get_current_rank())
            self.magic_path = char.get_magic_rank_image(char.get_current_rank())
            self.endurance = char.get_endurance(char.get_current_rank())
            self.endurance_path = char.get_endurance_rank_image(char.get_current_rank())
            self.dexterity = char.get_dexterity(char.get_current_rank())
            self.dexterity_path = char.get_dexterity_rank_image(char.get_current_rank())
            self.agility = char.get_agility(char.get_current_rank())
            self.agility_path = char.get_agility_rank_image(char.get_current_rank())
