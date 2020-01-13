from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

from src.modules.Screens.CharacterAttributeScreens.ProgressBar import ProgressBar
from src.entitites.Character import Scale

class StatusBoardManager(ScreenManager):

    def __init__(self, char, **kwargs):
        super(StatusBoardManager, self).__init__(**kwargs)
        self.screens = []
        self.ranks = char.ranks
        for x in range(10):
            self.screens.append(StatusBoard(x, self, self.ranks[x], char, char.ranks[x].grid.grid, name='grid %d' % x))
        self.currentGrid = 0
        self.current = 'grid %d' % self.currentGrid

    def nextGrid(self, instance, touch):
        if instance.collide_point(*touch.pos):
            if self.currentGrid < 9:
                if self.ranks[self.currentGrid + 1].unlocked:
                    self.currentGrid += 1
                    self.transition.direction = 'up'
                    self.current = 'grid %d' % self.currentGrid
                    self.parent.parent.updateRankPreviewLabels(self.currentGrid + 1)

    def lastGrid(self, instance, touch):
        if instance.collide_point(*touch.pos):
            if self.currentGrid > 0:
                self.currentGrid -= 1
                self.transition.direction = 'down'
                self.current = 'grid %d' % self.currentGrid
                self.parent.parent.updateRankPreviewLabels(self.currentGrid + 1)


class StatusBoard(Screen):

    def __init__(self, number, managerPass, rank, char, grid, **kwargs):
        super().__init__(**kwargs)
        self.managerObject = managerPass
        self.slots = []
        self.rank = rank
        self.char = char
        self.currentSlot = None
        if not number == 0:
            upButton = Button(size=(150, 150), size_hint=(None, None), pos=(1120 - 150, 1400 - 150),
                              on_touch_down=self.managerObject.lastGrid, background_normal='res/UpArrow.png',
                              background_down='res/UpArrowPressed.png', background_color=(1, 1, 1, .7))
            self.add_widget(upButton)
        if not number == 9:
            downButton = Button(size=(150, 150), size_hint=(None, None), pos=(1120 - 150, 0),
                                on_touch_down=self.managerObject.nextGrid, background_normal='res/DownArrow.png',
                                background_down='res/DownArrowPressed.png', background_color=(1, 1, 1, .7))
            self.add_widget(downButton)
        self.unlockAllButton = Button(font_size=40, text='Unlock All', size=(350, 50), size_hint=(None, None),
                                      pos=(0, 340), on_touch_down=self.unlockAll, color=(0, 0, 0, 1),
                                      background_normal='', background_color=(1, 1, 1, 1))
        self.add_widget(self.unlockAllButton)
        currentRow = 1
        index = len(grid) - 1
        diff = 1
        sqSize = int(1120 / (len(grid) * 2 - 1))
        if sqSize > 100:
            sqSize = 100
        sqSize *= 1.4
        xPosStart = int((1120 - (len(grid) * 2 - 1) * sqSize * .6) / 2 - sqSize / 2 * .6)  # 560 - 275
        yPosStart = int((1575 + (len(grid) * 2 - 1) * sqSize * .6) / 2 - sqSize / 2 * .6)  # 720 - 275
        for s in range(len(grid) * 2 - 1):
            for i in range(currentRow):
                if i > 0:
                    index += (len(grid) + 1) * i
                gridObject = grid[int(index / len(grid))][int(index % len(grid))]
                gridObjectX = int(xPosStart + (len(grid) - currentRow + (2 * i)) * sqSize * .6)
                # print("X: " + str(gridObjectX) + " | " + str(int((len(grid) - currentRow + (2*i)))))
                gridObjectY = int(yPosStart - (s * sqSize * .6))
                # print("Y: " + str(gridObjectY) + " | " + str(s))
                # sqSize *= 1.25
                if (gridObject) == 'S':
                    slot = CustomSlot(1, pos=(gridObjectX, gridObjectY), source='../res/screens/stats/SlotStrength.png',
                                      size=(sqSize, sqSize), on_touch_down=self.slotPressed)
                elif gridObject == 'M':
                    slot = CustomSlot(2, pos=(gridObjectX, gridObjectY), source='../res/screens/stats/SlotMagic.png',
                                      size=(sqSize, sqSize), on_touch_down=self.slotPressed)
                elif gridObject == 'A':
                    slot = CustomSlot(3, pos=(gridObjectX, gridObjectY), source='../res/screens/stats/SlotAgility.png',
                                      size=(sqSize, sqSize), on_touch_down=self.slotPressed)
                elif gridObject == 'D':
                    slot = CustomSlot(4, pos=(gridObjectX, gridObjectY), source='../res/screens/stats/SlotDexterity.png',
                                      size=(sqSize, sqSize), on_touch_down=self.slotPressed)
                elif gridObject == 'E':
                    slot = CustomSlot(5, pos=(gridObjectX, gridObjectY), source='../res/screens/stats/SlotEndurance.png',
                                      size=(sqSize, sqSize), on_touch_down=self.slotPressed)
                else:
                    slot = CustomSlot(6, pos=(gridObjectX, gridObjectY), source='../res/screens/stats/SlotEmpty.png',
                                      size=(sqSize, sqSize), on_touch_down=self.slotPressed)
                self.slots.append(slot)
                self.add_widget(slot)
                if i > 0:
                    index -= (len(grid) + 1) * i
            if s < len(grid) - 1:
                index -= 1
            else:
                index += len(grid)

            if (currentRow == len(grid)):
                diff = -1
            currentRow += diff

    def slotPressed(self, instance, touch):
        if instance.collide_point(*touch.pos):
            if self.currentSlot == None:
                # print(str(instance))
                if not instance.opened:
                    # print("slot pressed")
                    # print("True")
                    self.currentSlot = instance
                    self.confirm = Label(id='confirm_box', text='Are you sure?', size=(300, 150), font_size=50,
                                         pos=(0, 390), size_hint=(None, None), color=(1, 1, 1, 1))
                    with self.confirm.canvas.before:
                        Color(.1, .1, .1, .9)
                        Rectangle(size=(300, 150), pos=(self.confirm.x, self.confirm.y - 25))
                    yes = Button(text='unlock', color=(1, 1, 1, 1), size=(100, 45), font_size=30,
                                 pos=(self.confirm.x + 300 - 75 - 75 / 2, self.confirm.y), on_touch_down=self.onConfirm)
                    no = Button(text='cancel', color=(1, 1, 1, 1), size=(100, 45), font_size=30,
                                pos=(self.confirm.x + 75 - 75 / 2, self.confirm.y), on_touch_down=self.onCancel)
                    self.confirm.add_widget(yes)
                    self.confirm.add_widget(no)
                    self.add_widget(self.confirm)
                    # print(str(self))

    def unlockAll(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.confirm = Label(id='confirm_box', text='Are you sure?', size=(300, 150), font_size=50,
                                 center=(200, 400), size_hint=(None, None), color=(1, 1, 1, 1))
            with self.confirm.canvas.before:
                Color(.1, .1, .1, .9)
                Rectangle(size=(300, 150), pos=(self.confirm.x, self.confirm.y - 25))
            yes = Button(text='unlock', color=(1, 1, 1, 1), size=(100, 45), font_size=30,
                         pos=(self.confirm.x + 300 - 75 - 75 / 2, self.confirm.y), on_touch_down=self.onConfirmAll)
            no = Button(text='cancel', color=(1, 1, 1, 1), size=(100, 45), font_size=30,
                        pos=(self.confirm.x + 75 - 75 / 2, self.confirm.y), on_touch_down=self.onCancel)
            self.confirm.add_widget(yes)
            self.confirm.add_widget(no)
            self.add_widget(self.confirm)

    def unlockAllNum(self):
        for x in self.slots:
            if not x.opened:
                source = x.source[:-4]
                source += 'Unlocked.png'
                if x.slottype == 1:
                    self.rank.updateValues(0, 0, 0, self.rank.grid.SW, 0, 0, 0, 0)
                elif x.slottype == 2:
                    self.rank.updateValues(0, 0, 0, 0, self.rank.grid.MW, 0, 0, 0)
                elif x.slottype == 3:
                    self.rank.updateValues(0, 0, 0, 0, 0, self.rank.grid.AW, 0, 0)
                elif x.slottype == 4:
                    self.rank.updateValues(0, 0, 0, 0, 0, 0, self.rank.grid.DW, 0)
                elif x.slottype == 5:
                    self.rank.updateValues(0, 0, 0, 0, 0, 0, 0, self.rank.grid.EW)
                self.char.updateCharValues()
                self.managerObject.parent.parent.updateRankLabels()
                self.managerObject.parent.parent.updateRankPreviewLabels(self.rank.rankNum)
                x.source = source
                x.opened = True

    def onConfirmAll(self, instance, touch):
        if instance.collide_point(*touch.pos):
            for x in self.slots:
                if not x.opened:
                    source = x.source[:-4]
                    source += 'Unlocked.png'
                    if x.slottype == 1:
                        self.rank.updateValues(0, 0, 0, self.rank.grid.SW, 0, 0, 0, 0)
                    elif x.slottype == 2:
                        self.rank.updateValues(0, 0, 0, 0, self.rank.grid.MW, 0, 0, 0)
                    elif x.slottype == 3:
                        self.rank.updateValues(0, 0, 0, 0, 0, self.rank.grid.AW, 0, 0)
                    elif x.slottype == 4:
                        self.rank.updateValues(0, 0, 0, 0, 0, 0, self.rank.grid.DW, 0)
                    elif x.slottype == 5:
                        self.rank.updateValues(0, 0, 0, 0, 0, 0, 0, self.rank.grid.EW)
                    self.char.updateCharValues()
                    self.managerObject.parent.parent.updateRankLabels()
                    self.managerObject.parent.parent.updateRankPreviewLabels(self.rank.rankNum)
                    x.source = source
                    x.opened = True
            self.remove_widget(self.confirm)
            self.remove_widget(self.unlockAllButton)

    def onCancel(self, instance, touch):
        if instance.collide_point(*touch.pos):
            # print("Canceled")
            # print(str(self))
            self.currentSlot = None
            self.remove_widget(self.confirm)

    def onConfirm(self, instance, touch):
        if instance.collide_point(*touch.pos):
            if not self.currentSlot.opened:
                source = self.currentSlot.source[:-4]
                source += 'Unlocked.png'
                self.currentSlot.source = source
                # print("opened slot")
                if self.currentSlot.slottype == 1:
                    self.rank.updateValues(0, 0, 0, self.rank.grid.SW, 0, 0, 0, 0)
                elif self.currentSlot.slottype == 2:
                    self.rank.updateValues(0, 0, 0, 0, self.rank.grid.MW, 0, 0, 0)
                elif self.currentSlot.slottype == 3:
                    self.rank.updateValues(0, 0, 0, 0, 0, self.rank.grid.AW, 0, 0)
                elif self.currentSlot.slottype == 4:
                    self.rank.updateValues(0, 0, 0, 0, 0, 0, self.rank.grid.DW, 0)
                elif self.currentSlot.slottype == 5:
                    self.rank.updateValues(0, 0, 0, 0, 0, 0, 0, self.rank.grid.EW)
                self.char.updateCharValues()
                self.managerObject.parent.parent.updateRankLabels()
                self.managerObject.parent.parent.updateRankPreviewLabels(self.rank.rankNum)
                self.currentSlot.opened = True
                self.currentSlot = None
                self.remove_widget(self.confirm)

class NameLabel(Label):
    pass

class CustomSlot(Image):

    def __init__(self, slottype, **kwargs):
        kwargs.setdefault('keep_data', True)
        kwargs.setdefault('size_hint', (None, None))
        kwargs.setdefault('allow_stretch', True)
        # kwargs.setdefault('pos_hint', (None, None))
        super(CustomSlot, self).__init__(**kwargs)
        self.opacity = .8
        self.slottype = slottype
        self.opened = False

    def collide_point(self, x, y):
        if self.x <= x <= self.right and self.y <= y <= self.top:
            size = self.right - self.x
            scale = (200 / size)
            try:
                color = self._coreimage.read_pixel((x - self.x) * scale,
                                                   (self.height - (y - self.y)) * scale)
            except:
                color = 0, 0, 0, 0
            if color[-1] > 0:
                return True
        return False

class customButton(Image):

    def __init__(self, **kwargs):
        kwargs.setdefault('keep_data', True)
        kwargs.setdefault('size_hint', (None, None))
        super(customButton, self).__init__(**kwargs)
        self.opacity = 1

    def collide_point(self, x, y):
        if self.x <= x <= self.right and self.y <= y <= self.top:
            scale = self._coreimage.size[0] / (self.right - self.x)
            try:
                color = self._coreimage.read_pixel((x - self.x) * scale,
                                                   (self.height - (y - self.y)) * scale)
            except:
                color = 0, 0, 0, 0
            if color[-1] > 0:
                return True
        return False

class StatLabel(Label):

    def __init__(self, **kwargs):
        super(StatLabel, self).__init__(**kwargs)
        if self.font_size != 60 and self.font_size != 50:
            self.font_size = 40

class StatPreview(Image):

    def __init__(self, char, rank, attacktype, totalstats, physicalattack, magicalattack, magicalpoints, health,
                 defense, strength, magic, agility, dexterity, endurance, **kwargs):
        super(StatPreview, self).__init__(**kwargs)
        self.source = "../res/screens/stats/TotalSingleAttackWindow.png"
        self.size_hint = None, None
        self.allow_stretch = True
        self.keep_ratio = False
        x = self.x + 10
        y = self.y + self.height * .85
        # size: app.size
        # allow_stretch: True
        # keep_ratio: False
        # source: 'res/TotalSingleAttackWindow'

        if totalstats:
            y -= 25
            x += 10
            barwidth = 166
            barheight = (self.height * .85) / 5
            self.add_widget(Label(text="Total   Stats", color=(.1, .1, .1, 1), font_size=40, pos=(x + 55, y - 10)))
            y -= (barheight / 2 - 10) + 25
            self.add_widget(Image(source='../res/screens/stats/StatBar.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                                  allow_stretch=True))
            self.add_widget(Image(source='../res/screens/stats/Health.png', size=(40, 40), pos=(x + 15, y + 5)))
            self.healthlabel = StatLabel(text='HP')
            self.healthlabel.x = x + 65
            self.healthlabel.y = y
            self.healthlabelnumber = StatLabel(text='%d' % health, color=(0, 0, 0, 1))
            self.healthlabelnumber.x = x + 190
            self.healthlabelnumber.y = y
            self.healthlabeldiff = StatLabel(text='(+ 0)', color=(.3, .4, .6, 1))
            self.healthlabeldiff.x = x + 310
            self.healthlabeldiff.y = y
            self.add_widget(self.healthlabelnumber)
            self.add_widget(self.healthlabeldiff)
            self.add_widget(self.healthlabel)

            y -= (barheight + 5)
            self.add_widget(Image(source='../res/screens/stats/StatBar.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                                  allow_stretch=True))
            self.add_widget(Image(source='../res/screens/stats/Mana.png', size=(40, 40), pos=(x + 15, y + 5)))
            self.magicalpointlabel = StatLabel(text='MP')
            self.magicalpointlabel.x = x + 65
            self.magicalpointlabel.y = y
            self.magicalpointlabelnumber = StatLabel(text='%d' % magicalpoints, color=(0, 0, 0, 1))
            self.magicalpointlabelnumber.x = x + 190
            self.magicalpointlabelnumber.y = y
            self.magicalpointlabeldiff = StatLabel(text='(+0)', color=(.3, .4, .6, 1))
            self.magicalpointlabeldiff.x = x + 310
            self.magicalpointlabeldiff.y = y
            self.add_widget(self.magicalpointlabelnumber)
            self.add_widget(self.magicalpointlabeldiff)
            self.add_widget(self.magicalpointlabel)

            y -= (barheight + 5)
            if attacktype == 1:
                self.add_widget(
                    Image(source='../res/screens/stats/StatBar.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                          allow_stretch=True))
                self.add_widget(Image(source='../res/screens/stats/PhysicalAttack.png', size=(40, 40), pos=(x + 15, y + 5)))
                self.attacklabel = StatLabel(text='P.Atk')
                self.attacklabel.x = x + 65
                self.attacklabel.y = y
                self.attacklabelnumber = StatLabel(text='%d' % physicalattack, color=(0, 0, 0, 1))
                self.attacklabelnumber.x = x + 190
                self.attacklabelnumber.y = y
                self.attacklabeldiff = StatLabel(text='(+0)', color=(.3, .4, .6, 1))
                self.attacklabeldiff.x = x + 310
                self.attacklabeldiff.y = y
                self.add_widget(self.attacklabelnumber)
                self.add_widget(self.attacklabeldiff)
                self.add_widget(self.attacklabel)
            elif attacktype == 2:
                self.add_widget(
                    Image(source='../res/screens/stats/StatBar.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                          allow_stretch=True))
                self.add_widget(Image(source='../res/screens/stats/MagicalAttack.png', size=(40, 40), pos=(x + 15, y + 5)))
                self.attacklabel2 = StatLabel(text='M.Atk')
                self.attacklabel2.x = x + 65
                self.attacklabel2.y = y
                self.attacklabel2number = StatLabel(text='%d' % magicalattack, color=(0, 0, 0, 1))
                self.attacklabel2number.x = x + 190
                self.attacklabel2number.y = y
                self.attacklabel2diff = StatLabel(text='(+0)', color=(.3, .4, .6, 1))
                self.attacklabel2diff.x = x + 310
                self.attacklabel2diff.y = y
                self.add_widget(self.attacklabel2number)
                self.add_widget(self.attacklabel2diff)
                self.add_widget(self.attacklabel2)
            else:
                self.add_widget(
                    Image(source='../res/screens/stats/StatBar.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                          allow_stretch=True))
                self.add_widget(Image(source='../res/screens/stats/PhysicalAttack.png', size=(40, 40), pos=(x + 15, y + 5)))
                self.attacklabel = StatLabel(text='P.Atk')
                self.attacklabel.x = x + 65
                self.attacklabel.y = y
                self.attacklabelnumber = StatLabel(text='%d' % physicalattack, color=(0, 0, 0, 1))
                self.attacklabelnumber.x = x + 190
                self.attacklabelnumber.y = y
                self.attacklabeldiff = StatLabel(text='(+0)', color=(.3, .4, .6, 1))
                self.attacklabeldiff.x = x + 310
                self.attacklabeldiff.y = y
                self.add_widget(self.attacklabelnumber)
                self.add_widget(self.attacklabeldiff)
                self.add_widget(self.attacklabel)
                y -= (barheight + 5)
                self.add_widget(
                    Image(source='../res/screens/stats/StatBar.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                          allow_stretch=True))
                self.add_widget(Image(source='../res/screens/stats/magicalAttack.png', size=(40, 40), pos=(x + 15, y + 5)))
                self.attacklabel2 = StatLabel(text='M.Atk')
                self.attacklabel2.x = x + 65
                self.attacklabel2.y = y
                self.attacklabel2number = StatLabel(text='%d' % magicalattack, color=(0, 0, 0, 1))
                self.attacklabel2number.x = x + 190
                self.attacklabel2number.y = y
                self.attacklabel2diff = StatLabel(text='(+0)', color=(.3, .4, .6, 1))
                self.attacklabel2diff.x = x + 310
                self.attacklabel2diff.y = y
                self.add_widget(self.attacklabel2number)
                self.add_widget(self.attacklabel2diff)
                self.add_widget(self.attacklabel2)
            y -= (barheight + 5)
            self.add_widget(Image(source='../res/screens/stats/StatBar.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                                  allow_stretch=True))
            self.add_widget(Image(source='../res/screens/stats/Defense.png', size=(40, 40), pos=(x + 15, y + 5)))
            self.defenselabel = StatLabel(text='Def')
            self.defenselabel.x = x + 65
            self.defenselabel.y = y
            self.defenselabelnumber = StatLabel(text='%d' % defense, color=(0, 0, 0, 1))
            self.defenselabelnumber.x = x + 190
            self.defenselabelnumber.y = y

            self.defenselabeldiff = StatLabel(text='(+0)', color=(.3, .4, .6, 1))
            self.defenselabeldiff.x = x + 310
            self.defenselabeldiff.y = y
            self.add_widget(self.defenselabelnumber)
            self.add_widget(self.defenselabeldiff)
            self.add_widget(self.defenselabel)
            y += 200
            x += 470
            barwidth = 330
            barheight = 60
            if attacktype == 1:
                self.add_widget(
                    Image(source='../res/screens/stats/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                          allow_stretch=True))
                self.strengthlabel = StatLabel(text='Str.', font_size=50, color=(0, 0, 0, 1), pos=(x + 20, y))
                print(str(strength))
                print(str(char.ranks[9].strengthMax))
                self.strengthgrade = Image(source=Scale.getScaleAsImagePath(strength, char.totalCaps[0]),
                                           pos=(x + 90, y + 10), height=40, keep_ratio=True, allow_stretch=True)
                self.strengthnumber = StatLabel(text='%d' % strength, font_size=50, color=(0, 0, 0, 1),
                                                pos=(x + 180, y))
                self.add_widget(self.strengthgrade)
                self.add_widget(self.strengthlabel)
                self.add_widget(self.strengthnumber)
            elif attacktype == 2:
                self.add_widget(
                    Image(source='../res/screens/stats/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                          allow_stretch=True))
                self.magiclabel = StatLabel(text='Mag.', font_size=50, color=(0, 0, 0, 1), pos=(x + 20, y))
                self.magicgrade = Image(source=Scale.getScaleAsImagePath(magic, char.totalCaps[1]),
                                        pos=(x + 90, y + 10),
                                        height=40, keep_ratio=True, allow_stretch=True)
                self.magicnumber = StatLabel(text='%d' % magic, font_size=50, color=(0, 0, 0, 1), pos=(x + 180, y))
                self.add_widget(self.magicgrade)
                self.add_widget(self.magiclabel)
                self.add_widget(self.magicnumber)
            else:
                self.add_widget(
                    Image(source='../res/screens/stats/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                          allow_stretch=True))
                self.strengthlabel = StatLabel(text='Str.', font_size=50, color=(0, 0, 0, 1), pos=(x + 20, y))
                self.strengthgrade = Image(source=Scale.getScaleAsImagePath(strength, char.totalCaps[0]),
                                           pos=(x + 90, y + 10), height=40, keep_ratio=True, allow_stretch=True)
                self.strengthnumber = StatLabel(text='%d' % strength, font_size=50, color=(0, 0, 0, 1),
                                                pos=(x + 180, y))
                self.add_widget(self.strengthgrade)
                self.add_widget(self.strengthlabel)
                self.add_widget(self.strengthnumber)
                y -= 70
                self.add_widget(
                    Image(source='../res/screens/stats/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                          allow_stretch=True))
                self.magiclabel = StatLabel(text='Mag.', font_size=50, color=(0, 0, 0, 1), pos=(x + 20, y))
                self.magicgrade = Image(source=Scale.getScaleAsImagePath(magic, char.totalCaps[1]),
                                        pos=(x + 90, y + 10),
                                        height=40, keep_ratio=True, allow_stretch=True)
                self.magicnumber = StatLabel(text='%d' % magic, font_size=50, color=(0, 0, 0, 1), pos=(x + 180, y))
                self.add_widget(self.magicgrade)
                self.add_widget(self.magiclabel)
                self.add_widget(self.magicnumber)
            y -= 70
            self.add_widget(Image(source='../res/screens/stats/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                                  allow_stretch=True))
            self.agilitylabel = StatLabel(text='Agi.', font_size=50, color=(0, 0, 0, 1), pos=(x + 20, y))
            self.agilitygrade = Image(source=Scale.getScaleAsImagePath(agility, char.totalCaps[2]),
                                      pos=(x + 90, y + 10),
                                      height=40, keep_ratio=True, allow_stretch=True)
            self.agilitynumber = StatLabel(text='%d' % agility, font_size=50, color=(0, 0, 0, 1), pos=(x + 180, y))
            self.add_widget(self.agilitygrade)
            self.add_widget(self.agilitylabel)
            self.add_widget(self.agilitynumber)
            y -= 70
            self.add_widget(Image(source='../res/screens/stats/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                                  allow_stretch=True))
            self.dexteritylabel = StatLabel(text='Dex.', font_size=50, color=(0, 0, 0, 1), pos=(x + 20, y))
            self.dexteritygrade = Image(source=Scale.getScaleAsImagePath(dexterity, char.totalCaps[3]),
                                        pos=(x + 90, y + 10), height=40, keep_ratio=True, allow_stretch=True)
            self.dexteritynumber = StatLabel(text='%d' % dexterity, font_size=50, color=(0, 0, 0, 1), pos=(x + 180, y))
            self.add_widget(self.dexteritygrade)
            self.add_widget(self.dexteritylabel)
            self.add_widget(self.dexteritynumber)
            y -= 70
            self.add_widget(Image(source='../res/screens/stats/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                                  allow_stretch=True))
            self.endurancelabel = StatLabel(text='End.', font_size=50, color=(0, 0, 0, 1), pos=(x + 20, y))
            self.endurancegrade = Image(source=Scale.getScaleAsImagePath(endurance, char.totalCaps[4]),
                                        pos=(x + 90, y + 10), height=40, keep_ratio=True, allow_stretch=True)
            self.endurancenumber = StatLabel(text='%d' % endurance, font_size=50, color=(0, 0, 0, 1), pos=(x + 180, y))
            self.add_widget(self.endurancegrade)
            self.add_widget(self.endurancelabel)
            self.add_widget(self.endurancenumber)
            y += 200
            x += 470
            # self.healthLvlBar = ProgressBar(max = 120, value = 0, pos =(x, y), width = 200, height =25)
            # self.mpLvlBar = ProgressBar(max = 120, value = 0, pos= (x,y), width = 200, height = 25)
            # Health Exp Bar
            self.healthLvlBar = ProgressBar(1, (275, 25))
            self.healthLvlBar.max = char.ranks[char.currentRank - 1].expHpCap
            self.healthLvlBar.value = char.ranks[char.currentRank - 1].exphealth
            self.healthLvlBar.pos = 890, 190
            self.healthLvlTitle = Label(text='HP', font_size=30, color=(0, 0, 0, 1), size=(50, 20), pos=(860, 200))
            self.healthLvlTitle.size = self.healthLvlTitle.texture_size
            self.add_widget(self.healthLvlBar)
            self.add_widget(self.healthLvlTitle)
            # Mp Exp Bar
            self.mpLvlBar = ProgressBar(2, (275, 25))
            self.mpLvlBar.max = char.ranks[char.currentRank - 1].expMpCap
            self.mpLvlBar.value = char.ranks[char.currentRank - 1].expmagicalpoints
            self.mpLvlBar.pos = 890, 160
            self.mpLvlTitle = Label(text='MP', font_size=30, color=(0, 0, 0, 1), size=(50, 20), pos=(860, 170))
            self.mpLvlTitle.size = self.mpLvlTitle.texture_size
            self.add_widget(self.mpLvlBar)
            self.add_widget(self.mpLvlTitle)
            # Def Exp Bar
            self.defLvlBar = ProgressBar(0, (275, 25))
            self.defLvlBar.max = char.ranks[char.currentRank - 1].expDefCap
            self.defLvlBar.value = char.ranks[char.currentRank - 1].expdefense
            self.defLvlBar.pos = 890, 130
            self.defLvlTitle = Label(text='Def', font_size=30, color=(0, 0, 0, 1), size=(50, 20), pos=(860, 140))
            self.defLvlTitle.size = self.defLvlTitle.texture_size
            self.add_widget(self.defLvlBar)
            self.add_widget(self.defLvlTitle)
            # Str Exp Bar
            self.strLvlBar = ProgressBar(1, (275, 25))
            self.strLvlBar.max = char.ranks[char.currentRank - 1].expStrCap
            self.strLvlBar.value = char.ranks[char.currentRank - 1].expstrength
            self.strLvlBar.pos = 890, 100
            self.strLvlTitle = Label(text='Str', font_size=30, color=(0, 0, 0, 1), size=(50, 20), pos=(860, 110))
            self.strLvlTitle.size = self.strLvlTitle.texture_size
            self.add_widget(self.strLvlBar)
            self.add_widget(self.strLvlTitle)
            # Agi Exp Bar
            self.agiLvlBar = ProgressBar(3, (275, 25))
            self.agiLvlBar.max = char.ranks[char.currentRank - 1].expAgiCap
            self.agiLvlBar.value = char.ranks[char.currentRank - 1].expagility
            self.agiLvlBar.pos = 890, 70
            self.agiLvlTitle = Label(text='Agi', font_size=30, color=(0, 0, 0, 1), size=(50, 20), pos=(860, 80))
            self.agiLvlTitle.size = self.agiLvlTitle.texture_size
            self.add_widget(self.agiLvlBar)
            self.add_widget(self.agiLvlTitle)
            # Dex Exp Bar
            self.dexLvlBar = ProgressBar(4, (275, 25))
            self.dexLvlBar.max = char.ranks[char.currentRank - 1].expDexCap
            self.dexLvlBar.value = char.ranks[char.currentRank - 1].expdexterity
            self.dexLvlBar.pos = 890, 40
            self.dexLvlTitle = Label(text='Dex', font_size=30, color=(0, 0, 0, 1), size=(50, 20), pos=(860, 50))
            self.dexLvlTitle.size = self.dexLvlTitle.texture_size
            self.add_widget(self.dexLvlBar)
            self.add_widget(self.dexLvlTitle)
            # End Exp Bar
            self.endLvlBar = ProgressBar(5, (275, 25))
            self.endLvlBar.max = char.ranks[char.currentRank - 1].expEndCap
            self.endLvlBar.value = char.ranks[char.currentRank - 1].expendurance
            self.endLvlBar.pos = 890, 10
            self.endLvlTitle = Label(text='End', font_size=30, color=(0, 0, 0, 1), size=(50, 20), pos=(860, 20))
            self.endLvlTitle.size = self.endLvlTitle.texture_size
            self.add_widget(self.endLvlBar)
            self.add_widget(self.endLvlTitle)
            # self.add_widget(self.mpLvlBar)
        if not totalstats:
            y -= 50
            self.add_widget(Label(text="Rank Attributes", color=(.1, .1, .1, 1), font_size=40, pos=(x + 90, y + 20)))
            barwidth = 330
            barheight = 60
            y -= 15
            if attacktype == 1:
                self.add_widget(
                    Image(source='../res/screens/stats/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                          allow_stretch=True))
                self.strengthlabel = StatLabel(text='Str.', font_size=50, color=(0, 0, 0, 1), pos=(x + 20, y))
                self.strengthgrade = Image(source=Scale.getScaleAsImagePath(strength, char.ranks[rank - 1].strengthMax),
                                           pos=(x + 90, y + 10), height=40, keep_ratio=True, allow_stretch=True)
                self.strengthnumber = StatLabel(text='%d' % strength, font_size=50, color=(0, 0, 0, 1),
                                                pos=(x + 180, y))
                self.add_widget(self.strengthgrade)
                self.add_widget(self.strengthlabel)
                self.add_widget(self.strengthnumber)
            elif attacktype == 2:
                self.add_widget(
                    Image(source='../res/screens/stats/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                          allow_stretch=True))
                self.magiclabel = StatLabel(text='Mag.', font_size=50, color=(0, 0, 0, 1), pos=(x + 20, y))
                self.magicgrade = Image(source=Scale.getScaleAsImagePath(magic, char.ranks[rank - 1].magicMax),
                                        pos=(x + 90, y + 10), height=40, keep_ratio=True, allow_stretch=True)
                self.magicnumber = StatLabel(text='%d' % magic, font_size=50, color=(0, 0, 0, 1), pos=(x + 180, y))
                self.add_widget(self.magicgrade)
                self.add_widget(self.magiclabel)
                self.add_widget(self.magicnumber)
            else:
                self.add_widget(
                    Image(source='../res/screens/stats/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                          allow_stretch=True))
                self.strengthlabel = StatLabel(text='Str.', font_size=50, color=(0, 0, 0, 1), pos=(x + 20, y))
                self.strengthgrade = Image(source=Scale.getScaleAsImagePath(strength, char.ranks[rank - 1].strengthMax),
                                           pos=(x + 90, y + 10), height=40, keep_ratio=True, allow_stretch=True)
                self.strengthnumber = StatLabel(text='%d' % strength, font_size=50, color=(0, 0, 0, 1),
                                                pos=(x + 180, y))
                self.add_widget(self.strengthgrade)
                self.add_widget(self.strengthlabel)
                self.add_widget(self.strengthnumber)
                y -= 70
                self.add_widget(
                    Image(source='../res/screens/stats/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                          allow_stretch=True))
                self.magiclabel = StatLabel(text='Mag.', font_size=60, color=(0, 0, 0, 1), pos=(x + 20, y))
                self.magicgrade = Image(source=Scale.getScaleAsImagePath(magic, char.ranks[rank - 1].magicMax),
                                        pos=(x + 90, y + 10), height=40, keep_ratio=True, allow_stretch=True)
                self.magicnumber = StatLabel(text='%d' % magic, font_size=50, color=(0, 0, 0, 1), pos=(x + 180, y))
                self.add_widget(self.magicgrade)
                self.add_widget(self.magiclabel)
                self.add_widget(self.magicnumber)
            y -= 70
            self.add_widget(Image(source='../res/screens/stats/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                                  allow_stretch=True))
            self.agilitylabel = StatLabel(text='Agi.', font_size=50, color=(0, 0, 0, 1), pos=(x + 20, y))
            self.agilitygrade = Image(source=Scale.getScaleAsImagePath(agility, char.ranks[rank - 1].agilityMax),
                                      pos=(x + 90, y + 10), height=40, keep_ratio=True, allow_stretch=True)
            self.agilitynumber = StatLabel(text='%d' % agility, font_size=50, color=(0, 0, 0, 1), pos=(x + 180, y))
            self.add_widget(self.agilitygrade)
            self.add_widget(self.agilitylabel)
            self.add_widget(self.agilitynumber)
            y -= 70
            self.add_widget(Image(source='../res/screens/stats/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                                  allow_stretch=True))
            self.dexteritylabel = StatLabel(text='Dex.', font_size=50, color=(0, 0, 0, 1), pos=(x + 20, y))
            self.dexteritygrade = Image(source=Scale.getScaleAsImagePath(dexterity, char.ranks[rank - 1].dexterityMax),
                                        pos=(x + 90, y + 10), height=40, keep_ratio=True, allow_stretch=True)
            self.dexteritynumber = StatLabel(text='%d' % dexterity, font_size=50, color=(0, 0, 0, 1), pos=(x + 180, y))
            self.add_widget(self.dexteritygrade)
            self.add_widget(self.dexteritylabel)
            self.add_widget(self.dexteritynumber)
            y -= 70
            self.add_widget(Image(source='../res/screens/stats/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                                  allow_stretch=True))
            self.endurancelabel = StatLabel(text='End.', font_size=50, color=(0, 0, 0, 1), pos=(x + 20, y))
            self.endurancegrade = Image(source=Scale.getScaleAsImagePath(endurance, char.ranks[rank - 1].enduranceMax),
                                        pos=(x + 90, y + 10), height=40, keep_ratio=True, allow_stretch=True)
            self.endurancenumber = StatLabel(text='%d' % endurance, font_size=50, color=(0, 0, 0, 1), pos=(x + 180, y))
            self.add_widget(self.endurancegrade)
            self.add_widget(self.endurancelabel)
            self.add_widget(self.endurancenumber)