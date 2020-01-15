from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout

from src.modules.ScrollPanel import ScrollPanel

class ScrollPreview(Widget):
    def __init__(self, main_screen, preview, size, pos, slot_size, characters, isSupport):
        super().__init__(size=size, pos=pos)

        self.slot_size = slot_size
        self.main_screen = main_screen

        preview_width = size[0] - slot_size[0]
        gap = preview_width * 0.0125

        root = ScrollPanel(size_hint=(None, 1), size=(preview_width, slot_size[1] + gap * 2), pos=(pos[0] + slot_size[0]/2, pos[1] + (size[1] - slot_size[1]) / 2), do_scroll_y=False)
        self.layout = GridLayout(rows=1, padding=gap, spacing=gap, size_hint_x=None)
        self.layout.bind(minimum_width=self.layout.setter('width'))

        index = 0
        for character in characters:
            if character != preview.char and not isSupport or isSupport and character != preview.support:
                widget = character.get_select_widget()
                widget.main_screen = main_screen
                widget.preview = preview
                widget.size = slot_size
                widget.pos = (-1, -1)
                widget.reload()
                self.layout.add_widget(widget)
                index += 1

        root.add_widget(self.layout)
        self.add_widget(root)

