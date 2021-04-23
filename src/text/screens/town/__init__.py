from math import floor

from kivy.clock import Clock

from refs import END_OPT_C, OPT_C, RED_C, Refs
from text.screens.screen_names import ALMANAC_MAIN, CRAFTING_MAIN, DUNGEON_MAIN, HOUSING_MAIN, INVENTORY, NEW_GAME, PROFILE_MAIN, QUESTS_MAIN, SHOP_MAIN, TAVERN_MAIN, TOWN_MAIN


def get_town_header(console):
    name = Refs.gc.get_name()
    domain = Refs.gc.get_domain()
    renown = Refs.gc.get_renown()
    varenth = Refs.gc.format_number(int(Refs.gc.get_varenth()))
    skill_level = Refs.gc.get_skill_level()

    time = Refs.gc.get_time()
    width = console.get_width()
    sides = floor(width * 0.05)
    first_string = f'{name} - {domain} - Perks Unlocked {skill_level}'
    if Refs.gc.get_inventory().has_item('pocket_watch'):
        second_string = f'{time} - {varenth} Varenth - Renown {renown}'
    else:
        second_string = f'{varenth} Varenth - Renown {renown}'
    return '\n' + first_string.rjust(sides + len(first_string)) + ''.center(width - sides * 2 - len(first_string) - len(second_string)) + second_string.ljust(sides + len(second_string)) + '\n'


def get_screen(console, screen_data):
    console.header_callback = get_town_header
    display_text = '\n\tYou are currently in the town center.\n\tWhere would you like to go?\n'
    if Refs.gc.get_housing().get_bill_due() < 0:
        display_text += f'\n\t{RED_C}Your housing bill is overdue!{END_OPT_C}\n'
    elif Refs.gc.get_housing().get_bill_due() < 5:
        display_text += f'\n\t{RED_C}Your housing bill is due in {Refs.gc.get_housing().bill_due()} days.{END_OPT_C}\n'
    display_text += f'\n\t{OPT_C}0:{END_OPT_C} Tavern'
    if Refs.gc.is_tavern_locked():
        display_text += ' - LOCKED'
    display_text += f'\n\t{OPT_C}1:{END_OPT_C} Shop'
    display_text += f'\n\t{OPT_C}2:{END_OPT_C} Quests'
    display_text += f'\n\t{OPT_C}3:{END_OPT_C} Crafting'
    if Refs.gc.is_crafting_locked():
        display_text += ' - LOCKED'
    display_text += f'\n\t{OPT_C}4:{END_OPT_C} Inventory'
    display_text += f'\n\t{OPT_C}5:{END_OPT_C} Your profile'
    display_text += f'\n\t{OPT_C}6:{END_OPT_C} Housing'
    display_text += f'\n\t{OPT_C}7:{END_OPT_C} Almanac\n'
    display_text += f'\n\t{OPT_C}8:{END_OPT_C} Dungeon\n'
    display_text += f'\n\n\t{OPT_C}9:{END_OPT_C} Save Game\n'
    display_text += f'\t{OPT_C}10:{END_OPT_C} Exit to Main Menu\n'
    _options = {
        '0': TAVERN_MAIN,
        '1': SHOP_MAIN + ':main',
        '2': QUESTS_MAIN,
        '3': CRAFTING_MAIN,
        '4': INVENTORY + ':0',
        '5': PROFILE_MAIN,
        '6': HOUSING_MAIN,
        '7': ALMANAC_MAIN,
        '8': DUNGEON_MAIN,
        '9': 0,
        '10': 1
    }
    return display_text, _options


def handle_action(console, action):
    if action == 0:
        console.text = '\n\tSaving Game...'
        Clock.schedule_once(lambda dt: Refs.gc.save_game(lambda: console.set_screen(TOWN_MAIN, False)), 0.5)
    elif action == 1:
        console.text = '\n\tSaving Game...'
        console.loading_progress = {}
        Refs.app.reset_loader()
        Clock.schedule_once(lambda dt: Refs.gc.save_game(lambda: console.set_screen(NEW_GAME, False)), 0.5)
    else:
        # Check Tavern and Crafting Locks
        if action == CRAFTING_MAIN:
            if Refs.gc.is_crafting_locked():
                console.error_time = 2.5
                console.error_text = 'You need an adventurer with a crafting perk.'
                return
        elif action == TAVERN_MAIN:
            if Refs.gc.is_tavern_locked():
                console.error_time = 2.5
                console.error_text = 'You need at least 20k Varenth and Renown of H to visit the tavern.'
                return
        console.set_screen(action, True)
