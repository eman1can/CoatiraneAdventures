from kivy.clock import Clock
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, BooleanProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.label import Label

from src.modules.PartyPortfolio import PartyPortfolio
from src.modules.HTButton import HTButton


class DungeonMain(Screen):
    initialized = BooleanProperty(False)
    main_screen = ObjectProperty(None)
    party_score = NumericProperty(0)
    level = NumericProperty(0)
    boss = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'dungeon_main'

        self._size = (0, 0)
        self._level = -1
        self._party_score = -1

        self.background = Image(source="../res/screens/backgrounds/background.png", allow_stretch=True)

        self.title = Label(text="Coatirane Dungeons", size_hint=(None, None), color=(127 / 255, 0, 0, 1), font_name='../res/fnt/Precious.ttf')
        if self.level == 0:
            level_text = "Level - Surface"
        else:
            level_text = "Level - " + str(self.level)
        self.level_label = Label(text=level_text, size_hint=(None, None), color=(135 / 255, 28 / 255, 100 / 255, 1), font_name='../res/fnt/Precious.ttf')
        self.party_score_label = Label(text="Party Score - " + str(self.party_score), size_hint=(None, None), color=(24 / 255, 134 / 255, 140 / 255, 1), font_name='../res/fnt/Precious.ttf' )

        self.back_button = HTButton(size_hint=(None, None), path='../res/screens/buttons/back', on_release=self.on_back_press)
        self.ascend_button = HTButton(size_hint=(None, None), path='../res/screens/buttons/AscendButton', on_release=self.ascend, text="Ascend", font_name="../res/fnt/Precious.ttf")
        self.ascend_lock = Image(source="../res/screens/buttons/dungeon_button_lock.png", allow_stretch=True, size_hint=(None, None))
        self.descend_button = HTButton(size_hint=(None, None), path='../res/screens/buttons/DescendButton', on_release=self.descend, text="Descend", font_name="../res/fnt/Precious.ttf")

        self.portfolio = PartyPortfolio(main_screen=self.main_screen, dungeon=self, size_hint=(None, None))

        self.add_widget(self.background)
        self.add_widget(self.title)
        self.add_widget(self.level_label)
        self.add_widget(self.party_score_label)
        self.add_widget(self.portfolio)
        self.add_widget(self.back_button)
        self.add_widget(self.descend_button)
        self.add_widget(self.ascend_button)
        self.add_widget(self.ascend_lock)
        self.initialized = True

    def on_enter(self, *args):
        Clock.schedule_interval(lambda dt: self.portfolio.animate_arrows(), 3.5)
        self.update_party_score()
        self.update_buttons()
        self.reload()

    def on_leave(self, *args):
        Clock.unschedule(lambda dt: self.portfolio.animate_arrows())

    def reload(self):
        if self.initialized:
            if self.portfolio is not None:
                self.portfolio.reload()
            self.update_party_score()

    def on_size(self, instance, size):
        if not self.initialized or self._size == size:
            return
        self._size = size.copy()

        self.title.font_size = self.width * .1
        self.title.texture_update()
        self.title.size = self.title.texture_size
        self.title.pos = self.width - self.title.width - self.width * 0.025, self.height - self.title.height - self.width * 0.025

        self.level_label.font_size = self.width * .03
        self.level_label.texture_update()
        self.level_label.size = self.level_label.texture_size
        self.level_label.pos = self.width - self.title.width + self.width * 0.1, self.height - self.title.height - self.width * 0.025 - self.level_label.height * 1.5

        self.party_score_label.font_size = self.width * .03
        self.party_score_label.texture_update()
        self.party_score_label.size = self.party_score_label.texture_size
        self.party_score_label.pos = self.width - self.title.width - self.width * 0.025 + self.width * 0.35, self.height - self.title.height - self.width * 0.025 - self.level_label.height * 1.5

        self.back_button.size = self.width * .05, self.width * .05
        self.back_button.pos = 0, self.height - self.back_button.height

        button_width = self.width * .175
        button_height = button_width * 175 / 450
        spacer = (self.height * .6 - button_height * 2) / 3
        button_x = self.width * .8
        button_y = self.height * .6 + self.width * .025 - spacer - button_height

        self.ascend_button.size = button_width, button_height
        self.ascend_button.pos = button_x, button_y
        self.ascend_button.font_size = self.ascend_button.height * 0.6
        self.ascend_lock.size = button_width, button_height
        self.ascend_lock.pos = button_x, button_y
        self.descend_button.size = button_width, button_height
        self.descend_button.pos = button_x, button_y - button_height - spacer
        self.descend_button.font_size = self.descend_button.height * 0.6

        self.portfolio.size = self.width * .75, self.height * .6
        self.portfolio.pos = self.width * .025, self.height * .025

    def on_level(self, instance, level):
        if not self.initialized or self._level == level:
            return
        self._level = level
        if self.level == 0:
            self.level_label.text = "Level - Surface"
        else:
            self.level_label.text = "Level - " + str(self.level)
        self.level_label.texture_update()
        self.level_label.size = self.level_label.texture_size
        self.level_label.pos = self.width - self.title.width + self.width * 0.1, self.height - self.title.height - self.width * 0.025 - self.level_label.height * 1.5

    def on_party_score(self, instance, party_score):
        if not self.initialized or self._party_score == party_score:
            return
        self._party_score = party_score

        self.party_score_label.text = "Party Score - " + str(self.party_score)
        self.party_score_label.texture_update()
        self.party_score_label.size = self.party_score_label.texture_size
        self.party_score_label.pos = self.width - self.title.width - self.width * 0.025 + self.width * 0.35, self.height - self.title.height - self.width * 0.025 - self.level_label.height * 1.5

    def update_party_score(self):
        if not self.initialized:
            return
        party_score = self.portfolio.get_party_score()
        if self.party_score != party_score:
            self.party_score = party_score

    def update_buttons(self):
        if self.level == 0:
            self.back_button.disabled = False
            self.back_button.opacity = 1
            self.ascend_lock.opacity = 1
            self.ascend_button.disabled = True
            self.portfolio.update_lock(False)
        else:
            self.back_button.disabled = True
            self.back_button.opacity = 0
            self.ascend_lock.opacity = 0
            self.ascend_button.disabled = False
            self.portfolio.update_lock(True)

    def on_back_press(self, instance):
        if not instance.disabled:
            self.main_screen.display_screen(None, False, False)

    def descend(self, instance):
        # print("Delve")
        self.level += 1
        self.update_buttons()
        # descend = False
        # for x in self.main_screen.parties[0]:
        #     if not x == None:
        #         descend = True
        # if descend:
        #     print("Delving into the dungeon")
        #     # print(str(App.currentparty))
        #     self.floor = DungeonFloor(self.main_screen, self.level, True, self)
        #     self.floor.run()
        # else:
        #     print("Not enough Characters to explore")

    def ascend(self, instance):
        if not instance.disabled:
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