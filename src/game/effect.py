# Effect Types

STAT            = 0
COUNTER         = 1
DURATION        = 2
SPECIFIC_TARGET = 3
STATUS_EFFECT   = 4

# STAT Boost Targets
# Basic HMPMD and SMEAD
STRENGTH        = 0
MAGIC           = 1
ENDURANCE       = 2
AGILITY         = 3
DEXTERITY       = 4
HEALTH_REGEN    = 5
HEALTH_DOT      = 6
MANA_REGEN      = 7
MANA_DOT        = 8
PHYSICAL_ATTACK = 9
MAGICAL_ATTACK  = 10
DEFENSE         = 11

# Resists
PHYSICAL_RESIST = 11
MAGICAL_RESIST  = 12
HYBRID_RESIST   = 13
WATER_RESIST    = 14
FIRE_RESIST     = 15
THUNDER_RESIST  = 16
WIND_RESIST     = 17
EARTH_RESIST    = 18
LIGHT_RESIST    = 19
DARK_RESIST     = 20

# Chances
COUNTER_CHANCE     = 21
PENETRATION_CHANCE = 22
CRITICAL_CHANCE    = 23
BLOCK_CHANCE       = 24
EVADE_CHANCE       = 25

# TODO SMEAD Grabbing Doesn't Affect HMPMD in battle entities
STAT_TYPES = {
    STRENGTH: 'Str.',  # Implemented
    MAGIC: 'Mag.',  # Implemented
    ENDURANCE: 'End.',  # Implemented
    AGILITY: 'Agi.',  # Implemented
    DEXTERITY: 'Dex.',  # Implemented
    HEALTH_REGEN: 'HP Regen',  # Implemented
    HEALTH_DOT: 'HP DOT',  # Implemented
    MANA_REGEN: 'MP Regen',  # Implemented
    MANA_DOT: 'MP DOT',  # Implemented
    PHYSICAL_ATTACK: 'Phy. Atk.',  # Implemented
    MAGICAL_ATTACK: 'Mag. Atk.',  # Implemented
    DEFENSE: 'Def.',  # Implemented
    PHYSICAL_RESIST: 'Phy. Resist',  # Implemented
    MAGICAL_RESIST: 'Mag. Resist',  # Implemented
    HYBRID_RESIST: 'Hyb. Resist',  # Implemented
    WATER_RESIST: 'Water Resist',  # Implemented
    FIRE_RESIST: 'Fire Resist',  # Implemented
    THUNDER_RESIST: 'Thunder Resist',  # Implemented
    WIND_RESIST: 'Wind Resist',  # Implemented
    EARTH_RESIST: 'Earth Resist',  # Implemented
    LIGHT_RESIST: 'Light Resist',  # Implemented
    DARK_RESIST: 'Dark Resist',  # Implemented
    COUNTER_CHANCE: 'Counter',  # Implemented
    PENETRATION_CHANCE: 'Penetration',  # Implemented
    CRITICAL_CHANCE: 'Critical',  # Implemented
    BLOCK_CHANCE: 'Block',  # Implemented
    EVADE_CHANCE: 'Evade'  # Implemented
}

# Counter Types
NULL_ATK     = 26
NULL_PHY_ATK = 27
NULL_MAG_ATK = 28
NULL_HYB_ATK = 29

COUNTER_TYPES = {
    NULL_ATK: 'Null Atk.',  # Implemented
    NULL_PHY_ATK: 'Null P. Atk.',  # Implemented
    NULL_MAG_ATK: 'Null M. Atk.',  # Implemented
    NULL_HYB_ATK: 'Null H. Atk.'  # Implemented
}

# Duration Types
SPECIAL_BLOCK = 30
HEAL_BLOCK    = 31
POTION_BLOCK  = 32
ATTACK_ALLY   = 33



# Specific Target Types
SKILL_BLOCK = 0  # Counter is skill #


TYPES = {
    STAT: STAT_TYPES,
    COUNTER: COUNTER_TYPES
}


class Effect:
    def __init__(self, effect_type, sub_type=None, target=None, amount=None, duration=None):
        self._type = effect_type
        self._sub_type = sub_type

        self._target = target
        self._amount = amount
        self._duration = duration

    def get_type(self):
        return self._type

    def get_sub_type(self):
        return self._sub_type

    def get_target(self):
        return self._target

    def get_amount(self):
        return self._amount

    def get_duration(self):
        return self._duration

    def is_stat_effect(self):
        return self._type == STAT

    def is_counter_effect(self):
        return self._type == COUNTER

    def is_duration_effect(self):
        return self._type == DURATION

    def is_status_effect_effect(self):
        return self._type == STATUS_EFFECT

    def __str__(self):
        return f'<{STAT_TYPES[self._sub_type]} {self._amount}% {self._duration} turns>'


class AppliedEffect:
    def __init__(self, amount=0, duration=-1):
        self._amount = amount
        self._duration = duration

    def get_duration(self):
        return self._duration

    def get_amount(self):
        return self._amount

    def reduce_amount(self, delta):
        self._amount -= delta

    def reduce_duration(self, delta):
        self._duration -= delta
