from refs import END_OPT_C, OPT_C
from text.screens.screen_names import BACK, TAVERN_CHAT, TAVERN_RECRUIT, TAVERN_RELAX
from text.screens.town import get_town_header


def get_screen(console, screen_data):
    console.header_callback = get_town_header
    display_text = '\n\tWelcome to the tavern!\n\tWhat would you like to do?\n'

    display_text += f'\n\t{OPT_C}1:{END_OPT_C} Relax\n'
    display_text += f'\t{OPT_C}2:{END_OPT_C} Chat with others\n'
    display_text += f'\t{OPT_C}3:{END_OPT_C} Throw a recruitment party'

    _options = {
        '0': BACK,
        '1': TAVERN_RELAX,
        '2': TAVERN_CHAT,
        '3': TAVERN_RECRUIT
    }

    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} Back\n'
    return display_text, _options


def handle_action(console, action):
    console.set_screen(action, True)
