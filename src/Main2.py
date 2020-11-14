import os
os.environ['KIVY_HOME'] = '../save/'

from kivy.loader import Loader
Loader.max_upload_per_frame = 3
Loader.num_workers = 8

from kivy.cache import Cache
Cache.register('kv.texture', 5000, 120)

from kivy.logger import Logger
Logger.info('Loader: using a thread pool of {} workers'.format(Loader.num_workers))
Logger.info('Loader: set max upload per frame to {}'.format(Loader.max_upload_per_frame))
from kivy.utils import platform
if platform == 'win':
    Logger.info('CoatiraneAdventures: running on windows')

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from src.loader import CALoader
from src.modules.KivyBase.Hoverable import GameBounds as Bounds

import math


class GameApp(App):
    title = 'Coatirane Adventures - Alpha 0.1'

    def __init__(self, *args, **kwargs):
        Window.bind(on_resize=self.on_resize)
        Window.bind(on_request_close=self.close_window)
        Window.bind(on_memorywarning=self.on_memory_warning)
        self.program_type = "test"
        self._size = (0, 0)
        self.ratios = None
        super().__init__(**kwargs)
        self.initialized = False

    def build(self):
        if platform == 'win':
            import ctypes
            user32 = ctypes.windll.user32
            width = math.floor(user32.GetSystemMetrics(0) * 2 / 3)
            height = math.floor(user32.GetSystemMetrics(1) * 2 / 3)
            App.get_running_app().width = width
            App.get_running_app().heught = height
            Window.size = width, height
            Window.left = math.floor((user32.GetSystemMetrics(0) - width) / 2)
            Window.top = math.floor((user32.GetSystemMetrics(1) - height) / 2)
            Window.borderless = 0
            # Window.grab_mouse()
        elif platform == 'android' or platform == 'ios':
            width, height = Window.size
        else:
            raise Exception("Running on unsupported Platform!")
        self._size = (width, height)
        self.background = Bounds(source="../res/screens/game_bounds.png", allow_stretch=True, size=(width, height))

        self.loader = CALoader(self.program_type)

        self.loader.loadBaseValues()
        self.loader.size = width, height

        self.background.add_widget(self.loader)
        return self.background

    def on_start(self, *args):
        Clock.schedule_once(self.loader.load_game, 5)

    def close_window(self, *args):
        if platform == 'win':
            Window.close()

    def on_memory_warning(self):
        self.main.clean_whitelist()

    def on_stop(self):
        # On IOS and Android, DO NOT programmically close; Let OS handle
        #Save game stuff
        print("Stop the App!")
        if platform == 'win':
            quit()

    def on_pause(self):
        if platform == 'win':
            return True
        else:
            #Save Game
            return True

    def on_resize(self, *args):
        Clock.unschedule(self.fix_size)
        Clock.schedule_once(self.fix_size, .25)

    def fix_size(self, *args):
        if not self.initialized or self._size == Window.size:
            return
        self._size = Window.size

        self.background.size = Window.size

        offset = Window.width/2 - self.background.norm_image_size[0]/2, Window.height/2 - self.background.norm_image_size[1]/2
        if self.main is not None:
            self.main.size = self.background.norm_image_size
            self.main.pos = offset

    def get_dkey(self, key, x=None, y=None, z=None, w=None, t=None, u=None):
        dict_key, v = key.split(' ')
        if self.ratios is None:
            self.ratios = self.loader.ratios
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


if __name__ == "__main__":
    game = GameApp()
    game.run()
