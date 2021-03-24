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


def load_char_chunk(line, loader, program_type, callbacks):
    if line[0] != '/':
        values = line.split(",", -1)
        for index in range(len(values)):
            values[index] = values[index].strip()

        path = resource_find('data/' + program_type + '/grids/' + values[CHAR_ID] + '.txt')
        if path:
            ranks = Rank.load_ranks(path)
        else:
            ranks = Rank.load_ranks(resource_find('data/' + program_type + '/grids/base.txt'))
        # ranks = [CHAR_UNLOCKED, CHAR_LOCKED, CHAR_LOCKED, CHAR_LOCKED, CHAR_LOCKED, CHAR_LOCKED, CHAR_LOCKED, CHAR_LOCKED, CHAR_LOCKED, CHAR_LOCKED]
        res_path = 'res/characters/' + values[CHAR_ID] + '/' + values[CHAR_ID]
        skel_path = 'res/characters/' + values[CHAR_ID] + '/' + values[CHAR_SKEL_ID] + '.skel'

        skills = []
        if values[CHAR_TYPE] == 'A':
            skills.append(int(values[CHAR_BASE_MOVE]))
            skills.append(int(values[CHAR_COUNTER_MOVE]))
            skills.append(int(values[CHAR_BLOCK_MOVE]))
            skills.append(int(values[CHAR_MOVE_1]))
            skills.append(int(values[CHAR_MOVE_2]))
            skills.append(int(values[CHAR_MOVE_3]))
            skills.append(int(values[CHAR_MOVE_SPECIAL]))
            for x in range(int(values[CHAR_COMBO_AMOUNT])):
                skills.append(int(values[CHAR_COMBO_START + x]))
            for x, skill in enumerate(skills):
                skills[x] = loader.get('skills')[skill]
        else:
            skills.append(int(values[CHAR_BASE_MOVE]))
            if not values[CHAR_COUNTER_MOVE] == '-':
                skills.append(int(values[CHAR_COUNTER_MOVE]))
            else:
                skills.append(None)
            if not values[CHAR_BLOCK_MOVE] == '-':
                skills.append(int(values[CHAR_BLOCK_MOVE]))
            else:
                skills.append(None)
            for x, skill in enumerate(skills):
                if skills[x] is None:
                    continue
        if str(len(loader.get('chars'))) in loader.get('save')['character_development']:
            character_development = loader.get('save')['character_development'][str(len(loader.get('chars')))]
        else:
            character_development = None
        char = Character(values[CHAR_NAME], skel_path,
                           int(values[CHAR_HEALTH_BASE]), int(values[CHAR_MANA_BASE]), int(values[CHAR_STRENGTH_BASE]), int(values[CHAR_MAGIC_BASE]), int(values[CHAR_ENDURANCE_BASE]),
                           int(values[CHAR_STRENGTH_BASE]), int(values[CHAR_MAGIC_BASE]), int(values[CHAR_ENDURANCE_BASE]), int(values[CHAR_AGILITY_BASE]), int(values[CHAR_DEXTERITY_BASE]),
                           int(values[CHAR_ELEMENT]), skills, _display_name=values[CHAR_NICK_NAME], _index=len(loader.get('chars')), _is_support=values[CHAR_ATTACK_TYPE] == 'S', _ranks=ranks, _rank=1, _attack_type=int(values[CHAR_TYPE]),
                           _slide=res_path + '_slide.png', _slide_support=res_path + '_slide_support.png', _preview=res_path + '_preview.png', _full=res_path + '_full.png', _bust_up=res_path + '_bustup.png',
                           _character_id=values[CHAR_ID])
        if character_development is not None:
            char.set_family(character_development['family'])
        loader.append('chars', values[CHAR_ID], char)
    for callback in callbacks:
        if callback is not None:
            callback()
