from kivy.app import App
from kivy.core.image import Image
from kivy.animation import Animation
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty

from src.modules.KivyBase.Hoverable import ScreenH as Screen
from src.modules.Screens.CharacterPortfolio import CharacterPortfolio
from src.modules.DragScreen import DragSnapWidget


class DungeonMain(Screen):
    main_screen = ObjectProperty(None)
    party_score = NumericProperty(0)
    level = NumericProperty(0)
    boss = BooleanProperty(False)

    animation_left = ObjectProperty(None, allownone=True)
    animation_right = ObjectProperty(None, allownone=True)
    animate_distance = NumericProperty(100)
    animate_start_left = NumericProperty(5)
    animate_start_right = NumericProperty(95)

    background_texture = ObjectProperty(None)

    def __init__(self, **kwargs):
        self.name = 'dungeon_main'
        self.background_texture = Image('../res/screens/backgrounds/background.png').texture
        super().__init__(**kwargs)
        self.ids.portfolio.dungeon = self

        for index in range(0, len(App.get_running_app().main.parties) - 1):
            self.ids.portfolio.add_widget(CharacterPortfolio(party=App.get_running_app().main.parties[index + 1], party_index=(index + 1), dungeon=self))

    def on_mouse_pos(self, hover):
        if self.ids.inventory_button.dispatch('on_mouse_pos', hover):
            return True
        if self.ids.gear_button.dispatch('on_mouse_pos', hover):
            return True
        if self.ids.ascend_button.dispatch('on_mouse_pos', hover):
            return True
        if self.ids.descend_button.dispatch('on_mouse_pos', hover):
            return True
        if self.ids.portfolio.dispatch('on_mouse_pos', hover):
            return True
        return False

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
        self.animation_left.repeat = False
        self.animation_right.repeat = False

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

    def on_widget_move(self):
        self.ids.portfolio.reload()
        self.update_party_score()

    def update_buttons(self):
        if self.level == 0:
            self.ids.back_button.disabled = False
            self.ids.back_button.opacity = 1
            self.ids.ascend_lock.opacity = 1
            self.ids.ascend_button.disabled = True
            self.ids.portfolio.update_lock(False)
        else:
            self.ids.back_button.disabled = True
            self.ids.back_button.opacity = 0
            self.ids.ascend_lock.opacity = 0
            self.ids.ascend_button.disabled = False
            self.ids.portfolio.update_lock(True)

    def on_back_press(self):
        if not self.ids.back_button.disabled:
            App.get_running_app().main.display_screen(None, False, False)

    def descend(self):
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

    def ascend(self):
        if not self.ids.ascend_button.disabled:
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