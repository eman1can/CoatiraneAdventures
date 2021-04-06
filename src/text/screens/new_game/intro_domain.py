from loading.family import load_domains
from refs import END_OPT_C, OPT_C, Refs
from text.screens.screen_names import BACK, INTRO_DOMAIN, INTRO_SELECT


def get_screen(console, screen_data):
    page_num = int(screen_data)

    if page_num < 0:
        page_num = len(console.domains) - 1

    display_text = f'\n\tOh almighty {console.new_game_info["name"]}, what is your domain?\n'
    _options = {'0': BACK}

    if console.domains is None:
        console.domains = load_domains(Refs.gc.get_program_type())

    desc = console.domains[page_num].get_large_description().replace('\n', '\n\t\t')
    display_text += f'\n\t{OPT_C}1:{END_OPT_C} {console.domains[page_num].title}\n\t\t{desc}\n'
    print(page_num, console.domains)
    display_text += f'\n\t←────── {OPT_C}2{END_OPT_C} {console.domains[page_num - 1].title} | {console.domains[(page_num + 1) % len(console.domains)].title} {OPT_C}3{END_OPT_C} ──────→\n'
    display_text += f'\n\t{OPT_C}0:{END_OPT_C} back\n'
    _options['1'] = console.domains[page_num].title
    _options['2'] = INTRO_DOMAIN + ':' + str(page_num - 1)
    _options['3'] = INTRO_DOMAIN + ':' + str(page_num + 1)
    return display_text, _options


def handle_action(console, action):
    if action.startswith(INTRO_DOMAIN):
        console.set_screen(action)
    else:
        console.new_game_info['domain'] = action
        console.set_screen(INTRO_SELECT)
