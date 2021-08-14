# Kivy Imports
from kivy.properties import BooleanProperty

from kivy.uix.relativelayout import RelativeLayout
# KV Import
from loading.kv_loader import load_kv

load_kv(__name__)


class SinglePreview(RelativeLayout):
    is_support = BooleanProperty(False)

    def __init__(self, **kwargs):
        self._preview = None
        super().__init__(**kwargs)

    def update(self, preview, char, is_support):
        self._preview = preview
        self.ids.preview.character = char
        self.is_support = is_support

    def reload(self):
        self.ids.preview.reload()
