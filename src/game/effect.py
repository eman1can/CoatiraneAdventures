# Effect Types
from game.status_effect import StatusEffect

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
GUARD_CHANCE       = 21
COUNTER_CHANCE     = 22
PENETRATION_CHANCE = 23
CRITICAL_CHANCE    = 24
BLOCK_CHANCE       = 25
EVADE_CHANCE       = 26

STAT_TYPES = {
    STRENGTH: 'Str.',
    MAGIC: 'Mag.',
    ENDURANCE: 'End.',
    AGILITY: 'Agi.',
    DEXTERITY: 'Dex.',
    HEALTH_REGEN: 'HP Regen',
    HEALTH_DOT: 'HP DOT',
    MANA_REGEN: 'MP Regen',
    MANA_DOT: 'MP DOT',
    PHYSICAL_ATTACK: 'Phy. Atk.',
    MAGICAL_ATTACK: 'Mag. Atk.',
    DEFENSE: 'Def.',
    PHYSICAL_RESIST: 'Phy. Resist',
    MAGICAL_RESIST: 'Mag. Resist',
    HYBRID_RESIST: 'Hyb. Resist',
    WATER_RESIST: 'Water Resist',
    FIRE_RESIST: 'Fire Resist',
    THUNDER_RESIST: 'Thunder Resist',
    WIND_RESIST: 'Wind Resist',
    EARTH_RESIST: 'Earth Resist',
    LIGHT_RESIST: 'Light Resist',
    DARK_RESIST: 'Dark Resist',
    GUARD_CHANCE: 'Guard',
    COUNTER_CHANCE: 'Counter',
    PENETRATION_CHANCE: 'Penetration',
    CRITICAL_CHANCE: 'Critical',
    BLOCK_CHANCE: 'Block',
    EVADE_CHANCE: 'Evade'
}

# Counter Types
NULL_ATK     = 0
NULL_PHY_ATK = 1
NULL_MAG_ATK = 2
NULL_HYB_ATK = 3

COUNTER_TYPES = {
    NULL_ATK: 'Null Atk.',
    NULL_PHY_ATK: 'Null P. Atk.',
    NULL_MAG_ATK: 'Null M. Atk.',
    NULL_HYB_ATK: 'Null H. Atk.'
}

# Duration Types
SPECIAL_BLOCK = 0
HEAL_BLOCK    = 1
POTION_BLOCK  = 2
ATTACK_ALLY   = 3

# Specific Target Types
SKILL_BLOCK = 0  # Counter is skill #


TYPES = {
    STAT: STAT_TYPES,
    COUNTER: COUNTER_TYPES
}


class Effect:
    def __init__(self, effect_type, sub_type=None, target=None, amount=None, duration=None):
        self._type = effect_type
        self._sub_type = None

        self._target = None
        self._amount = None
        self._duration = None

    def is_stat_effect(self):
        return self._type == STAT

    def is_counter_effect(self):
        return self._type == COUNTER

    def is_duration_effect(self):
        return self._type == DURATION

    def is_status_effect_effect(self):
        return self._type == STATUS_EFFECT
