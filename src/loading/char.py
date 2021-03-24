#Char block functions
from game.character import Character
from game.rank import Rank
from game.skill import Skill
from kivy.resources import resource_find

TYPE           = 0
ID             = 1
NAME           = 2
DISPLAY_NAME   = 3
SKEL_ID        = 4
RACE           = 5
GENDER         = 6
AGE            = 7

ATTACK_TYPE     = 8
ELEMENT         = 9
WEAPON_TYPE     = 10
SUB_WEAPON_TYPE = 11
HEALTH          = 12
MANA            = 13
STRENGTH        = 14
MAGIC           = 15
ENDURANCE       = 16
AGILITY         = 17
DEXTERITY       = 18

BASE_MOVE        = 19
MOVE_1           = 20
MOVE_1_MANA_COST = 21
MOVE_2           = 22
MOVE_2_MANA_COST = 23
MOVE_3           = 24
MOVE_3_MANA_COST = 25
MOVE_SPECIAL     = 26
COUNTER_MOVE     = 27
BLOCK_MOVE       = 28
COMBO_AMOUNT     = 29
COMBO_START      = 30

EFFECT_1 = 17
EFFECT_2 = 18
EFFECT_3 = 19
EFFECT_4 = 20
EFFECT_5 = 21

RECRUITMENT_ITEM = -3
RECRUITMENT_ITEM_COUNT = -2
DESCRIPTION = -1


def get_skills(loader, values):
    skills = []
    if values[TYPE] == 'A':
        skills.append(int(values[BASE_MOVE]))
        skills.append(int(values[MOVE_1]))
        skills.append(int(values[MOVE_1_MANA_COST]))
        skills.append(int(values[MOVE_2]))
        skills.append(int(values[MOVE_2_MANA_COST]))
        skills.append(int(values[MOVE_3]))
        skills.append(int(values[MOVE_3_MANA_COST]))
        skills.append(int(values[MOVE_SPECIAL]))
        skills.append(int(values[COUNTER_MOVE]))
        skills.append(int(values[BLOCK_MOVE]))
        for x in range(int(values[COMBO_AMOUNT])):
            skills.append(int(values[COMBO_START + x]))
        for x, skill in enumerate(skills):
            skills[x] = loader.get('skills')[skill]
    else:
        skills.append(int(values[EFFECT_1]))
        skills.append(int(values[EFFECT_2]))
        skills.append(int(values[EFFECT_3]))
        skills.append(int(values[EFFECT_4]))
        skills.append(int(values[EFFECT_5]))
        for x, skill in enumerate(skills):
            skills[x] = loader.get('skills')[skill]
    return skills


def load_char_chunk(line, loader, program_type, callbacks):
    if line[0] != '/':
        values = line.split(",", -1)
        for index in range(len(values)):
            values[index] = values[index].strip()

        res_path = 'res/characters/' + values[ID] + '/' + values[ID]
        skel_path = 'res/characters/' + values[ID] + '/' + values[SKEL_ID] + '.skel'

        skills = get_skills(loader, values)

        character_development = None
        if str(len(loader.get('chars'))) in loader.get('save')['character_development']:
            character_development = loader.get('save')['character_development'][str(len(loader.get('chars')))]

        path = resource_find('data/' + program_type + '/grids/' + values[ID] + '.txt')
        if path:
            ranks = Rank.load_ranks(path, character_development)
        else:
            ranks = Rank.load_ranks(resource_find('data/' + program_type + '/grids/base.txt'), character_development)
        # TODO - Add rank loading from save/load

        char_id, name, display_name, skel_id = values[ID:SKEL_ID + 1]
        race = int(values[RACE])
        gender = int(values[GENDER])
        age = int(values[AGE])  # TODO: Adjust age based on played game time
        description = values[DESCRIPTION]

        hp, mp, s, m, e, a, d = values[HEALTH:DEXTERITY + 1]

        element = 0
        attack_type = None
        favorite_weapon = None
        favorite_sub_weapon = None
        if values[TYPE] == 'A':
            attack_type = int(values[ATTACK_TYPE])
            element = int(values[ELEMENT])

            favorite_weapon = int(values[WEAPON_TYPE])
            if values[SUB_WEAPON_TYPE] != '-':
                favorite_sub_weapon = int(values[SUB_WEAPON_TYPE])

        recruitment_items = {}
        for index in range(int(values[RECRUITMENT_ITEM_COUNT])):
            item_id, count = values[RECRUITMENT_ITEM - index].split('#')
            recruitment_items[loader.get('items')[item_id]] = count

        is_support = values[TYPE] == 'S'
        full, slide, preview, slide_support, bustup = f'{res_path}_full.png', f'{res_path}_slide.png', f'{res_path}_preview.png', f'{res_path}_slide_support.png', f'{res_path}_bustup.png'

        rank = 0
        for rank_status in character_development['unlocked']:
            if rank_status:
                rank += 1

        # TODO Add unlocked perks/abilities to save/load and character_development
        # TODO Add equiped items to save/load and character_development

        family, high_damage, floor_depth, monsters_slain, people_slain = character_development['family'], character_development['high_damage'], character_development['floor_depth'], character_development['monsters_slain'], character_development['people_slain']

        char = Character(name, skel_path, int(hp), int(mp), int(s), int(m), int(e), int(a), int(d), element, skills,
                         _race=race, _gender=gender, _age=age, _description=description,
                         _familiarities=character_development['familiarities'],
                         _character_id=char_id, _display_name=display_name, _index=len(loader.get('chars')), _is_support=is_support, _ranks=ranks, _rank=rank, _attack_type=attack_type,
                         _slide=slide, _slide_support=slide_support, _preview=preview, _full=full, _bust_up=bustup,
                         _family=family, _high_damage=high_damage, _floor_depth=floor_depth, _monsters_slain=monsters_slain, _people_slain=people_slain,
                         _recruitment_items=recruitment_items, _favorite_weapon=favorite_weapon, _favorite_sub_weapon=favorite_sub_weapon)

        loader.append('chars', char_id, char)
    for callback in callbacks:
        if callback is not None:
            callback()
