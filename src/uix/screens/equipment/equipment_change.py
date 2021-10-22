# UIX Imports
from kivy.properties import NumericProperty, ObjectProperty, StringProperty

# Kivy Imports
from game.equipment import BOOTS, CHEST, GLOVES, GRIEVES, HELMET, NECKLACE, RING, VAMBRACES, WEAPON
from kivy.animation import Animation
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
# KV Import
from loading.kv_loader import load_kv
from refs import Refs
from uix.modules.screen import Screen

load_kv(__name__)


class EquipmentChange(Screen):
    char = NumericProperty(-1)

    portrait_source = StringProperty('')

    def __init__(self, char, **kwargs):
        self.char = char
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        if self.char == -1:
            self.name = 'equipment_change_unassigned'
        else:
            char = Refs.gc.get_char_by_index(self.char)
            self.name = f'equipment_change_{char.get_id()}'
            self.portrait_source = char.get_image('portrait')
            outfit = char.get_equipment()
            self.ids.weapon.item = outfit.get_equipment(WEAPON)
            self.ids.helmet.item = outfit.get_equipment(HELMET)
            self.ids.chest.item = outfit.get_equipment(CHEST)
            self.ids.grieves.item = outfit.get_equipment(GRIEVES)
            self.ids.boots.item = outfit.get_equipment(BOOTS)
            self.ids.vambraces.item = outfit.get_equipment(VAMBRACES)
            self.ids.gloves.item = outfit.get_equipment(GLOVES)
            self.ids.necklace.item = outfit.get_equipment(NECKLACE)
            self.ids.ring.item = outfit.get_equipment(RING)

    def goto_equipment_change(self, direction):
        next_char = Refs.gc.get_next_char(self.char, direction)
        char = Refs.gc.get_char_by_index(next_char)
        Refs.gs.display_screen('equipment_change_' + char.get_id(), True, False, char)


class MultiEquipmentChange(GridLayout):
    char = NumericProperty(-1)

    weapon = ObjectProperty(None, allownone=True)
    helmet = ObjectProperty(None, allownone=True)
    chest = ObjectProperty(None, allownone=True)
    grieves = ObjectProperty(None, allownone=True)
    boots = ObjectProperty(None, allownone=True)
    vambraces = ObjectProperty(None, allownone=True)
    gloves = ObjectProperty(None, allownone=True)
    necklace = ObjectProperty(None, allownone=True)
    ring = ObjectProperty(None, allownone=True)

    def on_char(self, instance, value):
        if self.char == -1:
            self.weapon = self.helmet = self.chest = self.grieves = self.boots = self.vambraces = self.gloves = self.necklace = self.ring = None
        else:
            char = Refs.gc.get_char_by_index(self.char)
            outfit = char.get_equipment()
            self.weapon = outfit.get_equipment(WEAPON)
            self.helmet = outfit.get_equipment(HELMET)
            self.chest = outfit.get_equipment(CHEST)
            self.grieves = outfit.get_equipment(GRIEVES)
            self.boots = outfit.get_equipment(BOOTS)
            self.vambraces = outfit.get_equipment(VAMBRACES)
            self.gloves = outfit.get_equipment(GLOVES)
            self.necklace = outfit.get_equipment(NECKLACE)
            self.ring = outfit.get_equipment(RING)

class CharEquipButton(RelativeLayout):
    char = NumericProperty(-1)
    image_source = StringProperty('')

    def on_char(self, instance, value):
        if self.char != -1:
            char = Refs.gc.get_char_by_index(self.char)
            self.image_source = char.get_image('preview')

    def on_char_equip(self, *args):
        if self.char != -1:
            char = Refs.gc.get_char_by_index(self.char)
            Refs.gs.display_screen('equipment_change_' + char.get_id(), True, True, self.char)


class MissingEquip(RelativeLayout):
    pass


class GearChange(Screen):
    animate_distance = NumericProperty(0.0)
    animation_start_down = NumericProperty(0.0)
    animation_start_up = NumericProperty(0.0)
    animation_down = ObjectProperty(None, allownone=True)
    animation_up = ObjectProperty(None, allownone=True)

    def on_kv_post(self, base_widget):
        self.reload()

    def reload(self, *args):
        self.ids.char_overview.clear_widgets()
        self.ids.char_multi.clear_widgets()
        self.ids.char_missing.clear_widgets()
        self.ids.support_overview.clear_widgets()
        self.ids.support_multi.clear_widgets()
        self.ids.support_missing.clear_widgets()
        for index, character in enumerate(Refs.gc.get_current_party()):
            if index < 8:
                self.ids.char_overview.add_widget(CharEquipButton(char=character))
                self.ids.char_multi.add_widget(MultiEquipmentChange(char=character))
                if character != -1:
                    self.ids.char_missing.add_widget(MissingEquip())
                else:
                    self.ids.char_missing.add_widget(MissingEquip(opacity=0))
            else:
                self.ids.support_overview.add_widget(CharEquipButton(char=character))
                self.ids.support_multi.add_widget(MultiEquipmentChange(char=character))
                if character != -1:
                    self.ids.char_missing.add_widget(MissingEquip())
                else:
                    self.ids.support_missing.add_widget(MissingEquip(opacity=0))

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
