from math import sqrt

from refs import END_OPT_C, OPT_C, Refs


def status_board_main(console):
    display_string, _options = '', {}
    character_id_and_page = console.get_current_screen()[len('status_board_main_'):]
    index = character_id_and_page.rindex('_')
    character_id, page = character_id_and_page[:index], int(character_id_and_page[index + 1:])
    character = Refs.gc.get_char_by_id(character_id)

    # Display character header and current stats
    ABILITIES_HEADER_SIZE = 10
    RANK_CHAR_SIZE = 5
    STATS_HEADER_SIZE = ABILITIES_HEADER_SIZE + RANK_CHAR_SIZE
    NUMBER_SIZE = 6
    BOX_SIZE = ABILITIES_HEADER_SIZE + RANK_CHAR_SIZE + NUMBER_SIZE
    LARGE_EQUIPMENT_BOX = 33
    ELEMENT_COLORS = ['#FFFFFF', '#80C0FF', '#FF9090', '#E8E880', '#80C080', '#CCA078', '#FFFFFF', '#D094D0']
    TYPE_COLORS = ['#550000', '#050054', '#00460C', '#7F3300', '#7F006E']
    RANK_COLORS = {'I': '#FFFFFF', 'H': '#FFFFFF', 'G': '#FFFFFF',
                   'F': '#AF5113', 'E': '#AF5113',
                   'D': '#CCCCCC', 'C': '#CCCCCC', 'B': '#FFD400', 'A': '#FFD400',
                   'S': '#00BBFF', 'SS': '#00BBFF', 'SSS': '#00BBFF'}

    display_string += '\n'
    display_string += '\t  ' + character.get_name().ljust(BOX_SIZE) + '   ' + character.get_display_name().rjust(BOX_SIZE) + '   '

    display_string += f'\n\t  [color={TYPE_COLORS[character.get_attack_type()]}]' + (character.get_attack_type_string() + ' Type').ljust(BOX_SIZE) + '[/color]'
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
    display_string += '[/b] │\n\t│ ' + 'Health'.ljust(STATS_HEADER_SIZE) + f'{character.get_health()}'.rjust(NUMBER_SIZE)

    display_string += ' │ ' + 'Strength'.ljust(ABILITIES_HEADER_SIZE)
    display_string += f'[color={RANK_COLORS[character.get_strength_rank()]}]' + character.get_strength_rank().center(RANK_CHAR_SIZE) + '[/color]'
    display_string += f'{character.get_strength()}'.rjust(NUMBER_SIZE)

    display_string += ' │\n\t│ ' + 'Mana'.ljust(STATS_HEADER_SIZE) + f'{character.get_mana()}'.rjust(NUMBER_SIZE)
    display_string += ' │ ' + 'Magic'.ljust(ABILITIES_HEADER_SIZE)
    display_string += f'[color={RANK_COLORS[character.get_magic_rank()]}]' + character.get_magic_rank().center(RANK_CHAR_SIZE) + '[/color]'
    display_string += f'{character.get_magic()}'.rjust(NUMBER_SIZE)

    display_string += ' │\n\t│ ' + 'P.Attack'.ljust(STATS_HEADER_SIZE) + f'{character.get_physical_attack()}'.rjust(NUMBER_SIZE)
    display_string += ' │ ' + 'Endurance'.ljust(ABILITIES_HEADER_SIZE)
    display_string += f'[color={RANK_COLORS[character.get_endurance_rank()]}]' + character.get_endurance_rank().center(RANK_CHAR_SIZE) + '[/color]'
    display_string += f'{character.get_endurance()}'.rjust(NUMBER_SIZE)

    display_string += ' │\n\t│ ' + 'M.Attack'.ljust(STATS_HEADER_SIZE) + f'{character.get_magical_attack()}'.rjust(NUMBER_SIZE)
    display_string += ' │ ' + 'Dexterity'.ljust(ABILITIES_HEADER_SIZE)
    display_string += f'[color={RANK_COLORS[character.get_dexterity_rank()]}]' + character.get_dexterity_rank().center(RANK_CHAR_SIZE) + '[/color]'
    display_string += f'{character.get_dexterity()}'.rjust(NUMBER_SIZE)

    display_string += ' │\n\t│ ' + 'Defense'.ljust(STATS_HEADER_SIZE) + f'{character.get_defense()}'.rjust(NUMBER_SIZE)
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
    display_string += f'\n\n\tRank {page} Status Board'

    current_rank_index = character.get_current_rank()
    rank = character.get_rank(page)
    board = rank.get_board()
    s, m, e, a, d = rank.get_board().get_counts()
    sw, mw, ew, aw, dw = rank.get_board().get_values()

    tiles = []
    for _ in range(s):
        tiles.append(f'S {sw}')
    for _ in range(s):
        tiles.append(f'M {mw}')
    for _ in range(s):
        tiles.append(f'E {ew}')
    for _ in range(s):
        tiles.append(f'A {aw}')
    for _ in range(s):
        tiles.append(f'D {dw}')

    max_width = 0
    option_index = 7
    tile_sizes = []
    size = int(sqrt(s + m + e + a + d))
    for tile_y in range(size):
        for tile_x in range(size):
            tile_index = (tile_y * size) + tile_x
            max_width = max(max_width, len(f'{option_index + tile_index} {tiles[tile_index]}'))
            if board.get_unlocked(tile_index):
                tiles[tile_index] = f'[s]{OPT_C}{option_index + tile_index}{END_OPT_C} {tiles[tile_index]}[/s]'
                tile_sizes.append(len(f'[s]{OPT_C}{END_OPT_C}[/s]'))
            else:
                tiles[tile_index] = f'{OPT_C}{option_index + tile_index}{END_OPT_C} {tiles[tile_index]}'
                tile_sizes.append(len(f'{OPT_C}{END_OPT_C}'))
                _options[str(option_index + tile_index)] = f'status_board_unlock_{character_id}_{page}_{tile_index}'

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

    left = page > 1
    right = page < current_rank_index

    left_string = f'{OPT_C}1{END_OPT_C} Prev Status Board'
    right_string = f'Next Status Board {OPT_C}2{END_OPT_C}'

    if left:
        _options['1'] = f'status_board_main_{character_id}_{page - 1}'
    else:
        left_string = f'[s]{left_string}[/s]'

    if right:
        _options['2'] = f'status_board_main_{character_id}_{page + 1}'
    else:
        right_string = f'[s]{right_string}[/s]'

    display_string += f'\n\n\t←──── {left_string} | {right_string} ────→\n'

    display_string += f'\n\t{OPT_C}3:{END_OPT_C} Unlock All'
    display_string += f'\n\t{OPT_C}4:{END_OPT_C} View Available Falna'

    # display_string += f'\n\n\t{OPT_C}5:{END_OPT_C} Upgrade Combat Skills'
    # display_string += f'\n\t{OPT_C}6:{END_OPT_C} View All Abilities'

    display_string += f'\n\n\t{OPT_C}0:{END_OPT_C} Back\n'

    _options['3'] = f'status_board_unlock_{character_id}_{page}_all'
    _options['4'] = 'status_board_view_falna'
    # _options['5'] = 'status_board_upgrade_combat_skills'
    # _options['6'] = 'status_board_view_all_abilities'
    _options['0'] = 'back'
    return display_string, _options


def status_board_unlock(console):
    display_string, _options = '', {}
    string_info = console.get_current_screen()[len('status_board_unlock_'):]
    index = string_info.rindex('_', 0, string_info.rindex('_') - 1)
    character_id, page_info = string_info[:index], string_info[index + 1:]
    rank, unlock_option = page_info.split('_')
    rank = int(rank)
    character = Refs.gc.get_char_by_id(character_id)
    board = character.get_rank(rank).get_board()

    tiles_to_unlock = []
    if unlock_option == 'all':
        for index in range(board.get_count()):
            if not board.get_unlocked(index):
                tiles_to_unlock.append(index)
    else:
        tiles_to_unlock.append(int(unlock_option))

    s, m, e, a, d = board.get_counts()
    sv, mv, ev, av, dv = board.get_values()

    FALNA_COST = ['tiny', 'tiny', 'small', 'small', 'regular', 'regular', 'large', 'large', 'huge', 'huge']
    FALNA_COST_AMOUNT = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
    VARENTH_COST = [1500, 2500, 5000, 10000, 25000, 50000, 100000, 250000, 500000, 1000000]

    falna_type = FALNA_COST[rank - 1]
    falna_cost = FALNA_COST_AMOUNT[rank - 1]
    varenth_cost = VARENTH_COST[rank - 1]

    sc, mc, ec, ac, dc = 0, 0, 0, 0, 0
    for tile_index in tiles_to_unlock:
        if tile_index < s:
            sc += 1 * falna_cost
        elif tile_index < s + m:
            mc += 1 * falna_cost
        elif tile_index < s + m + e:
            ec += 1 * falna_cost
        elif tile_index < s + m + e + a:
            ac += 1 * falna_cost
        else:
            dc += 1 * falna_cost
    vcost = len(tiles_to_unlock) * varenth_cost
    sb, mb, eb, ab, db = sc * sv, mc * mv, ec * ev, ac * av, dc * dv

    if unlock_option == 'all':
        display_string += '\n\tUnlock All'
    else:
        display_string += '\n\tUnlock Tile'
    display_string += '\n\n\t'
    if sc > 0:
        display_string += f'Str. +{sb}'.center(10)
    if mc > 0:
        display_string += f'Mag. +{mb}'.center(10)
    if ec > 0:
        display_string += f'End. +{eb}'.center(10)
    if ac > 0:
        display_string += f'Agi. +{ab}'.center(10)
    if dc > 0:
        display_string += f'Dex. +{db}'.center(10)
    display_string += '\n\t'
    if sc > 0:
        display_string += f'{character.get_strength()} → {character.get_strength() + sb}'.center(10)
    if mc > 0:
        display_string += f'{character.get_magic()} → {character.get_magic() + mb}'.center(10)
    if ec > 0:
        display_string += f'{character.get_endurance()} → {character.get_endurance() + eb}'.center(10)
    if ac > 0:
        display_string += f'{character.get_agility()} → {character.get_agility() + ab}'.center(10)
    if dc > 0:
        display_string += f'{character.get_dexterity()} → {character.get_dexterity() + db}'.center(10)
    display_string += '\n\n\tCost:'

    hsc = Refs.gc.get_inventory().get_item_count(f"{falna_type}_strength_falna")
    hmc = Refs.gc.get_inventory().get_item_count(f"{falna_type}_magic_falna")
    hec = Refs.gc.get_inventory().get_item_count(f"{falna_type}_endurance_falna")
    hac = Refs.gc.get_inventory().get_item_count(f"{falna_type}_agility_falna")
    hdc = Refs.gc.get_inventory().get_item_count(f"{falna_type}_dexterity_falna")

    if sc > 0:
        display_string += f'\n\t\t{falna_type.title()} Strength Falna x{sc}'
        display_string += f'\n\t\t - In Inventory: {hsc}'
    if mc > 0:
        display_string += f'\n\t\t{falna_type.title()} Magic Falna x{mc}'
        display_string += f'\n\t\t - In Inventory: {hmc}'
    if ec > 0:
        display_string += f'\n\t\t{falna_type.title()} Endurance Falna x{ec}'
        display_string += f'\n\t\t - In Inventory: {hec}'
    if ac > 0:
        display_string += f'\n\t\t{falna_type.title()} Agility Falna x{ac}'
        display_string += f'\n\t\t - In Inventory: {hac}'
    if dc > 0:
        display_string += f'\n\t\t{falna_type.title()} Dexterity Falna x{dc}'
        display_string += f'\n\t\t - In Inventory: {hdc}'
    display_string += f'\n\n\t\tVarenth: {vcost}'
    varenth = Refs.gc.get_varenth()
    display_string += f'\n\t\t - Have: {varenth}\n'

    if hsc > sc and hmc > mc and hec > ec and hac > ac and hdc > dc and varenth > vcost:
        display_string += f'\n\t{OPT_C}1:{END_OPT_C} Continue'
        string = f'status_board_unlock_confirm_{hsc}_{hmc}_{hec}_{hac}_{hdc}_{falna_type}_{vcost}_{rank}#'
        for tile_index in tiles_to_unlock:
            string += f'{tile_index}_'
        _options['1'] = string[:-1] + f'#{character_id}'
    else:
        display_string += f'\n\t[s]{OPT_C}1:{END_OPT_C} Continue[/s]'

    display_string += f'\n\t{OPT_C}0:{END_OPT_C} Back\n'
    _options['0'] = 'back'

    return display_string, _options


def status_board_view_falna(console):
    _options = {}
    display_string = '\n\tFalna can be gathered by killing monsters'
    display_string += '\n\n\t             Str.      Mag.      End.      Agi.      Dex.   \n\t'

    for falna_size in ['tiny', 'small', 'regular', 'large', 'huge']:
        display_string += falna_size.title().rjust(7)
        for falna_type in ['strength', 'magic', 'endurance', 'agility', 'dexterity']:
            count = Refs.gc.get_inventory().get_item_count(f"{falna_size}_{falna_type}_falna")
            display_string += f'{count}'.center(10)
        display_string += '\n\t'

    display_string += f'\n\t{OPT_C}0:{END_OPT_C} Back\n'
    _options['0'] = 'back'

    return display_string, _options