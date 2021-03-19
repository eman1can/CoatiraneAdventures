from refs import END_OPT_C, OPT_C, Refs

INFO_WIDTH = 25
STATS_WIDTH = 10
BOX_WIDTH = INFO_WIDTH + STATS_WIDTH + 7
BOX_HEIGHT = 9


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
    strength = '-'
    magic = '-'
    endurance = '-'
    agility = '-'
    dexterity = '-'

    if item is not None:
        item_name = item.get_name()
        rank = str(item.get_rank())
        type = str(item.get_type())
        element = str(item.get_element())
        durability = str(item.get_durability()) + ' / ' + str(item.get_current_durability())
        score = str(item.get_score())
        value = str(item.get_value())
        health = str(item.get_health())
        mana = str(item.get_mana())
        strength = str(item.get_strength())
        magic = str(item.get_magic())
        endurance = str(item.get_endurance())
        agility = str(item.get_agility())
        dexterity = str(item.get_dexterity())

    string += f'│ {OPT_C}{index}{END_OPT_C} ' + name.ljust(INFO_WIDTH - len(f'{index} ')) + ' │ HP  ' + f'{health}'.rjust(6) + ' │\n'
    string += '│ ' + item_name.ljust(INFO_WIDTH - 3) + rank.rjust(3) + ' │ MP  ' + f'{mana}'.rjust(6) + ' │\n'
    string += '│ ' + 'Type'.ljust(10) + type.rjust(INFO_WIDTH - 10) + ' │ Str.' + f'{strength}'.rjust(6) + ' │\n'
    string += '│ ' + 'Element'.ljust(10) + element.rjust(INFO_WIDTH - 10) + ' │ Mag.' + f'{magic}'.rjust(6) + ' │\n'
    string += '│ ' + 'Durability'.ljust(10) + durability.rjust(INFO_WIDTH - 10) + ' │ End.' + f'{endurance}'.rjust(6) + ' │\n'
    string += '│ ' + 'Score'.ljust(10) + score.rjust(INFO_WIDTH - 10) + ' │ Agi.' + f'{agility}'.rjust(6) + ' │\n'
    string += '│ ' + 'Value'.ljust(10) + value.rjust(INFO_WIDTH - 10) + ' │ Dex.' + f'{dexterity}'.rjust(6) + ' │\n'

    string += '└'
    for _ in range(INFO_WIDTH + 2):
        string += '─'
    string += '┴'
    for _ in range(STATS_WIDTH + 2):
        string += '─'
    string += '┘\n'
    return string


def change_equip_main(console):
    display_string, _options = '', {}
    character_id = console.get_current_screen()[len('change_equip_main_'):]
    character = Refs.gc.get_char_by_id(character_id)

    outfit = character.get_outfit()
    column1, column2, column3 = '', '', ''
    column1 += get_equipment_box('Weapon', outfit.weapon, 1)
    column2 += get_equipment_box('Helmet', outfit.helmet, 2)
    column3 += get_equipment_box('Off-Hand Weapon', outfit.off_hand_weapon, 3)
    column1 += get_equipment_box('Necklace', outfit.necklace, 4)
    for _ in range(BOX_HEIGHT):
        for _ in range(BOX_WIDTH):
            column2 += ' '
        column2 += '\n'
    column3 += get_equipment_box('Ring', outfit.ring, 5)
    column1 += get_equipment_box('Vambraces', outfit.vambraces, 6)
    for _ in range(BOX_HEIGHT):
        for _ in range(BOX_WIDTH):
            column2 += ' '
        column2 += '\n'
    column3 += get_equipment_box('Grieves', outfit.grieves, 7)
    column1 += get_equipment_box('Gloves', outfit.gloves, 8)
    column2 += get_equipment_box('Chest', outfit.chest, 9)
    column3 += get_equipment_box('Boots', outfit.boots, 10)

    column1_rows = column1.split('\n')
    column2_rows = column2.split('\n')
    column3_rows = column3.split('\n')
    for x in range(len(column1_rows)):
        display_string += '\t' + column1_rows[x] + column2_rows[x] + column3_rows[x] + '\n'

    display_string += f'\t{OPT_C}0:{END_OPT_C} Back\n'

    _options = {
        '0': 'back',
        '1': 'change_equip_weapon',
        '2': 'change_equip_helmet',
        '3': 'change_equip_off_hand_weapon',
        '4': 'change_equip_necklace',
        '5': 'change_equip_ring',
        '6': 'change_equip_vambraces',
        '7': 'change_equip_grieves',
        '8': 'change_equip_gloves',
        '9': 'change_equip_chest',
        '10': 'change_equip_boots',
    }
    return display_string, _options
