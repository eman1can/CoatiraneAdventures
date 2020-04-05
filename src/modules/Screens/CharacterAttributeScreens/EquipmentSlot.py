from kivy.properties import StringProperty, ObjectProperty, ListProperty, NumericProperty
from src.modules.KivyBase.Hoverable import RelativeLayoutH as RelativeLayout


class EquipmentSlot(RelativeLayout):
    item = ObjectProperty(None, allownone=True)
    color = ListProperty([0, 0, 0, 0])
    font = StringProperty('')
    slot_name = StringProperty('')

    background_source = StringProperty('')

    def __init__(self, **kwargs):
        self.background_source = "../res/screens/attribute/equipment.png"
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
