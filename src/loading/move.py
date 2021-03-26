from game.effect import COUNTER, DURATION, Effect, SPECIFIC_TARGET, STAT, STATUS_EFFECT
from game.skill import AILMENT_CURE, ATTACK, Boost, HEAL, NORMAL, Skill

ID      = 0
NAME    = 1
ANIM_ID = 2
TYPE    = 3
TARGET  = 4

ATTACK_SPEED = 5
ATTACK_POWER = 6
ATTACK_TYPE  = 7
ELEMENT      = 8

BOOST_TYPE = 0
BOOST_STAT_TYPE = 1


def load_move_chunk(line, loader, program_type, callbacks):
    debug = False
    values = [x.strip() for x in line.split(',')]
    skill_id = int(values[ID])
    name = values[NAME]
    anim_id = values[ANIM_ID]
    skill_type = int(values[TYPE])
    target = int(values[TARGET])

    attack_speed = NORMAL
    attack_power = None
    attack_type = None
    element = None

    boost_index = TARGET + 1
    if skill_type == ATTACK:
        attack_speed = int(values[ATTACK_SPEED])
        attack_power = int(values[ATTACK_POWER])
        attack_type = int(values[ATTACK_TYPE])
        element = int(values[ELEMENT])
        boost_index = ELEMENT + 1
    elif skill_type == HEAL:
        attack_speed = int(values[ATTACK_SPEED])
        attack_power = int(values[ATTACK_POWER])
        boost_index = ATTACK_POWER + 1
    elif skill_type == AILMENT_CURE:
        attack_speed = int(values[ATTACK_SPEED])
        boost_index = ATTACK_SPEED + 1

    boost_count = int(values[boost_index])
    boosts = []
    for index in range(boost_count):
        boost_type = int(values[boost_index + index * 2 + 1])
        boost_stat_type = int(values[boost_index + index * 2 + 2])
        boosts.append(Boost(boost_type, boost_stat_type))

    effect_index = boost_index + 1 + boost_count * 2
    effect_count = int(values[effect_index])
    effects = []
    effect_index += 1
    for index in range(effect_count):
        effect_type = int(values[effect_index])
        effect_sub_type = None
        effect_target = None
        effect_amount = None
        effect_duration = None

        if effect_type == STAT:
            effect_sub_type = int(values[effect_index + 1])
            effect_target = int(values[effect_index + 2])
            effect_amount = int(values[effect_index + 3]) / 100
            effect_duration = int(values[effect_index + 4])
            effect_index += 5
        elif effect_type == COUNTER:
            effect_sub_type = int(values[effect_index + 1])
            effect_target = int(values[effect_index + 2])
            effect_amount = int(values[effect_index + 3])
            effect_index += 4
        elif effect_type == DURATION:
            effect_sub_type = int(values[effect_index + 1])
            effect_target = int(values[effect_index + 2])
            effect_duration = int(values[effect_index + 3])
            effect_index += 4
        elif effect_type == SPECIFIC_TARGET:
            pass
        elif effect_type == STATUS_EFFECT:
            effect_sub_type = int(values[effect_index + 1])
            effect_amount = int(values[effect_index + 2])
            effect_index += 3
        effects.append(Effect(effect_type, effect_sub_type, effect_target, effect_amount, effect_duration))
    skill = Skill(skill_id, name, anim_id, skill_type, target, attack_speed, attack_power, attack_type, element, boosts, effects)
    loader.append('skills', skill_id, skill)
    for callback in callbacks:
        if callback is not None:
            callback()
