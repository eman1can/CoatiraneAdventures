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

    def on_kv_post(self, base_widget):
        self.ids.portfolio.bind(on_index_update=self.on_snap_carousel_index)
        self.ids.indexer.bind(on_button=self.on_indexer_index)
        current_party_index = self.content.get_current_party_index()
        for index in range(0, 10):
            self.ids.portfolio.add_widget(CharacterPortfolio(party_index=index, locked=self.locked, current=(current_party_index == index)))
        self.ids.indexer.select_index(current_party_index)

    def on_indexer_index(self, instance, index):
        # print(instance, index)
        self.ids.portfolio.load_index(index)

    def on_snap_carousel_index(self, instance, index):
        # print('Current party is ', index)
        self.content.set_current_party_index(index)
        if self.ids.indexer.index != index:
            self.ids.indexer.select_index(index)
        self.ids.portfolio.reload()
        self.update_party_score()

    # def on_touch_hover(self, touch):
    #     if self.confirm_open:
    #         return False
    #     return self.dispatch_to_relative_children(touch)

    def on_enter(self, *args):
        self.ids.arrows.animate_arrows()
        self.update_buttons()
        self.reload()
        super().on_enter()

    def on_leave(self, *args):
        self.ids.arrows.un_animate_arrows()
        super().on_leave()

    def reload(self, **kwargs):
        for kw, arg in kwargs.items():
            if hasattr(self, kw):
                setattr(self, kw, arg)
        self.ids.portfolio.reload()
        self.update_party_score()

    def update_party_score(self):
        self.party_score = self.content.get_current_party_score()

    def update_buttons(self):
        if self.level == 0:
            self.ids.back_button.disabled = False
            self.ids.back_button.opacity = 1
            self.ids.ascend_lock.opacity = 1
            self.ids.gear_lock.opacity = 0
            self.ids.ascend_button.disabled = True
            self.ids.gear_button.disabled = False
            #self.ids.portfolio.update_lock(False)
        else:
            self.ids.back_button.disabled = True
            self.ids.back_button.opacity = 0
            self.ids.ascend_lock.opacity = 0
            self.ids.gear_lock.opacity = 1
            self.ids.ascend_button.disabled = False
            self.ids.gear_button.disabled = True
            #self.ids.portfolio.update_lock(True)

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
        floor_score, party_score = Refs.gc.get_floor_score(True), Refs.gc.get_current_party_score()
        Refs.gp.display_popup(self, 'dm_confirm', current_floor=str(self.level), next_floor=str(self.level + 1), rec_score=floor_score, act_score=party_score, on_confirm=lambda *args: self.do_confirm(True))

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
        self.update_buttons()
        descend = False
        for x in self.content.get_current_party():
            if not x == None:
                descend = True
        if descend:
            Refs.gc.set_next_floor(True)
            Refs.gc.save_game(None)
            print("Delving into the dungeon")
            self.manager.display_screen('dungeon_battle', True, False, self.level, self.boss, {})
        else:
            print("Not enough Characters to explore")

    def on_ascend(self):
        if not self.ids.ascend_button.disabled:
            current_floor = str(self.level)
            next_floor = str(self.level - 1)
            if self.level - 1 == 0:
                next_floor = 'Surface'
            Refs.gp.create_popup(self, 'dm_confirm', False, current_floor, next_floor, self.party_score, on_confirm=lambda *args: self.do_confirm(False))

    def do_ascend(self):
        # self.confirm.current_floor = str(self.level - 1)
        self.close_hints()
        self.level -= 1
        self.update_buttons()
        Refs.gc.set_next_floor(False)
        # # print("Ascend")
        # if len(shownparty) > 0:
        #     print("Ascending from dungeon")
        #     self.level = self.level - 1
        #     if (self.level < 2):
        #         print('disabling ascend')
        #         self.ids['ascend'].disabled = True
        #         self.ids['ascend_text'].text = '[s]Ascend[/s]'
        #     else:
        #         print('enabling ascend')
        #         self.ids['ascend_text'].text = 'Ascend'
        #         self.ids['ascend'].disabled = False
        # else:
        #     print("not enough Characters to explore")