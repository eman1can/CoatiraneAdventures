from refs import END_OPT_C, OPT_C, Refs
from text.screens.screen_names import BACK, PERK_BESTOW
from text.screens.town import get_town_header


def get_screen(console, screen_data):
    console.header_callback = get_town_header
    _options, perk_id = {}, screen_data
    perk = Refs.gc['perks'][perk_id]
    perk_cost = perk.get_cost()

    display_text = f'\n\n\t{perk.get_name()} - {perk.get_tree().title()}'
    display_text += f'\n\t\t' + perk.get_description().replace('\n', '\n\t\t')
    display_text += f'\n\n\t\tCosts {perk_cost} Perk Points to unlock\n'

    perk_points = Refs.gc.get_perk_points()
    meets_requirements = True
    for requirement in perk.get_requirements():
        if requirement == 'none':
            continue
        meets_requirements &= Refs.gc.has_perk(requirement)

    if perk_points >= perk_cost and (Refs.gc.get_skill_level() > perk_cost or perk_cost == 1) and meets_requirements:
        display_text += f'\n\t{OPT_C}1:{END_OPT_C} Bestow Perk Upon Adventurer'
        _options['1'] = f'{PERK_BESTOW}:{perk_id}'
    else:
        display_text += f'\n\t[s]{OPT_C}1:{END_OPT_C} Bestow Perk Upon Adventurer[/s]'

    display_text += f'\n\t{OPT_C}0:{END_OPT_C} Back\n'
    _options['0'] = BACK
    return display_text, _options


def handle_action(console, action):
    console.set_screen(action, True)
