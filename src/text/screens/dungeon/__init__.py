from random import randint

from game.enemy import NICKNAMES
from refs import END_OPT_C, OPT_C, Refs
from text.screens.common_functions import center
from text.screens.screen_names import BACK, CHARACTER_SELECTION, DUNGEON_CONFIRM, DUNGEON_MAIN, INVENTORY

BOX_WIDTH = 17


def create_bar(left, right, middle, divider, size=8):
    string = ""
    for x in range(size):
        if x == 0:
            string += left
        else:
            string += middle
        for _ in range(BOX_WIDTH):
            string += divider
    return string + right


def get_fam_stat(character):
    total, gold, bonus, hint_text = Refs.gc.calculate_familiarity_bonus(character)
    left, right = f'{int(total)}R', f'G{int(gold)}'
    return left + f'{int(bonus)}%'.center(BOX_WIDTH - 2 - len(left) - len(right)) + right


def _get_stat_string(char, index, char2=None):
    stat = [lambda c=char: get_fam_stat(c), char.get_name, char.get_current_rank, char.get_attack_type_string, char.get_element_string, char.get_health, char.get_mana, char.get_physical_attack, char.get_magical_attack, char.get_defense, char.get_strength, char.get_magic,
            char.get_endurance, char.get_agility, char.get_dexterity]
    if index <= 4:
        return stat[index]()
    if char2 is None:
        return Refs.gc.format_number(int(stat[index]()))
    else:
        stat2 = [lambda c=char2: get_fam_stat(c), char2.get_name, char2.get_current_rank, char2.get_attack_type_string, char2.get_element_string, char2.get_health, char2.get_mana, char2.get_physical_attack, char2.get_magical_attack, char2.get_defense,
                char2.get_strength, char2.get_magic, char2.get_endurance, char2.get_agility, char2.get_dexterity]
        return Refs.gc.format_number(int(stat[index]()) + int(stat2[index]()))


def center_stat(index, char, char2=None):
    stat_labels = ['', '', 'Rank', '', '', 'HP', 'MP', 'P.Atk.', 'M.Atk.', 'Def.', 'Str.', 'Mag.', 'End.', 'Agi.', 'Dex.']

    if char2 is not None and index >= 4:
        stat_string = _get_stat_string(char, index, char2)
    else:
        stat_string = _get_stat_string(char, index)

    if index == 1:
        if ' ' in stat_string:
            stat_string = stat_string.split(' ')[0]
        return f'{stat_string}'.center(BOX_WIDTH)
    if index == 3 or index == 4:
        return f'{stat_string}'.center(BOX_WIDTH)
    return f"{stat_labels[index]}{f'{stat_string}'.rjust(BOX_WIDTH - 2 - len(stat_labels[index]))}".center(BOX_WIDTH)


def create_box():
    party = Refs.gc.get_current_party()
    if None in party[:8]:
        adventurers = party[:8].index(None)
    else:
        adventurers = 7

    box = [create_bar('┌', '┐', '┬', '─')]
    for stat in range(5):
        box.append('\n│')
        for _ in range(8):
            box.append('')
            box.append('│')
        box.append('')
    bar = '\n' + create_bar('├', '┤', '┼', '─', adventurers)
    for _ in range(8 - adventurers):
        bar += ''.center(BOX_WIDTH)
        bar += '│'
    box.append(bar)
    for stat in range(3):
        box.append('\n│')
        for _ in range(8):
            box.append('')
            box.append('│')
        box.append('')
    box.append('\n│')
    for index in range(adventurers):
        box.append(OPT_C + f'{6 + adventurers + index}'.center(BOX_WIDTH) + END_OPT_C)
        box.append('│')
    for _ in range(8 - adventurers):
        box.append(''.center(BOX_WIDTH))
        box.append('│')
    box.append('')

    bar = '\n' + create_bar('├', '┤', '┼', '─', adventurers)
    for _ in range(8 - adventurers):
        bar += ''.center(BOX_WIDTH)
        bar += '│'
    box.append(bar)
    for stat in range(10):
        box.append('\n│')
        for _ in range(8):
            box.append('')
            box.append('│')
        box.append('')
    box.append('\n│')
    for index in range(adventurers + 1):
        box.append(OPT_C + f'{6 + index}'.center(BOX_WIDTH) + END_OPT_C)
        box.append('│')
    for _ in range(7 - adventurers):
        box.append(''.center(BOX_WIDTH))
        box.append('│')
    box.append('')
    box.append('\n' + create_bar('└', '┘', '┴', '─'))
    return box


def populate_box(box, party, locked=False):
    if None in party[:8]:
        adventurers = party[:8].index(None)
    else:
        adventurers = 7

    for index, char in enumerate(party[:8]):
        top_index = (index + 1) * 2
        for stat in range(5):
            if char:
                box[top_index + stat * 18] = center_stat(stat, char)
            else:
                box[top_index + stat * 18] = ''.center(BOX_WIDTH)
        top_index = (index + 1) * 2 + 164
        for stat in range(5, 15):
            if char:
                box[top_index + (stat - 5) * 18] = center_stat(stat, char, party[index + 8])
            else:
                if (index == 0 or party[index - 1]) and stat == 5:
                    box[top_index + (stat - 5) * 18] = '+'.center(BOX_WIDTH)
                else:
                    box[top_index + (stat - 5) * 18] = ''.center(BOX_WIDTH)
        if (not locked and (index == 0 or party[index - 1])) or party[index]:
            box[top_index + 10 * 18] = OPT_C + f'{6 + index}'.center(BOX_WIDTH) + END_OPT_C
        else:
            box[top_index + 10 * 18] = ''.center(BOX_WIDTH)
    for index, char in enumerate(party[8:]):
        top_index = (index + 1) * 2 + 91
        for stat in range(3):
            if char and party[index]:
                box[top_index + stat * 18] = center_stat(stat, char)
            else:
                if party[0] and (index == 0 or party[index + 7]) and stat == 1 and party[index]:
                    box[top_index + stat * 18] = '+'.center(BOX_WIDTH)
                else:
                    box[top_index + stat * 18] = ''.center(BOX_WIDTH)
        if (not locked and ((party[0] and index == 0) or (party[index + 7] and party[index]))) or party[index]:
            box[top_index + 3 * 18] = OPT_C + f'{6 + adventurers + index + 1}'.center(BOX_WIDTH) + END_OPT_C
        else:
            box[top_index + 3 * 18] = ''.center(BOX_WIDTH)

    bar = '\n' + create_bar('├', '┤', '┼', '─', adventurers)
    for _ in range(8 - adventurers):
        bar += ''.center(BOX_WIDTH)
        bar += '│'

    box[164] = box[91] = bar
    return box


def box_to_string(console, box):
    string = ''
    for index in range(len(box)):
        string += box[index]
    box_width = string.index('\n', 1)
    return f'Party {Refs.gc.get_current_party_index() + 1}'.center(console.get_width()) + ('\n' + string).replace('\n', '\n'.center(console.get_width() - box_width))


def get_screen(console, screen_data):
    console.header_callback = None
    if Refs.gc.get_floor_data() is None:
        display_text = f'\n\tFloor - Surface'
        display_text += '\n\tYou are currently at the surface of the dungeon. Who would you like to take with you?\n\n'
    else:
        display_text = f'\n\tFloor - {Refs.gc.get_floor_data().get_floor().get_id()}\n\n'

    # Display party
    party = Refs.gc.get_current_party()

    if console.party_box is None:
        console.party_box = create_box()

    display_text += box_to_string(console, populate_box(console.party_box, party))
    display_text += '\n' + center(f'←──── {OPT_C}4{END_OPT_C} Prev Party | Next Party {OPT_C}5{END_OPT_C} ────→', 39, console.get_width())
    _options = {}
    if Refs.gc.get_floor_data() is None:
        display_text += f'\n\t{OPT_C}0:{END_OPT_C} back\n'
        _options['0'] = BACK
    if Refs.gc.can_ascend():
        display_text += f'\n\t{OPT_C}1:{END_OPT_C} Ascend'
        _options['1'] = f'{DUNGEON_CONFIRM}:up'
    if Refs.gc.can_descend():
        display_text += f'\n\t{OPT_C}2:{END_OPT_C} Descend'
        _options['2'] = f'{DUNGEON_CONFIRM}:down'
    display_text += f'\n\t{OPT_C}3:{END_OPT_C} Inventory\n'

    _options['3'] = f'{INVENTORY}:0'
    _options['4'] = f'prev'
    _options['5'] = f'next'

    index = 0
    char = party[index]
    while char is not None:
        _options[str(index + 6)] = f'{CHARACTER_SELECTION}:{index}#{char.get_id()}'
        index += 1
        char = party[index]
    _options[str(index + 6)] = f'{CHARACTER_SELECTION}:{index}#none'
    index += 1

    gap = 8 - index
    char = party[index + gap]
    while char is not None:
        _options[str(index + 6)] = f'{CHARACTER_SELECTION}:{index + gap}#{char.get_id()}'
        index += 1
        char = party[index + gap]
    if party[index + gap - 8]:
        _options[str(index + 6)] = f'{CHARACTER_SELECTION}:{index + gap}#none'
    _options['5683'] = 'run_simulation'
    return display_text, _options


def handle_action(console, action):
    if action in ['prev', 'next']:
        if action == 'prev':
            index = Refs.gc.get_current_party_index() - 1
        else:
            index = Refs.gc.get_current_party_index() + 1
        if index == 10:
            index = 0
        elif index == -1:
            index = 9
        Refs.gc.set_current_party_index(index)
        console.set_screen(DUNGEON_MAIN, False)
    elif action == 'run_simulation':
        run_simulation(1000)
    else:
        console.set_screen(action, True)


def run_simulation(count):
    N, S, E, W = 1, 2, 4, 8  # 0001 0010 0100 1000

    counters = {}

    for floor_index in range(60):
        print(floor_index)
        floor = Refs.gc['floors'][floor_index + 1]
        counters[floor_index] = {}

        for (enemy, rarity) in floor.get_enemies().values():
            counters[floor_index][enemy.get_name()] = {
                'Minimum Spawns': 0,
                'Maximum Spawns': 0,
                'Average Spawns': 0
            }

        counters[floor_index]['Minimum Movements'] = 0
        counters[floor_index]['Maximum Movements'] = 0
        counters[floor_index]['Average Movements'] = 0
        counters[floor_index]['Minimum Encounters'] = 0
        counters[floor_index]['Maximum Encounters'] = 0
        counters[floor_index]['Average Encounters'] = 0
        for (enemy, rarity) in floor.get_enemies().values():
            counters[floor_index][enemy.get_name()]['Minimum Spawns'] = 0
            counters[floor_index][enemy.get_name()]['Maximum Spawns'] = 0
            counters[floor_index][enemy.get_name()]['Average Spawns'] = 0
        run_drop_items = []
        for run in range(count):
            # Solve the path to the end
            nodes, start, end = floor.get_map().get_node_values()
            visited = {}

            for node in nodes.keys():
                visited[node] = False

            x, y = start
            visited[start] = True
            travelled = [(0, 0)]
            distance = 0
            encounters = 0
            spawns = {}
            drop_items = {}
            for (enemy, rarity) in floor.get_enemies().values():
                spawns[enemy.get_name()] = 0

            while (x, y) != end:
                options = []
                if (nodes[(x, y)] & N) == N and travelled[-1] != S and not visited[(x, y - 1)]:
                    options.append((0, -1))
                if (nodes[(x, y)] & E) == E and travelled[-1] != W and not visited[(x + 1, y)]:
                    options.append((1, 0))
                if (nodes[(x, y)] & S) == S and travelled[-1] != N and not visited[(x, y + 1)]:
                    options.append((0, 1))
                if (nodes[(x, y)] & W) == W and travelled[-1] != E and not visited[(x - 1, y)]:
                    options.append((-1, 0))

                # Simulate encounter
                if randint(1, 100) <= 15:
                    encounters += 1
                    enemies = floor.generate_enemies('none', 0)
                    for enemy in enemies:
                        name = enemy.get_name()
                        for nickname in NICKNAMES[1:]:
                            if name.startswith(nickname):
                                name = name[len(nickname):]
                                break
                        spawns[name] += 1
                        drops = Refs.gc['enemies'][enemy.get_id()].generate_drop(enemy.get_boost(), 17)
                        for (drop, drop_count) in drops:
                            if drop not in drop_items:
                                drop_items[drop] = 0
                            drop_items[drop] += drop_count

                if len(options) == 0:
                    dx, dy = travelled.pop()
                    x, y = x - dx, y - dy
                    distance += 1
                else:
                    dx, dy = options[randint(0, len(options) - 1)]
                    travelled.append((dx, dy))
                    x, y = x + dx, y + dy
                    visited[(x, y)] = True
                    distance += 1
            if counters[floor_index]['Minimum Movements'] == 0:
                counters[floor_index]['Minimum Movements'] = distance
            else:
                counters[floor_index]['Minimum Movements'] = min(distance, counters[floor_index]['Minimum Movements'])
            counters[floor_index]['Maximum Movements'] = max(distance, counters[floor_index]['Maximum Movements'])
            counters[floor_index]['Average Movements'] += distance
            if counters[floor_index]['Minimum Encounters'] == 0:
                counters[floor_index]['Minimum Encounters'] = encounters
            else:
                counters[floor_index]['Minimum Encounters'] = min(encounters, counters[floor_index]['Minimum Encounters'])
            counters[floor_index]['Maximum Encounters'] = max(encounters, counters[floor_index]['Maximum Encounters'])
            counters[floor_index]['Average Encounters'] += encounters
            for enemy, spawns in spawns.items():
                if counters[floor_index][enemy]['Minimum Spawns'] == 0:
                    counters[floor_index][enemy]['Minimum Spawns'] = spawns
                else:
                    counters[floor_index][enemy]['Minimum Spawns'] = min(spawns, counters[floor_index][enemy]['Minimum Spawns'])
                counters[floor_index][enemy]['Maximum Spawns'] = max(spawns, counters[floor_index][enemy]['Maximum Spawns'])
                counters[floor_index][enemy]['Average Spawns'] += spawns
            run_drop_items.append(drop_items)

        counters[floor_index]['Average Movements'] /= count
        counters[floor_index]['Average Encounters'] /= count
        for (enemy, rarity) in floor.get_enemies().values():
            counters[floor_index][enemy.get_name()]['Average Spawns'] /= count
        counters[floor_index]['Drop Items'] = run_drop_items
    file = open('Counters.txt', 'w', encoding='utf-8')
    file.write(str(counters))
    file.close()
