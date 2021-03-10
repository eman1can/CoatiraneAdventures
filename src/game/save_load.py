from os.path import exists
from time import strftime, localtime, time

from kivy.storage.jsonstore import JsonStore

from loading.config_loader import GAME_VERSION
from game.skill import RANKS

SAVE_PATH = '../save/saves/'
SAVE_SLOT_1_INFO = f'{SAVE_PATH}save_game_1_info.json'
SAVE_SLOT_1 = f'{SAVE_PATH}save_game_1.dat'
SAVE_SLOT_2_INFO = f'{SAVE_PATH}save_game_2_info.json'
SAVE_SLOT_2 = f'{SAVE_PATH}save_game_2.dat'
SAVE_SLOT_3_INFO = f'{SAVE_PATH}save_game_3_info.json'
SAVE_SLOT_3 = f'{SAVE_PATH}save_game_3.dat'


def get_info_and_path(save_slot):
    if save_slot == 1:
        return SAVE_SLOT_1_INFO, SAVE_SLOT_1
    elif save_slot == 2:
        return SAVE_SLOT_2_INFO, SAVE_SLOT_2
    else:
        return SAVE_SLOT_3_INFO, SAVE_SLOT_3


def load_save_info(save_slot):
    save_info, save_path = get_info_and_path(save_slot)
    if exists(save_info):
        return JsonStore(save_info)
    return None


def create_new_save(save_slot, name, gender, symbol, domain, choice):
    save_info, save_path = get_info_and_path(save_slot)

    starting_rank = RANKS[0]
    starting_varenth = 3000
    starting_chars = 1
    starting_quests = 0
    starting_floor = 0
    starting_score = 0
    starting_skills = 0

    save_header(save_info, name, gender, domain, symbol, starting_rank, starting_varenth, starting_chars, starting_quests, starting_floor, starting_score, starting_skills)

    save_file = JsonStore(save_path)
    save_file['family'] = {
        'name': name,
        'gender': gender,
        'domain': domain,
        'symbol': symbol,
        'rank': starting_rank,
        'chars': starting_chars,
        'quests': starting_quests,
        'score': starting_score,
        'skills': starting_skills
    }
    save_file['lowest_floor'] = starting_floor
    save_file['obtained_characters'] = [choice]
    save_file['obtained_characters_a'] = [choice]
    save_file['obtained_characters_s'] = []
    save_file['character_development'] = {
        f'{choice}': {
            'ranks': {
                'unlocked': [True, False, False, False, False, False, False, False, False, False],
                'broken': [False, False, False, False, False, False, False, False, False, False],
                'boards': [
                    [False for _ in range(9)],
                    [False for _ in range(9)],
                    [False for _ in range(16)],
                    [False for _ in range(16)],
                    [False for _ in range(25)],
                    [False for _ in range(25)],
                    [False for _ in range(36)],
                    [False for _ in range(36)],
                    [False for _ in range(42)],
                    [False for _ in range(42)],
                ],
                'growth': [[0 for _ in range(7)] for _ in range(10)]
            },
            'equipment': [],
            'abilities': [],
            'familiarities': []
        }
    }
    save_file['equipment'] = []
    save_file['inventory'] = {}
    save_file['map_data'] = {}
    save_file['varenth'] = starting_varenth
    save_file['parties'] = [[None for _ in range(16)] for _ in range(10)]

    # - Obtained Characters (all, s, & a)
    # - Character Rank Info and Growth, Grid Progress
    # - Character Abilities & Skills
    # - Character Familiarity Info
    # - Character Stats
    # - Character Equipped Items
    # - Character
    # - Equipment
    # - Inventory/Items/Money
    # - Family Info
    # - Family Stats
    # - Any Floor Info (Not yet a thing)
    # - Family Skill Tree - Not yet a thing


def save_header(info_slot, name, gender, domain, symbol, rank, varenth, chars_collected, quest_count, lowest_floor, total_score, skill_level):
    info = JsonStore(info_slot)
    info['game_version'] = GAME_VERSION
    info['last_save_time'] = strftime('%d/%m/%y %I:%M %p', localtime(time()))
    info['save_name'] = name
    info['gender'] = gender
    info['domain'] = domain
    info['symbol'] = symbol
    info['rank'] = rank
    info['varenth'] = varenth
    info['chars_collected'] = chars_collected
    info['quests'] = quest_count
    info['lowest_floor'] = lowest_floor
    info['total_character_score'] = total_score
    info['skill_level'] = skill_level


def save_game():
    pass
    # Save the info to the disk
    # Save the actual game info to the disk
    # - Obtained Characters (all, s, & a)
    # - Character Rank Info, Grid Progress
    # - Character Abilities & Skills
    # - Character Familiarity Info
    # - Character Stats
    # - Character Equipped Items
    # - Character
    # - Equipment
    # - Inventory/Items/Money
    # - Family Info
    # - Family Stats
    # - Any Floor Info (Not yet a thing)
    # - Family Skill Tree - Not yet a thing


def load_game(save_slot):
    save_info, save_path = get_info_and_path(save_slot)

    if not exists(save_info) or not exists(save_path):
        return None

    return JsonStore(save_path)
