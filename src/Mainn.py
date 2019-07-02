from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
import ctypes
import math
from kivy.core.window import Window
from Entities import Character
from Entities.Character import Attack, Scale
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
import random
from kivy.graphics import Color, Rectangle, Mesh
from kivy.properties import NumericProperty, BooleanProperty, ObjectProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager, FadeTransition, Screen, SlideTransition
import time
from kivy.graphics.texture import Texture
from itertools import chain


def AdventureGame():
    pass

class Gradient(object):

    @staticmethod
    def horizontal(*args):
        texture = Texture.create(size=(len(args), 1), colorfmt='rgba')
        buf = bytes([ int(v * 255)  for v in chain(*args) ])  # flattens

        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        return texture

    @staticmethod
    def vertical(*args):
        texture = Texture.create(size=(1, len(args)), colorfmt='rgba')
        buf = bytes([ int(v * 255)  for v in chain(*args) ])  # flattens

        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        return texture

    @staticmethod
    def diagonal(*args):
        texture = Texture.create(size=(1, len(args)), colorfmt='rgba')
        buf = bytes([int(v * 255) for v in chain(*args)])  # flattens

        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        return texture

class MyScreenManager(ScreenManager):
    def __init__(self, *args, **kwargs):
        super(MyScreenManager, self).__init__(*args, **kwargs)
        self.list = []
    def makeArray(self):
        pass

    def setScreen(self, currscreenid, nextscreenid):
        self.list.append(currscreenid)
        self.current = nextscreenid

    def goto_previous(self):
        if self.list:
            self.current = self.list.pop()
            return True
        return False
class NewGameScreen(Screen):
    pass
class TitleScreen(Screen):
    pass
class SelectScreen(Screen):
    def chooseCharacter(self, choice):
        pass
class TownScreen(Screen):
    pass

class DungeonMain(Screen):
    level = NumericProperty(1)
    score = NumericProperty(1)
    boss = StringProperty('')
    def showcurrentparty(self):
        # print("showing party")
        global screenManager
        screenmanager = self.parent
        party = []
        for x in App.currentparty:
            party.append(App.characterArray[x])
            print(party[x].name)
        filled = len(party)
        if (filled > 4):
            filled = 4
        empty = 6 - filled

        slot = CharacterPreview()
        slot.pos = 2560 - (300 * 5 + 950), 100
        slot.id = 'slot%d' % 1
        slot2 = emptycharacterpreview()
        slot.add_widget(slot2)
        self.add_widget(slot)
        # for x in range(empty):
        #     slot = CharacterPreview()
        #     slot.pos = 2560 - (300 * x + 950), 100
        #     slot.id = 'slot%d' % x
        #     # print('(empty slot) making ' + str(slot.id))
        #     slot2 = emptycharacterpreview()
        #     slot.add_widget(slot2)
        #     self.add_widget(slot)
        # for x in range(filled):
        #     shownparty.append(party[filled - 1 - x])
        #     slot = CharacterPreview()
        #     slot.pos = 2560 - (300 * (x + empty) + 950), 100
        #     slot.id = 'slot%d' % (x + empty)
        #     # print('(filled slot) making ' + str(slot.id))
        #     slot2 = filledcharacterpreviewS(party[filled-1-x])
        #     slot.add_widget(slot2)
        #     self.add_widget(slot)
        if (self.level < 2):
            print('disabling ascend')
            self.ids['ascend'].disabled = True
            self.ids['ascend_text'].text = '[s]Ascend[/s]'
        else:
            print('enabling ascend')
            self.ids['ascend_text'].text = 'Ascend'
            self.ids['ascend'].disabled = False
        self.calculatepartyscore(App.currentparty)

    def delve(self):
        if len(shownparty) > 0:
            print('delving into dungeon!')
            # self.level = self.level + 1
            screen = DungeonBattle()

            screen.level = self.level
            screen.boss = self.boss
            self.parent.add_widget(screen)
            self.parent.current = 'dungeon_battle'
            # print(str(self.parent.children))
            if (self.level < 2):
                print('disabling ascend')
                self.ids['ascend'].disabled = True
                self.ids['ascend_text'].text = '[s]Ascend[/s]'
            else:
                print('enabling ascend')
                self.ids['ascend_text'].text = 'Ascend'
                self.ids['ascend'].disabled = False
        else:
            print("not enough cahracters to explore")

    def ascend(self):
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
            print("not enough cahracters to explore")

    def calculatepartyscore(self, party):
        tempparty = []
        for x in party:
            tempparty.append(App.characterArray[x])
        party = tempparty
        score = 0
        bigscore = 0
        for x in range(len(party)):
            score += party[x].gethealth()
            score += party[x].getmagicalpoints()
            score /= 1.5
            score += party[x].getdefense()
            score /= 1.2
            score += party[x].getphysicalattack()
            score += party[x].getmagicalattack()
            score /= 2
            score += party[x].getendurance()
            score += party[x].getstrength()
            score += party[x].getmagic()
            score += party[x].getdexterity()
            score += party[x].getagility()
            score /= 3
            score = math.ceil(score)
            bigscore += score
            score = 0
        self.score = bigscore
class DungeonBattle(Screen):
    level = NumericProperty(1)
    boss = BooleanProperty(False)
    level_label = ObjectProperty(None)
    screen = ObjectProperty(None)
    currentTurn = NumericProperty(1)


    def __init__(self):
        super(DungeonBattle, self).__init__()
        Clock.schedule_once(self.appear_main, 0.5)
        Clock.schedule_once(self.disappear_main, 1.5)
        self.enemyLocations = ((1500, 800), (1500, 1000), (1500, 600), (1700, 700), (1700, 900), (1700, 1100), (1700, 500), (1500, 1200), (1500, 400), (1900, 800), (1900, 1000), (1900, 600))
        self.enemyAmounts = (3, 3, 4, 5, 6)

    def appear_main(self, tis):

        if (self.boss):
            self.level_label.text= 'Level %d BOSS' % self.level
        else:
            self.level_label.text = 'Level %d' % self.level
    def disappear_main(self, tis):
        self.level_label.text = ''
        self.make_gui()

    def make_gui(self):
        currentparty = shownparty

        for x in range(len(currentparty)):
            # print(currentparty[x].getname() + shownparty[x].getname())
            preview = CharPreview(currentparty[x])
            sprite = Image()
            sprite.id = 'sprite%d' % x
            sprite.source = currentparty[x].getsprite()
            sprite.center = 450, 600 + (200*x)
            sprite.size = 200, 200
            sprite.keep_ratio = True
            sprite.allow_stretch = True
            sprite.size_hint = None, None
            preview.id = 'charid%d' % x
            preview.source = currentparty[x].getpreviewimage()
            preview.pos = (225 * x + 200, 50)

            self.main_layout.add_widget(sprite)
            self.screen.add_widget(preview)
        numofenemys = random.randint(0, self.enemyAmounts[0]-1) + 1 #generate enemys
        for x in range(numofenemys):
            enemy = Enemy()
            enemy.health = 100
            enemy.id = 'enemy%d' % x
            enemy.source = 'res/wolf.gif'
            enemy.size = 200, 200
            enemy.size_hint = None, None
            enemy.center = self.enemyLocations[x]
            self.enemy_layout.add_widget(enemy)
        bar = MoveBarObject()
        self.main_layout.add_widget(bar)

    def attack(self):
        self.currentTurn += 1
        print("Turn: " + str(self.currentTurn))
        numofchars = 4
        maxfoes = len(self.enemy_layout.children)
        if (maxfoes > 0):
            for y in range(maxfoes):
                print("Enemy #%d" % y)
                print("\tHealth: " + str(self.enemy_layout.children[maxfoes - 1 - y].health))
            for x in range(numofchars):
                maxfoes = len(self.enemy_layout.children)
                if maxfoes > 0:
                    attack = self.children[numofchars - 1 - x].char.getmove(self.children[numofchars - 1 - x].selectedMove)
                    foenum = -1
                    if attack.ttype == 0:
                        foenum = attack.findfoe(maxfoes-1)
                    print("DEBUG: " + str(foenum) + " " + str(maxfoes))
                    print("\u001B[32m" + self.children[numofchars-1-x].char.getname() + " uses " + attack.name)
                    print("\tAttack Targeting Type: " + str(attack.ttypeS))
                    print("\tAttack Type: " + attack.type)
                    damage = attack.generateDamage(self.children[numofchars - 1 - x].char.getattack(attack.type))
                    print("\tAttack Damage: " + str(damage) + "\u001B[29m")
                    if foenum == -1:
                        pass
                    else:
                        health = self.enemy_layout.children[maxfoes - 1 - foenum].health
                        self.enemy_layout.children[maxfoes - 1 - foenum].health = health - damage
                        health = self.enemy_layout.children[maxfoes - 1 - foenum].health
                        if (health < 0):
                            print("\u001B[31mEnemy #" + str(foenum) + " defeated! Removed from children list.\u001B[29m")
                            self.enemy_layout.remove_widget(self.enemy_layout.children[maxfoes - 1 - foenum])
                        print("\u001B[33mEnemy #" + str(foenum) + " takes " + str(damage) + " damage. Health is now " + str(health) + "\u001B[29m")
                else:
                    print("You have won!")
                    break

class CharacterPreview(ScreenManager):

    def __init__(self):
        super(CharacterPreview, self).__init__()

    def makepreviewscreen(self, currentCharacter):
        # print("making preview")
        screen = scrollcharacterpreview()
        screen.name = 'preview'
        shownparty = []
        # for x in App.currentparty:
        #     shownparty.append(App.characterArray[x])
        #     print(shownparty[x].name)
        party = App.characterArray
        # print(len(party))
        if (len(party) < 4):
            size = len(party)
        else:
            size = 4
        screen.size = 250 * size, 650
        self.size = 250 * size, 650

        screen.children[0].children[0].size = len(party)*250, 650

        for x in range(len(party)):
            preview = filledcharacterPreview(party[x], currentCharacter)
            for i in range(len(shownparty)):
                # print(str(shownparty[i].getname()))
                # print(str(party[x].getname()))
                if (shownparty[i].equals(party[x])):
                    if isinstance(currentCharacter, Character.Character):
                        if shownparty[i].equals(currentCharacter):
                            print("Character is Current! > " + str(currentCharacter.getid()))
                            label = Label(text='Current', color=(1, 1, 1, 1), pos=(250 * x, 0), font_size=48,
                                          size=(250, 650))
                            with preview.canvas:
                                Color(.1, .1, .1, .15)
                                Rect = Rectangle(size=(250, 650), pos=(250*x,0))
                            preview.add_widget(label)
                        else:
                            print("Character already shown! > " + str(party[x].getid()))
                            label = Label(text='In Party', color=(1, 1, 1, 1), pos=(250 * x, 0), font_size=48,
                                          size=(250, 650))
                            with preview.canvas:
                                Color(0, 0, 0, .35)
                                Rect = Rectangle(size=(250, 650), pos=(250 * x, 0))
                            preview.enabled = True
                            preview.disabled = True
                            preview.add_widget(label)
                    else:
                        print("Character already shown! > " + str(party[x].getid()))
                        label = Label(text='In Party', color=(1, 1, 1, 1), pos=(250 * x, 0), font_size=48,
                                      size=(250, 650))
                        with preview.canvas:
                            Color(0, 0, 0, .35)
                            Rect = Rectangle(size=(250, 650), pos=(250 * x, 0))
                        preview.enabled = True
                        preview.disabled = True
                        preview.add_widget(label)
            preview.pos = (250*x, 0)
            screen.children[0].children[0].add_widget(preview)
        self.switch_to(screen)
class filledcharacterpreviewS(Screen):
    def __init__(self, char):
        super(filledcharacterpreviewS, self).__init__()
        self.add_widget(filledcharacterPreview(char, "null"))
class filledcharacterPreview(Button):
    char = ObjectProperty()
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.enabled:
                if touch.button == 'left':
                    if not touch.is_double_tap:
                        Clock.schedule_once(self.empty, .4)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            if not self.enabled:
                print("disabled")
            else:
                if touch.button == 'right':
                    print("Filled Character Preview Screen Right Clicked")
                    # x = self
                    # while not isinstance(x, MyScreenManager):
                    #     x = self.parent
                    #     print(x)
                    if isinstance(self.parent, filledcharacterpreviewS):
                        self.manager = self.parent.parent.parent.parent
                    else:
                        self.manager = self.parent.parent.parent.parent.parent.parent
                    screen = CharacterAttributeScreen(self.char)
                    self.manager.add_widget(screen)
                    # App.manager = self.manager
                    self.manager.setScreen ('dungeon_main', screen.name)
                else:
                    if touch.is_double_tap:
                        print("Filled Character Preview Screen Double Clicked")
                    else:
                        print("Filled Character Preview Screen Left Clicked")
                        Clock.unschedule(self.empty)
                        if isinstance(self.parent, filledcharacterpreviewS):
                            self.parent.parent.makepreviewscreen(self.char)
                        elif isinstance(self.parent, BoxLayout):
                            screen = filledcharacterpreviewS(self.char)
                            App.currentparty.append(self.char.index)
                            shell = self.parent.parent.parent.parent
                            shell.parent.calculatepartyscore(App.currentparty)
                            screen.name = 'selection'
                            screen.id = 'selection'
                            if isinstance(self.oldchar, Character.Character):
                                if (self.char.equals(self.oldchar)):
                                    print("selected the current")
                                else:
                                    App.currentparty.remove(self.oldchar.index)
                                    print("Removed " + self.oldchar.getid())
                            shell.size = (250, 650)
                            shell.switch_to(screen, direction='right')

    def empty(self, its):
        if isinstance(self.parent, filledcharacterpreviewS):
            screen = emptycharacterpreview()
            App.currentparty.remove(self.char.index)
            screen.name = 'empty'
            screen.id = 'empty'
            self.parent.parent.switch_to(screen, direction='right')

    def __init__(self, char, oldchar):
        super(filledcharacterPreview, self).__init__()
        self.enabled = True
        self.char = char
        self.oldchar = oldchar
        self.id = char.getname()
        image = self.ids['image']
        image.source = char.getimage()
        self.showCharValues(char, self.x)

    def chooseselection(self):
        pass

    def showCharValues(self, char, x):
        label = self.ids['physicalattack']
        label.text = 'PA:' + str(char.getphysicalattack())
        label.font_size= 30
        label.size: label.texture_size
        label.size_hint= None, None

        label = self.ids['magicalattack']
        label.text = 'MA:' + str(char.getmagicalattack())
        label.font_size = 30
        label.size: label.texture_size
        label.size_hint = None, None

        label = self.ids['defense']
        label.text = 'Def:' + str(char.getdefense())
        label.font_size = 30
        label.size: label.texture_size
        label.size_hint = None, None

        label = self.ids['magicalpoints']
        label.text = 'MP:' + str(char.getmagicalpoints())
        label.font_size = 30
        label.size: label.texture_size
        label.size_hint = None, None

        label = self.ids['health']
        label.text = 'H:' + str(char.gethealth())
        label.font_size = 30
        label.size: label.texture_size
        label.size_hint = None, None

        label = self.ids['strength']
        label.text = 'Str:' + str(char.getstrength())
        label.font_size = 30
        label.size: label.texture_size
        label.size_hint = None, None

        label = self.ids['magic']
        label.text = 'Mag:' + str(char.getmagic())
        label.font_size = 30
        label.size: label.texture_size
        label.size_hint = None, None

        label = self.ids['endurance']
        label.text = 'End:' + str(char.getendurance())
        label.font_size = 30
        label.size: label.texture_size
        label.size_hint = None, None

        label = self.ids['dexterity']
        label.text = 'Dex:' + str(char.getdexterity())
        label.font_size = 30
        label.size: label.texture_size
        label.size_hint = None, None

        label = self.ids['agility']
        label.font_size = 30
        label.size: label.texture_size
        label.size_hint = None, None
        label.text = "Agi: " + str(char.getagility())

        label = self.ids['level']
        label.text = 'Level: 1'
        label.font_size = 48
        label.size: label.texture_size
        label.size_hint = None, None
class emptycharacterpreview(Screen):
    def __init__(self):
        super(emptycharacterpreview, self).__init__()
        button = Button()
        button.bind(on_touch_down = self.onPressed)
        button.size = 250, 650
        button.pos = -125, -325
        button.background_normal = ''
        button.background_down = ''
        button.size_hint = None, None
        with button.canvas:
            Color(1, 0, 0, 1)  # set the colour to red
            button.rect = Rectangle(pos=button.center,
                                  size=(button.width,
                                        button.height))
        image = Image()
        image.source = 'res/Empty.jpg'
        image.allow_stretch = True
        image.keep_ratio = True
        image.size_hint = None, None
        image.size = 250, 650
        button.add_widget(image)
        self.add_widget(button)
    def onPressed(self, instance, touch):
        if self.collide_point(*touch.pos):
            if touch.button == 'left':
                print("left click on empty preview")
                if isinstance(self.parent, CharacterPreview):
                    self.parent.makepreviewscreen("empty")
                # elif isinstance(self.parent, BoxLayout):
                #     screen = filledcharacterpreviewS(self.char)
                #     screen.name = 'selection'
                #     screen.id = 'selection'
                #     self.parent.parent.parent.parent.size = (250, 650)
                #     self.parent.parent.parent.parent.switch_to(screen, direction='left')
class scrollcharacterpreview(Screen):
    def __init__(self):
        super(scrollcharacterpreview, self).__init__()
        pass
class CharacterS(Screen):
    def on_enter(self):
        print("enter!")

    def showCharValues(self, char):
        label = Label(color=(0,0,0,1))
        label.id = 'physicalattack'
        label.text =  'PA:'
        label.font_size= 30
        label.pos= (10, 90)
        label.size: label.texture_size
        label.size_hint= None, None
        self.add_widget(label)
        label = Label(color=(0,0,0,1))
        label.id = 'magicalattack'
        label.text = 'MA:'
        label.font_size = 30
        label.pos = (10, 60)
        label.size: label.texture_size
        label.size_hint = None, None
        self.add_widget(label)
        label = Label(color=(0,0,0,1))
        label.id = 'defense'
        label.text = 'Def:'
        label.font_size = 30
        label.pos = (10, 30)
        label.size: label.texture_size
        label.size_hint = None, None
        self.add_widget(label)
        label = Label(color=(0,0,0,1))
        label.id = 'magicalpoints'
        label.text = 'MP:'
        label.font_size = 30
        label.pos = (10, 0)
        label.size: label.texture_size
        label.size_hint = None, None
        self.add_widget(label)
        label = Label(color=(0,0,0,1))
        label.id = 'health'
        label.text = 'H:'
        label.font_size = 30
        label.pos = (10, -30)
        label.size: label.texture_size
        label.size_hint = None, None
        self.add_widget(label)
        label = Label(color=(0,0,0,1))
        label.id = 'strength'
        label.text = 'Str:'
        label.font_size = 30
        label.size: label.texture_size
        label.pos = (self.parent.width - label.width - 10, 90)
        label.size_hint = None, None
        self.add_widget(label)
        label = Label(color=(0,0,0,1))
        label.id = 'magic'
        label.text = 'Mag:'
        label.font_size = 30
        label.size: label.texture_size
        label.pos = (self.parent.width - label.width - 10, 60)
        label.size_hint = None, None
        self.add_widget(label)
        label = Label(color=(0,0,0,1))
        label.id = 'endurance'
        label.text = 'End:'
        label.font_size = 30
        label.size: label.texture_size
        label.pos = (self.parent.width - label.width - 10, 30)
        label.size_hint = None, None
        self.add_widget(label)
        label = Label(color=(0,0,0,1))
        label.id = 'dexterity'
        label.text = 'Dex:'
        label.font_size = 30
        label.size: label.texture_size
        label.pos = (self.parent.width - label.width - 10, 0)
        label.size_hint = None, None
        self.add_widget(label)
        label = Label(color=(0,0,0,1))
        label.id = 'agility'
        label.text = 'Agi:'
        label.font_size = 30
        label.size: label.texture_size
        label.pos = (self.parent.width - label.width - 10, -30)
        label.size_hint = None, None
        self.add_widget(label)
        self.setCharValues(char)

        label = Label(color=(0, 0, 0, 1))
        label.id = 'level'
        label.text = 'Level: 1'
        label.font_size = 48
        label.size: label.texture_size
        label.pos =(45, self.parent.height-85)
        label.size_hint = None, None
        self.add_widget(label)

    def setCharValues(self, char):
        print("Working!!!")
        global agility
        global dexterity
        global endurance
        global strength
        global magic
        global health
        global magicalpoints
        global name
        global defense
        global pyhsicalattack
        global magicalattack

        print(str(self.children))
        label = self.children[0]
        agility = char.getagility()
        label.text = "Agi: " + str(agility)

        label = self.children[1]
        dexterity = char.getdexterity()
        label.text = "Dex: " + str(dexterity)

        label = self.children[2]
        endurance = char.getendurance()
        label.text = "End: " + str(endurance)

        label = self.children[3]
        magic = char.getmagic()
        label.text = "Mag: " + str(magic)

        label = self.children[4]
        strength = char.getstrength()
        label.text = "Str: " + str(strength)

        label = self.children[5]
        health = char.gethealth()
        label.text = "H: " + str(health)

        label = self.children[6]
        magicalpoints = char.getmagicalopoints()
        label.text = "MP: " + str(magicalpoints)

        label = self.children[7]
        defense = char.getdefense()
        label.text = "Def: " + str(defense)

        label = self.children[8]
        magicalattack = char.getmagicalattack()
        label.text = "MA: " + str(magicalattack)

        label = self.children[9]
        physicalattack = char.getphysicalattack()
        label.text = "PA: " + str(physicalattack)




    # def on_touch_move(self, touch):
    #     if touch.x < self.width / 3:
    #         self.player1.center_y = touch.y
    #     if touch.x > self.width - self.width / 3:
    #         self.player2.center_y = touch.y
class CharacterAttributeScreen(Screen):
    def __init__(self, char):
        super(CharacterAttributeScreen, self).__init__()
        self.char = char
        image = Image(source=char.getfullimage(),pos = (0, 0), size = (App.height, App.height), size_hint=(None, None), allow_stretch=True, keep_ratio=True)
        self.add_widget(image)
        count = 0
        cimage = CustomSlot(source='res/SlotStrength.png', size_hint=(None, None))
        cimage.size = cimage.texture_size
        for x in char.rank:
            print("Rank: " + str(x))
            if x == 1:
                self.add_widget(Image(source="res/star.png",pos=(200 + (count*100), 100), size=(140,140), size_hint=(None, None)))
            elif x == 2:
                self.add_widget(Image(source="res/rankbrk.png", pos=(200 + (count * 100), 100), size=(140, 140), size_hint=(None, None)))
            count += 1

        # Total Stat Window
        totalstatpreview = StatPreview(1, True, char.getphysicalattack(), char.getmagicalattack(), char.getmagicalpoints(), char.gethealth(), char.getdefense(), char.getstrength(), char.getmagic(), char.getagility(), char.getdexterity(), char.getendurance(), size=(450, 700), pos=(1150, App.height-800))
        rankstatpreview = StatPreview(1, False, char.getphysicalattack(), char.getmagicalattack(), char.getmagicalpoints(), char.gethealth(), char.getdefense(), char.getstrength(), char.getmagic(), char.getagility(), char.getdexterity(), char.getendurance(),size=(450, 425), pos=(1150, App.height-450-800))
        self.add_widget(totalstatpreview)
        self.add_widget(rankstatpreview)
class CustomSlot(Image):
    def __init__(self, **kwargs):
        kwargs.setdefault('keep_data', True)
        kwargs.setdefault('size_hint', (None,None))
        super(CustomSlot, self).__init__(**kwargs)
        self.pos_hint = {'center_x': .5, 'center_y': .5}
        self.opacity = 1

    def collide_point(self, x, y):
        # Do not want to upset the read_pixel method, in case of a bound error
        try:
            color = self._coreimage.read_pixel(x - self.x, self.height - (y - self.y))
        except:
            color = 0, 0, 0, 0
        if color[-1] > 0:
            return True
        return False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print("True")
        else:
            print("False")
class Empty(Screen):
    pass

class Enemy(Image):
    health = NumericProperty(100)
    healthmax = NumericProperty(100)
    mp = NumericProperty(10)
    mpmax = NumericProperty(10)
    def __init__(self):
        super(Enemy, self).__init__()
        self.healthmax = 1000
        self.health = 1000
        self.mp = 200
        self.mpmax = 200
class MoveBarObject(FloatLayout):

    def __init__(self, **kwargs):
        super(MoveBarObject, self).__init__(**kwargs)
        self.visible = False
        self.opacity = 0
        self.size = 0,0
        # for x in range(1):
        #     button = self.AtkBtn1
        #     button.size_hint = None, None
        #     button.text = '%s' % self.move1
        #     button.font_size = 40
        #     # button.color = self.color
        #     button.disabled = self.disabled
        #     button.background_color = .1, .1, .1, .2
        #     button.size = 175, 75
        #     button.disabled_color = 0, 0, 0, 0
        #     button.disabled_normal = ''
        #     button.disabled_background_color = 0, 0, 0, 0
        #     self.add_widget(button)
    def callback(self, text, movenum):
        if self.visible:
            # print(text)
            self.hide_widget()
            self.parent.text = text
            self.parent.parent.selectedMove = movenum
            print(self.parent.parent.selectedMove)
            print(self.parent.parent)
        else:
            print("not visible")
    def hide_widget(wid):
        # print(wid)
        if wid.visible:
                wid.size, wid.size_hint, wid.opacity = (0,0), (0,0), 0
                wid.visible = False
        else:
            wid.size, wid.size_hint_y, wid.opacity = (875, 75), 0, 1
            wid.visible = True
class CharPreview(Image):
    health = NumericProperty(100)
    healthmax = NumericProperty(100)
    mp = NumericProperty(10)
    mpmax = NumericProperty(10)

    selectedMove = NumericProperty(0)

    move1 = StringProperty("Base Move")
    move2 = StringProperty("Move 1")
    move3 = StringProperty("Move 2")
    move4 = StringProperty("Move 3")
    special = StringProperty("Special")

    def __init__(self, char):
        super(CharPreview, self).__init__()
        self.char = char
        self.move1 = self.char.getmove(0).name
        self.move2 = self.char.getmove(1)
        self.move3 = self.char.getmove(2)
        self.move4 = self.char.getmove(3)
        self.special = self.char.getmove(4)
        self.healthmax = char.gethealth()
        self.health = char.gethealth()
        self.mp = char.getmagicalpoints()
        self.mpmax = char.getmagicalpoints()

        # self.add_widget(moveBar())

class StatLabel(Label):

    def __init__(self, **kwargs):
        super(StatLabel, self).__init__(**kwargs)
        if self.font_size != 60 and self.font_size != 50:
            self.font_size = 40


class StatPreview(Image):
    def __init__(self, attacktype, totalstats, physicalattack, magicalattack, magicalpoints, health, defense, strength, magic, agility, dexterity, endurance, **kwargs):
        super(StatPreview, self).__init__(**kwargs)
        self.source = "res/TotalSingleAttackWindow.png"
        self.size_hint = None, None
        self.allow_stretch = True
        self.keep_ratio = False
        x = self.x + 10
        y = self.y + self.height * .9
        if totalstats:
            barwidth = 175
            barheight = 50
            self.add_widget(Label(text="Total Stats", color=(.1, .1, .1, 1), font_size=40, pos=(x + 55, y - 10)))
            y -= 35
            self.add_widget(Image(source='res/StatBar.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False, allow_stretch=True))
            self.add_widget(Image(source='res/Health.png', size=(40, 40), pos=(x + 15, y + 5)))
            healthlabel = StatLabel(text='HP')
            healthlabel.x = x + 65
            healthlabel.y = y
            healthlabelnumber = StatLabel(text='%d' % health, color=(0,0,0,1))
            healthlabelnumber.x = x + 190
            healthlabelnumber.y = y
            healthlabeldiff = StatLabel(text='(+600)', color=(.3,.4,.6,1))
            healthlabeldiff.x = x + 310
            healthlabeldiff.y = y
            self.add_widget(healthlabelnumber)
            self.add_widget(healthlabeldiff)
            self.add_widget(healthlabel)

            y -= 55
            self.add_widget(Image(source='res/StatBar.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False, allow_stretch=True))
            self.add_widget(Image(source='res/Mana.png', size=(40, 40), pos=(x + 15, y + 5)))
            magicalpointlabel = StatLabel(text='MP')
            magicalpointlabel.x = x + 65
            magicalpointlabel.y = y
            magicalpointlabelnumber = StatLabel(text='%d' % magicalpoints, color=(0, 0, 0, 1))
            magicalpointlabelnumber.x = x + 190
            magicalpointlabelnumber.y = y
            magicalpointlabeldiff = StatLabel(text='(+0)', color=(.3, .4, .6, 1))
            magicalpointlabeldiff.x = x + 310
            magicalpointlabeldiff.y = y
            self.add_widget(magicalpointlabelnumber)
            self.add_widget(magicalpointlabeldiff)
            self.add_widget(magicalpointlabel)

            y-= 55
            if attacktype == 1:
                self.add_widget(Image(source='res/StatBar.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False, allow_stretch=True))
                self.add_widget(Image(source='res/PhysicalAttack.png', size=(40, 40), pos=(x + 15, y + 5)))
                attacklabel = StatLabel(text='P.Atk')
                attacklabel.x = x + 65
                attacklabel.y = y
                attacklabelnumber = StatLabel(text='%d' % physicalattack, color=(0, 0, 0, 1))
                attacklabelnumber.x = x + 190
                attacklabelnumber.y = y
                attacklabeldiff = StatLabel(text='(+0)', color=(.3, .4, .6, 1))
                attacklabeldiff.x = x + 310
                attacklabeldiff.y = y
                self.add_widget(attacklabelnumber)
                self.add_widget(attacklabeldiff)
                self.add_widget(attacklabel)
            elif attacktype == 2:
                self.add_widget(
                    Image(source='res/StatBar.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False, allow_stretch=True))
                self.add_widget(Image(source='res/MagicalAttack.png', size=(40, 40), pos=(x + 15, y + 5)))
                attacklabel = StatLabel(text='M.Atk')
                attacklabel.x = x + 65
                attacklabel.y = y
                attacklabelnumber = StatLabel(text='%d' % magicalattack, color=(0, 0, 0, 1))
                attacklabelnumber.x = x + 190
                attacklabelnumber.y = y
                attacklabeldiff = StatLabel(text='(+0)', color=(.3, .4, .6, 1))
                attacklabeldiff.x = x + 310
                attacklabeldiff.y = y
                self.add_widget(attacklabelnumber)
                self.add_widget(attacklabeldiff)
                self.add_widget(attacklabel)
            else:
                self.add_widget(Image(source='res/StatBar.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False, allow_stretch=True))
                self.add_widget(Image(source='res/PhysicalAttack.png', size=(40, 40), pos=(x + 15, y + 5)))
                attacklabel = StatLabel(text='P.Atk')
                attacklabel.x = x + 65
                attacklabel.y = y
                attacklabelnumber = StatLabel(text='%d' % physicalattack, color=(0, 0, 0, 1))
                attacklabelnumber.x = x + 190
                attacklabelnumber.y = y
                attacklabeldiff = StatLabel(text='(+0)', color=(.3, .4, .6, 1))
                attacklabeldiff.x = x + 310
                attacklabeldiff.y = y
                self.add_widget(attacklabelnumber)
                self.add_widget(attacklabeldiff)
                self.add_widget(attacklabel)
                y-= 55
                self.add_widget(
                    Image(source='res/StatBar.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False, allow_stretch=True))
                self.add_widget(Image(source='res/magicalAttack.png', size=(40, 40), pos=(x + 15, y + 5)))
                attacklabel2 = StatLabel(text='M.Atk')
                attacklabel2.x = x + 65
                attacklabel2.y = y
                attacklabel2number = StatLabel(text='%d' % magicalattack, color=(0, 0, 0, 1))
                attacklabel2number.x = x + 190
                attacklabel2number.y = y
                attacklabel2diff = StatLabel(text='(+0)', color=(.3, .4, .6, 1))
                attacklabel2diff.x = x + 310
                attacklabel2diff.y = y
                self.add_widget(attacklabel2number)
                self.add_widget(attacklabel2diff)
                self.add_widget(attacklabel2)
            y -= 55
            self.add_widget(Image(source='res/StatBar.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False, allow_stretch=True))
            self.add_widget(Image(source='res/Defense.png', size=(40, 40), pos=(x + 15, y + 5)))
            defenselabel = StatLabel(text='Def')
            defenselabel.x = x + 65
            defenselabel.y = y
            defenselabelnumber = StatLabel(text='%d' % defense, color=(0, 0, 0, 1))
            defenselabelnumber.x = x + 190
            defenselabelnumber.y = y
            defenselabeldiff = StatLabel(text='(+0)', color=(.3, .4, .6, 1))
            defenselabeldiff.x = x + 310
            defenselabeldiff.y = y
            self.add_widget(defenselabelnumber)
            self.add_widget(defenselabeldiff)
            self.add_widget(defenselabel)
            y -= 100
        if not totalstats:
            y -= 60
            self.add_widget(Label(text="Rank Attributes", color=(.1, .1, .1, 1), font_size=40, pos=(x + 90, y + 20)))
        barwidth = 400
        barheight = 80
        y -= 35
        if attacktype == 1:
            self.add_widget(Image(source='res/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False, allow_stretch=True))
            strengthlabel = StatLabel(text='Str.', font_size=60, color=(0,0,0,1), pos=(x+20, y))
            strengthgrade = Image(source=Scale.getScaleAsImagePath(strength, 7), pos=(x + 140, y+ 10), height = 60, keep_ratio=True, allow_stretch=True)
            strengthnumber = StatLabel(text='%d' % health, font_size = 50, color = (0,0,0,1), pos=(x+240,y + 5))
            self.add_widget(strengthgrade)
            self.add_widget(strengthlabel)
            self.add_widget(strengthnumber)
        elif attacktype == 2:
            self.add_widget(Image(source='res/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                                  allow_stretch=True))
            magiclabel = StatLabel(text='Mag.', font_size=60, color=(0,0,0,1), pos=(x+20, y))
            magicgrade = Image(source=Scale.getScaleAsImagePath(magic, 7), pos=(x + 140, y+ 10), height = 60, keep_ratio=True, allow_stretch=True)
            self.add_widget(magicgrade)
            self.add_widget(magiclabel)
        else:
            self.add_widget(Image(source='res/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                                  allow_stretch=True))
            strengthlabel = StatLabel(text='Str.', font_size=60, color=(0,0,0,1), pos=(x+20, y))
            strengthgrade = Image(source=Scale.getScaleAsImagePath(strength, 7), pos=(x + 140, y+ 10), height = 60, keep_ratio=True, allow_stretch=True)
            self.add_widget(strengthgrade)
            self.add_widget(strengthlabel)
            y -= 90
            self.add_widget(Image(source='res/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                                  allow_stretch=True))
            magiclabel = StatLabel(text='Mag.', font_size=60, color=(0,0,0,1), pos=(x+20, y))
            magicgrade = Image(source=Scale.getScaleAsImagePath(magic, 12), pos=(x + 140, y+ 10), height = 60, keep_ratio=True, allow_stretch=True)
            self.add_widget(magicgrade)
            self.add_widget(magiclabel)
        y-=90
        self.add_widget(Image(source='res/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                              allow_stretch=True))
        agilitylabel = StatLabel(text='Agi.', font_size=60, color=(0,0,0,1), pos=(x+20, y))
        agilitygrade = Image(source=Scale.getScaleAsImagePath(agility, 13), pos=(x + 140, y+ 10), height = 60, keep_ratio=True, allow_stretch=True)
        self.add_widget(agilitygrade)
        self.add_widget(agilitylabel)

        y-= 90
        self.add_widget(Image(source='res/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                              allow_stretch=True))
        dexteritylabel = StatLabel(text='Dex.', font_size=60, color=(0,0,0,1), pos=(x+20, y))
        dexteritygrade = Image(source=Scale.getScaleAsImagePath(dexterity, 15), pos=(x + 140, y+ 10), height = 60, keep_ratio=True, allow_stretch=True)
        self.add_widget(dexteritygrade)
        self.add_widget(dexteritylabel)

        y-=90
        self.add_widget(Image(source='res/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                              allow_stretch=True))
        endurancelabel = StatLabel(text='End.', font_size=60, color=(0,0,0,1), pos=(x+20, y))
        endurancegrade = Image(source=Scale.getScaleAsImagePath(endurance, 11), pos=(x + 140, y+ 10), height = 60, keep_ratio=True, allow_stretch=True)
        self.add_widget(endurancegrade)
        self.add_widget(endurancelabel)

class AdventureApp(App):
    title = 'Coatirane Adventures'
    manager = ObjectProperty
    def build(self):

        user32 = ctypes.windll.user32
        width = math.floor(user32.GetSystemMetrics(0) * 2 / 3)
        height = math.floor(user32.GetSystemMetrics(1) * 2 / 3)
        App.width = width
        App.height = height
        Window.size = (width, height)
        Window.left = math.floor((user32.GetSystemMetrics(0) - width)/2)
        Window.top = math.floor((user32.GetSystemMetrics(1) - height)/2)
        Window.borderless = 1
        self.build_chars()
        # Clock.schedule_interval(game.update, 1.0 / 60.0)
        return AdventureGame()

    def build_chars(self):
        print(self.manager.screen)
        print("Loading Characters")
        App.characterArray = []
        App.party1 = []
        App.currentparty = []
        file = open("CharacterDefinitions.txt", "r")
        if file.mode == 'r':
            count = 0
            for x in file:
                if x[0] != '/':
                    values = x[:-1].split(" ", -1)
                    print("Loaded: " + str(values))
                    App.characterArray.append(Character.Character(count, values[0], values[1], int(values[2]), int(values[3]), int(values[4]), int(values[5]), int(values[6]), int(values[7]), int(values[8]), int(values[9]), int(values[10]), int(values[11]), values[12], values[13], values[14], (Attack(values[15] + " " + values[16], int(values[17]), values[18], int(values[19])), values[20], values[21], values[22], "Special Arts")))
                    App.party1.append(count)
                    App.currentparty.append(count)
                    count += 1
            file.close()
        else:
            raise Exception("Failed to open Character Definition file!")
if __name__ == '__main__':
    AdventureApp().run()