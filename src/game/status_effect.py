
# Status Effects
POISON = 0
STUN = 1
SLEEP = 2
SLOW = 3
TAUNT = 4
SEAL = 5
CHARM = 6

# Affect Types
HEALTH = 0              # st_1 is the amount - Reduce health on EOT
MANA = 1                # st_1 is the amount - Reduce mana on EOT
STRENGTH = 2            #C st_1 is the amount - Strength changed during attack
MAGIC = 3               #C st_1 is the amount - Magic changed during attack
ENDURANCE = 4           #C st_1 is the amount - Endurance changed during damage
DEXTERITY = 5           #C st_1 is the amount - Dexterity changed during attack
AGILITY = 6             #C st_1 is the amount - Agility changed during attack
PHYSICAL_ATTACK = 7     #C st_1 is the amount - Phy Atk changed during attack
MAGICAL_ATTACK = 8      #C st_1 is the amount - Mag Atk changed during attack
DEFENSE = 9             #C st_1 is the amount - Defense changed during damage
DAMAGE = 10             #C st_1 is the amount - Damage changed during attack
PHYSICAL_RESIST = 11    #C st_1 is the amount
MAGICAL_RESIST = 12     #C st_1 is the amount
PHYSICAL_NULL = 13      #C st_1 is the chance
MAGICAL_NULL = 14       #C st_1 is the chance
ACTION_TIME = 15        # st_1 is the amount
GUARD_CHANCE = 16       #C st_1 is the amount - Guard chance changed during attack
COUNTER_CHANCE = 17     #C st_1 is the amount - Counter chance changed during attack
USAGE_BLOCK = 18        # Has no st's
SPECIAL_BLOCK = 19      # Has no st's
TARGET_FOCUS = 20       # Has no st's
CAUSE_EFFECT = 21       # st_1 is the SE type; st_2 is the st level; st_3 is the chance
HEAL_BLOCK = 22         # Has no st's
POTION_BLOCK = 23       # Has no st's
FOCUS_LOCK = 24         # Has no st's
TREASON = 25            # st_1 is the amount
DROP_RATE = 26          # st_1 is the amount
DROP_CHANCE = 27        # st_1 is the amount
SPAWN_RATE = 28         # st_1 is the amount
AVOID = 29              # st_1 is the SE type; st_2 is the st level; st_3 is the chance
PENETRATION = 30        #C st_1 is the amount
CRITICAL = 31           #C st_1 is the amount - Critical chance changed during attack
BLOCK_CHANCE = 32       #C st_1 is the amount - Block chance changed during attack
EVADE_CHANCE = 33       #C st_1 is the amount - Evade chance changed during attack
STATUS_EFFECT = 34      # Placeholder

# Poison Damage
DAMAGE_HEALTH = 35      # st_1 is the percent health damage, st_2 is the hurt interval, st_3 is the current hurt interval duration, st_4 is disapation chance, st_5 is disapation interval, st_6 is disapation current interval, st_7 is minimum affects
# Sleep wake up
CANCEL_CHANCE = 36
SKILL_BLOCK = 37
ABILITY_BLOCK = 38



class StatusEffect:
    def __init__(self, type=POISON, effects=None):
        self.type = type
        if effects is None:
            effects = {}
        self.effects = effects

    def get_description(self):
        return ''


def create_status_effect(type, level, target=None):
    if type == POISON:
        return create_poison(level)
    if type == STUN:
        return create_stun(level)
    if type == SLEEP:
        return create_sleep(level)
    if type == SLOW:
        return create_slow(level)
    if type == TAUNT:
        return create_taunt(level, target)
    if type == SEAL:
        return create_seal(level)
    if type == CHARM:
        return create_charm(level, target)


def create_poison(level):
    status_effect = StatusEffect(type=POISON)
    if level == 1:
        status_effect.effects[DAMAGE_HEALTH] = Effect(target_type=SELF, type=DAMAGE_HEALTH, st=[0.10, 2, 2, 0.50, 1, 1, 2])
    if level == 2:
        status_effect.effects[DAMAGE_HEALTH] = Effect(target_type=SELF, type=DAMAGE_HEALTH, st=[0.15, 2, 2, 0.40, 1, 1, 3])
    if level == 3:
        status_effect.effects[DAMAGE_HEALTH] = Effect(target_type=SELF, type=DAMAGE_HEALTH, st=[0.10, 1, 1, 0.30, 1, 1, 2])
    if level == 4:
        status_effect.effects[DAMAGE_HEALTH] = Effect(target_type=SELF, type=DAMAGE_HEALTH, st=[0.20, 1, 1, 0.20, 1, 1, 4])


def create_stun(level):
    status_effect = StatusEffect(type=STUN)
    if level == 1:
        status_effect.effects[USAGE_BLOCK] = Effect(target_type=SELF, type=USAGE_BLOCK, duration=int(5 / 5))
        status_effect.effects[DEFENSE] = Effect(target_type=SELF, type=DEFENSE, duration=int(5 / 5), st=[-0.10])
        status_effect.effects[COUNTER_CHANCE] = Effect(target_type=SELF, type=COUNTER_CHANCE, duration=int(5 / 5), st=[-0.15])
        status_effect.effects[GUARD_CHANCE] = Effect(target_type=SELF, type=GUARD_CHANCE, duration=int(5 / 5), st=[-0.15])
    if level == 2:
        status_effect.effects[USAGE_BLOCK] = Effect(target_type=SELF, type=USAGE_BLOCK, duration=int(10 / 5))
        status_effect.effects[DEFENSE] = Effect(target_type=SELF, type=DEFENSE, duration=int(10 / 5), st=[-0.15])
        status_effect.effects[COUNTER_CHANCE] = Effect(target_type=SELF, type=COUNTER_CHANCE, duration=int(10 / 5), st=[-0.15])
        status_effect.effects[GUARD_CHANCE] = Effect(target_type=SELF, type=GUARD_CHANCE, duration=int(10 / 5), st=[-0.15])
    if level == 3:
        status_effect.effects[USAGE_BLOCK] = Effect(target_type=SELF, type=USAGE_BLOCK, duration=int(10 / 5))
        status_effect.effects[DEFENSE] = Effect(target_type=SELF, type=DEFENSE, duration=int(10 / 5), st=[-0.20])
        status_effect.effects[COUNTER_CHANCE] = Effect(target_type=SELF, type=COUNTER_CHANCE, duration=int(10 / 5), st=[-0.15])
        status_effect.effects[GUARD_CHANCE] = Effect(target_type=SELF, type=GUARD_CHANCE, duration=int(10 / 5), st=[-0.15])
    if level == 4:
        status_effect.effects[USAGE_BLOCK] = Effect(target_type=SELF, type=USAGE_BLOCK, duration=int(20 / 5))
        status_effect.effects[DEFENSE] = Effect(target_type=SELF, type=DEFENSE, duration=int(20 / 5), st=[-0.30])
        status_effect.effects[COUNTER_CHANCE] = Effect(target_type=SELF, type=COUNTER_CHANCE, duration=int(20 / 5), st=[-0.20])
        status_effect.effects[GUARD_CHANCE] = Effect(target_type=SELF, type=GUARD_CHANCE, duration=int(20 / 5), st=[-0.20])


def create_sleep(level):
    status_effect = StatusEffect(type=SLEEP)
    if level == 1:
        status_effect.effects[USAGE_BLOCK] = Effect(target_type=SELF, type=USAGE_BLOCK, duration=int(10 / 5))
        status_effect.effects[DEFENSE] = Effect(target_type=SELF, type=DEFENSE, duration=int(10 / 5), st=[-0.25])
        status_effect.effects[COUNTER_CHANCE] = Effect(target_type=SELF, type=COUNTER_CHANCE, duration=int(10 / 5), st=[-1])
        status_effect.effects[GUARD_CHANCE] = Effect(target_type=SELF, type=GUARD_CHANCE, duration=int(10 / 5), st=[-1])
        status_effect.effects[CANCEL_CHANCE] = Effect(target_type=SELF, type=CANCEL_CHANCE, duration=int(10 / 5), st=[0.45])
    if level == 2:
        status_effect.effects[USAGE_BLOCK] = Effect(target_type=SELF, type=USAGE_BLOCK, duration=int(15 / 5))
        status_effect.effects[DEFENSE] = Effect(target_type=SELF, type=DEFENSE, duration=int(15 / 5), st=[-0.35])
        status_effect.effects[COUNTER_CHANCE] = Effect(target_type=SELF, type=COUNTER_CHANCE, duration=int(15 / 5), st=[-1])
        status_effect.effects[GUARD_CHANCE] = Effect(target_type=SELF, type=GUARD_CHANCE, duration=int(15 / 5), st=[-1])
        status_effect.effects[CANCEL_CHANCE] = Effect(target_type=SELF, type=CANCEL_CHANCE, duration=int(15 / 5), st=[0.35])
    if level == 3:
        status_effect.effects[USAGE_BLOCK] = Effect(target_type=SELF, type=USAGE_BLOCK, duration=int(20 / 5))
        status_effect.effects[DEFENSE] = Effect(target_type=SELF, type=DEFENSE, duration=int(20 / 5), st=[-0.45])
        status_effect.effects[COUNTER_CHANCE] = Effect(target_type=SELF, type=COUNTER_CHANCE, duration=int(20 / 5), st=[-1])
        status_effect.effects[GUARD_CHANCE] = Effect(target_type=SELF, type=GUARD_CHANCE, duration=int(20 / 5), st=[-1])
        status_effect.effects[CANCEL_CHANCE] = Effect(target_type=SELF, type=CANCEL_CHANCE, duration=int(20 / 5), st=[0.25])
    if level == 4:
        status_effect.effects[USAGE_BLOCK] = Effect(target_type=SELF, type=USAGE_BLOCK, duration=int(30 / 5))
        status_effect.effects[DEFENSE] = Effect(target_type=SELF, type=DEFENSE, duration=int(30 / 5), st=[-0.60])
        status_effect.effects[COUNTER_CHANCE] = Effect(target_type=SELF, type=COUNTER_CHANCE, duration=int(30 / 5), st=[-1])
        status_effect.effects[GUARD_CHANCE] = Effect(target_type=SELF, type=GUARD_CHANCE, duration=int(30 / 5), st=[-1])
        status_effect.effects[CANCEL_CHANCE] = Effect(target_type=SELF, type=CANCEL_CHANCE, duration=int(30 / 5), st=[0.15])


def create_slow(level):
    status_effect = StatusEffect(type=SLOW)
    if level == 1:
        status_effect.effects[AGILITY] = Effect(target_type=SELF, type=AGILITY, duration=int(10 / 5), st=[-0.10])
        status_effect.effects[DEXTERITY] = Effect(target_type=SELF, type=DEXTERITY, duration=int(10 / 5), st=[-0.10])
        status_effect.effects[ACTION_TIME] = Effect(target_type=SELF, type=ACTION_TIME, duration=int(10 / 5), st=[0.25])
        status_effect.effects[COUNTER_CHANCE] = Effect(target_type=SELF, type=COUNTER_CHANCE, duration=int(10 / 5), st=[-0.10])
        status_effect.effects[GUARD_CHANCE] = Effect(target_type=SELF, type=GUARD_CHANCE, duration=int(10 / 5), st=[-0.10])
    if level == 2:
        status_effect.effects[AGILITY] = Effect(target_type=SELF, type=AGILITY, duration=int(15 / 5), st=[-0.15])
        status_effect.effects[DEXTERITY] = Effect(target_type=SELF, type=DEXTERITY, duration=int(15 / 5), st=[-0.15])
        status_effect.effects[ACTION_TIME] = Effect(target_type=SELF, type=ACTION_TIME, duration=int(15 / 5), st=[0.35])
        status_effect.effects[COUNTER_CHANCE] = Effect(target_type=SELF, type=COUNTER_CHANCE, duration=int(15 / 5), st=[-0.15])
        status_effect.effects[GUARD_CHANCE] = Effect(target_type=SELF, type=GUARD_CHANCE, duration=int(15 / 5), st=[-0.15])
    if level == 3:
        status_effect.effects[AGILITY] = Effect(target_type=SELF, type=AGILITY, duration=int(20 / 5), st=[-0.20])
        status_effect.effects[DEXTERITY] = Effect(target_type=SELF, type=DEXTERITY, duration=int(20 / 5), st=[-0.20])
        status_effect.effects[ACTION_TIME] = Effect(target_type=SELF, type=ACTION_TIME, duration=int(20 / 5), st=[0.45])
        status_effect.effects[COUNTER_CHANCE] = Effect(target_type=SELF, type=COUNTER_CHANCE, duration=int(20 / 5), st=[-0.20])
        status_effect.effects[GUARD_CHANCE] = Effect(target_type=SELF, type=GUARD_CHANCE, duration=int(20 / 5), st=[-0.20])
    if level == 4:
        status_effect.effects[AGILITY] = Effect(target_type=SELF, type=AGILITY, duration=int(30 / 5), st=[-0.30])
        status_effect.effects[DEXTERITY] = Effect(target_type=SELF, type=DEXTERITY, duration=int(30 / 5), st=[-0.30])
        status_effect.effects[ACTION_TIME] = Effect(target_type=SELF, type=ACTION_TIME, duration=int(30 / 5), st=[0.55])
        status_effect.effects[COUNTER_CHANCE] = Effect(target_type=SELF, type=COUNTER_CHANCE, duration=int(30 / 5), st=[-0.30])
        status_effect.effects[GUARD_CHANCE] = Effect(target_type=SELF, type=GUARD_CHANCE, duration=int(30 / 5), st=[-0.30])


def create_taunt(level, target):
    status_effect = StatusEffect(type=TAUNT)
    if level == 1:
        status_effect.effects[TARGET_FOCUS] = Effect(target_type=SELF, type=TARGET_FOCUS, duration=int(15 / 5), st=[target])
        status_effect.effects[SPECIAL_BLOCK] = Effect(target_type=SELF, type=SPECIAL_BLOCK, duration=int(20 / 5))
        status_effect.effects[CAUSE_EFFECT] = Effect(target_type=SELF, type=CAUSE_EFFECT, duration=int(15 / 5), st=[STUN, 1, 0.20])
    if level == 2:
        status_effect.effects[TARGET_FOCUS] = Effect(target_type=SELF, type=TARGET_FOCUS, duration=int(20 / 5), st=[target])
        status_effect.effects[SPECIAL_BLOCK] = Effect(target_type=SELF, type=SPECIAL_BLOCK, duration=int(20 / 5))
        status_effect.effects[CAUSE_EFFECT] = Effect(target_type=SELF, type=CAUSE_EFFECT, duration=int(20 / 5), st=[STUN, 1, 0.25])
    if level == 3:
        status_effect.effects[TARGET_FOCUS] = Effect(target_type=SELF, type=TARGET_FOCUS, duration=int(20 / 5), st=[target])
        status_effect.effects[SPECIAL_BLOCK] = Effect(target_type=SELF, type=SPECIAL_BLOCK, duration=int(25 / 5))
        status_effect.effects[CAUSE_EFFECT] = Effect(target_type=SELF, type=CAUSE_EFFECT, duration=int(20 / 5), st=[STUN, 2, 0.20])
    if level == 4:
        status_effect.effects[TARGET_FOCUS] = Effect(target_type=SELF, type=TARGET_FOCUS, duration=int(25 / 5), st=[target])
        status_effect.effects[SPECIAL_BLOCK] = Effect(target_type=SELF, type=SPECIAL_BLOCK, duration=int(30 / 5))
        status_effect.effects[CAUSE_EFFECT] = Effect(target_type=SELF, type=CAUSE_EFFECT, duration=int(25 / 5), st=[STUN, 3, 0.25])


def create_seal(level):
    status_effect = StatusEffect(type=TAUNT)
    if level == 1:
        status_effect.effects[SKILL_BLOCK] = Effect(target_type=SELF, type=SKILL_BLOCK, duration=int(10 / 5))
    if level == 2:
        status_effect.effects[SKILL_BLOCK] = Effect(target_type=SELF, type=SKILL_BLOCK, duration=int(15 / 5))
        status_effect.effects[HEAL_BLOCK] = Effect(target_type=SELF, type=HEAL_BLOCK, duration=int(5 / 5))
        status_effect.effects[POTION_BLOCK] = Effect(target_type=SELF, type=POTION_BLOCK, duration=int(5 / 5))
    if level == 3:
        status_effect.effects[SKILL_BLOCK] = Effect(target_type=SELF, type=SKILL_BLOCK, duration=int(20 / 5))
        status_effect.effects[HEAL_BLOCK] = Effect(target_type=SELF, type=HEAL_BLOCK, duration=int(10 / 5))
        status_effect.effects[POTION_BLOCK] = Effect(target_type=SELF, type=POTION_BLOCK, duration=int(10 / 5))
    if level == 4:
        status_effect.effects[SKILL_BLOCK] = Effect(target_type=SELF, type=SKILL_BLOCK, duration=int(25 / 5))
        status_effect.effects[HEAL_BLOCK] = Effect(target_type=SELF, type=HEAL_BLOCK, duration=int(20 / 5))
        status_effect.effects[POTION_BLOCK] = Effect(target_type=SELF, type=POTION_BLOCK, duration=int(20 / 5))
        status_effect.effects[ABILITY_BLOCK] = Effect(target_type=SELF, type=ABILITY_BLOCK, duration=int(15 / 5))


def create_charm(level, target):
    status_effect = StatusEffect(type=CHARM)
    if level == 1:
        status_effect.effects[SKILL_BLOCK] = Effect(target_type=SELF, type=SKILL_BLOCK, duration=int(10 / 5))
    if level == 2:
        status_effect.effects[SKILL_BLOCK] = Effect(target_type=SELF, type=SKILL_BLOCK, duration=int(15 / 5))
        status_effect.effects[TARGET_FOCUS] = Effect(target_type=SELF, type=TARGET_FOCUS, st=[target])
    if level == 3:
        status_effect.effects[SKILL_BLOCK] = Effect(target_type=SELF, type=SKILL_BLOCK, duration=int(20 / 5))
        status_effect.effects[TARGET_FOCUS] = Effect(target_type=SELF, type=TARGET_FOCUS, st=[target])
    if level == 2:
        status_effect.effects[SKILL_BLOCK] = Effect(target_type=SELF, type=SKILL_BLOCK, duration=int(30 / 5))
        status_effect.effects[TREASON] = Effect(target_type=SELF, type=TREASON, duration=int(30 / 5), st=[ALL_ALLIES, 0.50])
        status_effect.effects[TARGET_FOCUS] = Effect(target_type=SELF, type=TARGET_FOCUS, st=[target])
