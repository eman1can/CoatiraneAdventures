import math
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout

from src.modules.ScrollPanel import ScrollPanel

class GridPreview(Widget):
    def __init__(self, main_screen, preview, size, pos, slot_size, characters, isSupport):
        super().__init__(size=size, pos=pos)

        self.slot_size = slot_size
        self.main_screen = main_screen

        preview_width = size[0] - slot_size[0]
        count = math.floor(preview_width / (slot_size[0] * 1.25))
        gap = (preview_width - slot_size[0] * count) / (count + 1)

        root = ScrollPanel(size_hint=(1, None), size=(preview_width, size[1]), pos=(pos[0] + slot_size[0]/2, pos[1]), do_scroll_x=False)
        self.layout = GridLayout(cols=count, padding=gap, spacing=gap, width=preview_width, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        index = 0
        for character in characters:
            if character != preview.char and not isSupport or isSupport and character != preview.support:
                widget = character.get_select_square_widget()
                widget.main_screen = main_screen
                widget.preview = preview
                widget.size = slot_size
                widget.pos = (-1, -1)
                widget.reload()
                self.layout.add_widget(widget)
                index += 1

        root.add_widget(self.layout)
        self.add_widget(root)