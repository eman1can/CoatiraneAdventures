from math import floor

from game.equipment import EQUIPMENT_TOOL, EQUIPMENT_TYPES, EQUIPMENT_WEAPON
from refs import END_OPT_C, OPT_C, Refs
from text.screens.common_functions import item_page_list
from text.screens.screen_names import BACK, SHOP_MAIN
from text.screens.town import get_town_header


def get_screen(console, screen_data):
    console.header_callback = get_town_header
    display_text = '\n\t'
    _options = {'0': BACK}

    pages = {
        'main':                ['general', 'dungeon_materials', 'ingredients', 'potions_medicines', 'equipment', 'home_supplies', 'other'],
        'general':             ['floor_maps'],
        'equipment':           ['tools', 'weapons', 'armors'],
        'tools':               [],
        'weapons':             [],
        'armors':               [],
        'dungeon_materials':   [],
        'magic_stones':        [],
        'monster_drops':       [],
        'raw_materials':       [],
        'processed_materials': [],
        'ingredients':         [],
        'potions_medicines':   [],
        'floor_maps':          [f'floor_{floor_id}' for floor_id in range(1, min(len(Refs.gc['floors']), Refs.gc.get_lowest_floor()) + 1)]
             }

    # Header dsplay options
    headers = {
        'main':       'Welcome to the Guild Shopping District where you can find anything you need!\n\t',
        'general':    'Welcome to the General shop! Your premier provider of useful goods.\n\t',
        'floor_maps': 'Welcome to the map shop! As an extension of the guild, we have all the latest maps available!\n\t',
        'equipment':  'Welcome to the equipment district!\n\t'
    }

    # Sub header display options
    sub_headers = {
        'main':              'Where you you like to browse today?\n',
        'equipment':         'What form of equipment are you looking for?\n',
        'tools':             'What kind of tool are you looking for?\n',
        'weapons':           'What kind of weapon are you looking for?\n',
        'armors':            'What kind of armor are you looking for?\n',
        'general':           'What would you like to purchase?\n',
        'floor_maps':        'Which floor are you interested in?\n',
        'dungeon_materials': 'Which type of transaction would you like?\n'
    }

    # The Names to display for page links
    page_to_string = {'general': 'General Goods',
                      'dungeon_materials': 'Dungeon Materials',
                      'ingredients': 'Ingredients',
                      'potions_medicines': 'Potions & Medicines',
                      'equipment': 'Equipment',
                      'tools': 'Tools',
                      'weapons': 'Weapons',
                      'armors': 'Armor',
                      'home_supplies': 'Home Supplies',
                      'other': 'Other',
                      'floor_maps': 'Floor Maps',
                      'monster_drops': 'Monster Drop',
                      'magic_stones':  'Magic Stone',
                      'raw_materials': 'Raw Material',
                      'processed_materials': 'Processed Material'}

    # Sub categories that should have a Buy and Sell option listed
    bspages = {'dungeon_materials': ['magic_stones', 'monster_drops', 'raw_materials', 'processed_materials']}

    item_lists = {
        'general':             Refs.gc.get_shop_items,
        'ingredients':         lambda category: Refs.gc.get_ingredients(),
        'magic_stones':        lambda category: Refs.gc.get_magic_stone_types(),
        'monster_drops':       lambda category: Refs.gc.get_monster_drop_types(),
        'raw_materials':       lambda category: Refs.gc.get_raw_materials(),
        'processed_materials': lambda category: Refs.gc.get_processed_materials()
    }

    if '#' in screen_data:
        page, page_data = screen_data.split('#', 1)
    else:
        page = screen_data
        page_data = ''
    header, sub_header, sub_text, option_index, sub_options = '', '', '', 1, {}

    if page == 'floor_maps':
        for floor_id in range(1, min(len(Refs.gc['floors']), Refs.gc.get_lowest_floor()) + 1):
            page_to_string[f'floor_{floor_id}'] = f'Floor {floor_id}'
    elif page.startswith('floor'):
        pages[page] = []
        headers[page] = 'Which map type are you interested in?\n'
        item_lists[page] = Refs.gc.get_shop_items

    if page in ['equipment', 'tools', 'weapons', 'armors']:
        for item_id, equipment_class in Refs.gc['equipment'].items():
            equipment_category = EQUIPMENT_TYPES[equipment_class.get_type()].lower() + 's'
            pages[equipment_category].append(item_id)
            page_to_string[item_id] = equipment_class.get_name()
            item_lists[item_id] = None
    elif page in Refs.gc['equipment']:
        list_links = {
            'tools':   lambda category, page_name=page: Refs.gc.get_store_tools(page_name),
            'weapons': lambda category, page_name=page: Refs.gc.get_store_weapons(page_name),
            'armors':  lambda category, page_name=page: Refs.gc.get_store_armor(page_name)
        }
        equipment_class = Refs.gc['equipment'][page]
        equipment_category = EQUIPMENT_TYPES[equipment_class.get_type()].lower() + 's'
        pages[page] = []
        headers[page] = f'What kind of {equipment_class.get_name()} are you interested in?\n\n'
        item_lists[page] = list_links[equipment_category]

    texts = {
        'sell_start':   'Which of your {0}s would you like to sell?\n',
        'sell_fail':    '\n\tYou do not have any {0}s that you can sell.',
        'sell_current': 'Current going price',
        'sell_future':  'You will get',
        'buy_start':    'What type of {0} would you like to buy?\n',
        'buy_fail':     '\n\tNo items are available to purchase',  # \n\tYou are not eligible to purchase any floor maps.\n\tYou must visit the floor before you can purchase a map for it.
        'buy_current':  'Current price',
        'buy_future':   'This will cost'
    }

    page_list = pages[page]
    # Get sub pages that go on this page; Can be on pages w/ lists too
    if page in headers:
        header = headers[page]
    if page in sub_headers:
        sub_header = sub_headers[page]
    for page_link in page_list:
        sub_text += f'\n\t{OPT_C}{option_index}:{END_OPT_C} {page_to_string[page_link]}'
        if page_link in item_lists.keys():
            sub_options[str(option_index)] = (f'{SHOP_MAIN}:{page_link}#0', True)
        else:
            sub_options[str(option_index)] = (f'{SHOP_MAIN}:{page_link}', True)
        option_index += 1

    bstype = None
    if page_data.startswith('buy') or page_data.startswith('sell'):
        if '#' in page_data:
            bstype, page_data = page_data.split('#', 1)
        else:
            bstype = page_data
            page_data = ''

    page_num = None
    if page in item_lists:
        if '#' in page_data:
            page_num, page_data = page_data.split('#', 1)
        else:
            page_num = page_data
            page_data = ''
        page_num = int(page_num)

    if page in bspages:
        ip_text, ip_options = bspage_list(bspages[page], f'{SHOP_MAIN}:{page}', page_to_string)

        sub_text += ip_text
        for number, option in ip_options.items():
            sub_options[number] = (option, True)

        if sub_text != '':
            sub_text += '\n'

    if page_data == '' and page_num is not None:
        item_list = item_lists[page](page)

        if bstype == 'sell':
            item_list = Refs.gc.get_owned_items(item_list)

        if bstype == 'buy':
            sub_header = texts['buy_start'].format(page_to_string[page])
            ip_text, ip_options = item_page_list(option_index, f'{SHOP_MAIN}:{page}#buy', page_num, item_list, texts['buy_fail'], texts['buy_current'], get_item_string, page_num_first=False)
        elif bstype == 'sell':
            sub_header = texts['sell_start'].format(page_to_string[page])
            ip_text, ip_options = item_page_list(option_index, f'{SHOP_MAIN}:{page}#sell', page_num, item_list, texts['sell_fail'].format(page_to_string[page]), texts['sell_current'], get_item_string, page_num_first=False)
        else:
            ip_text, ip_options = item_page_list(option_index, f'{SHOP_MAIN}:{page}', page_num, item_list, texts['buy_fail'], texts['buy_current'], get_item_string, page_num_first=False)

        # Add to current page
        sub_text += ip_text
        for number, option in ip_options.items():
            sub_options[number] = (option, len(option.split('#')) > 3)
    elif page_data != '':
        item_id, item_count = page_data.split('#')
        if bstype:
            sub_header = texts[f'{bstype}_start'].format(Refs.gc.find_item(item_id).get_name())
            sub_text, sub_options = item_transaction(item_count, item_id, f'{SHOP_MAIN}:{page}#{bstype}#{page_num}', texts[f'{bstype}_current'], texts[f'{bstype}_future'])
        else:
            sub_text, sub_options = item_transaction(item_count, item_id, f'{SHOP_MAIN}:{page}#{page_num}', texts[f'buy_current'], texts[f'buy_future'])
        for number, option in sub_options.items():
            if 'confirm' not in option:
                sub_options[number] = (option, False)

    display_text += header
    display_text += sub_header
    display_text += sub_text
    _options.update(sub_options)

    if page == 'main':
        display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} Leave the market\n'
    else:
        display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} back\n'
    print(_options)
    return display_text, _options


def handle_action(console, action):
    if isinstance(action, str) and action.startswith('confirm'):
        page_category = None
        if action.count('#') == 5:  # Have a category
            page_name, page_category, page_num, item_id, item_count = action.split(':')[1].split('#')
        else:
            page_name, page_num, item_id, item_count = action.split(':')[1].split('#')
        if not do_transaction(item_id, int(item_count), 'sell' == page_category):
            console.error_time = 2.5
            console.error_text = 'Not Enough Money!'
            return
        if page_category:
            console.set_screen(f'{SHOP_MAIN}:{page_name}#{page_category}#{page_num}', False)
        else:
            console.set_screen(f'{SHOP_MAIN}:{page_name}#{page_num}', False)
        return
    print(action)
    console.set_screen(*action)


def bspage_list(sub_categories, page_name, id_to_string):
    display_text, option_index, _options = '', 1, {}

    for sub_category in sub_categories:
        for type in ['sell', 'buy']:
            display_text += f'\n\t{OPT_C}{option_index}:{END_OPT_C} {type.title()} {id_to_string[sub_category]}s'
            _options[str(option_index)] = f'{SHOP_MAIN}:{sub_category}#{type}#0'
            option_index += 1
    return display_text, _options


def get_item_string(item, index, current_text, page_name, page_num):
    if item.is_single():
        # Single item string
        name, desc, price = item.get_display()
        if Refs.gc.get_inventory().has_item(item.get_id()):
            return f'\n\t[s]{OPT_C}{index}:{END_OPT_C} {name}[/s] - Already purchased\n', None
        elif item.is_unlocked():
            return f'\n\t{OPT_C}{index}:{END_OPT_C} {name}\n\t\t- ' + desc.replace('\n', '\n\t\t- ') + f'\n\t{current_text}: {price}V\n', f'confirm#{page_name}#{page_num}#{item.get_id()}#1'
        return '', None
    else:
        # Multi item item string
        name, desc, min_price, max_price = item.get_display()
        if 'sell' in page_name:
            count = Refs.gc.get_inventory().get_item_count(item.get_id())
        else:
            count = min(floor(Refs.gc.get_varenth() / max_price), 50)
        return f'\n\t{OPT_C}{index}:{END_OPT_C} {name}\n\t\t- ' + desc.replace('\n', '\n\t\t- ') + f'\n\t{current_text}: {min_price}V\n\tIn Inventory: {count}\n', f'{page_name}#{page_num}#{item.get_id()}#{max(int(count / 2), 1)}'


def item_transaction(item_count, item_id, page_name, current_text, future_text):
    item = Refs.gc.find_item(item_id)
    if 'sell' in page_name:
        count = Refs.gc.get_inventory().get_item_count(item_id)
    else:
        count = min(floor(Refs.gc.get_varenth() / item.get_max_price()), 50)
    _options = {}

    display_text = f'\n\t{current_text}: {item.get_min_price()}V'
    left_string = '1'
    right_string = f'{count}'
    padding = max(len(left_string), len(right_string))
    arrow_string = left_string.rjust(padding) + '  ←───────→ ' + f'{count}'.ljust(padding)
    display_text += '\n\n\t' + f'{int(item_count)}'.center(len(arrow_string))
    display_text += f'\n\t{arrow_string}\n\n'
    display_text += f'\n\t{future_text}: {int(item_count) * item.get_min_price()}V\n'

    option_index = 1
    for (threshold, new_number, option_string) in [(count, count, 'All'), (max(int(count / 2), 1), max(int(count / 2), 1), 'Half'), (1, 1, 'One'), (count, int(item_count) + 1, 'More'), (1, int(item_count) - 1, 'Less')]:
        if int(item_count) == threshold:
            display_text += f'\n\t[s]{OPT_C}{option_index}:{END_OPT_C} {option_string}[/s]'
        else:
            display_text += f'\n\t{OPT_C}{option_index}:{END_OPT_C} {option_string}'
            _options[str(option_index)] = f'{page_name}#{item_id}#{new_number}'
        option_index += 1

    display_text += f'\n\t{OPT_C}{option_index}:{END_OPT_C} Confirm'
    _options[str(option_index)] = f'confirm#{page_name}#{item_id}#{item_count}'
    return display_text, _options


def do_transaction(item_id, count, selling):
    item = Refs.gc.find_item(item_id)
    if not selling:
        # Check if we have enough money
        # print(item.get_name(), item.get_max_price(), ' - ', Refs.gc.get_varenth())
        if item.get_max_price() > Refs.gc.get_varenth():
            return False

    # Adjust inventory
    if selling:
        Refs.gc.get_inventory().remove_item(item_id, count)
    else:
        if item.is_equipment():
            Refs.gc.get_inventory().add_item(item.get_class().get_id(), count, {'material_id': item.get_material_id(), 'sub_material1_id': None, 'sub_material2_id': None, 'hash': None})
        else:
            Refs.gc.get_inventory().add_item(item_id, count)

    # Adjust Varenth
    if selling:
        Refs.gc.update_varenth(item.get_min_price() * count)
    else:
        Refs.gc.update_varenth(-item.get_max_price() * count)

    # If map, update map data
    if item_id.startswith('full_map') and not Refs.gc.get_inventory().has_item('path_' + item_id[len('full_'):]):
        Refs.gc.get_inventory().add_item('path_' + item_id[len('full_'):])
    if item_id.startswith('path_map'):
        floor_id = int(item_id[len('path_map_floor_'):])
        Refs.gc.get_floor(floor_id).get_map().unlock_path_map()
    elif item_id.startswith('full_map'):
        floor_id = int(item_id[len('full_map_floor_'):])
        Refs.gc.get_floor(floor_id).get_map().unlock_full_map()
    return True
