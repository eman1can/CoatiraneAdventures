from kivy.properties import ObjectProperty, BooleanProperty, ListProperty
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

from src.modules.ScrollPanel import ScrollPanel
from src.modules.Sortable import Sortable
from src.modules.Filterable import Filterable


class ScrollPreview(Filterable, Sortable, Widget):
    initialized = BooleanProperty(False)
    main_screen = ObjectProperty(None)
    preview = ObjectProperty(None)

    characters = ListProperty([])
    is_support = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._size = (0, 0)
        self._pos = (-1, -1)
        self.non_label_added = False

        self.root = ScrollPanel(size_hint=(None, 1), do_scroll_y=False)
        self.non_label = Label(text="No results", font_name='../res/fnt/Gabriola.ttf', color=(0,0,0,1))
        self.layout = GridLayout(rows=1, size_hint_x=None)
        self.layout.bind(minimum_width=self.layout.setter('width'))

        index = 0
        previews = []
        values = []
        for character in self.characters:
            if character != self.preview.char and not self.is_support or self.is_support and character != self.preview.support:
                widget = character.get_select_widget()
                widget.main_screen = self.main_screen
                widget.preview = self.preview
                widget.reload()

                if character in self.main_screen.parties[self.main_screen.parties[0] + 1]:
                    if not widget.has_tag:
                        tag = Label(text="selected", color=(1, 1, 1, 1), font_name='../res/fnt/Gabriola.ttf', outline_color=(0, 0, 0, 1), outline_width=1)
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

        self.root.add_widget(self.layout)
        self.add_widget(self.root)
        self.initialized = True

    def on_size(self, instance, size):
        if not self.initialized or self._size == size:
            return
        self._size = size.copy()

        gap = self.height * 0.05
        slot_size = (self.height - gap * 2) * 250 / 935, self.height - gap * 2

        self.non_label.font_size = (self.width - gap * 2) * 0.125
        self.non_label.size = self.size

        self.root.size = self.width - gap * 2, slot_size[1]
        self.root.pos = self.x + gap, self.y + gap

        for preview in self.previews_filter:
            preview.size = slot_size
            preview.char_button._static_hover = True
            preview.char_button.hover_rect = [self.root.x, self.root.y, self.root.width, self.root.height]

        self.layout.height = slot_size[1]
        self.layout.padding = [0, 0, 0, 0]
        self.layout.spacing = gap, 0

    def on_pos(self, instance, pos):
        if not self.initialized or self._pos == pos:
            return
        self._pos = pos.copy()

        gap = self.height * 0.05
        self.root.pos = self.x + gap, self.y + gap
        self.non_label.pos = pos

        for preview in self.previews_filter:
            preview.char_button._static_hover = True
            preview.char_button.hover_rect = [self.root.x, self.root.y, self.root.width, self.root.height]

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
        if self.parent is not None:
            self.parent.update_number(len(self.output))
        self.previews_sort = self.output
        print(self.previews_filter)
        print(self.filters_applied)
        print(self.previews_sort)
        self.force_update_values()
