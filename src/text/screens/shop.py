from math import ceil, floor

from refs import END_OPT_C, OPT_C, Refs
from text.screens.town import get_town_header


def get_item_string(item, index, current_text, page_name, page_num):
    if item.is_single():
        # Single item string
        name, desc, price = item.get_display()
        if Refs.gc.in_inventory(item.get_id()):
            return f'\n\t[s]{OPT_C}{index}:{END_OPT_C} {name}[/s] - Already purchased\n', None
        elif item.is_unlocked():
            return f'\n\t{OPT_C}{index}:{END_OPT_C} {name}\n\t\t- ' + desc.replace('\n', '\n\t\t- ') + f'\n\t{current_text}: {price}V\n', f'{page_name}_page{page_num}_confirm1#{item.get_id()}'
        return '', None
    else:
        # Multi item item string
        name, desc, min_price, max_price = item.get_display()
        if 'sell' in page_name:
            count = Refs.gc.get_inventory_count(item.get_id())
        else:
            count = min(floor(Refs.gc.get_varenth() / max_price), 50)
        return f'\n\t{OPT_C}{index}:{END_OPT_C} {name}\n\t\t- ' + desc.replace('\n', '\n\t\t- ') + f'\n\t{current_text}: {min_price}V\n\tIn Inventory: {count}\n', f'{page_name}_page{page_num}_{max(int(count / 2), 1)}#{item.get_id()}'


def item_page_list(option_index, page_name, page_num, item_list, fail_text, current_text, item_string_function=get_item_string):
    display_text, _options = '', {}

    arrow_text = ''
    if len(item_list) > 5:
        # We want to enable pages of items...
        left = page_num != 0
        right = page_num != ceil(len(item_list) / 5) - 1

        left_string = f'{OPT_C}{option_index}{END_OPT_C} Prev Page'
        right_string = f'Next Page {OPT_C}{option_index + 1}{END_OPT_C}'

        if left:
            _options[str(option_index)] = f'{page_name}{page_num - 1}page'
        else:
            left_string = f'[s]{left_string}[/s]'

        if right:
            _options[str(option_index + 1)] = f'{page_name}{page_num + 1}page'
        else:
            right_string = f'[s]{right_string}[/s]'

        arrow_text = f'\n\t←──── {left_string} | {right_string} ────→'

        item_list = item_list[page_num * 5:(page_num + 1) * 5]
        option_index = page_num * 5 + 2 + option_index
    elif len(item_list) == 0:
        display_text += fail_text

    for item in item_list:
        # Get item display string if it exists
        item_text, item_option = item_string_function(item, option_index, current_text, page_name, page_num)

        display_text += item_text
        if item_option is not None:
            _options[str(option_index)] = item_option
        option_index += 1

    display_text += arrow_text

    return display_text, _options


def item_transaction(item_count, item_id, page_name, current_text, future_text):
    item = Refs.gc.get_drop_item(item_id)
    if 'sell' in page_name:
        count = Refs.gc.get_inventory_count(item_id)
    else:
        count = min(floor(Refs.gc.get_varenth() / item.get_max_price()), 50)
    _options = {}

    display_text = f'\n\t{current_text}: {item.get_min_price()}V\n'
    arrow_string = f'\n\t 1  ←───────→ {count}'
    display_text += f'{int(item_count)}'.center(len(arrow_string))
    display_text += f'\n\t{arrow_string}\n\n'
    display_text += f'\n\t{future_text}: {int(item_count) * item.get_min_price()}V\n'

    option_index = 1
    for (threshold, new_number, option_string) in [(count, count, 'All'), (max(int(count / 2), 1), max(int(count / 2), 1), 'Half'), (1, 1, 'One'), (count, int(item_count) + 1, 'More'), (1, int(item_count) - 1, 'Less')]:
        if int(item_count) == threshold:
            display_text += f'\n\t[s]{OPT_C}{option_index}:{END_OPT_C} {option_string}[/s]'
        else:
            display_text += f'\n\t{OPT_C}{option_index}:{END_OPT_C} {option_string}'
            _options[str(option_index)] = f'{page_name}_{new_number}#{item_id}'
        option_index += 1

    display_text += f'\n\t{OPT_C}{option_index}:{END_OPT_C} Confirm'
    _options[str(option_index)] = f'{page_name}_confirm{item_count}#{item_id}'
    return display_text, _options


def bspage_list(sub_categories, page_name, id_to_string):
    display_text, option_index, _options = '', 1, {}

    for sub_category in sub_categories:
        for type in ['sell', 'buy']:
            display_text += f'\n\t{OPT_C}{option_index}:{END_OPT_C} {type.title()} {id_to_string[sub_category]}s'
            _options[str(option_index)] = f'shop_{sub_category}_{type}0page'
            option_index += 1
    return display_text, _options


def shop(console):
    display_text = get_town_header()
    display_text += '\n\t'
    _options = {'0': 'back'}

    pages = {'main': ['general', 'dungeon_materials', 'ingredients', 'potions_medicines', 'equipment', 'home_supplies', 'other'],
             'general': ['floor_maps'],
             'dungeon_materials': [],
             'magic_stones': [],
             'monster_drops': [],
             'raw_materials': [],
             'processed_materials': [],
             'floor_maps': [f'floor_{floor_id}' for floor_id in range(1, min(len(Refs.gc['floors']), Refs.gc.get_lowest_floor()) + 1)]}

    # Header dsplay options
    headers = {'main': 'Welcome to the Guild Shopping District where you can find anything you need!\n\t',
               'general': 'Welcome to the General shop! Your premier provider of useful goods.\n\t',
               'floor_maps': 'Welcome to the map shop! As an extension of the guild, we have all the latest maps available!\n\t',}

    # Sub header display options
    sub_headers = {'main':    'Where you you like to browse today?\n',
               'general': 'What would you like to purchase?\n',
               'floor_maps': 'Which floor are you interested in?\n',
               'dungeon_materials': 'Which type of transaction would you like?\n'}

    # The Names to display for page links
    page_to_string = {'general': 'General Goods',
                      'dungeon_materials': 'Dungeon Materials',
                      'ingredients': 'Ingredients',
                      'potions_medicines': 'Potions & Medicines',
                      'equipment': 'Equipment',
                      'home_supplies': 'Home Supplies',
                      'other': 'Other',
                      'floor_maps': 'Floor Maps',
                      'monster_drops': 'Monster Drop',
                      'magic_stones':  'Magic Stone',
                      'raw_materials': 'Raw Materials',
                      'processed_materials': 'Processed Materials'}

    # Sub categories that should have a Buy and Sell option listed
    bspages = {'dungeon_materials': ['magic_stones', 'monster_drops', 'raw_materials', 'processed_materials']}

    item_lists = {'general': Refs.gc.get_shop_items,
                  'magic_stones': lambda category: Refs.gc.get_magic_stone_types(),
                  'monster_drops': lambda category: Refs.gc.get_monster_drop_types(),
                  'raw_materials': lambda category: Refs.gc.get_raw_materials(),
                  'processed_materials': lambda category: Refs.gc.get_processed_materials()}

    for floor_id in range(1, min(len(Refs.gc['floors']), Refs.gc.get_lowest_floor()) + 1):
        pages[f'floor_{floor_id}'] = []
        headers[f'floor_{floor_id}'] = 'Which map type are you interested in?\n'
        page_to_string[f'floor_{floor_id}'] = f'Floor {floor_id}'
        item_lists[f'floor_{floor_id}'] = Refs.gc.get_shop_items

    texts = {
        'sell_start': 'Which of your {0}s would you like to sell?\n',
        'sell_fail': '\n\tYou do not have any {0}s that you can sell.',
        'sell_current': 'Current going price',
        'sell_future': 'You will get',
        'buy_start':   'What type of {0} would you like to buy?\n',
        'buy_fail':    '\n\tNo items are available to purchase',  # \n\tYou are not eligible to purchase any floor maps.\n\tYou must visit the floor before you can purchase a map for it.
        'buy_current': 'Current price',
        'buy_future':  'This will cost'
    }

    current_screen_name = console.get_current_screen()
    header, sub_header, sub_text, option_index, sub_options = '', '', '', 1, {}

    # Add sub pages (aka floors)
    for page, page_list in pages.items():
        if current_screen_name.startswith(f'shop_{page}'):
            # Get sub pages that go on this page; Can be on pages w/ lists too
            if page in headers:
                header = headers[page]
            if page in sub_headers:
                sub_header = sub_headers[page]
            for page_link in page_list:
                sub_text += f'\n\t{OPT_C}{option_index}:{END_OPT_C} {page_to_string[page_link]}'
                if page_link in item_lists.keys():
                    sub_options[str(option_index)] = f'shop_{page_link}0page'
                else:
                    sub_options[str(option_index)] = f'shop_{page_link}'
                option_index += 1

            # Add Buy & Sell category page links
            if page in bspages:
                ip_text, ip_options = bspage_list(bspages[page], f'shop_{page}', page_to_string)

                # Add to current page
                sub_text += ip_text
                sub_options.update(ip_options)

            # If ends with page, then we have a list of items
            if 'page' in current_screen_name and '#' not in current_screen_name:
                # Divide page links from lists
                if sub_text != '':
                    sub_text += '\n'

                # The item list will stay the same, whether buy or sell
                item_list = item_lists[page](page)

                if 'buy' in current_screen_name:
                    page += '_buy'
                elif 'sell' in current_screen_name:
                    page += '_sell'
                    # Restrict to item_list that we have in inventory
                    item_list = Refs.gc.get_owned_items(item_list)

                # Page with a list in it
                print(current_screen_name)
                page_num = int(current_screen_name[len(f'shop_{page}'):-len('page')])

                if 'buy' in page:
                    sub_header = texts['buy_start'].format(page_to_string[page[:-4]])
                    ip_text, ip_options = item_page_list(option_index, f'shop_{page}', page_num, item_list, texts['buy_fail'], texts['buy_current'])
                elif 'sell' in page:
                    sub_header = texts['sell_start'].format(page_to_string[page[:-5]])
                    ip_text, ip_options = item_page_list(option_index, f'shop_{page}', page_num, item_list, texts['sell_fail'].format(page_to_string[page[:-5]]), texts['sell_current'])
                else:
                    ip_text, ip_options = item_page_list(option_index, f'shop_{page}', page_num, item_list, texts['buy_fail'], texts['buy_current'])

                # Buy or Sell page with a list in it
                #sub_header = texts[f'{type}_start'].format(category_to_string[sub_category])
                #sub_text, sub_options = item_page_list(current_screen_name, item_list, sub_page_name, texts[f'{type}_fail'].format(category_to_string[sub_category]), texts[f'{type}_current'])

                # Add to current page
                sub_text += ip_text
                sub_options.update(ip_options)
            # If there is a # in the string, then we have a item transaction screen
            if '#' in current_screen_name:
                # Item transaction screen
                if 'sell' in current_screen_name:
                    page += '_sell'
                    page_type = 'sell'
                else:
                    page += '_buy'
                    page_type = 'buy'

                page_data, item_id = current_screen_name[len(f'shop_{page}_page'):].split('#')
                page_num, item_count = page_data.split('_')
                sub_header = texts[f'{page_type}_start'].format(Refs.gc.get_drop_item(item_id).get_name())
                sub_text, sub_options = item_transaction(item_count, item_id, f'shop_{page}{page_num}page', texts[f'{page_type}_current'], texts[f'{page_type}_future'])
            break

    # shop_category_pagex_count#item_id
    # Add paged shop lists
    # for category, sub_categories in bscategories.items():
    #     # List sub categories
    #     if f'shop_{category}' == current_screen_name:
    #         sub_header = 'Which type of transaction would you like?\n'
    #         sub_text, sub_options = get_sub_category_page(sub_categories, f'shop_{category}', category_to_string)
    #     else:
    #         # Detect pages list from sub_category
    #         for sub_category in sub_categories:
    #             for type in ['sell', 'buy']:
    #                 sub_page_name = f'shop_{category}_{type}_{sub_category}'
    #                 if current_screen_name.startswith(sub_page_name):
    #                     if current_screen_name.endswith('page'):
    #                         item_list = item_lists[sub_category]()
    #
    #                         # When selling, we need to be restricted to inventory
    #                         if type == 'sell':
    #                             remove = []
    #                             for item in item_list:
    #                                 if Refs.gc.get_inventory_count(item.get_id()) <= 0:
    #                                     remove.append(item)
    #                             for item in remove:
    #                                 item_list.remove(item)
    #                             del remove
    #
    #                         sub_header = texts[f'{type}_start'].format(category_to_string[sub_category])
    #                         sub_text, sub_options = item_page_list(current_screen_name, item_list, sub_page_name, texts[f'{type}_fail'].format(category_to_string[sub_category]), texts[f'{type}_current'])
    #                     else:


    display_text += header
    display_text += sub_header
    display_text += sub_text
    _options.update(sub_options)

    if current_screen_name == 'shop_main':
        display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} Leave the market\n'
    else:
        display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} back\n'
    return display_text, _options


def do_transaction(item_id, count, selling):
    item = Refs.gc.get_shop_item(item_id)
    if item is None:
        item = Refs.gc.get_drop_item(item_id)
    if not selling:
        # Check if we have enough money
        print(item.get_name(), item.get_max_price(), ' - ', Refs.gc.get_varenth())
        if item.get_max_price() > Refs.gc.get_varenth():
            return False

    # Adjust inventory
    if selling:
        Refs.gc.remove_from_inventory(item_id, count)
    else:
        Refs.gc.add_to_inventory(item_id, count)

    # Adjust Varenth
    if selling:
        Refs.gc.update_varenth(item.get_min_price() * count)
    else:
        Refs.gc.update_varenth(-item.get_max_price() * count)

    # If map, update map data
    if item_id.startswith('full_map') and not Refs.gc.in_inventory('path_' + item_id[len('full_'):]):
        Refs.gc.add_to_inventory('path_' + item_id[len('full_'):])
    if item_id.startswith('path_map'):
        floor_id = int(item_id[len('path_map_floor_'):])
        Refs.gc.get_floor(floor_id).get_floor_map().unlock_path_map()
    elif item_id.startswith('full_map'):
        floor_id = int(item_id[len('full_map_floor_'):])
        Refs.gc.get_floor(floor_id).get_floor_map().unlock_full_map()
    return True
