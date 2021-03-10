# UIX Imports
from uix.popups.view import View

# Kivy Imports
from kivy.properties import BooleanProperty, NumericProperty, StringProperty

# KV Import
from loading.kv_loader import load_kv
load_kv(__name__)


class Confirm(View):
    descending = BooleanProperty(False)
    current_floor = StringProperty('')
    next_floor = StringProperty('')
    recc_score = NumericProperty(0)
    act_score = NumericProperty(0)

    def __init__(self, descending, current_floor, next_floor, act_score, **kwargs):
        self.register_event_type('on_confirm')
        confirm_callback = None
        if 'on_confirm' in kwargs:
            confirm_callback = kwargs.pop('on_confirm')
        super().__init__(**kwargs)
        if confirm_callback is not None:
            self.bind(on_confirm=confirm_callback)

        self.current_floor = current_floor
        self.next_floor = next_floor
        self.descending = descending

    def confirm(self):
        self.manager.goto_previous()
        self.dispatch('on_confirm')

    def on_confirm(self):
        pass
