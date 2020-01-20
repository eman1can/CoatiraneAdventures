from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image

from src.modules.HTButton import HTButton


class TownScreen(Screen):
    initialized = BooleanProperty(False)
    main_screen = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(TownScreen, self).__init__(**kwargs)
        self.name = 'town_screen'

        self._size = (0, 0)

        self.background = Image(source='../res/screens/backgrounds/townClip.jpg', allow_stretch=True)

        self.tavern_button = HTButton(size_hint=(None, None), path='../res/screens/buttons/TavernButton', collide_image='../res/screens/buttons/smallbutton.collision.png', text="Tavern", font_name='../res/fnt/Precious.ttf', label_color=(1, 1, 1, 1), on_release=self.on_tavern)
        self.shop_button = HTButton(size_hint=(None, None), path='../res/screens/buttons/ShopButton', collide_image='../res/screens/buttons/smallbutton.collision.png', text="Shop", font_name='../res/fnt/Precious.ttf', label_color=(1, 1, 1, 1))
        self.crafting_button = HTButton(size_hint=(None, None), path='../res/screens/buttons/CraftingButton', collide_image='../res/screens/buttons/smallbutton.collision.png', text="Crafting", font_name='../res/fnt/Precious.ttf', label_color=(1, 1, 1, 1))
        self.inventory_button = HTButton(size_hint=(None, None), path='../res/screens/buttons/inventory_button', collide_image='../res/screens/buttons/smallbutton.collision.png', text="Inventory", font_name='../res/fnt/Precious.ttf', label_color=(1, 1, 1, 1))
        self.quest_button = HTButton(size_hint=(None, None), path='../res/screens/buttons/QuestButton', collide_image='../res/screens/buttons/smallbutton.collision.png', text="Quest", font_name='../res/fnt/Precious.ttf', label_color=(1, 1, 1, 1))
        self.dungeon_button = HTButton(size_hint=(None, None), path='../res/screens/buttons/DungeonButton', collide_image='../res/screens/buttons/largebutton.collision.png', text="Dungeon", font_name='../res/fnt/Precious.ttf', label_color=(1, 1, 1, 1), on_release=self.on_dungeon)

        self.add_widget(self.background)
        self.add_widget(self.tavern_button)
        self.add_widget(self.shop_button)
        self.add_widget(self.crafting_button)
        self.add_widget(self.inventory_button)
        self.add_widget(self.quest_button)
        self.add_widget(self.dungeon_button)
        self.initialized = True

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

    def on_dungeon(self, instance):
        self.main_screen.display_screen('dungeon_main', True, True)

    def on_tavern(self, instance):
        self.main_screen.display_screen('tavern_main', True, True)

    def on_size(self, instance, size):
        if not self.initialized or self._size == size:
            return
        self._size = size.copy()

        small_button_size = .1 * self.main_screen.width, .1 * self.main_screen.width * 754 / 661
        large_button_size = .2 * self.main_screen.width, .2 * self.main_screen.width * 716 / 1016

        current_button_width = .05 * self.main_screen.width
        current_button_height = .05 * self.main_screen.height

        self.tavern_button.size = small_button_size
        self.tavern_button.pos = (current_button_width, current_button_height)
        self.tavern_button.font_size = small_button_size[1] * 0.15
        self.tavern_button.label_padding = [0, small_button_size[1] * 0.4, 0, 0]
        current_button_width += small_button_size[0]
        current_button_width += .025 * self.main_screen.width

        self.shop_button.size = small_button_size
        self.shop_button.pos = (current_button_width, current_button_height)
        self.shop_button.font_size = small_button_size[1] * 0.15
        self.shop_button.label_padding = [0, small_button_size[1] * 0.4, 0, 0]
        current_button_width += small_button_size[0]
        current_button_width += .025 * self.main_screen.width

        self.crafting_button.size = small_button_size
        self.crafting_button.pos = (current_button_width, current_button_height)
        self.crafting_button.font_size = small_button_size[1] * 0.15
        self.crafting_button.label_padding = [0, small_button_size[1] * 0.35, 0, 0]
        current_button_width += small_button_size[0]
        current_button_width += .025 * self.main_screen.width

        self.inventory_button.size = small_button_size
        self.inventory_button.pos = (current_button_width, current_button_height)
        self.inventory_button.font_size = small_button_size[1] * 0.15
        self.inventory_button.label_padding = [0, small_button_size[1] * 0.275, 0, 0]
        current_button_width += small_button_size[0]
        current_button_width += .025 * self.main_screen.width

        self.quest_button.size = small_button_size
        self.quest_button.pos = (current_button_width, current_button_height)
        self.quest_button.font_size = small_button_size[1] * 0.15
        self.quest_button.label_padding = [0, small_button_size[1] * 0.4, 0, 0]
        current_button_width += small_button_size[0]
        current_button_width += .05 * self.main_screen.width

        self.dungeon_button.size = large_button_size
        self.dungeon_button.pos = (current_button_width, current_button_height)
        self.dungeon_button.font_size = large_button_size[1] * 0.1875
        self.dungeon_button.label_padding = [0, large_button_size[1] * 0.4, 0, 0]

    def reload(self):
        pass
