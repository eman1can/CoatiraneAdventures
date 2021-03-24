from refs import END_OPT_C, OPT_C, Refs
from text.screens.town import get_town_header

"""
Process Materials - Requires Basic Tailor or Apprentice Blacksmith
Craft Alloys - Requires Apprentice Blacksmith
Craft Items - Requires Daedalus' Protégé
Craft Equipment - Requires Basic Tailor or Apprentice Blacksmith
Craft Potions - Required Fledgling Alchemist
"""


def crafting_main(console):
    display_text = get_town_header()
    display_text += '\n\tWhat kind of crafting would you like to do?\n'
    _options = {'0': 'back'}

    display_text += f'\n\t{OPT_C}1:{END_OPT_C} Process Materials'
    if not Refs.gc.has_perk('basic_tailor') and not Refs.gc.has_perk('apprentice_blacksmith'):
        display_text += ' - LOCKED'
    else:
        _options['1'] = 'crafting_process_materials'
    display_text += f'\n\t{OPT_C}2:{END_OPT_C} Craft Alloys'
    if not Refs.gc.has_perk('apprentice_blacksmith'):
        display_text += ' - LOCKED'
    else:
        _options['2'] = 'crafting_alloys'
    display_text += f'\n\t{OPT_C}3:{END_OPT_C} Craft Items'
    if not Refs.gc.has_perk('daedalus_protege'):
        display_text += ' - LOCKED'
    else:
        _options['3'] = 'crafting_items'
    display_text += f'\n\t{OPT_C}4:{END_OPT_C} Craft Equipment'
    if not Refs.gc.has_perk('basic_tailor') and not Refs.gc.has_perk('apprentice_blacksmith'):
        display_text += ' - LOCKED'
    else:
        _options['4'] = 'crafting_equipment'
    display_text += f'\n\t{OPT_C}5:{END_OPT_C} Craft Potions'
    if not Refs.gc.has_perk('fledgling_alchemist'):
        display_text += ' - LOCKED'
    else:
        _options['5'] = 'crafting_items'

    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} back\n'
    return display_text, _options


def crafting_process_materials(console):
    pass