from refs import END_OPT_C, OPT_C
from text.screens.screen_names import BACK, INTRO_DOMAIN


def get_screen(console, screen_data):
    display_text = f'\n\tOh almighty {console.new_game_info["name"]}, what is your gender?\n'
    display_text += f'\n\t{OPT_C}1:{END_OPT_C} God'
    display_text += f'\n\t{OPT_C}2:{END_OPT_C} Goddess'
    display_text += f'\n\t{OPT_C}3:{END_OPT_C} Goddex'
    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} back\n'
    _options = {'0': BACK, '1': 'male', '2': 'female', '3': 'neither'}
    return display_text, _options


def handle_action(console, action):
    console.new_game_info['gender'] = action
    console.set_screen(INTRO_DOMAIN + ':0', True)
