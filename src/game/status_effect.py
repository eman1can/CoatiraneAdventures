# Status Effects
POISON = 0
STUN = 1
SLEEP = 2
SLOW = 3
TAUNT = 4
SEAL = 5
CHARM = 6
BLEED = 7
SICKNESS = 8

STATUS_EFFECTS = {POISON: 'Poison', STUN: 'Stun', SLEEP: 'Sleep', SLOW: 'Slow',
                  TAUNT: 'Taunt', SEAL: 'Seal', CHARM: 'Charm', BLEED: 'Bleed',
                  SICKNESS: 'Sickness'}

# Levels
WEAK   = 0
NORMAL = 1
STRONG = 2
ULTRA  = 3

LEVELS = {WEAK: 'Weak', NORMAL: '', STRONG: 'Strong', ULTRA: 'Ultra'}

LEVELS_TO_DURATION = {
    WEAK: 2,
    NORMAL: 4,
    STRONG: 5,
    ULTRA: 6
}

LEVELS_TO_AMOUNT = {
    WEAK: 0.2,
    NORMAL: 0.35,
    STRONG: 0.45,
    ULTRA: 0.6
}


class StatusEffect:
    def __init__(self, status_effect_type, level):
        self._type = status_effect_type
        self._level = level
