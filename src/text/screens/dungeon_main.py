from refs import END_OPT_C, OPT_C, Refs

BOX_WIDTH = 13


def create_bar(left, right, middle, divider):
    string = ""
    for x in range(8):
        if x == 0:
            string += left
        else:
            string += middle
        for _ in range(BOX_WIDTH):
            string += divider
    return string + right


def center_stat(char, index):
    if char is None:
        if index == 6:
            return '-'.center(BOX_WIDTH)
        return ''.center(BOX_WIDTH)
    stat = [char.get_name(), char.get_current_rank(), char.get_health(), char.get_mana(), char.get_physical_attack(), char.get_magical_attack(), char.get_defense(), char.get_strength(), char.get_magic(), char.get_endurance(),
            char.get_agility(), char.get_dexterity()]
    stat_labels = ['', 'Rank', 'HP', 'MP', 'P.Atk.', 'M.Atk.', 'Def.', 'Str.', 'Mag.', 'End.', 'Agi.', 'Dex.']
    if index == 0:
        if ' ' in stat[index]:
            stat[index] = stat[index].split(' ')[0]
        return f'{stat[index]}'.center(BOX_WIDTH)
    return f"{stat_labels[index]}{f'{stat[index]}'.rjust(BOX_WIDTH - 2 - len(stat_labels[index]))}".center(BOX_WIDTH)


def create_box():
    box = ['\n\t' + create_bar('┌', '┐', '┬', '─')]
    for stat in range(12):
        box.append('\n\t│')
        for _ in range(8):
            box.append('')
            box.append('│')
        box.append('\t')
    box.append('\n\t│')
    for index in range(8):
        # box.append(f'{7 + index}'.center(BOX_WIDTH))
        box.append(OPT_C + f'{7 + index}'.center(BOX_WIDTH) + END_OPT_C)
        box.append('│')
    box.append('\n\t' + create_bar('├', '┤', '┼', '─'))
    for stat in range(12):
        box.append('\n\t│')
        for _ in range(8):
            box.append('')
            box.append('│')
        box.append('\t')
    box.append('\n\t│')
    for index in range(8):
        box.append(OPT_C + f'{15 + index}'.center(BOX_WIDTH) + END_OPT_C)
        box.append('│')
    box.append('\n\t' + create_bar('└', '┘', '┴', '─'))
    return box


def populate_box(box, party):
    for index, char in enumerate(party[:8]):
        top_index = (index + 1) * 2
        for stat in range(12):
            string = ''.center(BOX_WIDTH)
            if char is None:
                if stat == 6:
                    string = '+'.center(BOX_WIDTH)
            else:
                string = center_stat(char, stat)
            box[top_index + stat * 18] = string
    for index, char in enumerate(party[8:]):
        top_index = (index + 1) * 2 + 234
        for stat in range(12):
            if char is None:
                string = ''.center(BOX_WIDTH)
                if stat == 6:
                    string = '+'.center(BOX_WIDTH)
            else:
                string = center_stat(char, stat)
            box[top_index + stat * 18] = string
    return box


def box_to_string(box):
    string = ""
    for index in range(len(box)):
        string += box[index]
    return string


def dungeon_main(console):
    display_text = f'\n\t{OPT_C}0:{END_OPT_C} back\n\n\tYou are currently at the surface of the dungeon.\n\tWho would you like to take with you?\n\n\t'
    _options = {'0': 'back'}
    # Display party
    party = Refs.gc.get_current_party()

    display_text += '\t' + f'Party {Refs.gc.get_current_party_index() + 1}'.center(BOX_WIDTH * 8 + 10)
    if console.memory.party_box is None:
        console.memory.party_box = create_box()

    display_text += box_to_string(populate_box(console.memory.party_box, party))

    display_text += '\n\t'
    for _ in range(BOX_WIDTH * 4 - 14):
        display_text += ' '
    display_text += f'←──── {OPT_C}5{END_OPT_C} Prev Party | Next Party {OPT_C}6{END_OPT_C} ────→'
    display_text += f'\n\t{OPT_C}1:{END_OPT_C} Ascend'
    if not Refs.gc.can_ascend():
        display_text += ' - Not Possible'
    display_text += f'\n\t{OPT_C}2:{END_OPT_C} Descend'
    if not Refs.gc.can_descend():
        display_text += ' - Not Possible'
    display_text += f'\n\t{OPT_C}3:{END_OPT_C} Inventory'
    display_text += f'\n\t{OPT_C}4:{END_OPT_C} Gear' + '\n'
    if Refs.gc.can_ascend():
        _options['1'] = 'dungeon_confirm_up'
    if Refs.gc.can_descend():
        _options['2'] = 'dungeon_confirm_down'
    _options['3'] = 'inventory0page'
    _options['4'] = 'gear_main'
    _options['5'] = 'dungeon_main_prev'
    _options['6'] = 'dungeon_main_next'
    for index, char in enumerate(party):
        if char is None:
            _options[str(index + 7)] = f'dungeon_main_{index}_none'
        else:
            _options[str(index + 7)] = f'dungeon_main_{index}_{char.get_id()}'
    return display_text, _options


def dungeon_main_confirm(console):
    descend = console._current_screen.endswith('down')
    display_text = f'\n\tThe recommended score for this floor is: {Refs.gc.get_floor_score(descend)}'
    display_text += f'\n\tYour party score is: {Refs.gc.get_current_party_score()}'
    display_text += f'\n\n\tWould you like to continue?\n\n\t{OPT_C}0:{END_OPT_C} No\n\t{OPT_C}1:{END_OPT_C} Yes\n'
    _options = {'0': 'back', '1': f'dungeon_battle_start_{descend}'}
    return display_text, _options
