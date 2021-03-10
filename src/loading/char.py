#Char block functions
from game.character import Character
from game.rank import Rank
from game.skill import Skill

CHAR_ATTACK_TYPE = 0
CHAR_TYPE = 1
CHAR_ELEMENT = 2
CHAR_HEALTH_BASE = 3
CHAR_MANA_BASE = 4
CHAR_STRENGTH_BASE = 5
CHAR_MAGIC_BASE = 6
CHAR_ENDURANCE_BASE = 7
CHAR_DEXTERITY_BASE = 8
CHAR_AGILITY_BASE = 9
CHAR_NAME = 10
CHAR_NICK_NAME = 11
CHAR_ID = 12
CHAR_SKEL_ID = 13

CHAR_BASE_MOVE = 14
CHAR_COUNTER_MOVE = 15
CHAR_BLOCK_MOVE = 16
CHAR_MOVE_1 = 17
CHAR_MOVE_2 = 18
CHAR_MOVE_3 = 19
CHAR_MOVE_SPECIAL = 20
CHAR_COMBO_AMOUNT = 21
CHAR_COMBO_START = 22

CHAR_UNLOCKED = 1
CHAR_LOCKED = 0


def load_char_chunk(line, loader, program_type, callbacks):
    if line[0] != '/':
        values = line.split(",", -1)
        for index in range(len(values)):
            values[index] = values[index].strip()

        try:
            ranks = Rank.load_ranks("../save/char_load_data/" + program_type + "/grids/" + values[CHAR_ID] + ".txt")
        except FileNotFoundError:
            ranks = Rank.load_ranks("../save/char_load_data/" + program_type + "/grids/base.txt")
        # ranks = [CHAR_UNLOCKED, CHAR_LOCKED, CHAR_LOCKED, CHAR_LOCKED, CHAR_LOCKED, CHAR_LOCKED, CHAR_LOCKED, CHAR_LOCKED, CHAR_LOCKED, CHAR_LOCKED]
        res_path = '../res/characters/' + values[CHAR_ID] + '/' + values[CHAR_ID]
        skel_path = '../res/characters/' + values[CHAR_ID] + '/' + values[CHAR_SKEL_ID] + '.skel'
        skills = []
        if values[CHAR_ATTACK_TYPE] == 'A':
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
                # skills[x] = loader.get('abilities')[skill]
        char = Character(values[CHAR_NAME], skel_path,
                           int(values[CHAR_HEALTH_BASE]), int(values[CHAR_MANA_BASE]), int(values[CHAR_STRENGTH_BASE]), int(values[CHAR_MAGIC_BASE]), int(values[CHAR_ENDURANCE_BASE]),
                           int(values[CHAR_STRENGTH_BASE]), int(values[CHAR_MAGIC_BASE]), int(values[CHAR_ENDURANCE_BASE]), int(values[CHAR_AGILITY_BASE]), int(values[CHAR_DEXTERITY_BASE]),
                           int(values[CHAR_ELEMENT]), skills, _display_name=values[CHAR_NICK_NAME], _index=len(loader.get('chars')), _is_support=values[CHAR_ATTACK_TYPE] == 'S', _ranks=ranks, _rank=1, _attack_type=int(values[CHAR_TYPE]),
                           _slide=res_path + '_slide.png', _slide_support=res_path + '_slide_support.png', _preview=res_path + '_preview.png', _full=res_path + '_full.png', _bust_up=res_path + '_bustup.png',
                           _character_id=values[CHAR_ID])
        loader.append('chars', values[CHAR_ID], char)
    for callback in callbacks:
        if callback is not None:
            callback()
