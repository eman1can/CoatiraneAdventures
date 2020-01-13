from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout

from src.modules.ScrollPanel import ScrollPanel
from src.modules.Screens.FilledCharacterPreview import FilledCharacterPreview

class ScrollPreview(Widget):
    def __init__(self, main_screen, preview, size, pos, slot_size, characters, isSupport):
        super().__init__(size=size, pos=pos)

        self.slot_size = slot_size
        self.main_screen = main_screen

        with self.canvas:
            Color(0, 1, 0, .5)
            Rectangle(size=size, pos=pos)

        root = ScrollPanel(size_hint=(None, 1), size=(size[0] - slot_size[0], slot_size[1]), pos=(pos[0] + slot_size[0]/2, pos[1] + (size[1] - slot_size[1]) / 2))
        self.layout = GridLayout(rows=1, spacing=10, size_hint_x=None)
        with self.layout.canvas:
            Color(1, 0, 0, .5)
            Rectangle(size=self.layout.size,pos=self.layout.pos)
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

