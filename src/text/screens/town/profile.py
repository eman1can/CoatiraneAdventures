from refs import END_OPT_C, OPT_C, Refs
from text.screens.screen_names import BACK, SKILL_TREE_MAIN


def get_screen(console, screen_data):
    console.header_callback = None
    display_text = f'\n\n\n\t{Refs.gc.get_name()}'
    display_text += f'\n\t{Refs.gc.get_domain()} {Refs.gc.get_gender()}'
    domain = Refs.gc.get_domain_info()
    domain_desc = domain.get_large_description().replace('\n', '\n\t')
    display_text += f'\n\t{domain.get_title()}\n\t{domain_desc}\n'
    display_text += f'\n\tRenown - {Refs.gc.get_renown()}'
    display_text += f'\n\tCurrent Perk Points - {Refs.gc.get_perk_points()}'
    display_text += f'\n\tPerks Unlocked {Refs.gc.get_skill_level()}'
    display_text += f'\n\tYou have {Refs.gc.format_number(Refs.gc.get_varenth())} Varenth'
    display_text += f'\n\n\t{OPT_C}1:{END_OPT_C} Skill Trees'
    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} Back\n'
    _options = {'0': BACK, '1': SKILL_TREE_MAIN}
    return display_text, _options


def handle_action(console, action):
    console.set_screen(action, True)
