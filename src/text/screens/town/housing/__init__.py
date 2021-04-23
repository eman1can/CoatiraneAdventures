from refs import END_OPT_C, OPT_C, RED_C, Refs
from text.screens.screen_names import BACK, HOUSING_BROWSE, HOUSING_BUY, HOUSING_MAIN
from text.screens.town import get_town_header


def get_screen(console, screen_data):
    console.header_callback = get_town_header
    display_text = f'\n\tCurrent housing - {Refs.gc.get_housing().get_name()}'
    display_text += f'\n\t{Refs.gc.get_housing().get_description()}'
    display_text += f'{Refs.gc.get_housing().get_info()}'
    _options = {'0': BACK}
    if Refs.gc.get_housing().get_bill_count() > 0:
        if Refs.gc.get_housing().get_bill_due() < 0:
            display_text += f'\n\n\t{RED_C}Your bill is overdue by {-Refs.gc.get_housing().get_bill_due()} days!'
            display_text += f'\n\tYou owe {Refs.gc.format_number(Refs.gc.get_housing().get_bill_cost())} Varenth!'
            display_text += f'\n\tYou will be evicted in {5 + Refs.gc.get_housing().get_bill_due()} days!{END_OPT_C}'
            display_text += f'\n\n\t{OPT_C}1:{END_OPT_C} Pay overdue bill'
        elif Refs.gc.get_housing().get_bill_due() < 5:
            display_text += f'\n\n\tYour bill is due within the next {Refs.gc.get_housing().get_bill_due()} days. It will cost {Refs.gc.format_number(Refs.gc.get_housing().get_bill_cost())} Varenth.'
            display_text += f'\n\n\t{OPT_C}1:{END_OPT_C} Pay bill'
        else:
            display_text += f'\n\n\tYour next bill is due on {Refs.gc.get_housing().get_bill_date()} for {Refs.gc.format_number(Refs.gc.get_housing().get_bill_cost())} Varenth.'
            display_text += f'\n\n\t{OPT_C}1:{END_OPT_C} Pay bill in advance'

        if Refs.gc.get_housing().is_renting():
            display_text += f'\n\t{OPT_C}2:{END_OPT_C} Buy housing'
            display_text += f'\n\t{OPT_C}3:{END_OPT_C} Browse other housings'
            _options['1'] = 'pay_bill'
            _options['2'] = f'{HOUSING_BUY}:{Refs.gc.get_housing().get_id()}#{Refs.gc.get_housing().get_down_payment_minimum()}'
            _options['3'] = f'{HOUSING_BROWSE}:0'
        else:
            display_text += f'\n\t{OPT_C}2:{END_OPT_C} Browse other housings'
            _options['1'] = 'pay_bill'
            _options['2'] = f'{HOUSING_BROWSE}:0'
    else:
        display_text += f'\n\tYou have fully payed for this housing.\n'
        display_text += f'\n\t{OPT_C}1:{END_OPT_C} Browse other housings'
        _options['1'] = f'{HOUSING_BROWSE}:0'
    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} Back\n'

    return display_text, _options


def handle_action(console, action):
    if action == 'pay_bill':
        if not Refs.gc.get_housing().pay_bill():
            console.error_time = 2.5
            console.error_text = 'You don\'t have enough money to cover the payment!'
        console.set_screen(HOUSING_MAIN, False)
    else:
        console.set_screen(action, True)
