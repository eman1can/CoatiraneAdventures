from refs import Refs


class Item:
    def __init__(self, item_id, name, description, shop_category, purchase_type, price):
        self._id = item_id
        self._name = name
        self._purchase_type = purchase_type
        self._description = description
        self._category = shop_category
        self._price = int(price)
        self._unlock_type = None
        self._unlock_requirement = None

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def is_single(self):
        return self._purchase_type == 'single'

    def is_multi(self):
        return self._purchase_type == 'multi'

    def set_unlock_requirement(self, unlock_requirement):
        if unlock_requirement == 'none':
            return
        else:
            self._unlock_type, self._unlock_requirement = unlock_requirement.split(', ')

    def is_equipment(self):
        return False

    def is_unlocked(self):
        if self._unlock_type is None:
            return True
        if self._unlock_type == 'floor':
            return Refs.gc.get_lowest_floor() >= int(self._unlock_requirement)
        elif self._unlock_type == 'inventory':
            return Refs.gc.get_inventory().has_item(self._unlock_requirement)
        elif self._unlock_type == 'map_data':
            return Refs.gc.get_inventory().has_item(self._unlock_requirement)

    def get_display(self):
        return self._name, self._description, self._price

    def get_price(self):
        return self._price

    def get_min_price(self):
        return self._price

    def get_max_price(self):
        return self._price

    def get_category(self):
        return self._category


class DropItem:
    def __init__(self, item_id, name, description, purchase_type, min_price, max_price):
        self._id = item_id
        self._name = name
        self._purchase_type = purchase_type
        self._description = description
        self._min_price = int(min_price)
        self._max_price = int(max_price)

    def get_id(self):
        return self._id

    def is_equipment(self):
        return False

    def get_name(self):
        return self._name

    def is_single(self):
        return self._purchase_type == 'single'

    def is_multi(self):
        return self._purchase_type == 'multi'

    def get_display(self):
        return self._name, self._description, self._min_price, self._max_price

    def get_min_price(self):
        return self._min_price

    def get_max_price(self):
        return self._max_price


class Ingredient:
    def __init__(self, item_id, name, description, purchase_type, min_price, max_price):
        self._id = item_id
        self._name = name
        self._purchase_type = purchase_type
        self._description = description
        self._min_price = int(min_price)
        self._max_price = int(max_price)

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_category(self):
        return 'ingredients'

    def is_equipmetn(self):
        return False

    def is_single(self):
        return self._purchase_type == 'single'

    def is_multi(self):
        return self._purchase_type == 'multi'

    def get_display(self):
        return self._name, self._description, self._min_price, self._max_price

    def get_min_price(self):
        return self._min_price

    def get_max_price(self):
        return self._max_price
