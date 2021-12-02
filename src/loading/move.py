from game.effect import COUNTER, DURATION, Effect, SPECIFIC_TARGET, STAT, STATUS_EFFECT, parse_effect
from game.skill import AILMENT_CURE, ATTACK, Boost, HEAL, NONE, NORMAL, Skill

ID          = 0
NAME        = 1
DESCRIPTION = 2
ANIM_ID     = 3
ANIM_NAME   = 4
TYPE        = 5
TARGET      = 6

ATTACK_SPEED = 7
ATTACK_POWER = 8
ATTACK_TYPE  = 9
ELEMENT      = 10


def load_skill_chunk(line, loader, program_type, callbacks):
    values = [x.strip() for x in line.split('*')]
    skill_id = int(values[ID])
    name = values[NAME]
    description = values[DESCRIPTION]
    anim_id = values[ANIM_ID]
    anim_name = values[ANIM_NAME]
    skill_type = int(values[TYPE])
    target = int(values[TARGET])

    attack_speed = NORMAL
    attack_power = None
    attack_type = None
    element = NONE

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
        effect, effect_index = parse_effect(effect_index, values)
        effects.append(effect)
    skill = Skill(skill_id, name, description, anim_id, anim_name, skill_type, target, attack_speed, attack_power, attack_type, element, boosts, effects)
    loader.append('skills', skill_id, skill)
    for callback in callbacks:
        if callback is not None:
            callback()
