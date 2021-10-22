# UIX Imports
# Kivy Imports
from kivy.properties import NumericProperty, ObjectProperty, StringProperty

# KV Import
from loading.kv_loader import load_kv
from refs import Refs
from uix.modules.screen import Screen

load_kv(__name__)


class ImagePreview(Screen):
    char = NumericProperty(-1)
    char_image_source = StringProperty('')

    def __init__(self, character, **kwargs):
        self.char = character
        self.name = 'image_preview_unassigned'

        if character == -1:
            super().__init__(**kwargs)
            return

        char = Refs.gc.get_char_by_index(character)
        self.name = 'image_preview_' + str(char.get_id())
        self.char_image_source = char.get_image('inspect')
        super().__init__(**kwargs)
