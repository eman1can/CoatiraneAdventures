from math import floor

from refs import END_OPT_C, OPT_C, RED_C, Refs
from text.screens.shop import item_page_list
from text.screens.town import get_town_header


def housing_main(console):
    display_text = get_town_header()
    display_text += f'\n\tCurrent housing - {Refs.gc.get_housing().get_name()}'
    display_text += f'\n\t{Refs.gc.get_housing().get_description()}'
    display_text += f'{Refs.gc.get_housing().get_info()}'
    _options = {'0': 'back', }
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
            _options['1'] = 'housing_pay_bill'
            _options['2'] = f'housing_buy{Refs.gc.get_housing().get_id()}#{Refs.gc.get_housing().get_down_payment_minimum()}'
            _options['3'] = 'housing_browse0page'
        else:
            display_text += f'\n\t{OPT_C}2:{END_OPT_C} Browse other housings'
            _options['1'] = 'housing_pay_bill'
            _options['2'] = 'housing_browse0page'
    else:
        display_text += f'\n\tYou have fully payed for this housing.\n'
        display_text += f'\n\t{OPT_C}1:{END_OPT_C} Browse other housings'
        _options['1'] = 'housing_browse0page'
    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} Back\n'

    return display_text, _options


def get_housing_string(item, index, current_text, page_name, page_num):
    if Refs.gc.get_housing() != item:
        string = f'\n\t{item.get_name()}'
        string += f'\n\t\t' + item.get_description().replace('\n', '\n\t\t')
        string += f'\n\t{OPT_C}{index}:{END_OPT_C} Cost to rent: {Refs.gc.format_number(item.get_rent_cost())} per month'
        string += f'\n\t{OPT_C}{index + 1}:{END_OPT_C} Cost to buy: {Refs.gc.format_number(item.get_cost())}'
        string += f'\n\t\t- Minimum Downpayment: {Refs.gc.format_number(item.get_down_payment_minimum())}\n'
        _options = {str(index): f'housing_rent{item.get_id()}', str(index + 1): f'housing_buy{item.get_id()}#{item.get_down_payment_minimum()}'}
    else:
        _options = {}
        if Refs.gc.get_housing().is_renting():
            string = f'\n\t[s]{item.get_name()}[/s] - Currently Renting\n'
        else:
            string = f'\n\t[s]{item.get_name()}[/s] - Currently Bought\n'
    return string, _options


def housing_browse(console):
    display_text = get_town_header()
    item_list = Refs.gc.get_housing_options()

    page_num = int(console.get_current_screen()[len('housing_browse'):-len('page')])

    fail = '\n\tYou cannot buy any housing.'

    ip_text, ip_options = item_page_list(1, 'housing_browse', page_num, item_list, fail, '', get_housing_string)

    _options = {'0': 'back'}
    _options.update(ip_options)
    display_text += ip_text + f'\n\n\t{OPT_C}0:{END_OPT_C} back\n'
    return display_text, _options


def housing_rent(console):
    housing = Refs.gc['housing'][console.get_current_screen()[len('housing_rent'):]]

    current_housing = Refs.gc.get_housing()
    if current_housing.is_renting():
        money_back = floor(current_housing.get_bill_due() / 36)
    else:
        money_back = current_housing.get_cost() - (current_housing.get_bill_count() * current_housing.get_bill_cost(True))

    display_text = get_town_header()
    display_text += f'\n\tTo rent {housing.get_name()}, it will cost {Refs.gc.format_number(housing.get_cost())} per month.'
    display_text += f'\n\tYou will get {Refs.gc.format_number(money_back)} back from your {current_housing.get_name()}.'
    display_text += 'Are you sure that you want to do this?'
    display_text += f'\n\n\t{OPT_C}1:{END_OPT_C} Confirm'
    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} Back\n'
    _options = {'0': 'back', '1': console.get_current_screen() + 'confirm'}
    return display_text, _options


def housing_buy(console):
    housing_name, down_payment = console.get_current_screen().split('#')
    housing = Refs.gc['housing'][housing_name[len('housing_buy'):]]
    down_payment = int(down_payment)

    current_housing = Refs.gc.get_housing()
    if current_housing.is_renting():
        money_back = floor(current_housing.get_bill_due() / 36) * current_housing.get_bill_cost(True)
    else:
        money_back = current_housing.get_cost() - (current_housing.get_bill_count() * current_housing.get_bill_cost(True))

    display_text = get_town_header()
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
        display_text += f'\n\t{OPT_C}1:{END_OPT_C} Full'
        display_text += f'\n\t{OPT_C}2:{END_OPT_C} More'
    else:
        display_text += f'\n\t[s]{OPT_C}1:{END_OPT_C} Full[/s]'
        display_text += f'\n\t[s]{OPT_C}2:{END_OPT_C} More[/s]'
    if down_payment != int(cost / 2):
        display_text += f'\n\t{OPT_C}3:{END_OPT_C} Half'
    else:
        display_text += f'\n\t[s]{OPT_C}3:{END_OPT_C} Half[/s]'
    if down_payment != housing.get_down_payment_minimum():
        display_text += f'\n\t{OPT_C}4:{END_OPT_C} Less'
        display_text += f'\n\t{OPT_C}5:{END_OPT_C} Minimum'
    else:
        display_text += f'\n\n\t[s]{OPT_C}4:{END_OPT_C} Less[/s]'
        display_text += f'\n\n\t[s]{OPT_C}5:{END_OPT_C} Minimum[/s]'
    display_text += f'\n\n\t{OPT_C}6:{END_OPT_C} Confirm'
    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} Back\n'

    _options = {
        '0': 'back',
        '6': f'housing_buy{housing.get_id()}confirm#{down_payment}'
    }
    if down_payment != cost:
        _options['1'] = f'housing_buy{housing.get_id()}#{cost}'
        _options['2'] = f'housing_buy{housing.get_id()}#{down_payment + int(housing.get_cost() * 0.05)}'
    if down_payment != int(cost / 2):
        _options['3'] = f'housing_buy{housing.get_id()}#{int(cost / 2)}'
    if down_payment != housing.get_down_payment_minimum():
        _options['4'] = f'housing_buy{housing.get_id()}#{down_payment - int(housing.get_cost() * 0.05)}'
        _options['5'] = f'housing_buy{housing.get_id()}#{housing.get_down_payment_minimum()}'
    return display_text, _options
