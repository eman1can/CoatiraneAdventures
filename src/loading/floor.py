# Floor functions
from json import loads

from game.floor import Floor

FLOOR_ID = 0
FLOOR_MAX_ENEMIES = 1
FLOOR_BOSS_TYPE = 2
FLOOR_ARRAY_NUM = 3
FLOOR_END_OF_VALUES = 6
FLOOR_NUMBER_OF_VALUES = 2


def load_dict(string):
    out = {}
    if string == '{}':
        return out

    parts = string[2:-1].split(', (')
    for part in parts:
        key, value = part.split(': ')
        x, y = key[:-1].split(', ')
        out[(int(x), int(y))] = int(value)
    return out


def load_array(string):
    array = []
    print(string)
    if string == '[]':
        return array
    string = string[2:-1].replace('[', '(')
    string = string.replace(']', ')')
    tuples = string.split(', (')
    for tup in tuples:
        x, y = tup[:-1].split(', ')
        array.append((int(x), int(y)))
    return array


def load_floor_chunk(chunk, loader, program_type, callbacks):
    debug = False

    lines = chunk.split('\n')
    data = lines[0].split('; ')
    floor_id = int(data[FLOOR_ID])
    max_enemies = int(data[FLOOR_MAX_ENEMIES])
    boss_type = int(data[FLOOR_BOSS_TYPE])
    array_length = int(data[FLOOR_ARRAY_NUM])
    array = data[FLOOR_ARRAY_NUM + 1:FLOOR_ARRAY_NUM + 1 + array_length]
    enemies = []
    probabilities = {}
    for enemy in array:
        enemy_id, probability = enemy.split(',')
        enemies.append(loader.get('enemies')[enemy_id])
        probabilities[enemy_id] = float(probability)

    if debug:
        print('Floor ID:', floor_id)
        print('Max Enemies:', max_enemies)
        print('Boss Type:', boss_type)
        print('Enemy IDS:', enemies)
        print('Enemy Probabilities:', probabilities)

    floor_data = load_dict(lines[1])
    path_data = load_array(lines[2])
    safe_zone_data = load_array(lines[3])

    floor_map = '\n'.join(lines[4:])

    if debug:
        print('Floor Data:', floor_data)
        print('Path Data:', path_data)
        print('Safe Zone Data:', safe_zone_data)
        print('Floor Map:\n' + floor_map)

    loader.append('floors', floor_id, Floor(floor_id, max_enemies, boss_type, enemies, probabilities, floor_data, path_data, floor_map, safe_zone_data))
    for callback in callbacks:
        if callback is not None:
            callback()
