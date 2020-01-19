from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout

from src.modules.Screens.FilledCharacterPreview import FilledCharacterPreview


class SinglePreview(Widget):
    initialized = BooleanProperty(False)
    main_screen = ObjectProperty(None)

    preview = ObjectProperty(None)
    character = ObjectProperty(None)
    is_support = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._size = (0, 0)

        self.root = FilledCharacterPreview(main_screen=self.main_screen, preview=self.preview, is_select=True, character=self.character, is_support=self.is_support, new_image_instance=True)

        self.add_widget(self.root)
        self.initialized = True

    def on_size(self, instance, size):
        if not self.initialized or self._size == size:
            return
        self._size = size.copy()

        gap = self.height * 0.025
        slot_size = (self.height - gap * 2) * 250 / 935, self.height - gap * 2
        self.root.size = slot_size
        self.root.pos = self.x + (self.width - self.root.width) / 2, self.y + (self.height - self.root.height) / 2

    def reload(self):
        self.root.reload()
