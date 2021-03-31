from refs import END_OPT_C, OPT_C, Refs
from text.screens.common_functions import item_page_list
from text.screens.screen_names import BACK, CRAFTING_POTIONS, CRAFT_ITEM_MULTIPLE
from text.screens.town import get_town_header
from text.screens.town.crafting.craft_item_multiple import get_craft_item


def get_screen(console, screen_data):
    console.header_callback = get_town_header
    display_text = '\n\tWhat type of potion would you like to make?\n'

    recipes = Refs.gc.get_potion_recipes()

    page_num = int(screen_data)

    fail = '\n\tThere is nothing that you can craft.'

    item_func = lambda item, option_index, current, page_name, page_num: get_craft_item(item, option_index, current, CRAFT_ITEM_MULTIPLE, page_num)
    ip_text, ip_options = item_page_list(1, CRAFTING_POTIONS, page_num, recipes, fail, '', item_func)

    _options = {'0': BACK}
    _options.update(ip_options)
    display_text += ip_text + f'\n\n\t{OPT_C}0:{END_OPT_C} back\n'
    return display_text, _options


def handle_action(console, action):
    console.set_screen(action)
