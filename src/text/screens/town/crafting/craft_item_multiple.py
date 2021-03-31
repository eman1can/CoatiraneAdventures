from math import floor

from refs import END_OPT_C, OPT_C, Refs
from text.screens.screen_names import BACK, CRAFT_ITEM_MULTIPLE
from text.screens.town import get_town_header


def get_screen(console, screen_data):
    console.header_callback = get_town_header
    display_text = '\n\tHow many would you like to create?'

    page_num, recipe_id, recipe_count = screen_data.split('#')
    page_num, recipe_count = int(page_num), int(recipe_count)

    recipe = Refs.gc['recipes'][recipe_id]

    _options = {'0': BACK}
    craft_text, craft_options = craft_items(recipe_count, recipe_id, recipe, f'{CRAFT_ITEM_MULTIPLE}:{page_num}')
    _options.update(craft_options)
    display_text += craft_text

    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} Back\n'
    return display_text, _options


def handle_action(console, action):
    if action.startswith('confirm'):
        recipe_id, recipe_count = action.split('#')[1:]
        recipe = Refs.gc['recipes'][recipe_id]
        recipe_count = int(recipe_count)
        inventory = Refs.gc.get_inventory()
        for ingredient, count in recipe.get_ingredients().items():
            inventory.remove_item(ingredient, count * recipe_count)
        inventory.add_item(recipe.get_item_id(), recipe_count)
        console.set_screen(BACK)
    else:
        console.set_screen(action)


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
        display_text += f'\n\t{ingredient.get_name()} ' + f'{ingredient_have}'.ljust(5) + ' → ' + f'{ingredient_have - (recipe.get_ingredients()[ingredient.get_id()] * recipe_count)}'
    display_text += f'\n\t{recipe_item.get_name()} ' + f'{have_recipe_count}'.ljust(5) + ' → ' + f'{have_recipe_count + recipe_count}\n\n'

    option_index = 1
    for (threshold, new_number, option_string) in [(count, count, 'All'), (max(int(count / 2), 1), max(int(count / 2), 1), 'Half'), (1, 1, 'One'), (count, int(recipe_count) + 1, 'More'), (1, int(recipe_count) - 1, 'Less')]:
        if int(recipe_count) == threshold:
            display_text += f'\n\t[s]{OPT_C}{option_index}:{END_OPT_C} {option_string}[/s]'
        else:
            display_text += f'\n\t{OPT_C}{option_index}:{END_OPT_C} {option_string}'
            _options[str(option_index)] = f'{page_name}#{recipe_id}#{new_number}'
        option_index += 1

    display_text += f'\n\t{OPT_C}{option_index}:{END_OPT_C} Confirm'
    _options[str(option_index)] = f'confirm#{recipe_id}#{recipe_count}'
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
        return f'\n\t{OPT_C}{index}:{END_OPT_C} {item.get_name()} x{recipe.get_item_count()}\n\t\t' + require_string[:-3], f'{page_name}:{page_num}#{recipe.get_item_id()}#{max_create}'
    else:
        return f'\n\t[s]{OPT_C}{index}:{END_OPT_C} {item.get_name()} x{recipe.get_item_count()}\n\t\t' + require_string[:-3], ''
