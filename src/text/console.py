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
from text.memory import Memory
from text.screens.map_options import map_options
from text.screens.change_equip import change_equip_main
from text.screens.character_attribute_screen import character_attribute_main
from text.screens.crafting import crafting_alloys, crafting_equipment, crafting_main, crafting_process_material, crafting_process_materials
from text.screens.dungeon_main import dungeon_main, dungeon_main_confirm, locked_dungeon_main
from text.screens.gear import gear_main
from text.screens.housing import housing_browse, housing_buy, housing_main, housing_rent
from text.screens.inventory import inventory, inventory_battle, inventory_battle_select
from text.screens.new_game import game_loading, intro_domain, intro_domain_gender, intro_domain_name, intro_news, intro_select, new_game, save_select
from text.screens.select_char import select_screen_char
from text.screens.shop import do_transaction, shop
from text.screens.skill_tree import perk_bestow, perk_info, skill_tree_main
from text.screens.status_board import status_board_main, status_board_unlock, status_board_view_falna
from text.screens.town import profile_main, quests_main, tavern_main, tavern_recruit, tavern_recruit_show, tavern_relax, town_main
from text.screens.dungeon_battle import dungeon_battle, dungeon_battle_action, dungeon_dig_result, dungeon_mine_result, dungeon_result

SCREEN_NAMES = ['new_game', 'save_select', 'intro_domain_name', 'intro_domain_gender', 'intro_domain', 'intro_select', 'game_loading', 'town_main', 'tavern_main', 'shop', 'quests_main', 'crafting_main', 'dungeon_main', 'select_screen_char',
                'dungeon_confirm', 'dungeon_battle', 'dungeon_result', 'tavern_recruit_show', 'tavern_recruit', 'tavern_relax', 'intro_news', 'profile_main', 'housing_main', 'housing_browse', 'housing_rent', 'housing_buy',
                'character_attribute_main', 'status_board_main', 'status_board_unlock', 'status_board_view_falna', 'change_equip_main', 'gear_main', 'map_options', 'skill_tree_main', 'perk_info', 'perk_bestow', 'dungeon_mine_result',
                'dungeon_dig_result', 'inventory_battle_select', 'inventory_battle', 'inventory', 'crafting_process_materials', 'crafting_alloys', 'crafting_process_material', 'crafting_equipment', 'locked_dungeon_main']
SCREENS = [new_game, save_select, intro_domain_name, intro_domain_gender, intro_domain, intro_select, game_loading, town_main, tavern_main, shop, quests_main, crafting_main, dungeon_main, select_screen_char,
           dungeon_main_confirm, dungeon_battle, dungeon_result, tavern_recruit_show, tavern_recruit, tavern_relax, intro_news, profile_main, housing_main, housing_browse, housing_rent, housing_buy, character_attribute_main,
           status_board_main, status_board_unlock, status_board_view_falna, change_equip_main, gear_main, map_options, skill_tree_main, perk_info, perk_bestow, dungeon_mine_result, dungeon_dig_result, inventory_battle_select,
           inventory_battle, inventory, crafting_process_materials, crafting_alloys, crafting_process_material, crafting_equipment, locked_dungeon_main]


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
        self._back_list = []
        self._current_screen = None
        self.error_time = 0.5
        self.memory = Memory()
        self.memory.game_info = {}
        self.memory.loading_progress = {}
        self.memory.party_box = None
        self.memory.select_box = None
        self.header_callback = None

        self.memory.domains = None
        self.memory.current_domain = 0
        self._width = None

        super().__init__(**kwargs)

        self.set_screen('new_game')

    def on_global_font_size(self, *args):
        self._refresh()

    def get_global_font_size(self):
        return int(self.global_font_size[:-2])

    def get_current_screen(self):
        return self._current_screen

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
        if self._current_screen == 'game_loading':
            return
        option = self.current_text.strip()
        if option in self.get_options():
            self.current_text = ""
            self.execute_action(self.get_options()[option])
        else:
            if self._current_screen == 'intro_domain_name':
                self.execute_action('intro_domain_gender')
                return
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
        if self._current_screen != 'intro_domain_name':
            for char in substring:
                valid &= char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        if valid:
            self.current_text += substring

    def do_backspace(self, from_undo=False, mode='bkspc'):
        self.current_text = self.current_text[:-1]

    def save_screen(self, current_screen):
        if self._current_screen is not None and self._current_screen != current_screen:
            if current_screen in self._back_list:
                while self._back_list[-1] != current_screen:
                    self._back_list.pop(-1)
                self._back_list.pop(-1)
                return False
            else:
                if '*' in self._current_screen:
                    if '#' not in self._current_screen:
                        if '#' in current_screen:
                            print('Add', self._current_screen, 'to list')
                            self._back_list.append(self._current_screen)
                            return True
                        else:
                            screen_name = self._current_screen.split('*')[0]
                            if self._back_list[-1].startswith(screen_name):
                                print('Replace', self._back_list[-1], 'with', self._current_screen, 'to list')
                                self._back_list[-1] = self._current_screen
                                return True
                    return False
                self._back_list.append(self._current_screen)
                return True
        return False

    # Screen manager options
    def set_screen(self, screen_name):
        # if screen_name != 'game_loading':
            # print('Set Screen', screen_name)
        if screen_name == 'back':
            print(self._back_list, '←', self._current_screen)
            screen_name = self._back_list.pop()
        else:
            self.save_screen(screen_name)
                # print('Add', self._current_screen, 'to backlist.')
        self._current_screen = screen_name

        for index, screen in enumerate(SCREEN_NAMES):
            if screen_name.startswith(screen):
                self.display_text, self._options = SCREENS[index](self)
                self._refresh_header()
                return

    def set_loading_progress(self, type, label, value, max):
        # print(type, label, value, max)
        self.memory.loading_progress[label] = (value, max)
        self.set_screen('game_loading')

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

    def execute_action(self, action):
        print(action)
        screens = {'start_game': 'save_select'}
        if action in screens:
            self.set_screen(screens[action])
            return
        elif action == 'exit_game':
            Refs.app.stop()
        elif action.startswith('new_game_'):
            self.memory.game_info['save_slot'] = int(action[-1])
            self.set_screen('intro_domain_name')
        elif action == 'goto_new_game':
            self.memory.loading_progress = {}
            Refs.app.reset_loader()
            self.text = '\n\tSaving Game...'
            Clock.schedule_once(lambda dt: Refs.gc.save_game(lambda: self.set_screen('new_game')), 0.5)
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
            create_new_save(self.memory.game_info['save_slot'], self.memory.game_info['name'], self.memory.game_info['gender'], 'symbol_1', self.memory.game_info['domain'], choice)
            self.set_screen('game_loading')
            Refs.app.start_loading(self, self.memory.game_info['save_slot'], 'intro_news')
        elif action.startswith('load_game'):
            self.set_screen('game_loading')
            Refs.app.start_loading(self, int(action[-1]), 'town_main')
            return
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
        elif action == 'dungeon_main' and self._current_screen == 'dungeon_result_experience':
            self.text = '\n\tSaving Game...'
            Clock.schedule_once(lambda dt: Refs.gc.save_game(lambda: self.set_screen('dungeon_main')), 0.5)
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
        elif action.startswith('dungeon_battle_start'):
            Refs.gc.set_next_floor(bool(action[6:]))
            self.text = '\n\tSaving Game...'
            Clock.schedule_once(lambda dt: Refs.gc.save_game(lambda: self.set_screen('dungeon_battle')), 0.5)
        elif action.startswith('dungeon_battle'):
            floor_data = Refs.gc.get_floor_data()
            dungeon_battle_action(self, action)

            if not floor_data.is_in_encounter() and floor_data.get_floor().get_map().is_marker(EXIT):
                if not floor_data.have_beaten_boss():
                    print('Set to locked dungeon main')
                    self.set_screen('locked_dungeon_main')
                    return
        elif action.startswith('shop') and 'confirm' in action:
            screen_data, item_id, count = action.split('#')[:-1]
            screen_name, page_num = screen_data.split('*')
            if not do_transaction(item_id, int(count), 'sell' in screen_name):
                self.error_text = 'Not enough Money!'
                return
            self.set_screen(screen_data)
        elif action == 'save_game':
            self.text = '\n\tSaving Game...'
            Clock.schedule_once(lambda dt: Refs.gc.save_game(lambda: self.set_screen('town_main')), 0.5)
        elif action == 'crafting_main':
            if Refs.gc.is_crafting_locked():
                self.error_time = 2.5
                self.error_text = 'You need an adventurer with a crafting perk.'
            else:
                self.set_screen(action)
        elif action == 'crafting_potions':
            if Refs.gc.is_potion_crafting_locked():
                self.error_time = 2.5
                self.error_text = 'You need an adventurer with the Fledgling Alchemist perk.'
            else:
                self.set_screen(action)
        elif action == 'crafting_blacksmithing':
            if Refs.gc.is_blacksmithing_locked():
                self.error_time = 2.5
                self.error_text = 'You need an adventurer with the Apprentice Blacksmith perk.'
            else:
                self.set_screen(action)
        elif action == 'tavern_main':
            if Refs.gc.is_tavern_locked():
                self.error_time = 2.5
                self.error_text = 'You need at least 20k Varenth and Renown of H to visit the tavern.'
            else:
                self.set_screen(action)
        elif action == 'tavern_recruit_start':
            cost = 25000
            if cost > Refs.gc.get_varenth():
                self.error_time = 2.5
                self.error_text = 'You don\'t have that much money!'
            else:
                Refs.gc.update_varenth(-cost)
                success = randint(1, 99) < 33
                if success:
                    chars = Refs.gc.get_non_obtained_characters()
                    count = choices([x + 1 for x in range(len(chars))], [len(chars) - x for x in range(len(chars))])[0]
                    # Change to choose characters based on a recruitment weight
                    recruited = choices(chars, k=count)
                    string = ''
                    for char in recruited:
                        string += char.get_id() + '#'
                else:
                    string = 'failure#'
                self.set_screen(f'tavern_recruit_show#{string[:-1]}')
        elif action.startswith('tavern_recruit_end'):
            character_id = action.split('#')[1]
            character = Refs.gc.get_char_by_id(character_id)
            for item_id, count in character.get_recruitment_items().items():
                material_ids = item_id.split('/')
                item_id = material_ids.pop(-1)
                if len(material_ids) > 0:
                    metadata = {'material_id': material_ids[0]}
                    if len(material_ids) > 1:
                        metadata['sub_material1_id'] = material_ids[1]
                        if len(material_ids) > 2:
                            metadata['sub_material2_id'] = material_ids[2]
                else:
                    metadata = None

                if Refs.gc.get_inventory().get_item_count(item_id, metadata) < count:
                    self.error_time = 2.5
                    self.error_text = 'You don\'t have the required items!'
                else:
                    Refs.gc.obtain_character(character.get_index(), character.is_support())
                    self.set_screen('tavern_recruit')
        elif action == 'housing_pay_bill':
            if not Refs.gc.get_housing().pay_bill():
                self.error_time = 2.5
                self.error_text = 'You don\'t have enough money to cover the payment!'
            self.set_screen('housing_main')
        elif action.startswith('housing_rent') and 'confirm' in action:
            housing = Refs.gc['housing'][action.split('#')[1]]
            if Housing.rent_housing(Refs.gc.get_housing(), housing):
                self.set_screen('housing_main')
            else:
                self.error_time = 2.5
                self.error_text = 'You don\'t have enough money to cover the first payment!'
        elif action.startswith('housing_buy') and 'confirm' in action:
            housing_name, down_payment = action.split('#')[1:-1]
            housing = Refs.gc['housing'][housing_name]
            if Housing.buy_housing(Refs.gc.get_housing(), housing, int(down_payment)):
                self.set_screen('housing_main')
            else:
                self.error_time = 2.5
                self.error_text = 'You don\'t have that much money!'
        elif action.startswith('status_board_unlock_confirm_'):
            info_string = action[len('status_board_unlock_confirm_'):]
            info_string, tile_list, character_id = info_string.split('#')
            hsc, hmc, hec, hac, hdc, ftype, vcost, rank_index = info_string.split('_')
            Refs.gc.update_varenth(-int(vcost))
            if int(hsc) > 0:
                Refs.gc.remove_from_inventory(f'{ftype}_strength_falna', int(hsc))
            if int(hmc) > 0:
                Refs.gc.remove_from_inventory(f'{ftype}_magic_falna', int(hmc))
            if int(hec) > 0:
                Refs.gc.remove_from_inventory(f'{ftype}_endurance_falna', int(hec))
            if int(hac) > 0:
                Refs.gc.remove_from_inventory(f'{ftype}_agility_falna', int(hac))
            if int(hdc) > 0:
                Refs.gc.remove_from_inventory(f'{ftype}_dexterity_falna', int(hdc))
            board = Refs.gc.get_char_by_id(character_id).get_rank(rank_index).get_baord()
            for tile_index in tile_list.split('_'):
                board.unlock_index(int(tile_index))
            self.set_screen(f'status_board_main_{character_id}_{rank_index}')
        elif action.startswith('map_options_'):
            action = action[len('map_options_'):]
            floor_map = Refs.gc.get_floor_data().get_floor().get_map()

            if action.startswith('toggle'):
                active = action.endswith('True')
                active_length = 5 if active else 6
                layer = action[len('toggle_'):-active_length]
                if layer == 'map':
                    floor_map.set_enabled(active)
                else:
                    floor_map.set_layer_active(layer, active)
                self.set_screen('map_options')
                return
            elif action.startswith('change_destination_'):
                path = action[len('change_destination_'):]
                floor_map.set_current_path(path)
                self.set_screen('map_options')
                return
            elif action.startswith('change_radius_'):
                radius = action[len('change_radius_'):]
                floor_map.set_radius(int(radius))
                self.set_screen('map_options')
                return
            self.set_screen('map_options_' + action)
        elif action.startswith('perk_bestow') and '#' in action:
            perk_information, character_id = action.split('#')
            perk_id = perk_information[len('perk_bestow_'):]
            perk = Refs.gc['perks'][perk_id]
            character = Refs.gc.get_char_by_id(character_id)
            character.bestow_perk(perk)
            Refs.gc.unlock_perk(perk)
            self.set_screen('perk_info_' + perk_id)
        elif action == 'dungeon_result_harvest_materials':
            current_harvesting_knife = Refs.gc.get_inventory().get_current_harvesting_knife()
            if current_harvesting_knife is None:
                self.error_time = 2.5
                self.error_text = 'You have no harvesting knife selected!'
            else:
                self.set_screen(action)
        elif action == 'dungeon_mine_result':
            current_pickaxe = Refs.gc.get_inventory().get_current_pickaxe()
            if current_pickaxe is None:
                self.error_time = 2.5
                self.error_text = 'You have no pickaxe selected!'
            else:
                if current_pickaxe.get_hardness() < Refs.gc.get_floor_data().get_floor().get_hardness():
                    self.error_time = 2.5
                    self.error_text = 'Your pickaxe is not hard enough!'
                else:
                    self.set_screen(action)
        elif action == 'dungeon_dig_result':
            current_shovel = Refs.gc.get_inventory().get_current_shovel()
            if current_shovel is None:
                self.error_time = 2.5
                self.error_text = 'You have no shovel selected!'
            else:
                if current_shovel.get_hardness() < Refs.gc.get_floor_data().get_floor().get_hardness():
                    self.error_time = 2.5
                    self.error_text = 'Your shovel is not hard enough!'
                else:
                    self.set_screen(action)
        elif action.startswith('inventory_battle_use'):
            pass  # TODO Implement potions
        elif action.startswith('inventory_battle_set'):
            page_data, key, item_id = action.split('#', 2)
            page_name, page_num = page_data.split('*')
            page_num = int(page_num)

            item_hash = None
            if item_id != 'none':
                item_id, item_hash = item_id.split('#')
                item_hash = int(item_hash)

            inventory = Refs.gc.get_inventory()

            if item_id == 'pickaxe':
                item = inventory.set_current_pickaxe(item_hash)
            elif item_id == 'shovel':
                item = inventory.set_current_shovel(item_hash)
            else:
                item = inventory.set_current_harvesting_knife(item_hash)
            if item is None:
                self.set_screen(f'inventory_battle_select{key}*{page_num}#none')
            else:
                self.set_screen(f'inventory_battle_select{key}*{page_num}#{item.get_full_id()}')
        elif action.startswith('crafting_process_material') and 'confirm' in action:
            page_name, recipe_id, recipe_count = action.split('#')
            page_num = page_name.split('*')
            recipe = Refs.gc['recipes'][recipe_id]
            recipe_count = int(recipe_count)
            inventory = Refs.gc.get_inventory()
            for ingredient, count in recipe.get_ingredients().items():
                inventory.remove_item(ingredient, count * recipe_count)
            inventory.add_item(recipe.get_item_id(), recipe_count)
            self.set_screen(f'crafting_process_materials*{page_num}')
        else:
            self.set_screen(action)
