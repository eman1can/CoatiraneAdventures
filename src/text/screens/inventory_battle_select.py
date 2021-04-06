from refs import END_OPT_C, OPT_C, Refs
from text.screens.common_functions import item_page_list
from text.screens.screen_names import BACK, INVENTORY_BATTLE_SELECT


def get_screen(console, screen_data):
    console.header_callback = None
    display_text = ''

    page_num, key, item_id = screen_data.split('#', 2)
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
    _options = {'0': BACK}
    if current_item is not None:
        display_text += f'\n\tCurrent selected: {current_item.get_name()}\n\t\tDurability: {current_item.get_current_durability()} / {current_item.get_durability()}\n\t{OPT_C}1:{END_OPT_C} Deselect\n'
        _options['1'] = f'set#{page_num}#{key}#none'
        option_index += 1

    ip_text, ip_options = item_page_list(option_index, f'set#{page_num}#{key}', page_num, item_list, fail, '', get_inventory_select_item)

    _options.update(ip_options)
    display_text += ip_text

    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} back\n'
    return display_text, _options


def handle_action(console, action):
    if action.startswith('set'):
        page_num, key, item_id = action.split('#', 2)
        page_num = int(page_num)

        item_hash = None
        if item_id != 'none':
            item_id, item_hash = item_id.split('#')
            item_hash = int(item_hash)

        inventory = Refs.gc.get_inventory()

        if item_id == 'pickaxe':
            item = inventory.set_current_pickaxe(item_hash)
        elif item_id == 'shovel':
            item = inventory.set_current_shovel(item_hash)
        else:
            item = inventory.set_current_harvesting_knife(item_hash)
        if item is None:
            console.set_screen(f'{INVENTORY_BATTLE_SELECT}:{key}*{page_num}#none')
        else:
            console.set_screen(f'{INVENTORY_BATTLE_SELECT}:{key}*{page_num}#{item.get_full_id()}')


def get_inventory_select_item(item, index, current_text, page_name, page_num):
    return f'\n\t{item.get_name()}\n\t\t- Durability: {item.get_current_durability()} / {item.get_durability()}\n\t\t{OPT_C}{index}:{END_OPT_C} Select', f'{page_name}#{item.get_full_id()}'
