# Kivy Imports
from kivy.properties import BooleanProperty

from kivy.uix.relativelayout import RelativeLayout
# KV Import
from loading.kv_loader import load_kv

load_kv(__name__)


class SinglePreview(RelativeLayout):
    is_support = BooleanProperty(False)

    def update(self, preview, char):
        self.ids.preview.preview = preview
        self.ids.preview.character = char

    def reload(self):
        self.root.reload()
