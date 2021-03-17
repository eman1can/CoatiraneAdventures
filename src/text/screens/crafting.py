from refs import END_OPT_C, OPT_C, Refs
from text.screens.town import get_town_header


# Crafting General
# - Process Soft materials
# - Craft using soft materials
# Crafting Potions
# - Craft Potion
#   - Try to find new potion recipe
#   - Craft Known Potion
# Forging
# - Process Hard Materials
# - Crafting using hard materials

def crafting_main(console):
    display_text = get_town_header()
    display_text += '\n\tWhat kind of crafting would you like to do?\n'
    display_text += f'\n\t{OPT_C}1:{END_OPT_C} Process Soft Materials'
    display_text += f'\n\t{OPT_C}2:{END_OPT_C} Craft Using Soft Materials'
    display_text += f'\n\t{OPT_C}3:{END_OPT_C} Craft Potions'
    if Refs.gc.is_potion_crafting_locked():
        display_text += ' - LOCKED'
    display_text += f'\n\t{OPT_C}4:{END_OPT_C} Process Hard Materials'
    if Refs.gc.is_blacksmithing_locked():
        display_text += ' - LOCKED'
    display_text += f'\n\t{OPT_C}5:{END_OPT_C} Craft Using Hard Materials'
    if Refs.gc.is_blacksmithing_locked():
        display_text += ' - LOCKED'
    _options = {
        '0': 'back',
        '1': 'crafting_process_soft',
        '2': 'crafting_equipment_soft',
        '3': 'crafting_potions',
        '4': 'crafting_process_hard',
        '5': 'crafting_equipment_hard'
    }
    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} back\n'
    return display_text, _options


def crafting_general(console):
    pass