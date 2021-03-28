from math import floor

from game.calendar import Calendar, MONTHS, NUMBER_ENDINGS
from refs import Refs


class Housing:
    def __init__(self, identifier, name, description, adventurer_limit, feature_list, installed_features, cost):
        self._id = identifier
        self._name = name
        self._description = description
        self._adventurer_limit = adventurer_limit
        self._feature_list = feature_list
        self._installed_features = installed_features
        self._cost = cost

        self._type = None
        self._bill_due = None
        self._bill_cost = int(self._cost * 0.05)
        self._bill_count = 1

    def set_data(self, type, date, count, cost=0):
        self._type = type
        self._bill_due = date
        if self._type == 'buy':
            self._bill_cost = cost
            self._bill_count = count
        else:
            self._bill_count = count
            self._bill_cost = int(self._cost * 0.05)

    def set_installed(self, installed):
        self._installed_features = installed

    def is_renting(self):
        return self._type == 'rent'

    def pay_bill(self):
        if self.get_bill_due() < 0:
            bill_cost = int(self._bill_cost * 1.5)
        else:
            bill_cost = self._bill_cost
        if bill_cost > Refs.gc.get_varenth():
            return False
        else:
            Refs.gc.update_varenth(-bill_cost)
        if self._type == 'buy':
            self._bill_count -= 1
        else:
            self._bill_count += 1
        if self._bill_count > 0:
            self._bill_due += 54000  # The number of minutes in a month
        return True

    def get_bill_cost(self, static=False):
        if self.get_bill_due() < 0 and not static:
            return int(self._bill_cost * 1.5)
        else:
            return self._bill_cost

    def get_bill_count(self):
        return self._bill_count

    def get_bill_date(self):
        return Calendar.int_time_to_date(self._bill_due)

    def get_bill_due(self):
        return Refs.gc.get_calendar().get_days_until(self._bill_due)

    def get_bill_due_int_time(self):
        return self._bill_due

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_description(self):
        return self._description

    def get_installed_features(self):
        return self._installed_features

    def is_under_limit(self):
        return len(Refs.gc.get_all_obtained_character_indexes()) < self._adventurer_limit

    def get_info(self):
        string = ''
        if self.can_have_mixing_room():
            string += '\n\tMixing Room - '
            if self.mixing_room_installed():
                string += 'Installed'
            else:
                string += 'Not Installed'
        if self.can_have_forge():
            string += '\n\tForge - '
            if self.forge_installed():
                string += 'Installed'
            else:
                string += 'Not Installed'
        if self.can_have_storefront():
            string += '\n\tStorefront - '
            if self.storefront_installed():
                string += 'Installed'
            else:
                string += 'Not Installed'
        return string

    def can_have_forge(self):
        return 'forge' in self._feature_list

    def forge_installed(self):
        return 'forge' in self._installed_features

    def can_have_mixing_room(self):
        return 'mixing_room' in self._feature_list

    def mixing_room_installed(self):
        return 'mixing_room' in self._installed_features

    def can_have_storefront(self):
        return 'storefront' in self._feature_list

    def storefront_installed(self):
        return 'storefront' in self._installed_features

    def get_cost(self):
        return self._cost

    def get_down_payment_minimum(self):
        return int(self._cost * 0.2)

    def get_rent_cost(self):
        return int(self._cost * 0.05)

    @staticmethod
    def rent_housing(current_housing, target_housing):
        # If we have payed rent in advance, return every future month's rent or return how much we have paid for the house
        if current_housing.is_renting():
            money_back = floor(current_housing.get_bill_due() / 36)
        else:
            money_back = current_housing.get_cost() - (current_housing.get_bill_count() * current_housing.get_bill_cost(True))
        # Set bill date and count, and subtract first payment
        if Refs.gc.get_varenth() + money_back < target_housing.get_rent_cost():
            return False
        Refs.gc.update_varenth(money_back)
        target_housing.set_data('rent', Refs.gc.get_calendar().get_int_time() + 54000)
        Refs.gc.update_varenth(-target_housing.get_rent_cost())
        # Switch housing in Refs
        Refs.gc.set_current_housing(target_housing)
        return True

    @staticmethod
    def buy_housing(current_housing, target_housing, down_payment):
        # If we have payed rent in advance, return every future month's rent or return how much we have paid for the house
        cost = target_housing.get_cost() - down_payment
        if current_housing.is_renting():
            money_back = floor(current_housing.get_bill_due() / 36) * current_housing.get_bill_cost(True)
            if current_housing == target_housing:
                cost -= money_back
                money_back = 0
        else:
            money_back = current_housing.get_cost() - (current_housing.get_bill_count() * current_housing.get_bill_cost(True))
        # Set bill date and count, and subtract first payment
        if Refs.gc.get_varenth() + money_back < down_payment:
            return False
        Refs.gc.update_varenth(money_back)
        if cost > 50000000:
            bill_count = 64
        elif cost > 10000000:
            bill_count = 48
        elif cost > 5000000:
            bill_count = 32
        else:
            bill_count = 16
        bill_cost = int(cost / bill_count)
        target_housing.set_data('buy', Refs.gc.get_calendar().get_int_time() + 54000, bill_count, bill_cost)
        Refs.gc.update_varenth(-down_payment)
        # Switch housing in Refs
        Refs.gc.set_current_housing(target_housing)
        return True
