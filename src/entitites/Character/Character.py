import math
import random

from kivy.properties import NumericProperty, ObjectProperty, ReferenceListProperty, StringProperty, BooleanProperty, ListProperty, DictProperty
from kivy.uix.widget import WidgetBase
from kivy.clock import mainthread
from src.entitites.Character.Scale import Scale
from src.modules.Screens.CharacterAttributeScreens.CharacterAttributeScreen import CharacterAttributeScreen


class Character(WidgetBase):
    health_base = NumericProperty(0)
    mana_base = NumericProperty(0)
    strength_base = NumericProperty(0)
    magic_base = NumericProperty(0)
    endurance_base = NumericProperty(0)
    dexterity_base = NumericProperty(0)
    agility_base = NumericProperty(0)

    name = StringProperty(None)
    display_name = StringProperty(None)
    id = StringProperty(None)
    _is_support = BooleanProperty(False)
    index = NumericProperty(0)

    slide_image_source = StringProperty(None)
    slide_support_image_source = StringProperty(None)
    preview_image_source = StringProperty(None)
    full_image_source = StringProperty(None)
    program_type = StringProperty(None)

    current_rank = NumericProperty(1)
    current_health = NumericProperty(0)

    element = StringProperty('')
    type = StringProperty('')

    familiarities = DictProperty({})
    familiarity_bonus = NumericProperty(1.0)

    @mainthread
    def __init__(self, rank, type, element, moves, familias, **kwargs):
        super().__init__(**kwargs)

        # Experimental
        self.familia = None
        for familia in familias:
            if familia.name == 'Hestia':
                self.familia = familia
                break
        self.race = 'Human'
        self.gender = 'Female'
        self.score = 0
        self.worth = 0
        self.high_dmg = 0
        self.floor_depth = 0
        self.monsters_slain = 0
        self.people_slain = 0

        self.equipment = Equipment()
        self.equipment.ring = EquipmentItem("Crystal Ring", 'ring_1', 'Magical', 'water', 'G', [0, 10, 0, 15, 5, 0, 20, 0, 15, 20, 900, 545, 100, 1000])
        self.equipment.necklace = EquipmentItem("Sapphire Necklace", 'necklace_2', 'Magical', 'dark', 'SSS', [15, 100, 0, 25, 5, 0, 150, 75, 15, 20, 900, 880, 600, 10000])

        if self.id == 'athlethic_sofi':
            self.familiarities = {
                'amatuer_model': 26.7,
                'architect': 2.02,
                'actresses_alexis_and_emilia': 19.9,
                'badass_ais': 13.2,
                'aye_aye_andrea': 42.3,
                'backyard_abigail': 100.0
            }
        elif self.id == 'amatuer_model_calyse':
            self.familiarities = {
                'athlethic_sofi': 26.7,
                'architect': 13.2,
                'actresses_alexis_and_emilia': 19.6,
                'badass_ais': 14.3,
                'aye_aye_andrea': 42.3,
                'backyard_abigail': 53.2
            }
        elif self.id == 'architect_lexi':
            self.familiarities = {
                'amatuer_model_calyse': 13.2,
                'athlethic_sofi': 2.02,
                'actresses_alexis_and_emilia': 98.06,
                'badass_ais': 68.4,
                'aye_aye_andrea': 100.0,
                'backyard_abigail': 12.3
            }
        elif self.id == 'actresses_alexis_and_emilia':
            self.familiarities = {
                'amatuer_model_calyse': 19.6,
                'architect_lexi': 98.06,
                'athlethic_sofi': 19.9,
                'badass_ais': 16.6,
                'aye_aye_andrea': 54.2,
                'backyard_abigail': 12.3
            }
        elif self.id == 'badass_ais':
            self.familiarities = {
                'amatuer_model_calyse': 14.3,
                'architect_lexi': 68.4,
                'actresses_alexis_and_emilia': 16.6,
                'athlethic_sofi': 13.2,
                'aye_aye_andrea': 15.6,
                'backyard_abigail': 96.0
            }
        elif self.id == 'aye_aye_andrea':
            self.familiarities = {
                'amatuer_model_calyse': 42.3,
                'architect_lexi': 100.0,
                'actresses_alexis_and_emilia': 54.2,
                'badass_ais': 15.6,
                'athlethic_sofi': 42.3,
                'backyard_abigail': 58.0
            }
        elif self.id == 'backyard_abigail':
            self.familiarities = {
                'amatuer_model_calyse': 53.2,
                'architect_lexi': 12.3,
                'actresses_alexis_and_emilia': 12.3,
                'badass_ais': 96.2,
                'aye_aye_andrea': 42.3,
                'athlethic_sofi': 100.0
            }


        # End Experimental

        self.moves = moves
        if type == 0:
            self.type = 'Magical'
        elif type == 1:
            self.type = 'Physical'
        elif type == 2:
            self.type = 'Balanced'
        elif type == 3:
            self.type = 'Defensive'
        else:
            self.type = 'Healing'

        if element == 0:
            self.element = 'Light'
        elif element == 1:
            self.element = 'Dark'
        elif element == 2:
            self.element = 'Earth'
        elif element == 3:
            self.element = 'Wind'
        elif element == 4:
            self.element = 'Thunder'
        elif element == 5:
            self.element = 'Fire'
        else:
            self.element = 'Water'

        try:
            self.ranks = Rank.load_weights("../save/char_load_data/" + self.program_type + '/ranks/' + self.id + '.txt', self.id, rank, self.program_type)
        except FileNotFoundError:
            self.ranks = Rank.load_weights("../save/char_load_data/" + self.program_type + '/ranks/base.txt', self.id, rank, self.program_type)

        self.update_score()

    def update_score(self):
        score = 0
        if self.type == 'Physical':
            score += self.get_strength() / 7.5
            score += self.get_magic() / 10
            score += self.get_endurance() / 8.5
            score += self.get_dexterity() / 9
            score += self.get_agility() / 9
        elif self.type == 'Magical':
            score += self.get_strength() / 10
            score += self.get_magic() / 7.5
            score += self.get_endurance() / 10
            score += self.get_dexterity() / 9
            score += self.get_agility() / 9
        elif self.type == 'Balanced':
            score += self.get_strength() / 8.5
            score += self.get_magic() / 8.5
            score += self.get_endurance() / 9.5
            score += self.get_dexterity() / 9
            score += self.get_agility() / 9
        elif self.type == 'Defensive':
            score += self.get_strength() / 8.5
            score += self.get_magic() / 10
            score += self.get_endurance() / 7.5
            score += self.get_dexterity() / 9
            score += self.get_agility() / 9
        elif self.type == 'Healing':
            score += self.get_strength() / 10
            score += self.get_magic() / 8.5
            score += self.get_endurance() / 10
            score += self.get_dexterity() / 9
            score += self.get_agility() / 9
        self.score = score

    def is_support(self):
        return self._is_support

    def get_type(self):
        return self.type

    def get_index(self):
        return self.index

    def get_familia(self):
        return self.familia

    def get_race(self):
        return self.race

    def get_gender(self):
        return self.gender

    def get_worth(self):
        return self.worth

    def get_high_dmg(self):
        return self.high_dmg

    def get_floor_depth(self):
        return self.floor_depth

    def get_monsters_killed(self):
        return self.monsters_slain

    def get_people_killed(self):
        return self.people_slain

    def get_equipment(self):
        return self.equipment

    def get_element(self):
        return self.element

    def get_current_rank(self):
        return self.current_rank

    def get_rank(self, index):
        return self.ranks[index - 1]

    def rank_up(self):
        if self.current_rank < 10:
            self.current_rank += 1
            self.ranks[self.current_rank - 1].unlocked = True
        else:
            raise Exception("Character at max rank")

    def rank_break(self):
        if not self.ranks[self.current_rank - 1].broken:
            self.ranks[self.current_rank - 1].break_rank(self.type)
            self.update_score()
        else:
            raise Exception("Character already rank broken")

    def get_sprite(self):
        return self.sprite

    def get_name(self):
        return self.name

    def get_display_name(self):
        return self.display_name

    def get_id(self):
        return self.id

    def get_move(self, movenum):
        return self.moves[movenum]

    def get_phyatk(self, rank=0):
        return self.get_strength(rank) + self.equipment.get_phyatk()

    def get_magatk(self, rank=0):
        return self.get_magic(rank) + self.equipment.get_magatk()

    def get_defense(self, rank=0):
        return self.get_endurance(rank) + self.equipment.get_defense()

    def get_health(self, rank=0):
        if rank > 0:
            return self.get_rank(rank).get_health() * self.familiarity_bonus
        health = self.health_base + self.equipment.get_health()
        for rank in self.ranks:
            if rank.unlocked:
                health += rank.get_health()
        return health * self.familiarity_bonus

    def get_mana(self, rank=0):
        if rank > 0:
            return self.get_rank(rank).get_mana() * self.familiarity_bonus
        mana = self.mana_base + self.equipment.get_mana()
        for rank in self.ranks:
            if rank.unlocked:
                mana += rank.get_mana()
        return mana * self.familiarity_bonus

    def get_strength(self, rank=0):
        if rank > 0:
            return self.get_rank(rank).get_strength() * self.familiarity_bonus
        strength = self.strength_base + self.equipment.get_strength()
        for rank in self.ranks:
            if rank.unlocked:
                strength += rank.get_strength()
        return strength * self.familiarity_bonus

    def get_strength_rank(self, rank=0):
        return Scale.get_scale_as_image_path(self.get_strength(rank), 999)

    def get_magic(self, rank=0):
        if rank > 0:
            return self.get_rank(rank).get_magic() * self.familiarity_bonus
        magic = self.magic_base + self.equipment.get_magic()
        for rank in self.ranks:
            if rank.unlocked:
                magic += rank.get_magic()
        return magic * self.familiarity_bonus

    def get_magic_rank(self, rank=0):
        return Scale.get_scale_as_image_path(self.get_magic(rank), 999)

    def get_endurance(self, rank=0):
        if rank > 0:
            return self.get_rank(rank).get_endurance() * self.familiarity_bonus
        endurance = self.endurance_base + self.equipment.get_endurance()
        for rank in self.ranks:
            if rank.unlocked:
                endurance += rank.get_endurance()
        return endurance * self.familiarity_bonus

    def get_endurance_rank(self, rank=0):
        return Scale.get_scale_as_image_path(self.get_endurance(rank), 999)

    def get_dexterity(self, rank=0):
        if rank > 0:
            return self.get_rank(rank).get_dexterity() * self.familiarity_bonus
        dexterity = self.dexterity_base + self.equipment.get_dexterity()
        for rank in self.ranks:
            if rank.unlocked:
                dexterity += rank.get_dexterity()
        return dexterity * self.familiarity_bonus

    def get_dexterity_rank(self, rank=0):
        return Scale.get_scale_as_image_path(self.get_dexterity(rank), 999)

    def get_agility(self, rank=0):
        if rank > 0:
            return self.get_rank(rank).get_agility() * self.familiarity_bonus
        agility = self.agility_base + self.equipment.get_agility()
        for rank in self.ranks:
            if rank.unlocked:
                agility += rank.get_agility()
        return agility * self.familiarity_bonus

    def get_agility_rank(self, rank=0):
        return Scale.get_scale_as_image_path(self.get_agility(rank), 999)

    def get_score(self):
        return round(self.score, 1)

    def update_health(self, health_change, rank, board=False):
        self.ranks[rank].update_health(health_change, board)
        self.update_score()

    def update_mana(self, mana_change, rank, board=False):
        self.ranks[rank].update_mana(mana_change, board)
        self.update_score()

    def update_strength(self, strength_change, rank, board=False):
        self.ranks[rank].update_strength(strength_change, board)
        self.update_score()

    def update_magic(self, magic_change, rank, board=False):
        self.ranks[rank].update_magic(magic_change, board)
        self.update_score()

    def update_endurance(self, endurance_change, rank, board=False):
        self.ranks[rank].update_endurance(endurance_change, board)
        self.update_score()

    def update_dexterity(self, dexterity_change, rank, board=False):
        self.ranks[rank].update_dexterity(dexterity_change, board)
        self.update_score()

    def update_agility(self, agility_change, rank, board=False):
        self.ranks[rank].update_agility(agility_change, board)
        self.update_score()

    def equip_equipment(self, slot, equipment):
        if self.equipment.get_type(slot) is not None:
            print("Item already equipped")
        else:
            self.equipment.set_type(slot, equipment)
        self.update_score()

    def unequip_equipment(self, slot):
        if self.equipment.get_type(slot) is None:
            print("There is no item equipped")
        else:
            self.equipment.set_type(slot, None)

    def update_equipment(self, slot, stat):
        self.equipment.update_type(slot, stat)

    def get_grids(self):
        return self.ranks

    def get_familiarity(self, char_id):
        if char_id in self.familiarities:
            return self.familiarities[char_id]
        return 0

    def add_familiarity(self, key, value):
        if key in self.familiarities:
            if self.familiarities[key] == 100.00:
                return
            if self.familiarities[key] + value > 100.00:
                self.familiarities[key] = 100.00
                return
            self.familiarities[key] += value
        else:
            self.familiarities[key] = value


class Rank(WidgetBase):
    ability_max = NumericProperty(999)
    health_max = NumericProperty(999)
    mana_max = NumericProperty(299)

    # Defense is endurance
    # Attack is Strength / Magic / Both

    health = NumericProperty(0)
    mana = NumericProperty(0)

    strength = NumericProperty(0)
    strength_board = NumericProperty(0)
    magic = NumericProperty(0)
    magic_board = NumericProperty(0)
    endurance = NumericProperty(0)
    endurance_board = NumericProperty(0)
    dexterity = NumericProperty(0)
    dexterity_board = NumericProperty(0)
    agility = NumericProperty(0)
    agility_board = NumericProperty(0)

    def __init__(self, rank, grid, unlocked, broken, **kwargs):
        super().__init__(**kwargs)
        self.unlocked = unlocked
        self.broken = broken
        self.index = rank
        self.grid = grid
        self.brkinc = 1.13

        # self.grid.count()

    def get_health(self):
        return math.floor(self.health)

    def get_health_cap(self):
        return self.health_max

    def get_mana(self):
        return math.floor(self.mana)

    def get_mana_cap(self):
        return self.mana_max

    def get_ability_cap(self):
        return self.ability_max

    def get_strength(self):
        return math.floor(self.strength) + math.floor(self.strength_board)

    def get_magic(self):
        return math.floor(self.magic) + math.floor(self.magic_board)

    def get_endurance(self):
        return math.floor(self.endurance) + math.floor(self.endurance_board)

    def get_dexterity(self):
        return math.floor(self.dexterity) + math.floor(self.dexterity_board)

    def get_agility(self):
        return math.floor(self.agility) + math.floor(self.agility_board)

    def get_rank_stats(self):
        return [self.get_health(), self.get_mana(), self.get_strength(), self.get_magic(), self.get_endurance(), self.get_dexterity(), self.get_agility()]

    def break_rank(self, type):
        self.broken = True
        self.health *= self.brkinc
        if type == 'Physical':
            self.mana *= self.brkinc * 0.75
            self.strength *= self.brkinc
            self.strength_board *= self.brkinc
            self.magic *= self.brkinc * 0.75
            self.magic_board *= self.brkinc * 0.75
            self.endurance *= self.brkinc * 0.75
            self.endurance_board *= self.brkinc * 0.75
        elif type == 'Magical':
            self.mana *= self.brkinc
            self.strength *= self.brkinc * 0.75
            self.strength_board *= self.brkinc * 0.75
            self.magic *= self.brkinc
            self.magic_board *= self.brkinc
            self.endurance *= self.brkinc * 0.75
            self.endurance_board *= self.brkinc * 0.75
        elif type == 'Balanced':
            self.mana *= self.brkinc * 0.75
            self.strength *= self.brkinc * 0.9
            self.strength_board *= self.brkinc * 0.9
            self.magic *= self.brkinc * 0.9
            self.magic_board *= self.brkinc * 0.9
            self.endurance *= self.brkinc * 0.75
            self.endurance_board *= self.brkinc * 0.75
        elif type == 'Defensive':
            self.mana *= self.brkinc * 0.75
            self.strength *= self.brkinc * 0.9
            self.strength_board *= self.brkinc * 0.9
            self.magic *= self.brkinc * 0.75
            self.magic_board *= self.brkinc * 0.75
            self.endurance *= self.brkinc
            self.endurance_board *= self.brkinc
        elif type == 'Healer':
            self.mana *= self.brkinc * 0.9
            self.strength *= self.brkinc * 0.75
            self.strength_board *= self.brkinc * 0.75
            self.magic *= self.brkinc * 0.9
            self.magic_board *= self.brkinc * 0.9
            self.endurance *= self.brkinc * 0.75
            self.endurance_board *= self.brkinc * 0.75
        self.dexterity *= self.brkinc * 0.9
        self.dexterity_board *= self.brkinc * 0.9
        self.agility *= self.brkinc * 0.9
        self.agility_board *= self.brkinc * 0.9

    def update_strength(self, strength_change, board=False):
        if board:
            self.strength_board += strength_change
            # print(self.strength_board)
        else:
            if self.strength < self.ability_max:
                self.strength += strength_change

    def update_magic(self, magic_change, board=False):
        if board:
            self.magic_board += magic_change
        else:
            if self.magic < self.ability_max:
                self.magic += magic_change

    def update_endurance(self, endurance_change, board=False):
        if board:
            self.endurance_board += endurance_change
        else:
            if self.endurance < self.ability_max:
                self.endurance += endurance_change

    def update_dexterity(self, dexterity_change, board=False):
        if board:
            self.dexterity_board += dexterity_change
        else:
            if self.dexterity < self.ability_max:
                self.dexterity += dexterity_change

    def update_agility(self, agility_change, board=False):
        if board:
            self.agility_board += agility_change
        else:
            if self.agility < self.ability_max:
                self.agility += agility_change

    @staticmethod
    def load_weights(filename, id, rank_nums, program_type):
        file = open(filename)
        try:
            grids = Grid.load_grids("../save/char_load_data/" + program_type + "/grids/" + id + ".txt")
        except FileNotFoundError:
            grids = Grid.load_grids("../save/char_load_data/" + program_type + "/grids/base.txt")
        ranks = []
        count = 1
        # print("Loading Weights & girds")
        for level in range(0, len(rank_nums)):
            unlocked = rank_nums[level] > 0
            broken = rank_nums[level] == 2
            ranks.append(Rank(count, grids[count - 1], unlocked, broken))
            count += 1
        # for x in file:
        #     values = x[:-1].split(' ', -1)
        #     print("Loaded: " + str(values))
        #     if not count == 11:
        #         if ranknums[count-1] == 1:
        #             unlocked = True
        #             broken = False
        #         elif ranknums[count-1] == 2:
        #             unlocked = True
        #             broken = True
        #         else:
        #             unlocked = False
        #             broken = False
        #         rank = Rank(count, grids[count-1], unlocked, broken)
        #         count += 1
        #         ranks.append(rank)
        #     else:
        #         ranks.append(values)
        return ranks


class Equipment(WidgetBase):
    weapon = ObjectProperty(None, allownone=True)
    necklace = ObjectProperty(None, allownone=True)
    ring = ObjectProperty(None, allownone=True)
    helmet = ObjectProperty(None, allownone=True)
    vambraces = ObjectProperty(None, allownone=True)
    gloves = ObjectProperty(None, allownone=True)
    chest = ObjectProperty(None, allownone=True)
    grieves = ObjectProperty(None, allownone=True)
    boots = ObjectProperty(None, allownone=True)
    items = ReferenceListProperty(weapon, necklace, ring, helmet, vambraces, gloves, chest, grieves, boots)
    types = ListProperty(['weapon', 'necklace', 'ring', 'helmet', 'vambraces', 'gloves', 'chest', 'grieves', 'boots'])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_type(self, type):
        return self.items[self.types.index(type)]

    def get_health(self):
        health = 0
        for item in self.items:
            if item is not None:
                health += item.get_health()
        return health

    def get_mana(self):
        mana = 0
        for item in self.items:
            if item is not None:
                mana += item.get_mana()
        return mana

    def get_phyatk(self):
        atk = 0
        for item in self.items:
            if item is not None:
                atk += item.get_phyatk()
        return atk

    def get_magatk(self):
        atk = 0
        for item in self.items:
            if item is not None:
                atk += item.get_magatk()
        return atk

    def get_defense(self):
        defense = 0
        for item in self.items:
            if item is not None:
                defense += item.get_defense()
        return defense

    def get_strength(self):
        strength = 0
        for item in self.items:
            if item is not None:
                strength += item.get_strength()
        return strength

    def get_magic(self):
        magic = 0
        for item in self.items:
            if item is not None:
                magic += item.get_magic()
        return magic

    def get_endurance(self):
        endurance = 0
        for item in self.items:
            if item is not None:
                endurance += item.get_endurance()
        return endurance

    def get_dexterity(self):
        dexterity = 0
        for item in self.items:
            if item is not None:
                dexterity += item.get_dexterity()
        return dexterity

    def get_agility(self):
        agility = 0
        for item in self.items:
            if item is not None:
                agility += item.get_agility()
        return agility

    def set_type(self, type, item):
        self.items[self.types.index(type)] = item

    def update_type(self, type, stat):
        item = self.items[self.types.index(type)]


class EquipmentItem:
    def __init__(self, name, id, type, element, rank, values):
        self.name = name
        self.id = id
        self.type = type
        self.values = values
        self.element = element
        self.rank = rank

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def get_type(self):
        return self.type

    def get_element(self):
        return self.element

    def get_health(self):
        return self.values[0]

    def get_mana(self):
        return self.values[1]

    def get_phyatk(self):
        return self.values[2]

    def get_magatk(self):
        return self.values[3]

    def get_defense(self):
        return self.values[4]

    def get_strength(self):
        return self.values[5]

    def get_magic(self):
        return self.values[6]

    def get_endurance(self):
        return self.values[7]

    def get_dexterity(self):
        return self.values[8]

    def get_agility(self):
        return self.values[9]

    def get_durability(self):
        return self.values[10]

    def get_durability_current(self):
        return self.values[11]

    def get_score(self):
        return self.values[12]

    def get_value(self):
        return self.values[13]

    def get_rank(self):
        return self.rank


class Grid:
    def __init__(self, rank_num, grid, unlocked, amounts):
        self.index = rank_num
        self.grid = grid
        self.unlocked = unlocked
        self.amounts = amounts

    def get_grid(self):
        return self.grid, self.unlocked

    def unlock(self, index):
        if self.unlocked[index] == 1:
            print("already unlocked")
        else:
            self.unlocked[index] = 1

    @staticmethod
    def load_grids(filename):
        file = open(filename)
        grids = []
        for x in file:
            grid = []
            ugrid = []
            values = x[:-1].split(" ", -1)
            rank_num = int(values[0])
            length = int(values[1])
            strength = int(values[2])
            magic = int(values[3])
            agility = int(values[4])
            dexterity = int(values[5])
            endurance = int(values[6])
            amounts = [strength, magic, agility, dexterity, endurance]
            values = values[7:]
            row_index = 0
            for y in range(length):
                row = []
                urow = []
                for x in range(length):
                    row.append(str(values[row_index * int(length) + x]))
                    urow.append(0)
                grid.append(list(row))
                ugrid.append(urow)
                row_index += 1
            grids.append(Grid(rank_num, grid, ugrid, amounts))
        return grids
    #update grids to be loaded at the same time as characters, and for base weights to be loaded into the first star. Add label updates to the preview screen. finish configuring the rank updates on the rank label
    #add the experience counter, cost function, cost preview, and stat experience window and stats. centralize characterstrength updates into the character class and by rank. with an update function
    #add a testing rank up button and rank break button to test changes
    #implement basic console fighting during delve to test the combar system. on that note. make the combat system.
    #Make sure to load maximum values unto the character load process.


class Move:
    def __init__(self, name, cover, truename, type, power, effects):
        self.name = name
        self.cover = cover
        self.truename = truename
        self.type = type
        if power == "Low":
            self.powerMin = .15
            self.powerMax = .25
        elif power == "Mid":
            self.powerMin = .35
            self.powerMax = .55
        elif power == "High":
            self.powerMin = .75
            self.powerMax = 1.00
        elif power == "Ultra":
            self.powerMin = .95
            self.powerMax = 1.20
        self.powerString = power
        self.effects = effects

    def generateDamage(self, strength, magic):
        if self.type == 0:
            attack = strength
        else:
            attack = magic
        print("Min: " + str(int(attack * self.powerMin)) + "Max: " + str(int(attack * self.powerMax)))
        damage = random.randint(int(attack * self.powerMin), int(attack*self.powerMax))
        return damage

    def get_name(self):
        if self.cover:
            return self.truename
        else:
            return self.name

    @staticmethod
    def getmove(move_array, move_name):
        for move in move_array:
            if move.get_name() == move_name:
                return move
        return None


class Attack:
    def __init__(self, name, ttype, type, damage):
        self.name = name
        self.ttype = ttype
        self.type = type
        self.damage = damage
        if self.ttype == 0:
            self.ttypeS = "Foe"
        else:
            self.ttypeS = "Foes"

    def generateDamage(self, power):
        percent = random.randint(0, 19) + 1
        damage = percent / 14.0 * (power * ((self.damage+1.0)/3.4))
        if self.ttype == 1:
            damage * 0.8
        return damage

    def findfoe(self, numoffoes):
        return random.randint(0, numoffoes)
    #attack Name
    #attack targeting type
    #attack type 0 - foe 1 - foes
    #attack damage 0 - Low 1 - Mid 2 - High 3 - Ultra 0-4,5-9,10-14,15-20

    #attack elemental type
    #attack special effects
    #makeattack(power, type, effects) returns damage