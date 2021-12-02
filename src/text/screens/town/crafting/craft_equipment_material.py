from refs import END_OPT_C, OPT_C, Refs
from text.screens.common_functions import item_page_list
from text.screens.screen_names import BACK, CRAFT_EQUIPMENT, CRAFT_EQUIPMENT_MATERIAL
from text.screens.town import get_town_header


def get_screen(console, screen_data):
    console.header_callback = get_town_header
    _options = {'0': BACK}

    screen_data_options = screen_data.split('#')
    recipe = Refs.gc['recipes'][screen_data_options[0]]
    equipment = Refs.gc['equipment'][recipe.get_output_id()]
    material_index = int(screen_data_options[-1])
    current_material_id = screen_data_options[material_index + 1]
    current_material = None
    if current_material_id != 'none':
        current_material = Refs.gc['materials'][current_material_id]

    display_text = '\n\tWhich material would you like to use?'

    if current_material is None:
        display_text += '\n\n\tCurrent Material: None\n'
    else:
        display_text += f'\n\n\tCurrent Material: {current_material.get_name()}\n'

    if equipment.is_weapon():
        material_index = max(0, material_index - 2)
    material_type = list(recipe.get_ingredients())[material_index]
    print(list(recipe.get_ingredients()), list(recipe.get_ingredients().keys()))
    count = recipe.get_ingredients()[material_type]
    if equipment.is_weapon() and int(screen_data_options[-1]) in [1, 2]:
        count *= 0.2

    materials = []
    inventory = Refs.gc.get_inventory()
    if material_type == 'hard':
        for material in Refs.gc['materials'].values():
            if material.is_hard() and inventory.get_item_count(material.get_processed_id()) > count:
                materials.append(material)
    elif material_type == 'soft':
        for material in Refs.gc['materials'].values():
            if material.is_soft() and inventory.get_item_count(material.get_processed_id()) > count:
                materials.append(material)
    elif material_type == 'wood':
        for material in Refs.gc['materials'].values():
            if material.is_wood() and inventory.get_item_count(material.get_processed_id()) > count:
                materials.append(material)

    fail = '\n\tYou do not have any available materials.\n'
    item_func = lambda item, option_index, current, page_name, page_num: get_equipment_material(equipment.is_weapon(), item, option_index, current, page_name, page_num)
    ip_text, ip_options = item_page_list(1, CRAFT_EQUIPMENT_MATERIAL, 0, materials, fail, '', item_func)
    display_text += ip_text
    _options.update(ip_options)
    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} Back\n'
    return display_text, _options


def handle_action(console, action):
    data = console.get_current_data().split('#')
    print(data)
    data[int(data[-1]) + 1] = action
    print(data)
    console.set_screen(f'{CRAFT_EQUIPMENT}:{"#".join(data[:-1])}', True)


def get_equipment_material(is_weapon, item, option_index, current, page_name, page_num):
    string = f'\t{OPT_C}{option_index}: {END_OPT_C}{item.get_name()} - {item.get_hardness()} → {item.get_max_hardness()}'
    string += f'\n\t\t{item.get_defining_effect(is_weapon)}'
    string += f'\n\t\t{item.get_sub_effect(is_weapon)}\n'
    return string, item.get_id()
