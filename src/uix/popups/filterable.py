# KV Import
from uix.popups.view import View

from loading.kv_loader import load_kv
load_kv(__name__)


class FilterPopup(View):
    # sort_text = StringProperty("")

    def __init__(self, filter_callback, filter_edit_callback, **kwargs):
        # self.sort_text = sort_text
        self._filter_callback = filter_callback
        self._filter_edit_callback = filter_edit_callback
        super().__init__(**kwargs)

    def modify_filtering(self, filter_type):
        if isinstance(filter_type, str):
            self._filter_edit_callback(f'type_{filter_type.lower()}')
        else:
            self._filter_edit_callback(f'rank_{filter_type}')

    def do_filtering(self):
        self._filter_callback()

    def size_override(self):
        return .75, .9
