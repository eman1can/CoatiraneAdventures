# UIX Imports
from refs import Refs
from uix.modules.screen import Screen

# Kivy Imports
from kivy.animation import Animation
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout

# KV Import
from loading.kv_loader import load_kv
load_kv(__name__)


class EquipmentChange(Screen):
    char = ObjectProperty()

    weapon = ObjectProperty(None, allownone=True)
    helmet = ObjectProperty(None, allownone=True)
    chest = ObjectProperty(None, allownone=True)
    grieves = ObjectProperty(None, allownone=True)
    boots = ObjectProperty(None, allownone=True)
    vambraces = ObjectProperty(None, allownone=True)
    gloves = ObjectProperty(None, allownone=True)
    necklace = ObjectProperty(None, allownone=True)
    ring = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def goto_equipment_change(self, direction):
        next_char = Refs.gc.get_next_char(self.char, direction)
        Refs.gs.display_screen('equipment_change_' + next_char.get_id(), True, False, next_char)


class MultiEquipmentChange(GridLayout):
    char = ObjectProperty(None, allownone=True)


class CharEquipButton(RelativeLayout):
    char = ObjectProperty(None, allownone=True)

    def on_char_equip(self, *args):
        if self.char is not None:
            Refs.gs.display_screen('equipment_change_' + self.char.get_id(), True, True, self.char)


class MissingEquip(RelativeLayout):
    pass


class GearChange(Screen):
    animate_distance = NumericProperty(0.0)
    animation_start_down = NumericProperty(0.0)
    animation_start_up = NumericProperty(0.0)
    animation_down = ObjectProperty(None, allownone=True)
    animation_up = ObjectProperty(None, allownone=True)

    def on_enter(self, *args):
        self.animate_arrows()

    def on_leave(self, *args):
        self.unanimate_arrows()

    def animate_arrows(self):
        self.ensure_creation()
        self.animation_down.start(self.ids.arrow_down)
        self.animation_up.start(self.ids.arrow_up)

    def ensure_creation(self):
        if self.animation_down is None or self.animation_up is None:
            self.animation_down = Animation(y=self.animation_start_down - self.animate_distance, duration=1) + Animation(y=self.animation_start_down, duration=0.25)
            self.animation_up = Animation(y=self.animation_start_up + self.animate_distance, duration=1) + Animation(y=self.animation_start_up, duration=0.25)
        self.animation_down.repeat = True
        self.animation_up.repeat = True

    def unanimate_arrows(self):
        if self.animation_down is not None:
            self.animation_down.repeat = False
        if self.animation_up is not None:
            self.animation_up.repeat = False
