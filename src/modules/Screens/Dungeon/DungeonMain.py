from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from src.modules.PartyPortfolio import PartyPortfolio
from src.modules.CustomHoverableButton import CustomHoverableButton

class DungeonMain(Screen):
    level = NumericProperty(1)
    score = NumericProperty(1)
    boss = StringProperty('')
    first = BooleanProperty(True)
    wasInCharScreen = BooleanProperty(False)

    def __init__(self, main_screen, size, **kwargs):
        super().__init__(**kwargs)
        self.main_screen = main_screen
        self.screen_size = 3840

        self.background = Image(source="../res/screens/backgrounds/background.png", size=size, pos=(0, 0), keep_ratio=True, allow_stretch=True)

        self.back_button = CustomHoverableButton(size=(256 * size[0] / self.screen_size, 256 * size[0] / self.screen_size), pos=(0, size[1] - (256 * size[0] / self.screen_size)), path='../res/screens/buttons/back', on_touch_up=self.on_back_press)
        self.ascend_button = CustomHoverableButton(size=(450 * size[0] / self.screen_size, 175 * size[0] / self.screen_size), pos=(size[0] - 675 * size[0] / self.screen_size, size[1] / 2 - 900 * size[0] / self.screen_size), path='../res/screens/buttons/AscendButton', on_touch_up=self.ascend)
        self.descend_button = CustomHoverableButton(size=(450 * size[0] / self.screen_size, 175 * size[0] / self.screen_size), pos=(size[0] - 675 * size[0] / self.screen_size, size[1] / 2), path='../res/screens/buttons/DescendButton', on_touch_up=self.descend)

        self.portfolio = PartyPortfolio(main_screen, (size[0] * .75, size[1] * .6), (size[0] * .025, size[0] * .025))

        self.add_widget(self.background)
        self.add_widget(self.portfolio)
        self.add_widget(self.back_button)
        self.add_widget(self.descend_button)
        self.add_widget(self.ascend_button)

    def on_enter(self, *args):
        Clock.schedule_interval(lambda dt: self.portfolio.animate_arrows(), 2)

    def on_leave(self, *args):
        Clock.unschedule(lambda dt: self.portfolio.animate_arrows())

    def reload(self):
        if self.portfolio is not None:
            self.portfolio.reload()

    def on_size(self, instance, size):
        self.background.size = size
        self.back_button.size = (256 * size[0] / self.screen_size, 256 * size[0] / self.screen_size)
        self.back_button.pos = (0, size[1] - self.back_button.height)
        self.portfolio.size = (self.width * .75, self.height * .5)
        self.portfolio.pos = (self.width * .05, self.width * .05)

    def updateCurrent(self):
        if self.first:
            pass
            # self.first = False
            # self.showparty(self.main_screen.parties[0])
        else:
            pass
            # if not self.wasInCharScreen:
            #     for x in self.main_screen.:
            #         if x.inPreview:
            #             x.collapse()
            # else:
            #     self.wasInCharScreen = False

    def update_buttons(self):
        pass
        # if (self.level < 2):
        # print("enabling back button")
        # self.backButton.disabled = False
        # self.backButton.opacity = 1
        # print('disabling ascend')
        # self.ascendButton.disabled = True
        # self.ascendButtonText.text = '[s]Ascend[/s]'
        # else:
        # print('disabling back button')
        # self.backButton.disabled = True
        # self.backButton.opacity = 0
        # print('enabling ascend')
        # self.ascendButtonText.text = 'Ascend'
        # self.ascendButton.disabled = False

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
            descend = False
            for x in self.main_screen.parties[0]:
                if not x == None:
                    descend = True
            if descend:
                print("Delving into the dungeon")
                # print(str(App.currentparty))
                self.floor = DungeonFloor(self.main_screen, self.level, True, self)
                self.floor.run()
            else:
                print("Not enough Characters to explore")

    def ascend(self, instance, touch):
        if instance.collide_point(*touch.pos):
            if not instance.disabled:
                # print("Ascend")
                if len(shownparty) > 0:
                    print("Ascending from dungeon")
                    self.level = self.level - 1
                    if (self.level < 2):
                        print('disabling ascend')
                        self.ids['ascend'].disabled = True
                        self.ids['ascend_text'].text = '[s]Ascend[/s]'
                    else:
                        print('enabling ascend')
                        self.ids['ascend_text'].text = 'Ascend'
                        self.ids['ascend'].disabled = False
                else:
                    print("not enough Characters to explore")

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