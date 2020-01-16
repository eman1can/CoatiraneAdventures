import math
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

from src.modules.Sortable import Sortable
from src.modules.Filterable import Filterable
from src.modules.ScrollPanel import ScrollPanel


class GridPreview(Filterable, Sortable, Widget):
    def __init__(self, main_screen, preview, size, pos, slot_size, characters, isSupport):
        super().__init__(size=size, pos=pos)

        self.slot_size = slot_size
        self.main_screen = main_screen
        self.non_label_added = False

        preview_width = size[0] - slot_size[0]
        count = math.floor(preview_width / (slot_size[0] * 1.25))
        gap = (preview_width - slot_size[0] * count) / (count + 1)

        root = ScrollPanel(size_hint=(1, None), size=(preview_width, size[1]), pos=(pos[0] + slot_size[0]/2, pos[1]), do_scroll_x=False)
        self.non_label = Label(size=self.size, text="No results", font_name='../res/fnt/Gabriola.ttf', font_size=preview_width * 0.125, color=(0,0,0,1))
        self.layout = GridLayout(cols=count, padding=gap, spacing=gap, width=preview_width, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        index = 0
        previews = []
        values = []
        for character in characters:
            if character != preview.char and not isSupport or isSupport and character != preview.support:
                widget = character.get_select_square_widget()
                widget.main_screen = main_screen
                widget.preview = preview
                widget.size = slot_size
                widget.pos = (-1, -1)
                widget.reload()

                previews.append(widget)
                values.append(character.get_strength())
                widget.char = character

                self.layout.add_widget(widget)
                index += 1

        self.no_sort = True
        self.no_filter = True
        self.previews_filter = previews
        self.previews_sort = previews
        self.values_sort = values
        self.no_sort = False
        self.no_filter = False
        self.filter()

        root.add_widget(self.layout)
        self.add_widget(root)

    def on_after_sort(self):
        if self.non_label_added:
            self.non_label_added = False
            self.remove_widget(self.non_label)
        self.layout.clear_widgets()
        for preview in self.previews_sort:
            self.layout.add_widget(preview)
        if len(self.previews_sort) == 0:
            self.add_widget(self.non_label)

    def on_after_filter(self):
        self.previews_sort = self.output
        self.force_update_values()
