from math import sqrt

from refs import END_OPT_C, OPT_C, Refs
from text.screens.character_attributes import ABILITIES_HEADER_SIZE, BOX_SIZE, ELEMENT_COLORS, NUMBER_SIZE, RANK_CHAR_SIZE, RANK_COLORS, STATS_HEADER_SIZE, TYPE_COLORS
from text.screens.screen_names import BACK, STATUS_BOARD, STATUS_BOARD_UNLOCK, STATUS_BOARD_VIEW_FALNA


def get_screen(console, screen_data):
    display_string, _options = '', {}
    rank, character_id = screen_data.split('#')
    character = Refs.gc.get_char_by_id(character_id)

    display_string += '\n'
    display_string += '\t  ' + character.get_name().ljust(BOX_SIZE) + '   ' + character.get_display_name().rjust(BOX_SIZE) + '   '

    if not character.is_support():
        display_string += f'\n\t  [color={TYPE_COLORS[character.get_attack_type()]}]' + (character.get_attack_type_string() + ' Type').ljust(BOX_SIZE) + '[/color]'
    else:
        display_string += f'\n\t  ' + ''.ljust(BOX_SIZE)
    if not character.is_support():
        display_string += f'   [color={ELEMENT_COLORS[character.get_element()]}]' + character.get_element_string().rjust(BOX_SIZE) + '[/color]   '

    # Create the first row of the box
    display_string += '\n\t┌'
    for _ in range(2):
        for _ in range(BOX_SIZE + 2):
            display_string += '─'
        display_string += '┬'
    display_string = display_string[:-1] + '┐'

    display_string += '\n\t│ [b]' + 'Total Stats'.center(BOX_SIZE)
    display_string += '[/b] │ [b]' + 'Total Abilities'.center(BOX_SIZE)

    display_string += '[/b] │\n\t│ ' + 'Health'.ljust(STATS_HEADER_SIZE) + f'{Refs.gc.format_number(int(character.get_health()))}'.rjust(NUMBER_SIZE)
    display_string += ' │ ' + 'Strength'.ljust(ABILITIES_HEADER_SIZE)
    display_string += f'[color={RANK_COLORS[character.get_strength_rank()]}]' + character.get_strength_rank().center(RANK_CHAR_SIZE) + '[/color]'
    display_string += f'{character.get_strength()}'.rjust(NUMBER_SIZE)

    display_string += ' │\n\t│ ' + 'Mana'.ljust(STATS_HEADER_SIZE) + f'{Refs.gc.format_number(int(character.get_mana()))}'.rjust(NUMBER_SIZE)
    display_string += ' │ ' + 'Magic'.ljust(ABILITIES_HEADER_SIZE)
    display_string += f'[color={RANK_COLORS[character.get_magic_rank()]}]' + character.get_magic_rank().center(RANK_CHAR_SIZE) + '[/color]'
    display_string += f'{character.get_magic()}'.rjust(NUMBER_SIZE)

    display_string += ' │\n\t│ ' + 'P.Attack'.ljust(STATS_HEADER_SIZE) + f'{Refs.gc.format_number(int(character.get_physical_attack()))}'.rjust(NUMBER_SIZE)
    display_string += ' │ ' + 'Endurance'.ljust(ABILITIES_HEADER_SIZE)
    display_string += f'[color={RANK_COLORS[character.get_endurance_rank()]}]' + character.get_endurance_rank().center(RANK_CHAR_SIZE) + '[/color]'
    display_string += f'{character.get_endurance()}'.rjust(NUMBER_SIZE)

    display_string += ' │\n\t│ ' + 'M.Attack'.ljust(STATS_HEADER_SIZE) + f'{Refs.gc.format_number(int(character.get_magical_attack()))}'.rjust(NUMBER_SIZE)
    display_string += ' │ ' + 'Dexterity'.ljust(ABILITIES_HEADER_SIZE)
    display_string += f'[color={RANK_COLORS[character.get_dexterity_rank()]}]' + character.get_dexterity_rank().center(RANK_CHAR_SIZE) + '[/color]'
    display_string += f'{character.get_dexterity()}'.rjust(NUMBER_SIZE)

    display_string += ' │\n\t│ ' + 'Defense'.ljust(STATS_HEADER_SIZE) + f'{Refs.gc.format_number(int(character.get_defense()))}'.rjust(NUMBER_SIZE)
    display_string += ' │ ' + 'Agility'.ljust(ABILITIES_HEADER_SIZE)
    display_string += f'[color={RANK_COLORS[character.get_agility_rank()]}]' + character.get_agility_rank().center(RANK_CHAR_SIZE) + '[/color]'
    display_string += f'{character.get_agility()}'.rjust(NUMBER_SIZE)

    display_string += ' │\n\t'

    display_string += '└'
    for _ in range(2):
        for _ in range(BOX_SIZE + 2):
            display_string += '─'
        display_string += '┴'
    display_string = display_string[:-1] + '┘'

    # Display the current page status board
    display_string += f'\n\n\tRank {rank} Status Board'

    current_rank_index = character.get_current_rank()
    char_rank = character.get_rank(int(rank))
    board = char_rank.get_board()
    s, m, e, a, d = char_rank.get_board().get_counts()
    sw, mw, ew, aw, dw = char_rank.get_board().get_values()

    tiles = []
    for _ in range(s):
        tiles.append(f'S {sw}')
    for _ in range(m):
        tiles.append(f'M {mw}')
    for _ in range(e):
        tiles.append(f'E {ew}')
    for _ in range(a):
        tiles.append(f'A {aw}')
    for _ in range(d):
        tiles.append(f'D {dw}')

    max_width = 0
    option_index = 7
    tile_sizes = []
    size = int(sqrt(s + m + e + a + d))
    for tile_y in range(size):  # 0 1 2
        for tile_x in range(size):  # 0 1 2
            tile_index = (tile_y * size) + tile_x
            max_width = max(max_width, len(f'{option_index + tile_index} {tiles[tile_index]}'))
            if board.get_unlocked(tile_index):
                tiles[tile_index] = f'[s]{OPT_C}{option_index + tile_index}{END_OPT_C} {tiles[tile_index]}[/s]'
                tile_sizes.append(len(f'[s]{OPT_C}{END_OPT_C}[/s]'))
            else:
                tiles[tile_index] = f'{OPT_C}{option_index + tile_index}{END_OPT_C} {tiles[tile_index]}'
                tile_sizes.append(len(f'{OPT_C}{END_OPT_C}'))
                _options[str(option_index + tile_index)] = (f'{STATUS_BOARD_UNLOCK}:{rank}#{character_id}#{tile_index}', True)

    # Make top line
    display_string += '\n\t┌'
    for _ in range(size):
        for _ in range(max_width + 2):
            display_string += '─'
        display_string += '┬'
    display_string = display_string[:-1] + '┐\n\t'
    # Make rows
    for y in range(size):
        display_string += '│'
        for x in range(size):
            display_string += f' {tiles[(y * size) + x].rjust(max_width + tile_sizes[(y * size) + x])} │'
        display_string += '\n\t'
        if y != size - 1:
            display_string += '├'
            for _ in range(size):
                for _ in range(max_width + 2):
                    display_string += '─'
                display_string += '┼'
            display_string = display_string[:-1] + '┤\n\t'
    # Make bottom line
    display_string += '└'
    for _ in range(size):
        for _ in range(max_width + 2):
            display_string += '─'
        display_string += '┴'
    display_string = display_string[:-1] + '┘'

    left = int(rank) > 1
    right = int(rank) < current_rank_index

    left_string = f'{OPT_C}1{END_OPT_C} Prev Status Board'
    right_string = f'Next Status Board {OPT_C}2{END_OPT_C}'

    if left:
        _options['1'] = (f'{STATUS_BOARD}:{int(rank) - 1}#{character_id}', False)
    else:
        left_string = f'[s]{left_string}[/s]'

    if right:
        _options['2'] = (f'{STATUS_BOARD}:{int(rank) + 1}#{character_id}', False)
    else:
        right_string = f'[s]{right_string}[/s]'

    display_string += f'\n\n\t←──── {left_string} | {right_string} ────→\n'

    display_string += f'\n\t{OPT_C}3:{END_OPT_C} Unlock All'
    display_string += f'\n\t{OPT_C}4:{END_OPT_C} View Available Falna'

    display_string += f'\n\n\t{OPT_C}0:{END_OPT_C} Back\n'

    _options['3'] = (f'{STATUS_BOARD_UNLOCK}:{rank}#{character_id}#all', True)
    _options['4'] = (STATUS_BOARD_VIEW_FALNA, True)
    _options['0'] = BACK
    return display_string, _options


def handle_action(console, action):
    console.set_screen(*action)


