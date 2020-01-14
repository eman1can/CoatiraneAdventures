from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from src.modules.PartyPortfolio import PartyPortfolio
from src.modules.CustomHoverableButton import CustomHoverableButton

class DungeonMain(Screen):
    level = NumericProperty(1)
    party_score = NumericProperty(0)
    boss = BooleanProperty(False)

    def __init__(self, main_screen, size, **kwargs):
        self.initalized = False
        super().__init__(size=size, **kwargs)
        self.main_screen = main_screen

        self.background = Image(source="../res/screens/backgrounds/background.png", size=size, pos=(0, 0), keep_ratio=True, allow_stretch=True)

        self.title = Label(text="Coatirane Dungeons", font_size=self.main_screen.width * .1, size_hint=(None, None),
                           color=(1, .2, .2, 1), font_name='../res/fnt/Precious.ttf')
        self.title._label.refresh()
        self.title.size = self.title._label.texture.size
        self.title.pos = size[0] - self.title.width - size[0] * 0.025, size[1] - self.title.height - size[0] * 0.025

        self.level_label = Label(text="Level - " + str(self.level), font_size=self.main_screen.width * .03, size_hint=(None, None), color=(135 / 255, 28 / 255, 100 / 255, 1), font_name='../res/fnt/Precious.ttf' )
        self.level_label._label.refresh()
        self.level_label.size = self.level_label._label.texture.size
        self.level_label.pos = size[0] - self.title.width + self.size[0] * 0.1, size[1] - self.title.height - size[0] * 0.025 - self.level_label.height * 1.5

        self.party_score_label = Label(text="Party Score - " + str(self.party_score), font_size=self.main_screen.width * .03, size_hint=(None, None), color=(24 / 255, 134 / 255, 140 / 255, 1), font_name='../res/fnt/Precious.ttf' )
        self.party_score_label._label.refresh()
        self.party_score_label.size = self.party_score_label._label.texture.size
        self.party_score_label.pos = size[0] - self.title.width - size[0] * 0.025 + self.size[0] * 0.35, size[1] - self.title.height - size[0] * 0.025 - self.level_label.height * 1.5


        back_button_size = (size[0] * .05, size[0] * .05)
        back_button_pos = 0, size[1] - back_button_size[1]

        button_x = size[0] * .175
        button_y = button_x * 175 / 450
        button_size = button_x, button_y
        spacer = (size[1] * .6 - button_y * 2) / 3
        button_pos = size[0] * .8, size[1] * .6 + size[0] * .025 - spacer - button_y

        self.back_button = CustomHoverableButton(size=back_button_size, pos=back_button_pos, path='../res/screens/buttons/back', on_touch_up=self.on_back_press, background_disabled_normal=True)
        self.ascend_button = CustomHoverableButton(size=button_size, pos=button_pos, path='../res/screens/buttons/AscendButton', on_touch_up=self.ascend, background_disabled_normal=True)
        self.descend_button = CustomHoverableButton(size=button_size, pos=(button_pos[0], button_pos[1] - button_y - spacer), path='../res/screens/buttons/DescendButton', on_touch_up=self.descend)

        self.portfolio = PartyPortfolio(main_screen, (size[0] * .75, size[1] * .6), (size[0] * .025, size[0] * .025), self)

        self.add_widget(self.background)
        self.add_widget(self.title)
        self.add_widget(self.level_label)
        self.add_widget(self.party_score_label)
        self.add_widget(self.portfolio)
        self.add_widget(self.back_button)
        self.add_widget(self.descend_button)
        self.add_widget(self.ascend_button)

        self.initalized = True
        self.update_party_score()
        self.update_buttons()

    def on_enter(self, *args):
        Clock.schedule_interval(lambda dt: self.portfolio.animate_arrows(), 3.5)
        self.update_party_score()
        self.update_buttons()

    def on_leave(self, *args):
        Clock.unschedule(lambda dt: self.portfolio.animate_arrows())

    def reload(self):
        if self.portfolio is not None:
            self.portfolio.reload()
        if self.initalized:
            self.update_party_score()

    def on_size(self, instance, size):
        if not self.initalized:
            return
        self.background.size = size

        back_button_size = (size[0] * .05, size[0] * .05)
        back_button_pos = 0, size[1] - back_button_size[1]

        button_x = size[0] * .175
        button_y = button_x * 175 / 450
        button_size = button_x, button_y
        spacer = (size[1] * .6 - button_y * 2) / 3
        button_pos = size[0] * .8, size[1] * .6 + size[0] * .025 - spacer - button_y

        self.back_button.size = back_button_size
        self.back_button.pos = back_button_pos
        self.ascend_button.size = button_size
        self.ascend_button.pos = button_pos
        self.descend_button.size = button_size
        self.descend_button.pos = button_pos[0], button_pos[1] - button_y - spacer
        self.portfolio.size = (size[0] * .75, size[1] * .6)
        self.portfolio.pos = (size[0] * .025, size[1] * .025)

    def on_level(self, instance, level):
        if not self.initalized:
            return
        self.level_label.text = "Level - " + str(level)
        self.level_label._label.refresh()
        self.level_label.size = self.level_label._label.texture.size
        self.level_label.pos = self.size[0] - self.title.width + self.size[0] * 0.1, self.size[1] - self.title.height - self.size[0] * 0.025 - self.level_label.height * 1.5

    def on_party_score(self, instance, party_score):
        if not self.initalized:
            return
        self.party_score_label.text = "Party Score - " + str(party_score)
        self.party_score_label._label.refresh()
        self.party_score_label.size = self.party_score_label._label.texture.size
        self.party_score_label.pos = self.size[0] - self.title.width - self.size[0] * 0.025 + self.size[0] * 0.35, self.size[
            1] - self.title.height - self.size[0] * 0.025 - self.level_label.height * 1.5

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

    # def showparty(self, party):
    #     # for x in App.currentparty:
    #     #     if not x == None:
    #     #         party.append(App.characterArray[x])
    #     #     else:
    #     #         party.append(None)
    #     self.portfolio = CharacterPortfolio(self.main_screen, (self.width * .75, self.height * .5), (self.width * .05, self.width * .05)) # id=('slot%d' % x), transition=SlideTransition(duration=.25)
    #     self.add_widget(self.portfolio)
    # for x in range(len(party)):
    #     if party[x] == None:
    #         slot = CharacterPreview((self.width * .5, self.width * .5 * .2), id=('slot%d' % x), transition=SlideTransition(duration=.25))
    #         slot.isDisabled = False
    #         slot.pos = 2560 - (300 * x + 950), 100
    #         slot.number = x
    #         App.slots.append(slot)
    #         slot2 = emptycharacterpreview(slot, name='empty')
    #         slot.goto_next(slot2, 'right')
    #         self.add_widget(slot)
    #     else:
    #         # print("Slot %d: %s" % (x, party[x].getname()))
    #         slot = CharacterPreview(id=('slot%d' % x), transition=SlideTransition(duration=.25))
    #         slot.isDisabled = False
    #         slot.pos = 2560 - (300 * x + 950), 100
    #         slot2 = filledcharacterpreviewS(slot, party[x], size=(250, 650))
    #         slot.number = x
    #         slot.char = party[x]
    #         App.slots.append(slot)
    #         slot.goto_next(slot2, 'right')
    #         self.add_widget(slot)
    #
    # self.calculatepartyscore(App.currentparty)

    def descend(self, instance, touch):
        if instance.collide_point(*touch.pos):
            # print("Delve")
            self.level += 1
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

    def calculatepartyscore(self, party):
        tempparty = []
        for x in party:
            if not x == None:
                tempparty.append(App.characterArray[x])
        party = tempparty
        score = 0
        bigscore = 0
        for x in range(len(party)):
            score += party[x].totalHealth
            score += party[x].totalMP
            score /= 1.5
            score += party[x].totalDefense
            score /= 1.2
            score += party[x].totalPhysicalAttack
            score += party[x].totalMagicalAttack
            score /= 2
            score += party[x].totalEndurance
            score += party[x].totalStrength
            score += party[x].totalMagic
            score += party[x].totalDexterity
            score += party[x].totalAgility
            score /= 3
            score = math.ceil(score)
            bigscore += score
            score = 0
        self.score = bigscore