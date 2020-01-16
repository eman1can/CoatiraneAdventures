from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from src.modules.PartyPortfolio import PartyPortfolio
from src.modules.HTButton import HTButton

class DungeonMain(Screen):
    party_score = NumericProperty(0)
    level = NumericProperty(1)
    boss = BooleanProperty(False)

    def __init__(self, main_screen, **kwargs):
        self.initalized = False
        super().__init__(**kwargs)
        self.name = 'dungeon_main'

        self.main_screen = main_screen

        self._size = (0, 0)

        self.background = Image(source="../res/screens/backgrounds/background.png", allow_stretch=True)

        self.title = Label(text="Coatirane Dungeons", size_hint=(None, None), color=(1, .2, .2, 1), font_name='../res/fnt/Precious.ttf')
        self.level_label = Label(text="Level - " + str(self.level), size_hint=(None, None), color=(135 / 255, 28 / 255, 100 / 255, 1), font_name='../res/fnt/Precious.ttf')
        self.party_score_label = Label(text="Party Score - " + str(self.party_score), size_hint=(None, None), color=(24 / 255, 134 / 255, 140 / 255, 1), font_name='../res/fnt/Precious.ttf' )

        self.back_button = HTButton(size_hint=(None, None), path='../res/screens/buttons/back', on_touch_up=self.on_back_press, background_disabled_normal_use=True)
        self.ascend_button = HTButton(size_hint=(None, None), path='../res/screens/buttons/AscendButton', on_touch_up=self.ascend, background_disabled_normal_use=True)
        self.descend_button = HTButton(size_hint=(None, None), path='../res/screens/buttons/DescendButton', on_touch_up=self.descend)

        self.portfolio = PartyPortfolio(main_screen, self)

        self.add_widget(self.background)
        self.add_widget(self.title)
        self.add_widget(self.level_label)
        self.add_widget(self.party_score_label)
        self.add_widget(self.portfolio)
        self.add_widget(self.back_button)
        self.add_widget(self.descend_button)
        self.add_widget(self.ascend_button)
        self.initalized = True

    def on_enter(self, *args):
        Clock.schedule_interval(lambda dt: self.portfolio.animate_arrows(), 3.5)
        self.update_party_score()
        self.update_buttons()

    def on_leave(self, *args):
        Clock.unschedule(lambda dt: self.portfolio.animate_arrows())

    def reload(self):
        if self.initalized:
            if self.portfolio is not None:
                self.portfolio.reload()
            self.update_party_score()

    def on_size(self, instance, size):
        if not self.initalized or self._size == size:
            return
        self._size = size.copy()

        self.title.font_size = self.width * .1
        self.title.texture_update()
        self.title.size = self.title.texture_size
        self.title.pos = self.width - self.title.width - self.width * 0.025, self.height - self.title.height - self.width * 0.025

        self.level_label.font_size = self.width * .03
        self.dispatch('on_level')
        self.party_score_label.font_size = self.width * .03
        self.dispatch('on_party_score')

        self.back_button.size = self.width * .05, self.width * .05
        self.back_button.pos = 0, self.height - self.back_button.height

        button_width = self.width * .175
        button_height = button_width * 175 / 450
        spacer = (self.height * .6 - button_height * 2) / 3
        button_x = self.width * .8
        button_y = self.height * .6 + self.width * .025 - spacer - button_height

        self.ascend_button.size = button_width, button_height
        self.ascend_button.pos = button_x, button_y
        self.descend_button.size = button_width, button_height
        self.descend_button.pos = button_x, button_y - button_height - spacer

        self.portfolio.size = self.width * .75, self.height * .6
        self.portfolio.pos = self.width * .025, self.height * .025

    def on_level(self, instance, level):
        if not self.initalized:
            return
        self.level_label.text = "Level - " + str(level)
        self.level_label.texture_update()
        self.level_label.size = self.level_label.texture_size
        self.level_label.pos = self.width - self.title.width + self.width * 0.1, self.height - self.title.height - self.width * 0.025 - self.level_label.height * 1.5

    def on_party_score(self, instance, party_score):
        if not self.initalized:
            return
        self.party_score_label.text = "Party Score - " + str(party_score)
        self.party_score_label.texture_update()
        self.party_score_label.size = self.party_score_label.texture_size
        self.party_score_label.pos = self.width - self.title.width - self.width * 0.025 + self.width * 0.35, self.height - self.title.height - self.width * 0.025 - self.level_label.height * 1.5

    def update_party_score(self):
        if not self.initalized:
            return
        party_score = self.portfolio.get_party_score()
        if self.party_score != party_score:
            self.party_score = party_score

    def update_buttons(self):
        if (self.level < 2):
            self.back_button.disabled = False
            self.back_button.opacity = 1
            self.ascend_button.disabled = True
        else:
            self.back_button.disabled = True
            self.back_button.opacity = 0
            self.ascend_button.disabled = False

    def on_back_press(self, instance, touch):
        if instance.collide_point(*touch.pos):
            if not instance.disabled:
                self.main_screen.display_screen(None, False, False)

    def descend(self, instance, touch):
        if instance.collide_point(*touch.pos):
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

    def ascend(self, instance, touch):
        if instance.collide_point(*touch.pos):
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