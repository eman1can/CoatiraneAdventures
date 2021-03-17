__all__ = ('Skill', 'ATTACK_TYPES', 'ATTACK_TYPE_INDEX_TO_STRING', 'ELEMENTS', 'ELEMENT_INDEX_TO_STRING', 'MODIFIERS', 'MOD_INDEX_TO_STRING', 'SPEEDS', 'SPEED_INDEX_TO_STRING', 'TARGET_INDEX_TO_STRING', 'ALL_ALLIES', 'ALL_FOES', 'FOE', 'SELF',)

# Ranks
RANKS = ['I', 'H', 'G', 'F', 'E', 'D', 'C', 'B', 'A', 'S', 'SS', 'SSS']

# LINE TYPES
SKILL = 0
ABILITY = 1

# Skill Attack type
ATTACK_TYPE_PHYSICAL = 0
ATTACK_TYPE_MAGICAL = 1
ATTACK_TYPE_HYBRID = 2
ATTACK_TYPES = [ATTACK_TYPE_PHYSICAL, ATTACK_TYPE_MAGICAL, ATTACK_TYPE_HYBRID]
ATTACK_TYPE_INDEX_TO_STRING = ['Phy. Atk.', 'Mag. Atk.', 'Hyb. Atk.']

# Target types
FOE = 0
SELF = 1
ALL_FOES = 2
ALL_ALLIES = 3
TARGET_INDEX_TO_STRING = ['Foe', 'Self', 'Foes', 'Allies']

# MODIFIERS
SINGLE_LOW = 0.5
SINGLE_MID = 0.7
SINGLE_HIGH = 0.9
SINGLE_SUPER = 1.1
SINGLE_ULTRA = 3.0

SINGLE_TEMP = 0.3
SINGLE_TEMP_SA = 0.4

SINGLE_MODS = [SINGLE_LOW, SINGLE_MID, SINGLE_HIGH, SINGLE_SUPER, SINGLE_ULTRA]

MULTI_LOW = 0.1
MULTI_MID = 0.15
MULTI_HIGH = 0.2
MULTI_SUPER = 0.4
MULTI_ULTRA = 2.6

MULTI_TEMP = 0.4
MULTI_TEMP_SA = 0.4

MULTI_MODS = [MULTI_LOW, MULTI_MID, MULTI_HIGH, MULTI_SUPER, MULTI_ULTRA]

MOD_LOW = 0
MOD_MID = 1
MOD_HIGH = 2
MOD_SUPER = 3
MOD_ULTRA = 4
MODIFIERS = [MOD_LOW, MOD_MID, MOD_HIGH, MOD_SUPER, MOD_ULTRA]
MOD_INDEX_TO_STRING = ['Low', 'Mid', 'High', 'Super', 'Ultra']

# Attack Speed
SPEED_SLOW = 0.5
SPEED_NORMAL = 1
SPEED_FAST = 1.5
SPEEDS = [SPEED_SLOW, SPEED_NORMAL, SPEED_FAST]
SPEED_INDEX_TO_STRING = ['Slow', '', 'Fast']

# Element Types
ELEMENT_NONE = 0
ELEMENT_WATER = 1
ELEMENT_FIRE = 2
ELEMENT_THUNDER = 3
ELEMENT_WIND = 4
ELEMENT_EARTH = 5
ELEMENT_LIGHT = 6
ELEMENT_DARK = 7
ELEMENTS = [ELEMENT_NONE, ELEMENT_WATER, ELEMENT_FIRE, ELEMENT_THUNDER, ELEMENT_WIND, ELEMENT_EARTH, ELEMENT_LIGHT, ELEMENT_DARK]
ELEMENT_INDEX_TO_STRING = ['None', 'Water', 'Fire', 'Thunder', 'Wind', 'Earth', 'Light', 'Dark']


class Skill:
    # Skills need
    # - A id
    # - A name
    # - An animation for the character
    #
    # - A current rank
    # - A usage count
    #
    # - An attack type
    # - A target
    # - A Modifier
    # - A Speed
    # - A element
    # - A mana cost
    # - A list of effects

    def __init__(self, skill_id, skill_name, animation_id, attack_type, target, modifier, speed, element, mana_cost, effects):
        self._id = skill_id
        self._name = skill_name
        self._animation_id = animation_id
        self._attack_type = attack_type
        self._target = target
        if self._target in [FOE, SELF]:
            self._modifier = SINGLE_MODS[modifier]
        else:
            self._modifier = MULTI_MODS[modifier]
        self._speed = SPEEDS[speed]
        self._element = element
        self._mana_cost = mana_cost
        self._effects = effects
        self._special = False

    def set_special(self):
        self._special = True

    def is_special(self):
        return self._special

    def get_name(self):
        if self._special:
            return f'Special: {self._name}'
        return self._name

    def get_attack_type(self):
        return self._attack_type

    def get_target(self):
        return self._target

    def get_speed(self):
        return self._speed

    def get_modifier(self):
        return self._modifier

    def get_mana_cost(self):
        return self._mana_cost

    def get_effects(self):
        return self._effects

    @staticmethod
    def boost(move_type, target_type):
        if move_type == ELEMENT_LIGHT and target_type == ELEMENT_DARK:
            return True
        if move_type == ELEMENT_DARK and target_type == ELEMENT_LIGHT:
            return True
        if move_type == ELEMENT_THUNDER and target_type == ELEMENT_WATER:
            return True
        if move_type == ELEMENT_WATER and target_type == ELEMENT_FIRE:
            return True
        if move_type == ELEMENT_FIRE and target_type == ELEMENT_WIND:
            return True
        if move_type == ELEMENT_WIND and target_type == ELEMENT_EARTH:
            return True
        if move_type == ELEMENT_EARTH and target_type == ELEMENT_THUNDER:
            return True
        return False

    def element_modifier(self, target):
        if self.boost(self._element, target.get_element()):
            return 1.5
        if self.boost(target.get_element(), self._element):
            return 0.5
        return 1
