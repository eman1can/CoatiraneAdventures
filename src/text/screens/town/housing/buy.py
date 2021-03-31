from math import floor

from game.housing import Housing
from refs import END_OPT_C, OPT_C, Refs
from text.screens.screen_names import BACK, HOUSING_BUY, HOUSING_MAIN
from text.screens.town import get_town_header


def get_screen(console, screen_data):
    housing_name, down_payment = screen_data.split('#')
    housing = Refs.gc['housing'][housing_name]
    down_payment = int(down_payment)

    current_housing = Refs.gc.get_housing()
    if current_housing.is_renting():
        money_back = floor(current_housing.get_bill_due() / 36) * current_housing.get_bill_cost(True)
    else:
        money_back = current_housing.get_cost() - (current_housing.get_bill_count() * current_housing.get_bill_cost(True))

    console.header_callback = get_town_header
    display_text = ''
    cost = housing.get_cost()
    if housing == current_housing:
        # We are buying our rented place.
        display_text += f'\n\t{Refs.gc.format_number(money_back)} is subtracted from the cost of the housing from future rent payments.'
        cost -= money_back
    else:
        display_text += f'\n\tYou will get {Refs.gc.format_number(money_back)} back from your {current_housing.get_name()}.'
    display_text += '\n\tHow much of a down payment would you like to put down?\n'
    arrow_string = f'{Refs.gc.format_number(housing.get_down_payment_minimum())}  ←───────→ {Refs.gc.format_number(cost)}'
    display_text += '\n\t' + f'{Refs.gc.format_number(down_payment)}'.center(len(arrow_string))
    display_text += f'\n\t{arrow_string}\n\n'

    if cost - down_payment > 50000000:
        bill_count = 64
    elif cost - down_payment > 10000000:
        bill_count = 48
    elif cost - down_payment > 5000000:
        bill_count = 32
    else:
        bill_count = 16
    bill_cost = int((cost - down_payment) / bill_count)
    display_text += f'\n\tYou will pay {Refs.gc.format_number(bill_cost)} for {bill_count} months.'

    if down_payment != cost:
        display_text += f'\n\n\t{OPT_C}1:{END_OPT_C} Full'
        display_text += f'\n\t{OPT_C}2:{END_OPT_C} More'
    else:
        display_text += f'\n\n\t[s]{OPT_C}1:{END_OPT_C} Full[/s]'
        display_text += f'\n\t[s]{OPT_C}2:{END_OPT_C} More[/s]'
    if down_payment != int(cost / 2):
        display_text += f'\n\t{OPT_C}3:{END_OPT_C} Half'
    else:
        display_text += f'\n\t[s]{OPT_C}3:{END_OPT_C} Half[/s]'

    if down_payment != housing.get_down_payment_minimum():
        display_text += f'\n\t{OPT_C}4:{END_OPT_C} Less'
        display_text += f'\n\t{OPT_C}5:{END_OPT_C} Minimum'
    else:
        display_text += f'\n\t[s]{OPT_C}4:{END_OPT_C} Less[/s]'
        display_text += f'\n\t[s]{OPT_C}5:{END_OPT_C} Minimum[/s]'
    display_text += f'\n\n\t{OPT_C}6:{END_OPT_C} Confirm'
    display_text += f'\n\t{OPT_C}0:{END_OPT_C} Back\n'

    _options = {
        '0': BACK,
        '6': f'confirm#{housing.get_id()}#{down_payment}'
    }
    if down_payment != cost:
        _options['1'] = f'{HOUSING_BUY}:{housing.get_id()}#{cost}'
        _options['2'] = f'{HOUSING_BUY}:{housing.get_id()}#{down_payment + int(housing.get_cost() * 0.05)}'
    if down_payment != int(cost / 2):
        _options['3'] = f'{HOUSING_BUY}:{housing.get_id()}#{int(cost / 2)}'
    if down_payment != housing.get_down_payment_minimum():
        _options['4'] = f'{HOUSING_BUY}:{housing.get_id()}#{down_payment - int(housing.get_cost() * 0.05)}'
        _options['5'] = f'{HOUSING_BUY}:{housing.get_id()}#{housing.get_down_payment_minimum()}'
    return display_text, _options


def handle_action(console, action):
    if action.startswith('confirm'):
        housing_name, down_payment = action.split('#')[1:]
        housing = Refs.gc['housing'][housing_name]
        if Housing.buy_housing(Refs.gc.get_housing(), housing, int(down_payment)):
            console.set_screen(HOUSING_MAIN)
        else:
            console.error_time = 2.5
            console.error_text = 'You don\'t have that much money!'
    else:
        console.set_screen(action)