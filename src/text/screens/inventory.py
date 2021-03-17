from refs import END_OPT_C, OPT_C, Refs
from text.screens.shop import item_page_list
from text.screens.town import get_town_header


def get_inventory_item(item, index, current_text, page_name, page_num):
    if item.is_single():
        name, desc, price = item.get_display()
        count_string = ''
    else:
        name, desc, min_price, max_price = item.get_display()
        count = Refs.gc.get_inventory_count(item.get_id())
        count_string = f'\n\tHave: {count}'
    return f'\n\t{name}\n\t\t- ' + desc.replace('\n', '\n\t\t- ') + count_string + '\n', {}


def inventory(console):
    display_text = get_town_header()
    item_list = Refs.gc.get_inventory_list()

    page_num = int(console.get_current_screen()[len('inventory'):-len('page')])

    fail = '\n\tYou have no items in your inventory.'

    ip_text, ip_options = item_page_list(1, 'inventory', page_num, item_list, fail, '', get_inventory_item)

    _options = {'0': 'back'}
    _options.update(ip_options)
    display_text += ip_text + f'\n\n\t{OPT_C}0:{END_OPT_C} back\n'
    return display_text, _options
