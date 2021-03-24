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
    def __init__(self, effect_type):
        self._type = effect_type
        self._sub_type = None

    def is_stat_effect(self):
        return False

    def is_counter_effect(self):
        return False

    def is_duration_effect(self):
        return False

    def is_status_effect_effect(self):
        return False


class StatEffect(Effect):
    def __init__(self, sub_type, target, amount, duration):
        super().__init__(STAT)
        self._sub_type = sub_type

        self._target = target
        self._amount = amount
        self._duration = duration

    def is_stat_effect(self):
        return True

    def get_target(self):
        return self._target

    def get_amount(self):
        return self._amount

    def get_duration(self):
        return self._duration

    def decrease_duration(self, delta=1):
        self._duration -= delta


class CounterEffect(Effect):
    def __init__(self, sub_type, count):
        super().__init__(COUNTER)
        self._sub_type = sub_type

        self._count = count

    def is_counter_effect(self):
        return True

    def get_count(self):
        return self._count

    def decrease_count(self, delta=1):
        self._count -= delta


class DurationEffect(Effect):
    def __init__(self, sub_type, duration):
        super().__init__(DURATION)
        self._sub_type = sub_type

        self._duration = duration

    def is_duration_effect(self):
        return True

    def get_duration(self):
        return self._duration

    def decrease_duration(self, delta=1):
        self._duration -= delta


class CauseStatusEffectEffect:
    def __init__(self, status_effect_id, status_effect_level, chance):
        super().__init__(STATUS_EFFECT)

        self._chance = chance
        self._id = status_effect_id
        self._level = status_effect_level

    def is_status_effect_effect(self):
        return True

    def get_status_effect(self):
        return StatusEffect(self._id, self._level)

    def get_chance(self):
        return self._chance