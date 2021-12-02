from refs import END_OPT_C, OPT_C, Refs
from text.screens.screen_names import BACK, CRAFTING_ALLOYS, CRAFTING_EQUIPMENT, CRAFTING_ITEMS, CRAFTING_POTIONS, CRAFTING_PROCESS_MATERIALS
from text.screens.town import get_town_header

"""
Process Materials - Requires Basic Tailor or Apprentice Blacksmith
Craft Alloys - Requires Basic Tailor or Apprentice Blacksmith
Craft Items - Requires Daedalus' Protégé
Craft Equipment - Requires Basic Tailor or Apprentice Blacksmith
Craft Potions - Required Fledgling Alchemist
"""


def get_screen(console, screen_data):
    console.header_callback = get_town_header
    display_text = '\n\tWhat kind of crafting would you like to do?\n'
    _options = {'0': BACK}

    display_text += f'\n\t{OPT_C}1:{END_OPT_C} Process Materials'
    if not Refs.gc.has_perk('basic_tailor') and not Refs.gc.has_perk('apprentice_blacksmith'):
        display_text += ' - LOCKED'
    else:
        _options['1'] = f'{CRAFTING_PROCESS_MATERIALS}:0'
    display_text += f'\n\t{OPT_C}2:{END_OPT_C} Craft Alloys'
    if not Refs.gc.has_perk('apprentice_blacksmith'):
        display_text += ' - LOCKED'
    else:
        _options['2'] = f'{CRAFTING_ALLOYS}:0'
    display_text += f'\n\t{OPT_C}3:{END_OPT_C} Craft Items'
    if not Refs.gc.has_perk('daedalus_protege'):
        display_text += ' - LOCKED'
    else:
        _options['3'] = f'{CRAFTING_ITEMS}:0'
    display_text += f'\n\t{OPT_C}4:{END_OPT_C} Craft Equipment'
    if not Refs.gc.has_perk('reputable_tailor') and not Refs.gc.has_perk('skilled_blacksmith'):
        display_text += ' - LOCKED'
    else:
        _options['4'] = f'{CRAFTING_EQUIPMENT}:0'
    display_text += f'\n\t{OPT_C}5:{END_OPT_C} Craft Potions'
    if not Refs.gc.has_perk('fledgling_alchemist'):
        display_text += ' - LOCKED'
    else:
        _options['5'] = f'{CRAFTING_POTIONS}:0'

    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} back\n'
    return display_text, _options


def handle_action(console, action):
    console.set_screen(action, True)
