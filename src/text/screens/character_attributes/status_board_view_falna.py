from refs import END_OPT_C, OPT_C, Refs
from text.screens.screen_names import BACK


def get_screen(console, screen_data):
    _options = {}
    display_string = '\n\tFalna can be gathered by killing monsters'
    display_string += '\n\n\t          Str.      Mag.      End.      Agi.      Dex.   \n\t'

    for falna_size in ['tiny', 'small', 'regular', 'large', 'huge']:
        display_string += falna_size.title().rjust(7)
        for falna_type in ['strength', 'magic', 'endurance', 'agility', 'dexterity']:
            count = Refs.gc.get_inventory().get_item_count(f"{falna_size}_{falna_type}_falna")
            display_string += f'{count}'.center(10)
        display_string += '\n\t'

    display_string += f'\n\t{OPT_C}0:{END_OPT_C} Back\n'
    _options['0'] = BACK

    return display_string, _options


def handle_action(console, action):
    pass
