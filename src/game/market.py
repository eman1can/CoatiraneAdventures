

class Market:
    def __init__(self):
        self._tracked_items = {}

    @staticmethod
    def is_price_static(base_price, min_price, max_price):
        return base_price == min_price == max_price

    def add_item_to_market(self, item_id, price_tracker):
        self._tracked_items[item_id] = price_tracker

    def get_category(self, item_id):
        return self._tracked_items[item_id].get_category()

    def get_price(self, item_id):
        return self._tracked_items[item_id].get_price()

    def get_min_price(self, item_id):
        return self._tracked_items[item_id].get_min()

    def get_max_price(self, item_id):
        return self._tracked_items[item_id].get_max()

    def set_price(self, item_id, price):
        self._tracked_items[item_id].set_price(price)

    def set_min_price(self, item_id, min_price):
        self._tracked_items[item_id].set_min(min_price)

    def set_max_price(self, item_id, max_price):
        self._tracked_items[item_id].set_max(max_price)

    def get_sell_price(self, item_id):
        """
        The sell price trends towards the floor, and rises to barter skills
        :param item_id:
        :return: price
        """
        return self._tracked_items[item_id].get_sell_price()

    def get_buy_price(self, item_id):
        """
        The buy price trends towards the limit, and lowers to barter skills
        :param item_id:
        :return: price
        """
        return self._tracked_items[item_id].get_buy_price()

    def get_items_by_category(self, item_category):
        output_ids = []
        for item_id, price_tracker in self._tracked_items.items():
            if item_category == price_tracker.get_category():
                output_ids.append(item_id)
        return output_ids

    def adjust_market(self, item_id, count, buy=False):
        tracker = self._tracked_items[item_id]
        if buy:
            tracker.adjust_from_buy(count)
        else:
            tracker.adjust_from_sell(count)

    def adjust_market_random(self):
        pass


class PriceTracker:
    def __init__(self, category, base, min, max, elasticity=1):
        self._category = category
        self._base = base
        self._min = min
        self._max = max

        self._current = base
        self._sell = min
        self._buy = max
        self._elasticity = elasticity

    def __str__(self):
        return f'{self._min} → {self._base} → {self._max}'

    def get_category(self):
        return self._category

    def get_price(self):
        return self._current

    def get_min(self):
        return self._min

    def get_max(self):
        return self._max

    def get_sell_price(self):
        return self._sell

    def get_buy_price(self):
        return self._buy

    def set_price(self, new_base):
        self._current = new_base

    def set_min(self, new_min):
        self._min = new_min

    def set_max(self, new_max):
        self._max = new_max

    def is_static(self):
        return self._base == self._min == self._max

    def adjust_from_sell(self, count):
        if self.is_static():
            return

    def adjust_from_buy(self, count):
        if self.is_static():
            return
