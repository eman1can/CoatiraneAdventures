from refs import END_OPT_C, OPT_C, Refs
from text.screens.common_functions import item_page_list
from text.screens.screen_names import BACK, HOUSING_BROWSE, HOUSING_BUY, HOUSING_RENT
from text.screens.town import get_town_header


def get_housing_string(item, index, current_text, page_name, page_num):
    if Refs.gc.get_housing() != item:
        string = f'\n\t{item.get_name()}'
        string += f'\n\t\t' + item.get_description().replace('\n', '\n\t\t')
        string += f'\n\t{OPT_C}{index}:{END_OPT_C} Cost to rent: {Refs.gc.format_number(item.get_rent_cost())} per month'
        string += f'\n\t{OPT_C}{index + 1}:{END_OPT_C} Cost to buy: {Refs.gc.format_number(item.get_cost())}'
        string += f'\n\t\t- Minimum Downpayment: {Refs.gc.format_number(item.get_down_payment_minimum())}\n'
        _options = {str(index): f'{HOUSING_RENT}:{item.get_id()}', str(index + 1): f'{HOUSING_BUY}:{item.get_id()}#{item.get_down_payment_minimum()}'}
    else:
        _options = {}
        if Refs.gc.get_housing().is_renting():
            string = f'\n\t[s]{item.get_name()}[/s] - Currently Renting\n'
        else:
            string = f'\n\t[s]{item.get_name()}[/s] - Currently Bought\n'
    return string, _options


def get_screen(console, screen_data):
    console.header_callback = get_town_header
    item_list = Refs.gc.get_housing_options()

    page_num = int(screen_data)

    fail = '\n\tYou cannot buy any housing.'

    ip_text, ip_options = item_page_list(1, HOUSING_BROWSE, page_num, item_list, fail, '', get_housing_string)

    _options = {'0': BACK}
    _options.update(ip_options)
    display_text = ip_text + f'\n\n\t{OPT_C}0:{END_OPT_C} back\n'
    return display_text, _options


def handle_action(console, action):
    console.set_screen(action)
