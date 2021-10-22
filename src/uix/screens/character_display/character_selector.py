# UIX Imports
from kivy.properties import BooleanProperty, ListProperty, NumericProperty

# Kivy Imports
from kivy.clock import Clock
# KV Import
from loading.kv_loader import load_kv
from refs import Refs
from uix.modules.screen import Screen

load_kv(__name__)


class CharacterSelector(Screen):
    has_left = BooleanProperty(False)
    toggle = BooleanProperty(False)  # When False, Is Slots

    character_num = NumericProperty(0.0)

    base_character_list = ListProperty([])

    def __init__(self, preview, is_support, **kwargs):
        self._return = preview
        self.is_support = is_support
        self._size = 0, 0
        super().__init__(**kwargs)

    def set_character_list(self, characters):
        self.base_character_list = characters
        # if 'multi' in self.ids:
            # self.ids.multi

    def reload(self, preview, is_support, **kwargs):
        self._return = preview
        self.is_support = is_support
        self.update_screen()

    def on_kv_post(self, base_widget):
        self.update_screen()
        self.ids.sort.text = self.ids.multi.sort_type

    def update_screen(self):
        if self.is_support:
            char = self._return.support
        else:
            char = self._return.character

        self.has_left = char != -1

        if self.has_left:
            self.ids.single.update(self._return, char, self.is_support)

        self.ids.multi.update(self._return, char, self.is_support)

    def on_pre_enter(self, *args):
        self.update_number()

    def on_scroll(self):
        self.ids.multi.set_scroll()

    def on_grid(self):
        self.ids.multi.set_grid()

    def on_sort(self):
        Refs.gp.display_popup(self, 'sort', self.ids.multi.ascending, self.ids.multi.sort_type, self.do_sort)

    def do_sort(self, sort_type):
        self.reset_scroll()
        if sort_type == 'Ascending':
            self.ids.multi.ascending = True
        elif sort_type == 'Descending':
            self.ids.multi.ascending = False
        else:
            if sort_type in ['Party', 'Name']:
                self.ids.multi.ascending = True
            else:
                self.ids.multi.ascending = False
            self.ids.sort.text = sort_type
            self.ids.multi.sort_type = sort_type
        return self.ids.multi.ascending

    def on_filter(self):
        Refs.gp.display_popup(self, 'filter', self.do_filter, self.modify_filter)

    def modify_filter(self, filter_type):
        self.ids.multi.no_filter = True
        if filter_type in self.ids.multi.filters_applied:
            self.ids.multi.filters_applied.remove(filter_type)
        else:
            self.ids.multi.filters_applied.append(filter_type)
        self.ids.multi.no_filter = False

    def do_filter(self):
        self.reset_scroll()
        self.ids.multi.filter()
        self.close_filter()
        self.update_number()

    def update_number(self):
        if self.ids.multi is None:
            self.character_num = 0
        else:
            self.character_num = len(self.ids.multi.output)

    def reset_scroll(self):
        self.ids.multi.scroll_x = 0
        self.ids.multi.scroll_y = 1

    # def close_sort(self):
    #     self.ids.switch_display.disabled = False
    #     self.ids.switch_display.do_hover = True
    #     self.ids.multi.change_hover(True)
    #     self.sort.dismiss()

    # def close_filter(self):
    #     self.ids.switch_display.disabled = False
    #     self.ids.switch_display.do_hover = True
    #     self.ids.multi.change_hover(True)
    #     self.filter.dismiss()
