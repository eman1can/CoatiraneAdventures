from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.properties import StringProperty
from kivy.app import App
import random

from src.entitites.Character.Scale import Scale
from src.modules.CustomHoverableButton import CustomHoverableButton


class CharacterAttributeScreen(Screen):
    charname = StringProperty('')

    # chardisplayname = StringProperty('')
    # charid = StringProperty('')
    # charfullimage = StringProperty('')

    def __init__(self, main_screen, preview, size, pos, char, name):
        self.main_screen = main_screen
        self.preview = preview
        self.initalized = False
        super(CharacterAttributeScreen, self).__init__(name=name, size=size, pos=pos)

        back_button_size = (size[0] * .05, size[0] * .05)
        back_button_pos = 0, size[1] - back_button_size[1]
        self.back_button = CustomHoverableButton(size=back_button_size, pos=back_button_pos, path='../res/screens/buttons/back', on_touch_up=self.on_back_press, background_disabled_normal=True)

        # self.charname = char.getname()
        # # self.preview = preview
        # # self.chardisplayname = char.getdisplayname()
        # # self.charid = char.getid()
        # # self.charfullimage = char.getfullimage()
        # self.layout = FloatLayout()
        #
        # self.add_widget(self.layout)
        # self.bg = Image(source='res/charattributebg.png', size=(2560, 1440), pos=(0, 0), allow_stretch=True,
        #                 keep_ratio=False)
        # self.layout.add_widget(self.bg)
        # self.char = char
        # self.id = self.name
        image = char.get_full_image(False)
        image.size = (image.image_ratio * size[1], size[1])
        image.pos = (-(size[0] - image.image_ratio * size[1]) / 2, 0)
        # image.pos = (image.norm_image_size[0] / 2 - size[0] / 2, 0)

        # self.layout.add_widget(image)
        # self.backButton = customButton(id='back', source='res/BackArrow.png', size=(100, 100),
        #                                pos=(100, self.height - 200),
        #                                on_touch_down=self.onBackPress)
        # self.layout.add_widget(self.backButton)
        #
        # ###### DEV BUTTONS ######
        # self.maxStats = Button(text="Max Stats", font_size=40, pos=(500, 1000), size=(200, 200),
        #                        on_touch_down=self.maxOut, size_hint=(None, None))
        # self.rankupButton = Button(text="Rank Up", font_size=40, pos=(900, 500), size=(200, 200),
        #                            on_touch_down=self.onRankUp, size_hint=(None, None))
        # self.rankbreakButton = Button(text="Rank Break", font_size=40, pos=(900, 300), size=(200, 200),
        #                               on_touch_down=self.onRankBreak, size_hint=(None, None))
        #
        # self.hpexpincreaseButton = Button(text="Increase Hp Exp", font_size=40, pos=(1200, 1000), size=(300, 50),
        #                                   on_touch_down=self.increaseExpStat, size_hint=(None, None))
        # self.mpexpincreaseButton = Button(text="Increase Mp Exp", font_size=40, pos=(1200, 925), size=(300, 50),
        #                                   on_touch_down=self.increaseExpStat, size_hint=(None, None))
        # self.defexpincreaseButton = Button(text="Increase Def Exp", font_size=40, pos=(1200, 850), size=(300, 50),
        #                                    on_touch_down=self.increaseExpStat, size_hint=(None, None))
        # self.strexpincreaseButton = Button(text="Increase Str Exp", font_size=40, pos=(1200, 775), size=(300, 50),
        #                                    on_touch_down=self.increaseExpStat, size_hint=(None, None))
        # self.agiexpincreaseButton = Button(text="Increase Agi Exp", font_size=40, pos=(1200, 700), size=(300, 50),
        #                                    on_touch_down=self.increaseExpStat, size_hint=(None, None))
        # self.dexexpincreaseButton = Button(text="Increase Dex Exp", font_size=40, pos=(1200, 625), size=(300, 50),
        #                                    on_touch_down=self.increaseExpStat, size_hint=(None, None))
        # self.endexpincreaseButton = Button(text="Increase End Exp", font_size=40, pos=(1200, 550), size=(300, 50),
        #                                    on_touch_down=self.increaseExpStat, size_hint=(None, None))
        #
        # # self.add_widget(self.maxStats)
        # # self.add_widget(self.rankupButton)
        # # self.add_widget(self.rankbreakButton)
        # # self.add_widget(self.hpexpincreaseButton)
        # # self.add_widget(self.mpexpincreaseButton)
        # # self.add_widget(self.defexpincreaseButton)
        # # self.add_widget(self.strexpincreaseButton)
        # # self.add_widget(self.agiexpincreaseButton)
        # # self.add_widget(self.dexexpincreaseButton)
        # # self.add_widget(self.endexpincreaseButton)
        #
        # ###### DEV BUTTONS END ######
        #
        # count = 0
        # self.stars = []
        # addx = False
        # for x in char.ranks:
        #     # print("Rank: " + str(x))
        #     xpos = 50
        #     if addx:
        #         xpos += 25
        #     if x.unlocked:
        #         if not x.broken:
        #             self.stars.append(Image(source="../res/screens/stats/star.png", pos=(xpos, 350 + (count * 75)), size=(140, 140),
        #                                     size_hint=(None, None), opacity=1))
        #             self.layout.add_widget(self.stars[count])
        #         else:
        #             self.stars.append(Image(source="../res/screens/stats/rankbrk.png", pos=(xpos, 350 + (count * 75)), size=(140, 140),
        #                                     size_hint=(None, None), opacity=1))
        #             self.layout.add_widget(self.stars[count])
        #     else:
        #         self.stars.append(Image(pos=(xpos, 350 + (count * 75)), size=(140, 140),
        #                                 size_hint=(None, None), opacity=0))
        #         self.layout.add_widget(self.stars[count])
        #     count += 1
        #     if addx:
        #         xpos -= 25
        #     addx = not addx
        #
        # self.nameLabel = Label(text='[b]' + self.char.getname() + '[/b]', size_hint=(None, None), font_size=120,
        #                        color=(1, 1, 1, .8), markup=True)
        # with self.nameLabel.canvas.before:
        #     Color(.1, .1, .1, .6)
        #     Rectangle(size=(len(self.char.getname()) * 60 + 75, 160),
        #               pos=(App.height - len(self.char.getname()) * 55.5 - 100, App.height - 160))
        # self.displaynameLabel = Label(text='[b]' + self.char.getdisplayname() + '[/b]', size_hint=(None, None),
        #                               color=(1, 1, 1, .75), font_size=90, markup=True)
        #
        # # Total Stat Window
        #
        # # self.status_board_manager = StatusBoardManager(self.char, size=(1120, 1440), pos=(1440, 0),
        # #                                                size_hint=(None, None),
        # #                                                transition=SlideTransition(duration=.375))
        # # self.layout.add_widget(self.status_board_manager)
        # self.layout.add_widget(self.nameLabel)
        # self.totalstatpreview = StatPreview(self.char, 1, 1, True, char.totalPhysicalAttack, char.totalMagicalAttack,
        #                                     char.totalMP,
        #                                     char.totalHealth, char.totalDefense, char.totalStrength, char.totalMagic,
        #                                     char.totalAgility, char.totalDexterity, char.totalEndurance,
        #                                     size=(1300, 300), pos=(0, 0))
        # self.rankstatpreview = StatPreview(self.char, 1, 1, False, char.ranks[0].rankstrengthtotal,
        #                                    char.ranks[0].rankmagictotal,
        #                                    char.ranks[0].rankmagicalpointstotal, char.ranks[0].rankhealthtotal,
        #                                    char.ranks[0].rankdefensetotal,
        #                                    char.ranks[0].rankstrengthtotal, char.ranks[0].rankmagictotal,
        #                                    char.ranks[0].rankagilitytotal, char.ranks[0].rankdexteritytotal,
        #                                    char.ranks[0].rankendurancetotal, size=(350, 340), pos=(App.height, 0))
        # self.layout.add_widget(self.totalstatpreview)
        # self.layout.add_widget(self.rankstatpreview)
        # Clock.schedule_once(self.updatelabels)

        self.add_widget(image)
        self.add_widget(self.back_button)
        self.initalized = True

    def on_size(self, instance, size):
        pass

    def reload(self):
        pass

    def maxOut(self, instance, touch):
        if instance.collide_point(*touch.pos) and instance == self.maxStats:
            for x in range(10):
                self.status_board_manager.screens[x].unlockAllNum()
                self.increaseExpStatNum(0)
                self.increaseExpStatNum(1)
                self.increaseExpStatNum(2)
                self.increaseExpStatNum(3)
                self.increaseExpStatNum(4)
                self.increaseExpStatNum(5)
                self.increaseExpStatNum(6)
                self.char.printstats()
                self.char.rankbreak()
                self.updateStars()
                self.char.ranks[self.char.currentRank - 1].calcvalues()
                self.char.ranks[self.char.currentRank - 1].calcexpvalues()
                self.char.updateCharValues()
                self.updateRankLabels()
                self.updateRankPreviewLabels(self.char.currentRank)
                self.updateexpbars()
                self.char.printstats()
                if not x == 9:
                    if not self.char.first == None:
                        # print("character is first")
                        if self.char.currentRank > 2:
                            # print("unlocking the tavern")
                            App.tavern_unlocked = False
                    self.char.rankup()
                    self.updateStars()
                    self.updateexpbarsmaxs()

    def increaseExpStatNum(self, statType):
        if statType == 0:
            if self.char.currentRank == 1:
                valuerange = self.char.ranks[self.char.currentRank - 1].expHpCap - self.char.ranks[
                    self.char.currentRank - 1].exphealthraw
            else:
                valuerange = (self.char.ranks[self.char.currentRank - 1].expHpCap - self.char.ranks[
                    self.char.currentRank - 2].expHpCap) - self.char.ranks[
                                 self.char.currentRank - 1].exphealthraw
            toprange = float(valuerange) * 1
            bottomrange = float(valuerange) * 1
            self.char.ranks[self.char.currentRank - 1].exphealthraw += random.uniform(bottomrange, toprange)
            self.char.ranks[self.char.currentRank - 1].calcexpvalues()
            self.char.updateCharValues()
            self.totalstatpreview.healthLvlBar.value = self.char.exphealthtotal
            self.updateRankLabels()
        elif statType == 1:
            if self.char.currentRank == 1:
                valuerange = self.char.ranks[self.char.currentRank - 1].expMpCap - self.char.ranks[
                    self.char.currentRank - 1].expmagicalpointsraw
            else:
                valuerange = (self.char.ranks[self.char.currentRank - 1].expMpCap - self.char.ranks[
                    self.char.currentRank - 2].expMpCap) - self.char.ranks[
                                 self.char.currentRank - 1].expmagicalpointsraw
            toprange = float(valuerange) * 1
            bottomrange = float(valuerange) * 1
            self.char.ranks[self.char.currentRank - 1].expmagicalpointsraw += random.uniform(bottomrange,
                                                                                             toprange)
            self.char.ranks[self.char.currentRank - 1].calcexpvalues()
            self.char.updateCharValues()
            self.totalstatpreview.mpLvlBar.value = self.char.expmptotal
            self.updateRankLabels()
        elif statType == 2:
            if self.char.currentRank == 1:
                valuerange = self.char.ranks[self.char.currentRank - 1].expDefCap - self.char.ranks[
                    self.char.currentRank - 1].expdefenseraw
            else:
                valuerange = (self.char.ranks[self.char.currentRank - 1].expDefCap - self.char.ranks[
                    self.char.currentRank - 2].expDefCap) - self.char.ranks[
                                 self.char.currentRank - 1].expdefenseraw
            toprange = float(valuerange) * 1
            bottomrange = float(valuerange) * 1
            self.char.ranks[self.char.currentRank - 1].expdefenseraw += random.uniform(bottomrange,
                                                                                       toprange)
            self.char.ranks[self.char.currentRank - 1].calcexpvalues()
            self.char.updateCharValues()
            self.totalstatpreview.defLvlBar.value = self.char.expdeftotal
            self.updateRankLabels()
        elif statType == 3:
            if self.char.currentRank == 1:
                valuerange = self.char.ranks[self.char.currentRank - 1].expStrCap - self.char.ranks[
                    self.char.currentRank - 1].expstrengthraw
            else:
                valuerange = (self.char.ranks[self.char.currentRank - 1].expStrCap - self.char.ranks[
                    self.char.currentRank - 2].expStrCap) - self.char.ranks[
                                 self.char.currentRank - 1].expstrengthraw
            toprange = float(valuerange) * 1
            bottomrange = float(valuerange) * 1
            self.char.ranks[self.char.currentRank - 1].expstrengthraw += random.uniform(bottomrange,
                                                                                        toprange)
            self.char.ranks[self.char.currentRank - 1].calcexpvalues()
            self.char.updateCharValues()
            self.totalstatpreview.strLvlBar.value = self.char.expstrtotal
            self.updateRankLabels()
            if self.status_board_manager.currentGrid + 1 == self.char.currentRank:
                self.updateRankPreviewLabels(self.char.currentRank)
        elif statType == 4:
            if self.char.currentRank == 1:
                valuerange = self.char.ranks[self.char.currentRank - 1].expAgiCap - self.char.ranks[
                    self.char.currentRank - 1].expagilityraw
            else:
                valuerange = (self.char.ranks[self.char.currentRank - 1].expAgiCap - self.char.ranks[
                    self.char.currentRank - 2].expAgiCap) - self.char.ranks[
                                 self.char.currentRank - 1].expagilityraw
            toprange = float(valuerange) * 1
            bottomrange = float(valuerange) * 1
            self.char.ranks[self.char.currentRank - 1].expagilityraw += random.uniform(bottomrange,
                                                                                       toprange)
            self.char.ranks[self.char.currentRank - 1].calcexpvalues()
            self.char.updateCharValues()
            self.totalstatpreview.agiLvlBar.value = self.char.expagitotal
            self.updateRankLabels()
            if self.status_board_manager.currentGrid + 1 == self.char.currentRank:
                self.updateRankPreviewLabels(self.char.currentRank)
        elif statType == 5:
            if self.char.currentRank == 1:
                valuerange = self.char.ranks[self.char.currentRank - 1].expDexCap - self.char.ranks[
                    self.char.currentRank - 1].expdexterityraw
            else:
                valuerange = (self.char.ranks[self.char.currentRank - 1].expDexCap - self.char.ranks[
                    self.char.currentRank - 2].expDexCap) - self.char.ranks[
                                 self.char.currentRank - 1].expdexterityraw
            toprange = float(valuerange) * 1
            bottomrange = float(valuerange) * 1
            self.char.ranks[self.char.currentRank - 1].expdexterityraw += random.uniform(bottomrange,
                                                                                         toprange)
            self.char.ranks[self.char.currentRank - 1].calcexpvalues()
            self.char.updateCharValues()
            self.totalstatpreview.dexLvlBar.value = self.char.expdextotal
            self.updateRankLabels()
            if self.status_board_manager.currentGrid + 1 == self.char.currentRank:
                self.updateRankPreviewLabels(self.char.currentRank)
        elif statType == 6:
            if self.char.currentRank == 1:
                valuerange = self.char.ranks[self.char.currentRank - 1].expEndCap - self.char.ranks[
                    self.char.currentRank - 1].expenduranceraw
            else:
                valuerange = (self.char.ranks[self.char.currentRank - 1].expEndCap - self.char.ranks[
                    self.char.currentRank - 2].expEndCap) - self.char.ranks[
                                 self.char.currentRank - 1].expenduranceraw
            toprange = float(valuerange) * 1
            bottomrange = float(valuerange) * 1
            self.char.ranks[self.char.currentRank - 1].expenduranceraw += random.uniform(bottomrange,
                                                                                         toprange)
            self.char.ranks[self.char.currentRank - 1].calcexpvalues()
            self.char.updateCharValues()
            self.totalstatpreview.endLvlBar.value = self.char.expendtotal
            self.updateRankLabels()
            if self.status_board_manager.currentGrid + 1 == self.char.currentRank:
                self.updateRankPreviewLabels(self.char.currentRank)

    def increaseExpStat(self, instance, touch):
        if self.hpexpincreaseButton.collide_point(*touch.pos) and instance == self.hpexpincreaseButton:
            if self.char.currentRank == 1:
                valuerange = self.char.ranks[self.char.currentRank - 1].expHpCap - self.char.ranks[
                    self.char.currentRank - 1].exphealthraw
            else:
                valuerange = (self.char.ranks[self.char.currentRank - 1].expHpCap - self.char.ranks[
                    self.char.currentRank - 2].expHpCap) - self.char.ranks[self.char.currentRank - 1].exphealthraw
            toprange = float(valuerange) * 1
            bottomrange = float(valuerange) * 1
            self.char.ranks[self.char.currentRank - 1].exphealthraw += random.uniform(bottomrange, toprange)
            self.char.ranks[self.char.currentRank - 1].calcexpvalues()
            self.char.updateCharValues()
            self.totalstatpreview.healthLvlBar.value = self.char.exphealthtotal
            self.updateRankLabels()
        elif self.mpexpincreaseButton.collide_point(*touch.pos) and instance == self.mpexpincreaseButton:
            if self.char.currentRank == 1:
                valuerange = self.char.ranks[self.char.currentRank - 1].expMpCap - self.char.ranks[
                    self.char.currentRank - 1].expmagicalpointsraw
            else:
                valuerange = (self.char.ranks[self.char.currentRank - 1].expMpCap - self.char.ranks[
                    self.char.currentRank - 2].expMpCap) - self.char.ranks[
                                 self.char.currentRank - 1].expmagicalpointsraw
            toprange = float(valuerange) * 1
            bottomrange = float(valuerange) * 1
            self.char.ranks[self.char.currentRank - 1].expmagicalpointsraw += random.uniform(bottomrange, toprange)
            self.char.ranks[self.char.currentRank - 1].calcexpvalues()
            self.char.updateCharValues()
            self.totalstatpreview.mpLvlBar.value = self.char.expmptotal
            self.updateRankLabels()
        elif self.defexpincreaseButton.collide_point(*touch.pos) and instance == self.defexpincreaseButton:
            if self.char.currentRank == 1:
                valuerange = self.char.ranks[self.char.currentRank - 1].expDefCap - self.char.ranks[
                    self.char.currentRank - 1].expdefenseraw
            else:
                valuerange = (self.char.ranks[self.char.currentRank - 1].expDefCap - self.char.ranks[
                    self.char.currentRank - 2].expDefCap) - self.char.ranks[self.char.currentRank - 1].expdefenseraw
            toprange = float(valuerange) * 1
            bottomrange = float(valuerange) * 1
            self.char.ranks[self.char.currentRank - 1].expdefenseraw += random.uniform(bottomrange, toprange)
            self.char.ranks[self.char.currentRank - 1].calcexpvalues()
            self.char.updateCharValues()
            self.totalstatpreview.defLvlBar.value = self.char.expdeftotal
            self.updateRankLabels()
        elif self.strexpincreaseButton.collide_point(*touch.pos) and instance == self.strexpincreaseButton:
            if self.char.currentRank == 1:
                valuerange = self.char.ranks[self.char.currentRank - 1].expStrCap - self.char.ranks[
                    self.char.currentRank - 1].expstrengthraw
            else:
                valuerange = (self.char.ranks[self.char.currentRank - 1].expStrCap - self.char.ranks[
                    self.char.currentRank - 2].expStrCap) - self.char.ranks[self.char.currentRank - 1].expstrengthraw
            toprange = float(valuerange) * 1
            bottomrange = float(valuerange) * 1
            self.char.ranks[self.char.currentRank - 1].expstrengthraw += random.uniform(bottomrange, toprange)
            self.char.ranks[self.char.currentRank - 1].calcexpvalues()
            self.char.updateCharValues()
            self.totalstatpreview.strLvlBar.value = self.char.expstrtotal
            self.updateRankLabels()
            if self.status_board_manager.currentGrid + 1 == self.char.currentRank:
                self.updateRankPreviewLabels(self.char.currentRank)
        elif self.agiexpincreaseButton.collide_point(*touch.pos) and instance == self.agiexpincreaseButton:
            if self.char.currentRank == 1:
                valuerange = self.char.ranks[self.char.currentRank - 1].expAgiCap - self.char.ranks[
                    self.char.currentRank - 1].expagilityraw
            else:
                valuerange = (self.char.ranks[self.char.currentRank - 1].expAgiCap - self.char.ranks[
                    self.char.currentRank - 2].expAgiCap) - self.char.ranks[self.char.currentRank - 1].expagilityraw
            toprange = float(valuerange) * 1
            bottomrange = float(valuerange) * 1
            self.char.ranks[self.char.currentRank - 1].expagilityraw += random.uniform(bottomrange, toprange)
            self.char.ranks[self.char.currentRank - 1].calcexpvalues()
            self.char.updateCharValues()
            self.totalstatpreview.agiLvlBar.value = self.char.expagitotal
            self.updateRankLabels()
            if self.status_board_manager.currentGrid + 1 == self.char.currentRank:
                self.updateRankPreviewLabels(self.char.currentRank)
        elif self.dexexpincreaseButton.collide_point(*touch.pos) and instance == self.dexexpincreaseButton:
            if self.char.currentRank == 1:
                valuerange = self.char.ranks[self.char.currentRank - 1].expDexCap - self.char.ranks[
                    self.char.currentRank - 1].expdexterityraw
            else:
                valuerange = (self.char.ranks[self.char.currentRank - 1].expDexCap - self.char.ranks[
                    self.char.currentRank - 2].expDexCap) - self.char.ranks[self.char.currentRank - 1].expdexterityraw
            toprange = float(valuerange) * 1
            bottomrange = float(valuerange) * 1
            self.char.ranks[self.char.currentRank - 1].expdexterityraw += random.uniform(bottomrange, toprange)
            self.char.ranks[self.char.currentRank - 1].calcexpvalues()
            self.char.updateCharValues()
            self.totalstatpreview.dexLvlBar.value = self.char.expdextotal
            self.updateRankLabels()
            if self.status_board_manager.currentGrid + 1 == self.char.currentRank:
                self.updateRankPreviewLabels(self.char.currentRank)
        elif self.endexpincreaseButton.collide_point(*touch.pos) and instance == self.endexpincreaseButton:
            if self.char.currentRank == 1:
                valuerange = self.char.ranks[self.char.currentRank - 1].expEndCap - self.char.ranks[
                    self.char.currentRank - 1].expenduranceraw
            else:
                valuerange = (self.char.ranks[self.char.currentRank - 1].expEndCap - self.char.ranks[
                    self.char.currentRank - 2].expEndCap) - self.char.ranks[self.char.currentRank - 1].expenduranceraw
            toprange = float(valuerange) * 1
            bottomrange = float(valuerange) * 1
            self.char.ranks[self.char.currentRank - 1].expenduranceraw += random.uniform(bottomrange, toprange)
            self.char.ranks[self.char.currentRank - 1].calcexpvalues()
            self.char.updateCharValues()
            self.totalstatpreview.endLvlBar.value = self.char.expendtotal
            self.updateRankLabels()
            if self.status_board_manager.currentGrid + 1 == self.char.currentRank:
                self.updateRankPreviewLabels(self.char.currentRank)

    def updateStars(self):
        count = 0
        for x in self.char.ranks:
            if x.unlocked:
                if not x.broken:
                    self.stars[count].source = '../res/screens/stats/star.png'
                    self.stars[count].opacity = 1
                else:
                    self.stars[count].source = '../res/screens/stats/rankbrk.png'
                    self.stars[count].opacity = 1
            count += 1
        self.preview.updateStars(self.char)

    def onRankUp(self, instance, touch):
        if instance.collide_point(*touch.pos):
            if not self.char.first == None:
                # print("character is first")
                if self.char.currentRank > 2:
                    # print("unlocking the tavern")
                    App.tavern_unlocked = False
            self.char.rankup()
            self.updateStars()
            self.updateexpbarsmaxs()
            # self.preview.updateStars()

    def onRankBreak(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.char.printstats()
            self.char.rankbreak()
            self.updateStars()
            self.char.ranks[self.char.currentRank - 1].calcvalues()
            self.char.ranks[self.char.currentRank - 1].calcexpvalues()
            self.char.updateCharValues()
            self.updateRankLabels()
            self.updateRankPreviewLabels(self.char.currentRank)
            self.updateexpbars()
            self.char.printstats()

    def updateexpbars(self, *args):
        self.totalstatpreview.healthLvlBar.value = self.char.exphealthtotal
        self.totalstatpreview.mpLvlBar.value = self.char.expmptotal
        self.totalstatpreview.defLvlBar.value = self.char.expdeftotal
        self.totalstatpreview.strLvlBar.value = self.char.expstrtotal
        self.totalstatpreview.agiLvlBar.value = self.char.expagitotal
        self.totalstatpreview.dexLvlBar.value = self.char.expdextotal
        self.totalstatpreview.endLvlBar.value = self.char.expendtotal

    def updateexpbarsmaxs(self):
        self.totalstatpreview.healthLvlBar.max = self.char.ranks[self.char.currentRank - 1].expHpCap
        self.totalstatpreview.mpLvlBar.max = self.char.ranks[self.char.currentRank - 1].expMpCap
        self.totalstatpreview.defLvlBar.max = self.char.ranks[self.char.currentRank - 1].expDefCap
        self.totalstatpreview.strLvlBar.max = self.char.ranks[self.char.currentRank - 1].expStrCap
        self.totalstatpreview.agiLvlBar.max = self.char.ranks[self.char.currentRank - 1].expAgiCap
        self.totalstatpreview.dexLvlBar.max = self.char.ranks[self.char.currentRank - 1].expDexCap
        self.totalstatpreview.endLvlBar.max = self.char.ranks[self.char.currentRank - 1].expEndCap

    def updateRankLabels(self, *args):
        self.totalstatpreview.healthlabelnumber.text = '%d' % self.char.totalHealth
        self.totalstatpreview.magicalpointlabelnumber.text = '%d' % self.char.totalMP
        self.totalstatpreview.attacklabelnumber.text = '%d' % self.char.totalPhysicalAttack
        self.totalstatpreview.defenselabelnumber.text = '%d' % self.char.totalDefense
        self.totalstatpreview.strengthnumber.text = '%d' % self.char.totalStrength
        self.totalstatpreview.agilitynumber.text = '%d' % self.char.totalAgility
        self.totalstatpreview.dexteritynumber.text = '%d' % self.char.totalDexterity
        self.totalstatpreview.endurancenumber.text = '%d' % self.char.totalEndurance
        self.totalstatpreview.strengthgrade.source = Scale.getScaleAsImagePath(self.char.totalStrength,
                                                                               self.char.ranks[9].strengthMax)
        self.totalstatpreview.agilitygrade.source = Scale.getScaleAsImagePath(self.char.totalAgility,
                                                                              self.char.ranks[9].agilityMax)
        self.totalstatpreview.dexteritygrade.source = Scale.getScaleAsImagePath(self.char.totalDexterity,
                                                                                self.char.ranks[9].dexterityMax)
        self.totalstatpreview.endurancegrade.source = Scale.getScaleAsImagePath(self.char.totalEndurance,
                                                                                self.char.ranks[9].enduranceMax)

    def updateRankPreviewLabels(self, rank):
        self.rankstatpreview.strengthnumber.text = '%d' % self.char.ranks[rank - 1].rankstrengthtotal
        self.rankstatpreview.strengthgrade.source = Scale.getScaleAsImagePath(
            self.char.ranks[rank - 1].rankstrengthtotal,
            self.char.ranks[rank - 1].strengthMax)
        self.rankstatpreview.agilitynumber.text = '%d' % self.char.ranks[rank - 1].rankagilitytotal
        self.rankstatpreview.agilitygrade.source = Scale.getScaleAsImagePath(self.char.ranks[rank - 1].rankagilitytotal,
                                                                             self.char.ranks[rank - 1].agilityMax)
        self.rankstatpreview.dexteritynumber.text = '%d' % self.char.ranks[rank - 1].rankdexteritytotal
        self.rankstatpreview.dexteritygrade.source = Scale.getScaleAsImagePath(
            self.char.ranks[rank - 1].rankdexteritytotal,
            self.char.ranks[rank - 1].dexterityMax)
        self.rankstatpreview.endurancenumber.text = '%d' % self.char.ranks[rank - 1].rankendurancetotal
        self.rankstatpreview.endurancegrade.source = Scale.getScaleAsImagePath(
            self.char.ranks[rank - 1].rankendurancetotal,
            self.char.ranks[rank - 1].enduranceMax)

    def updatelabels(self, *args):
        # print(self.nameLabel.texture_size)
        # print(self.displaynameLabel.texture_size)
        self.nameLabel.pos = App.height - 100 - self.nameLabel.texture_size[0] / 2, App.height - 140
        # self.displaynameLabel.pos = self.nameLabel.texture_size[0] + 200 + 100 + self.displaynameLabel.texture_size[0]/2, App.height - 159
        # self.layout.add_widget(self.displaynameLabel)

    def on_back_press(self, instance, touch):
        if instance.collide_point(*touch.pos):
            if self.main_screen is not None:
                self.main_screen.display_screen(None, False, False)