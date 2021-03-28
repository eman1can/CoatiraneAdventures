from refs import END_OPT_C, OPT_C, Refs
from text.screens.shop import item_page_list
from text.screens.town import get_town_header


def get_inventory_item(item, index, current_text, page_name, page_num):
    if item.is_single():
        name, desc, price = item.get_display()
        count_string = ''
    else:
        name, desc, min_price, max_price = item.get_display()
        count = Refs.gc.get_inventory().get_item_count(item.get_id())
        count_string = f'\n\tHave: {count}'
    return f'\n\t{name}\n\t\t- ' + desc.replace('\n', '\n\t\t- ') + count_string + '\n', ''


def get_inventory_battle_item(item, index, current_text, page_name, page_num):
    if item.is_single():
        name, desc, price = item.get_display()
        count_string = ''
    else:
        name, desc, min_price, max_price = item.get_display()
        count = Refs.gc.get_inventory().get_item_count(item.get_id())
        count_string = f'\n\tHave: {count}'
    return f'\n\t{name} - Use: {OPT_C}{index}{END_OPT_C}\n\t\t- ' + desc.replace('\n', '\n\t\t- ') + count_string + f'\n', f'inventory_battle_use_{item.get_id()}'


def get_inventory_select_item(item, index, current_text, page_name, page_num):
    name = item.get_name()

    return f'\n\t{name}\n\t\t- Durability: {item.get_current_durability()} / {item.get_durability()}\n\t\t{OPT_C}{index}:{END_OPT_C} Select', f'{page_name}#{item.get_full_id()}'


def inventory(console):
    console.header_callback = get_town_header
    item_list = Refs.gc.get_inventory().get_items()

    page_name, page_num = console.get_current_screen().split('*')
    page_num = int(page_num)

    fail = '\n\tYou have no items in your inventory.'

    ip_text, ip_options = item_page_list(1, 'inventory', page_num, item_list, fail, '', get_inventory_item)

    _options = {'0': 'back'}
    _options.update(ip_options)
    display_text = ip_text + f'\n\n\t{OPT_C}0:{END_OPT_C} back\n'
    return display_text, _options


def inventory_battle(console):
    console.header_callback = None
    item_list = list(Refs.gc.get_floor_data().get_gained_items().keys())
    item_list += Refs.gc.get_potions()

    page_name, page_num = console.get_current_screen().split('*')
    page_num = int(page_num)

    fail = '\n\tYou have no items in your inventory.'

    ip_text, ip_options = item_page_list(1, 'inventory_battle', page_num, item_list, fail, '', get_inventory_battle_item)

    _options = {'0': 'back'}
    _options.update(ip_options)
    display_text = ip_text

    inventory = Refs.gc.get_inventory()
    pickaxe = inventory.get_current_pickaxe()
    shovel = inventory.get_current_shovel()
    harvesting_knife = inventory.get_current_harvesting_knife()
    option_index = len(_options)

    if pickaxe is None:
        display_text += f'\n\n\t{OPT_C}{option_index}:{END_OPT_C} Current Pickaxe: None'
        _options[str(option_index)] = f'inventory_battle_select*0#pickaxe#none'
    else:
        display_text += f'\n\n\t{OPT_C}{option_index}:{END_OPT_C} Current Pickaxe: {pickaxe.get_name()}'
        _options[str(option_index)] = f'inventory_battle_select*0#pickaxe#{pickaxe.get_full_id()}'
    option_index += 1

    if shovel is None:
        display_text += f'\n\t{OPT_C}{option_index}:{END_OPT_C} Current Shovel: None'
        _options[str(option_index)] = f'inventory_battle_select*0#shovel#none'
    else:
        display_text += f'\n\t{OPT_C}{option_index}:{END_OPT_C} Current Shovel: {shovel.get_name()}'
        _options[str(option_index)] = f'inventory_battle_select*0#shovel#{shovel.get_full_id()}'
    option_index += 1
    if harvesting_knife is None:
        display_text += f'\n\t{OPT_C}{option_index}:{END_OPT_C} Current Harvesting Knife: None'
        _options[str(option_index)] = f'inventory_battle_select*0#harvesting_knife#none'
    else:
        display_text += f'\n\t{OPT_C}{option_index}:{END_OPT_C} Current Harvesting Knife: {harvesting_knife.get_name()}'
        _options[str(option_index)] = f'inventory_battle_select*0#harvesting_knife#{harvesting_knife.get_full_id()}'

    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} back\n'
    return display_text, _options


def inventory_battle_select(console):
    console.header_callback = None
    display_text = ''

    page_data, key, item_id = console.get_current_screen().split('#', 2)
    page_name, page_num = page_data.split('*')
    page_num = int(page_num)

    inventory = Refs.gc.get_inventory()
    item_list = inventory.get_metadata_items(key)

    current_item = None
    if item_id != 'none':
        for index in range(len(item_list)):
            if item_list[index].get_full_id() == item_id:
                current_item = item_list.pop(index)
                break

    fail = '\n\tYou have no items in your inventory.'
    option_index = 1
    _options = {'0': 'back'}
    if current_item is not None:
        display_text += f'\n\tCurrent selected: {current_item.get_name()}\n\t\tDurability: {current_item.get_current_durability()} / {current_item.get_durability()}\n\t{OPT_C}1:{END_OPT_C} Deselect\n'
        _options['1'] = f'inventory_battle_set*{page_num}#{key}#none'
        option_index += 1

    ip_text, ip_options = item_page_list(option_index, f'inventory_battle_set*{page_num}#{key}', page_num, item_list, fail, '', get_inventory_select_item)

    _options.update(ip_options)
    display_text += ip_text

    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} back\n'
    return display_text, _options
