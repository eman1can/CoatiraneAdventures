# UIX Imports
# KV Import
from loading.kv_loader import load_kv
from uix.modules.screen import Screen

load_kv(__name__)


class TownScreen(Screen):
    # def __init__(self, **kwargs):
        # super().__init__(**kwargs)

        # self.sound = SoundLoader.load('res/town.mp3')
        # self.sound.loop = True

    def on_pre_enter(self, *args):
        self.check_locks()

    # def on_enter(self):
    #     pass
        # if self.sound:
        #     self.sound.play()

    # def on_leave(self):
    #     pass
        # if self.sound:
        #     self.sound.stop()

    def on_dungeon(self):
        self.manager.display_screen('dungeon_main', True, True)

    def on_tavern(self):
        if not self.content.is_tavern_locked():
            self.manager.display_screen('tavern_main', True, True)

    def on_crafting(self):
        if not self.content.is_tavern_locked():
            self.manager.display_screen('crafting_main', True, True)

    def check_locks(self):
        self.ids.tavern_lock.opacity = int(self.content.is_tavern_locked())
        self.ids.crafting_lock.opacity = int(self.content.is_tavern_locked())
