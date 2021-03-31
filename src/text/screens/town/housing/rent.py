from math import floor

from game.housing import Housing
from refs import END_OPT_C, OPT_C, Refs
from text.screens.screen_names import BACK, HOUSING_MAIN
from text.screens.town import get_town_header


def get_screen(console, screen_data):
    housing = Refs.gc['housing'][screen_data]

    current_housing = Refs.gc.get_housing()
    if current_housing.is_renting():
        money_back = floor(current_housing.get_bill_due() / 36)
    else:
        money_back = current_housing.get_cost() - (current_housing.get_bill_count() * current_housing.get_bill_cost(True))

    console.header_callback = get_town_header
    display_text = f'\n\tTo rent {housing.get_name()}, it will cost {Refs.gc.format_number(housing.get_cost())} per month.'
    display_text += f'\n\tYou will get {Refs.gc.format_number(money_back)} back from your {current_housing.get_name()}.'
    display_text += ' Are you sure that you want to do this?'
    display_text += f'\n\n\t{OPT_C}1:{END_OPT_C} Confirm'
    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} Back\n'
    _options = {'0': BACK, '1': screen_data}
    return display_text, _options


def handle_action(console, action):
    housing = Refs.gc['housing'][action]
    if Housing.rent_housing(Refs.gc.get_housing(), housing):
        console.set_screen(HOUSING_MAIN)
    else:
        console.error_time = 2.5
        console.error_text = 'You don\'t have enough money to cover the first payment!'
