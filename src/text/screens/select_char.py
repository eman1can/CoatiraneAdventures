from game.character import CHARACTER_ATTACK_TYPES, CHARACTER_TYPES
from game.skill import ATTACK_TYPES, ELEMENTS
from refs import END_OPT_C, OPT_C, Refs
from text.screens.dungeon_main import box_to_string

BOX_WIDTH = 13


def center_stat(char, index):
    if char is None:
        if index == 6:
            return '-'.center(BOX_WIDTH)
        return ''.center(BOX_WIDTH)
    element = ELEMENTS[char.get_element()]
    attack = CHARACTER_ATTACK_TYPES[char.get_attack_type()]
    stat = [char.get_name(), char.get_current_rank(), element, attack, char.get_health(), char.get_mana(), char.get_physical_attack(), char.get_magical_attack(),
            char.get_defense(), char.get_strength(), char.get_magic(), char.get_endurance(), char.get_agility(), char.get_dexterity()]
    stat_labels = ['', 'Rank', '', '', 'HP', 'MP', 'P.Atk.', 'M.Atk.', 'Def.', 'Str.', 'Mag.', 'End.', 'Agi.', 'Dex.']
    if index == 0 or index == 2 or index == 3:
        if ' ' in stat[index]:
            stat[index] = stat[index].split(' ')[0]
        return f'{stat[index]}'.center(BOX_WIDTH)
    return f"{stat_labels[index]}{f'{stat[index]}'.rjust(BOX_WIDTH - 2 - len(stat_labels[index]))}".center(BOX_WIDTH)


def create_bar(left, right, middle, divider, size):
    if size == 0:
        return ''
    string = ''
    for x in range(size):
        if x == 0:
            string += left
        else:
            string += middle
        for _ in range(BOX_WIDTH):
            string += divider
    return string + right


def create_box(size):
    # TODO - Add Selected Labels to box
    box = ['\n\t' + create_bar('┌', '┐', '┬', '─', 1) + '   ' + create_bar('┌', '┐', '┬', '─', size)]
    for stat in range(12):
        box.append('\n\t│')
        box.append('')
        if stat == 6:
            if size == 0:
                box.append('│ ← No Characters obtained')
            else:
                box.append('│ ← │')
        else:
            if size == 0:
                box.append('│')
            else:
                box.append('│   │')
        for _ in range(size):
            box.append('')
            box.append('│')
        # box.append('\t')
    box.append('\n\t│')
    if size == 0:
        box.append(f'{OPT_C}' + '0'.center(BOX_WIDTH) + f'{END_OPT_C}│')
    else:
        box.append(f'{OPT_C}' + '0'.center(BOX_WIDTH) + f'{END_OPT_C}│   │')
    for index in range(size):
        box.append(f'{OPT_C}' + f'{3 + index}'.center(BOX_WIDTH) + f'{END_OPT_C}')
        box.append('│')
    box.append('\n\t' + create_bar('└', '┘', '┴', '─', 1) + '   ' + create_bar('└', '┘', '┴', '─', size))
    # print(box)
    return box


def populate_box(box, single_char, party, size):
    string = ''.center(BOX_WIDTH)
    gap = 3 + size * 2
    for stat in range(12): # 2 → 9 → 16  7 7
        if single_char is not None:
            box[2 + gap * stat] = center_stat(single_char, stat)
        else:
            if stat == 6:
                box[2 + gap * stat] = '-'.center(BOX_WIDTH)
            else:
                box[2 + gap * stat] = string
        for x in range(size):
            char = party[x]
            if char is not None:
                box[(2 * x + 4) + gap * stat] = center_stat(char, stat)
            else:
                if stat == 6:
                    box[(2 * x + 4) + gap * stat] = '-'.center(BOX_WIDTH)
                else:
                    box[(2 * x + 4) + gap * stat] = string
    return box


def select_screen_char(console):
    char_id_and_index = console._current_screen[len('select_screen_char_'):]
    index = int(char_id_and_index[:char_id_and_index.index('_')])
    character_id = char_id_and_index[char_id_and_index.index('_') + 1:]
    single_char = None
    if character_id != 'none':
        single_char = Refs.gc.get_char_by_id(character_id)

    obtained_chars = Refs.gc.get_obtained_characters(index >= 8)
    if single_char is not None:
        obtained_chars.remove(single_char)
    display_text = '\n\tChoose a character to put in this slot\n\n'

    if console.memory.select_box is None:
        console.memory.select_box_size = len(obtained_chars) if len(obtained_chars) < 9 else 8
        console.memory.select_box = create_box(console.memory.select_box_size)
    else:
        if len(obtained_chars) < console.memory.select_box_size or (console.memory.select_box_size < 8 and len(obtained_chars) > console.memory.select_box_size):
            console.memory.select_box_size = len(obtained_chars) if len(obtained_chars) < 9 else 8
            console.memory.select_box = create_box(console.memory.select_box_size)

    display_text += box_to_string(populate_box(console.memory.select_box, single_char, obtained_chars, console.memory.select_box_size))
    _options = {'0': 'back'}
    if single_char is not None:
        display_text += f'\n\n\t{OPT_C}1:{END_OPT_C} Remove character'
        display_text += f'\n\t{OPT_C}2:{END_OPT_C} Character Attribute Screen\n'
        _options['1'] = f'set_char_{index}_none'
        _options['2'] = f'character_attribute_main_{character_id}'
    else:
        display_text += '\n'
    for char_index in range(len(obtained_chars)):
        _options[str(char_index + 3)] = f'set_char_{index}_' + obtained_chars[char_index].get_id()
    return display_text, _options
