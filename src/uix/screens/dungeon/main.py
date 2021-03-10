# UIX Imports
from refs import Refs
from uix.modules.screen import Screen
from uix.screens.character_display.portfolio import CharacterPortfolio

# Kivy Imports
from kivy.properties import NumericProperty, BooleanProperty

# KV Import
from loading.kv_loader import load_kv
load_kv(__name__)


class DungeonMain(Screen):
    party_score = NumericProperty(0)
    level = NumericProperty(0)
    boss = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def initialize_data(self, dt):
        current_party_index = 0
        for index in range(0, 10):
            self.ids.portfolio.add_widget(CharacterPortfolio(self.manager.app, self, current_party_index, party=self.content.get_party(index), party_index=index))
        #self.ids.indexer.update_sources(self.content.get_current_party_index())
        self.ids.indexer.bind(on_click=self.on_click)

    def on_click(self, instance, index):
        self.ids.portfolio.load_slide(self.ids.portfolio.slides[index])

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

    def reload(self):
        self.ids.portfolio.reload()
        self.update_party_score()

    def update_party_score(self):
        self.party_score = self.content.get_current_party_score()

    def on_widget_move(self, index):
        self.content.set_current_party_index(0 if index is None else index)
        self.ids.portfolio.reload()
        self.update_party_score()

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
        pass

    def add_bonus(self):
        current_party = self.content.get_current_party()
        for x in range(200):
            self.content.generate_familiarity_bonuses(current_party)
        self.manager.clean_whitelist()

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
        current_floor = str(self.level)
        next_floor = str(self.level + 1)
        Refs.gp.display_popup(self, 'dm_confirm', True, current_floor, next_floor, self.party_score, on_confirm=lambda *args: self.do_confirm(True))

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