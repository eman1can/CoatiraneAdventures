from math import floor

from refs import END_OPT_C, OPT_C, Refs
from text.screens.shop import item_page_list
from text.screens.town import get_town_header

"""
Process Materials - Requires Basic Tailor or Apprentice Blacksmith
Craft Alloys - Requires Apprentice Blacksmith
Craft Items - Requires Daedalus' Protégé
Craft Equipment - Requires Basic Tailor or Apprentice Blacksmith
Craft Potions - Required Fledgling Alchemist
"""


def crafting_main(console):
    console.header_callback = get_town_header
    display_text = '\n\tWhat kind of crafting would you like to do?\n'
    _options = {'0': 'back'}

    display_text += f'\n\t{OPT_C}1:{END_OPT_C} Process Materials'
    if not Refs.gc.has_perk('basic_tailor') and not Refs.gc.has_perk('apprentice_blacksmith'):
        display_text += ' - LOCKED'
    else:
        _options['1'] = 'crafting_process_materials*0'
    display_text += f'\n\t{OPT_C}2:{END_OPT_C} Craft Alloys'
    if not Refs.gc.has_perk('apprentice_blacksmith'):
        display_text += ' - LOCKED'
    else:
        _options['2'] = 'crafting_alloys*0'
    display_text += f'\n\t{OPT_C}3:{END_OPT_C} Craft Items'
    if not Refs.gc.has_perk('daedalus_protege'):
        display_text += ' - LOCKED'
    else:
        _options['3'] = 'crafting_items*0'
    display_text += f'\n\t{OPT_C}4:{END_OPT_C} Craft Equipment'
    if not Refs.gc.has_perk('reputable_tailor') and not Refs.gc.has_perk('skilled_blacksmith'):
        display_text += ' - LOCKED'
    else:
        _options['4'] = 'crafting_equipment*0'
    display_text += f'\n\t{OPT_C}5:{END_OPT_C} Craft Potions'
    if not Refs.gc.has_perk('fledgling_alchemist'):
        display_text += ' - LOCKED'
    else:
        _options['5'] = 'crafting_items*0'

    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} back\n'
    return display_text, _options


def get_craft_item(recipe, index, current_text, page_name, page_num):
    valid = True
    inventory = Refs.gc.get_inventory()
    require_string = ''
    max_create = 0
    for ingredient, count in recipe.get_ingredients().items():
        item = Refs.gc.find_item(ingredient)
        item_count = inventory.get_item_count(ingredient)
        require_string += f'{count}x {item.get_name()}\n\t\t'
        valid &= item_count > count
        max_create = max(max_create, floor(item_count / count))
    item = Refs.gc.find_item(recipe.get_item_id())

    if valid:
        return f'\n\t{OPT_C}{index}:{END_OPT_C} {item.get_name()} x{recipe.get_item_count()}\n\t\t' + require_string[:-3], f'crafting_process_material{page_num}page#{recipe.get_item_id()}#{max_create}'
    else:
        return f'\n\t[s]{OPT_C}{index}:{END_OPT_C} {item.get_name()} x{recipe.get_item_count()}\n\t\t' + require_string[:-3], ''


def get_craft_equipment_item(recipe, index, current_text, page_name, page_num):
    require_string = ''
    for ingredient, count in recipe.get_ingredients().items():
        require_string += f'{count}x {ingredient}\n\t\t'
    item = Refs.gc['equipment' \
                   ''][recipe.get_item_id()]

    return f'\n\t{OPT_C}{index}:{END_OPT_C} {item.get_name()} x{recipe.get_item_count()}\n\t\t' + require_string[:-3], f'crafting_craft_equipment{page_num}page#{recipe.get_item_id()}'


def crafting_process_materials(console):
    console.header_callback = get_town_header
    display_text = '\n\tWhat type of finished material would you like to make?\n'

    recipes = Refs.gc.get_process_recipes()

    page_num = int(console.get_current_screen()[len('crafting_process_materials'):-len('page')])

    fail = '\n\tThere is nothing that you can craft.'

    ip_text, ip_options = item_page_list(1, 'crafting_process_materials', page_num, recipes, fail, '', get_craft_item)

    _options = {'0': 'back'}
    _options.update(ip_options)
    display_text += ip_text + f'\n\n\t{OPT_C}0:{END_OPT_C} back\n'
    return display_text, _options


def craft_items(recipe_count, recipe_id, recipe, page_name):
    count = 0
    inventory = Refs.gc.get_inventory()
    ingredients = {}
    recipe_item = Refs.gc.find_item(recipe.get_item_id())
    have_recipe_count = inventory.get_item_count(recipe.get_item_id())
    for ingredient, cost in recipe.get_ingredients().items():
        item = Refs.gc.find_item(ingredient)
        item_count = inventory.get_item_count(ingredient)
        ingredients[item] = item_count
        count = max(cost, floor(item_count / cost))

    _options = {}
    display_text = '\n\n\t'
    arrow_string = '1'.rjust(4) + f' ←───────→ ' + f'{count}'.ljust(4)
    display_text += '\n\t' + f'{int(recipe_count)}'.center(len(arrow_string))
    display_text += f'\n\t{arrow_string}\n\n'
    for ingredient, ingredient_have in ingredients.items():
        display_text += f'\n\t{ingredient.get_name()} ' + '{ingredient_have}'.ljust(5) + ' → ' + f'{ingredient_have - (recipe.get_ingredients()[ingredient.get_id()] * recipe_count)}'
    display_text += f'\n\t{recipe_item.get_name()} ' + '{have_recipe_count}'.ljust(5) + ' → ' + f'{have_recipe_count + recipe_count}\n\n'

    option_index = 1
    for (threshold, new_number, option_string) in [(count, count, 'All'), (max(int(count / 2), 1), max(int(count / 2), 1), 'Half'), (1, 1, 'One'), (count, int(recipe_count) + 1, 'More'), (1, int(recipe_count) - 1, 'Less')]:
        if int(recipe_count) == threshold:
            display_text += f'\n\t[s]{OPT_C}{option_index}:{END_OPT_C} {option_string}[/s]'
        else:
            display_text += f'\n\t{OPT_C}{option_index}:{END_OPT_C} {option_string}'
            _options[str(option_index)] = f'{page_name}#{recipe_id}#{new_number}'
        option_index += 1

    display_text += f'\n\t{OPT_C}{option_index}:{END_OPT_C} Confirm'
    _options[str(option_index)] = f'{page_name}_confirm#{recipe_id}#{recipe_count}'
    return display_text, _options


def crafting_process_material(console):
    console.header_callback = get_town_header
    display_text = '\n\tHow many would you like to create?\n'

    page_name, recipe_id, recipe_count = console.get_current_screen().split('#')
    page_num = int(page_name[len('crafting_process_material'):-len('page')])

    recipe = Refs.gc['recipes'][recipe_id]

    _options = {'0': 'back'}
    craft_text, craft_options = craft_items(int(recipe_count), recipe_id, recipe, f'crafting_process_material{page_num}page')
    _options.update(craft_options)
    display_text += craft_text

    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} back\n'
    return display_text, _options


def crafting_alloys(console):
    console.header_callback = get_town_header
    display_text = '\n\tWhat type of finished alloy would you like to make?\n'

    recipes = Refs.gc.get_alloy_recipes()

    page_num = int(console.get_current_screen()[len('crafting_alloys'):-len('page')])

    fail = '\n\tThere is nothing that you can craft.'

    ip_text, ip_options = item_page_list(1, 'crafting_alloys', page_num, recipes, fail, '', get_craft_item)

    _options = {'0': 'back'}
    _options.update(ip_options)
    display_text += ip_text + f'\n\n\t{OPT_C}0:{END_OPT_C} back\n'
    return display_text, _options


def crafting_equipment(console):
    console.header_callback = get_town_header
    display_text = '\n\tWhat type of equipment would you like to make?\n'

    recipes = Refs.gc.get_equipment_recipes()

    page_num = int(console.get_current_screen()[len('crafting_equipment'):-len('page')])

    fail = '\n\tThere is nothing that you can craft.'

    ip_text, ip_options = item_page_list(1, 'crafting_equipment', page_num, recipes, fail, '', get_craft_equipment_item)

    _options = {'0': 'back'}
    _options.update(ip_options)
    display_text += ip_text + f'\n\n\t{OPT_C}0:{END_OPT_C} back\n'
    return display_text, _options


# def crafting_craft_equipment(console):
