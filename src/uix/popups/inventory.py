from kivy.properties import ObjectProperty, StringProperty

from kivy.uix.relativelayout import RelativeLayout
from loading.kv_loader import load_kv
from refs import Refs
from uix.popups.view import View

load_kv(__name__)


class EquippedItem(RelativeLayout):
    type = StringProperty('None')

    background_source = StringProperty('res/uix/items/frame_1.png')
    portrait_source = StringProperty('res/uix/items/ring_2.png')

    name = StringProperty('No - Equipped')
    description = StringProperty('')

    def __init__(self, **kwargs):
        self.register_event_type('on_change_item')
        super().__init__(**kwargs)
        self.item = None

    def on_type(self, instance, type):
        self.name = f'No {self.type} Equipped'

    def set_item(self, item):
        self.item = item
        self.name = item.get_name()
        self.description = item.get_description()
        self.portrait_source = f'res/uix/items/{item.get_material_id()}_{item.get_id()}.png'
        self.ids.portrait.opacity = 1
        self.ids.background.opacity = 1
        self.ids.description.opacity = 1

    def on_change_item(self):
        pass


class Inventory(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_item = None

    def on_pre_open(self):
        inventory = Refs.gc.get_inventory()
        pickaxe = inventory.get_current_pickaxe()
        if pickaxe is not None:
            self.ids.pickaxe.set_item(pickaxe)
        self.ids.pickaxe.bind(on_change_item=self.on_change_pickaxe)
        shovel = inventory.get_current_shovel()
        if shovel is not None:
            self.ids.shovel.set_item(pickaxe)
        self.ids.shovel.bind(on_change_item=self.on_change_shovel)
        harvesting_knife = inventory.get_current_harvesting_knife()
        if harvesting_knife is not None:
            self.ids.knife.set_item(harvesting_knife)
        self.ids.knife.bind(on_change_item=self.on_change_knife)

        items = []
        for item in inventory.get_items():
            if item.is_single():
                name, desc, price = item.get_display()
                items.append({'item': item, 'name': name, 'description': desc, 'is_single': True, 'tint': 0, 'button_disabled': True})
            else:
                name, desc, min_price, max_price = item.get_display()
                count = Refs.gc.get_inventory().get_item_count(item.get_id())
                items.append({'item': item, 'name': name, 'description': desc, 'is_single': False, 'count': count, 'tint': 0, 'button_disabled': True})
        self.ids.inventory_items.data = items

    def on_pre_dismiss(self):
        self.manager.previous.refresh_harvest()

    def on_change_pickaxe(self, instance):
        if self.selected_item == 'pickaxe':
            self.unselect_items()
            return
        self.on_change_item(instance, 'pickaxe')
        self.selected_item = 'pickaxe'

    def on_change_shovel(self, instance):
        if self.selected_item == 'shovel':
            self.unselect_items()
            return
        self.on_change_item(instance, 'shovel')
        self.selected_item = 'shovel'

    def on_change_knife(self, instance):
        if self.selected_item == 'knife':
            self.unselect_items()
            return
        self.on_change_item(instance, 'harvesting_knife')
        self.selected_item = 'knife'

    def on_change_item(self, instance, type):
        items = self.ids.inventory_items.data
        full_id = None
        if instance.item is not None:
            full_id = instance.item.get_full_id()
        for item in items:
            if item['item'].get_id() != type or item['item'].get_full_id() == full_id:
                item['tint'] = 0.5
                item['button_disabled'] = True
            else:
                item['tint'] = 0
                item['button_disabled'] = False
                item['callback'] = lambda obj=item['item']: self.select_item(obj)
        self.ids.inventory_items.data = items
        self.ids.inventory_items.refresh_from_data()

    def unselect_items(self):
        items = self.ids.inventory_items.data
        for item in items:
            item['tint'] = 0
            item['button_disabled'] = True
            item['callback'] = None
        self.ids.inventory_items.data = items
        self.ids.inventory_items.refresh_from_data()
        self.selected_item = None

    def select_item(self, item):
        self.unselect_items()
        inventory = Refs.gc.get_inventory()
        if item.get_id() == 'pickaxe':
            self.ids.pickaxe.set_item(item)
            inventory.set_current_pickaxe(item.get_hash())
        elif item.get_id() == 'shovel':
            self.ids.shovel.set_item(item)
            inventory.set_current_shovel(item.get_hash())
        elif item.get_id() == 'harvesting_knife':
            self.ids.knife.set_item(item)
            inventory.set_current_harvesting_knife(item.get_hash())