from game.equipment import BOOTS, CHEST, GLOVES, GRIEVES, HELMET, NECKLACE, OFF_HAND_WEAPON, RING, VAMBRACES, WEAPON
from game.skill import ELEMENTS
from refs import END_OPT_C, OPT_C, Refs
from text.screens.common_functions import center, get_plain_size
from text.screens.screen_names import BACK, CHANGE_EQUIP_ITEM

INFO_WIDTH = 25
STATS_WIDTH = 13
BOX_WIDTH = INFO_WIDTH + STATS_WIDTH + 7
BOX_HEIGHT = 8


def get_equipment_box(name, item, index):
    string = '┌'
    for _ in range(INFO_WIDTH + 2):
        string += '─'
    string += '┬'
    for _ in range(STATS_WIDTH + 2):
        string += '─'
    string += '┐\n'

    item_name = 'Not Equipped'
    rank = '-'
    type = '-'
    element = '-'
    durability = '-'
    score = '-'
    value = '-'
    health = '-'
    mana = '-'
    physical_attack = '-'
    magical_attack = '-'
    defense = '-'

    if item is not None:
        item_name = item.get_name()
        rank = str(item.get_rank())
        element = ELEMENTS[item.get_element()]
        durability = str(int(item.get_durability())) + '/' + str(int(item.get_current_durability()))
        score = str(int(item.get_score()))
        value = str(int(item.get_value()))
        health = str(int(item.get_health()))
        mana = str(int(item.get_mana()))
        physical_attack = str(int(item.get_physical_attack()))
        magical_attack = str(int(item.get_magical_attack()))
        defense = str(int(item.get_defense()))

    string += f'│ {OPT_C}{index}{END_OPT_C} ' + name.ljust(INFO_WIDTH - len(f'{index} ')) + ' │ HP     ' + f'{health}'.rjust(6) + ' │\n'
    string += '│ ' + item_name.ljust(INFO_WIDTH - 3) + rank.rjust(3) + ' │ MP     ' + f'{mana}'.rjust(6) + ' │\n'
    string += '│ ' + ''.ljust(10) + ''.rjust(INFO_WIDTH - 10) + ' │ P. Atk.' + f'{physical_attack}'.rjust(6) + ' │\n'
    string += '│ ' + 'Element'.ljust(10) + element.rjust(INFO_WIDTH - 10) + ' │ M. Atk.' + f'{magical_attack}'.rjust(6) + ' │\n'
    string += '│ ' + 'Durability'.ljust(10) + durability.rjust(INFO_WIDTH - 10) + ' │ Def.   ' + f'{defense}'.rjust(6) + ' │\n'
    string += '│ ' + 'Value'.ljust(10) + value.rjust(INFO_WIDTH - 10) + ' │ Score  ' + f'{score}'.rjust(6) + ' │\n'
    # string += '│ ' + 'Value'.ljust(10) + value.rjust(INFO_WIDTH - 10) + ' │ Dex.   ' + f'{dexterity}'.rjust(6) + ' │\n'

    string += '└'
    for _ in range(INFO_WIDTH + 2):
        string += '─'
    string += '┴'
    for _ in range(STATS_WIDTH + 2):
        string += '─'
    string += '┘\n'
    return string


def get_screen(console, screen_data):
    display_string, _options = '', {}
    character = Refs.gc.get_char_by_id(screen_data)

    outfit = character.get_outfit()
    column1, column2, column3 = '', '', ''
    column1 += get_equipment_box('Weapon', outfit.get_equipment(WEAPON), 1)
    column2 += get_equipment_box('Helmet', outfit.get_equipment(HELMET), 2)
    column3 += get_equipment_box('Off-Hand Weapon', outfit.get_equipment(OFF_HAND_WEAPON), 3)
    column1 += get_equipment_box('Necklace', outfit.get_equipment(NECKLACE), 4)
    column2 += ''.center(BOX_WIDTH) + '\n'
    column2 += f'{character.get_display_name()}'.center(BOX_WIDTH) + '\n'
    column2 += f'{character.get_name()}'.center(BOX_WIDTH) + '\n'
    column2 += ''.center(BOX_WIDTH) + '\n'
    column2 += f'Favorite Weapon: {character.get_favorite_weapon()}'.center(BOX_WIDTH) + '\n'
    column2 += f'Favorite Sub-Weapon: {character.get_favorite_sub_weapon()}'.center(BOX_WIDTH) + '\n'
    for _ in range(BOX_HEIGHT - 6):
        column2 += ''.center(BOX_WIDTH) + '\n'
    column3 += get_equipment_box('Ring', outfit.get_equipment(RING), 5)
    column1 += get_equipment_box('Vambraces', outfit.get_equipment(VAMBRACES), 6)
    for _ in range(BOX_HEIGHT):
        column2 += ''.center(BOX_WIDTH) + '\n'
    column3 += get_equipment_box('Grieves', outfit.get_equipment(GRIEVES), 7)
    column1 += get_equipment_box('Gloves', outfit.get_equipment(GLOVES), 8)
    column2 += get_equipment_box('Chest', outfit.get_equipment(CHEST), 9)
    column3 += get_equipment_box('Boots', outfit.get_equipment(BOOTS), 10)

    column1_rows = column1.split('\n')
    column2_rows = column2.split('\n')
    column3_rows = column3.split('\n')
    for x in range(len(column1_rows)):
        row = column1_rows[x] + ' ' + column2_rows[x] + ' ' + column3_rows[x]
        display_string += center(row, get_plain_size(row), console.get_width()) + '\n'

    display_string += f'\t{OPT_C}0:{END_OPT_C} Back\n'

    _options = {
        '0':  BACK,
        '1':  f'{CHANGE_EQUIP_ITEM}:{WEAPON}#{screen_data}#0',
        '2':  f'{CHANGE_EQUIP_ITEM}:{HELMET}#{screen_data}#0',
        '3':  f'{CHANGE_EQUIP_ITEM}:{OFF_HAND_WEAPON}#{screen_data}#0',
        '4':  f'{CHANGE_EQUIP_ITEM}:{NECKLACE}#{screen_data}#0',
        '5':  f'{CHANGE_EQUIP_ITEM}:{RING}#{screen_data}#0',
        '6':  f'{CHANGE_EQUIP_ITEM}:{VAMBRACES}#{screen_data}#0',
        '7':  f'{CHANGE_EQUIP_ITEM}:{GRIEVES}#{screen_data}#0',
        '8':  f'{CHANGE_EQUIP_ITEM}:{GLOVES}#{screen_data}#0',
        '9':  f'{CHANGE_EQUIP_ITEM}:{CHEST}#{screen_data}#0',
        '10': f'{CHANGE_EQUIP_ITEM}:{BOOTS}#{screen_data}#0',
    }
    return display_string, _options


def handle_action(console, action):
    console.set_screen(action)

