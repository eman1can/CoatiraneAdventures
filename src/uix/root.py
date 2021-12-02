__all__ = ('Root',)

# Kivy Imports
import gc

from kivy.cache import Cache
from kivy.uix.screenmanager import FadeTransition, ScreenManager
# Project Imports
from lists import SCREEN_LIST, SCREEN_NON_WHITELIST, SCREEN_BLACKLIST
from refs import Refs


class Root(ScreenManager):
    def __init__(self, app, **kwargs):
        self._initialized = False
        self.app = app
        super().__init__(**kwargs)

        Cache.register('screens', 20, 60 * 10)

        self.transition = FadeTransition(duration=0.25)
        self.whitelist = []
        self.list = []

        self._create_screen('start_game')
        self.current = 'start_game'

        self._initialized = True

    def make_screens(self):
        pass

    def clean_whitelist(self):
        remove = []
        for screen_name in self.whitelist:
            for non_whitelist in SCREEN_NON_WHITELIST:
                if screen_name.startswith(non_whitelist):
                    remove.append(screen_name)
                    break
        for screen_name in remove:
            if screen_name == self.current_screen.name:
                continue
            self.whitelist.remove(screen_name)
            screen_s = None
            for screen in self.screens:
                if screen.name == screen_name:
                    screen_s = screen
                    break
            self.remove_widget(screen_s)
        del remove

    def get_screen(self, screen_name):
        return Cache.get('screens', screen_name)

    def display_screen(self, next_screen, direction, track, *args, **kwargs):
        old_screen = None
        if isinstance(next_screen, str):
            screen = Cache.get('screens', next_screen)
            if screen is None or next_screen in SCREEN_BLACKLIST:
                screen = self._create_screen(next_screen, *args, **kwargs)
            else:
                screen.reload(*args, **kwargs)
            next_screen = screen
        if len(self.children) > 0:
            old_screen = self.children[0]
        if not direction:
            if len(self.list) > 0:
                next_screen = self.list.pop()
                next_screen.reload(*args, **kwargs)
            else:
                print("No more screens to backtrack.")
                return

        if old_screen is None:
            Refs.log(f'Display {next_screen.name}')
        else:
            Refs.log(f'{old_screen.name} → {next_screen.name}')
        if next_screen not in self.screens:
            self.add_widget(next_screen)
        self.current = next_screen.name
        if old_screen is not None:
            if old_screen.name == 'dungeon_battle' and old_screen.boss_encounter:
                Refs.log(f'Battle from boss encounter - Dont delete')
                return
            self.remove_widget(old_screen)
            if track and old_screen.name not in SCREEN_BLACKLIST:
                self.list.append(old_screen)
            if old_screen.name in SCREEN_BLACKLIST:
                Cache.remove('screens', old_screen)

    def _create_screen(self, screen_name, *args, **kwargs):
        found = False
        for screen_option, screen_class in SCREEN_LIST.items():
            if screen_name.startswith(screen_option):
                screen = screen_class(*args, **kwargs)
                Cache.append('screens', screen_name, screen)
                found = True
                break
        if not found:
            raise Exception("Unsupported Screen type", screen_name)
        screen.size = self.size
        self.add_widget(screen)
        return screen

    def on_size(self, instance, size):
        for child in self.screens:
            child.size = self.size
