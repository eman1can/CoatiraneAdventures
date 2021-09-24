from kivy.properties import StringProperty

from kivy.uix.relativelayout import RelativeLayout
from loading.kv_loader import load_kv

load_kv(__name__)


class CharFlag(RelativeLayout):
    type = StringProperty('adventurer')

    def on_type(self, instance, type):
        self.ids.flag_label.text = self.type.title()


class TypeFlag(RelativeLayout):
    type = StringProperty('physical')

    def on_type(self, instance, type):
        self.ids.flag_label.text = self.type.title()


class ElementFlag(RelativeLayout):
    type = StringProperty('wind')

    def on_type(self, instance, type):
        self.ids.flag_label.text = self.type.title()