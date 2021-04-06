import importlib
from math import floor
from random import choices, randint

from game.floor import EXIT
from game.housing import Housing
from game.save_load import create_new_save
from kivy.base import EventLoop
from kivy.clock import Clock
from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivy.uix.textinput import CutBuffer, TextInput
from refs import Refs
from text.screens.screen_names import BACK, GAME_LOADING, HOUSING_BUY, HOUSING_RENT, INTRO_DOMAIN_NAME, NEW_GAME, PERK_BESTOW

Builder.load_string("""
<Console>:
    id: console
    background_normal: ''
    background_active: ''
    background_color: 0, 0, 0, 1
    foreground_color: 1, 1, 1, 1
    font_name: 'Fantasque'
    global_font_size: str(int(self.width * 15 / 1706)) + 'pt'
    font_size: self.global_font_size
    markup: True
""")

CURSOR = '\n\t>> '


class Console(TextInput):
    header_text = StringProperty('')
    display_text = StringProperty('')
    error_text = StringProperty('')
    current_text = StringProperty('')

    global_font_size = StringProperty('15pt')

    def __init__(self, **kwargs):
        self._options = {}
        self._back_list = {}
        self.error_time = 0.5

        self._current_screen = None
        self._current_screen_data = None
        self._current_module = None
        self.header_callback = None
        self._width = None

        self.loading_progress = {}

        self.party_box = None
        self.select_box = None

        self.new_game_info = {}
        self.domains = None

        super().__init__(**kwargs)

        self.set_screen(NEW_GAME)

    def on_global_font_size(self, *args):
        self._refresh()

    def get_global_font_size(self):
        return int(self.global_font_size[:-2])

    def get_current_screen(self):
        return self._current_screen

    def get_current_data(self):
        return self._current_screen_data

    def get_last_screen(self):
        return self._back_list[-1]

    def on_display_text(self, *args):
        self.text = f'{self.header_text}{self.display_text}{CURSOR}{self.current_text}'

    def on_current_text(self, *args):
        self.text = f'{self.header_text}{self.display_text}{CURSOR}{self.current_text}'

    def on_error_text(self, *args):
        if self.error_text == '':
            self.text = f'{self.header_text}{self.display_text}{CURSOR}{self.current_text}'
        else:
            self.text = f'{self.header_text}{self.display_text}\n\t{self.error_text}\n{CURSOR}{self.current_text}'
            Clock.schedule_once(self.clear_error_text, self.error_time)

    def clear_error_text(self, *args):
        self.error_time = 0.5
        self.error_text = ''

    def on_touch_down(self, touch):
        if self.disabled:
            return

        touch_pos = touch.pos
        if not self.collide_point(*touch_pos):
            return False
        if super(TextInput, self).on_touch_down(touch):
            return True

        if self.focus:
            self._trigger_cursor_reset()

        # Check for scroll wheel
        if 'button' in touch.profile and touch.button.startswith('scroll'):
            # TODO: implement 'scrollleft' and 'scrollright'
            scroll_type = touch.button[6:]
            if scroll_type == 'down':
                if self.multiline:
                    if self.scroll_y > 0:
                        self.scroll_y -= self.line_height
                        self._trigger_update_graphics()
                else:
                    if self.scroll_x > 0:
                        self.scroll_x -= self.line_height
                        self._trigger_update_graphics()
            if scroll_type == 'up':
                if self.multiline:
                    viewport_height = self.height \
                                      - self.padding[1] - self.padding[3]
                    text_height = len(self._lines) * (self.line_height
                                                      + self.line_spacing)
                    if viewport_height < text_height - self.scroll_y:
                        self.scroll_y += self.line_height
                        self._trigger_update_graphics()
                else:
                    if (self.scroll_x + self.width <
                            self._lines_rects[-1].texture.size[0]):
                        self.scroll_x += self.line_height
                        self._trigger_update_graphics()
            return True

        touch.grab(self)
        self._touch_count += 1
        if touch.is_double_tap:
            self.dispatch('on_double_tap')
        if touch.is_triple_tap:
            self.dispatch('on_triple_tap')
        if self._touch_count == 4:
            self.dispatch('on_quad_touch')

        self._hide_cut_copy_paste(EventLoop.window)
        # schedule long touch for paste
        self._long_touch_pos = touch.pos
        self._long_touch_ev = Clock.schedule_once(self.long_touch, .5)

        # self.cursor = self.get_cursor_from_xy(*touch_pos)
        if not self._selection_touch:
            self.cancel_selection()
            self._selection_touch = touch
            self._selection_from = self._selection_to = self.cursor_index()
            self._update_selection()

        if CutBuffer and 'button' in touch.profile and \
                touch.button == 'middle':
            self.insert_text(CutBuffer.get_cutbuffer())
            return True

        return True

    def on_touch_move(self, touch):
        if touch.grab_current is not self:
            return
        if not self.focus:
            touch.ungrab(self)
            if self._selection_touch is touch:
                self._selection_touch = None
            return False
        if self._selection_touch is touch:
            # self.cursor = self.get_cursor_from_xy(touch.x, touch.y)
            self._selection_to = self.cursor_index()
            self._update_selection()
            return True

    def on_text_validate(self):
        if self._current_screen == GAME_LOADING:
            return
        option = self.current_text.strip()
        self.current_text = ''
        if option in self.get_options():
            action = self.get_options()[option]
            if action == BACK:
                self.set_screen(BACK)
            else:
                getattr(self._current_module, 'handle_action')(self, action)
        elif self._current_screen == INTRO_DOMAIN_NAME:
            getattr(self._current_module, 'handle_action')(self, option)
        else:
            self.error_text = 'Invalid Option!'

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if keycode[1] == 'backspace' and self.current_text == "":  # backspace
            return
        else:
            super().keyboard_on_key_down(window, keycode, text, modifiers)
        if keycode[1] == 'enter' or keycode[1] == 'numpadenter':  # Enter
            self.dispatch('on_text_validate')
        if keycode[1] == 'left':  # Left
            if self.cursor_row >= 5 and self.cursor_col > 4:
                super().keyboard_on_key_down(window, keycode, text, modifiers)
        elif keycode[1] == 'right':  # Right
            if self.cursor_row >= 5 and self.cursor_col >= 4:
                super().keyboard_on_key_down(window, keycode, text, modifiers)

    def keyboard_on_key_up(self, window, keycode):
        pass

    def insert_text(self, substring, from_undo=False):
        valid = True
        if self._current_screen != INTRO_DOMAIN_NAME:
            for char in substring:
                valid &= char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        if valid:
            self.current_text += substring

    def do_backspace(self, from_undo=False, mode='bkspc'):
        self.current_text = self.current_text[:-1]

    def save_screen(self, class_name):
        if self._current_screen in self._back_list:
            for key in reversed(list(self._back_list.keys())):
                if key == self._current_screen:
                    break
                self._back_list.pop(key)
            return False
        if class_name in self._back_list:
            for key in reversed(list(self._back_list.keys())):
                if key == class_name:
                    self._back_list.pop(key)
                    break
                self._back_list.pop(key)
            return False
        if self._current_screen == class_name:
            return False
        self._back_list[self._current_screen] = self._current_screen_data
        return True

    def break_down_name(self, screen_name):
        if ':' in screen_name:
            return screen_name.split(':')
        return screen_name, None

    # Screen manager options
    def set_screen(self, screen_name):
        class_name, screen_data = self.break_down_name(screen_name)
        if class_name == BACK:
            class_name = list(self._back_list.keys())[-1]
            screen_data = self._back_list.pop(class_name)
        else:
            if self.save_screen(class_name):
                print('Set to', screen_name)
                print('\t', self._back_list)
                print()

        self._current_screen = class_name
        self._current_screen_data = screen_data

        self._current_module = importlib.import_module('text.screens.' + class_name)
        self.display_text, self._options = getattr(self._current_module, 'get_screen')(self, screen_data)

        self._refresh_header()

    def set_loading_progress(self, label, value, max):
        self.loading_progress[label] = (value, max)
        self.set_screen(GAME_LOADING)

    def update_calendar_callback(self):
        Refs.gc.set_calendar_callback(self._refresh_header)

    def _refresh_text(self, text, *largs):
        super()._refresh_text(text, *largs)
        if self._label_cached:
            width = floor(self.width / self._label_cached.get_extents(' ')[0]) - 1
            if self._width != width:
                self._width = width
                self._refresh()

    def get_width(self):
        return self._width

    def _refresh(self):
        if self._current_screen is None:
            return
        if self._current_screen_data:
            self.set_screen(self._current_screen + ':' + self._current_screen_data)
        else:
            self.set_screen(self._current_screen)

    def _refresh_header(self):
        if self._current_screen is None:
            return
        if self.header_callback:
            self.header_text = self.header_callback(self)
        else:
            self.header_text = ''
        if self.error_text == '':
            self.text = f'{self.header_text}{self.display_text}{CURSOR}{self.current_text}'
        else:
            self.text = f'{self.header_text}{self.display_text}\n\t{self.error_text}\n{CURSOR}{self.current_text}'

    def get_options(self):
        return self._options
