from refs import Refs


class Item:
    def __init__(self, item_id, name, description, visible_after_floor):
        self._id = item_id
        self._name = name
        if 'floor' in item_id:
            map_type, floor = item_id.split('_floor_')
            self._image = f'items/{map_type}.png'
        elif 'ingot' in item_id:
            type = item_id.split('_ingot')[0]
            self._image = f'items/{type}/ingot.png'
        else:
            self._image = f'items/{item_id}.png'
        self._description = description
        self._visible_after_floor = visible_after_floor
        self._unlock_type = None
        self._unlock_requirement = None

    def __str__(self):
        return f'{self._id} - {self._name}'

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def is_equipment(self):
        return False

    def is_item(self):
        return True

    def is_drop_item(self):
        return False

    def is_shop_item(self):
        return False

    def is_ingredient(self):
        return False

    def is_potion(self):
        return False

    def is_floor_map(self):
        return False

    def set_unlock_requirement(self, unlock_requirement):
        if unlock_requirement == 'none':
            return
        else:
            self._unlock_type, self._unlock_requirement = unlock_requirement.split(', ')

    def get_visible_floor(self):
        return self._visible_after_floor

    def is_unlocked(self):
        if self._visible_after_floor > Refs.gc.get_lowest_floor():
            return False
        if self._unlock_type is None:
            return True
        if self._unlock_type == 'floor':
            return Refs.gc.get_lowest_floor() >= int(self._unlock_requirement)
        elif self._unlock_type == 'inventory':
            return Refs.gc.get_inventory().has_item(self._unlock_requirement)
        elif self._unlock_type == 'map_data':
            return Refs.gc.get_inventory().has_item(self._unlock_requirement)

    def get_display(self):
        return self._name, self._description

    def get_description(self):
        return self._description

    def get_image(self):
        return self._image


class ShopItem(Item):
    def __init__(self, item_id, name, description, visible_after_floor, shop_category, can_own_multiple=True):
        super().__init__(item_id, name, description, visible_after_floor)
        self._category = shop_category
        self._can_own_multiple = can_own_multiple

    def get_category(self):
        return self._category

    def get_own_multiple(self):
        return self._can_own_multiple

    def is_shop_item(self):
        return True


class DropItem(ShopItem):
    def __init__(self, item_id, name, description, visible_after_floor):
        super().__init__(item_id, name, description, visible_after_floor, 'drop_items')

    def is_drop_item(self):
        return True


class Ingredient(ShopItem):
    def __init__(self, item_id, name, description, visible_after_floor):
        super().__init__(item_id, name, description, visible_after_floor, 'ingredients')
        if 'raw' in item_id:
            name, type = item_id.split('_', 1)
        else:
            type, name = item_id.rsplit('_', 1)
        self._image = f'items/{type}/{name}.png'

    def is_ingredient(self):
        return True


class Potion(ShopItem):
    def __init__(self, item_id, name, description, visible_after_floor):
        super().__init__(item_id, name, description, visible_after_floor, 'potions')

    def is_potion(self):
        return True


class FloorMap(ShopItem):
    def __init__(self, item_id, name, description, visible_after_floor, shop_category):
        super().__init__(item_id, name, description, visible_after_floor, shop_category, False)

    def is_floor_map(self):
        return True
