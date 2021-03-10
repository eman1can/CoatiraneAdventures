__all__ = ('GameContent',)

# Project Imports
from game.battle_character import create_battle_character
from game.floor_data import FloorData
from refs import Refs
from src.spine.skeleton.skeletonloader import SkeletonLoader

# Standard Library Imports
import random


class GameContent:
    def __init__(self, program_type):
        self._obtained_characters = None
        self._obtained_characters_s = None
        self._obtained_characters_a = None
        self._character_skeletons = None
        self._skeleton_states = None
        self._parties = None

        self._tavern_locked = False
        self._crafting_locked = True

        self._data = None
        self._program_type = program_type

        self._skeleton_scale = 0.325
        self._skel_loader = SkeletonLoader()

        self._current_floor = 0
        self._floor_data = None

        self._name = ''
        self._domain = ''
        self._skill_level = 0
        self._inventory = None
        self._varenth = 0
        self._renown = ''
        self._lowest_floor = 0  # 0 = Surface

    def get_item_data(self, item_id):
        if item_id in self._data['shop_items']:
            return self._data['shop_items'][item_id]
        else:
            return self._data['drop_items'][item_id]

    def update_data(self, save_data):  # inventory, lowest_floor):
        self._inventory = {}
        for item_id, count in save_data['inventory'].items():
            self._inventory[item_id] = self.get_item_data(item_id)
            self._inventory[f'{item_id}_count'] = count
        self._lowest_floor = save_data['lowest_floor']
        self._varenth = save_data['varenth']
        self._skill_level = save_data['family']['skills']
        self._name = save_data['family']['name']
        self._domain = save_data['family']['domain']
        self._renown = save_data['family']['rank']

    def update_lowest_floor(self, floor_num):
        if floor_num > self._lowest_floor:
            self._lowest_floor = floor_num

    def get_lowest_floor(self):
        return self._lowest_floor

    def get_varenth(self):
        return self._varenth

    def get_name(self):
        return self._name

    def get_skill_level(self):
        return self._skill_level

    def get_domain(self):
        return self._domain

    def update_varenth(self, delta):
        self._varenth += delta

    def get_renown(self):
        return self._renown

    def get_program_type(self):
        return self._program_type

    def setup_parties(self):
        self._obtained_characters = []
        self._obtained_characters_a = []
        self._obtained_characters_s = []
        self._character_skeletons = []
        self._skeleton_states = []
        self._parties = [0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]

    def create_empty_parties(self):
        for x in range(len(self._parties) - 1):
            self.set_party([None for _ in range(16)], x)

    def load_parties(self, oc, oca, ocs, cp):
        self._obtained_characters = oc
        self._obtained_characters_a = oca
        self._obtained_characters_s = ocs
        if cp is not None:
            self._parties = cp

    def initialize(self, loader):
        keys = ['skills', 'abilities', 'enemies', 'floors', 'families', 'chars', 'shop_items', 'drop_items']
        self._data = {}
        for key in keys:
            self._data[key] = loader.get(key)

    def __getitem__(self, item):
        if self._data is None:
            return None
        return self._data[item]

    def get_current_party_index(self):
        return self._parties[0]

    def set_current_party_index(self, index):
        self._parties[0] = index

    def get_current_party(self):
        return self._parties[self._parties[0] + 1]

    def get_party(self, index):
        return self._parties[index + 1]

    def get_party_index(self, char):
        index = -1
        for index, party in enumerate(self._parties[1:]):
            for character in party:
                if character == char:
                    return index
        return index

    def set_party(self, party, index):
        self._parties[index + 1] = party

    def get_char_by_id(self, char_id):
        for char in list(self._data['chars'].values()):
            if char.get_id() == char_id:
                return char
        return None

    def get_obtained_characters(self, support):
        chars = []
        if support:
            for char_index in self._obtained_characters_s:
                chars.append(list(self._data['chars'].values())[char_index])
        else:
            for char_index in self._obtained_characters_a:
                chars.append(list(self._data['chars'].values())[char_index])
        return chars

    def get_all_obtained_character_indexes(self):
        return self._obtained_characters

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
        for char in party:
            if char is not None:
                score += char.get_score()
        return round(score, 2)

    def load_party_skeletons(self):
        battle_chars = []
        skeletons = {}
        for character in self.get_current_party():
            if character is None or character.is_support():
                continue
            battle_chars.append(create_battle_character(character))
        for character in battle_chars:
            skeletons[character] = character.load_skeleton(self._skel_loader)
        return skeletons

    def is_tavern_locked(self):
        return self._tavern_locked

    def is_crafting_locked(self):
        return self._crafting_locked

    def get_lowest_floor(self):
        return self._lowest_floor

    def in_inventory(self, item_id):
        return item_id in self._inventory
    
    def get_inventory_count(self, item_id):
        if item_id in self._inventory:
            return self._inventory[f'{item_id}_count']
        return 0
    
    def get_magic_stone_types(self):
        items = []
        for drop_item_id, drop_item in self._data['drop_items'].items():
            if drop_item_id.endswith('magic_stone'):
                items.append(drop_item)
        return items
    
    def get_monster_drop_types(self):
        items = []
        for drop_item_id, drop_item in self._data['drop_items'].items():
            if drop_item_id.endswith('monster_drop'):
                items.append(drop_item)
        return items

    def get_ingredient_types(self):
        items = []
        for drop_item_id, drop_item in self._data['drop_items'].items():
            if drop_item_id.endswith('ingredient'):
                items.append(drop_item)
        return items

    def get_ore_types(self):
        items = []
        for drop_item_id, drop_item in self._data['drop_items'].items():
            if drop_item_id.endswith('ore'):
                items.append(drop_item)
        return items

    def add_to_inventory(self, item_id, count=1):
        if item_id in self._inventory:
            self._inventory[f'{item_id}_count'] += count
        else:
            self._inventory[item_id] = self.get_item_data(item_id)
            self._inventory[f'{item_id}_count'] = count
        return self._inventory[item_id]

    def remove_from_inventory(self, item_id, count=1):
        if item_id not in self._inventory:
            print(item_id, 'not in inventory')
            return
        else:
            self._inventory[f'{item_id}_count'] -= count
            if self._inventory[f'{item_id}_count'] <= 0:
                self._inventory.pop(item_id)
                self._inventory.pop(f'{item_id}_count')

    def get_shop_items(self, category):
        print('Get Item List', category)
        items = []
        for item in self._data['shop_items'].values():
            if item.get_category() == category and item.is_unlocked():
                items.append(item)
        return items

    def get_shop_item(self, item_id):
        return self._data['shop_items'][item_id]

    def get_drop_item(self, item_id):
        return self._data['drop_items'][item_id]

    def get_owned_items(self, item_list):
        remove = []
        for item in item_list:
            if self.get_inventory_count(item.get_id()) <= 0:
                # item_list.remove(item)
                remove.append(item)
        for item in remove:
            item_list.remove(item)
        return item_list

    def get_char_list(self, current_char):
        party = self.get_current_party()
        if current_char in party and len(party) > 1:
            return [char for char in party if char is not None]
        else:
            chars = Refs.gs.get_screen('select_char').ids.multi.data
            return [char['character'] for char in chars]

    def get_next_char(self, current_char, direction):
        char_list = self.get_char_list(current_char)
        return char_list[char_list.index(current_char) - 1] if direction else char_list[(char_list.index(current_char) + 1) % len(char_list)]

    def get_abilities(self):
        return self._data['abilities']

    def get_floor_score(self, descend=True):
        if descend:
            return self._data['floors'][self._current_floor + 1].get_score()
        else:
            return self._data['floors'][self._current_floor - 1].get_score()

    def set_next_floor(self, descend=True):
        if descend:
            self._floor_data = FloorData(descend, self._current_floor + 1)
            self.update_lowest_floor(self._current_floor + 1)
            return self._current_floor + 1
        else:
            self._floor_data = FloorData(descend, self._current_floor - 1)
            return self._current_floor - 1

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

    """
    Name: Familiarity Bonus
    A bonus value that goes from 0-100
    and generates a 0-48% increase in base stats for characters

    Every Encounter which will call this method will give between a
    0.01 to 0.05 with a round of 3 digits
    """
    @staticmethod
    def generate_familiarity_bonuses(party):
        visited = []
        for char in party:
            if char is None:
                continue
            for partner_char in party:
                if partner_char is None:
                    continue
                if char == partner_char:
                    continue
                if (char, partner_char) in visited or (partner_char, char) in visited:
                    continue
                visited.append((char, partner_char))
                bonus = round(random.uniform(0.01, 0.05), 3)
                # print("Add between ", char.get_id(), partner_char.get_id(), bonus)
                char.add_familiarity(partner_char.get_id(), bonus)
                partner_char.add_familiarity(char.get_id(), bonus)

    """
    Familiarity Bonus Mechanics
    Each character can have a 0.00-100.00 point bonus with another char
    For each 100% they have, they get a 2% bonus w/ and additional 1% at 100
    ex: 50% → 1%, 25% → 0.5%, 99% → 1.98%, 100 -> 3%

    """
    def calculate_familiarity_bonus(self, char_checking, char_exclude=None):
        if char_checking is None:
            return -1

        value_gold = 0.00
        value_total = 0.00
        bonus = 0.00

        count = 0
        fam = {}
        for char in self.get_current_party():
            if char == char_checking or char == char_exclude:
                continue
            if char is not None:
                percentage = char_checking.get_familiarity(char.get_id())
                fam[char.get_display_name().capitalize() + ' ' + char.get_name().capitalize()] = percentage
                if percentage == 100.00:  # gold
                    value_gold += 1
                    bonus += 1
                value_total += percentage / 100
                bonus += 2 * (percentage / 100)
                count += 1
        if count < 1:
            return -1, -1, -1, {}
        return value_total / count, value_gold / count, bonus, fam

    """
    Can be -5%, -4%, -3%, -2%, -1%, 0%, 1%, 2%, 3%, 4%, 5%
    Randomizes the output values for attack and agility
    """
    def get_random_attack_modifier(self):
        return random.choices([0.95, 0.96, 0.97, 0.98, 0.99, 1, 1.1, 1.2, 1.3, 1.4, 1.5], k=1)[0]

    """
        Can be 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.5, 2.75, 3, 3.5, 3.75, 4, 4.75
        Randomizes the output values for attack and agility
        """

    def get_random_critical_modifier(self):
        return random.choices([1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.5, 2.75, 3, 3.5, 3.75, 4, 4.75], k=1)[0]
