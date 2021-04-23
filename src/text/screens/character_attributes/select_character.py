from game.character import CHARACTER_ATTACK_TYPES
from game.skill import ELEMENTS
from refs import END_OPT_C, OPT_C, Refs
from text.screens.screen_names import BACK, CHARACTER_ATTRIBUTE, DUNGEON_MAIN

BOX_WIDTH = 13


def center_stat(char, index):
    if char is None:
        if index == 6:
            return '+'.center(BOX_WIDTH)
        return ''.center(BOX_WIDTH)
    if char.is_support():
        stat = [char.get_name, char.get_current_rank, char.get_health, char.get_mana, char.get_physical_attack, char.get_magical_attack,
                char.get_defense, char.get_strength, char.get_magic, char.get_endurance, char.get_agility, char.get_dexterity]
        stat_labels = ['', 'Rank', 'HP', 'MP', 'P.Atk.', 'M.Atk.', 'Def.', 'Str.', 'Mag.', 'End.', 'Agi.', 'Dex.']
        if index <= 1:
            stat_string = stat[index]()
        else:
            stat_string = Refs.gc.format_number(int(stat[index]()))
    else:
        stat = [char.get_name, char.get_current_rank, char.get_element_string, char.get_attack_type_string, char.get_health, char.get_mana, char.get_physical_attack, char.get_magical_attack,
                char.get_defense, char.get_strength, char.get_magic, char.get_endurance, char.get_agility, char.get_dexterity]
        stat_labels = ['', 'Rank', '', '', 'HP', 'MP', 'P.Atk.', 'M.Atk.', 'Def.', 'Str.', 'Mag.', 'End.', 'Agi.', 'Dex.']
        if index <= 3:
            stat_string = stat[index]()
        else:
            stat_string = Refs.gc.format_number(int(stat[index]()))
        if index == 0 or index == 2 or index == 3:
            if ' ' in stat_string:
                stat_string = stat_string.split(' ')[0]
            return f'{stat_string}'.center(BOX_WIDTH)
    return f"{stat_labels[index]}{f'{stat_string}'.rjust(BOX_WIDTH - 2 - len(stat_labels[index]))}".center(BOX_WIDTH)


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


def box_to_string(console, box):
    string = ''
    for index in range(len(box)):
        string += box[index]
    return string


def create_box(size):
    box = ['\n\t' + ''.ljust(BOX_WIDTH + 2) + '   '] + ['Selected'.center(BOX_WIDTH + 1) for _ in range(size)] + ['\n\t' + create_bar('┌', '┐', '┬', '─', 1) + '   ' + create_bar('┌', '┐', '┬', '─', size)]
    for stat in range(12):
        box.append('\n\t│')
        box.append('')
        if stat == 6:
            if size == 0:
                box.append('│ ← No Characters available.')
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
    box.append('\n\t│')
    if size == 0:
        box.append(f'{OPT_C}' + '0'.center(BOX_WIDTH) + f'{END_OPT_C}│')
    else:
        box.append(f'{OPT_C}' + '0'.center(BOX_WIDTH) + f'{END_OPT_C}│   │')
    for index in range(size):
        box.append(f'{OPT_C}' + f'{3 + index}'.center(BOX_WIDTH) + f'{END_OPT_C}')
        box.append('│')
    box.append('\n\t' + create_bar('└', '┘', '┴', '─', 1) + '   ' + create_bar('└', '┘', '┴', '─', size))
    return box


def populate_box(box, single_char, party, size):
    string = ''.center(BOX_WIDTH)
    gap = 3 + size * 2

    for index, char in enumerate(party):
        if char in Refs.gc.get_current_party():
            box[index + 1] = 'Selected'.center(BOX_WIDTH + 1)
        else:
            box[index + 1] = ''.center(BOX_WIDTH + 1)

    OFFSET = size + 3
    for stat in range(12):
        if single_char is not None:
            box[OFFSET + gap * stat] = center_stat(single_char, stat)
        else:
            if stat == 6:
                box[OFFSET + gap * stat] = '+'.center(BOX_WIDTH)
            else:
                box[OFFSET + gap * stat] = string
        for x in range(size):
            char = party[x]
            if char is not None:
                box[(2 * x + OFFSET + 2) + gap * stat] = center_stat(char, stat)
            else:
                if stat == 6:
                    box[(2 * x + OFFSET + 2) + gap * stat] = '+'.center(BOX_WIDTH)
                else:
                    box[(2 * x + OFFSET + 2) + gap * stat] = string
    return box


def get_screen(console, screen_data):
    index, character_id = screen_data.split('#')
    index = int(index)
    single_char = None
    if character_id != 'none':
        single_char = Refs.gc.get_char_by_id(character_id)

    obtained_chars = Refs.gc.get_obtained_characters(index >= 8)
    if single_char is not None:
        obtained_chars.remove(single_char)
    else:
        # Remove party chars
        for char in Refs.gc.get_current_party():
            if char in obtained_chars:
                obtained_chars.remove(char)

    display_text = '\n\tChoose a character to put in this slot\n\n'

    if console.select_box is None:
        console.select_box_size = len(obtained_chars) if len(obtained_chars) < 9 else 8
        console.select_box = create_box(console.select_box_size)
    else:
        if len(obtained_chars) < console.select_box_size or (console.select_box_size < 8 and len(obtained_chars) > console.select_box_size):
            console.select_box_size = len(obtained_chars) if len(obtained_chars) < 9 else 8
            console.select_box = create_box(console.select_box_size)

    display_text += box_to_string(console, populate_box(console.select_box, single_char, obtained_chars, console.select_box_size))
    _options = {'0': BACK}
    if single_char is not None:
        display_text += f'\n\n\t{OPT_C}1:{END_OPT_C} Remove character'
        display_text += f'\n\t{OPT_C}2:{END_OPT_C} Character Attribute Screen\n'
        _options['1'] = f'set_char#{index}#none'
        _options['2'] = f'{CHARACTER_ATTRIBUTE}:{character_id}'
    else:
        display_text += '\n'
    for char_index in range(len(obtained_chars)):
        _options[str(char_index + 3)] = f'set_char#{index}#' + obtained_chars[char_index].get_id()
    return display_text, _options


def handle_action(console, action):
    if action.startswith('set_char'):
        index, character_id = action.split('#')[1:]
        index = int(index)
        char = None
        if character_id != 'none':
            char = Refs.gc.get_char_by_id(character_id)

        # Resolve
        if char is not None and char in Refs.gc.get_current_party():
            # Set the char in the party to None
            if Refs.gc.get_current_party()[index] is None:
                Refs.gc.get_current_party()[Refs.gc.get_current_party().index(char)] = None
            else:
                Refs.gc.get_current_party()[Refs.gc.get_current_party().index(char)] = Refs.gc.get_current_party()[index]

        Refs.gc.get_current_party()[index] = char
        if char is None and index < 8:
            Refs.gc.get_current_party()[index + 8] = char
        console.set_screen(DUNGEON_MAIN, False)
    else:
        console.set_screen(action, True)
