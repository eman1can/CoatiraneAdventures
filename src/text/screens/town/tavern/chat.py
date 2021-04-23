from refs import END_OPT_C, OPT_C
from text.screens.screen_names import BACK


def get_screen(console, screen_data):
    display_text, _options = '', {'0': BACK}
    display_text = '\n\tThis screen is not implemented!'
    display_text += f'\n\n{OPT_C}0:{END_OPT_C} Back\n'
    return display_text, _options


def handle_action(console, action):
    console.set_screen(action, True)
