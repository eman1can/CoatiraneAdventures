from refs import END_OPT_C, OPT_C, Refs
from text.screens.dungeon import BOX_WIDTH, box_to_string, create_box, populate_box
from text.screens.screen_names import BACK, CHARACTER_ATTRIBUTE, DUNGEON_BATTLE, DUNGEON_CONFIRM, INVENTORY_BATTLE


def get_screen(console, screen_data):
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
    if console.party_box is None:
        console.party_box = create_box()

    display_text += box_to_string(console, populate_box(console.party_box, party, True))

    display_text += '\n\t'
    for _ in range(BOX_WIDTH * 4 - 14):
        display_text += ' '
    display_text += f'←──── [s]{OPT_C}5{END_OPT_C} Prev Party[/s] | [s]Next Party {OPT_C}6{END_OPT_C}[/s] ────→'

    if floor_data.get_floor().get_id() > floor_data.get_next_floor():
        # Ascending
        display_text += f'\n\t{OPT_C}0:{END_OPT_C} Go to previous floor.'
        _options['0'] = f'{DUNGEON_CONFIRM}:up'
        display_text += f'\n\t{OPT_C}1:{END_OPT_C} Back to current floor.'
        _options['1'] = BACK
        display_text += f'\n\t{OPT_C}2:{END_OPT_C} Inventory\n'
        _options['2'] = f'{INVENTORY_BATTLE}:0'
    else:
        # Descending
        if floor_data.have_beaten_boss():
            display_text += f'\n\t{OPT_C}0:{END_OPT_C} Back to current floor.'
            _options['0'] = BACK
            display_text += f'\n\t{OPT_C}1:{END_OPT_C} Descend to next floor.'
            _options['1'] = f'{DUNGEON_CONFIRM}:down'
            display_text += f'\n\t{OPT_C}2:{END_OPT_C} Inventory\n'
            _options['2'] = f'{INVENTORY_BATTLE}:0'
        else:
            display_text += f'\n\t{OPT_C}0:{END_OPT_C} Inventory\n'
            display_text += f'\n\t{OPT_C}1:{END_OPT_C} Fight\n'
            _options['0'] = f'{INVENTORY_BATTLE}:0'
            _options['1'] = 'fight_boss'
    index = 6
    for char in party:
        if char is None:
            continue
        _options[str(index)] = f'{CHARACTER_ATTRIBUTE}:{char.get_id()}'
        index += 1

    print(_options)
    return display_text, _options


def handle_action(console, action):
    if action == 'fight_boss':
        Refs.gc.get_floor_data().generate_boss_encounter()
        console.set_screen(DUNGEON_BATTLE, False)
    else:
        console.set_screen(action, True)
