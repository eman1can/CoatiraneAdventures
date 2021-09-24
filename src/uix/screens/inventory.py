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


class InventoryMain(Screen):
    def on_enter(self):
        Clock.schedule_interval(self.update_time_header, 5)
        inventory_items = Refs.gc.get_inventory().get_items()
        items = []
        for item in inventory_items:
            if item.is_single():
                name, desc, price = item.get_display()
                items.append({'name': name, 'description': desc, 'is_single': True})
            else:
                name, desc, min_price, max_price = item.get_display()
                count = Refs.gc.get_inventory().get_item_count(item.get_id())
                items.append({'name': name, 'description': desc, 'is_single': False, 'count': count})
        self.ids.inventory_items.data = items

    def on_leave(self):
        Clock.unschedule(self.update_time_header)

    def update_time_header(self, dt):
        self.ids.time_header.text = time_header()


