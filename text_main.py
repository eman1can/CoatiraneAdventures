# Project imports
from loading.config_loader import GAME_VERSION, PROGRAM_TYPE  # Must be first
from kivy.uix.scrollview import ScrollView
from loading.base_text import TextCALoader
from modules.game_content import GameContent
from refs import Refs
from text.console import Console

# Standard Library Imports
import os
import sys

# UIX Imports
from uix.settings import Settings

# Kivy Imports
from kivy.app import App
from kivy import Logger
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.utils import platform
from kivy.resources import resource_add_path, resource_find
from kivy.uix.relativelayout import RelativeLayout


class ClickableScrollView(ScrollView):
    def on_touch_down(self, touch):
        if self.opacity == 0:
            return False
        return super().on_touch_down(touch)


class CoatiraneAdventures(App):
    title = f'Coatirane Adventures - {GAME_VERSION}'

    def __init__(self, *args, **kwargs):
        Window.bind(on_request_close=self.close_window)

        self._content = GameContent(PROGRAM_TYPE)

        Refs.gc = self._content
        Refs.log = self.log
        Refs.app = self
        #
        self._loader = TextCALoader(PROGRAM_TYPE)
        self._loader.load_base_values()
        self.scroll_widget = None
        self.use_kivy_settings = False
        self._end_screen = None

        self.settings_cls = Settings

        super().__init__(**kwargs)


    def log(self, message, level='info'):
        Logger.log({'info': 20, 'warn': 30, 'debug': 10, 'error': 40}[level], f"CoatiraneAdventures: {message}")

    def build(self):
        layout = RelativeLayout()
        layout.add_widget(Console())
        self.scroll_widget = Builder.load_string("""
ClickableScrollView:
    size_hint: 0.6, 0.45
    pos_hint: {'right': 1}
    do_scroll_x: False
    effect_cls: 'ScrollEffect'
    Label:
        id: label
        size_hint: None, None
        size: self.texture_size
        font_name: 'Fantasque'
        font_size: str(int(root.width / 0.6 * 15 / 1706)) + 'pt'
        line_height: 1.15
        markup: True
        color: 1, 1, 1, 1
""")
        self.scroll_widget.opacity = 0
        self.scroll_widget.ids.label.text = ''
        layout.add_widget(self.scroll_widget)
        return layout

    def start_loading(self, console, save_slot, finish_screen):
        self.log('Starting background loader')
        self._loader.load_game(console, save_slot)
        Refs.gc.set_save_slot(save_slot)
        self._end_screen = finish_screen
        self._console = console

    def reset_loader(self):
        self._loader.reset()

    def finished_loading(self):
        self.log('Finished Loading')
        self._console.set_screen(self._end_screen, False)

    def close_window(self, *args):
        self.log('Save Game')
        self.log('Closing the window')
        if platform == 'win':
            Window.close()


if __name__ == "__main__":
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    game = CoatiraneAdventures()
    game.run()
    del game
    sys.exit()
