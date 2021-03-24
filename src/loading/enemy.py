#Enenmy Chunk Functions
from game.enemy import Enemy
from game.skill import Skill

ENEMY_ID            = 0
ENEMY_NAME          = 1
ENEMY_SKEL_ID       = 2
ENEMY_ELEMENT       = 3
ENEMY_SUB_ELEMENT   = 4
ENEMY_ATTACK_TYPE   = 5
ENEMY_HEALTH_MIN    = 6
ENEMY_HEALTH_MAX    = 7
ENEMY_STRENGTH_MIN  = 8
ENEMY_STRENGTH_MAX  = 9
ENEMY_MAGIC_MIN     = 10
ENEMY_MAGIC_MAX     = 11
ENEMY_ENDURANCE_MIN = 12
ENEMY_ENDURANCE_MAX = 13
ENEMY_AGILITY_MIN   = 14
ENEMY_AGILITY_MAX   = 15
ENEMY_DEXTERITY_MIN = 16
ENEMY_DEXTERITY_MAX = 17

ENEMY_MOVE_SKILL_AMOUNT       = 18
ENEMY_BASIC_MOVE_ID           = 19
ENEMY_BASIC_MOVE_CHANCE       = 20
ENEMY_COUNTER_MOVE_ID         = 21
ENEMY_COUNTER_MOVE_CHANCE     = 22
ENEMY_BLOCK_MOVE_ID           = 23
ENEMY_BLOCK_MOVE_CHANCE       = 24
ENEMY_MOVE_SKILL_ID_START     = 25
ENEMY_MOVE_SKILL_CHANCE_START = 26


def get_skill_data(values, loader):
    skills = []
    skill_chances = []

    skills.append(int(values[ENEMY_BASIC_MOVE_ID]))
    skill_chances.append(float(values[ENEMY_BASIC_MOVE_CHANCE]))
    if values[ENEMY_COUNTER_MOVE_ID] == '-':
        skills.append(None)
        skill_chances.append(None)
    else:
        skills.append(int(values[ENEMY_COUNTER_MOVE_ID]))
        skill_chances.append(float(values[ENEMY_COUNTER_MOVE_CHANCE]))
    if values[ENEMY_BLOCK_MOVE_ID] == '-':
        skills.append(None)
        skill_chances.append(None)
    else:
        skills.append(int(values[ENEMY_BLOCK_MOVE_ID]))
        skill_chances.append(float(values[ENEMY_BLOCK_MOVE_CHANCE]))

    for x in range(int(values[ENEMY_MOVE_SKILL_AMOUNT])):
        skills.append(int(values[ENEMY_MOVE_SKILL_ID_START + (2 * x)]))
        skill_chances.append(float(values[ENEMY_MOVE_SKILL_CHANCE_START + (2 * x)]))
    for x, skill in enumerate(skills):
        if skill is None:
            continue
        skills[x] = loader.get('skills')[skill]
    return skills, skill_chances


def load_enemy_chunk(chunk, loader, program_type, callbacks):
    enemy_data, item_data = chunk.strip().split('\n')
    values = enemy_data.split(',')
    for x in range(len(values)):
        values[x] = values[x].strip()

    skills, skill_chances = get_skill_data(values, loader)
    for x in range(ENEMY_HEALTH_MIN, ENEMY_ENDURANCE_MAX+1):
        values[x] = int(values[x])

    drops = {'guaranteed': [], 'crystal': [], 'falna': [], 'drop': []}

    for drop_list in item_data.split(';'):
        if len(drop_list) == 0:
            continue
        key = list(drops.keys())[0]
        for drop in drop_list.split(','):
            item_id, rarity = drop.split('/')
            if rarity == '':
                drops[key] += item_id
            else:
                drops[key] += (item_id, int(rarity))

    min_smead = [int(values[ENEMY_HEALTH_MIN]), 0, int(values[ENEMY_STRENGTH_MIN]), int(values[ENEMY_MAGIC_MIN]), int(values[ENEMY_AGILITY_MIN]), int(values[ENEMY_DEXTERITY_MIN]), int(values[ENEMY_ENDURANCE_MIN])]
    max_smead = [int(values[ENEMY_HEALTH_MAX]), 0, int(values[ENEMY_STRENGTH_MAX]), int(values[ENEMY_MAGIC_MAX]), int(values[ENEMY_AGILITY_MAX]), int(values[ENEMY_DEXTERITY_MAX]), int(values[ENEMY_ENDURANCE_MAX])]
    elements = [values[ENEMY_ELEMENT], values[ENEMY_SUB_ELEMENT]]
    enemy = Enemy(values[ENEMY_ID], values[ENEMY_NAME], values[ENEMY_SKEL_ID], program_type, values[ENEMY_ATTACK_TYPE], min_smead, max_smead, elements, skills, skill_chances, drops)

    loader.append('enemies', values[ENEMY_ID], enemy)
    for callback in callbacks:
        if callback is not None:
            callback()
