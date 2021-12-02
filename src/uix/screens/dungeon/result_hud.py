from kivy.properties import BooleanProperty, DictProperty, ListProperty, NumericProperty, StringProperty

from game.enemy import NICKNAMES
from kivy.uix.relativelayout import RelativeLayout
from loading.kv_loader import load_kv

load_kv(__name__)


class ResultListItem(RelativeLayout):
    name = StringProperty('')
    count = NumericProperty(0)
    color = ListProperty([1, 1, 1, 1])

    background_source = StringProperty('res/uix/items/frame_1.png')
    portrait_source = StringProperty('res/uix/items/empty.png')

    def on_name(self, instance, value):
        self.background_source = f'res/uix/items/frame_1.png'
        self.portrait_source = f'res/uix/items/{value}.png'


class EnemyListItem(ResultListItem):
    def on_name(self, instance, value):
        for index, nickname in enumerate(NICKNAMES[1:]):
            if value.startswith(nickname):
                self.background_source = f'res/uix/items/frame_{int((index + 1) / 3) + 1}.png'
                monster_name = value[len(nickname):].lower().replace(" ", "_")
                if index < 5:
                    self.portrait_source = f'res/uix/items/{monster_name}_{index + 2}.png'
                else:
                    self.portrait_source = f'res/uix/items/{monster_name}_{index - 1}.png'
                return
        self.background_source = f'res/uix/items/frame_1.png'
        self.portrait_source = f'res/uix/items/{value} 1.png'


class ResultHud(RelativeLayout):
    encounter = BooleanProperty(True)

    def __init__(self, **kwargs):
        self.register_event_type('on_continue')
        self.register_event_type('on_harvest')
        super().__init__(**kwargs)

    def on_continue(self):
        pass

    def on_harvest(self):
        pass

    def disable_harvest(self):
        self.ids.harvest.text = 'You need a Harvesting Knife to gather materials'
        self.ids.harvest_button.disabled = True

    def enable_harvest(self):
        self.ids.harvest.text = 'Harvest Materials'
        self.ids.harvest_button.disabled = False

    def reset(self):
        self.ids.items_title.opacity = 0
        self.ids.item_list.opacity = 0
        self.ids.harvest.opacity = 1
        self.ids.harvest.text = 'Harvest Materials'
        self.ids.harvest_button.disabled = False
        self.ids.button.disabled = True
        self.ids.enemy_list.data = []
        self.ids.item_list.data = []

    def set_enemies_defeated(self, enemies):
        enemy_list = {}
        for (name, count) in enemies.items():
            if name not in enemy_list:
                enemy_list[name] = {'name': name, 'count': 0, 'color': (1, 1, 1, 1) if self.encounter else (0, 0, 0, 1)}
            enemy_list[name]['count'] += count
        self.ids.harvest.text = 'Harvest Materials'
        self.ids.button.disabled = False
        self.ids.enemy_list.data = list(enemy_list.values())
        self.ids.enemy_list.refresh_from_data()

    def set_items_obtained(self, items):
        self.ids.items_title.opacity = 1
        self.ids.item_list.opacity = 1
        self.ids.harvest.opacity = 0
        self.ids.harvest_button.disabled = True
        list = []
        for item, count in items.items():
            list.append({'name': item.get_name(), 'count': count, 'color': (1, 1, 1, 1) if self.encounter else (0, 0, 0, 1)})
        self.ids.item_list.data = list
        self.ids.item_list.refresh_from_data()

    def continue_click(self):
        self.dispatch('on_continue')
