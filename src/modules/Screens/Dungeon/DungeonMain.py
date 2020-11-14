from kivy.app import App
from kivy.animation import Animation
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty

from src.modules.GameMechanics import GameMechanics
from src.modules.KivyBase.Hoverable import ScreenBase as Screen
from src.modules.Screens.CharacterDisplay.CharacterPortfolio import CharacterPortfolio
from src.modules.Screens.Dungeon.modals import DMConfirmWidget


class DungeonMain(Screen):
    party_score = NumericProperty(0)
    level = NumericProperty(0)
    boss = BooleanProperty(False)

    animation_left = ObjectProperty(None, allownone=True)
    animation_right = ObjectProperty(None, allownone=True)
    animate_distance = NumericProperty(100)
    animate_start_left = NumericProperty(5)
    animate_start_right = NumericProperty(95)

    confirm_open = BooleanProperty(False)

    def __init__(self, **kwargs):
        self.confirm = DMConfirmWidget()
        self.confirm.current_floor = 'Surface'
        self.confirm.next_floor = '1'
        super().__init__(**kwargs)
        self.confirm.bind(on_confirm=self.do_confirm)
        self.confirm.bind(on_dismiss=self.dismiss_confirm)
        self.ids.portfolio.dungeon = self

        for index in range(0, len(App.get_running_app().main.parties) - 1):
            self.ids.portfolio.add_widget(CharacterPortfolio(party=App.get_running_app().main.parties[index + 1], party_index=(index + 1), dungeon=self))
        self.ids.indexer.bind(on_click=self.on_click)

    def on_click(self, instance, index):
        self.ids.portfolio.load_slide(self.ids.portfolio.slides[index])

    def on_touch_hover(self, touch):
        if self.confirm_open:
            return False
        return self.dispatch_to_relative_children(touch)

    def on_arrow_touch(self, direction):
        if direction:
            self.ids.portfolio.load_previous()
        else:
            self.ids.portfolio.load_next()

    def animate_arrows(self):
        if self.animation_left is None or self.animation_right is None:
            self.animation_left = Animation(x=self.animate_start_left - self.animate_distance, duration=1) + Animation(x=self.animate_start_left, duration=0.25)
            self.animation_right = Animation(x=self.animate_start_right + self.animate_distance, duration=1) + Animation(x=self.animate_start_right, duration=0.25)
        self.animation_left.repeat = True
        self.animation_right.repeat = True
        self.animation_left.start(self.ids.left_arrow)
        self.animation_right.start(self.ids.right_arrow)

    def unanimate_arrows(self):
        if self.animation_right is not None:
            self.animation_right.repeat = False
        if self.animation_left is not None:
            self.animation_left.repeat = False

    def on_enter(self, *args):
        self.animate_arrows()
        self.update_party_score()
        self.update_buttons()
        self.reload()

    def on_leave(self, *args):
        self.unanimate_arrows()

    def reload(self):
        self.ids.portfolio.reload()
        self.update_party_score()

    def update_party_score(self):
        party_score = self.ids.portfolio.get_party_score()
        if self.party_score != party_score:
            self.party_score = party_score
        self.confirm.act_score = party_score

    def on_widget_move(self, index):
        App.get_running_app().main.parties[0] = 0 if index is None else index
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
            self.ids.portfolio.update_lock(False)
        else:
            self.ids.back_button.disabled = True
            self.ids.back_button.opacity = 0
            self.ids.ascend_lock.opacity = 0
            self.ids.gear_lock.opacity = 1
            self.ids.ascend_button.disabled = False
            self.ids.gear_button.disabled = True
            self.ids.portfolio.update_lock(True)

    def on_gear(self):
        if not self.ids.gear_button.disabled:
            self.close_hints()
            screen, made = App.get_running_app().main.create_screen('gear_change')
            App.get_running_app().main.display_screen(screen, True, True)

    def on_inventory(self):
        pass

    def add_bonus(self):
        for x in range(200):
            GameMechanics.generateFamiliarityBonuses(App.get_running_app().main.parties[App.get_running_app().main.parties[0] + 1])
        App.get_running_app().main.clean_whitelist()

    def on_back_press(self):
        if super().on_back_press():
            self.close_hints()

    def close_hints(self):
        self.ids.portfolio.close_hints()

    def on_descend(self):
        if self.level == 0:
            root = App.get_running_app().main
            count = 0
            for char in root.parties[root.parties[0] + 1]:
                if char is not None:
                    count += 1
            if count == 0:
                return
        self.confirm.descending = True
        self.confirm.next_floor = str(self.level + 1)
        self.confirm.open()
        self.confirm_open = True

    def do_confirm(self, *args):
        self.confirm_open = False
        if self.confirm.descending:
            self.do_descend()
        else:
            self.do_ascend()

    def dismiss_confirm(self, *args):
        self.confirm_open = False

    def do_descend(self):
        self.confirm.current_floor = str(self.level + 1)
        self.close_hints()
        # print("Delve")
        self.level += 1
        self.update_buttons()
        # descend = False
        # for x in App.get_running_app().parties[0]:
        #     if not x == None:
        #         descend = True
        # if descend:
        #     print("Delving into the dungeon")
        #     # print(str(App.currentparty))
        #     self.floor = DungeonFloor(App.get_running_app(), self.level, True, self)
        #     self.floor.run()
        # else:
        #     print("Not enough Characters to explore")

    def on_ascend(self):
        if not self.ids.ascend_button.disabled:
            self.confirm.descending = False
            self.confirm.next_floor = str(self.level - 1)
            if self.level - 1 == 0:
                self.confirm.next_floor = 'Surface'
            self.confirm.open()
            self.confirm_open = True

    def do_ascend(self):
        self.confirm.current_floor = str(self.level - 1)
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