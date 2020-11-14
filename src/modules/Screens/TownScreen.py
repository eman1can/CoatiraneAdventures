from kivy.app import App
from kivy.core.image import Image
from kivy.properties import ObjectProperty, BooleanProperty, NumericProperty, ReferenceListProperty

from src.modules.KivyBase.Hoverable import ScreenBase as Screen


class TownScreen(Screen):
    tavern_locked = BooleanProperty(True)
    tavern_lock_opacity = NumericProperty(1)
    crafting_locked = BooleanProperty(True)
    crafting_lock_opacity = NumericProperty(1)

    small_lock_texture = ObjectProperty(None)

    small_button_width = NumericProperty(0.0)
    small_button_height = NumericProperty(0.0)
    small_button_size = ReferenceListProperty(small_button_width, small_button_height)

    large_button_width = NumericProperty(0.0)
    large_button_height = NumericProperty(0.0)
    large_button_size = ReferenceListProperty(large_button_width, large_button_height)

    def __init__(self, **kwargs):
        self.small_lock_texture = Image("../res/screens/buttons/small_button_lock.png").texture
        self.root = App.get_running_app()
        super(TownScreen, self).__init__(**kwargs)

        # self.sound = SoundLoader.load('res/town.mp3')
        # self.sound.loop = True

    def on_pre_enter(self, *args):
        self.check_locks()

    def on_enter(self):
        pass
        # if self.sound:
        #     self.sound.play()

    def on_leave(self):
        pass
        # if self.sound:
        #     self.sound.stop()

    def on_size(self, instance, size):
        self.small_button_width = self.root.width * 0.1
        self.small_button_height = self.root.width * 0.1 * 754 / 661
        self.large_button_width = self.root.width * 0.2
        self.large_button_height = self.root.width * 0.2 * 754 / 1016

    def on_dungeon(self):
        self.root.main.display_screen('dungeon_main', True, True)

    def on_tavern(self):
        if not self.tavern_locked:
            self.root.main.display_screen('tavern_main', True, True)

    def on_crafting(self):
        if not self.crafting_locked:
            pass

    def check_locks(self):
        self.tavern_locked = App.get_running_app().main.tavern_locked
        self.crafting_locked = App.get_running_app().main.crafting_locked
        if not self.tavern_locked:
            self.tavern_lock_opacity = 0
        if not self.crafting_locked:
            self.crafting_lock_opacity = 0
