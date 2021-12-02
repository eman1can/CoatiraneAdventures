__all__ = ('GameContent',)

# Project Imports
from game.crafting_queue import CraftingChar, CraftingQueue
from game.game_calendar import Calendar
from game.battle_character import create_battle_character
from game.crafting_recipe import ALLOY, EQUIPMENT, ITEM, PROCESS
from game.equipment import NECKLACE, RING, UnGeneratedArmor, UnGeneratedTool, UnGeneratedWeapon
from game.floor_data import FloorData
from game.inventory import Inventory
from game.market import Market, PriceTracker
from game.quest_manager import QuestManager
from game.save_load import load_floor_data, save_game
from kivy.cache import Cache
from kivy.clock import Clock
from loading.base import LOADING_LAYERS
from refs import Refs
# from src.spine.skeleton.skeletonloader import SkeletonLoader

# Standard Library Imports
import random


class GameContent:
    def __init__(self, program_type):
        self._obtained_characters = None
        self._obtained_characters_s = None
        self._obtained_characters_a = None
        self._character_skeletons = None
        self._parties = None
        self._characters = None

        self._tavern_locked = True
        self._potion_crafting_locked = False
        self._blacksmithing_locked = False

        self._data = None
        self._program_type = program_type

        self._skeleton_scale = 0.125

        self._current_floor = 0
        self._floor_data = None
        self._save_slot = None

        self._calendar = None
        self._current_housing = None
        self._market = None
        self._quest_manager = None
        self._crafting_queue = None
        self._crafting_queue_advance = None

        self._items = None
        self._general_items = None
        self._shop_items = None
        self._drop_items = None
        self._ingredients = None
        self._potions = None
        self._floor_maps = None

        self._name = ''
        self._domain = ''
        self._domain_object = None
        self._perk_points = 1
        self._unlocked_perks = {}
        self._gender = ''
        self._symbol = ''
        self._quests = 0
        self._inventory = None
        self._varenth = 0
        self._renown = ''
        self._renown_rank = 0
        self._renown_points = 0
        self._last_save_time = 0
        self._lowest_floor = 0  # 0 = Surface

    @staticmethod
    def format_number(number):
        string = ''
        number = str(number)
        end = ''
        if '.' in number:
            end = number[number.index('.'):]
            number = number[:number.index('.')]
        for index, char in enumerate(reversed(number)):
            if index % 3 == 0 and index != 0:
                string = ',' + string
            string = char + string
        return string + end

    @staticmethod
    def number_to_name(number, past=True):
        if past:
            tens = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth']
            teens = ['eleventh', 'twelfth', 'thirteenth', 'fourteenth', 'fifteenth', 'sixteenth', 'seventeenth', 'eighteenth', 'nineteenth']
            ends = ['tenth', 'twent', 'thirt', 'fort', 'fift', 'sixt', 'sevent', 'eight', 'ninet']
        else:  # present
            tens = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
            teens = ['eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'ninetee']
            ends = ['twn', 'twent', 'thirt', 'fort', 'fift', 'sixt', 'sevent', 'eight', 'ninet']

        if number <= 9:
            return tens[number - 1]
        elif 10 < number <= 19:
            return teens[number - 11]
        elif number % 10 == 0:
            base = ends[int(number / 10) - 1]
            if number > 10:
                base += 'ieth' if past else 'y'
            return base
        else:
            base = ends[int(number / 10) - 1]
            suffix = teens[int(number % 10) - 1]
            base += 'y'
            base += f'-{suffix}'
            return base

    def get_item_data(self, item_id):
        if item_id in self._items:
            return self._items[item_id]
        return None

    def get_equipment_data(self, equipment_id):
        if equipment_id in self._data['equipment']:
            return self._data['equipment'][equipment_id]
        return None

    def initialize(self, loader):
        keys = LOADING_LAYERS
        self._data = {}
        for key in keys:
            self._data[key] = loader.get(key)
        for perk_id in self._data['perks']:
            self._unlocked_perks[perk_id] = False

        Cache.register('preview.slides', 25, 60)

        self._market = Market()
        self._quest_manager = QuestManager()
        self._crafting_queue = CraftingQueue()
        self._load_items(self._data['items'])

        self.generate_equipment_market_prices()

        for item_id, price_tracker in self._data['market_prices'].items():
            self._market.add_item_to_market(item_id, price_tracker)

    def _load_items(self, items):
        self._items = items
        self._general_items = {}
        self._shop_items = {}
        self._drop_items = {}
        self._ingredients = {}
        self._potions = {}
        self._floor_maps = {}
        for item_id, item in items.items():
            if not item.is_item():
                continue
            if item.is_floor_map():
                self._floor_maps[item_id] = item
            elif item.is_potion():
                self._potions[item_id] = item
            elif item.is_ingredient():
                self._ingredients[item_id] = item
            elif item.is_drop_item():
                self._drop_items[item_id] = item
            elif item.is_shop_item():
                self._shop_items[item_id] = item
            else:
                self._general_items[item_id] = item

    def update_data(self, save_data):
        self._inventory = Inventory(self['items'], self['equipment'], save_data['inventory'])
        self._crafting_queue.set_inventory(self._inventory)
        self._lowest_floor = save_data['lowest_floor']
        self._varenth = save_data['varenth']
        self._name = save_data['family']['name']
        self._symbol = save_data['family']['symbol']
        self._gender = save_data['family']['gender']
        self._domain = save_data['family']['domain']
        self._renown = save_data['family']['rank']
        self._renown_rank = save_data['family']['rank_index']
        self._renown_points = save_data['family']['rank_points']
        self._last_save_time = save_data['time']
        self._calendar = Calendar(save_data['time'])

        housing_id = save_data['housing']['id']
        self._current_housing = self._data['housing'][housing_id]
        housing_type = save_data['housing']['type']
        bill_due = save_data['housing']['bill_due']
        bill_count = save_data['housing']['bill_count']
        if housing_type == 'rent':
            self._current_housing.set_data(housing_type, bill_due, bill_count)
        else:
            bill_cost = save_data['housing']['bill_cost']
            self._current_housing.set_data(housing_type, bill_due, bill_count, bill_cost)
        self._current_housing.set_installed(save_data['housing']['installed_features'])

        if self._varenth > 20000 and self._renown >= 'H':
            self._tavern_locked = False

        # Load map data into floors
        for floor_id in save_data['map_data']:
            floor_map = self._data['floors'][int(floor_id)].get_map()
            floor_map.create_current_map(save_data['map_data'][floor_id])
            floor_map.load_node_exploration(save_data['map_node_data'][floor_id], save_data['map_node_counters'][floor_id])

        self._perk_points = save_data['perk_points']
        for perk_id in save_data['perks']:
            self._unlocked_perks[perk_id] = True
        self._crafting_queue.load(save_data['crafting_queue'])
        # Load Market Data into market
        for index, floor in enumerate(self._data['floors'].values()):
            defeated = save_data['boss_defeated'][str(floor.get_id())]
            respawn_time = save_data['boss_respawn_time'][str(floor.get_id())]
            floor.set_boss_status(defeated, respawn_time)

    # Crafting Queue

    def initialize_crafting_queue(self):
        for character in self._data['chars'].values():
            self._crafting_queue.init_char(character.get_full_name(), character)

    def add_recipe_to_crafting_queue(self, output_id, type, time, count):
        self._crafting_queue.add_recipe_to_queue(output_id, type, time, count)
        if self._crafting_queue_advance is None:
            self._crafting_queue_advance = Clock.schedule_interval(self.update_crafting_queue, 0.1)

    def update_crafting_queue(self, delta):
        if self._crafting_queue.advance(delta):
            self._crafting_queue_advance.cancel()
            self._crafting_queue_advance = None

    def attach_crafting_queue_display(self, display, item_displays):
        self._crafting_queue.set_display(display, item_displays)

    def detach_crafting_queue_display(self):
        self._crafting_queue.remove_display()

    def get_queue_time(self):
        return self._crafting_queue.get_queue_time()

    # Quest Manager

    def get_quest_manager(self):
        return self._quest_manager

    def set_current_housing(self, housing):
        self._current_housing = housing

    def get_last_save_time(self):
        return self._last_save_time

    def set_domains(self, domain_list):
        self._domains = domain_list
        for domain in self._domains:
            if domain.get_title() == self._domain:
                self._domain_object = domain
                break

    def get_skeleton_scale(self):
        return self._skeleton_scale

    def get_domain_info(self):
        return self._domain_object

    def set_save_slot(self, save_slot):
        self._save_slot = save_slot

    def save_game(self, callback=None):
        if not self._calendar:
            return
        self._last_save_time = self._calendar.get_int_time()
        save_game(self._save_slot, self)
        if callback is not None:
            callback()

    def get_time(self):
        return self._calendar.get_time()

    def get_calendar(self):
        return self._calendar

    def set_calendar_callback(self, callback):
        self._calendar.set_callback(callback)

    def update_lowest_floor(self, floor_num):
        if floor_num > self._lowest_floor:
            self._lowest_floor = floor_num

    def get_lowest_floor(self):
        return self._lowest_floor

    def get_housing(self):
        return self._current_housing

    def get_housing_options(self):
        return list(self._data['housing'].values())

    def get_varenth(self):
        return int(self._varenth)

    def get_name(self):
        return self._name

    def get_gender(self):
        return self._gender

    def get_symbol(self):
        return self._symbol

    def get_score(self):
        score = 0
        for character in self.get_all_obtained_characters():
            score += character.get_score()
        return score

    def get_quests(self):
        return self._quests

    def get_skill_level(self):
        return list(self._unlocked_perks.values()).count(True)

    def add_skill_point(self):
        self._perk_points += 1

    def get_domain(self):
        return self._domain

    def update_varenth(self, delta):
        Refs.log(f'Varenth {self._varenth} → {self._varenth + delta}')
        self._varenth += delta

        if self._varenth < 20000:
            self._tavern_locked = True
        elif self._renown > 'H':
            self._tavern_locked = False

    def get_renown(self):
        return self._renown

    def get_renown_as_index(self):
        return self._renown_rank

    def get_renown_points(self):
        return self._renown_points

    def add_renown_points(self, points):
        self._renown_points += points
        if self._renown_points > 999:
            # TODO: Show Renown Proving Quest
            self._renown_points = 999

    def get_program_type(self):
        return self._program_type

    def __getitem__(self, item):
        if self._data is None:
            return None
        return self._data[item]

    def setup_parties(self):
        self._obtained_characters = []
        self._obtained_characters_a = []
        self._obtained_characters_s = []
        self._character_skeletons = []
        self._parties = [0] + [None for x in range(16)]

    def create_empty_parties(self):
        for x in range(len(self._parties) - 1):
            self.set_party([-1 for _ in range(16)], x)

    def load_parties(self, oc, oca, ocs, cp):
        self._obtained_characters = oc
        self._obtained_characters_a = oca
        self._obtained_characters_s = ocs
        if cp is not None:
            self._parties = cp
        # self.obtain_character(1, False)
        # self.obtain_character(2, False)
        # self.obtain_character(3, False)

    def load_characters(self, characters):
        self._characters = list(characters.values())

    def load_quests(self, quest_data):
        self._quest_manager.load_from_data(quest_data)

    def get_current_party_index(self):
        return self._parties[0]

    def set_current_party_index(self, index):
        self._parties[0] = index

    def get_current_party(self):
        return self._parties[self._parties[0] + 1]

    def get_party(self, index):
        return self._parties[index + 1]

    def get_party_index(self, char_index):
        index = -1
        for index, party in enumerate(self._parties[1:]):
            for character in party:
                if character == char_index:
                    return index
        return index

    def set_party(self, party, index):
        self._parties[index + 1] = party

    def get_char_by_id(self, char_id):
        return self._data['chars'][char_id]

    def get_char_by_index(self, index):
        if index == -1:
            return None
        return self._characters[index]

    def get_characters(self):
        return self._characters

    def get_obtained_characters(self, support):
        chars = []
        if support:
            for char_index in self._obtained_characters_s:
                chars.append(self._characters[char_index])
        else:
            for char_index in self._obtained_characters_a:
                chars.append(self._characters[char_index])
        return chars

    def get_all_obtained_characters(self):
        chars = []
        for char_index in self._obtained_characters:
            chars.append(self._characters[char_index])
        return chars

    def get_obtained_character_indexes(self, support):
        if support:
            return self._obtained_characters_s
        else:
            return self._obtained_characters_a

    def get_all_obtained_character_indexes(self):
        return self._obtained_characters

    def get_non_obtained_characters(self):
        chars = []
        for char in self._characters:
            if char.get_index() not in self._obtained_characters:
                chars.append(char)
        return chars

    def obtain_character(self, char_index, is_support):
        if is_support:
            self._obtained_characters_s.append(char_index)
        else:
            self._obtained_characters_a.append(char_index)
        self._obtained_characters.append(char_index)

    def get_current_party_score(self):
        party = self.get_current_party()
        score = 0
        if party is None:
            return score
        for char_index in party:
            if char_index == -1:
                continue
            score += self._characters[char_index].get_score()
        return round(score, 2)

    def get_char_list(self, current_char):
        party = self.get_current_party()
        if current_char in party and len(party) > 1:
            return [char for char in party if char != -1]
        else:
            # TODO: Need to some how incorporate sorting into chars?
            chars = Refs.gs.get_screen('select_char').ids.multi.data
            return [char['character'] for char in chars]

    def get_next_char(self, current_char, direction):
        char_list = self.get_char_list(current_char)
        return char_list[char_list.index(current_char) - 1] if direction else char_list[(char_list.index(current_char) + 1) % len(char_list)]

    def is_tavern_locked(self):
        return self._tavern_locked

    def is_crafting_locked(self):
        return not self.has_perk('basic_tailor') and not self.has_perk('apprentice_blacksmith') and not self.has_perk('fledgling_alchemist') and not self.has_perk('daedalus_protege')

    def get_perk_points(self):
        return self._perk_points

    def add_perk_point(self):
        self._perk_points += 1

    def has_perk(self, perk_id):
        return self._unlocked_perks[perk_id]

    def unlock_perk(self, perk):
        self._unlocked_perks[perk.get_id()] = True
        self._perk_points -= perk.get_cost()

    def get_unlocked_perks(self):
        perks = []
        for perk_id, unlocked in self._unlocked_perks.items():
            if unlocked:
                perks.append(perk_id)
        return perks

    def find_item(self, item_id):
        if not '/' in item_id:
            if item_id in self._items.keys():
                return self._items[item_id]
            if item_id in self._data['equipment']:
                return self._data['equipment'][item_id]
            return None

        material_ids = item_id.split('/')[:-1]
        if len(material_ids) == 0:
            return None
        material_id = material_ids[0]
        if material_id not in self._data['materials']:
            return None
        material = self._data['materials'][material_id]
        sub_material1 = None
        sub_material2 = None
        if len(material_ids) > 1:
            material_id1 = material_ids[1]
            if material_id1 not in self._data['materials']:
                return None
            sub_material1 = self._data['materials'][material_id1]
            if len(material_ids) > 2:
                material_id2 = material_ids[2]
                if material_id2 not in self._data['materials']:
                    return None
                sub_material2 = self._data['materials'][material_id2]

        equipment_id = item_id.split('/')[-1]
        if equipment_id in self._data['equipment']:
            equipment_class = self._data['equipment'][equipment_id]

            if equipment_class.is_weapon():
                return UnGeneratedWeapon(equipment_class, material, sub_material1, sub_material2)
            elif equipment_class.is_armor():
                return UnGeneratedArmor(equipment_class, material, sub_material1, sub_material2)
            elif equipment_class.is_tool():
                return UnGeneratedTool(equipment_class, material)
            else:
                raise Exception(f"Unimplemented equipment type: {equipment_class}")
        return None

    def find_items(self, item_id_list):
        found_items = []
        for item_id in item_id_list:
            found_items.append(self.find_item(item_id))
        return found_items

    def get_owned_items(self, item_list):
        remove = []
        for item in item_list:
            if self._inventory.get_item_count(item.get_id()) <= 0:
                remove.append(item)
        for item in remove:
            item_list.remove(item)
        return item_list

    def get_market_price(self, item_id):
        return self._market.get_price(item_id)

    def get_market_sell_price(self, item_id):
        return self._market.get_sell_price(item_id)

    def get_market_buy_price(self, item_id):
        return self._market.get_buy_price(item_id)

    def get_inventory(self):
        return self._inventory
    
    def get_magic_stone_types(self):
        items = []
        for drop_item_id, drop_item in self._drop_items.items():
            if drop_item_id.endswith('magic_stone') and Refs.gc.get_lowest_floor() >= drop_item.get_visible_floor():
                items.append(drop_item)
        return items
    
    def get_monster_drop_types(self):
        items = []
        for drop_item_id, drop_item in self._drop_items.items():
            if drop_item_id.endswith('wing') or drop_item_id.endswith('venom') or drop_item_id.endswith('blood') or drop_item_id.startswith('egg') or drop_item_id.endswith('tongue') or drop_item_id.endswith('meat'):
                if Refs.gc.get_lowest_floor() >= drop_item.get_visible_floor():
                    items.append(drop_item)
        return items

    def get_raw_materials(self):
        items = self.get_ore_types()
        for drop_item_id, drop_item in self._drop_items.items():
            if drop_item_id.endswith('scale') or drop_item_id.endswith('hide') or drop_item_id.endswith('claw') or drop_item_id.endswith('fang') or drop_item_id.endswith('horn'):
                if drop_item_id.startswith('raw') and Refs.gc.get_lowest_floor() >= drop_item.get_visible_floor():
                    items.append(drop_item)
        return items

    def get_processed_materials(self):
        items = self.get_ingot_types()
        for drop_item_id, drop_item in self._drop_items.items():
            if drop_item_id.endswith('processed') or drop_item_id.endswith('ingot'):
                if Refs.gc.get_lowest_floor() >= drop_item.get_visible_floor():
                    items.append(drop_item)
        return items

    def get_wood_materials(self):
        materials = []
        for material_id, material in self._data['materials'].items():
            if material.is_wood():
                materials.append(material)
        return materials

    def get_hard_materials(self):
        materials = []
        for material_id, material in self._data['materials'].items():
            if material.is_hard():
                materials.append(material)
        return materials

    def get_soft_materials(self):
        materials = []
        for material_id, material in self._data['materials'].items():
            if material.is_soft():
                materials.append(material)
        return materials

    def get_gem_materials(self):
        materials = []
        for material_id, material in self._data['materials'].items():
            if material.is_gem():
                materials.append(material)
        return materials

    def get_ingredients(self):
        items = []
        for item_id, item in self._ingredients.items():
            if Refs.gc.get_lowest_floor() >= item.get_visible_floor():
                items.append(item)
        return items

    def get_ore_types(self):
        items = []
        for item_id, item in self._ingredients.items():
            if item_id.endswith('ore') and Refs.gc.get_lowest_floor() >= item.get_visible_floor():
                items.append(item)
        return items

    def get_ingot_types(self):
        items = []
        for item_id, item in self._ingredients.items():
            if item_id.endswith('ingot') and Refs.gc.get_lowest_floor() >= item.get_visible_floor():
                items.append(item)
        return items

    def get_shop_item(self, item_id):
        if item_id in self._shop_items:
            return self._shop_items[item_id]
        return None

    def get_shop_items(self, category):
        items = []
        for item_id, item in self._shop_items.items():
            if item.get_category() == category:
                items.append(item)
        return items

    def get_potion(self, item_id):
        if item_id in self._potions:
            return self._potions[item_id]
        return None

    def get_potions(self):
        return self._potions.values()

    def get_drop_item(self, item_id):
        if item_id in self._drop_items:
            return self._drop_items[item_id]
        return None

    def get_drop_items(self):
        return self._drop_items.values()

    def get_floor_maps(self, floor_id):
        items = []
        for floor_map_id, floor_map in self._floor_maps.items():
            if floor_map.get_category() == floor_id:
                items.append(floor_map)
        return items

    def get_store_tools(self, item_id):
        items = []
        equipment_class = self._data['equipment'][item_id]
        for material_id, material in self._data['materials'].items():
            if material.is_hard() and material.is_natural() and not material.is_gem():
                items.append(UnGeneratedTool(equipment_class, material))
        return items

    def get_store_weapons(self, item_id):
        items = []
        equipment_class = self._data['equipment'][item_id]
        for material_id, material in self._data['materials'].items():
            if material.is_hard() and material.is_natural() and not material.is_gem():
                items.append(UnGeneratedWeapon(equipment_class, material, None, None))
        return items

    def get_store_armor(self, item_id):
        items = []
        equipment_class = self._data['equipment'][item_id]
        for material_id, material in self._data['materials'].items():
            if equipment_class.get_sub_type() in [NECKLACE, RING] and material.is_gem():
                items.append(UnGeneratedArmor(equipment_class, material, None, None))
            elif material.is_natural() and not material.is_gem():
                items.append(UnGeneratedArmor(equipment_class, material, None, None))
        return items

    def generate_equipment_market_prices(self):
        for item_id, equipment_class in self._data['equipment'].items():
            for material_id, material in self._data['materials'].items():
                item = None
                if equipment_class.is_tool():
                    if material.is_hard() and material.is_natural() and not material.is_gem():
                        item = UnGeneratedTool(equipment_class, material)
                elif equipment_class.is_weapon():
                    if material.is_hard() and material.is_natural() and not material.is_gem():
                        item = UnGeneratedTool(equipment_class, material)
                elif equipment_class.is_armor():
                    if equipment_class.get_sub_type() in [NECKLACE, RING] and material.is_gem():
                        item = UnGeneratedTool(equipment_class, material)
                    elif material.is_natural() and not material.is_gem():
                        item = UnGeneratedTool(equipment_class, material)
                if item is not None:
                    self._data['market_prices'][item.get_id()] = PriceTracker(item.get_category(), 500, 250, 750, 1)

    def get_equipment(self, equipment_type):
        return self._inventory.get_equipment(equipment_type)

    def get_craftable_recipes(self):
        viable_recipes = []
        viable_recipes += self.get_item_recipes()
        viable_recipes += self.get_potion_recipes()
        viable_recipes += self.get_alloy_recipes()
        viable_recipes += self.get_process_recipes()
        viable_recipes += self.get_equipment_recipes()
        return viable_recipes

    def get_process_recipes(self):
        viable_recipes = []
        for crafting_recipe in self._data['recipes'].values():
            if crafting_recipe.get_type() == PROCESS and self.has_perk(crafting_recipe.get_perk_requirement()):
                viable_recipes.append(crafting_recipe)
        return viable_recipes

    def get_alloy_recipes(self):
        viable_recipes = []
        for crafting_recipe in self._data['recipes'].values():
            if crafting_recipe.get_type() == ALLOY and self.has_perk(crafting_recipe.get_perk_requirement()):
                viable_recipes.append(crafting_recipe)
        return viable_recipes

    def get_item_recipes(self):
        viable_recipes = []
        for crafting_recipe in self._data['recipes'].values():
            if crafting_recipe.get_type() == ITEM and self.has_perk(crafting_recipe.get_perk_requirement()):
                viable_recipes.append(crafting_recipe)
        return viable_recipes

    def get_equipment_recipes(self):
        viable_recipes = []
        for crafting_recipe in self._data['recipes'].values():
            if crafting_recipe.get_type() == EQUIPMENT:
                viable_recipes.append(crafting_recipe)
        return viable_recipes

    def get_potion_recipes(self):
        viable_recipes = []
        return viable_recipes

    def get_abilities(self):
        return self._data['abilities']

    def get_stamina_weight(self):
        stamina_weight = 0
        for character in self._floor_data.get_characters():
            if character.is_dead():
                stamina_weight += 0.35
            elif character.get_stamina() <= 0:
                stamina_weight += 0.25
        return stamina_weight

    def get_enemies_to_floor(self, floor_id):
        enemies = []
        for floor_index in range(floor_id):
            enemies += list(self._data['floors'][floor_index + 1].get_enemies().keys())
        return enemies

    def get_materials_to_floor(self, floor_id):
        materials = []
        for floor_index in range(floor_id):
            floor_materials = self._data['floors'][floor_index + 1].get_resources()
            materials += list(floor_materials['metals'].keys())
            materials += list(floor_materials['gems'].keys())
        return materials

    def get_floor_score(self, floor):
        return self._data['floors'][floor].get_score()

    def set_next_floor(self, descend=True):
        new_floor = self._current_floor + (1 if descend else -1)
        self._floor_data = FloorData(descend, new_floor, self._floor_data)
        self._current_floor = new_floor
        return new_floor

    def reset_floor_data(self):
        self._current_floor = 0
        self._floor_data = None

    def get_floor_data(self):
        return self._floor_data

    def get_floor(self, floor_id):
        return self._data['floors'][floor_id]

    def can_ascend(self):
        return self._current_floor > 0

    def can_descend(self):
        return True

    def load_floor_node_data(self, floor):
        return load_floor_data(self._save_slot, floor)

    """
    Name: Familiarity Bonus
    A bonus value that goes from 0-100
    and generates a 0-48% increase in base stats for characters

    Every Encounter which will call this method will give between a
    0.01 to 0.05 with a round of 3 digits
    """
    @staticmethod
    def generate_familiarity_bonuses(party):
        visited = {}
        bonuses = {}
        for char_index in party:
            if char_index == -1:
                continue
            visited[char_index] = []
            for partner_index in party:
                if partner_index == -1 or char_index == partner_index:
                    continue
                if char_index in visited and partner_index in visited[char_index]:
                    continue
                if partner_index in visited and char_index in visited[partner_index]:
                    continue

                visited[char_index].append(partner_index)
                bonus = round(random.uniform(0.01, 0.05), 3)

                if char_index not in bonuses:
                    bonuses[char_index] = {}
                bonuses[char_index][partner_index] = bonus
                if partner_index not in bonuses:
                    bonuses[partner_index] = {}
                bonuses[partner_index][char_index] = bonus
        del visited
        return bonuses

    """
    Familiarity Bonus Mechanics
    Each character can have a 0.00-100.00 point bonus with another char
    For each 100% they have, they get a 2% bonus w/ and additional 1% at 100
    ex: 50% → 1%, 25% → 0.5%, 99% → 1.98%, 100 -> 3%

    """
    def calculate_familiarity_bonus(self, checking_index, exclude_index=-1, party=None):
        if checking_index == -1:
            return -1, 0, 0, {}

        value_gold = 0.00
        value_total = 0.00
        bonus = 0.00

        count = 0
        familiarity = {}
        character_checking = self.get_char_by_index(checking_index)
        if party is None:
            party = self.get_current_party()
        for char in party:
            if char == checking_index or char == exclude_index or char == -1:
                continue
            character = self.get_char_by_index(char)

            percentage = character_checking.get_familiarity(character.get_id())
            familiarity[character.get_full_name()] = percentage
            if percentage == 100.00:  # gold
                value_gold += 1.0
                bonus += 1.0
            value_total += percentage / 100.0
            bonus += 2.0 * (percentage / 100.0)
            count += 1
        character_checking.familiarity_bonus = 1 + bonus / 100
        if count < 1:
            return -1, 0, 0, {}
        return value_total / count, value_gold / count, bonus, familiarity

    """
    Can be -5%, -4%, -3%, -2%, -1%, 0%, 1%, 2%, 3%, 4%, 5%
    Randomizes the output values for attack and agility
    """
    def get_random_attack_modifier(self):
        return random.choices([0.95, 0.96, 0.97, 0.98, 0.99, 1, 1.1, 1.2, 1.3, 1.4, 1.5], k=1)[0]

    """
    Can be 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.5, 2.75, 3, 3.5, 3.75, 4, 4.75
    Randomizes the output values for the critical
    """
    def get_random_critical_modifier(self):
        return random.choices([1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.5, 2.75, 3, 3.5, 3.75, 4, 4.75], k=1)[0]

    def get_random_modifier(self):
        return random.choices([1.0, 1.1, 1.2, 1.3, 1.4, 1.5], k=1)[0]

    def get_random_wear_amount(self):
        return random.uniform(0.5, 3.0)

    def get_random_stat_increase(self):
        return random.uniform(0.01, 0.1)
