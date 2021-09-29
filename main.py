__all__ = ('CoatiraneAdventures',)

# Project imports
import sys
from datetime import datetime
from os import mkdir, environ, getcwd
from os.path import exists, expanduser

# Add src to python path
base_path = getcwd()
sys.path.insert(0, f'{base_path}\\src')
sys.path.insert(0, f'{base_path}\\res')
environ['KIVY_HOME'] = f'{base_path}\\data'

from loading.config_loader import GAME_VERSION, PROGRAM_TYPE  # import must be first

from refs import Refs
from loading.base import CALoader
from modules.game_content import GameContent

# UIX imports
from uix.popups.popup_manager import PopupManager
from uix.root import Root
from uix.settings import Settings

# Kivy imports
from kivy import Config
from kivy.app import App
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.utils import platform
from kivy.core.window import Window
from kivy.uix.image import Image


class CoatiraneAdventures(App):
    title = f'Coatirane Adventures - {GAME_VERSION}'

    def __init__(self, *args, **kwargs):
        Window.bind(on_resize=self.on_resize)
        Window.bind(on_request_close=self.close_window)
        Window.bind(on_memorywarning=self.on_memory_warning)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

        # Builder.load_file('Game.kv')

        self._size = Window.size
        self.ratios = None
        self._background = None
        self._loader = None
        self._screen_manager = None
        self._popup_manager = PopupManager()
        self.use_kivy_settings = False
        self.width, self.height = self._size
        self.x, self.y = 0, 0
        self._end_screen = 'town_main'

        self._content = GameContent(PROGRAM_TYPE)

        Refs.gc = self._content
        Refs.gp = self._popup_manager
        Refs.log = self.log
        Refs.app = self

        self.settings_cls = Settings
        self._keyboard_bindings = {
            'on_key_up': [],
            'on_key_down': []
        }

        super().__init__(**kwargs)
        self.initialized = False

    def _keyboard_closed(self):
        self.log('The keyboard has been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def map_key_name(self, code):
        if code == '':
            return
        key_name = None
        if code in ('w', 'up'):
            key_name = 'move_up'
        elif code in ('a', 'left'):
            key_name = 'move_left'
        elif code in ('s', 'down'):
            key_name = 'move_down'
        elif code in ('d', 'right'):
            key_name = 'move_right'
        elif code in ('m',):
            key_name = 'map'
        elif code in ('o',):
            key_name = 'options'
        elif code in ('i',):
            key_name = 'inventory'
        elif code in ('esc',):
            key_name = 'pause'
        elif code in ('q',):
            key_name = 'secondary_action_1'
        elif code in ('e',):
            key_name = 'secondary_action_2'
        elif code in ('f',):
            key_name = 'primary_action'
        elif code in ('f12',):
            key_name = 'screenshot'
        return key_name

    def take_screenshot(self):
        path = expanduser('~/Saved Games/Coatirane Adventures/screenshots/').replace('\\', '/')
        if not exists(path):
            mkdir(path)
        Window.screenshot(f'{path}Coatirane Adventures - {datetime.now().strftime("%d-%m-%Y %H-%M-%S")}.png')

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        Refs.log(f'Key was pressed - {keycode}')
        key_name = self.map_key_name(keycode[1])
        if key_name is not None:
            if key_name == 'screenshot':
                self.take_screenshot()
            else:
                for callback in self._keyboard_bindings['on_key_down']:
                    callback(keyboard, key_name, text, modifiers)

    def _on_keyboard_up(self, keyboard, keycode):
        key_name = self.map_key_name(keycode[1])
        if key_name == 'screenshot' or key_name is None:
            return
        for callback in self._keyboard_bindings['on_key_up']:
            callback(keyboard, key_name)

    def bind_keyboard(self, **kwargs):
        self.log(f'Add binding for master keyboard')
        for key, callback in kwargs.items():
            self._keyboard_bindings[key].append(callback)

    def unbind_keyboard(self, **kwargs):
        self.log(f'Remove binding for master keyboard')
        for key, callback in kwargs.items():
            self._keyboard_bindings[key].remove(callback)

    def log(self, message, level='info', tag='CoatiraneAdventures'):
        Logger.log({'info': 20, 'warn': 30, 'debug': 10, 'error': 40}[level], f"{tag}: {message}")

    def to_window(self, x, y):
        return x, y

    def build(self):
        self.log('loading the starting game window')
        self._background = Image(source="game_bounds.png", allow_stretch=True)

        self.log('creating background loader')
        self._loader = CALoader(PROGRAM_TYPE)

        self._loader.load_base_values()
        self._loader.size = self._size

        self.ratios = self._loader.load_ratios()

        # self.background.add_widget(self.loader)
        self._screen_manager = Root(self)
        Refs.gs = self._screen_manager
        self._screen_manager.size = self._size
        self._background.add_widget(self._screen_manager)
        return self._background

    def start_loading(self, save_slot, finish_screen):
        self.log('Starting background loader')
        self._background.add_widget(self._loader)
        self._screen_manager.opacity = 0
        self._end_screen = finish_screen
        Refs.gc.set_save_slot(save_slot)
        Clock.schedule_once(lambda dt: self._loader.load_game(save_slot), 0)

    def finished_loading(self):
        self.log('Finished Loading')
        self._background.remove_widget(self._loader)
        self._screen_manager.display_screen(self._end_screen, True, False)
        self._screen_manager.opacity = 1

    def get_manager(self):
        return self._screen_manager

    # def add_manager(self, manager):
    #     self._screen_manager = manager
    #     manager.size = self.width, self.height
    #
    # def set_manager(self):
    #     self._background.add_widget(self._screen_manager)

    def allow_sleep(self):
        Window.allow_screensaver = True

    def deny_sleep(self):
        Window.deny_screensaver = True

    def close_window(self, *args):
        self.log('Save Game')
        self.log('Closing the window')
        if platform == 'win':
            Window.close()

    def on_memory_warning(self):
        self.log('received memory warning')

    # The game may or may not return from a pause.
    def on_pause(self):
        self.log('game paused')
        if platform == 'win':
            return True
        else:
            return True

    def exit_game(self):
        self.stop()

    def on_resize(self, *args):
        Clock.unschedule(self.fix_size)
        Clock.schedule_once(self.fix_size, .25)

    def get_content(self):
        return self._content

    def make_windowed(self):
        Window.fullscreen = 0
        Window.borderless = 0
        w, h = int(Config.get('graphics', 'width')), int(Config.get('graphics', 'height'))
        sw, sh = int(Config.get('graphics', 'screen_width')), int(Config.get('graphics', 'screen_height'))
        if w == sw and h == sh:
            w, h = int(w * 2 / 3), int(h * 2 / 3)
            l, t = int(sw / 2 - w / 2), int(sh / 2 - h / 2)
            Window.left = l
            Window.top = t
            Config.set('graphics', 'width', int(w))
            Config.set('graphics', 'height', int(h))
            Config.set('graphics', 'left', l)
            Config.set('graphics', 'top', t)
            Config.write()
        Window.size = w, h
        self.log(f'Window size is {w}x{h}')
        self.width, self.height = w, h

    def make_fake_fullscreen(self):
        Window.fullscreen = 0
        Window.borderless = 1
        Window.pos = 0, 0
        Window.left = 0
        Window.top = 0
        width, height = int(Config.get('graphics', 'screen_width')), int(Config.get('graphics', 'screen_height'))
        Config.set('graphics', 'width', width)
        Config.set('graphics', 'height', height)
        Config.set('graphics', 'left', 0)
        Config.set('graphics', 'top', 0)
        Config.write()
        Window.size = width, height
        self.width, self.height = width, height

    def fix_size(self, *args):
        if self._size == Window.size:
            return
        self._size = Window.size
        self._background.size = Window.size

        offset = self._background.width/2 - self._background.norm_image_size[0]/2, self._background.height/2 - self._background.norm_image_size[1]/2
        if self._loader:
            self._loader.size = self._background.norm_image_size
            self._loader.pos = offset
        #if self.initialized:
            self._screen_manager.size = self._background.norm_image_size
            self._screen_manager.pos = offset

    def get_dkey(self, key, x=None, y=None, z=None, w=None, t=None, u=None):
        # This is to get a ratio. All ratios will be designed at res 1706 x 960
        # This function will get the ratios for 1x and scale them up or down if needed

        dict_key, v = key.split(' ')
        d = self.ratios
        for k in dict_key.split('.'):
            d = d.get(k)
        if v == 'p_h':
            # print(d['p_h'])
            values = d['p_h']
            for key in values.keys():
                if not isinstance(values[key], float) and not isinstance(values[key], int):
                    values[key] = eval(values[key].format(x=x, y=y, z=z, w=w, t=t, u=u))
            return values
        elif v == 's' or v == 'p':
            return eval(d[v + '_x'].format(x=x, y=y, z=z, w=w, t=t, u=u)), eval(d[v + '_y'].format(x=x, y=y, z=z, w=w, t=t, u=u))
        else:
            return eval(d[v].format(x=x, y=y, z=z, w=w, t=t, u=u))


game = CoatiraneAdventures()
game.run()
sys.exit(0)
