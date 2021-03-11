from refs import Refs

OPT_C = '[color=#CA353E]'
END_OPT_C = '[/color]'


def get_town_header():
    # Return a string that contains Name, Varenth and current Renown
    # 165 is the width of the screen, approximately
    name = Refs.gc.get_name()
    domain = Refs.gc.get_domain()
    renown = Refs.gc.get_renown()
    varenth = Refs.gc.get_varenth()
    skill_level = Refs.gc.get_skill_level()
    return '\n' + f'{name} - {domain} - Skill Level {skill_level}'.rjust(40).ljust(110) + f'{varenth} Varenth - Renown {renown}'.ljust(30).rjust(55) + '\n'


def town_main(console):
    display_text = get_town_header()
    display_text += '\n\tYou are currently in the town center.\n\tWhere would you like to go?\n'
    display_text += f'\n\t{OPT_C}0:{END_OPT_C} Tavern'
    if Refs.gc.is_tavern_locked():
        display_text += ' - LOCKED'
    display_text += f'\n\t{OPT_C}1:{END_OPT_C} Shop'
    display_text += f'\n\t{OPT_C}2:{END_OPT_C} Quests'
    display_text += f'\n\t{OPT_C}3:{END_OPT_C} Crafting'
    if Refs.gc.is_crafting_locked():
        display_text += ' - LOCKED'
    display_text += f'\n\t{OPT_C}4:{END_OPT_C} Inventory\n'
    display_text += f'\n\t{OPT_C}5:{END_OPT_C} Dungeon\n'
    _options = {'0': 'tavern_main', '1': 'shop_main', '2': 'quests_main', '3': 'crafting_main', '4': 'inventory_main', '5': 'dungeon_main'}
    return display_text, _options


def tavern_main(console):
    display_text = get_town_header()
    _options = {'0': 'back'}
    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} back\n'
    return display_text, _options


def quests_main(console):
    display_text = get_town_header()
    _options = {'0': 'back'}
    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} back\n'
    return display_text, _options


def crafting_main(console):
    display_text = get_town_header()
    _options = {'0': 'back'}
    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} back\n'
    return display_text, _options


def inventory_main(console):
    display_text = get_town_header()
    _options = {'0': 'back'}
    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} back\n'
    return display_text, _options
