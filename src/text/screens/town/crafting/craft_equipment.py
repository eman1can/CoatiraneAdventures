from refs import END_OPT_C, OPT_C, Refs
from text.screens.screen_names import BACK, CRAFT_EQUIPMENT
from text.screens.town import get_town_header


def get_screen(console, screen_data):
    console.header_callback = get_town_header
    page_num, recipe_id, material_id, sub_material1_id, sub_material2_id = screen_data.split('#')
    page_num = int(page_num)
    _options = {'0': BACK}
    recipe = Refs.gc['recipes'][recipe_id]

    equipment = Refs.gc['equipment'][recipe.get_item_id()]
    display_text = f'\n\tWhat materials would you like to use in the {equipment.get_name()}?'

    material = None
    sub_material1 = None
    sub_material2 = None
    if material_id != 'none':
        material = Refs.gc['materials'][material_id]
    if sub_material1_id != 'none':
        sub_material1 = Refs.gc['materials'][sub_material1_id]
    if sub_material2_id != 'none':
        sub_material2 = Refs.gc['materials'][sub_material2_id]

    craft_text, craft_options = craft_items(recipe_count, recipe_id, recipe, f'{CRAFT_EQUIPMENT}:{page_num}')
    _options.update(craft_options)
    display_text += craft_text

    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} Back\n'
    return display_text, _options


def get_craft_equipment_item(recipe, index, current_text, page_name, page_num):
    require_string = ''
    for ingredient, count in recipe.get_ingredients().items():
        require_string += f'{count}x {ingredient}\n\t\t'
    item = Refs.gc['equipment'][recipe.get_item_id()]

    return f'\n\t{OPT_C}{index}:{END_OPT_C} {item.get_name()} x{recipe.get_item_count()}\n\t\t' + require_string[:-3], f'{page_name}:{recipe.get_item_id()}#none#none#none'
