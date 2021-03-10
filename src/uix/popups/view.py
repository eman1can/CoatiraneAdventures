# Kivy Imports
from kivy.properties import ObjectProperty
from kivy.uix.relativelayout import RelativeLayout


class View(RelativeLayout):
    manager = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        self.register_event_type('on_pre_open')
        self.register_event_type('on_pre_dismiss')
        super().__init__(**kwargs)

    def hover_subscribe(self, widget=None, layer=0, adjust=None):
        super().hover_subscribe(widget, layer+1, adjust)

    def size_override(self):
        return 0.9, 0.9

    def refresh(self, *args):
        pass

    def on_pre_open(self):
        pass

    def get_name(self):
        return ''

    def on_pre_dismiss(self):
        pass

    def get_next(self):
        return None
