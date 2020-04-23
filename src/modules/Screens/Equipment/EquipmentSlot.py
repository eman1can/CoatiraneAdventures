from kivy.properties import StringProperty, ObjectProperty, ListProperty, NumericProperty
from src.modules.KivyBase.Hoverable import RelativeLayoutH as RelativeLayout


class EquipmentSlot(RelativeLayout):
    item = ObjectProperty(None, allownone=True)
    color = ListProperty([0, 0, 0, 1])
    font = StringProperty('../res/fnt/Gabriola.ttf')
    slot_name = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class DisplayEquipmentSlot(EquipmentSlot):
    background_source = StringProperty("../res/screens/attribute/equipment.png")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class DetailEquipmentSlot(EquipmentSlot):
    background_source = StringProperty("../res/screens/equip/background.png")
    slot_source = StringProperty("../res/screens/equip/slot.png")
    list_source = StringProperty("../res/screens/equip/list.png")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class DurabilityBar(RelativeLayout):
    max = NumericProperty(100.0)
    value = NumericProperty(0.0)
    opacity = NumericProperty(1)

    background_source = StringProperty('')
    foreground_source = StringProperty('')

    def __init__(self, **kwargs):
        self.background_source = '../res/screens/stats/progress_background.png'
        self.foreground_source = '../res/screens/stats/progress_foreground.png'
        super().__init__(**kwargs)
