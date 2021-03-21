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
    number_of_monsters = int(data[FLOOR_ARRAY_NUM])
    monsters = data[FLOOR_ARRAY_NUM + 1:FLOOR_ARRAY_NUM + 1 + number_of_monsters]

    enemies = {}
    for enemy in monsters:
        enemy_id, rarity = enemy.split(',')
        enemies[enemy_id] = (loader.get('enemies')[enemy_id], int(rarity))

    if debug:
        print('Floor ID:', floor_id)
        print('Max Enemies:', max_enemies)
        print('Boss Type:', boss_type)
        print('Enemies:', enemies)

    resources = lines[1].split('; ')
    number_of_metals = int(resources[0])
    metal_data = resources[1:number_of_metals + 1]
    number_of_gems = int(resources[number_of_metals + 1])
    gem_data = resources[number_of_metals + 2: number_of_metals + 2 + number_of_gems]

    metals = {}
    gems = {}

    for metal in metal_data:
        name, hardness = metal.split(',')
        metals[name] = float(hardness)
    for gem in gem_data:
        name, hardness = gem.split(',')
        gems[name] = float(hardness)
    floor_data = load_dict(lines[2])
    path_data = load_array(lines[3])
    safe_zone_data = load_array(lines[4])

    floor_map = '\n'.join(lines[5:])

    if debug:
        print('Floor Data:', floor_data)
        print('Path Data:', path_data)
        print('Safe Zone Data:', safe_zone_data)
        print('Floor Map:\n' + floor_map)

    loader.append('floors', floor_id, Floor(floor_id, max_enemies, boss_type, enemies, metals, gems, floor_data, path_data, floor_map, safe_zone_data))
    for callback in callbacks:
        if callback is not None:
            callback()
