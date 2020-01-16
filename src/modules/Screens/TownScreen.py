from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.properties import NumericProperty
from kivy.graphics import Color, Rectangle
from src.modules.HTButton import HTButton

class TownScreen(Screen):

    def __init__(self, main_screen, **kwargs):
        self.initalized = False
        super(TownScreen, self).__init__(**kwargs)
        self.name = 'town_screen'

        self.main_screen = main_screen

        self._size = (0, 0)

        self.background = Image(source='../res/screens/backgrounds/townClip.jpg', allow_stretch=True)

        self.tavern_button = HTButton(size_hint=(None, None), path='../res/screens/buttons/TavernButton', collide_image='../res/screens/buttons/smallbutton.collision.png', border=[0, 0, 0, 0], text="\n\nTaverm", font_name='../res/fnt/Precious.ttf', color=(1, 1, 1, 1), on_touch_down=self.on_tavern)
        self.shopButton = HTButton(size_hint=(None, None), path='../res/screens/buttons/ShopButton', collide_image='../res/screens/buttons/smallbutton.collision.png', border=[0, 0, 0, 0], text="\n\nShop", font_name='../res/fnt/Precious.ttf', color=(1, 1, 1, 1))
        self.craftingButton = HTButton(size_hint=(None, None), path='../res/screens/buttons/CraftingButton', collide_image='../res/screens/buttons/smallbutton.collision.png', border=[0, 0, 0, 0], text="\n\nCrafting", font_name='../res/fnt/Precious.ttf', color=(1, 1, 1, 1))
        self.questButton = HTButton(size_hint=(None, None), path='../res/screens/buttons/QuestButton', collide_image='../res/screens/buttons/smallbutton.collision.png', border=[0, 0, 0, 0], text="\n\nQuest", font_name='../res/fnt/Precious.ttf', color=(1, 1, 1, 1))

        self.dungeonButton = HTButton(size_hint=(None, None), path='../res/screens/buttons/DungeonButton', collide_image='../res/screens/buttons/largebutton.collision.png', border=[0, 0, 0, 0], text="\n\nDungeon", font_name='../res/fnt/Precious.ttf', color=(1, 1, 1, 1), on_touch_down=self.on_dungeon)

        self.add_widget(self.background)
        self.add_widget(self.tavern_button)
        self.add_widget(self.shopButton)
        self.add_widget(self.craftingButton)
        self.add_widget(self.questButton)
        self.add_widget(self.dungeonButton)
        self.initalized = True

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

    def on_dungeon(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.main_screen.display_screen('dungeon_main', True, True)

    def on_tavern(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.main_screen.display_screen('tavern_main', True, True)

    def on_size(self, instance, size):
        if not self.initalized or self._size == size:
            return
        self._size = size.copy()

        small_button_size = .1 * self.main_screen.width, .1 * self.main_screen.width * 754 / 661
        large_button_size = .2 * self.main_screen.width, .2 * self.main_screen.width * 716 / 1016

        current_button_width = .1 * self.main_screen.width
        current_button_height = .05 * self.main_screen.height

        self.tavern_button.size = small_button_size
        self.tavern_button.pos = (current_button_width, current_button_height)
        self.tavern_button.font_size = small_button_size[1] * 0.15
        current_button_width += small_button_size[0]
        current_button_width += .025 * self.main_screen.width

        self.shopButton.size = small_button_size
        self.shopButton.pos = (current_button_width, current_button_height)
        self.shopButton.font_size = small_button_size[1] * 0.15
        current_button_width += small_button_size[0]
        current_button_width += .025 * self.main_screen.width

        self.craftingButton.size = small_button_size
        self.craftingButton.pos = (current_button_width, current_button_height)
        self.craftingButton.font_size = small_button_size[1] * 0.15
        current_button_width += small_button_size[0]
        current_button_width += .025 * self.main_screen.width

        self.questButton.size = small_button_size
        self.questButton.pos = (current_button_width, current_button_height)
        self.questButton.font_size = small_button_size[1] * 0.15
        current_button_width += small_button_size[0]
        current_button_width += .05 * self.main_screen.width

        self.dungeonButton.size = large_button_size
        self.dungeonButton.pos = (current_button_width, current_button_height)
        self.dungeonButton.font_size = large_button_size[1] * 0.1875

    def reload(self):
        pass
