from game.equipment import EQUIPMENT_CATEGORIES, WEAPON
from refs import END_OPT_C, OPT_C, Refs
from text.screens.character_attributes.change_equip import get_equipment_box
from text.screens.common_functions import item_page_list
from text.screens.screen_names import BACK, CHANGE_EQUIP, CHANGE_EQUIP_ITEM

INFO_WIDTH = 25
STATS_WIDTH = 10
BOX_WIDTH = INFO_WIDTH + STATS_WIDTH + 7
BOX_HEIGHT = 9


def get_screen(console, screen_data):
    display_string, _options = '', {}
    equipment_id, character_id, page_num = screen_data.split('#')
    page_num = int(page_num)
    equipment_id = int(equipment_id)
    character = Refs.gc.get_char_by_id(character_id)
    outfit = character.get_outfit()

    display_string += '\n\t'
    display_string += get_equipment_box(EQUIPMENT_CATEGORIES[equipment_id], outfit.items[equipment_id - WEAPON], 1).replace('\n', '\n\t')

    items = Refs.gc.get_equipment(equipment_id)

    _options = {'0': BACK}
    if outfit.items[equipment_id - WEAPON] is not None:
        display_string += f'\n\t{OPT_C}1:{END_OPT_C} Unequip {outfit.items[equipment_id - WEAPON].get_name()}\n'
        _options['1'] = f'confirm{CHANGE_EQUIP_ITEM}:{equipment_id}#{character_id}#0#none#none'

    display_string += '\n'

    fail = '\tYou have no matching equipment.\n'
    ip_text, ip_options = item_page_list(2, f'{CHANGE_EQUIP_ITEM}:{equipment_id}#{character_id}', page_num, items, fail, '', get_equipment_item, page_num_first=False, size_check=2)

    display_string += ip_text
    _options.update(ip_options)

    if outfit.items[equipment_id - WEAPON] is not None:
        display_string += f'\n\t{OPT_C}0:{END_OPT_C} Keep Item\n'
    else:
        display_string += f'\n\t{OPT_C}0:{END_OPT_C} Back\n'
    return display_string, _options


def handle_action(console, action):
    if action.startswith('confirm'):
        equipment_id, character_id, page_num, item_id, item_hash = action.split(':')[1].split('#')
        item = None
        if item_id != 'none':
            item = Refs.gc.get_inventory().get_item(item_id, int(item_hash))
        character = Refs.gc.get_char_by_id(character_id)
        outfit = character.get_outfit()
        outfit.set_equipment(int(equipment_id), item)
        character.refresh_stats()
        console.set_screen(f'{CHANGE_EQUIP}:{character_id}')
    else:
        console.set_screen(action)


def get_equipment_item(equipment, index, current_text, page_name, page_num):
    durability = str(int(equipment.get_durability())) + ' / ' + str(int(equipment.get_current_durability()))
    string = f'\n\t{equipment.get_name()}'

    gap = 4
    string += f'\n\t\t- Durability: {durability}'
    string += f'\n\t\t- Score:     ' + f'{int(equipment.get_score())}'.rjust(gap)
    string += f' - Value:     ' + f'{int(equipment.get_value())}'.rjust(gap)
    string += f'\n\t\t- HP:        ' + f'{int(equipment.get_health())}'.rjust(gap)
    string += f' - MP:        ' + f'{int(equipment.get_mana())}'.rjust(gap)
    string += f'\n\t\t- Phy. Atk.: ' + f'{int(equipment.get_physical_attack())}'.rjust(gap)
    string += f' - Mag. Atk.: ' + f'{int(equipment.get_magical_attack())}'.rjust(gap)
    string += f'\n\t\t- Def.:      ' + f'{int(equipment.get_defense())}'.rjust(gap)
    string += f'\n\t{OPT_C}{index}{END_OPT_C} Select\n'
    return string, f'confirm{page_name}#{page_num}#{equipment.get_full_id()}'
