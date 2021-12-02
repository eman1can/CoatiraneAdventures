from copy import copy
from math import floor

from kivy.clock import Clock
from kivy.properties import BooleanProperty, ListProperty, NumericProperty, ObjectProperty, OptionProperty, StringProperty
from kivy.uix.relativelayout import RelativeLayout

from game.equipment import EQUIPMENT_TYPES
from loading.kv_loader import load_kv
from refs import Refs
from spine.animation.animationstate import AnimationState
from spine.animation.animationstatedata import AnimationStateData
from spine.skeleton.skeletonloader import SkeletonLoader
from spine.skeleton.skeletonrenderer import SkeletonRenderer
from uix.modules.spine_display import SpineDisplay
from uix.screens.header_screen import HeaderScreen

load_kv(__name__)


class Shop(HeaderScreen):
    header = StringProperty('')
    sub_header = StringProperty('')
    page_data = ListProperty([])
    transaction_visible = BooleanProperty(False)

    def __init__(self, page, **kwargs):
        self._page = page
        self._bstype = None
        self._last = []

        self._displayed_transaction = None
        self._calculated_transaction = None

        self.title_source = ''

        super().__init__(**kwargs)

        floor_cap = min(len(Refs.gc['floors']), Refs.gc.get_lowest_floor()) + 1
        self.pages = {
            'main':                ['general', 'dungeon_materials', 'ingredients', 'potions_medicines', 'equipment', 'home_supplies'],
            'general':             ['floor_maps'],
            'equipment':           ['tools', 'weapons', 'armors'],
            'tools':               [],
            'weapons':             [],
            'armors':              [],
            'dungeon_materials':   [],
            'magic_stones':        [],
            'monster_drops':       [],
            'raw_materials':       [],
            'processed_materials': [],
            'ingredients':         [],
            'potions_medicines':   [],
            'home_supplies':       [],
            'floor_maps':          [f'floor_{floor_id}' for floor_id in range(1, floor_cap)]
        }

        self.titles = {
            'main': 'screen_title/shop.png',
            'general': 'screen_title/shop_general.png',
            'equipment': 'screen_title/shop_equipment.png',
            'tools': 'screen_title/shop_tools.png',
            'weapons': 'screen_title/shop_weapons.png',
            'armors': 'screen_title/shop_armors.png',
            'dungeon_materials': 'screen_title/shop_materials.png',
            'magic_stones': 'screen_title/shop_magic_stones.png',
            'monster_drops': 'screen_title/shop_materials.png',
            'raw_materials': 'screen_title/shop_materials.png',
            'processed_materials': 'screen_title/shop_materials.png',
            'ingredients': 'screen_title/shop_ingredients.png',
            'potions_medicines': 'screen_title/shop_potions.png',
            'home_supplies': 'screen_title/shop_home_supplies.png',
            'floor_maps': 'screen_title/shop_floor_maps.png',
        }

        self.headers = {
            'main':       'Welcome to the Guild Shopping District!',
            'general':    'Welcome to the General shop!',
            'floor_maps': 'Welcome to the Map shop!',
            'equipment':  'Welcome to the equipment district!'
        }

        self.sub_headers = {
            'main':              'Where you you like to browse today?',
            'equipment':         'What form of equipment are you looking for?',
            'tools':             'What kind of tool are you looking for?',
            'weapons':           'What kind of weapon are you looking for?',
            'armors':            'What kind of armor are you looking for?',
            'general':           'What would you like to purchase?',
            'floor_maps':        'Which floor are you interested in?',
            'dungeon_materials': 'Which type of transaction would you like?'
        }

        self.page_to_string = {
            'main':                'Central Market',
            'general':             'General Goods',
            'dungeon_materials':   'Dungeon Materials',
            'ingredients':         'Ingredients',
            'potions_medicines':   'Potions & Medicines',
            'equipment':           'Equipment',
            'tools':               'Tools',
            'weapons':             'Weapons',
            'armors':              'Armor',
            'home_supplies':       'Home Supplies',
            'other':               'Other',
            'floor_maps':          'Floor Maps',
            'monster_drops':       'Monster Drop',
            'magic_stones':        'Magic Stone',
            'raw_materials':       'Raw Material',
            'processed_materials': 'Processed Material'
        }

        self.page_to_image = {
            'main':                '',
            'general':             'icons/general.png',
            'dungeon_materials':   'items/coal/ore.png',
            'ingredients':         'items/cotton/cloth.png',
            'potions_medicines':   'icons/potion.png',
            'equipment':           'icons/equipment.png',
            'tools':               'icons/tools.png',
            'weapons':             'icons/weapons.png',
            'armors':              'icons/equipment.png',
            'home_supplies':       'icons/home_supplies.png',
            'other':               'Other',
            'floor_maps':          'icons/floor_maps.png',
            'monster_drops':       'items/infant_dragon_meat.png',
            'magic_stones':        'items/regular_large_magic_stone.png',
            'raw_materials':       'items/coal/ore.png',
            'processed_materials': 'items/kobold_hide_processed.png'
        }

        self.bspages = {'dungeon_materials': ['magic_stones', 'monster_drops', 'raw_materials', 'processed_materials']}

        self.item_lists = {
            'general':             Refs.gc.get_shop_items,
            'ingredients':         lambda category: Refs.gc.get_ingredients(),
            'magic_stones':        lambda category: Refs.gc.get_magic_stone_types(),
            'monster_drops':       lambda category: Refs.gc.get_monster_drop_types(),
            'raw_materials':       lambda category: Refs.gc.get_raw_materials(),
            'processed_materials': lambda category: Refs.gc.get_processed_materials()
        }

        self.texts = {
            'sell_start':   'Which of your {0}s would you like to sell?',
            'sell_fail':    'You do not have any {0}s that you can sell.',
            'sell_current': 'Current going price',
            'sell_future':  'You will get',
            'buy_start':    'What type of {0} would you like to buy?',
            'buy_fail':     'No items are available to purchase',
            'buy_current':  'Current price',
            'buy_future':   'This will cost'
        }

        for floor_id in range(1, floor_cap):
            self.page_to_string[f'floor_{floor_id}'] = f'Floor {floor_id}'
            self.page_to_image[f'floor_{floor_id}'] = 'shop/floor_map.png'
            self.pages[f'floor_{floor_id}'] = []
            self.headers[f'floor_{floor_id}'] = 'Which map type are you interested in?'
            self.item_lists[f'floor_{floor_id}'] = Refs.gc.get_floor_maps
            self.titles[f'floor_{floor_id}'] = 'screen_title/shop_floor_maps.png'

        equipment_lists = {
            'tools':   Refs.gc.get_store_tools,
            'weapons': Refs.gc.get_store_weapons,
            'armors':  Refs.gc.get_store_armor
        }

        for page_link in ['equipment', 'tools', 'weapons', 'armors']:
            for item_id, equipment_class in Refs.gc['equipment'].items():
                equipment_category = EQUIPMENT_TYPES[equipment_class.get_type()].lower() + 's'
                if equipment_category != page_link:
                    continue
                # print([x.get_id() for x in Refs.gc.get_store_tools(item_id)])
                self.pages[equipment_category].append(item_id)
                self.pages[item_id] = []
                self.titles[item_id] = f'{item_id}'
                self.headers[item_id] = f''
                self.page_to_string[item_id] = equipment_class.get_name()
                # for specific_item in Refs.gc.get_store_tools(item_id):
                #     self.pages[specific_item.get_id()] = []

                self.item_lists[item_id] = lambda category, page_name=item_id, callback=equipment_lists[equipment_category]: callback(page_name)

        # for page_link in Refs.gc['equipment'].keys():
        #     equipment_class = Refs.gc['equipment'][page_link]
        #     equipment_category = EQUIPMENT_TYPES[equipment_class.get_type()].lower() + 's'
        #     self.pages[page_link] = []
        #     self.titles[page_link] = self.titles[self._last[-1]]
        #     self.headers[page_link] = f'What kind of {equipment_class.get_name()} are you interested in?\n\n'
        #     self.item_lists[page_link] = list_links[equipment_category]

        self.display_page()

    def on_enter(self):
        frame_rate = 30
        Clock.schedule_interval(self.ids.spine_display.update, 1 / frame_rate)

    def on_leave(self):
        Clock.unschedule(self.ids.spine_display.update)

    def after_transaction(self):
        self.reload(self._page)

    def reload(self, page):
        self._page = page

        self.display_page()

    def display_previous(self):
        self._last.pop()
        page = self._last.pop()
        self.reload(page)

    def display_page(self):
        self._bstype = None
        if self._page.startswith('buy') or self._page.startswith('sell'):
            self._bstype = self._page[:self._page.index('_')]
            self._page = self._page[self._page.index('_') + 1:]

        page_list = self.pages[self._page]

        if self._page in self.headers:
            self.header = self.headers[self._page]
        else:
            self.header = ''

        if self._page in self.sub_headers:
            self.sub_header = self.sub_headers[self._page]
        else:
            self.sub_header = ''

        self.title_source = self.titles[self._page]

        self.page_data = []
        for page_link in page_list:
            if page_link in Refs.gc['equipment']:
                self.page_to_image[page_link] = f'items/default/{page_link}.png'
            data = {
                'mode': 'page',
                'text': self.page_to_string[page_link],
                'sub_text': '',
                'image_source': self.page_to_image[page_link],
                'price': '',
                'button_disabled': False,
                'inventory': '',
                'callback': lambda link=page_link: self.reload(link)
            }
            self.page_data.append(data)

        if self._page in self.bspages:
            for bspage_link in self.bspages[self._page]:
                for type in ['sell', 'buy']:
                    page_link = f'{type}_{bspage_link}'
                    page_text = f'{type.title()} {self.page_to_string[bspage_link]}'
                    data = {
                        'mode': 'page',
                        'text': page_text,
                        'sub_text': '',
                        'image_source': self.page_to_image[bspage_link],
                        'price': '',
                        'button_disabled': False,
                        'inventory': '',
                        'callback': lambda link=page_link: self.reload(link)
                    }
                    self.page_data.append(data)

        if self._page in self.item_lists:
            items = self.item_lists[self._page](self._page)

            if self._bstype == 'sell':
                self.sub_header = self.texts['sell_start'].format(self.page_to_string[self._page])
                items = Refs.gc.get_owned_items(items)
            elif self._bstype == 'buy':
                self.sub_header = self.texts['buy_start'].format(self.page_to_string[self._page])

            for item in items:
                data = {'mode': 'item', 'button_disabled': False, 'inventory': ''}
                name, description = item.get_display()
                price = Refs.gc.get_market_price(item.get_id())

                data['price'] = f'{price}V'
                data['text'] = name
                data['sub_text'] = description
                data['image_source'] = item.get_image()
                data['callback'] = lambda titem=item: self.do_transaction(titem)

                if item.is_item():
                    item_id = item.get_id()
                    metadata = None
                else:
                    item_id = item.get_base_id()
                    metadata = {'material_id': item.get_material_id()}

                if item.get_own_multiple():
                    data['inventory'] = f'{Refs.gc.get_inventory().get_item_count(item_id, metadata)} in inventory'
                elif Refs.gc.get_inventory().has_item(item.get_id()):
                    data['price'] = 'Owned'
                    data['callback'] = lambda: None
                    data['button_disabled'] = True

                self.page_data.append(data)

        if len(self._last) != 0:
            last_page = self._last[-1]
            last_title = self.page_to_string[last_page]
            last_source = self.page_to_image[last_page]
            data = {
                'mode': 'page',
                'text': f'Back to {last_title}',
                'sub_text': '',
                'image_source': last_source,
                'price': '',
                'button_disabled': False,
                'inventory': '',
                'callback': lambda link=last_page: self.display_previous()
            }
            self.page_data.insert(0, data)

        if len(self._last) == 0 or self._last[-1] != self._page:
            self._last.append(self._page)

    def display_transaction(self, item, selling):
        if self.transaction_visible and self._displayed_transaction == item:
            self.transaction_visible = False
            self._displayed_transaction = None
            return
        self.transaction_visible = True
        self._displayed_transaction = item
        if self._calculated_transaction != item:
            self._calculated_transaction = item

            panel = self.ids.transaction_panel
            panel.set_item(self, item, selling)

    def do_transaction(self, item):
        selling = 'sell' == self._bstype
        self.display_transaction(item, selling)


class TransactionPanel(RelativeLayout):
    mode = OptionProperty('single', options=['single', 'multi'])
    text = StringProperty('')
    sub_text = StringProperty('')
    price = StringProperty('')
    image_source = StringProperty('')

    panel_height = NumericProperty(0)

    def __init__(self, **kwargs):
        self._screen = None
        self._item = None
        self.selling = False
        self._price = 0
        super().__init__(**kwargs)

    def set_item(self, screen, item, selling):
        self._screen = screen
        self._item = item
        self.selling = selling

        if item.get_own_multiple():
            self.panel_height = 0.5
        else:
            self.panel_height = 0.3
        self.display_transaction()

    def display_transaction(self):
        self.text, self.sub_text = self._item.get_display()
        self._price = Refs.gc.get_market_price(self._item.get_id())

        if not self._item.get_own_multiple():
            self.mode = 'single'
            self.image_source = self._item.get_image()
            count = 1
        else:
            self.mode = 'multi'
            if self.selling:
                count = Refs.gc.get_inventory().get_item_count(self._item.get_id())
                self._price = Refs.gc.get_market_sell_price(self._item.get_id())
                self.ids.confirm.text = 'Sell'
            else:
                varenth = Refs.gc.get_varenth()
                self._price = Refs.gc.get_market_buy_price(self._item.get_id())
                count = min(floor(varenth / self._price), 50)
                self.ids.confirm.text = 'Purchase'
        self.ids.slider.min = 1
        self.ids.slider.value = 1 + floor((count - 1) / 2)
        self.ids.slider.max = count
        self.update_price(count)

    def update_price(self, count):
        if self.selling:
            self.price = f'Receive: {count * self._price} V'
        else:
            self.price = f'Cost: {count * self._price} V'

    def do_transaction(self):
        count = self.ids.slider.value
        item_id = self._item.get_id()

        # Check if we have enough money
        if not self.selling and Refs.gc.get_market_buy_price(item_id) > Refs.gc.get_varenth():
            return

        # Adjust Inventory
        if self.selling:
            Refs.gc.get_inventory().remove_item(item_id, count)
        else:
            if self._item.is_equipment():
                Refs.gc.get_inventory().add_item(self._item.get_class().get_id(), count, {'material_id': self._item.get_material_id(), 'sub_material1_id': None, 'sub_material2_id': None, 'hash': None})
            else:
                Refs.gc.get_inventory().add_item(item_id, count)

        # Adjust Varenth
        if self.selling:
            Refs.gc.update_varenth(Refs.gc.get_market_sell_price(item_id) * count)
        else:
            Refs.gc.update_varenth(-Refs.gc.get_market_buy_price(item_id) * count)

        # If map, update map data
        if item_id.startswith('full_map') and not Refs.gc.get_inventory().has_item('path_' + item_id[len('full_'):]):
            Refs.gc.get_inventory().add_item('path_' + item_id[len('full_'):])
        if item_id.startswith('path_map'):
            floor_id = int(item_id[len('path_map_floor_'):])
            Refs.gc.get_floor(floor_id).get_map().unlock_path_map()
        elif item_id.startswith('full_map'):
            floor_id = int(item_id[len('full_map_floor_'):])
            Refs.gc.get_floor(floor_id).get_map().unlock_full_map()
        self._screen.after_transaction()


class ShopDisplay(RelativeLayout):
    mode = OptionProperty('page', options=['page', 'item'])
    text = StringProperty('')
    sub_text = StringProperty('')
    price = StringProperty('')
    inventory = StringProperty('')
    image_source = StringProperty('')
    callback = ObjectProperty(None)
    button_disabled = BooleanProperty(False)

    def do_callback(self, *args):
        if self.callback is None:
            return
        self.callback()
