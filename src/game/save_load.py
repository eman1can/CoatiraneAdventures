from os import mkdir
from os.path import exists, expanduser
from random import randint
from shutil import rmtree
from time import strftime, localtime, time

from kivy.storage.jsonstore import JsonStore

from loading.config_loader import GAME_VERSION

SAVE_PATH = expanduser('~/Saved Games/Coatirane Adventures/saves/')
if not exists(expanduser('~/Saved Games/')):
    mkdir(expanduser('~/Saved Games/'))
if not exists(expanduser('~/Saved Games/Coatirane Adventures/')):
    mkdir(expanduser('~/Saved Games/Coatirane Adventures/'))
if not exists(expanduser('~/Saved Games/Coatirane Adventures/saves/')):
    mkdir(expanduser('~/Saved Games/Coatirane Adventures/saves/'))

SAVE_SLOT_1_PATH = f'{SAVE_PATH}/save1/'
SAVE_SLOT_2_PATH = f'{SAVE_PATH}/save2/'
SAVE_SLOT_3_PATH = f'{SAVE_PATH}/save3/'
SAVE_SLOT_1_INFO = f'{SAVE_SLOT_1_PATH}save_game_1_info.json'
SAVE_SLOT_1 = f'{SAVE_SLOT_1_PATH}save_game_1.dat'
SAVE_SLOT_2_INFO = f'{SAVE_SLOT_2_PATH}save_game_2_info.json'
SAVE_SLOT_2 = f'{SAVE_SLOT_2_PATH}save_game_2.dat'
SAVE_SLOT_3_INFO = f'{SAVE_SLOT_3_PATH}save_game_3_info.json'
SAVE_SLOT_3 = f'{SAVE_SLOT_3_PATH}save_game_3.dat'
FLOOR_DATA_SAVE_PATH = '/floor_data/'
SAVE_PATHS = [SAVE_SLOT_1_PATH, SAVE_SLOT_2_PATH, SAVE_SLOT_3_PATH]

SECONDS_IN_WEEK = 60 * 60 * 24 * 7

# uniform(1000000000, 9000000000)
VERSION_440856 = 8166431662
VERSION_2484264 = 2647992870
LATEST_VERSION = VERSION_2484264


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


def delete_save(save_slot):
    rmtree(SAVE_PATHS[save_slot - 1])


def create_new_save(save_slot, name, gender, symbol, domain, choice):
    save_info, save_path = get_info_and_path(save_slot)
    if not exists(SAVE_PATHS[save_slot - 1]):
        mkdir(SAVE_PATHS[save_slot - 1])

    starting_rank = 'I'
    starting_varenth = 3000
    starting_chars = 1
    starting_quests = 0
    starting_floor = 0
    starting_score = 0
    perks_unlocked = 0

    save_header(save_info, name, gender, domain, symbol, starting_rank, starting_varenth, starting_chars, starting_quests, starting_floor, starting_score, perks_unlocked)

    save_file = JsonStore(save_path)
    save_file['file_version'] = LATEST_VERSION
    save_file['family'] = {
        'name':   name,
        'gender': gender,
        'domain': domain,
        'symbol': symbol,
        'rank':   starting_rank,
        'rank_index': 0,
        'rank_points': 0,
        'chars':  starting_chars,
        'quests': starting_quests,
        'score':  starting_score
    }
    save_file['time'] = 824316914
    save_file['housing'] = {}
    save_file['housing']['id'] = 'two_room_flat'
    save_file['housing']['type'] = 'rent'
    save_file['housing']['installed_features'] = []
    save_file['housing']['bill_due'] = 824370914
    save_file['housing']['bill_count'] = 1
    save_file['lowest_floor'] = starting_floor

    save_file['obtained_characters'] = [choice]
    save_file['obtained_characters_a'] = [choice]
    save_file['obtained_characters_s'] = []

    starting_char_ids = ['a_whisper_of_wind_ais', 'hero_bell']
    chosen_char_id = starting_char_ids[choice]
    char_develop = {
        chosen_char_id: {
            'ranks':          {
                'unlocked': [True, False, False, False, False, False, False, False, False, False],
                'broken':   [False, False, False, False, False, False, False, False, False, False],
                'boards':   [
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
                'growth':   [[0 for _ in range(7)] for _ in range(10)]
            },
            'family':         name,
            'high_damage':    0,
            'floor_depth':    0,
            'monsters_slain': 0,
            'people_slain':   0,
            'equipment':      [None, None, None, None, None, None, None, None, None, None],
            'abilities':      [],
            'perks':      [],
            'familiarities':  {}
        }
    }
    save_file['character_development'] = char_develop
    save_file['inventory'] = {
        'current_pickaxe_hash':          None,
        'current_shovel_hash':           None,
        'current_harvesting_knife_hash': None
    }
    save_file['map_data'] = {}
    save_file['varenth'] = starting_varenth
    save_file['parties'] = [0] + [[-1 for _ in range(16)] for _ in range(10)]
    save_file['map_data'] = {}
    save_file['map_node_data'] = {}
    save_file['map_node_counters'] = {}
    save_file['boss_defeated'] = {}
    save_file['boss_respawn_time'] = {}
    for floor in range(1, 9):
        save_file['map_data'][str(floor)] = {}
        save_file['map_node_data'][str(floor)] = {}
        save_file['map_node_counters'][str(floor)] = {}
        save_file['boss_defeated'][str(floor)] = False
        save_file['boss_respawn_time'][str(floor)] = 0
    save_file['perk_points'] = 1
    save_file['perks'] = []
    save_file['crafting_queue'] = {
        'unassigned_chars': [choice],
        'queue': []
    }
    save_file['quest_data'] = {
        'timestamp':       973148400.0,
        'daily_quests':    [],
        'weekly_quests':   [],
        'monthly_quests':  [],
        'campaign_quests': []
    }


def save_header(info_slot, name, gender, domain, symbol, rank, varenth, chars_collected, quest_count, lowest_floor, total_score, perks_unlocked):
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
    info['skill_level'] = perks_unlocked


def migrate_save_version(current_version, save_file):
    if current_version == VERSION_440856:
        # VERSION_440856 → VERSION_2484264
        # This version added boss_defeated and boss_respawn_time
        save_file['boss_defeated'] = {}
        save_file['boss_respawn_time'] = {}
        for floor in range(1, 9):
            save_file['boss_defeated'][str(floor)] = False
            save_file['boss_respawn_time'][str(floor)] = 0
        save_file['file_version'] = VERSION_2484264
        return VERSION_2484264, save_file
    raise Exception(f'Unknown Save File Version. Cannot migrate!')


def save_game(save_slot, game_content):
    save_info, save_path = get_info_and_path(save_slot)

    if not exists(save_path):
        mkdir(save_path)

    name = game_content.get_name()
    gender = game_content.get_gender()
    domain = game_content.get_domain()
    symbol = game_content.get_symbol()
    rank = game_content.get_renown()
    rank_index = game_content.get_renown_as_index()
    rank_points = game_content.get_renown_points()
    varenth = game_content.get_varenth()
    char_count = len(game_content.get_all_obtained_character_indexes())
    quest_count = game_content.get_quests()
    lowest_floor = game_content.get_lowest_floor()
    score = game_content.get_score()
    perks_unlocked = game_content.get_skill_level()

    save_header(save_info, name, gender, domain, symbol, rank, varenth, char_count, quest_count, lowest_floor, score, perks_unlocked)

    save_file = JsonStore(save_path)

    if save_file['file_version'] != LATEST_VERSION:
        current_version = save_file['file_version']
        while current_version != LATEST_VERSION:
            current_version, save_file = migrate_save_version(current_version, save_file)

    save_file['family'] = {
        'name':        name,
        'gender':      gender,
        'domain':      domain,
        'symbol':      symbol,
        'rank':        rank,
        'rank_index':  rank_index,
        'rank_points': rank_points,
        'chars':       char_count,
        'quests':      quest_count,
        'score':       score
    }
    save_file['time'] = game_content.get_calendar().get_int_time()
    save_file['housing'] = {}
    housing = game_content.get_housing()
    save_file['housing']['id'] = housing.get_id()
    save_file['housing']['type'] = 'rent' if housing.is_renting() else 'buy'
    save_file['housing']['installed_features'] = housing.get_installed_features()
    save_file['housing']['bill_due'] = housing.get_bill_due_int_time()
    save_file['housing']['bill_count'] = housing.get_bill_count()
    if not housing.is_renting():
        save_file['housing']['bill_cost'] = housing.get_bill_cost(True)
    save_file['lowest_floor'] = lowest_floor
    save_file['obtained_characters'] = game_content.get_all_obtained_character_indexes()
    save_file['obtained_characters_a'] = game_content.get_obtained_character_indexes(False)
    save_file['obtained_characters_s'] = game_content.get_obtained_character_indexes(True)
    character_development = {}
    for character in game_content.get_all_obtained_characters():
        char_develop = {'ranks': {}, 'equipment': [], 'abilities': [], 'familiarities': {}}
        char_develop['ranks']['unlocked'] = [rank.is_unlocked() for rank in character.get_ranks()]
        char_develop['ranks']['broken'] = [rank.is_broken() for rank in character.get_ranks()]
        char_develop['ranks']['boards'] = [[rank.get_board().get_unlocked(tile) for tile in range(rank.get_board().get_count())] for rank in character.get_ranks()]
        char_develop['ranks']['growth'] = [rank.get_growth().get_stats() for rank in character.get_ranks()]
        char_develop['family'] = character.get_family()
        char_develop['high_damage'] = character.get_high_damage()
        char_develop['floor_depth'] = character.get_floor_depth()
        char_develop['monsters_slain'] = character.get_monsters_killed()
        char_develop['people_slain'] = character.get_people_killed()
        char_develop['familiarities'] = character.get_familiarities()
        equipment = []
        for item in character.get_outfit().items:
            if item is None:
                equipment.append(None)
            else:
                equipment.append(item.get_full_id())
        char_develop['equipment'] = equipment
        char_develop['abilities'] = character.get_all_abilities()
        char_develop['perks'] = character.get_all_perks()
        character_development[character.get_id()] = char_develop
    save_file['character_development'] = character_development

    save_file['inventory'] = game_content.get_inventory().get_save_output()
    save_file['map_data'] = {}
    save_file['map_node_data'] = {}
    save_file['map_node_counters'] = {}
    save_file['boss_defeated'] = {}
    save_file['boss_respawn_time'] = {}
    for floor in game_content['floors'].values():
        explored_array = {}
        for node, discovered in floor.get_map().get_explored().items():
            if discovered:
                explored_array[str(node)] = discovered
        save_file['map_data'][str(floor.get_id())] = explored_array

        explored_nodes, explored_node_counters = floor.get_map().get_node_exploration()
        explored_array = {}
        explored_counter_array = {}
        for node, discovered in explored_nodes.items():
            explored_array[str(node)] = discovered
            if not discovered:
                explored_counter_array[str(node)] = explored_node_counters[node]
        save_file['map_node_data'][str(floor.get_id())] = explored_array
        save_file['map_node_counters'][str(floor.get_id())] = explored_counter_array
        save_file['boss_defeated'][str(floor.get_id())] = floor.is_boss_defeated()
        save_file['boss_respawn_time'][str(floor.get_id())] = floor.boss_spawn_time()

    save_file['perk_points'] = game_content.get_perk_points()
    save_file['perks'] = game_content.get_unlocked_perks()

    save_file['varenth'] = varenth
    parties = [game_content.get_current_party_index()]
    for index in range(10):
        parties.append(game_content.get_party(index))
    save_file['parties'] = parties
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
    # - Quests
    save_file['quest_data'] = game_content.get_quest_manager().get_data_to_save()


def load_game(save_slot):
    save_info, save_path = get_info_and_path(save_slot)

    if not exists(save_info) or not exists(save_path):
        return None

    save_data = JsonStore(save_path)

    if save_data['file_version'] != LATEST_VERSION:
        current_version = save_data['file_version']
        while current_version != LATEST_VERSION:
            current_version, save_data = migrate_save_version(current_version, save_data)
    return save_data


def get_random_node(size):
    return randint(0, size - 1), randint(0, size - 1)


def get_arrays(json_data):
    node_data = {}
    for marker in json_data.store_keys():
        if marker == 'save_time':
            continue
        node_data[marker] = []
        for node in json_data.get(marker):
            node_data[marker].append(tuple(node))
    return node_data


def generate_data(file_path, floor):
    data = JsonStore(file_path)
    size = floor.get_map().get_size()

    node_amount = int(size * size / 20)

    generated_nodes = []
    # Blacklist entrance, exit and safe zones
    for marker_type, routes in floor.get_map().get_markers().items():
        if marker_type in ['exit', 'entrance', 'safe_zones']:
            generated_nodes += routes

    node_lists = {}
    # Generate nodes for every resource
    for resource in floor.get_resources().keys():
        node_lists[resource] = []
        for index in range(node_amount):
            node = get_random_node(size)
            while node in generated_nodes:
                node = get_random_node(size)
            generated_nodes.append(node)
            node_lists[resource].append(node)

    # Generate nodes for every enemy
    for enemy in floor.get_enemies().keys():
        node_lists[enemy] = []
        for index in range(node_amount):
            node = get_random_node(size)
            while node in generated_nodes:
                node = get_random_node(size)
            generated_nodes.append(node)
            node_lists[enemy].append(node)
    for node_type, node_list in node_lists.items():
        data[node_type] = node_list
    data['save_time'] = time()
    return get_arrays(data)


def load_floor_data(save_slot, floor):
    path = SAVE_PATHS[save_slot - 1] + FLOOR_DATA_SAVE_PATH
    if not exists(path):
        mkdir(path)
    file_path = path + str(floor.get_id()) + '.json'
    if not exists(file_path):
        return generate_data(file_path, floor), True
    else:
        data = JsonStore(file_path)
        if time() - data.get('save_time') > SECONDS_IN_WEEK:
            return generate_data(file_path, floor), True
        return get_arrays(data), False
