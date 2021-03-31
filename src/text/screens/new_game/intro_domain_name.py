from refs import END_OPT_C, OPT_C
from text.screens.screen_names import BACK, INTRO_DOMAIN_GENDER


def get_screen(console, screen_data):
    display_text = f'\n\tOh almighty Deity, please bless us with your name.\n'
    display_text += f'\n\t{OPT_C}0:{END_OPT_C} Cancel\n'
    _options = {'0': BACK}
    return display_text, _options


def handle_action(console, action):
    console.new_game_info['name'] = action
    console.set_screen(INTRO_DOMAIN_GENDER)
