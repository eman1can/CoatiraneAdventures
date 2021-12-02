# UIX Imports
# KV Import
from kivy.clock import Clock
from kivy.properties import BooleanProperty, NumericProperty, ObjectProperty, StringProperty
from kivy.uix.recycleview import RecycleView
from kivy.uix.relativelayout import RelativeLayout
from loading.kv_loader import load_kv
from refs import Refs
from uix.modules.headers import time_header
from uix.modules.screen import Screen
from uix.screens.header_screen import HeaderScreen

load_kv(__name__)


class InventoryItem(RelativeLayout):
    name = StringProperty('Default')
    description = StringProperty('I am an item.')
    is_single = BooleanProperty(True)

    tint = NumericProperty(0)

    count = NumericProperty(1)

    portrait_source = StringProperty('res/uix/items/empty.png')
    background_source = StringProperty('res/uix/items/frame_1.png')

    callback = ObjectProperty(None, allownone=True)
    button_disabled = BooleanProperty(True)

    def on_name(self, instance, name):
        self.portrait_source = f'res/uix/items/{name}.png'


class InventoryItemList(RecycleView):
    pass


class InventoryMain(HeaderScreen):
    def on_enter(self):
        Clock.schedule_interval(self.update_time_header, 5)
        inventory_items = Refs.gc.get_inventory().get_items()
        items = []
        for item in inventory_items:
            name, description = item.get_display()
            if item.get_own_multiple():
                count = Refs.gc.get_inventory().get_item_count(item.get_id())
                items.append({'name': name, 'description': description, 'is_single': False, 'count': count})
            else:
                items.append({'name': name, 'description': description, 'is_single': True})

        self.ids.inventory_items.data = items
