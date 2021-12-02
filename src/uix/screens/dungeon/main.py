# UIX Imports
# Kivy Imports
from kivy.properties import BooleanProperty, NumericProperty

# KV Import
from loading.kv_loader import load_kv
from refs import Refs
from uix.modules.screen import Screen
from uix.screens.character_display.portfolio import CharacterPortfolio

load_kv(__name__)


class DungeonMain(Screen):
    party_score = NumericProperty(0)
    level = NumericProperty(0)
    boss = BooleanProperty(False)
    locked = BooleanProperty(False)
    at_entrance = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.portfolio.locked = self.locked

    def reload(self, **kwargs):
        self.set_kwargs(kwargs)
        self.ids.portfolio.reload(locked=self.locked)
        self.update_party_score()
        self.update_level_label()

    def set_kwargs(self, kwargs):
        for key in list(kwargs.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs.pop(key))

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.ids.portfolio.bind(on_index_update=self.on_snap_carousel_index)
        self.ids.indexer.bind(on_button=self.on_indexer_index)
        current_party_index = self.content.get_current_party_index()
        for index in range(0, 10):
            self.ids.portfolio.add_widget(CharacterPortfolio(party_index=index, locked=self.locked, current=(current_party_index == index)))
        self.ids.indexer.select_index(current_party_index)
        self.update_level_label()

    def update_party_score(self):
        self.party_score = self.content.get_current_party_score()

    def on_level(self, *args):
        self.update_level_label()

    def on_boss(self, *args):
        self.update_level_label()

    def update_level_label(self):
        if 'level_label' not in self.ids:
            return
        if self.boss:
            self.ids.level_label.text = '[color=ff0000][b]Boss[/b][/color]'
        elif self.level == 0:
            self.ids.level_label.text = 'Level - Surface'
        else:
            self.ids.level_label.text = f'Level - {self.level}'

    def on_indexer_index(self, instance, index):
        self.ids.portfolio.load_index(index)

    def on_snap_carousel_index(self, instance, index):
        self.content.set_current_party_index(index)
        if self.ids.indexer.index != index:
            self.ids.indexer.select_index(index)
        self.ids.portfolio.reload()
        self.update_party_score()

    def on_enter(self, *args):
        self.ids.arrows.animate_arrows()
        super().on_enter()

    def on_leave(self, *args):
        self.ids.arrows.un_animate_arrows()
        super().on_leave()

    def on_gear(self):
        if not self.ids.gear_button.disabled:
            self.close_hints()
            self.manager.display_screen('gear_change', True, True)

    def on_inventory(self):
        if Refs.gp.is_popup_open('inventory'):
            Refs.gp.close_popup('inventory')
        else:
            Refs.gp.display_popup(self, 'inventory')

    def on_back_press(self):
        if super().on_back_press():
            self.close_hints()

    def close_hints(self):
        self.ids.portfolio.close_hints()

    def on_descend(self):
        if self.level == 0:
            count = 0
            for char in self.content.get_current_party():
                if char is not None:
                    count += 1
            if count == 0:
                return
        floor_score, party_score = Refs.gc.get_floor_score(self.level + 1), Refs.gc.get_current_party_score()
        Refs.gp.display_popup(self, 'dm_confirm', current_floor=self.level, next_floor=self.level + 1, rec_score=floor_score, act_score=party_score, on_confirm=lambda *args: self.do_confirm(True))

    def do_confirm(self, descending):
        if descending:
            self.do_descend()
        else:
            self.do_ascend()

    def dismiss_confirm(self, *args):
        self.confirm_open = False

    def do_descend(self):
        self.close_hints()
        self.level += 1
        Refs.gc.set_next_floor(True)
        Refs.gc.save_game(None)
        self.manager.display_screen('dungeon_battle', True, False, self.level, self.boss, {})

    def on_ascend(self):
        if not self.ids.ascend_button.disabled:
            floor_score, party_score = Refs.gc.get_floor_score(self.level - 1), Refs.gc.get_current_party_score()
            Refs.gp.display_popup(self, 'dm_confirm', current_floor=self.level, next_floor=self.level - 1, rec_score=floor_score, act_score=party_score, on_confirm=lambda *args: self.do_confirm(True))

    def do_ascend(self):
        self.close_hints()
        self.level -= 1
        Refs.gc.set_next_floor(False)
        Refs.gc.save_game(None)
        self.manager.display_screen('dungeon_battle', True, False, self.level, self.boss, {})

    def on_fight(self):
        self.manager.display_screen('dungeon_battle', True, False, self.level, self.boss, {})
