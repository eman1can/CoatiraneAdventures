from kivy.properties import StringProperty

# KV Import
from loading.kv_loader import load_kv
from uix.popups.view import View

load_kv(__name__)


class SortPopup(View):
    sort_text = StringProperty("")

    def __init__(self, sort_text, sort_callback, **kwargs):
        self.sort_text = sort_text
        self._sort_callback = sort_callback
        super().__init__(**kwargs)

    def do_sorting(self, sort_type):
        self._sort_callback(sort_type)

    def size_override(self):
        return .633, .9
