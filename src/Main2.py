from kivy.config import Config

Config.set('input', 'mouse', 'mouse, multitouch_on_demand')
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, BooleanProperty
from kivy.clock import Clock
import ctypes
import math
from kivy.core.window import Window
from Entities.Character import Character, Attack, Scale, Move
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.core.audio import SoundLoader, Sound
import random
from kivy.graphics import Color, Rectangle, Mesh
from kivy.properties import NumericProperty, BooleanProperty, ObjectProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager, FadeTransition, Screen, SlideTransition, RiseInTransition
import time
from kivy.graphics.texture import Texture
from itertools import chain


class Root(ScreenManager):

    def __init__(self, *args, **kwargs):
        super(Root, self).__init__(*args, **kwargs)
        self.list = []
        App.root = self

    def goto_next(self, next_screen):
        if isinstance(next_screen, Screen):
            old_screen = self.children[0]
            self.list.append(old_screen)
            self.add_widget(next_screen)
            self.current = next_screen.name
            self.remove_widget(old_screen)
            print("Added: " + next_screen.name)
            print("Saved: " + old_screen.name)
            print("Removed: " + old_screen.name)
        else:
            raise Exception("Goto_next only works with Screen Objects!")

    def goto_next_no_track(self, next_screen):
        if isinstance(next_screen, Screen):
            old_screen = self.children[0]
            self.add_widget(next_screen)
            self.current = next_screen.name
            self.remove_widget(old_screen)
            print("Added: " + next_screen.name)
            print("Removed: " + old_screen.name)
        else:
            raise Exception("Goto_next_no_track only works with Screen Objects!")

    def goto_back(self):
        if self.list:
            old_screen = self.children[0]
            next_screen = self.list.pop()
            self.add_widget(next_screen)
            self.current = next_screen.name
            self.remove_widget(old_screen)
            print("Rollback: " + next_screen.name)
            print("Removed: " + old_screen.name)
            return True
        print("No more screens. Closing App")
        App.get_running_app().stop()
        Window.close()


class NewGameScreen(Screen):

    def __init__(self, **kwargs):
        super(NewGameScreen, self).__init__(**kwargs)
        self.bind(size=self.on_size)
        self.background = Image(source='res/newgamebackground.png', keep_ratio=False, allow_stretch=True,
                                size_hint=(None, None))
        # self.buttonTest = Button(size=(128,128),pos=(600,800), size_hint=(None,None))
        self.newgame = CustomHoverableButton(size=(750, 350), pos=(100, 100),
                                             collide_image='res/buttons/newgame.collision.png',
                                             background_normal='res/buttons/newgame.normal.png',
                                             background_down='res/buttons/newgame.down.png',
                                             background_hover='res/buttons/newgame.hover.png',
                                             background_disabled='res/buttons/newgame.disabled.png')
        self.newgame.bind(on_touch_down=self.on_new_game)
        self.loadgame = CustomHoverableButton(size=(750, 350), pos=(800, 100),
                                              collide_image='res/buttons/loadgame.collision.png',
                                              background_normal='res/buttons/loadgame.normal.png',
                                              background_down='res/buttons/loadgame.down.png',
                                              background_hover='res/buttons/loadgame.hover.png',
                                              background_disabled='res/buttons/loadgame.disabled.png')
        self.title = Image(source='res/Title.png', keep_ratio=True, allow_stretch=True, size_hint=(None, None))
        # self.button = CustomCollisionButton(size=(128, 128), pos=(0, App.height - 128), collide_image='res/back.collision.png',
        #                                     background_normal='res/back.normal.png', background_down='res/back.effect.png',
        #                                     background_hover='res/back.highlighted.png', background_disabled = 'res/back.disabled.png')
        # self.add_widget(self.button)
        # with self.button.canvas.before:
        #     Color = (1,1,1,.3)
        #     Rectangle(size=self.button.size, pos=self.button.pos)
        # self.add_widget(self.buttonTest)
        self.loadgame.disabled = True
        self.add_widget(self.background)
        self.add_widget(self.newgame)
        self.add_widget(self.loadgame)
        self.add_widget(self.title)

    def on_new_game(self, instance, touch):
        if instance.collide_point(*touch.pos):
            App.root.goto_next_no_track(SelectScreen())

    def on_load_game(self, *args):
        pass

    def on_size(self, *args):
        self.background.size = self.width, self.height
        self.newgame.size = self.width / 3, self.height / 3.25
        self.newgame.pos = (self.width / 2) - self.newgame.width - self.width / 12, self.height * .12
        self.loadgame.size = self.width / 3, self.height / 3.25
        self.loadgame.pos = (self.width / 2) + self.width / 12, self.height * .12
        self.title.size = self.width / 1.5, self.height / 2.14
        self.title.pos = self.width * .05, self.height * .43


class HoverBehavior(object):
    """Hover behavior.
    :Events:
        `on_enter`
            Fired when mouse enter the bbox of the widget.
        `on_leave`
            Fired when the mouse exit the widget
    """

    hovered = BooleanProperty(False)
    '''Contains the last relevant point received by the Hoverable. This can
    be used in `on_enter` or `on_leave` in order to know where was dispatched the event.
    '''

    def __init__(self, **kwargs):
        self.register_event_type('on_enter')
        self.register_event_type('on_leave')
        Window.bind(mouse_pos=self.on_mouse_pos)
        super(HoverBehavior, self).__init__(**kwargs)

    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return  # do proceed if I'm not displayed <=> If have no parent
        pos = args[1]
        # Next line to_widget allow to compensate for relative layout
        inside = self.collide_point(*self.to_widget(*pos))
        if self.hovered == inside:
            # We have already done what was needed
            return
        self.hovered = inside
        if inside:
            self.dispatch('on_enter')
        else:
            self.dispatch('on_leave')

    def on_enter(self):
        pass

    def on_leave(self):
        pass


class CustomHoverableButton(Button, HoverBehavior):
    def __init__(self, **kwargs):
        kwargs.setdefault('size', (0, 0))
        kwargs.setdefault('pos', (0, 0))
        kwargs.setdefault('size_hint', (None, None))
        kwargs.setdefault('background_disabled_down', '')
        if kwargs is not None:
            if kwargs.get('size'):
                self.size = kwargs.get('size')
            if kwargs.get('pos'):
                self.pos = kwargs.get('pos')
            if kwargs.get('collide_image'):
                self.collide_image = kwargs.pop('collide_image')
            if kwargs.get('background_normal'):
                self.background_normal = kwargs.get('background_normal')
            if kwargs.get('background_disabled_normal'):
                self.background_disabled_normal = kwargs.get('background_disabled_normal')
            if kwargs.get('background_disabled_down'):
                self.background_disabled_down = kwargs.get('background_disabled_down')
            if kwargs.get('background_down'):
                self.background_down = kwargs.get('background_down')
            if kwargs.get('background_hover'):
                self.background_hover = kwargs.get('background_hover')
        super(CustomHoverableButton, self).__init__()
        self.size_hint = (None, None)
        self._collide_image = Image(source=self.collide_image, keep_data=True)._coreimage
        self.background_normal_temp = self.background_normal

    def collide_point(self, x, y):
        if self.x <= x <= self.right and self.y <= y <= self.top:
            scale = (self._collide_image.width / (self.right - self.x))
            try:
                color = self._collide_image.read_pixel((x - self.x) * scale, (self.height - (y - self.y)) * scale)
            except:
                color = 0, 0, 0, 0
            if color[-1] > 0:
                return True
        return False

    def on_enter(self):
        self.background_normal = self.background_hover

    def on_leave(self):
        self.background_normal = self.background_normal_temp


class SelectScreen(Screen):
    font_size = NumericProperty(150)
    font_size2 = NumericProperty(75)
    title_x = NumericProperty(500)

    def __init__(self, **kwargs):
        super(SelectScreen, self).__init__(**kwargs)
        self.id = 'select_screen'
        self.name = 'select_screen'
        self.newgamebell = CustomHoverableButton(size=(600, 600), pos=(200, 200),
                                                 collide_image='res/buttons/newgame.bell.collide.png',
                                                 background_normal='res/buttons/newgame.bell.normal.png',
                                                 background_down='res/buttons/newgame.bell.down.png',
                                                 background_hover='res/buttons/newgame.bell.hover.png',
                                                 background_disabled='')
        self.newgamebell.bind(on_touch_down=lambda instance, touch: self.chooseCharacter(instance, touch, 'hero_bell'))
        self.newgameais = CustomHoverableButton(size=(600, 600), pos=(200, 200),
                                                collide_image='res/buttons/newgame.ais.collide.png',
                                                background_normal='res/buttons/newgame.ais.normal.png',
                                                background_down='res/buttons/newgame.ais.down.png',
                                                background_hover='res/buttons/newgame.ais.hover.png',
                                                background_disabled='')
        self.newgameais.bind(
            on_touch_down=lambda instance, touch: (self.chooseCharacter(instance, touch, 'badass_ais')))
        self.add_widget(self.newgamebell)
        self.add_widget(self.newgameais)

    def chooseCharacter(self, instance, touch, choice):
        if instance.collide_point(*touch.pos):
            print('Chosen Character: %s, adding to char Array.' % choice)
            self.bind(size=self.on_size)
            for x in App.characterArray:
                # print(x.getid())
                if x.getid() == choice:
                    x.first = True
                    App.obtainedcharsArray.append(x.getindex())
                    App.root.goto_next_no_track(TownScreen())
                    return True

    def on_size(self, *args):
        self.font_size = self.height / 9.6
        self.font_size2 = self.height / 19.2
        self.newgameais.size = self.height / 2.22, self.height / 2.22
        self.newgameais.pos = self.width / 3 - self.newgameais.width / 2, self.height * 2 / 8
        self.newgamebell.size = self.height / 2.22, self.height / 2.22
        self.newgamebell.pos = self.width * 2 / 3 - self.newgameais.width / 2, self.height * 2 / 8
        self.title_x = self.width / 4

        # Name, ID, Health, Defense, Physical Attack, magical Attack, Mana, Strength, Magic, Endurance, Agility, Dexterity, Slide Image, Square Image, Full Image

        # Lena | fanciful_lena
        # Min: H 110 M 0 Str 20 Mag 0 End 14 Agi 15 Dex 16 | MAtk 10 PAtk 20 Defense 14
        # Max: H 3432 M 0 Str 1220 Mag 0 End 414 Agi 512 Dex 467 | MAtk 315 PAtk 1220 Defense 414
        # Physical Type
        # Base: Foe: Lo Physical Attack w/ 5% stun
        # 1) Foes: Mid Physical Attack && Foes: Str -10%
        # 2) Foes: High Physical Attack w/ temp Str Boost
        # 3) Allies: Str +50% && Self Str +75% for 2 turns
        # Special: Ultra Physical Attack with temp Str Boost && Allies +10% to health of damage
        # For Each Rank -> I to S
        # For Each  Rank -> Level 0 -> 50
        # For each Rank, Attribute star w/ unlocks by Gems
        # For Each Rank, you choose an ability


class TownScreen(Screen):
    button_width = NumericProperty(300)
    smallButton_height = NumericProperty(250)
    largeButton_height = NumericProperty(200)

    def __init__(self, **kwargs):
        super(TownScreen, self).__init__(**kwargs)
        self.id = 'town_screen'
        self.name = 'town_screen'
        self.bgImage = Image(source='res/townClip.jpg', allow_stretch=True, keep_ratio=True,
                             size=(App.width, App.height), size_hint=(None, None), pos=(0, 0))
        # self.tavernButton = customButton(source='res/TavernButton.png', on_touch_down=self.onTavern, size=(300, 250),
        #                                  pos=(100, 100))
        self.tavernButton = CustomHoverableButton(size=(300, 250), pos=(100, 100),
                                              collide_image='res/buttons/smallbutton.collision.png',
                                              background_normal='res/buttons/TavernButton.png',
                                              background_down='res/buttons/smallbutton.down.png',
                                              background_hover='res/buttons/smallbutton.hover.png')
        self.tavernButton.bind(on_touch_down=self.onTavern)
        # self.shopButton = customButton(source='res/ShopButton.png', size=(300, 250), pos=(100, 100))
        self.shopButton = CustomHoverableButton(size=(300, 250), pos=(100, 100),
                                                  collide_image='res/buttons/smallbutton.collision.png',
                                                  background_normal='res/buttons/ShopButton.png',
                                                  background_down='res/buttons/smallbutton.down.png',
                                                  background_hover='res/buttons/smallbutton.hover.png')
        # self.craftingButton = customButton(source='res/CraftingButton.png', size=(300, 250), pos=(100, 100))
        self.craftingButton = CustomHoverableButton(size=(300, 250), pos=(100, 100),
                                                collide_image='res/buttons/smallbutton.collision.png',
                                                background_normal='res/buttons/CraftingButton.png',
                                                background_down='res/buttons/smallbutton.down.png',
                                                background_hover='res/buttons/smallbutton.hover.png')
        # self.questButton = customButton(source='res/QuestButton.png', size=(300, 250), pos=(100, 100))
        self.questButton = CustomHoverableButton(size=(300, 250), pos=(100, 100),
                                                collide_image='res/buttons/smallbutton.collision.png',
                                                background_normal='res/buttons/QuestButton.png',
                                                background_down='res/buttons/smallbutton.down.png',
                                                background_hover='res/buttons/smallbutton.hover.png')
        # self.dungeonButton = customButton(source='res/DungeonButton.png', on_touch_down=self.onDungeon, size=(300, 200),
        #                                   pos=(1400, 100))
        self.dungeonButton = CustomHoverableButton(size=(300, 250), pos=(100, 100),
                                                collide_image='res/buttons/largebutton.collision.png',
                                                background_normal='res/buttons/DungeonButton.png',
                                                background_down='res/buttons/largebutton.down.png',
                                                background_hover='res/buttons/largebutton.hover.png')
        self.dungeonButton.bind(on_touch_down=self.onDungeon)
        self.bind(size=self.on_size)

        self.add_widget(self.bgImage)
        self.add_widget(self.tavernButton)
        self.add_widget(self.shopButton)
        self.add_widget(self.craftingButton)
        self.add_widget(self.questButton)
        self.add_widget(self.dungeonButton)
        # self.sound = SoundLoader.load('res/town.mp3')
        # self.sound.loop = True

    def on_enter(self):
        pass
        # if self.sound:
        #     self.sound.play()

    def on_leave(self):
        pass
        # if self.sound:
        #     self.sound.stop()

    def onDungeon(self, instance, touch):
        if instance.collide_point(*touch.pos):
            App.root.goto_next(DungeonMain())

    def onTavern(self, instance, touch):
        if instance.collide_point(*touch.pos):
            App.root.goto_next(TavernMain())

    def on_size(self, *args):
        self.button_width = self.height / 4.6
        self.button_interval = self.width / 25.6
        self.button_height = self.height / 14.1
        self.dungeon_x = self.width / 1.82
        self.smallButton_height = self.height / 5.76
        self.largeButton_height = self.height / 7.2
        self.bgImage.size = self.width, self.height

        self.tavernButton.size = self.button_width, self.smallButton_height
        self.shopButton.size = self.button_width, self.smallButton_height
        self.craftingButton.size = self.button_width, self.smallButton_height
        self.questButton.size = self.button_width, self.smallButton_height
        self.dungeonButton.size = self.button_width, self.largeButton_height

        self.tavernButton.pos = self.button_interval, self.button_height
        self.shopButton.pos = self.button_interval + self.button_width, self.button_height
        self.craftingButton.pos = self.button_interval + self.button_width * 2, self.button_height
        self.questButton.pos = self.button_interval + self.button_width * 3, self.button_height
        self.dungeonButton.pos = self.dungeon_x, self.button_height


class TavernMain(Screen):
    def __init__(self, **kwargs):
        super(TavernMain, self).__init__(**kwargs)
        self.bg = Image(size=(App.width, App.height), pos=(0, 0), allow_stretch=True, keep_ratio=True,
                        source='res/collage.png')
        self.add_widget(self.bg)
        self.title = Label(text="[b]Recruitment[/b]", markup=True, font_size=175, color=(1, 1, 1, 1),
                           pos=(650, App.height - 200), size=(200, 50), size_hint=(None, None))
        self.add_widget(self.title)
        self.recruitButton = customButton(source='res/buttons/recruitButton.png', size=(270, 180),
                                          pos=(App.width / 2 - 270 / 2, 100), on_touch_down=self.onRecruit)
        self.add_widget(self.recruitButton)
        self.lock = Image(size=(App.width, App.height), pos=(0, 0), allow_stretch=True, keep_ratio=True,
                          source='res/locked.png')
        # print("Locking")
        self.add_widget(self.lock)
        self.locked = True
        self.disabled = False
        self.backButton = customButton(id='back', source='res/BackArrow.png', size=(100, 100),
                                       pos=(100, App.height - 200),
                                       on_touch_down=self.onBackPress)
        self.add_widget(self.backButton)

    def on_size(self, *args):
        self.title.font_size = self.height / 7.2
        self.title.pos = self.width / 3, self.height / 1.14
        self.backButton.size = self.height / 14.4, self.height / 14.4
        self.backButton.pos = self.height / 7.2, self.height - self.height / 7.2
        self.recruitButton.size = self.height / 4, self.height / 6
        self.recruitButton.pos = self.width / 2 - self.recruitButton.width / 2, self.height / 10.8

    def onRecruit(self, instance, touch):
        if instance.collide_point(*touch.pos):
            if not self.locked:
                if not self.disabled:

                    # print("Recruit")
                    notobtained = False
                    while not notobtained:
                        index = random.randint(0, len(App.characterArray) - 1)
                        print(str(index))
                        print(str(App.obtainedcharsArray))
                        notobtained = index not in App.obtainedcharsArray
                    print(str(App.characterArray[index].getname()))
                    preview = RecruitPreview(App.characterArray[index])
                    App.root.transition = RiseInTransition(duration=.3)
                    App.root.goto_next(preview)

    def check_unlock(self):
        # print(str(App.tavern_unlocked))
        self.locked = App.tavern_unlocked
        if not self.locked:
            # print("unlocking")
            self.remove_widget(self.lock)

    def onBackPress(self, instance, touch):
        if instance.collide_point(*touch.pos):
            App.root.transition = SlideTransition()
            App.root.goto_back()


class RecruitPreview(Screen):
    def __init__(self, char, **kwargs):
        super(RecruitPreview, self).__init__(**kwargs, name='RecruitPreview_%s' % char.getid(), id='RecruitPreview')
        # self.size = (2560*4/5, 1440*2/3)

        # with self.canvas.before:
        #     Color(0,0,0,.7)
        #     Rectangle(size=(2560*4/5, 1440*2/3), pos=(App.width/10, App.height/6))
        self.image = Image(source=char.getfullimage(), size=(App.height * 2 / 3, App.height * 2 / 3), pos=(0, 0),
                           allow_stretch=True, keep_ratio=True)
        self.add_widget(self.image)
        self.title = Label(text="[b]" + char.getname() + "[/b]", markup=True, color=(1, 1, 1, 1), size=(200, 50),
                           font_size=80, pos=((App.width - (App.height * 2 / 3)) / 2, App.height - 100))
        self.add_widget(self.title)
        self.rollAgainButton = customButton(source='res/buttons/RecruitButtonRollAgain.png', size=(270, 180),
                                            pos=(200 - 135, App.height / 2), on_touch_down=self.onRollAgain)
        self.confirmButton = customButton(source='res/buttons/RecruitButtonConfirm.png', size=(270, 180),
                                          pos=(App.width - 200 - 135, App.height / 2), on_touch_down=self.onConfirm)
        self.cancelButton = customButton(source='res/buttons/RecruitButtonCancel.png', size=(270, 180),
                                         pos=(App.width - 200 - 135, App.height / 2 - 200), on_touch_down=self.onCancel)
        self.add_widget(self.rollAgainButton)
        self.add_widget(self.confirmButton)
        self.add_widget(self.cancelButton)
        self.char = char

    def on_size(self, *args):
        self.rollAgainButton.size = self.height / 4, self.height / 6
        self.rollAgainButton.pos = self.height / 5.4 - self.rollAgainButton.width / 2, self.height / 2 - self.rollAgainButton.height / 2
        self.confirmButton.size = self.height / 4, self.height / 6
        self.confirmButton.pos = self.width - self.height / 5.4 - self.confirmButton.width / 2, self.height / 2
        self.cancelButton.size = self.height / 4, self.height / 6
        self.cancelButton.pos = self.width - self.height / 5.4 - self.cancelButton.width / 2, self.height / 2 - self.rollAgainButton.height

    def onRollAgain(self, instance, touch):
        if instance.collide_point(*touch.pos):
            notobtained = False
            while not notobtained:
                index = random.randint(0, len(App.characterArray) - 1)
                print(str(index))
                print(str(App.obtainedcharsArray))
                notobtained = index not in App.obtainedcharsArray
            print(str(App.characterArray[index].getname()))
            preview = RecruitPreview(App.characterArray[index])
            App.root.transition = RiseInTransition(duration=.3)
            App.root.goto_next_no_track(preview)

    def onConfirm(self, instance, touch):
        if instance.collide_point(*touch.pos):
            App.obtainedcharsArray.append(self.char.getindex())
            App.root.goto_back()

    def onCancel(self, instance, touch):
        if instance.collide_point(*touch.pos):
            App.root.goto_back('tavern_main')


class DungeonMain(Screen):
    level = NumericProperty(1)
    score = NumericProperty(1)
    boss = StringProperty('')
    first = BooleanProperty(True)
    wasInCharScreen = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(DungeonMain, self).__init__(**kwargs)
        self.backButton = customButton(id='back', source='res/BackArrow.png', size=(100, 100),
                                       pos=(100, App.height - 200),
                                       on_touch_down=self.onBackPress)
        self.add_widget(self.backButton)
        self.delveButton = customButton(source='res/delveButton.png', on_touch_down=self.delve, pos=(250, 800),
                                        size=(450, 175), size_hint=(None, None), id='delve')
        self.delveButtonText = Label(text="Delve", markup=True, size=(450, 175), pos=(250, 800), color=(0, 0, 0, 1),
                                     size_hint=(None, None), font_size=90, id='delve_text')
        self.delveButton.add_widget(self.delveButtonText)
        self.ascendButton = customButton(source='res/ascendButton.png', on_touch_down=self.ascend, pos=(1000, 800),
                                         size=(450, 175), size_hint=(None, None), id='ascend')
        self.ascendButtonText = Label(text="Ascend", markup=True, size=(450, 175), pos=(1000, 800), color=(0, 0, 0, 1),
                                      size_hint=(None, None), font_size=90, id='ascend_text')
        self.ascendButton.add_widget(self.ascendButtonText)
        self.add_widget(self.delveButton)
        self.add_widget(self.ascendButton)
        #         Button:

    #         id: delve
    #         text: 'Delve'
    #         size_hint: None, None
    #         background_normal: ''
    #         background_color: 0, .55, .55, 1
    #         color: 0, 0, 0, 1
    #         font_size: 90
    #         size: (450, 175)
    #         on_release:
    #         print("Delve")
    #         root.delve()
    #
    #     pos: (self.parent.width - self.width - 100 - 25, (self.parent.height - self.height) / 2 - self.height - 75)
    #     canvas.before:
    #     Color:
    #     rgba: 0, .55, .55, 1
    #
    #
    # Mesh:
    # mode: 'triangle_fan'
    # vertices: [self.pos[0] + 450, self.pos[1] + 175 / 2, 0, 0, self.pos[0] + 475, self.pos[1] + 0, 0, 0, self.pos[0] - 25,
    #            self.pos[1] + 0, 0, 0, self.pos[0], self.pos[1] + 175 / 2, 0, 0, self.pos[0] - 25, self.pos[1] + 175, 0, 0,
    #            self.pos[0] + 475, self.pos[1] + 175, 0, 0]
    # indices: [0, 1, 2, 3, 4, 5]
    #
    # Button:
    # id: ascend
    # size_hint: None, None
    # background_normal: ''
    # background_disabled_normal: self.background_normal
    # on_release:
    # print("Ascend")
    # root.ascend()
    # background_color: 0.45, 0, .55, 1
    # size: (450, 175)
    # pos: (self.parent.width - self.width - 100 - 25, (self.parent.height - self.height) / 2)
    # canvas.before:
    # Color:
    # rgba: 0.45, 0, .55, 1
    # Mesh:
    # mode: 'triangle_fan'
    # vertices: [self.pos[0] + 450, self.pos[1] + 175 / 2, 0, 0, self.pos[0] + 475, self.pos[1] + 0, 0, 0, self.pos[0] - 25,
    #            self.pos[1] + 0, 0, 0, self.pos[0], self.pos[1] + 175 / 2, 0, 0, self.pos[0] - 25, self.pos[1] + 175, 0, 0,
    #            self.pos[0] + 475, self.pos[1] + 175, 0, 0]
    # indices: [0, 1, 2, 3, 4, 5]
    # Label:
    # id: ascend_text
    # text: 'Ascend'
    # color: 0, 0, 0, 1
    # font_size: 90
    # disabled_color: 0, 0, 0, 1
    # size_hint: None, None
    # size: self.texture_size
    # pos: self.parent.pos[0] + 75, self.parent.pos[1] + 35
    # markup: True
    def updateCurrent(self):
        if self.first:
            self.first = False
            self.showcurrentparty()
        else:
            if not self.wasInCharScreen:
                for x in App.slots:
                    if x.inPreview:
                        x.collapse()
            else:
                self.wasInCharScreen = False

    def update_buttons(self):
        if (self.level < 2):
            # print("enabling back button")
            self.backButton.disabled = False
            self.backButton.opacity = 1
            # print('disabling ascend')
            self.ascendButton.disabled = True
            self.ascendButtonText.text = '[s]Ascend[/s]'
        else:
            # print('disabling back button')
            self.backButton.disabled = True
            self.backButton.opacity = 0
            # print('enabling ascend')
            self.ascendButtonText.text = 'Ascend'
            self.ascendButton.disabled = False

    def onBackPress(self, instance, touch):
        if self.backButton.collide_point(*touch.pos):
            if not self.backButton.disabled:
                App.root.goto_back()

    def showcurrentparty(self):
        party = []
        for x in App.currentparty:
            if not x == None:
                party.append(App.characterArray[x])
            else:
                party.append(None)
        for x in range(len(party)):
            if party[x] == None:
                slot = CharacterPreview(id=('slot%d' % x), transition=SlideTransition(duration=.25))
                slot.isDisabled = False
                slot.pos = 2560 - (300 * x + 950), 100
                slot.number = x
                App.slots.append(slot)
                slot2 = emptycharacterpreview(slot, name='empty')
                slot.goto_next(slot2, 'right')
                self.add_widget(slot)
            else:
                # print("Slot %d: %s" % (x, party[x].getname()))
                slot = CharacterPreview(id=('slot%d' % x), transition=SlideTransition(duration=.25))
                slot.isDisabled = False
                slot.pos = 2560 - (300 * x + 950), 100
                slot2 = filledcharacterpreviewS(slot, party[x], size=(250, 650))
                slot.number = x
                slot.char = party[x]
                App.slots.append(slot)
                slot.goto_next(slot2, 'right')
                self.add_widget(slot)

        self.calculatepartyscore(App.currentparty)

    def delve(self, instance, touch):
        if instance.collide_point(*touch.pos):
            # print("Delve")
            delve = False
            for x in App.currentparty:
                if not x == None:
                    delve = True
            if delve:
                print("Delving into the dungeon")
                # print(str(App.currentparty))
                self.floor = DungeonFloor(App.root, self.level, True, self)
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


class DungeonFloor:
    def __init__(self, screenManager, floorNum, direction, dungeonScreen):
        self.floor = App.floors[floorNum - 1]
        self.dungeonScreen = dungeonScreen
        self.screenManager = screenManager
        self.screenManager.transition = FadeTransition(duration=.4)
        self.encounterNumber = self.floor.generateEncounterNumber()
        self.runNumber = 1
        self.direction = direction
        print("Generated a floor run instance")
        print("\tWill run for %d encounters." % self.encounterNumber)

    def run(self):
        # print("DungeonFloor Run")
        if (self.runNumber <= self.encounterNumber):
            screen = DungeonBattle(self.runNumber == self.encounterNumber, self.runNumber, self.floor, self,
                                   name='battleScreen%d' % self.runNumber)
            if self.runNumber > 0:
                self.screenManager.goto_next_and_remove(screen)
            else:
                self.screenManager.goto_next(screen)
            screen.run()
            self.runNumber += 1
        else:
            if self.direction:
                num = self.floor.floornum + 1
            else:
                num = self.floor.floornum - 1
            self.screenManager.current = 'dungeon_main'
            self.dungeonScreen.level = num
            self.dungeonScreen.update_buttons()
            print("return to delve screen. Floor: " + str(num))


class DungeonBattle(Screen):
    level = NumericProperty(1)
    boss = BooleanProperty(False)
    level_label = ObjectProperty(None)
    encounterLabel = ObjectProperty(None)
    turn_label = ObjectProperty(None)
    currentTurn = NumericProperty(1)

    def __init__(self, boss, encounternum, floor, floorManager, **kwargs):
        super(DungeonBattle, self).__init__(**kwargs)
        self.chars = []
        self.floor = floor
        self.floorManager = floorManager
        self.boss = boss
        self.level = self.floor.floornum
        if (self.boss):
            self.level_label.text = 'Level %d BOSS' % self.level
            self.encounter_label.text = ''
        else:
            self.level_label.text = 'Level %d' % self.level
            self.encounter_label.text = 'Encounter %d' % encounternum
        if self.boss:
            self.enemies = self.floor.generateBoss()
        else:
            self.enemies = self.floor.generateEnemies()
        # self.enemyLocations = ((1500, 800), (1500, 1000), (1500, 600), (1700, 700), (1700, 900), (1700, 1100), (1700, 500), (1500, 1200), (1500, 400), (1900, 800), (1900, 1000), (1900, 600))
        # self.enemyAmounts = (3, 3, 4, 5, 6)

    def run(self):
        anim = Animation(opacity=0, duration=2.5)
        anim.start(self.level_label)
        anim = Animation(opacity=0, duration=3.5)
        anim.start(self.encounter_label)
        Clock.schedule_once(lambda dt: self.make_gui(), 4)

    def on_currentTurn(self, *args):
        self.turn_label.text = 'Turn: %d' % self.currentTurn
        self.textbox.text = self.textbox.text + "\nIt is now turn %d!" % self.currentTurn

    def make_gui(self):
        currentparty = []
        # print(str("Showing GUI"))
        self.turn_label.text = 'Turn: %d' % self.currentTurn
        self.attackButton = customButton(size=(270, 180), source='res/AttackButton.png', pos=(2000, 100),
                                         size_hint=(None, None), on_touch_down=self.attack)
        self.add_widget(self.attackButton)
        self.text = ScrollView(size=(2160, 890), pos=(200, 370), size_hint=(None, None), do_scroll_x=False)
        self.textbox = TextInput(text="You have delved into the dungeon!", size=(2160, 890), size_hint=(None, None),
                                 pos=(200, 370), multiline=True, readonly=True)
        self.text.add_widget(self.textbox)
        self.add_widget(self.text)
        count = 0
        for x in range(len(App.currentparty)):
            if not App.currentparty[x] == None:
                char = App.characterArray[App.currentparty[x]]
                self.textbox.text = self.textbox.text + "\n" + char.getdisplayname() + " has entered the dungeon!"
                preview = CharPreview(char, (250 * count + 200, 50))
                self.chars.append(preview)
                preview.id = 'charid%d' % x
                preview.source = char.getpreviewimage()
                count += 1
                self.add_widget(preview)

        if self.boss:
            self.textbox.text = self.textbox.text + "\nBOSS Encountered!"
        else:
            self.textbox.text = self.textbox.text + "\nEnemies Encountered!"
        for x in self.enemies:
            self.textbox.text = self.textbox.text + "\nA " + x.name + " appears! " + str(x.health) + " health."

        # for x in range(len(currentparty)):
        #     # print(currentparty[x].getname() + shownparty[x].getname())
        #     preview = CharPreview(currentparty[x])
        #     sprite = Image()
        #     sprite.id = 'sprite%d' % x
        #     sprite.source = currentparty[x].getsprite()
        #     sprite.center = 450, 600 + (200*x)
        #     sprite.size = 200, 200
        #     sprite.keep_ratio = True
        #     sprite.allow_stretch = True
        #     sprite.size_hint = None, None
        #     preview.id = 'charid%d' % x
        #     preview.source = currentparty[x].getpreviewimage()
        #     preview.pos = (225 * x + 200, 50)
        #
        #     self.main_layout.add_widget(sprite)
        #     self.screen.add_widget(preview)
        # numofenemys = random.randint(0, self.enemyAmounts[0]-1) + 1 #generate enemys
        # for x in range(numofenemys):
        #     enemy = Enemy()
        #     enemy.health = 100
        #     enemy.id = 'enemy%d' % x
        #     enemy.source = 'res/wolf.gif'
        #     enemy.size = 200, 200
        #     enemy.size_hint = None, None
        #     enemy.center = self.enemyLocations[x]
        #     self.enemy_layout.add_widget(enemy)
        # bar = MoveBarObject()
        # self.main_layout.add_widget(bar)

    def moveBarPressed(self, char):
        pass

    def attack(self, instance, touch):
        if instance.collide_point(*touch.pos):
            if not instance.disabled:
                objects = []
                speeds = []
                attackOrder = []
                for x in self.chars:
                    speeds.append(x.char.generateSpeed())
                    objects.append(x)
                for x in self.enemies:
                    speeds.append(x.generateSpeed())
                    objects.append(x)
                for x in range(len(speeds)):
                    y = speeds.index(min(speeds))
                    attackOrder.append(objects.pop(y))
                    speeds.pop(y)

                for x in attackOrder:
                    if isinstance(x, Enemy):
                        move = x.generateMove()
                        damage = move.generateDamage(x.str, x.mag)
                        nextUndead = self.next_undead(self.chars)
                        if move.getname() == "EnmyAttack":
                            self.textbox.text = self.textbox.text + "\n " + x.name + " attacks " + nextUndead.char.getname() + "!"
                        else:
                            self.textbox.text = self.textbox.text + "\n " + x.name + " attacks " + nextUndead.char.getname() + " with " + move.getname() + "!"
                        damage = nextUndead.processDamage(damage, x.agi)
                        if damage > 0:
                            self.textbox.text = self.textbox.text + " " + x.name + " deals " + str(
                                damage) + " damage to " + nextUndead.char.getname() + "!"
                            if nextUndead.health > 0:
                                self.textbox.text = self.textbox.text + " " + nextUndead.char.getname() + " took " + str(
                                    damage) + " damage. Health is now: " + str(nextUndead.health)
                            else:
                                self.textbox.text = self.textbox.text + " " + nextUndead.char.getname() + " is now dead."
                        # finish enemy attack against a single char, if multi move than attack all. Add a attack targeting type to move class
                        # Add player addack all enemies targeting. Add countering. Add guarding as the endurance block. Add Critical hits. Add penetration as agi boost
                        # Move bar, mp from attacks, drop items. look at danmachi wiki
                        # Add Unguard type to moves. Fix ascend. Add more floors. Add character death.
                    else:
                        # print(str(x.ids.move_box.text))
                        move = x.char.getmove(x.selectedMove)
                        self.textbox.text = self.textbox.text + "\n" + x.char.getdisplayname() + " uses " + move.getname() + "!"
                        damage = move.generateDamage(x.char.totalPhysicalAttack, x.char.totalMagicalAttack)
                        if len(self.enemies) > 0:
                            damage = self.enemies[0].processDamage(damage, x.char.totalAgility)
                            if damage > 0:
                                self.textbox.text = self.textbox.text + " " + x.char.getdisplayname() + " deals " + str(
                                    damage) + " damage to " + self.enemies[0].name + "."
                                if self.enemies[0].health > 0:
                                    self.textbox.text = self.textbox.text + " " + self.enemies[0].name + " took " + str(
                                        damage) + " damage. Health is now: " + str(self.enemies[0].health)
                                else:
                                    self.textbox.text = self.textbox.text + " The " + self.enemies[
                                        0].name + " is now dead."
                                    self.enemies.remove(self.enemies[0])
                            else:
                                self.textbox.text = self.textbox.text + " " + x.char.getdisplayname() + " deals no damage to " + \
                                                    self.enemies[0].name + "."
                if len(self.enemies) == 0:
                    self.textbox.text = self.textbox.text + "\n" + "This encounter has been won!"
                    self.attackButton.disabled = True
                    self.winBackground = Image(source='res/SuccessBackground.png', size_hint=(None, None), pos=(0, 0),
                                               size=(2560, 1440), opacity=0)
                    self.winLabel = Label(text='Success!', size_hint=(None, None), pos=(1280, 720), font_size=120,
                                          color=(.2, 0, .65, 1))
                    self.add_widget(self.winBackground)
                    self.winBackground.add_widget(self.winLabel)
                    anim = Animation(opacity=1, duration=3.5)
                    anim.start(self.winBackground)
                    anim = Animation(opacity=1, duration=2.5)
                    anim.start(self.winLabel)
                    Clock.schedule_once(lambda dt: self.floorManager.run(), 4)
                    # print(str(damage))
                    # print()

                # print all moves
                # for fights lasting more than 15 turns, incur a 10% speed penalty and a 5% attack penalty
                # for fights lasting more than 20, incur an addl 10% speed penalty and a 10% attack penalty
                # for fights lasting more than 25 turns incur an addl 10% speed penalty and a 10% attack penalty

                self.currentTurn += 1
                # print("Turn %d" % self.currentTurn)
                # self.textbox.text = self.textbox.text + "It is now turn %d!" % self.currentTurn
            # print("Turn: " + str(self.currentTurn))
            # numofchars = 4
            # maxfoes = len(self.enemy_layout.children)
            # if (maxfoes > 0):
            #     for y in range(maxfoes):
            #         print("Enemy #%d" % y)
            #         print("\tHealth: " + str(self.enemy_layout.children[maxfoes - 1 - y].health))
            #     for x in range(numofchars):
            #         maxfoes = len(self.enemy_layout.children)
            #         if maxfoes > 0:
            #             attack = self.children[numofchars - 1 - x].char.getmove(self.children[numofchars - 1 - x].selectedMove)
            #             foenum = -1
            #             if attack.ttype == 0:
            #                 foenum = attack.findfoe(maxfoes-1)
            #             print("DEBUG: " + str(foenum) + " " + str(maxfoes))
            #             print("\u001B[32m" + self.children[numofchars-1-x].char.getname() + " uses " + attack.name)
            #             print("\tAttack Targeting Type: " + str(attack.ttypeS))
            #             print("\tAttack Type: " + attack.type)
            #             damage = attack.generateDamage(self.children[numofchars - 1 - x].char.getattack(attack.type))
            #             print("\tAttack Damage: " + str(damage) + "\u001B[29m")
            #             if foenum == -1:
            #                 pass
            #             else:
            #                 health = self.enemy_layout.children[maxfoes - 1 - foenum].health
            #                 self.enemy_layout.children[maxfoes - 1 - foenum].health = health - damage
            #                 health = self.enemy_layout.children[maxfoes - 1 - foenum].health
            #                 if (health < 0):
            #                     print("\u001B[31mEnemy #" + str(foenum) + " defeated! Removed from children list.\u001B[29m")
            #                     self.enemy_layout.remove_widget(self.enemy_layout.children[maxfoes - 1 - foenum])
            #                 print("\u001B[33mEnemy #" + str(foenum) + " takes " + str(damage) + " damage. Health is now " + str(health) + "\u001B[29m")
            #         else:
            #             print("You have won!")
            #             break

    @staticmethod
    def next_undead(chars):
        return all(chars.health > 0)


class CharacterPreview(ScreenManager):
    number = NumericProperty(0)

    def __init__(self, **kwargs):
        super(CharacterPreview, self).__init__(**kwargs)
        self.list = []
        self.char = None
        self.inPreview = False

    def goto_next(self, next_screen, direction):
        if isinstance(next_screen, Screen):
            # print("Adding a screen")
            self.add_widget(next_screen)
            self.list.append(next_screen.name)
            self.transition.direction = direction
            self.current = next_screen.name
            return True
        self.list.append(self.current)
        self.transition.direction = direction
        self.current = next_screen
        return True

    def goto_next_and_remove(self, next_screen, direction):
        if isinstance(next_screen, Screen):
            if len(self.list) > 0:
                self.list.pop()
            self.list.append(next_screen.name)
            self.switch_to(next_screen, direction=direction)
        else:
            if len(self.list) > 0:
                self.list.pop()
            self.list.append(next_screen)
            self.switch_to(self.ids[next_screen], direction=direction)

    def goto_back(self):
        if self.list:
            last_screen = self.current
            self.current = self.list.pop()
            # self.remove_widget(self.ids[last_screen])
            return True
        return False

    def setCharScreen(self, character):
        for x in App.slots:
            if isinstance(x.char, Character):
                print(str(x.number) + " " + x.char.getname())
            else:
                print(str(x.number) + " empty")
            if not x == self:
                x.isDisabled = False
        self.inPreview = False
        if not self.char == character:
            print("character is not current")
            for x in App.slots:
                if x.char == character:
                    x.setEmpty()
            if isinstance(self.char, Character):
                App.currentparty[self.number] = None
            App.currentparty[self.number] = character.getindex()
            self.char = character
            self.parent.calculatepartyscore(App.currentparty)
        else:
            print("character is current")
        screen = filledcharacterpreviewS(self, character, name=('preview%s' % character.getname()), id='preview')

        self.size = 250, 650
        self.goto_next_and_remove(screen, 'right')
        # for x in App.slots:
        #     if isinstance(x.char, Character):
        #         print("Slot %d,%s" % (x.number, x.char.getname()), end=" ")
        #     else:
        #         print("Slot %d,%s" % (x.number, "Empty"), end=" ")
        #     print("")

    def setEmpty(self, *args):
        for x in App.slots:
            if not x == self:
                x.isDisabled = False
        self.inPreview = False
        screen = emptycharacterpreview(self, size=(250, 650), pos=(0, 0))
        if isinstance(self.char, Character):
            App.currentparty[self.number] = None
            self.parent.calculatepartyscore(App.currentparty)
            self.char = None
        self.size = 250, 650
        self.goto_next_and_remove(screen, 'right')
        # for x in App.slots:
        #     if isinstance(x.char, Character):
        #         print("Slot %d,%s" % (x.number, x.char.getname()), end=" ")
        #     else:
        #         print("Slot %d,%s" % (x.number, "Empty"), end=" ")
        #     print("")

    def setPreview(self, character):
        for x in App.slots:
            if not x == self:
                x.isDisabled = True
                if x.inPreview:
                    x.collapse()
        self.inPreview = True
        screen = scrollcharacterpreview(name='selection', id='selection')
        avaliableparty = []
        displayedparty = []
        for x in App.obtainedcharsArray:
            avaliableparty.append(App.characterArray[x])
        for x in App.currentparty:
            if not x == None:
                displayedparty.append(App.characterArray[x])
        if (len(avaliableparty) + 1 < 4):
            size = len(avaliableparty) + 1
        else:
            size = 4
        if isinstance(self.char, Character):
            removepreview = removeSlot(self, self.char, "Remove", size=(250, 650), pos=(0, 0))
        else:
            removepreview = removeSlot(self, self.char, "Cancel", size=(250, 650), pos=(0, 0))
        screen.ids.charPane.add_widget(removepreview)
        for x in range(len(avaliableparty) + 1):
            if not x == 0:
                preview = filledcharacterPreview(self, avaliableparty[x - 1], pos=(250 * x, 0), size=(250, 650))
                preview.preview = True
                if avaliableparty[x - 1].getindex() in App.currentparty:
                    if avaliableparty[x - 1] == self.char:
                        label = Label(text='Current', color=(1, 1, 1, 1), pos=(250 * x, 0), font_size=48,
                                      size=(250, 650))
                        with preview.canvas:
                            Color(.1, .1, .1, .15)
                            Rect = Rectangle(size=(250, 650), pos=(250 * x, 0))
                        preview.add_widget(label)
                    else:
                        label = Label(text='In Party', color=(1, 1, 1, 1), pos=(250 * x, 0), font_size=48,
                                      size=(250, 650))
                        with preview.canvas:
                            Color(0, 0, 0, .35)
                            Rect = Rectangle(size=(250, 650), pos=(250 * x, 0))
                        # preview.otherParty =
                        preview.add_widget(label)
                screen.ids.charPane.add_widget(preview)
        self.goto_next_and_remove(screen, 'right')
        self.sizePass = size
        screen.size = 250 * size, 650
        screen.ids.charPane.size = 250 * (len(avaliableparty) + 1), 650
        Clock.schedule_once(self.extend, .28)

    def extend(self, *args):
        self.size = 250 * self.sizePass, 650

    def collapse(self):
        self.inPreview = False
        if isinstance(self.char, Character):
            screen = filledcharacterpreviewS(self, self.char)
            self.size = 250, 650
            self.goto_next_and_remove(screen, 'left')
        else:
            self.setEmpty()


class filledcharacterpreviewS(Screen):

    def __init__(self, managerPass, char, **kwargs):
        super(filledcharacterpreviewS, self).__init__(**kwargs)
        self.managerObject = managerPass
        self.add_widget(filledcharacterPreview(self.managerObject, char, size=(250, 650), pos=(0, 0)))


class filledcharacterPreview(Button):
    char = ObjectProperty()
    xPos = ObjectProperty(0)
    yPos = ObjectProperty(0)
    cWidth = ObjectProperty(250)
    cHeight = ObjectProperty(650)

    def __init__(self, managerPass, char, **kwargs):
        super(filledcharacterPreview, self).__init__(**kwargs)
        self.managerObject = managerPass
        self.xPos = self.x
        self.yPos = self.y
        self.cWidth = self.width
        self.cHeight = self.height
        self.preview = False
        self.char = char
        self.id = char.getname()
        self.ids.image.source = self.char.getimage()
        self.ids.image.pos = self.pos
        self.ids.image.size = self.size
        self.showCharValues(char)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if not self.preview:
                if touch.is_touch:
                    if touch.button == 'left':
                        if not touch.is_double_tap:
                            Clock.schedule_once(self.managerObject.setEmpty, .4)
                else:
                    if not touch.is_double_tap:
                        Clock.schedule_once(self.managerObject.setEmpty, .4)

    def updateStars(self, char):
        # print("updating preview stars")
        count = 0
        for x in char.ranks:
            # print(str(self.stars[count].opacity))
            if x.unlocked:
                if not x.broken:
                    self.stars[count].source = 'res/star.png'
                    self.stars[count].opacity = 1
                else:
                    self.stars[count].source = 'res/rankbrk.png'
                    self.stars[count].opacity = 1
            count += 1

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            if touch.button == 'right':
                if not self.char.hasAttributeScreen:
                    self.char.hasAttributeScreen = True
                    screen = CharacterAttributeScreen(self.char, self,
                                                      name='character_attribute_screen_%s' % self.char.getdisplayname(),
                                                      size=(2560, 1440), pos=(0, 0))
                    App.root.add_widget(screen)
                    App.root.goto_next(screen.name)
                else:
                    App.root.goto_next('character_attribute_screen_%s' % self.char.getdisplayname())
                self.managerObject.parent.wasInCharScreen = True

            else:
                if touch.is_double_tap:
                    pass
                else:
                    if not self.managerObject.isDisabled:
                        if self.preview:
                            Clock.unschedule(self.managerObject.setEmpty)
                            self.managerObject.setCharScreen(self.char)
                        else:
                            Clock.unschedule(self.managerObject.setEmpty)
                            self.managerObject.setPreview(self.char)

    def showCharValues(self, char):
        self.physatklabel = self.ids.physicalattack
        self.physatklabel.text = 'PA:' + str(char.totalPhysicalAttack)

        self.magatklabel = self.ids.magicalattack
        self.magatklabel.text = 'MA:' + str(char.totalMagicalAttack)

        self.deflabel = self.ids.defense
        self.deflabel.text = 'Def:' + str(char.totalDefense)

        self.mplabel = self.ids.magicalpoints
        self.mplabel.text = 'MP:' + str(char.totalMP)

        self.healthlabel = self.ids.health
        self.healthlabel.text = 'H:' + str(char.totalHealth)

        self.strengthlabel = self.ids.strength
        self.strengthlabel.text = 'Str:' + str(char.totalStrength)

        self.magiclabel = self.ids.magic
        self.magiclabel.text = 'Mag:' + str(char.totalMagic)

        self.endlabel = self.ids.endurance
        self.endlabel.text = 'End:' + str(char.totalEndurance)

        self.dexlabel = self.ids.dexterity
        self.dexlabel.text = 'Dex:' + str(char.totalDexterity)

        self.agilabel = self.ids.agility
        self.agilabel.text = "Agi: " + str(char.totalAgility)

        count = 0
        self.stars = []
        for x in char.ranks:
            if x.unlocked:
                if not x.broken:
                    self.stars.append(Image(source="res/star.png", pos=(self.x + 20 * count + 5, 590), size=(60, 60),
                                            size_hint=(None, None), opacity=1))
                else:
                    self.stars.append(Image(source="res/rankbrk.png", pos=(self.x + 20 * count + 5, 590), size=(60, 60),
                                            size_hint=(None, None), opacity=1))
                self.add_widget(self.stars[count])
            else:
                self.stars.append(Image(source='res/star.png', pos=(self.x + 20 * count + 5, 590), size=(60, 60),
                                        size_hint=(None, None), opacity=0))
                self.add_widget(self.stars[count])
            count += 1

    def updateCharLabels(self, char):
        self.physatklabel = self.ids.physicalattack
        self.physatklabel.text = 'PA:' + str(char.totalPhysicalAttack)

        self.magatklabel = self.ids.magicalattack
        self.magatklabel.text = 'MA:' + str(char.totalMagicalAttack)

        self.deflabel = self.ids.defense
        self.deflabel.text = 'Def:' + str(char.totalDefense)

        self.mplabel = self.ids.magicalpoints
        self.mplabel.text = 'MP:' + str(char.totalMP)

        self.healthlabel = self.ids.health
        self.healthlabel.text = 'H:' + str(char.totalHealth)

        self.strengthlabel = self.ids.strength
        self.strengthlabel.text = 'Str:' + str(char.totalStrength)

        self.magiclabel = self.ids.magic
        self.magiclabel.text = 'Mag:' + str(char.totalMagic)

        self.endlabel = self.ids.endurance
        self.endlabel.text = 'End:' + str(char.totalEndurance)

        self.dexlabel = self.ids.dexterity
        self.dexlabel.text = 'Dex:' + str(char.totalDexterity)

        self.agilabel = self.ids.agility
        self.agilabel.text = "Agi: " + str(char.totalAgility)
        self.updateStars(char)


class emptycharacterpreview(Screen):

    def __init__(self, managerPass, **kwargs):
        super(emptycharacterpreview, self).__init__(**kwargs)
        self.managerObject = managerPass
        self.button = Button(size=(250, 650), pos=(0, 0), size_hint=(None, None), background_normal='',
                             background_down='', background_color=(0, 0, 0, 0))
        self.button.bind(on_touch_down=self.onPressed)
        with self.button.canvas:
            color = Color(1, 1, 1, 1)
            rect = Rectangle(size=(250, 650), pos=(0, 0))
        image = Image(source='res/Empty.jpg', allow_stretch=True, keep_ratio=True, size_hint=(None, None),
                      size=(250, 650))
        self.button.add_widget(image)
        self.add_widget(self.button)

    def onPressed(self, instance, touch):
        if self.button.collide_point(*touch.pos):
            if touch.is_touch:
                if touch.button == 'left':
                    if not self.managerObject.isDisabled:
                        self.managerObject.setPreview("empty")
            else:
                if not self.managerObject.isDisabled:
                    self.managerObject.setPreview("empty")


class removeSlot(Screen):

    def __init__(self, managerPass, char, message, **kwargs):
        super(removeSlot, self).__init__(**kwargs)
        self.managerObject = managerPass
        self.button = Button(on_touch_down=self.onPressed, size=(250, 650), pos=(0, 0), size_hint=(None, None))
        image = Image(source='res/removeSlot.png', allow_stretch=True, keep_ratio=True, size_hint=(None, None),
                      size=(250, 650))
        label = Label(text=message, font_size=40, pos=(75, 175), color=(0, 0, 0, 1))
        image.add_widget(label)
        self.char = char
        self.button.add_widget(image)
        self.add_widget(self.button)

    def onPressed(self, instance, touch):
        if self.button.collide_point(*touch.pos):
            if touch.is_touch:
                if touch.button == 'left':
                    self.managerObject.setEmpty()
            else:
                self.managerObject.setEmpty()


class scrollcharacterpreview(Screen):

    def __init__(self, **kwargs):
        super(scrollcharacterpreview, self).__init__(**kwargs)
        pass


class CharacterAttributeScreen(Screen):
    charname = StringProperty('')

    # chardisplayname = StringProperty('')
    # charid = StringProperty('')
    # charfullimage = StringProperty('')
    def __init__(self, char, preview, **kwargs):
        super(CharacterAttributeScreen, self).__init__(**kwargs)
        self.charname = char.getname()
        self.preview = preview
        # self.chardisplayname = char.getdisplayname()
        # self.charid = char.getid()
        # self.charfullimage = char.getfullimage()
        self.layout = FloatLayout()

        self.add_widget(self.layout)
        self.bg = Image(source='res/charattributebg.png', size=(2560, 1440), pos=(0, 0), allow_stretch=True,
                        keep_ratio=False)
        self.layout.add_widget(self.bg)
        self.char = char
        self.id = self.name
        image = Image(source=char.getfullimage(), pos=(0, 0), size=(App.height, App.height), size_hint=(None, None),
                      allow_stretch=True, keep_ratio=True)
        self.layout.add_widget(image)
        self.backButton = customButton(id='back', source='res/BackArrow.png', size=(100, 100),
                                       pos=(100, self.height - 200),
                                       on_touch_down=self.onBackPress)
        self.layout.add_widget(self.backButton)

        ###### DEV BUTTONS ######
        self.maxStats = Button(text="Max Stats", font_size=40, pos=(500, 1000), size=(200, 200),
                               on_touch_down=self.maxOut, size_hint=(None, None))
        self.rankupButton = Button(text="Rank Up", font_size=40, pos=(900, 500), size=(200, 200),
                                   on_touch_down=self.onRankUp, size_hint=(None, None))
        self.rankbreakButton = Button(text="Rank Break", font_size=40, pos=(900, 300), size=(200, 200),
                                      on_touch_down=self.onRankBreak, size_hint=(None, None))

        self.hpexpincreaseButton = Button(text="Increase Hp Exp", font_size=40, pos=(1200, 1000), size=(300, 50),
                                          on_touch_down=self.increaseExpStat, size_hint=(None, None))
        self.mpexpincreaseButton = Button(text="Increase Mp Exp", font_size=40, pos=(1200, 925), size=(300, 50),
                                          on_touch_down=self.increaseExpStat, size_hint=(None, None))
        self.defexpincreaseButton = Button(text="Increase Def Exp", font_size=40, pos=(1200, 850), size=(300, 50),
                                           on_touch_down=self.increaseExpStat, size_hint=(None, None))
        self.strexpincreaseButton = Button(text="Increase Str Exp", font_size=40, pos=(1200, 775), size=(300, 50),
                                           on_touch_down=self.increaseExpStat, size_hint=(None, None))
        self.agiexpincreaseButton = Button(text="Increase Agi Exp", font_size=40, pos=(1200, 700), size=(300, 50),
                                           on_touch_down=self.increaseExpStat, size_hint=(None, None))
        self.dexexpincreaseButton = Button(text="Increase Dex Exp", font_size=40, pos=(1200, 625), size=(300, 50),
                                           on_touch_down=self.increaseExpStat, size_hint=(None, None))
        self.endexpincreaseButton = Button(text="Increase End Exp", font_size=40, pos=(1200, 550), size=(300, 50),
                                           on_touch_down=self.increaseExpStat, size_hint=(None, None))

        # self.add_widget(self.maxStats)
        # self.add_widget(self.rankupButton)
        # self.add_widget(self.rankbreakButton)
        # self.add_widget(self.hpexpincreaseButton)
        # self.add_widget(self.mpexpincreaseButton)
        # self.add_widget(self.defexpincreaseButton)
        # self.add_widget(self.strexpincreaseButton)
        # self.add_widget(self.agiexpincreaseButton)
        # self.add_widget(self.dexexpincreaseButton)
        # self.add_widget(self.endexpincreaseButton)

        ###### DEV BUTTONS END ######

        count = 0
        self.stars = []
        addx = False
        for x in char.ranks:
            # print("Rank: " + str(x))
            xpos = 50
            if addx:
                xpos += 25
            if x.unlocked:
                if not x.broken:
                    self.stars.append(Image(source="res/star.png", pos=(xpos, 350 + (count * 75)), size=(140, 140),
                                            size_hint=(None, None), opacity=1))
                    self.layout.add_widget(self.stars[count])
                else:
                    self.stars.append(Image(source="res/rankbrk.png", pos=(xpos, 350 + (count * 75)), size=(140, 140),
                                            size_hint=(None, None), opacity=1))
                    self.layout.add_widget(self.stars[count])
            else:
                self.stars.append(Image(pos=(xpos, 350 + (count * 75)), size=(140, 140),
                                        size_hint=(None, None), opacity=0))
                self.layout.add_widget(self.stars[count])
            count += 1
            if addx:
                xpos -= 25
            addx = not addx

        self.nameLabel = Label(text='[b]' + self.char.getname() + '[/b]', size_hint=(None, None), font_size=120,
                               color=(1, 1, 1, .8), markup=True)
        with self.nameLabel.canvas.before:
            Color(.1, .1, .1, .6)
            Rectangle(size=(len(self.char.getname()) * 60 + 75, 160),
                      pos=(App.height - len(self.char.getname()) * 55.5 - 100, App.height - 160))
        self.displaynameLabel = Label(text='[b]' + self.char.getdisplayname() + '[/b]', size_hint=(None, None),
                                      color=(1, 1, 1, .75), font_size=90, markup=True)

        # Total Stat Window

        self.status_board_manager = StatusBoardManager(self.char, size=(1120, 1440), pos=(1440, 0),
                                                       size_hint=(None, None),
                                                       transition=SlideTransition(duration=.375))
        self.layout.add_widget(self.status_board_manager)
        self.layout.add_widget(self.nameLabel)
        self.totalstatpreview = StatPreview(self.char, 1, 1, True, char.totalPhysicalAttack, char.totalMagicalAttack,
                                            char.totalMP,
                                            char.totalHealth, char.totalDefense, char.totalStrength, char.totalMagic,
                                            char.totalAgility, char.totalDexterity, char.totalEndurance,
                                            size=(1300, 300), pos=(0, 0))
        self.rankstatpreview = StatPreview(self.char, 1, 1, False, char.ranks[0].rankstrengthtotal,
                                           char.ranks[0].rankmagictotal,
                                           char.ranks[0].rankmagicalpointstotal, char.ranks[0].rankhealthtotal,
                                           char.ranks[0].rankdefensetotal,
                                           char.ranks[0].rankstrengthtotal, char.ranks[0].rankmagictotal,
                                           char.ranks[0].rankagilitytotal, char.ranks[0].rankdexteritytotal,
                                           char.ranks[0].rankendurancetotal, size=(350, 340), pos=(App.height, 0))
        self.layout.add_widget(self.totalstatpreview)
        self.layout.add_widget(self.rankstatpreview)
        Clock.schedule_once(self.updatelabels)

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
                    self.stars[count].source = 'res/star.png'
                    self.stars[count].opacity = 1
                else:
                    self.stars[count].source = 'res/rankbrk.png'
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

    def onBackPress(self, instance, touch):
        if self.backButton.collide_point(*touch.pos):
            App.root.goto_back()


class StatusBoardManager(ScreenManager):
    def __init__(self, char, **kwargs):
        super(StatusBoardManager, self).__init__(**kwargs)
        self.screens = []
        self.ranks = char.ranks
        for x in range(10):
            self.screens.append(statusBoard(x, self, self.ranks[x], char, char.ranks[x].grid.grid, name='grid %d' % x))
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


class statusBoard(Screen):
    def __init__(self, number, managerPass, rank, char, grid, **kwargs):
        super(statusBoard, self).__init__(**kwargs)
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
                    slot = CustomSlot(1, pos=(gridObjectX, gridObjectY), source='res/SlotStrength.png',
                                      size=(sqSize, sqSize), on_touch_down=self.slotPressed)
                elif gridObject == 'M':
                    slot = CustomSlot(2, pos=(gridObjectX, gridObjectY), source='res/SlotMagic.png',
                                      size=(sqSize, sqSize), on_touch_down=self.slotPressed)
                elif gridObject == 'A':
                    slot = CustomSlot(3, pos=(gridObjectX, gridObjectY), source='res/SlotAgility.png',
                                      size=(sqSize, sqSize), on_touch_down=self.slotPressed)
                elif gridObject == 'D':
                    slot = CustomSlot(4, pos=(gridObjectX, gridObjectY), source='res/SlotDexterity.png',
                                      size=(sqSize, sqSize), on_touch_down=self.slotPressed)
                elif gridObject == 'E':
                    slot = CustomSlot(5, pos=(gridObjectX, gridObjectY), source='res/SlotEndurance.png',
                                      size=(sqSize, sqSize), on_touch_down=self.slotPressed)
                else:
                    slot = CustomSlot(6, pos=(gridObjectX, gridObjectY), source='res/SlotEmpty.png',
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
                color = self._coreimage.read_pixel((x - self.x) * scale, (self.height - (y - self.y)) * scale)
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
                color = self._coreimage.read_pixel((x - self.x) * scale, (self.height - (y - self.y)) * scale)
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
        self.source = "res/TotalSingleAttackWindow.png"
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
            self.add_widget(Image(source='res/StatBar.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                                  allow_stretch=True))
            self.add_widget(Image(source='res/Health.png', size=(40, 40), pos=(x + 15, y + 5)))
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
            self.add_widget(Image(source='res/StatBar.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                                  allow_stretch=True))
            self.add_widget(Image(source='res/Mana.png', size=(40, 40), pos=(x + 15, y + 5)))
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
                    Image(source='res/StatBar.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                          allow_stretch=True))
                self.add_widget(Image(source='res/PhysicalAttack.png', size=(40, 40), pos=(x + 15, y + 5)))
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
                    Image(source='res/StatBar.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                          allow_stretch=True))
                self.add_widget(Image(source='res/MagicalAttack.png', size=(40, 40), pos=(x + 15, y + 5)))
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
                    Image(source='res/StatBar.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                          allow_stretch=True))
                self.add_widget(Image(source='res/PhysicalAttack.png', size=(40, 40), pos=(x + 15, y + 5)))
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
                    Image(source='res/StatBar.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                          allow_stretch=True))
                self.add_widget(Image(source='res/magicalAttack.png', size=(40, 40), pos=(x + 15, y + 5)))
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
            self.add_widget(Image(source='res/StatBar.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                                  allow_stretch=True))
            self.add_widget(Image(source='res/Defense.png', size=(40, 40), pos=(x + 15, y + 5)))
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
                    Image(source='res/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
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
                    Image(source='res/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
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
                    Image(source='res/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
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
                    Image(source='res/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
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
            self.add_widget(Image(source='res/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
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
            self.add_widget(Image(source='res/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                                  allow_stretch=True))
            self.dexteritylabel = StatLabel(text='Dex.', font_size=50, color=(0, 0, 0, 1), pos=(x + 20, y))
            self.dexteritygrade = Image(source=Scale.getScaleAsImagePath(dexterity, char.totalCaps[3]),
                                        pos=(x + 90, y + 10), height=40, keep_ratio=True, allow_stretch=True)
            self.dexteritynumber = StatLabel(text='%d' % dexterity, font_size=50, color=(0, 0, 0, 1), pos=(x + 180, y))
            self.add_widget(self.dexteritygrade)
            self.add_widget(self.dexteritylabel)
            self.add_widget(self.dexteritynumber)
            y -= 70
            self.add_widget(Image(source='res/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
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
            self.healthLvlBar = ProgressBarCustom(1, (275, 25))
            self.healthLvlBar.max = char.ranks[char.currentRank - 1].expHpCap
            self.healthLvlBar.value = char.ranks[char.currentRank - 1].exphealth
            self.healthLvlBar.pos = 890, 190
            self.healthLvlTitle = Label(text='HP', font_size=30, color=(0, 0, 0, 1), size=(50, 20), pos=(860, 200))
            self.healthLvlTitle.size = self.healthLvlTitle.texture_size
            self.add_widget(self.healthLvlBar)
            self.add_widget(self.healthLvlTitle)
            # Mp Exp Bar
            self.mpLvlBar = ProgressBarCustom(2, (275, 25))
            self.mpLvlBar.max = char.ranks[char.currentRank - 1].expMpCap
            self.mpLvlBar.value = char.ranks[char.currentRank - 1].expmagicalpoints
            self.mpLvlBar.pos = 890, 160
            self.mpLvlTitle = Label(text='MP', font_size=30, color=(0, 0, 0, 1), size=(50, 20), pos=(860, 170))
            self.mpLvlTitle.size = self.mpLvlTitle.texture_size
            self.add_widget(self.mpLvlBar)
            self.add_widget(self.mpLvlTitle)
            # Def Exp Bar
            self.defLvlBar = ProgressBarCustom(0, (275, 25))
            self.defLvlBar.max = char.ranks[char.currentRank - 1].expDefCap
            self.defLvlBar.value = char.ranks[char.currentRank - 1].expdefense
            self.defLvlBar.pos = 890, 130
            self.defLvlTitle = Label(text='Def', font_size=30, color=(0, 0, 0, 1), size=(50, 20), pos=(860, 140))
            self.defLvlTitle.size = self.defLvlTitle.texture_size
            self.add_widget(self.defLvlBar)
            self.add_widget(self.defLvlTitle)
            # Str Exp Bar
            self.strLvlBar = ProgressBarCustom(1, (275, 25))
            self.strLvlBar.max = char.ranks[char.currentRank - 1].expStrCap
            self.strLvlBar.value = char.ranks[char.currentRank - 1].expstrength
            self.strLvlBar.pos = 890, 100
            self.strLvlTitle = Label(text='Str', font_size=30, color=(0, 0, 0, 1), size=(50, 20), pos=(860, 110))
            self.strLvlTitle.size = self.strLvlTitle.texture_size
            self.add_widget(self.strLvlBar)
            self.add_widget(self.strLvlTitle)
            # Agi Exp Bar
            self.agiLvlBar = ProgressBarCustom(3, (275, 25))
            self.agiLvlBar.max = char.ranks[char.currentRank - 1].expAgiCap
            self.agiLvlBar.value = char.ranks[char.currentRank - 1].expagility
            self.agiLvlBar.pos = 890, 70
            self.agiLvlTitle = Label(text='Agi', font_size=30, color=(0, 0, 0, 1), size=(50, 20), pos=(860, 80))
            self.agiLvlTitle.size = self.agiLvlTitle.texture_size
            self.add_widget(self.agiLvlBar)
            self.add_widget(self.agiLvlTitle)
            # Dex Exp Bar
            self.dexLvlBar = ProgressBarCustom(4, (275, 25))
            self.dexLvlBar.max = char.ranks[char.currentRank - 1].expDexCap
            self.dexLvlBar.value = char.ranks[char.currentRank - 1].expdexterity
            self.dexLvlBar.pos = 890, 40
            self.dexLvlTitle = Label(text='Dex', font_size=30, color=(0, 0, 0, 1), size=(50, 20), pos=(860, 50))
            self.dexLvlTitle.size = self.dexLvlTitle.texture_size
            self.add_widget(self.dexLvlBar)
            self.add_widget(self.dexLvlTitle)
            # End Exp Bar
            self.endLvlBar = ProgressBarCustom(5, (275, 25))
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
                    Image(source='res/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
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
                    Image(source='res/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
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
                    Image(source='res/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
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
                    Image(source='res/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                          allow_stretch=True))
                self.magiclabel = StatLabel(text='Mag.', font_size=60, color=(0, 0, 0, 1), pos=(x + 20, y))
                self.magicgrade = Image(source=Scale.getScaleAsImagePath(magic, char.ranks[rank - 1].magicMax),
                                        pos=(x + 90, y + 10), height=40, keep_ratio=True, allow_stretch=True)
                self.magicnumber = StatLabel(text='%d' % magic, font_size=50, color=(0, 0, 0, 1), pos=(x + 180, y))
                self.add_widget(self.magicgrade)
                self.add_widget(self.magiclabel)
                self.add_widget(self.magicnumber)
            y -= 70
            self.add_widget(Image(source='res/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                                  allow_stretch=True))
            self.agilitylabel = StatLabel(text='Agi.', font_size=50, color=(0, 0, 0, 1), pos=(x + 20, y))
            self.agilitygrade = Image(source=Scale.getScaleAsImagePath(agility, char.ranks[rank - 1].agilityMax),
                                      pos=(x + 90, y + 10), height=40, keep_ratio=True, allow_stretch=True)
            self.agilitynumber = StatLabel(text='%d' % agility, font_size=50, color=(0, 0, 0, 1), pos=(x + 180, y))
            self.add_widget(self.agilitygrade)
            self.add_widget(self.agilitylabel)
            self.add_widget(self.agilitynumber)
            y -= 70
            self.add_widget(Image(source='res/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                                  allow_stretch=True))
            self.dexteritylabel = StatLabel(text='Dex.', font_size=50, color=(0, 0, 0, 1), pos=(x + 20, y))
            self.dexteritygrade = Image(source=Scale.getScaleAsImagePath(dexterity, char.ranks[rank - 1].dexterityMax),
                                        pos=(x + 90, y + 10), height=40, keep_ratio=True, allow_stretch=True)
            self.dexteritynumber = StatLabel(text='%d' % dexterity, font_size=50, color=(0, 0, 0, 1), pos=(x + 180, y))
            self.add_widget(self.dexteritygrade)
            self.add_widget(self.dexteritylabel)
            self.add_widget(self.dexteritynumber)
            y -= 70
            self.add_widget(Image(source='res/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
                                  allow_stretch=True))
            self.endurancelabel = StatLabel(text='End.', font_size=50, color=(0, 0, 0, 1), pos=(x + 20, y))
            self.endurancegrade = Image(source=Scale.getScaleAsImagePath(endurance, char.ranks[rank - 1].enduranceMax),
                                        pos=(x + 90, y + 10), height=40, keep_ratio=True, allow_stretch=True)
            self.endurancenumber = StatLabel(text='%d' % endurance, font_size=50, color=(0, 0, 0, 1), pos=(x + 180, y))
            self.add_widget(self.endurancegrade)
            self.add_widget(self.endurancelabel)
            self.add_widget(self.endurancenumber)


class ProgressBarCustom(Widget):
    value = NumericProperty(0)
    max = NumericProperty(100)

    def __init__(self, type, size, *args):
        super(ProgressBarCustom, self).__init__()
        self.size = size
        self.isRainbow = False

        foreground = ''
        background = 'res/ProgressBarBackground.png'
        if type == 0:
            foreground = 'res/ProgressBarBlack.png'
        elif type == 1:
            foreground = 'res/ProgressBarRed.png'
        elif type == 2:
            foreground = 'res/ProgressBarBlue.png'
        elif type == 3:
            foreground = 'res/ProgressBarGreen.png'
        elif type == 4:
            foreground = 'res/ProgressBarPurple.png'
        elif type == 5:
            foreground = 'res/ProgressBarOrange.png'

        self.background = Image(source=background, size=self.size, pos=self.pos, keep_ratio=False, allow_stretch=True)
        self.maxValue = Label(text='%d' % self.max, pos=(self.pos[0] + self.width + 50, self.pos[1] + 10),
                              color=(0, 0, 0, 1), font_size=30)
        self.maxValue.size = self.maxValue.texture_size
        diff = 0
        if self.value > self.max:
            self.foreground.oldsource = self.foreground.source
            foreground = 'res/ProgressBarRainbow.png'
            diff = self.max
            self.isRainbow = True
        self.foreground = Image(source=foreground,
                                size=((self.width * ((self.value - diff) / self.max), self.height), self.height),
                                pos=self.pos, keep_ratio=False, allow_stretch=True)
        self.add_widget(self.background)
        self.add_widget(self.foreground)
        self.add_widget(self.maxValue)

    def on_value(self, *args):
        diff = 0
        if self.value > self.max:
            if not self.isRainbow:
                self.foreground.oldsource = self.foreground.source
                self.foreground.source = 'res/ProgressBarRainbow.png'
                diff = self.max
                if self.value > self.max * 2:
                    self.value = self.max * 2
                self.isRainbow = True
        else:
            if self.isRainbow:
                self.foreground.source = self.foreground.oldsource
                self.foreground.oldsource = ''
                self.isRainbow = False
        self.foreground.size = (self.width * ((self.value - diff) / self.max), self.height)

    def on_max(self, *args):
        self.maxValue.text = ('{:6}'.format('{:0.1f}'.format(self.max)))
        # self.maxValue.size = self.maxValue.texture_size
        # self.maxValue.pos = (self.pos[0] + self.width + 50, self.pos[1] + 10)

        diff = 0
        if self.value > self.max:
            if not self.isRainbow:
                self.foreground.oldsource = self.foreground.source
                self.foreground.source = 'res/ProgressBarRainbow.png'
                diff = self.max
                self.isRainbow = True
        else:
            if self.isRainbow:
                self.foreground.source = self.foreground.oldsource
                self.foreground.oldsource = ''
                self.isRainbow = False
        self.foreground.width = self.width * ((self.value - diff) / self.max)

    def on_pos(self, *args):
        self.foreground.pos = self.pos
        self.background.pos = self.pos
        self.maxValue.pos = (self.pos[0] + self.width + 50, self.pos[1] + 10)


class MoveBarObject(FloatLayout):

    def __init__(self, **kwargs):
        super(MoveBarObject, self).__init__(**kwargs)
        self.visible = False
        self.opacity = 0
        self.size = 0, 0
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
            # print(self.parent.parent.selectedMove)
            # print(self.parent.parent)
        else:
            print("not visible")

    def hide_widget(wid):
        # print(wid)
        if wid.visible:
            wid.size, wid.size_hint, wid.opacity = (0, 0), (0, 0), 0
            wid.visible = False
        else:
            wid.size, wid.size_hint, wid.opacity = (875, 75), (0, 0), 1
            wid.visible = True


class CharPreview(Image):
    health = NumericProperty(0)
    mp = NumericProperty(0)
    selectedMove = NumericProperty(0)

    move1 = ObjectProperty(None)
    move2 = ObjectProperty(None)
    move3 = ObjectProperty(None)
    move4 = ObjectProperty(None)
    special = ObjectProperty(None)
    move1name = StringProperty("")
    move2name = StringProperty("")
    move3name = StringProperty("")
    move4name = StringProperty("")
    specialname = StringProperty("")

    def __init__(self, char, pos):
        super(CharPreview, self).__init__()
        self.char = char
        # print(str(self.char.getmove(0)))
        self.move1 = self.char.getmove(0)
        self.move2 = self.char.getmove(1)
        self.move3 = self.char.getmove(2)
        self.move4 = self.char.getmove(3)
        self.special = self.char.getmove(4)
        self.source = self.char.getpreviewimage()
        self.size = 200, 200
        self.pos = pos
        self.size_hint = None, None
        self.allow_stretch = True
        self.keep_ratio = True
        with self.canvas:
            Color(1, 1, 1, .6)
            Rectangle(pos=self.pos, size=(200, 55))
        self.healthLabel = Label(text="[b]HP[/b]", font_size=24, markup=True, pos=(self.pos[0] + 10, self.pos[1] + 30),
                                 size=(20, 20),
                                 color=(0, 0, 0, 1), size_hint=(None, None))
        self.healthBar = ProgressBarCustom(1, (145, 20))
        self.healthBar.pos = self.pos[0] + 45, self.pos[1] + 30
        self.healthBar.max = self.char.totalHealth
        self.healthBar.value = self.health
        self.mpLabel = Label(text="[b]MP[/b]", font_size=24, markup=True, pos=(self.pos[0] + 10, self.pos[1] + 5),
                             size=(20, 20),
                             color=(0, 0, 0, 1), size_hint=(None, None))
        self.mpBar = ProgressBarCustom(2, (145, 20))
        self.mpBar.pos = self.pos[0] + 45, self.pos[1] + 5
        self.mpBar.max = self.char.totalMP
        self.mpBar.value = self.mp
        self.add_widget(self.healthBar)
        self.add_widget(self.healthLabel)
        self.add_widget(self.mpBar)
        self.add_widget(self.mpLabel)
        self.health = char.totalHealth
        self.mp = char.totalMP
        # self.add_widget(moveBar())

    def on_health(self, *args):
        self.healthBar.value = self.health

    def on_mp(self, *args):
        self.mpBar.value = self.mp

    def on_move1(self, *args):
        self.move1name = self.move1.getname()

    def on_move2(self, *args):
        self.move2name = self.move2.getname()

    def on_move3(self, *args):
        self.move3name = self.move3.getname()

    def on_move4(self, *args):
        self.move4name = self.move4.getname()

    def on_special(self, *args):
        self.specialname = self.special.getname()


class EnemyType:
    def __init__(self, name, attackType, healthMin, healthMax, strMin, strMax, magMin, magMax, agiMin, agiMax, dexMin,
                 dexMax, endMin, endMax, moves, movesPropabilities):
        self.name = name
        self.moves = moves
        self.movePropabilities = movesPropabilities
        self.attackType = attackType
        self.healthMin = healthMin
        self.healthMax = healthMax
        self.strMin = strMin
        self.strMax = strMax
        self.magMin = magMin
        self.magMax = magMax
        self.agiMin = agiMin
        self.agiMax = agiMax
        self.dexMin = dexMin
        self.dexMax = dexMax
        self.endMin = endMin
        self.endMax = endMax

    def new_instance(self, statMultiplier):
        return Enemy(self.name, self.attackType,
                     random.randint(self.healthMin * statMultiplier, self.healthMax * statMultiplier),
                     random.randint(self.strMin * statMultiplier, self.strMax * statMultiplier),
                     random.randint(self.magMin * statMultiplier,
                                    self.magMax * statMultiplier),
                     random.randint(self.agiMin * statMultiplier, self.agiMax * statMultiplier),
                     random.randint(self.dexMin * statMultiplier, self.dexMax * statMultiplier),
                     random.randint(self.endMin * statMultiplier, self.endMax * statMultiplier), self.moves,
                     self.movePropabilities)


class Enemy:
    def __init__(self, name, attackType, health, str, mag, agi, dex, end, moves, movePropabilities):
        self.name, self.attackType, self.health, self.str, self.mag, self.agi, self.dex, self.end = name, attackType, health, str, mag, agi, dex, end
        self.moves = moves
        self.movePropabilities = movePropabilities

    def generateSpeed(self):
        return random.randint(int(self.agi * .85 * 21), int(self.agi * 21))

    def processDamage(self, damage, char):
        print("Damage is " + str(damage))
        # base damage calculation

        # Penetration
        pen = random.randint(0, 100) <= 20 * (1 + (Scale.getScale_as_number(char.totalStrength, char.ranks[
            char.currentRank - 1].StrengthMax) + Scale.getScale_as_number(char.totalDexterity, char.ranks[
            char.currentRank - 1].dexterityMax) / 2))
        if pen:
            print("Penetration.")
            damage *= 1.5
        # Guarding
        guard = random.randint(0, 100) <= 20 * (1 + (Scale.getScale_as_number(char.totalAgility, char.ranks[
            char.currentRank - 1].agilityMax) + Scale.getScale_as_number(char.totalDexterity, char.ranks[
            char.currentRank - 1].dexterityMax) / 2))
        if guard and not pen:
            print("Guard.")
            damage *= 0.5
        # Calculating Critical dex & agi
        crit = random.randint(0, 100) <= 20 * (1 + (Scale.getScale_as_number(char.totalAgility, char.ranks[
            char.currentRank - 1].agilityMax) + Scale.getScale_as_number(char.totalDexterity, char.ranks[
            char.currentRank - 1].dexterityMax) / 2))

        if crit:
            print("Critical hit.")
            damage *= 1.5

        # Penetration
        if agi > self.dex:
            topShelf = 0
            print("No Miss. Damage mult 2.4")
            damage *= 2.4
        else:
            topShelf = agi / self.dex
        print("Hit Chance is " + str((topShelf * 100) - 20))
        if not topShelf == 0:
            hit = random.randint(0, int(topShelf * 100)) > 20
        else:
            hit = True
        print("Hit: " + str(hit) + " for " + str(damage))
        if hit:
            self.health -= damage
        else:
            damage = 0
        return damage


class Floor:
    """
    Boss Type:
    0 - Boss is a single Enemy and has been passed in the boss parameter
    1 - Boss is multiple of the passed boss parameter with maxCounts
    2 - Boss is multiple of the passed boss parameter with maxCounts upped by 40%
    3 - Boss is multiple of normally passed enemies - maxCounts upped by 40%
    4 - Boss is multiple of normally passed enemies - maxCounts upped by 40% & stats upped by 30%
    """

    def __init__(self, floornum, maxEnemies, minEncounters, maxEncounters, bossType, boss, Enemies, propabilities):
        self.floornum, self.maxEnemies = floornum, maxEnemies
        self.minEncounters, self.maxEncounters = minEncounters, maxEncounters
        self.bossType, self.boss = bossType, boss
        self.enemies = Enemies
        self.propabilities = propabilities
        self.PERCENT100 = 100
        self.BOSSMULTIPLIER = .4
        self.BOSSSTATMULTIPLIER = .3
        self.MINMAXENEMIES = .25

    def generateEncounterNumber(self):
        return random.randint(self.minEncounters, self.maxEncounters)

    def generateBoss(self):
        if self.bossType == 0:
            return [self.boss]
        elif self.bossType == 1:
            min = int(self.maxEnemies * self.MINMAXENEMIES)
            if not min > 1:
                min = 1
            num = random.randint(min, self.maxEnemies)
            enemies = []
            for x in range(num):
                enemies.append(self.boss)
            return enemies
        elif self.bossType == 2:
            min = int(self.maxEnemies * (self.MINMAXENEMIES + self.BOSSMULTIPLIER))
            if not min > 1:
                min = 1
            num = random.randint(min,
                                 int(self.maxEnemies * (1 + self.BOSSMULTIPLIER)))
            enemies = []
            for x in range(num):
                enemies.append(self.boss)
            return enemies
        elif self.bossType == 3:
            min = int(self.maxEnemies * (self.MINMAXENEMIES + self.BOSSMULTIPLIER))
            if not min > 1:
                min = 1
            num = random.randint(min, int(self.maxEnemies * (1 + self.BOSSMULTIPLIER)))
            enemies = []
            for x in range(num):
                num = random.randint(0, self.PERCENT100)
                for y in range(len(self.propabilities)):
                    if num < (self.propabilities[y] * self.PERCENT100):
                        enemies.append(self.enemies[y].new_instance(1))
                        break
                    else:
                        num -= (self.propabilities[y] * self.PERCENT100)
            return enemies
        elif self.bossType == 4:
            min = int(self.maxEnemies * (self.MINMAXENEMIES + self.BOSSMULTIPLIER))
            if not min > 1:
                min = 1
            num = random.randint(min, int(self.maxEnemies * (1 + self.BOSSMULTIPLIER)))
            enemies = []
            for x in range(num):
                num = random.randint(0, self.PERCENT100)
                for y in range(len(self.propabilities)):
                    if num < (self.propabilities[y] * self.PERCENT100):
                        enemies.append(self.enemies[y].new_instance(1 + self.BOSSSTATMULTIPLIER))
                        break
                    else:
                        num -= (self.propabilities[y] * self.PERCENT100)
            return enemies

    def generateEnemies(self):
        min = int(self.maxEnemies * self.MINMAXENEMIES)
        if not min > 1:
            min = 1
        num = random.randint(min, self.maxEnemies)
        enemies = []
        for x in range(num):
            num = random.randint(0, self.PERCENT100)
            for y in range(len(self.propabilities)):
                if num < (self.propabilities[y] * self.PERCENT100):
                    enemies.append(self.enemies[y].new_instance(1))
                    break
                else:
                    num -= (self.propabilities[y] * self.PERCENT100)
        return enemies


class GameApp(App):
    title = 'Coatirane Adventures'

    def __init__(self, *args, **kwargs):
        super(GameApp, self).__init__(*args, **kwargs)
        self.maxWidth = 1920
        self.maxHeight = 1080

    def build(self):
        App.tavern_unlocked = False
        # user32 = ctypes.windll.user32
        # width = math.floor(user32.GetSystemMetrics(0) * 2 / 3)
        # height = math.floor(user32.GetSystemMetrics(1) * 2 / 3)
        width = 1920
        height = 1080
        if width > self.maxWidth:
            width = self.maxWidth
        if height > self.maxHeight:
            height = self.maxHeight
        App.width = width
        App.height = height
        Window.size = (width, height)
        Window
        Window.minimum_width = 960
        Window.minimum_height = 540
        Window.left = 256
        Window.top = 256
        # Window.left = math.floor((user32.GetSystemMetrics(0) - width) / 2)
        # Window.top = math.floor((user32.GetSystemMetrics(1) - height) / 2)
        Window.borderless = 0
        self.build_moves()
        self.build_enemies()
        self.build_floors()
        self.build_chars()
        return Root()

    def build_moves(self):
        print("Loading Moves")
        App.moves = []
        file = open("chars/Moves.txt", "r")
        totalNum = 0
        if file.mode == 'r':
            count = 0
            for x in file:
                if x[0] != '/':
                    totalNum += 1
                    values = x[:-1].split(",", -1)
                    print("Loaded: " + str(values))
                    # MoveName, MovePower, EffectNum, MoveEffects
                    effects = []
                    effects.append(["Stun", 0])
                    effects.append(["Sleep", 0])
                    effects.append(["Poison", 0])
                    effects.append(["Burn", 0])
                    effects.append(["Charm", 0])
                    effects.append(["Seal", 0])
                    effects.append(["Taunt", 0])
                    for x in range(int(values[3])):
                        for y in effects:
                            if values[5 + (x * 2)] == y[0]:
                                y[1] = float(values[6 + (x * 2)])
                    covername = None
                    # print(str(bool(values[1] == "True")))
                    if bool(values[1] == "True"):
                        covername = values[2]
                    # MoveName, MoveCover, CoverName, MoveType, MovePower, Stun, Charm, Poision, Burn, Sleep, Seal, Taunt
                    App.moves.append(
                        Move(values[0], bool(values[1] == "True"), covername, int(values[3]), values[4], effects))
            file.close()
            print("Loaded %d moves." % totalNum)
        else:
            raise Exception("Failed to open Move Definition file!")

    def build_floors(self):
        print("Loading Floors")
        App.floors = []
        file = open("chars/Floors.txt", "r")
        totalNum = 0
        if file.mode == 'r':
            for x in file:
                if x[0] != '/':
                    totalNum += 1
                    values = x[:-1].split(",", -1)
                    print("Loaded: " + str(values))
                    propabilities = []
                    enemies = []
                    boss = None
                    for x in range(int(values[2])):
                        currStr = values[6 + (x * 2)]
                        temp = None
                        for y in App.enemies:
                            if y.name == currStr:
                                enemies.append(y)
                                temp = y
                                break
                        if values[6 + (x * 2)] == "BOSS":
                            boss = temp
                        else:
                            propabilities.append(float(values[7 + (x * 2)]))
                    # // FloorNum, MaxEnemies, MinEncounters, MaxEncounters, BossType, ArrayNum, [EnemyName, EnemyProbability]
                    App.floors.append(
                        Floor(int(values[0]), int(values[1]), int(values[2]), int(values[3]), int(values[4]), boss,
                              enemies, propabilities))
            file.close()
            print("Loaded %d floors." % totalNum)
        else:
            raise Exception("Failed to open Floor Definition file!")

    def build_enemies(self):
        print("Loading Enemies")
        App.enemies = []
        file = open("chars/Enemies.txt", "r")
        totalNum = 0
        if file.mode == 'r':
            for x in file:
                if x[0] != '/':
                    totalNum += 1
                    values = x[:-1].split(",", -1)
                    print("Loaded: " + str(values))
                    moves = []
                    movePropabilities = []
                    for x in range(int(values[14])):
                        moves.append(Move.getmove(App.moves, values[15 + (2 * x)]))
                        movePropabilities.append(values[16 + (2 * x)])

                    App.enemies.append(
                        EnemyType(values[0], int(values[3]), int(values[1]), int(values[2]), int(values[4]),
                                  int(values[5]), int(values[6]), int(values[7]), int(values[8]), int(values[9]),
                                  int(values[10]), int(values[11]), int(values[12]), int(values[13]), moves,
                                  movePropabilities))
                    # // EnemyName, HealthMin, HealthMax, AttackType, StrMin, StrMax, MagMin, MagMax, AgiMin, AgiMax, DexMin, DexMax, EndMin, EndMax
            file.close()
            print("Loaded %d enemies." % totalNum)
        else:
            raise Exception("Failed to open Enemy Definition file!")

    def build_chars(self):
        print("Loading Characters")
        App.characterArray = []
        App.party1 = []
        App.currentparty = []
        App.slots = []
        App.slotscreens = []
        App.obtainedcharsArray = []
        for x in range(6):
            App.currentparty.append(None)
        file = open("chars/CharacterDefinitions.txt", "r")
        totalNum = 0
        if file.mode == 'r':
            count = 0
            for x in file:
                if x[0] != '/':
                    totalNum += 1
                    values = x[:-1].split(",", -1)
                    print("Loaded: " + str(values))
                    # Name,Type Name,Id,Rank(0 - 10),Health,Defense PhysicalAttack MagicalAttack MagicalPoints Strength Magic Endurance Dexterity Agility BasicAtkPwr Atk Type
                    rank = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                    # for x in range(len(values)):
                    #     print("%d : %s" % (x, str(values[x]))
                    App.characterArray.append(
                        Character(count, values[0], values[1], values[2], rank, int(values[3]), int(values[4]),
                                  int(values[5]), int(values[6]), int(values[7]), int(values[8]), int(values[9]),
                                  int(values[10]), int(values[11]), int(values[12]),
                                  'res/Prev/' + values[2] + '_slide.png', 'res/Prev/' + values[2] + '_preview.png',
                                  'res/Prev/' + values[2] + '_full.png', (
                                      Move.getmove(App.moves, values[13]), Move.getmove(App.moves, values[14]),
                                      Move.getmove(App.moves, values[15]), Move.getmove(App.moves, values[16]),
                                      Move.getmove(App.moves, values[17]))))
                    count += 1
            file.close()
            print("Loaded %d characters." % totalNum)
        else:
            raise Exception("Failed to open Character Definition file!")


if __name__ == "__main__":
    GameApp().run()
