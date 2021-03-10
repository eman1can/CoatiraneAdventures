from game.effect import Effect
from game.skill import RANKS, Skill

LINE_TYPE = 0
TYPE_SKILL = 0
TYPE_ABILITY = 1
RANK_NUM = 12

#Skills
SKILL_ID = 1
SKILL_NAME = 2
SKILL_ANIM_ID = 3
SKILL_ATTACK_TYPE = 4
SKILL_TARGET = 5
SKILL_MODIFIER = 6
SKILL_SPEED = 7
SKILL_ELEMENT = 8
SKILL_MANA_COST = 9
SKILL_EFFECT_ARRAY_LENGTH = 10
SKILL_ARRAY = 11

#Abilities
ABILITY_ID = 1
ABILITY_NAME = 2
ABILITY_DESCRIPTION = 3
ABILITY_HAS_EFFECT = 4
ABILITY_EFFECT_ARRAY_LENGTH = 5

#Effects
EFFECT_TARGET_TYPE = 0
EFFECT_TYPE = 1
EFFECT_DURATION = 2
EFFECT_SUB_TYPE_LENGTH = 3
EFFECT_FIRST_SUB_TYPE = 4


def get_rank_array(debug, num, values, offset):
    rank_array = []
    for z in range(RANK_NUM):
        effect_array = []
        if debug:
            print("\t", RANKS[z], ": ")
        for x in range(num):
            effect = Effect()
            effect.target_type = int(values[offset + EFFECT_TARGET_TYPE].strip())
            if debug:
                print("\t\tTarget Type: ", effect.target_type)
            effect.type = int(values[offset + EFFECT_TYPE].strip())
            if debug:
                print("\t\tType: ", effect.type)
            if '-' not in values[offset + EFFECT_DURATION]:
                effect.duration = float(values[offset + EFFECT_DURATION]) / 5  # This is for turn based attack 5 secs = 1 turn
                if debug:
                    print("\t\tDuration: ", effect.duration)
            st_len = int(values[offset + EFFECT_SUB_TYPE_LENGTH].strip())
            if debug:
                print("\t\tSubType Length: ", st_len)
            for y in range(st_len):
                effect.st.append(float(values[offset + EFFECT_FIRST_SUB_TYPE + y]))
                if debug:
                    print("\t\tSt_", y + 1, ": ", effect.st[y])
            offset += EFFECT_FIRST_SUB_TYPE + st_len
            effect_array.append(effect)
        rank_array.append(effect_array)
    return rank_array


def load_move_chunk(line, loader, program_type, callbacks):
    debug = False
    if line[0] != '/':
        values = [x.strip() for x in line[:-1].split(",", -1)]
        if int(values[LINE_TYPE]) == TYPE_SKILL:
            if debug:
                print("Reading Skill: ")

            skill_id = int(values[SKILL_ID])
            if debug:
                print("\tId: ", skill_id)

            skill_name = str(values[SKILL_NAME])
            if debug:
                print("\tName: ", skill_name)

            skill_anim_id = str(values[SKILL_ANIM_ID])
            if debug:
                print("\tAnimation ID: ", skill_anim_id)

            skill_attack_type = int(values[SKILL_ATTACK_TYPE])
            if debug:
                print("\tAttack Type: ", skill_attack_type)

            skill_target = int(values[SKILL_TARGET])
            if debug:
                print("\tTarget: ", skill_target)

            skill_modifier = int(values[SKILL_MODIFIER])
            if debug:
                print("\tModifier: ", skill_modifier)

            skill_speed = int(values[SKILL_SPEED])
            if debug:
                print("\tSpeed: ", skill_speed)

            skill_element = int(values[SKILL_ELEMENT])
            if debug:
                print("\tElement: ", skill_element)

            skill_mana_cost = int(values[SKILL_MANA_COST])
            if debug:
                print("\tMana Cost: ", skill_mana_cost)

            effect_array_length = int(values[SKILL_EFFECT_ARRAY_LENGTH])
            skill_effects = None
            if effect_array_length > 0:
                if debug:
                    print("\tEffect: ")
                offset = SKILL_EFFECT_ARRAY_LENGTH + 1
                skill_effects = get_rank_array(debug, effect_array_length, values, offset)
            skill = Skill(skill_id, skill_name, skill_anim_id, skill_attack_type, skill_target, skill_modifier, skill_speed, skill_element, skill_mana_cost, skill_effects)
            loader.append('skills', int(values[SKILL_ID]), skill)
        # else:
        #     if debug:
        #         print("Reading Ability: ")
        #     ability = Ability()
        #     ability.id = int(values[ABILITY_ID])
        #     if debug:
        #         print("\tId: ", ability.id)
        #     ability.name = str(values[ABILITY_NAME])
        #     if debug:
        #         print("\tName: ", ability.name)
        #     ability.description = str(values[ABILITY_DESCRIPTION])
        #     if debug:
        #         print("\tDesc: ", ability.description)
        #     ability.has_effect = bool(int(values[ABILITY_HAS_EFFECT]))
        #     if ability.has_effect:
        #         if debug:
        #             print("\tEffect: ")
        #         offset = ABILITY_EFFECT_ARRAY_LENGTH + 1
        #         num = int(values[ABILITY_EFFECT_ARRAY_LENGTH])
        #         ability.effects = get_rank_array(debug, num, values, offset)
        #     loader.append('abilities', int(values[ABILITY_ID]), ability)
    for callback in callbacks:
        if callback is not None:
            callback()
