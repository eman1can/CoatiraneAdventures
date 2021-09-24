__all__ = ('Skill', 'AILMENT_CURE', 'ALLIES', 'ALLY', 'ATTACK', 'CAUSE_EFFECT', 'ELEMENTS', 'FOES', 'FOE', 'HEAL', 'MAGICAL', 'PHYSICAL', 'SELF', 'TEMP_BOOST_BY_TARGET')

# Skill Types
ATTACK       = 0
CAUSE_EFFECT = 1
HEAL         = 2
AILMENT_CURE = 3

SKILL_TYPES = {ATTACK: 'Attack', CAUSE_EFFECT: 'Cause Effect', HEAL: 'Heal', AILMENT_CURE: 'Ailment Cure'}

# Targets
FOE    = 0
FOES   = 1
SELF   = 2
ALLY   = 3
ALLIES = 4
TARGETS = {FOE: 'Foe', FOES: 'Foes', SELF: 'Self', ALLY: 'Ally', ALLIES: 'Allies'}

# Attack Speed
SLOW   = 0
NORMAL = 1
FAST   = 2
ATTACK_SPEEDS = {SLOW: 'Slow', NORMAL: '', FAST: 'Fast'}

ATTACK_SPEED_MODIFIER = {
    SLOW: 0.5,
    NORMAL: 1.0,
    FAST: 1.5
}

# Attack Power
LOW   = 0
MID   = 1
HIGH  = 2
SUPER = 3
ULTRA = 4
ATTACK_POWERS = {LOW: 'Low', MID: 'Mid', HIGH: 'High', SUPER: 'Super', ULTRA: 'Ultra'}

ATTACK_POWERS_EFFECT_BY_TARGET = {
    FOE: {
        LOW:   0.6,
        MID:   0.8,
        HIGH:  1.0,
        SUPER: 1.3,
        ULTRA: 3.0
    },
    ALLY: {
        LOW:   0.6,
        MID:   0.8,
        HIGH:  1.0,
        SUPER: 1.3,
        ULTRA: 3.0
    },
    SELF: {
        LOW:   0.6,
        MID:   0.8,
        HIGH:  1.0,
        SUPER: 1.3,
        ULTRA: 3.0
    },
    FOES: {
        LOW:   0.3,
        MID:   0.5,
        HIGH:  0.75,
        SUPER: 1.1,
        ULTRA: 2.5
    },
    ALLIES: {
        LOW:   0.3,
        MID:   0.5,
        HIGH:  0.75,
        SUPER: 1.1,
        ULTRA: 2.5
    }
}

# Skill Attack type
PHYSICAL = 0
MAGICAL  = 1
HYBRID   = 2
ATTACK_TYPES = {PHYSICAL: 'P.', MAGICAL: 'M.', HYBRID: 'H.'}

# Elements
NONE = 0
WATER = 1
FIRE = 2
THUNDER = 3
WIND = 4
EARTH = 5
LIGHT = 6
DARK = 7

WEAK = 0.5
NORMAL = 1.0
STRONG = 2.0

ELEMENTS = {NONE: '', WATER: 'Water', FIRE: 'Fire', THUNDER: 'Thunder', WIND: 'Wind', EARTH: 'Earth', LIGHT: 'Light', DARK: 'Dark'}

# Temporary Boost
BOOST       = 0
GREAT_BOOST = 1
BOOST_TYPES = {BOOST: 'Boost', GREAT_BOOST: 'Great Boost'}
TEMP_BOOST_BY_TARGET = {
    BOOST: {
        FOE: 0.4,
        ALLY: 0.4,
        SELF: 0.4,
        FOES: 0.3,
        ALLIES: 0.3
    },
    GREAT_BOOST: {
        FOE: 0.6,
        ALLY: 0.6,
        SELF: 0.7,
        FOES: 0.5,
        ALLIES: 0.5
    }
}


class Skill:
    def __init__(self, skill_id, name, description, animation_id, animation_name, skill_type, target, speed, power, attack_type, element, boosts, effect_list):
        self._id = skill_id
        self._name = name
        self._description = description
        self._animation_id = animation_id
        self._animation_name = animation_name

        self._type = skill_type
        self._target = target
        self._speed = speed
        self._power = power
        self._attack_type = attack_type
        self._element = element

        self._boosts = boosts
        self._effect_list = effect_list

        self._special = False

    # For character specific actions
    def set_special(self):
        self._special = True

    def is_special(self):
        return self._special

    def get_name(self):
        if self._special:
            return f'Special: {self._name}'
        return self._name

    def get_animation_path(self):
        return self._animation_id

    def get_animation_name(self):
        return self._animation_name

    def get_description(self):
        return self._description

    def get_id(self):
        return self._id

    def get_type(self):
        return self._type

    def get_attack_type(self):
        return self._attack_type

    def get_target(self):
        return self._target

    def get_speed(self):
        return ATTACK_SPEED_MODIFIER[self._speed]

    def get_power(self):
        return ATTACK_POWERS_EFFECT_BY_TARGET[self._target][self._power]

    def get_element(self):
        return self._element

    def get_effects(self):
        return self._effect_list

    def get_boosts(self):
        return self._boosts


class Boost:
    def __init__(self, type, stat_type):
        self._type = type
        self._stat_type = stat_type

    def get_type(self):
        return self._type

    def get_stat_type(self):
        return self._stat_type


def element_modifier(base_element, element):
    circle = {
        WATER: {
            FIRE: STRONG,
            THUNDER: WEAK
        },
        FIRE: {
            WIND: STRONG,
            WATER: WEAK
        },
        THUNDER: {
            WATER: STRONG,
            EARTH: WEAK
        },
        WIND: {
            EARTH: STRONG,
            FIRE: WEAK
        },
        EARTH: {
            THUNDER: STRONG,
            WIND: WEAK
        },
        LIGHT: {
            DARK: STRONG
        },
        DARK: {
            LIGHT: STRONG
        }
    }
    if element in circle:
        if base_element in circle[element]:
            return circle[element][base_element]
    return NORMAL
