from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

from src.modules.ScrollPanel import ScrollPanel
from src.modules.Sortable import Sortable
from src.modules.Filterable import Filterable


class ScrollPreview(Filterable, Sortable, Widget):
    def __init__(self, main_screen, preview, size, pos, slot_size, characters, isSupport):
        super().__init__(size=size, pos=pos)

        self.slot_size = slot_size
        self.main_screen = main_screen
        self.non_label_added = False

        preview_width = size[0] - slot_size[0]
        gap = preview_width * 0.0125

        root = ScrollPanel(size_hint=(None, 1), size=(preview_width, slot_size[1] + gap * 2), pos=(pos[0] + slot_size[0]/2, pos[1] + (size[1] - slot_size[1]) / 2), do_scroll_y=False)
        self.non_label = Label(size=self.size, text="No results", font_name='../res/fnt/Gabriola.ttf', font_size=preview_width * 0.125, color=(0,0,0,1))
        self.layout = GridLayout(rows=1, padding=gap, spacing=gap, size_hint_x=None)
        self.layout.bind(minimum_width=self.layout.setter('width'))

        index = 0
        previews = []
        values = []
        for character in characters:
            if character != preview.char and not isSupport or isSupport and character != preview.support:
                widget = character.get_select_widget()
                widget.main_screen = main_screen
                widget.preview = preview
                widget.size = slot_size
                widget.pos = (-1, -1)
                widget.reload()

                if character in self.main_screen.parties[self.main_screen.parties[0] + 1]:
                    tag = Label(text="selected", color=(1, 1, 1, 1), font_size=slot_size[0] * 0.25, font_name='../res/fnt/Gabriola.ttf', outline_color=(0, 0, 0, 1), outline_width=1)
                    tag._label.refresh()
                    tag.size = slot_size[0], tag._label.texture.size[0]
                    tag.pos = (widget.pos[0], widget.pos[1] + widget.size[1] - (60 * widget.size[1] / 935) - tag.height)
                    widget.tag = tag
                    widget.has_tag = True
                    widget.add_widget(tag)
                elif widget.has_tag:
                    widget.has_tag = False
                    widget.remove_widget(widget.tag)

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
            self.non_label_added = True
            self.add_widget(self.non_label)


    def on_after_filter(self):
        self.previews_sort = self.output
        self.force_update_values()
