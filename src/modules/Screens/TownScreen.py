from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.properties import NumericProperty

from src.modules.CustomHoverableButton import CustomHoverableButton

class TownScreen(Screen):
    smallButton_width_scale = NumericProperty(.1)
    smallButton_left_scale = NumericProperty(.1)
    smallButton_bottom_scale = NumericProperty(.025)

    largeButton_width_scale = NumericProperty(.15)

    def __init__(self, main_screen, **kwargs):
        self.initalized = False
        super(TownScreen, self).__init__(**kwargs)
        self.main_screen = main_screen
        self.id = 'town_screen'
        self.name = 'town_screen'
        self.bgImage = Image(source='../res/screens/backgrounds/townClip.jpg', allow_stretch=True, keep_ratio=True,
                             size=(main_screen.width, main_screen.height), size_hint=(None, None), pos=(0, 0))

        small_button_size = self.smallButton_width_scale * main_screen.width, self.smallButton_width_scale * main_screen.width * 620 / 520
        large_button_size = self.largeButton_width_scale * main_screen.width, self.largeButton_width_scale * main_screen.width * 620 / 920

        current_button_width = self.smallButton_left_scale * main_screen.width
        current_button_height = self.smallButton_bottom_scale * main_screen.height

        self.tavern_button = CustomHoverableButton(size=small_button_size, size_hint=(None, None), pos=(current_button_width, current_button_height), path='../res/screens/buttons/TavernButton', collision='../res/screens/buttons/smallbutton.collision.png')
        self.tavern_button.bind(on_touch_down=self.onTavern)
        current_button_width += small_button_size[0]
        current_button_width += small_button_size[0] * .25

        self.shopButton = CustomHoverableButton(size=small_button_size, pos=(current_button_width, current_button_height), path='../res/screens/buttons/ShopButton', collision='../res/screens/buttons/smallbutton.collision.png')
        current_button_width += small_button_size[0]
        current_button_width += small_button_size[0] * .25

        self.craftingButton = CustomHoverableButton(size=small_button_size, pos=(current_button_width, current_button_height), path='../res/screens/buttons/CraftingButton', collision='../res/screens/buttons/smallbutton.collision.png')
        current_button_width += small_button_size[0]
        current_button_width += small_button_size[0] * .25

        self.questButton = CustomHoverableButton(size=small_button_size, pos=(current_button_width, current_button_height), path='../res/screens/buttons/QuestButton', collision='../res/screens/buttons/smallbutton.collision.png')
        current_button_width += small_button_size[0]
        current_button_width += small_button_size[0] * .25

        self.dungeonButton = CustomHoverableButton(size=large_button_size, pos=(current_button_width, current_button_height), path='../res/screens/buttons/DungeonButton', collision='../res/screens/buttons/largebutton.collision.png')
        self.dungeonButton.bind(on_touch_down=self.onDungeon)

        # self.bind(size=self.on_size)

        self.add_widget(self.bgImage)
        self.add_widget(self.tavern_button)
        self.add_widget(self.shopButton)
        self.add_widget(self.craftingButton)
        self.add_widget(self.questButton)
        self.add_widget(self.dungeonButton)

        self.initalized = True

        # self.sound = SoundLoader.load('res/town.mp3')
        # self.sound.loop = True

    def on_smallButton_dynamic_width_multiplier(self, *args):
        self.update_button_offsets()

    def on_smallButton_static_ratio_multiplier(self, *args):
        self.update_button_offsets()

    def on_smallButton_bottom_offset_multiplier(self, *args):
        self.update_button_offsets()

    def on_smallButton_left_offset_multiplier(self, *args):
        self.update_button_offsets()

    def update_button_offsets(self, *args):
        print("update button offsets!")
        # self.test.size = (self.main_screen.width * self.smallButton_dynamic_width_multiplier, self.main_screen.width * self.smallButton_dynamic_width_multiplier * self.smallButton_static_ratio_multiplier)
        # self.test.pos = (self.main_screen.width * self.smallButton_left_offset_multiplier, self.main_screen.height * self.smallButton_bottom_offset_multiplier)

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
            self.main_screen.create_screen('dungeon_main')

    def onTavern(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.main_screen.create_screen('tavern_main')

    def on_size(self, instance, size):


        self.bgImage.size = size

        small_button_size = self.smallButton_width_scale * self.main_screen.width, self.smallButton_width_scale * self.main_screen.width * 620 / 520
        large_button_size = self.largeButton_width_scale * self.main_screen.width, self.largeButton_width_scale * self.main_screen.width * 620 / 920
        current_button_width = self.smallButton_left_scale * self.main_screen.width
        current_button_height = self.smallButton_bottom_scale * self.main_screen.height

        self.tavern_button.size = small_button_size
        self.tavern_button.pos = (current_button_width, current_button_height)
        current_button_width += small_button_size[0]
        current_button_width += small_button_size[0] * .25

        self.shopButton.size = small_button_size
        self.shopButton.pos = (current_button_width, current_button_height)
        current_button_width += small_button_size[0]
        current_button_width += small_button_size[0] * .25

        self.craftingButton.size = small_button_size
        self.craftingButton.pos = (current_button_width, current_button_height)
        current_button_width += small_button_size[0]
        current_button_width += small_button_size[0] * .25

        self.questButton.size = small_button_size
        self.questButton.pos = (current_button_width, current_button_height)
        current_button_width += small_button_size[0]
        current_button_width += small_button_size[0] * .25

        self.dungeonButton.size = large_button_size
        self.dungeonButton.pos = (current_button_width, current_button_height)

    def reload(self):
        pass
