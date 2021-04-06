from random import choices, randint

from refs import END_OPT_C, OPT_C, Refs
from text.screens.screen_names import BACK, TAVERN_RECRUIT_SHOW
from text.screens.town import get_town_header


def get_screen(console, screen_data):
    console.header_callback = get_town_header

    display_text = '\n\tThrowing a party for recruitment will cost 25,000V.\n\tAre you sure you would like to throw a party?'

    _options = {'0': BACK, '1': 0}
    display_text += f'\n\n\t{OPT_C}1:{END_OPT_C} Yes! Party time!'
    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} Back\n'
    return display_text, _options


def handle_action(console, action):
    cost = 25000
    if cost > Refs.gc.get_varenth():
        console.error_time = 2.5
        console.error_text = 'You don\'t have that much money!'
    else:
        Refs.gc.update_varenth(-cost)
        success = randint(1, 99) < 33
        if success:
            chars = Refs.gc.get_non_obtained_characters()
            count = choices([x + 1 for x in range(len(chars))], [len(chars) - x for x in range(len(chars))])[0]
            # Change to choose characters based on a recruitment weight
            recruited = choices(chars, k=count)
            string = ''
            for char in recruited:
                string += char.get_id() + '#'
        else:
            string = 'failure#'
        console.set_screen(f'{TAVERN_RECRUIT_SHOW}:#{string[:-1]}')
