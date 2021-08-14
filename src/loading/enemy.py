#Enenmy Chunk Functions
from game.enemy import Enemy
from game.skill import Skill

ID            = 0
NAME          = 1
SKEL_ID       = 2
ELEMENT       = 3
SUB_ELEMENT   = 4
ATTACK_TYPE   = 5

HEALTH_MIN    = 6
HEALTH_MAX    = 7
STRENGTH_MIN  = 8
STRENGTH_MAX  = 9
MAGIC_MIN     = 10
MAGIC_MAX     = 11
ENDURANCE_MIN = 12
ENDURANCE_MAX = 13
AGILITY_MIN   = 14
AGILITY_MAX   = 15
DEXTERITY_MIN = 16
DEXTERITY_MAX = 17

SKILL_AMOUNT       = 18
BASIC_ID           = 19
BASIC_CHANCE       = 20
SKILL_ID_START     = 21
SKILL_CHANCE_START = 22
COUNTER_ID = -2
BLOCK_ID = -1


def get_skill_data(values, loader):
    skill_ids = []
    skill_chances = []

    skill_amount = int(values[SKILL_AMOUNT])
    for index in range(BASIC_ID, SKILL_ID_START + 2 * skill_amount):
        if index % 2 != 0:
            skill_ids.append(int(values[index]))
        else:
            skill_chances.append(float(values[index]))

    skill_ids.append(int(values[COUNTER_ID]))
    if values[BLOCK_ID] != '-':
        skill_ids.append(int(values[BLOCK_ID]))
    else:
        skill_ids.append(None)

    for x, skill_id in enumerate(skill_ids):
        if skill_id is None:
            continue
        skill_ids[x] = loader.get('skills')[skill_id]
    return skill_ids, skill_chances


def load_enemy_chunk(chunk, loader, program_type, callbacks):
    enemy_data, item_data = chunk.strip().split('\n')
    values = enemy_data.split(',')
    for x in range(len(values)):
        values[x] = values[x].strip()

    skills, skill_chances = get_skill_data(values, loader)

    drops = {'guaranteed': [], 'crystal': [], 'falna': [], 'drop': []}

    drop_lists = item_data.split(';')

    harvest_hardness = float(drop_lists[0])

    for index, drop_list in enumerate(drop_lists[1:]):
        if len(drop_list) == 0:
            continue
        key = list(drops.keys())[index]
        for drop in drop_list.split(','):
            item_id, rarity = drop.split('/')
            if rarity == '':  # Guaranteed
                drops[key].append(item_id)
            else:
                drops[key].append((item_id, int(rarity)))

    min_hsmead, max_hsmead = [], []
    for index in range(HEALTH_MIN, DEXTERITY_MAX + 1):
        if index % 2 == 0:
            min_hsmead.append(int(values[index]))
        else:
            max_hsmead.append(int(values[index]))

    elements = [int(values[ELEMENT]), int(values[SUB_ELEMENT])]
    enemy = Enemy(values[ID], values[NAME], values[SKEL_ID], program_type, values[ATTACK_TYPE], min_hsmead, max_hsmead, elements, harvest_hardness, skills, skill_chances, drops)

    loader.append('enemies', values[ID], enemy)
    for callback in callbacks:
        if callback is not None:
            callback()
