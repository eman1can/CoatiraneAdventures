from refs import END_OPT_C, OPT_C, Refs
from text.screens.common_functions import item_page_list
from text.screens.screen_names import BACK, INVENTORY_BATTLE, INVENTORY_BATTLE_SELECT


def get_inventory_battle_item(item, index, current_text, page_name, page_num):
    if item.is_single():
        name, desc, price = item.get_display()
        count_string = ''
    else:
        name, desc, min_price, max_price = item.get_display()
        count = Refs.gc.get_floor_data().get_gained_items()[item]
        count_string = f'\n\tHave: {count}'
    if item.is_potion():
        return f'\n\t{name} - Use: {OPT_C}{index}{END_OPT_C}\n\t\t- ' + desc.replace('\n', '\n\t\t- ') + count_string + f'\n', f'use#{item.get_id()}'
    else:
        return f'\n\t{name}\n\t\t- ' + desc.replace('\n', '\n\t\t- ') + count_string + f'\n', ''


def get_screen(console, screen_data):
    console.header_callback = None
    item_list = list(Refs.gc.get_floor_data().get_gained_items().keys())
    item_list += Refs.gc.get_potions()

    page_num = int(screen_data)

    fail = '\n\tYou have no items in your inventory.'

    ip_text, ip_options = item_page_list(1, INVENTORY_BATTLE, page_num, item_list, fail, '', get_inventory_battle_item)

    _options = {'0': BACK}
    _options.update(ip_options)
    display_text = ip_text

    inventory = Refs.gc.get_inventory()
    pickaxe = inventory.get_current_pickaxe()
    shovel = inventory.get_current_shovel()
    harvesting_knife = inventory.get_current_harvesting_knife()
    option_index = len(_options)

    if pickaxe is None:
        display_text += f'\n\n\t{OPT_C}{option_index}:{END_OPT_C} Current Pickaxe: None'
        _options[str(option_index)] = f'{INVENTORY_BATTLE_SELECT}:0#pickaxe#none'
    else:
        display_text += f'\n\n\t{OPT_C}{option_index}:{END_OPT_C} Current Pickaxe: {pickaxe.get_name()}'
        _options[str(option_index)] = f'{INVENTORY_BATTLE_SELECT}:0#pickaxe#{pickaxe.get_full_id()}'
    option_index += 1

    if shovel is None:
        display_text += f'\n\t{OPT_C}{option_index}:{END_OPT_C} Current Shovel: None'
        _options[str(option_index)] = f'{INVENTORY_BATTLE_SELECT}:0#shovel#none'
    else:
        display_text += f'\n\t{OPT_C}{option_index}:{END_OPT_C} Current Shovel: {shovel.get_name()}'
        _options[str(option_index)] = f'{INVENTORY_BATTLE_SELECT}:0#shovel#{shovel.get_full_id()}'
    option_index += 1
    if harvesting_knife is None:
        display_text += f'\n\t{OPT_C}{option_index}:{END_OPT_C} Current Harvesting Knife: None'
        _options[str(option_index)] = f'{INVENTORY_BATTLE_SELECT}:0#harvesting_knife#none'
    else:
        display_text += f'\n\t{OPT_C}{option_index}:{END_OPT_C} Current Harvesting Knife: {harvesting_knife.get_name()}'
        _options[str(option_index)] = f'{INVENTORY_BATTLE_SELECT}:0#harvesting_knife#{harvesting_knife.get_full_id()}'

    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} back\n'
    return display_text, _options


def handle_action(console, action):
    if action.startswith('use'):
        pass
    else:
        console.set_screen(action)
