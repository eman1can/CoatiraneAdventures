from kivy.properties import BooleanProperty, StringProperty

# KV Import
from loading.kv_loader import load_kv
from uix.popups.view import View

load_kv(__name__)


class SortPopup(View):
    ascending = BooleanProperty(False)
    sort_text = StringProperty("")

    def __init__(self, ascending, sort_text, sort_callback, **kwargs):
        self.ascending = ascending
        self.sort_text = sort_text
        self._sort_callback = sort_callback
        super().__init__(**kwargs)

    def do_sorting(self, sort_type):
        ascending = self._sort_callback(sort_type)
        if ascending != self.ascending:
            self.ascending = ascending

    def size_override(self):
        return .633, .9
