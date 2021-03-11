from game.save_load import create_new_save
from kivy.base import EventLoop
from kivy.clock import Clock
from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivy.uix.textinput import CutBuffer, TextInput
from refs import Refs
from text.memory import Memory
from text.screens.dungeon_main import dungeon_main, dungeon_main_confirm
from text.screens.new_game import game_loading, intro_domain, intro_domain_gender, intro_domain_name, intro_select, new_game, save_select
from text.screens.select_char import select_screen_char
from text.screens.shop import do_transaction, shop
from text.screens.town import crafting_main, inventory_main, quests_main, tavern_main, town_main
from text.screens.dungeon_battle import dungeon_battle, dungeon_battle_action, dungeon_result

TEST_TEXT = 'Level 1 Goblin entered the battle!\nLevel 1 Goblin entered the battle!\nLevel 1 Goblin entered the battle!\nLevel 1 Goblin entered the battle!\nAis Wallenstein joined the battle!\nLexi Buhr joined the battle!\nSofi joined' \
            ' the battle!\nSophie Nicholson joined the battle!\nSophie Nicholson used support skill Invigoration!\nMaya Lurch joined the battle!\nMaya Lurch used support skill Invigoration!\nSophie Nicholson joined the battle!\nSophie Nicholson ' \
            'used support skill Invigoration!'

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
OPT_C = '[color=#CA353E]'
END_OPT_C = '[/color]'


class Console(TextInput):
    display_text = StringProperty("")
    error_text = StringProperty("")
    current_text = StringProperty("")

    global_font_size = StringProperty('15pt')

    def __init__(self, **kwargs):
        self._options = {}
        self._back_list = []
        self._current_screen = None
        # Clock.schedule_once(lambda dt: self.grab_focus, 0.5)
        self.memory = Memory()
        self.memory.game_info = {}
        self.memory.loading_progress = {}
        self.memory.party_box = None
        self.memory.select_box = None

        self.memory.domains = None
        self.memory.current_domain = 0

        super().__init__(**kwargs)

        self.set_screen('new_game')

    def on_global_font_size(self, *args):
        self.set_screen('new_game')
    #     print('Global Font Size: ', self.global_font_size)

    def get_global_font_size(self):
        return int(self.global_font_size[:-2])

    # def grab_focus(self):
    #     self.focus = True
        # self.ids.console_log.text = TEST_TEXT

    def get_current_screen(self):
        return self._current_screen

    def on_display_text(self, *args):
        self.text = f'{self.display_text}{CURSOR}{self.current_text}'

    def on_current_text(self, *args):
        self.text = f'{self.display_text}{CURSOR}{self.current_text}'

    def on_error_text(self, *args):
        if self.error_text == "":
            self.text = f'{self.display_text}{CURSOR}{self.current_text}'
        else:
            self.text = f'{self.display_text}\n{self.error_text}\n{CURSOR}{self.current_text}'
            Clock.schedule_once(self.clear_error_text, 0.5)

    def clear_error_text(self, *args):
        self.error_text = ""

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

        self.cursor = self.get_cursor_from_xy(*touch_pos)
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
            self.cursor = self.get_cursor_from_xy(touch.x, touch.y)
            self._selection_to = self.cursor_index()
            self._update_selection()
            return True

    def on_text_validate(self):
        if self._current_screen == 'game_loading':
            return
        if self.current_text.strip() in self.get_options():
            self.execute_action(self.get_options()[self.current_text.strip()])
            self.current_text = ""
        else:
            if self._current_screen == 'intro_domain_name':
                self.execute_action('intro_domain_gender')
                return
            self.error_text = 'Invalid Option!'
        # print('Selection Option: ', int(self.current_text))

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
        if self._current_screen != 'intro_domain_name':
            for char in substring:
                valid &= char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        if valid:
            self.current_text += substring

    def do_backspace(self, from_undo=False, mode='bkspc'):
        # print('Delete something')
        self.current_text = self.current_text[:-1]

    # Screen manager options
    def set_screen(self, screen_name):
        if screen_name == 'back':
            print(screen_name, '←', self._back_list)
            screen_name = self._back_list.pop()
            self._current_screen = screen_name
        else:
            print(self._current_screen, screen_name, self._back_list)
            if self._current_screen is not None and self._current_screen != screen_name:
                for whitelist_name in ['new_name', 'save_select', 'intro_domain', 'intro_select', 'town_main', 'dungeon_main', 'shop']:
                    if self._current_screen.startswith(whitelist_name):
                        self._back_list.append(self._current_screen)
        self._current_screen = screen_name

        names = ['new_game', 'save_select', 'intro_domain_name', 'intro_domain_gender', 'intro_domain', 'intro_select', 'game_loading', 'town_main', 'tavern_main', 'shop', 'quests_main', 'crafting_main', 'inventory_main', 'dungeon_main',
                 'select_screen_char', 'dungeon_confirm', 'dungeon_battle', 'dungeon_result']
        screens = [new_game, save_select, intro_domain_name, intro_domain_gender, intro_domain, intro_select, game_loading, town_main, tavern_main, shop, quests_main, crafting_main, inventory_main, dungeon_main, select_screen_char,
                   dungeon_main_confirm, dungeon_battle, dungeon_result]
        for index, screen in enumerate(names):
            if screen_name.startswith(screen):
                self.display_text, self._options = screens[index](self)
                return
        print('Unknown Screen:', screen_name)

    def set_loading_progress(self, type, label, value, max):
        # print(type, label, value, max)
        self.memory.loading_progress[label] = (value, max)
        self.set_screen('game_loading')

    def get_options(self):
        return self._options

    def execute_action(self, action):
        screens = {'start_game': 'save_select'}
        if action in screens:
            self.set_screen(screens[action])
            return
        elif action == 'exit_game':
            Refs.app.stop()
        elif action.startswith('new_game_'):
            self.memory.game_info['save_slot'] = int(action[-1])
            self.set_screen('intro_domain_name')
        elif action == 'intro_domain_gender':
            self.memory.game_info['name'] = self.current_text.strip()
            self.current_text = ""
            self.set_screen('intro_domain_gender')
        elif action.startswith('gender_'):
            self.memory.game_info['gender'] = action[len('gender_'):]
            self.set_screen('intro_domain')
        elif action.startswith('domain_'):
            if action.endswith('next'):
                self.memory.current_domain += 1
                self.set_screen('intro_domain')
                return
            elif action.endswith('prev'):
                self.memory.current_domain -= 1
                self.set_screen('intro_domain')
                return
            self.memory.game_info['domain'] = action[len('domain_'):]
            self.set_screen('intro_select')
        elif action.startswith('select_'):
            if action.endswith('ais'):
                choice = 0
            else:
                choice = 1
            create_new_save(self.memory.game_info['save_slot'], self.memory.game_info['name'], self.memory.game_info['gender'], None, self.memory.game_info['domain'], choice)
            self.set_screen('game_loading')
            Refs.app.start_loading(self, self.memory.game_info['save_slot'])
        elif action.startswith('load_game'):
            self.set_screen('game_loading')
            Refs.app.start_loading(self, int(action[-1]))
        elif action.startswith('dungeon_main_'):
            index = 0
            if action.endswith('next'):
                index = Refs.gc.get_current_party_index() + 1
            elif action.endswith('prev'):
                index = Refs.gc.get_current_party_index() - 1
            else:
                id = action[len('dungeon_main_'):]
                self.set_screen('select_screen_char_' + id)
                return
            if index == 10:
                index = 0
            elif index == -1:
                index = 9
            Refs.gc.set_current_party_index(index)
            self.set_screen('dungeon_main')
        elif action.startswith('set_char_'):
            char_id_and_index = action[len('set_char_'):]
            index = int(char_id_and_index[:char_id_and_index.index('_')])
            char_id = char_id_and_index[char_id_and_index.index('_') + 1:]
            char = None
            if char_id != 'none':
                char = Refs.gc.get_char_by_id(char_id)

            # Resolve
            if char is not None and char in Refs.gc.get_current_party():
                # Set the char in the party to None
                if Refs.gc.get_current_party()[index] is None:
                    Refs.gc.get_current_party()[Refs.gc.get_current_party().index(char)] = None
                else:
                    Refs.gc.get_current_party()[Refs.gc.get_current_party().index(char)] = Refs.gc.get_current_party()[index]

            Refs.gc.get_current_party()[index] = char
            self.set_screen('dungeon_main')
        elif action.startswith('dungeon_battle'):
            dungeon_battle_action(self, action)
        elif action.startswith('shop') and 'confirm' in action:
            screen_data, item_id = action[len('purchase_'):].split('#')
            screen_name, count = screen_data.split('_confirm')
            # shop_general_confirm1#shovel_weak
            # → shop_general
            do_transaction(item_id, int(count), 'sell' in screen_name)
            self.set_screen(screen_name)
        else:
            self.set_screen(action)

    # More Gamey functions
    def on_start_game(self):
        pass

    def on_load_game(self):
        pass
