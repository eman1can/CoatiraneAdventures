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


def _get_stat_string(char, index):
    stat = [lambda c=char: get_fam_stat(c), char.get_name, char.get_current_rank, char.get_attack_type_string, char.get_element_string, char.get_health, char.get_mana, char.get_physical_attack, char.get_magical_attack, char.get_defense, char.get_strength, char.get_magic,
            char.get_endurance, char.get_agility, char.get_dexterity]
    return stat[index]()


def center_stat(index, char, char2=None):
    stat_labels = ['', '', 'Rank', '', '', 'HP', 'MP', 'P.Atk.', 'M.Atk.', 'Def.', 'Str.', 'Mag.', 'End.', 'Agi.', 'Dex.']
    stat_string = _get_stat_string(char, index)
    if char2 is not None and index >= 4:
        stat_string += _get_stat_string(char, index)

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


def populate_box(box, party):
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
        if index == 0 or party[index - 1]:
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
        # box[top_index + 2 * 18] = ''.center(BOX_WIDTH)
        if party[0] and (index == 0 or party[index + 7]) and party[index]:
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
        console.set_screen(DUNGEON_MAIN)
    else:
        console.set_screen(action)
