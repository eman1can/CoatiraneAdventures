from game.entity import Entity
from game.equipment import WEAPON_TYPES
from game.outfit import Outfit
from game.rank import MAX_RANK
from game.scale import Scale
from game.skill import ELEMENTS
from refs import Refs

ADVENTURER = 0
SUPPORTER  = 1
CHARACTER_TYPES = {ADVENTURER: 'Adventurer', SUPPORTER: 'Supporter'}

PHYSICAL_ATTACK = 0
MAGICAL_ATTACK = 1
HYBRID_ATTACK = 2
DEFENSIVE = 3
HEALING = 4

CHARACTER_ATTACK_TYPES = {
    PHYSICAL_ATTACK: 'Physical',
    MAGICAL_ATTACK: 'Magical',
    HYBRID_ATTACK: 'Hybrid',
    DEFENSIVE: 'Defensive',
    HEALING: 'Healing'
}

UNKNOWN = 0
MALE = 1
FEMALE = 2
GENDERS = {UNKNOWN: 'Unknown', MALE: 'Male', FEMALE: 'Female'}

HUMAN         = 1
GOD           = 2
SPIRIT        = 3
PALLUM        = 4
HALF_PALLUM   = 5
ELF           = 6
HIGH_ELF      = 7
HALF_ELF      = 8
DARK_ELF      = 9
HIGH_DARK_ELF = 10
HALF_DARK_ELF = 11
DWARF         = 12
HALF_DWARF    = 13
AMAZON        = 14
BOAZ          = 15
CHIENTHROPE   = 16
CAT_PEOPLE    = 17
COW           = 18
RACCOON       = 19
HUME_BUNNY    = 20
SHEEP         = 21
RENARD        = 22
WEREWOLF      = 23
WERETIGER     = 24
XENOS         = 25
RACES = {
    UNKNOWN: 'Unknown',
    HUMAN: 'Human',
    GOD: 'God',
    SPIRIT: 'Spirit',
    PALLUM: 'Pallum',
    HALF_PALLUM: 'Half Pallum',
    ELF: 'Elf',
    HIGH_ELF: 'High Elf',
    HALF_ELF: 'Half Elf',
    DARK_ELF: 'Dark Elf',
    HIGH_DARK_ELF: 'High Dark Elf',
    HALF_DARK_ELF: 'Half Dark Elf',
    DWARF: 'Dwarf',
    HALF_DWARF: 'Half Dwarf',
    AMAZON: 'Amazon',
    BOAZ: 'Boaz',
    CHIENTHROPE: 'Chienthrope',
    CAT_PEOPLE: 'Cat People',
    COW: 'Cow',
    RACCOON: 'Raccoon',
    HUME_BUNNY: 'Hume Bunny',
    SHEEP: 'Sheep',
    RENARD: 'Renard',
    WEREWOLF: 'Werewolf',
    WERETIGER: 'Weretiger',
    XENOS: 'Xenos'
}

HEALTH    = 0
MANA      = 1
STRENGTH  = 2
MAGIC     = 3
ENDURANCE = 4
AGILITY   = 5
DEXTERITY = 6


class Character(Entity):
    def __init__(self, identifier, name, skel_path, res_path, hp, mp, s, m, e, a, d, element, skills, **kwargs):
        # Values set by kwargs
        self._display_name = ''
        self._family = ''
        self._gender = ''
        self._race = ''
        self._age = 0
        self._description = ''

        self._high_damage = 0  # Not yet implemented
        self._lowest_floor = 0  # Not yet implemented
        self._monsters_slain = 0  # Not yet implemented
        self._people_slain = 0  # Not yet implemented

        self._is_support = False
        self._index = -1

        self._full = f'{res_path}_full.png'
        self._inspect = f'{res_path}_inspect.png'
        self._slide = f'{res_path}_slide.png'
        self._preview = f'{res_path}_preview.png'
        self._slide_support = f'{res_path}_slide_support.png'
        self._bustup = f'{res_path}_bustup.png'
        self._portrait = f'{res_path}_portrait.png'
        self._symbol = Refs.gc.get_symbol()

        self._rank = -1
        self._ranks = None
        self._attack_type = -1

        self._familiarities = {}
        self._familiarity_bonus = 1

        self._recruitment_items = {}
        self._favorite_weapon = -1
        self._favorite_sub_weapon = -1

        self._outfit = Outfit()

        self._abilities = []

        # Load kwargs
        for kwarg, value in kwargs.items():
            if hasattr(self, kwarg):
                setattr(self, kwarg, value)
        for key in [kwarg for kwarg in kwargs if hasattr(self, kwarg)]:
            del kwargs[key]
        if len(kwargs) > 0:
            print(kwargs)
            raise ValueError("Unknown kwarg values for Character")

        self._score = 0
        self._worth = 0  # Not yet implemented

        if not self._is_support:
            skills[7].set_special()

        super().__init__(identifier, name, skel_path, hp, mp, s, m, e, s, m, e, a, d, element, skills)

        self.refresh_stats()

    # Refresh and calculation functions

    def refresh_stats(self):
        for rank in self._ranks:
            rank.refresh_stats()
        self._outfit.refresh_stats(self._favorite_weapon, self._favorite_sub_weapon)
        super().refresh_stats()
        self.update_score()
        self.update_worth()

    def update_score(self):
        self._score = 0
        weights = [[7.5, 10, 8.5, 9, 9], [10, 7.5, 10, 9, 9], [8.5, 8.5, 9.5, 9, 9], [8.5, 10, 7.5, 9, 9], [10, 8.5, 10, 9, 9]]
        if self._attack_type is not None:
            weight_set = weights[self._attack_type]
        else:
            weight_set = [9, 9, 9, 9, 9]
        value_array = [self.strength, self.magic, self.endurance, self.dexterity, self.agility]
        for index in range(5):
            self._score += value_array[index] / weight_set[index]

    def update_worth(self):
        self._worth = 0

    def get_score(self):
        return round(self._score, 1)

    def get_familiarity(self, char_id):
        if char_id in self._familiarities:
            return self._familiarities[char_id]
        return 0

    def get_familiarities(self):
        return self._familiarities

    def add_familiarity(self, key, value):
        if key in self._familiarities:
            if self._familiarities[key] == 100.00:
                return
            if self._familiarities[key] + value > 100.00:
                self._familiarities[key] = 100.00
                return
            self._familiarities[key] += value
        else:
            self._familiarities[key] = value

    def set_familiarity_bonus(self, bonus):
        self._familiarity_bonus = bonus

    # Basic info functions

    def get_id(self):
        return self._id

    def get_display_name(self):
        return self._display_name

    def get_full_name(self):
        return f'{self._display_name.title()} {self.get_name().title()}'

    def get_skills(self):
        # 0 Basic 1 Move1 2 Move1 Mana 3 Move2 4 Move2 Mana 5 Move3 6 Move3 Mana 7 Special
        return self._moves[:2] + self._moves[3:4] + self._moves[5:6] + self._moves[7:8]

    def get_mana_cost(self, skill):
        index = self._moves.index(skill)
        if index in (0, 7, 8, 9):
            return 0
        return self._moves[index + 1]

    def get_counter_skill(self):
        return self._moves[-2]

    def get_block_skill(self):
        return self._moves[-1]

    def get_support_skill(self):
        if self._rank == 10:
            return self._moves[4]
        elif self._rank >= 7:
            return self._moves[3]
        elif self._rank >= 5:
            return self._moves[2]
        elif self._rank >= 3:
            return self._moves[1]
        else:
            return self._moves[0]

    def get_image(self, image_type):
        if image_type == 'slide':
            return self._slide
        elif image_type == 'slide_support':
            return self._slide_support
        elif image_type == 'preview':
            return self._preview
        elif image_type == 'bustup':
            return self._bustup
        elif image_type == 'full':
            return self._full
        elif image_type == 'portrait':
            return self._portrait
        else:
            return self._inspect

    def is_support(self):
        return self._is_support

    def get_attack_type(self):
        return self._attack_type

    def get_attack_type_string(self):
        if self._attack_type not in CHARACTER_ATTACK_TYPES:
            return ''
        return CHARACTER_ATTACK_TYPES[self._attack_type]

    def get_index(self):
        return self._index

    def get_family(self):
        return self._family

    def get_race(self):
        return RACES[self._race]

    def get_gender(self):
        return GENDERS[self._gender]

    def get_age(self):
        return self._age

    def get_description(self):
        return self._description

    def get_recruitment_items(self):
        return self._recruitment_items

    def get_favorite_weapon(self):
        return WEAPON_TYPES[self._favorite_weapon]

    def get_favorite_sub_weapon(self):
        if self._favorite_sub_weapon is None:
            return None
        return WEAPON_TYPES[self._favorite_sub_weapon]

    def get_worth(self):
        return self._worth

    def get_high_damage(self):
        return self._high_damage

    def get_floor_depth(self):
        return self._lowest_floor

    def get_monsters_killed(self):
        return self._monsters_slain

    def get_people_killed(self):
        return self._people_slain

    def get_outfit(self):
        return self._outfit

    def get_element_string(self):
        if self._element not in ELEMENTS:
            return ''
        return ELEMENTS[self._element]





    # Rank and ability management functions

    def get_current_rank(self):
        return self._rank

    def get_rank(self, index=None):
        if index is None:
            index = self._rank
        return self._ranks[index - 1]

    def get_ranks(self):
        return self._ranks

    def rank_up(self):
        if self._rank < MAX_RANK:
            self._rank += 1
            self.get_rank().unlock()

    def rank_break(self):
        rank = self.get_rank()
        if not rank.is_broken():
            rank.break_rank(self._attack_type)
        self.refresh_stats()

    def max_stats(self):
        self.get_rank().max_stats()
        self.refresh_stats()

    # TODO: Make ability class
    # - Ability class is in Skill file
    def get_ability(self, index):
        print(self._abilities)
        if index < len(self._abilities):
            return self._abilities[index]
        return None

    def has_perk(self, perk_id):
        return perk_id in self._abilities

    def bestow_perk(self, perk):
        self._abilities.append(perk.get_id())

    def get_perks(self):
        return self._abilities

    # def get_ability_options(self, abilities):
    #     return abilities[:3]
    def add_ability(self, ability):
        self._abilities.append(ability)

    def get_abilities(self):
        return self._abilities

    # HMPMD & SMEAD Functions
    def get_physical_attack(self, rank=0):
        if rank > 0:
            return self.get_rank(rank).get_strength()
        return self.physical_attack

    def update_physical_attack(self):
        physical_attack = self._physical_attack + self._outfit.get_physical_attack()
        for rank in self._ranks:
            if rank.is_unlocked():
                physical_attack += rank.get_strength()
        self.physical_attack = physical_attack

    def get_magical_attack(self, rank=0):
        if rank > 0:
            return self.get_rank(rank).get_magic()
        return self.magical_attack

    def update_magical_attack(self):
        magical_attack = self._magical_attack + self._outfit.get_magical_attack()
        for rank in self._ranks:
            if rank.is_unlocked():
                magical_attack += rank.get_magic()
        self.magical_attack = magical_attack

    def get_defense(self, rank=0):
        if rank > 0:
            return self.get_rank(rank).get_endurance()
        return self.defense

    def update_defense(self):
        defense = self._defense + self._outfit.get_defense()
        for rank in self._ranks:
            if rank.is_unlocked():
                defense += rank.get_endurance()
        self.defense = defense

    def get_health(self, rank=0):
        if rank > 0:
            return self.get_rank(rank).get_health() * self._familiarity_bonus
        return self.health

    def update_health(self):
        health = self._health + self._outfit.get_health()
        for rank in self._ranks:
            if rank.is_unlocked():
                health += rank.get_health()
        self.health = health * self._familiarity_bonus

    def increase_health(self, delta):
        self.get_rank().increase_health(delta)
        self.update_health()

    def get_mana(self, rank=0):
        if rank > 0:
            return self.get_rank(rank).get_mana() * self._familiarity_bonus
        return self.mana

    def update_mana(self):
        mana = self._mana + self._outfit.get_mana()
        for rank in self._ranks:
            if rank.is_unlocked():
                mana += rank.get_mana()
        self.mana = mana * self._familiarity_bonus

    def increase_mana(self, delta):
        self.get_rank().increase_mana(delta)
        self.update_mana()

    def get_strength(self, rank=0):
        if rank > 0:
            return self.get_rank(rank).get_strength() * self._familiarity_bonus
        return self.strength

    def update_strength(self):
        strength = self._strength
        for rank in self._ranks:
            if rank.is_unlocked():
                strength += rank.get_strength()
        self.strength = strength * self._familiarity_bonus

    def increase_strength(self, delta):
        self.get_rank().increase_strength(delta)
        self.update_strength()
        self.update_physical_attack()

    def get_magic(self, rank=0):
        if rank > 0:
            return self.get_rank(rank).get_magic() * self._familiarity_bonus
        return self.magic

    def update_magic(self):
        magic = self._magic
        for rank in self._ranks:
            if rank.is_unlocked():
                magic += rank.get_magic()
        self.magic = magic * self._familiarity_bonus

    def increase_magic(self, delta):
        self.get_rank().increase_magic(delta)
        self.update_magic()
        self.update_magical_attack()

    def get_endurance(self, rank=0):
        if rank > 0:
            return self.get_rank(rank).get_endurance() * self._familiarity_bonus
        return self.endurance

    def update_endurance(self):
        endurance = self._endurance
        for rank in self._ranks:
            if rank.is_unlocked():
                endurance += rank.get_endurance()
        self.endurance = endurance * self._familiarity_bonus

    def increase_endurance(self, delta):
        self.get_rank().increase_endurance(delta)
        self.update_endurance()
        self.update_defense()

    def get_agility(self, rank=0):
        if rank > 0:
            return self.get_rank(rank).get_agility() * self._familiarity_bonus
        return self.agility

    def update_agility(self):
        agility = self._agility
        for rank in self._ranks:
            if rank.is_unlocked():
                agility += rank.get_agility()
        self.agility = agility * self._familiarity_bonus

    def increase_agility(self, delta):
        self.get_rank().increase_agility(delta)
        self.update_agility()

    def get_dexterity(self, rank=0):
        if rank > 0:
            return self.get_rank(rank).get_dexterity() * self._familiarity_bonus
        return self.dexterity

    def update_dexterity(self):
        dexterity = self._dexterity
        for rank in self._ranks:
            if rank.is_unlocked():
                dexterity += rank.get_dexterity()
        self.dexterity = dexterity * self._familiarity_bonus

    def increase_dexterity(self, delta):
        self.get_rank().increase_dexterity(delta)
        self.update_dexterity()

    # Rank functions
    def get_strength_rank_image(self, rank=0):
        if rank > 1:
            return Scale.get_scale_as_image_path(self.get_strength(rank), 100)
        return Scale.get_scale_as_image_path(self.get_strength(), 1000)

    def get_strength_rank(self, rank=0):
        if rank > 1:
            return Scale.get_scale_as_character(self.get_strength(rank), 100)
        return Scale.get_scale_as_character(self.get_strength(), 1000)

    def get_magic_rank_image(self, rank=0):
        if rank > 1:
            return Scale.get_scale_as_image_path(self.get_magic(rank), 100)
        return Scale.get_scale_as_image_path(self.get_magic(), 1000)

    def get_magic_rank(self, rank=0):
        if rank > 1:
            return Scale.get_scale_as_character(self.get_magic(rank), 100)
        return Scale.get_scale_as_character(self.get_magic(), 1000)

    def get_endurance_rank_image(self, rank=0):
        if rank > 1:
            return Scale.get_scale_as_image_path(self.get_endurance(rank), 100)
        return Scale.get_scale_as_image_path(self.get_endurance(), 1000)

    def get_endurance_rank(self, rank=0):
        if rank > 1:
            return Scale.get_scale_as_character(self.get_endurance(rank), 100)
        return Scale.get_scale_as_character(self.get_endurance(), 1000)

    def get_dexterity_rank_image(self, rank=0):
        if rank > 1:
            return Scale.get_scale_as_image_path(self.get_dexterity(rank), 100)
        return Scale.get_scale_as_image_path(self.get_dexterity(), 1000)

    def get_dexterity_rank(self, rank=0):
        if rank > 1:
            return Scale.get_scale_as_character(self.get_dexterity(rank), 100)
        return Scale.get_scale_as_character(self.get_dexterity(), 1000)

    def get_agility_rank_image(self, rank=0):
        if rank > 1:
            return Scale.get_scale_as_image_path(self.get_agility(rank), 100)
        return Scale.get_scale_as_image_path(self.get_agility(), 1000)

    def get_agility_rank(self, rank=0):
        if rank > 1:
            return Scale.get_scale_as_character(self.get_agility(rank), 100)
        return Scale.get_scale_as_character(self.get_agility(), 1000)

    # Equipment functions
    def get_equipment(self):
        return self._outfit

    def equip_equipment(self, slot, equipment):
        if self._outfit.get_type(slot) is not None:
            print("Item already equipped")
        else:
            self._outfit.set_type(slot, equipment)
        self.refresh_stats()

    def un_equip_equipment(self, slot):
        if self._outfit.get_type(slot) is None:
            print("There is no item equipped")
        else:
            self._outfit.set_type(slot, None)
        self.refresh_stats()

    def update_equipment(self, slot, stat):
        self._outfit.update_type(slot, stat)
        self.refresh_stats()
