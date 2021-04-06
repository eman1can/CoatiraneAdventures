from game.equipment import CAN_DUAL_WIELD, OFF_HAND_WEAPON, WEAPON


class Inventory:
    def __init__(self, items, drop_items, equipment, metadata):
        self._items = {}
        self._has_metadata = {}

        for item_id, item in items.items():
            self._items[item_id] = {}

            if item_id in metadata:
                self._items[item_id]['count'] = metadata[item_id]['count']
            else:
                self._items[item_id]['count'] = 0
            self._items[item_id]['class'] = item
            self._has_metadata[item_id] = False

        for item_id, drop_item in drop_items.items():
            self._items[item_id] = {}

            if item_id in metadata:
                self._items[item_id]['count'] = metadata[item_id]['count']
            else:
                self._items[item_id]['count'] = 0
            self._items[item_id]['class'] = drop_item
            self._has_metadata[item_id] = False

        for item_id, equipment in equipment.items():
            self._items[item_id] = {}

            if item_id in metadata:
                self._items[item_id]['count'] = metadata[item_id]['count']
            else:
                self._items[item_id]['count'] = 0
            self._items[item_id]['class'] = equipment
            self._items[item_id]['items'] = {}

            if item_id in metadata:
                for item_hash, item_metadata in metadata[item_id]['items'].items():
                    item = self._items[item_id]['class'].new_instance(item_metadata)
                    self._items[item_id]['items'][item.get_hash()] = item

            self._has_metadata[item_id] = True

        self._current_pickaxe = None
        self._current_shovel = None
        self._current_harvesting_knife = None
        if metadata['current_pickaxe_hash'] is not None:
            self._current_pickaxe = self._items['pickaxe']['items'][metadata['current_pickaxe_hash']]
        if metadata['current_shovel_hash'] is not None:
            self._current_shovel = self._items['shovel']['items'][metadata['current_shovel_hash']]
        if metadata['current_harvesting_knife_hash'] is not None:
            self._current_harvesting_knife = self._items['harvesting_knife']['items'][metadata['current_harvesting_knife_hash']]

    def get_save_output(self):
        pickaxe_hash = shovel_hash = harvesting_knife_hash = None
        if self._current_pickaxe is not None:
            pickaxe_hash = self._current_pickaxe.get_hash()
        if self._current_shovel is not None:
            shovel_hash = self._current_shovel.get_hash()
        if self._current_harvesting_knife is not None:
            harvesting_knife_hash = self._current_harvesting_knife.get_hash()
        output = {
            'current_pickaxe_hash':          pickaxe_hash,
            'current_shovel_hash':           shovel_hash,
            'current_harvesting_knife_hash': harvesting_knife_hash
        }
        for item_id, metadata in self._items.items():
            if metadata['count'] == 0:
                continue
            output[item_id] = {'count': metadata['count']}
            if self._has_metadata[item_id]:
                output[item_id]['items'] = {}
                for item_hash, item in metadata['items'].items():
                    output[item_id]['items'][item_hash] = item.get_metadata()
        return output

    def add_item(self, item_id, count, metadata=None):
        if not self._has_metadata[item_id]:
            self._items[item_id]['count'] += count
        else:
            self._items[item_id]['count'] += count
            for _ in range(count):
                item = self._items[item_id]['class'].new_instance(metadata)
                self._items[item_id]['items'][item.get_hash()] = item

    def remove_item(self, item_id, count, hash=None):
        if self._has_metadata[item_id]:
            if hash is None:
                raise Exception('Can\'t remove metadataed item with no hash')
            else:
                self._items[item_id]['count'] -= 1
                self._items[item_id]['items'].pop(hash)
        else:
            self._items[item_id]['count'] -= count

    def get_item(self, item_id, hash=None):
        if self._has_metadata:
            if hash is None:
                return self._items[item_id]['items']
            else:
                return self._items[item_id]['items'][hash]
        else:
            return self._items[item_id]['class']

    def get_items(self):
        items = []
        for item_id, metadata in self._items.items():
            if metadata['count'] > 0:
                if self._has_metadata[item_id]:
                    items += list(metadata['items'].values())
                else:
                    items.append(metadata['class'])
        return items

    def get_equipment(self, equipment_type):
        items = []
        for item_id, item_data in self._items.items():
            if not self._has_metadata[item_id]:
                continue
            for item in item_data['items'].values():
                print(item.get_name(), item.get_sub_type(), equipment_type)
                if equipment_type == WEAPON and item.is_weapon():
                    items.append(item)
                elif equipment_type == OFF_HAND_WEAPON and item.is_weapon() and CAN_DUAL_WIELD[item.get_sub_type()]:
                    items.append(item)
                elif item.is_armor() and equipment_type == item.get_sub_type():
                    items.append(item)
        return items

    def get_metadata_items(self, item_id):
        return list(self._items[item_id]['items'].values())

    def get_id_list(self):
        return list(self._items.keys())

    def get_item_count(self, item_id, metadata=None):
        if metadata is not None:
            count = 0
            for item in self._items[item_id]['items'].values():
                same = True
                for key in metadata.keys():
                    same &= metadata[key] == item.get_metadata()[key]
                if same:
                    count += 1
        else:
            return self._items[item_id]['count']

    def has_item(self, item_id):
        return self._items[item_id]['count'] > 0

    def get_current_pickaxe(self):
        return self._current_pickaxe

    def has_pickaxe(self):
        return len(self._items['pickaxe']['items']) > 0

    def get_current_shovel(self):
        return self._current_shovel

    def has_shovel(self):
        return len(self._items['shovel']['items']) > 0

    def get_current_harvesting_knife(self):
        return self._current_harvesting_knife

    def has_harvesting_knife(self):
        return len(self._items['harvesting_knife']['items']) > 0

    def set_current_pickaxe(self, item_hash):
        if item_hash is None:
            self._current_pickaxe = None
            return None
        else:
            self._current_pickaxe = self._items['pickaxe']['items'][item_hash]
            return self._current_pickaxe

    def set_current_shovel(self, item_hash):
        if item_hash is None:
            self._current_shovel = None
            return None
        else:
            self._current_shovel = self._items['shovel']['items'][item_hash]
            return self._current_shovel

    def set_current_harvesting_knife(self, item_hash):
        if item_hash is None:
            self._current_harvesting_knife = None
            return None
        else:
            self._current_harvesting_knife = self._items['harvesting_knife']['items'][item_hash]
            return self._current_harvesting_knife
