# Effect Types
from random import randint

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
HYBRID_ATTACK   = 36
DEFENSE         = 11

# Resists
PHYSICAL_RESIST = 12
MAGICAL_RESIST  = 13
HYBRID_RESIST   = 14
WATER_RESIST    = 15
FIRE_RESIST     = 16
THUNDER_RESIST  = 17
WIND_RESIST     = 18
EARTH_RESIST    = 19
LIGHT_RESIST    = 20
DARK_RESIST     = 21

# Chances
COUNTER_CHANCE     = 22
PENETRATION_CHANCE = 23
CRITICAL_CHANCE    = 24
BLOCK_CHANCE       = 25
EVADE_CHANCE       = 26

# STATUS EFFECT TYPES
POISON = 27
# Level 1 – Reduce 10% health every 10 seconds. Has a 50% chance to dissipate every 2 seconds after 2 afflictions.
# Level 2 – Reduce 15% health every 10 seconds. Has a 40% chance to dissipate every 2 seconds after 3 afflictions.
# Level 3 – Reduce 10% health every 5 seconds.  Has a 30% chance to dissipate every 3 seconds after 2 afflictions.
# Level 4 – Reduce 20% health every 4 seconds.  Has a 20% chance to dissipate every 3 seconds after 4 afflictions.

# Level 1 - Reduce 5% health every turn.    Has a 75% chance to dissipate every turn after 2 afflictions.
# Level 2 - Reduce 7.5% health every turn.  Has a 40% chance to dissipate every turn after 3 afflictions.
# Level 3 - Reduce 10% health every turn.   Has a 30% chance to dissipate every turn after 2 afflictions.
# Level 4 - Reduce 17.5% health every turn. Has a 20% chance to dissipate every turn after 4 afflictions.

SICKNESS = 28
# Level 1 – Reduce 10% health every 10 seconds. Str, Agi, Dex -10%. Has a 50% chance to dissipate every 2 seconds after 2 afflictions.
# Level 2 – Reduce 15% health every 10 seconds. Str, Agi, Dex -15%. Has a 40% chance to dissipate every 2 seconds after 3 afflictions.
# Level 3 – Reduce 10% health every 5 seconds.  Str, Agi, Dex -20%. Has a 30% chance to dissipate every 3 seconds after 2 afflictions.
# Level 4 – Reduce 20% health every 4 seconds.  Str, Agi, Dex -25%. Has a 20% chance to dissipate every 3 seconds after 4 afflictions.

# Level 1 - Reduce 5% health every turn.    Str, Agi, Dex -10%. Has a 75% chance to dissipate every turn after 2 afflictions.
# Level 2 - Reduce 7.5% health every turn.  Str, Agi, Dex -15%. Has a 40% chance to dissipate every turn after 3 afflictions.
# Level 3 - Reduce 10% health every turn.   Str, Agi, Dex -20%. Has a 30% chance to dissipate every turn after 2 afflictions.
# Level 4 - Reduce 17.5% health every turn. Str, Agi, Dex -25%. Has a 20% chance to dissipate every turn after 4 afflictions.

BLEED = 29
# Level 1 – Reduce 10% health every 10 seconds. Str -10% and Def -10%. Has a 50% chance to dissipate every 2 seconds after 2 afflictions.
# Level 2 – Reduce 15% health every 10 seconds. Str -10% and Def -15%. Has a 40% chance to dissipate every 2 seconds after 3 afflictions.
# Level 3 – Reduce 10% health every 5 seconds.  Str -15% and Def -20%. Has a 30% chance to dissipate every 3 seconds after 2 afflictions.
# Level 4 – Reduce 20% health every 4 seconds.  Str -20% and Def -20%. Has a 20% chance to dissipate every 3 seconds after 4 afflictions.

# Level 1 - Reduce 5% health every turn.    Str, Def -10%.         Has a 75% chance to dissipate every turn after 2 afflictions.
# Level 2 - Reduce 7.5% health every turn.  Str -10% and Def -15%. Has a 40% chance to dissipate every turn after 3 afflictions.
# Level 3 - Reduce 10% health every turn.   Str -15% and Def -20%. Has a 30% chance to dissipate every turn after 2 afflictions.
# Level 4 - Reduce 17.5% health every turn. Str, Def -20%.         Has a 20% chance to dissipate every turn after 4 afflictions.

STUN = 30
# Level 1 – Unable to use character for 5 seconds. Character takes 10% more damage while stunned. Character has a 15% reduction in counter and guard chances.
# Level 2 – Unable to use character for 10 seconds. Character takes 15% more damage while stunned. Character has a 15% reduction in counter and guard chances.
# Level 3 – Unable to use character for 10 seconds. Character takes 20% more damage while stunned. Character has a 15% reduction in counter and guard chances.
# Level 4 – Unable to use character for 20 seconds. Character takes 30% more damage while stunned. Character has a 20% reduction in counter and guard chances.
SLEEP = 31
# Level 1 – Unable to use character for 10 seconds. Character takes 25% more damage while asleep. Character is unable to guard or counter. Character has a 45% chance to be woken upon hit.
# Level 2 – Unable to use character for 15 seconds. Character takes 35% more damage while asleep. Character is unable to guard or counter. Character has a 35% chance to be woken upon hit.
# Level 3 – Unable to use character for 20 seconds. Character takes 45% more damage while asleep. Character is unable to guard or counter. Character has a 25% chance to be woken upon hit.
# Level 4 – Unable to use character for 30 seconds. Character takes 60% more damage while asleep. Character is unable to guard or counter. Character has a 15% chance to be woken upon hit.
SEAL = 32
# Level 1 – Character is unable to use skills for 10 seconds.
# Level 2 – Character is unable to use skills for 15 seconds. Character is unable to be healed or use any potions for 5 seconds.
# Level 3 – Character is unable to use skills for 20 seconds. Character is unable to be healed or use any potions for 10 seconds.
# Level 4 – Character is unable to use skills for 25 seconds. Character is unable to be healed or use any potions for 20 seconds. Character’s abilities are nulled for 15 seconds.
TAUNT = 33
# Level 1 – Character is unable to attack anyone except the targeted for 15 seconds. Character is unable to use special attack for 20 seconds. Character has a 20% chance to incur a level 1 stun after 15 seconds.
# Level 2 – Character is unable to attack anyone except the targeted for 20 seconds. Character is unable to use special attack for 20 seconds. Character has a 25% chance to incur a level 1 stun after 20 seconds.
# Level 3 – Character is unable to attack anyone except the targeted for 20 seconds. Character is unable to use special attack for 25 seconds. Character has a 20% chance to incur a level 2 stun after 20 seconds.
# Level 4 – Character is unable to attack anyone except the targeted for 25 seconds. Character is unable to use special attack for 30 seconds. Character has a 25% chance to incur a level 3 stun after 25 seconds.
CHARM = 34
# Level 1 – Character is unable to attack for 10 seconds.
# Level 2 – Character is unable to attack for 15 seconds. Character is only able to attack targeted until defeat or targeted is defeated.
# Level 3 – Character is unable to attack for 20 seconds. Character is only able to attack targeted until defeat or targeted is defeated.
# Level 4 – Character is unable to attack for 30 seconds.  For the next 30 seconds, the character will attack allies for 50% of normal strength. Character is only able to attack targeted until defeat or targeted is defeated.
SLOW = 35
# Level 1 – Character’s agility and dexterity are reduced by 10%. Character’s action time increased by 25%. Character has a 10% reduction in guard and counter chances.
# Level 2 – Character’s agility and dexterity are reduced by 15%. Character’s action time increased by 35%. Character has a 15% reduction in guard and counter chances.
# Level 3 – Character’s agility and dexterity are reduced by 20%. Character’s action time increased by 45%. Character has a 20% reduction in guard and counter chances.
# Level 4 – Character’s agility and dexterity are reduced by 30%. Character’s action time increased by 55%. Character has a 30% reduction in guard and counter chances.

CONDITION = 36

# STATUS EFFECT LEVELS
WEAK = 0
NORMAL = 1
STRONG = 2
DEVASTATING = 3

EFFECT_TYPES = {
    POISON: {
        WEAK: 'Weak Poison',
        NORMAL: 'Poison',
        STRONG: 'Strong Poison',
        DEVASTATING: 'Devastating Poison'
    },
    SICKNESS: {
        WEAK: 'Weak Sickness',
        NORMAL: 'Sickness',
        STRONG: 'Strong Sickness',
        DEVASTATING: 'Devastating Sickness'
    },
    BLEED: {
        WEAK: 'Weak Bleed',
        NORMAL: 'Bleed',
        STRONG: 'Strong Bleed',
        DEVASTATING: 'Devastating Bleed'
    },
    STUN: {
        WEAK: 'Weak Stun',
        NORMAL: 'Stun',
        STRONG: 'Strong Stun',
        DEVASTATING: 'Devastating Stun'
    },
    SLEEP: {
        WEAK: 'Weak Sleep',
        NORMAL: 'Sleep',
        STRONG: 'Strong Sleep',
        DEVASTATING: 'Devastating Sleep'
    },
    SEAL: {
        WEAK: 'Weak Seal',
        NORMAL: 'Seal',
        STRONG: 'Strong Seal',
        DEVASTATING: 'Devastating Seal'
    },
    TAUNT: {
        WEAK: 'Weak Taunt',
        NORMAL: 'Taunt',
        STRONG: 'Strong Taunt',
        DEVASTATING: 'Devastating Taunt'
    },
    CHARM: {
        WEAK: 'Weak Charm',
        NORMAL: 'Charm',
        STRONG: 'Strong Charm',
        DEVASTATING: 'Devastating Charm'
    },
    SLOW: {
        WEAK: 'Weak Slow',
        NORMAL: 'Slow',
        STRONG: 'Strong Slow',
        DEVASTATING: 'Devastating Slow'
    }
}

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
NULL_ATK     = 37
NULL_PHY_ATK = 38
NULL_MAG_ATK = 39
NULL_HYB_ATK = 40

COUNTER_TYPES = {
    NULL_ATK: 'Null Atk.',  # Implemented
    NULL_PHY_ATK: 'Null P. Atk.',  # Implemented
    NULL_MAG_ATK: 'Null M. Atk.',  # Implemented
    NULL_HYB_ATK: 'Null H. Atk.'  # Implemented
}

# Duration Types
SPECIAL_BLOCK = 41
HEAL_BLOCK    = 42
POTION_BLOCK  = 43
ATTACK_ALLY   = 44

DURATION_TYPES = {
    SPECIAL_BLOCK: 'Block Special',
    HEAL_BLOCK: 'Block Healing',
    POTION_BLOCK: 'Block Potions',
    ATTACK_ALLY: 'Attack Ally'
}

# Specific Target Types
SKILL_BLOCK = 0  # Counter is skill #


TYPES = {
    STAT: STAT_TYPES,
    COUNTER: COUNTER_TYPES,
    DURATION: DURATION_TYPES,
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

    def set_duration(self, condition):
        self._duration = condition

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
    def __init__(self, amount=0.0, duration=0):
        self._amount = amount
        self._duration = duration

        self._parent_name = None
        self._applied_name = None

    def set_info(self, parent, applied):
        self._parent_name = parent
        self._applied_name = applied

    def get_parent_name(self):
        return self._parent_name

    def get_applied_name(self):
        return self._applied_name

    def get_duration(self):
        return self._duration

    def get_amount(self):
        return self._amount

    def reduce_amount(self, delta):
        self._amount -= delta

    def reduce_duration(self, delta):
        self._duration -= delta

    # Return a dict with the effects
    def build(self, type):
        if type == POISON:
            if self.get_amount() == WEAK:
                return {HEALTH_DOT: AppliedEffect(0.05), CONDITION: Condition(Condition(None, RECURRING_CHANCE, 0.75, 1), AFFLICTIONS, 2)}
            elif self.get_amount() == NORMAL:
                return {HEALTH_DOT: AppliedEffect(0.075), CONDITION: Condition(Condition(None, RECURRING_CHANCE, 0.40, 1), AFFLICTIONS, 3)}
            elif self.get_amount() == STRONG:
                return {HEALTH_DOT: AppliedEffect(0.10), CONDITION: Condition(Condition(None, RECURRING_CHANCE, 0.30, 1), AFFLICTIONS, 2)}
            else:
                return {HEALTH_DOT: AppliedEffect(0.175), CONDITION: Condition(Condition(None, RECURRING_CHANCE, 0.20, 1), AFFLICTIONS, 4)}
        elif type == SICKNESS:
            if self.get_amount() == WEAK:
                return {HEALTH_DOT: AppliedEffect(0.05), STRENGTH: AppliedEffect(-0.10), AGILITY: AppliedEffect(-0.10),
                        DEXTERITY:  AppliedEffect(-0.10), CONDITION: Condition(Condition(None, RECURRING_CHANCE, 0.75, 1), AFFLICTIONS, 2)}
            elif self.get_amount() == NORMAL:
                return {HEALTH_DOT: AppliedEffect(0.075), STRENGTH: AppliedEffect(-0.15), AGILITY: AppliedEffect(-0.15),
                        DEXTERITY:  AppliedEffect(-0.15), CONDITION: Condition(Condition(None, RECURRING_CHANCE, 0.40, 1), AFFLICTIONS, 3)}
            elif self.get_amount() == STRONG:
                return {HEALTH_DOT: AppliedEffect(0.10), STRENGTH: AppliedEffect(-0.20), AGILITY: AppliedEffect(-0.20),
                        DEXTERITY:  AppliedEffect(-0.20), CONDITION: Condition(Condition(None, RECURRING_CHANCE, 0.30, 1), AFFLICTIONS, 2)}
            else:
                return {HEALTH_DOT: AppliedEffect(0.175), STRENGTH: AppliedEffect(-0.25), AGILITY: AppliedEffect(-0.25),
                        DEXTERITY:  AppliedEffect(-0.25), CONDITION: Condition(Condition(None, RECURRING_CHANCE, 0.20, 1), AFFLICTIONS, 4)}
        elif type == BLEED:
            if self.get_amount() == WEAK:
                return {HEALTH_DOT: AppliedEffect(0.05), STRENGTH: AppliedEffect(-0.10), DEFENSE: AppliedEffect(-0.10),
                        CONDITION: Condition(Condition(None, RECURRING_CHANCE, 0.75, 1), AFFLICTIONS, 2)}
            elif self.get_amount() == NORMAL:
                return {HEALTH_DOT: AppliedEffect(0.075), STRENGTH: AppliedEffect(-0.10), DEFENSE: AppliedEffect(-0.15),
                        CONDITION: Condition(Condition(None, RECURRING_CHANCE, 0.40, 1), AFFLICTIONS, 3)}
            elif self.get_amount() == STRONG:
                return {HEALTH_DOT: AppliedEffect(0.10), STRENGTH: AppliedEffect(-0.15), DEFENSE: AppliedEffect(-0.20),
                        CONDITION: Condition(Condition(None, RECURRING_CHANCE, 0.30, 1), AFFLICTIONS, 2)}
            else:
                return {HEALTH_DOT: AppliedEffect(0.175), STRENGTH: AppliedEffect(-0.20), DEFENSE: AppliedEffect(-0.20),
                        CONDITION: Condition(Condition(None, RECURRING_CHANCE, 0.20, 1), AFFLICTIONS, 4)}
        else:
            print('Unimplemented Status Effect')


# End Condition types
TIME_LENGTH      = 0  # After 6 seconds
# Length of time
AFFLICTIONS      = 1  # After 4 affects
# Number of afflictions
RECURRING_CHANCE = 2  # 20% after 4 seconds
# Chance
# Recurrence


class Condition:
    def __init__(self, child, type, *args):
        self._child = child
        self._type = type

        self._nums = list(args)
        if self._type == RECURRING_CHANCE:
            self._nums += [0]

    def __str__(self):
        if self._type == TIME_LENGTH:
            return f'Condition - {self._nums[0]} more turns'
        elif self._type == AFFLICTIONS:
            return f'Condition - {self._nums[0]} more afflictions'
        elif self._type == RECURRING_CHANCE:
            return f'Condition - {self._nums[1] - self._nums[2]} before {self._nums[0] * 100}% chance'

    def get_type(self):
        return self._type

    def get_child(self):
        return self._child

    def reduce(self):
        if self._type == TIME_LENGTH or self._type == AFFLICTIONS:
            self._nums[0] -= 1
            return self._nums[0] == 0
        if self._type == RECURRING_CHANCE:
            self._nums[2] += 1
            if self._nums[2] == self._nums[1]:
                self._nums[2] = 0
                return randint(1, 100) <= self._nums[0] * 100
            return False
