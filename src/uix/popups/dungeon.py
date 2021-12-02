# UIX Imports
# Kivy Imports
from kivy.properties import BooleanProperty, Clock, NumericProperty, StringProperty

# KV Import
from loading.kv_loader import load_kv
from refs import Refs
from uix.popups.view import View

load_kv(__name__)


class DungeonConfirm(View):
    current_floor = NumericProperty(0)
    next_floor = NumericProperty(0)
    rec_score = NumericProperty(-1)
    act_score = NumericProperty(-1)
    floor_text = StringProperty('')

    def __init__(self, **kwargs):
        self.register_event_type('on_confirm')
        confirm_callback = None
        if 'on_confirm' in kwargs:
            confirm_callback = kwargs.pop('on_confirm')
        super().__init__(**kwargs)
        if confirm_callback is not None:
            self.bind(on_confirm=confirm_callback)

    def on_kv_post(self, base_widget):
        if self.current_floor is None or self.next_floor is None:
            self.ids.floor_info.opacity = 0
        if self.rec_score == -1:
            self.ids.rec_score_info.opacity = 0
        if self.act_score == -1:
            self.ids.act_score_info.opacity = 0

        prefix = self.floor_to_string(self.current_floor)
        suffix = self.floor_to_string(self.next_floor)
        self.floor_text = f'{prefix} -> {suffix}'

    def floor_to_string(self, floor):
        if floor == 0:
            return 'Surface'
        return f'Floor {floor}'

    def confirm(self):
        self.manager.goto_previous()
        self.dispatch('on_confirm')
        return False

    def dismiss(self):
        self.manager.dismiss()

    def on_confirm(self):
        pass
