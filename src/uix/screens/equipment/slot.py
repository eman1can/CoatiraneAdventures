# Kivy Imports
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, StringProperty

from kivy.uix.relativelayout import RelativeLayout
# KV Import
from loading.kv_loader import load_kv

load_kv(__name__)


class EquipmentSlot(RelativeLayout):
    item = ObjectProperty(None, allownone=True)
    color = ListProperty([0, 0, 0, 1])
    font = StringProperty('Gabriola')
    slot_name = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class DisplayEquipmentSlot(EquipmentSlot):
    background_source = StringProperty('screens/attributes/equipment.png')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class DetailEquipmentSlot(EquipmentSlot):
    background_source = StringProperty('screens/equip/background.png')
    slot_source = StringProperty('screens/equip/slot.png')
    list_source = StringProperty('screens/equip/list.png')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# TODO: Make Gradient
class DurabilityBar(RelativeLayout):
    max = NumericProperty(100.0)
    value = NumericProperty(0.0)
    opacity = NumericProperty(1)

    background_source = StringProperty('')
    foreground_source = StringProperty('')

    def __init__(self, **kwargs):
        self.background_source = 'screens/stats/progress_background.png'
        self.foreground_source = 'screens/stats/progress_foreground.png'
        super().__init__(**kwargs)
