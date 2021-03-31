from refs import END_OPT_C, OPT_C, Refs
from text.screens.screen_names import BACK, STATUS_BOARD


def get_screen(console, screen_data):
    display_string, _options = '', {}
    rank, character_id, unlock_option = screen_data.split('#')
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

    if hsc >= sc and hmc >= mc and hec >= ec and hac >= ac and hdc >= dc and varenth > vcost:
        display_string += f'\n\t{OPT_C}1:{END_OPT_C} Continue'
        string = f'{sc}#{mc}#{ec}#{ac}#{dc}#{falna_type}#{vcost}#{rank}#{character_id}#'
        for tile_index in tiles_to_unlock:
            string += f'{tile_index}#'
        _options['1'] = string[:-1]
    else:
        display_string += f'\n\t[s]{OPT_C}1:{END_OPT_C} Continue[/s]'

    display_string += f'\n\t{OPT_C}0:{END_OPT_C} Back\n'
    _options['0'] = BACK

    return display_string, _options


def handle_action(console, action):
    hsc, hmc, hec, hac, hdc, ftype, vcost, rank_index, character_id, tile_list = action.split('#', 9)
    Refs.gc.update_varenth(-int(vcost))
    if int(hsc) > 0:
        Refs.gc.get_inventory().remove_item(f'{ftype}_strength_falna', int(hsc))
    if int(hmc) > 0:
        Refs.gc.get_inventory().remove_item(f'{ftype}_magic_falna', int(hmc))
    if int(hec) > 0:
        Refs.gc.get_inventory().remove_item(f'{ftype}_endurance_falna', int(hec))
    if int(hac) > 0:
        Refs.gc.get_inventory().remove_item(f'{ftype}_agility_falna', int(hac))
    if int(hdc) > 0:
        Refs.gc.get_inventory().remove_item(f'{ftype}_dexterity_falna', int(hdc))
    character = Refs.gc.get_char_by_id(character_id)
    rank = character.get_rank(int(rank_index))
    board = rank.get_board()
    for tile_index in tile_list.split('_'):
        board.unlock_index(int(tile_index))
    character.refresh_stats()
    console.set_screen(f'{STATUS_BOARD}:{rank_index}#{character_id}')
