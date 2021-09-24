__all__ = ('GAME_VERSION', 'PROGRAM_TYPE',)

from os import environ

base_path = environ['CA_PATH']
environ['KIVY_HOME'] = base_path + '/data/'

from kivy.config import Config
first_open = Config.get('kivy', 'first_open')

from kivy.loader import Loader
Loader.max_upload_per_frame = 3
Loader.num_workers = 8

from kivy.cache import Cache
Cache.register('kv.texture', 5000, 120)

from kivy.logger import Logger
Logger.info('Loader: using a thread pool of {} workers'.format(Loader.num_workers))
Logger.info('Loader: set max upload per frame to {}'.format(Loader.max_upload_per_frame))
# from kivy.utils import platform
if first_open == 'True':
    Config.set('kivy', 'first_open', False)
    Logger.info('CoatiraneAdventures: Detected first opening')

# if platform == 'win':
#     # Use ctypes to get resolution
#     import ctypes
#     GetSystemMetrics = ctypes.windll.user32.GetSystemMetrics
#     width, height = GetSystemMetrics(0), GetSystemMetrics(1)
# else:
#     raise Exception("Running on unsupported Platform!")

    # Logger.info('CoatiraneAdventures: Setting window size')
    # Config.set('graphics', 'screen_width', width)
    # Config.set('graphics', 'screen_height', height)
    # Config.set('graphics', 'width', int(width * 2 / 3))
    # Config.set('graphics', 'minimum_width', int(width * 2 / 6))
    # Config.set('graphics', 'height', int(height * 2 / 3))
    # Config.set('graphics', 'minimum_height', int(height * 2 / 6))
    # Config.write()

GAME_VERSION = Config.get('coatiraneadventures', 'version')
PROGRAM_TYPE = Config.get('coatiraneadventures', 'type')

from kivy.resources import resource_add_path
resource_add_path(base_path + '\\' + Config.get('paths', 'kv'))
resource_add_path(base_path + '\\' + Config.get('paths', 'font'))
resource_add_path(base_path + '\\' + Config.get('paths', 'icon'))
resource_add_path(base_path + '\\' + Config.get('paths', 'splash'))
resource_add_path(base_path + '\\' + Config.get('paths', 'sound'))
resource_add_path(base_path + '\\' + Config.get('paths', 'uix'))
resource_add_path(base_path + '\\' + Config.get('paths', 'characters'))
resource_add_path(base_path + '\\' + Config.get('paths', 'enemies'))
