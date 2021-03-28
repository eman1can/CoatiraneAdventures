from refs import END_OPT_C, OPT_C, Refs
from text.screens.dungeon_battle import center

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
                if (index == 0 or party[index - 1]) and stat == 4:
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


def dungeon_main(console):
    console.header_callback = None
    if Refs.gc.get_floor_data() is None:
        display_text = f'\n\tFloor - Surface'
        display_text += '\n\tYou are currently at the surface of the dungeon. Who would you like to take with you?\n\n'
    else:
        display_text = f'\n\tFloor - {Refs.gc.get_floor_data().get_floor().get_id()}\n\n'

    # Display party
    party = Refs.gc.get_current_party()

    if console.memory.party_box is None:
        console.memory.party_box = create_box()

    display_text += box_to_string(console, populate_box(console.memory.party_box, party))
    display_text += '\n' + center(f'←──── {OPT_C}4{END_OPT_C} Prev Party | Next Party {OPT_C}5{END_OPT_C} ────→', 39, console.get_width())
    _options = {}
    if Refs.gc.get_floor_data() is None:
        display_text += f'\n\t{OPT_C}0:{END_OPT_C} back\n'
        _options['0'] = 'back'
    if Refs.gc.can_ascend():
        display_text += f'\n\t{OPT_C}1:{END_OPT_C} Ascend'
        _options['1'] = 'dungeon_confirm_up'
    if Refs.gc.can_descend():
        display_text += f'\n\t{OPT_C}2:{END_OPT_C} Descend'
        _options['2'] = 'dungeon_confirm_down'
    display_text += f'\n\t{OPT_C}3:{END_OPT_C} Inventory\n'

    _options['3'] = 'inventory*0'
    _options['4'] = 'dungeon_main_prev'
    _options['5'] = 'dungeon_main_next'

    index = 0
    char = party[index]
    while char is not None:
        _options[str(index + 6)] = f'dungeon_main_{index}_{char.get_id()}'
        index += 1
        char = party[index]
    _options[str(index + 6)] = f'dungeon_main_{index}_none'
    index += 1

    gap = 8 - index
    char = party[index + gap]
    while char is not None:
        _options[str(index + 6)] = f'dungeon_main_{index + gap}_{char.get_id()}'
        index += 1
        char = party[index + gap]
    if party[index + gap - 8]:
        _options[str(index + 6)] = f'dungeon_main_{index + gap}_none'

    return display_text, _options


def locked_dungeon_main(console):
    console.header_callback = None
    floor_data = Refs.gc.get_floor_data()
    if floor_data.get_floor().get_id() > floor_data.get_next_floor():
        # Ascending
        display_text = f'\n\tFloor - {floor_data.get_floor().get_id()}'
        display_text += f'\n\tYou have arrived at the staircase to the previous floor.\n\tWhat would you like to do?\n\n\t'
    else:
        # Descending
        if floor_data.have_beaten_boss():
            display_text = f'\n\tFloor - {floor_data.get_floor().get_id()}'
            display_text += f'\n\tYou have arrived at the staircase to the next floor.\n\tWhat would you like to do?\n\n\t'
        else:
            display_text = f'\n\tFloor - {floor_data.get_floor().get_id()} - BOSS'
            if floor_data.get_floor().get_boss_type() <= 2:
                display_text += f'\n\tYou have run into the boss of the floor!\n\tYou must fight to escape!\n\n\t'
            else:
                display_text += f'\n\tYou have run into the boss horde of the floor!\n\tYou must fight to escape!\n\n\t'
    _options = {}
    # Display party
    party = Refs.gc.get_current_party()

    display_text += '\t' + f'Party {Refs.gc.get_current_party_index() + 1}'.center(BOX_WIDTH * 8 + 10)
    if console.memory.party_box is None:
        console.memory.party_box = create_box()

    display_text += box_to_string(console, populate_box(console.memory.party_box, party))

    display_text += '\n\t'
    for _ in range(BOX_WIDTH * 4 - 14):
        display_text += ' '
    display_text += f'←──── [s]{OPT_C}5{END_OPT_C} Prev Party[/s] | [s]Next Party {OPT_C}6{END_OPT_C}[/s] ────→'

    if floor_data.get_floor().get_id() > floor_data.get_next_floor():
        # Ascending
        if Refs.gc.can_ascend():
            display_text += f'\n\t{OPT_C}0:{END_OPT_C} Go to previous floor.'
            _options['0'] = 'dungeon_battle'
        if Refs.gc.can_descend():
            display_text += f'\n\t{OPT_C}0:{END_OPT_C} Back to current floor.'
            _options['0'] = 'dungeon_confirm_down'
        display_text += f'\n\t{OPT_C}1:{END_OPT_C} Inventory\n'
        _options['1'] = 'inventory*0'
    else:
        # Descending
        if floor_data.have_beaten_boss():
            if Refs.gc.can_ascend():
                display_text += f'\n\t{OPT_C}0:{END_OPT_C} Back to current floor.'
                _options['0'] = 'dungeon_battle'
            if Refs.gc.can_descend():
                display_text += f'\n\t{OPT_C}0:{END_OPT_C} Descend to next floor.'
                _options['0'] = 'dungeon_confirm_down'
            display_text += f'\n\t{OPT_C}1:{END_OPT_C} Inventory\n'
            _options['1'] = 'inventory*0'
        else:
            display_text += f'\n\t{OPT_C}0:{END_OPT_C} Inventory\n'
            display_text += f'\n\t{OPT_C}1:{END_OPT_C} Fight\n'
            _options['0'] = 'inventory_battle*0'
            _options['1'] = 'dungeon_battle_fight_boss'
    for index, char in enumerate(party):
        if char is None:
            continue
        _options[str(index + 6)] = f'character_attribute_main_{char.get_id()}'
    return display_text, _options


def dungeon_main_confirm(console):
    count = 0
    for character in Refs.gc.get_current_party():
        if character is None:
            continue
        count += 1
    if count == 0:
        console.set_screen('dungeon_main')
        return

    descend = console._current_screen.endswith('down')
    display_text = f'\n\tThe recommended score for this floor is: {Refs.gc.get_floor_score(descend)}'
    display_text += f'\n\tYour party score is: {Refs.gc.get_current_party_score()}'
    display_text += f'\n\n\tWould you like to continue?\n\n\t{OPT_C}0:{END_OPT_C} No\n\t{OPT_C}1:{END_OPT_C} Yes\n'
    _options = {'0': 'back', '1': f'dungeon_battle_start_{descend}'}
    return display_text, _options
