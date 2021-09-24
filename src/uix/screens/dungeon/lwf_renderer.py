from os import getcwd

from kivy.cache import Cache
from kivy.core.image import Image

from lwf.format.data import Data
from lwf.lwf import LWF
from lwf.renderer import RendererFactory
from refs import Refs


def load_texture(filename, path):
    try:
        return Image(f'{path}{filename}').texture
    except AttributeError:
        Refs.log(f'Not found <{path}{filename}>', 'error')


class LWFRenderer:
    def __init__(self, canvas):
        self._canvas = canvas

        self._texture_handlers = {}
        self._factory = RendererFactory(self._canvas, '', self.load_texture)

        self._lwfs = {}
        self._paths = {}
        self._destroy = []
        self._debug = False

        Cache.register('lwf_data', 10, 120)

    def register_lwf(self, lwf_name, lwf_specific_name, texture_handler):
        self._texture_handlers[lwf_specific_name] = texture_handler

        if self._debug:
            Refs.log(f'Create {lwf_specific_name}', tag='LwfRenderer')

        data = Cache.get('lwf_data', lwf_name)
        if data is None:
            lwf_name = 'res/lwf/' + lwf_name
            path = lwf_name[:lwf_name.rindex('/') + 1]
            self._paths[lwf_specific_name] = path
            data = Data(lwf_name)
            Cache.append('lwf_data', lwf_name, data)
        lwf = LWF(data, self._factory, lwf_specific_name)
        self._lwfs[lwf_specific_name] = lwf
        return lwf

    def destroy_lwf(self, lwf_specific_name):
        if self._debug:
            Refs.log(f'Flag to destroy {lwf_specific_name}', tag='LwfRenderer')
        self._destroy.append(lwf_specific_name)

    def get_lwf(self, lwf_specific_name):
        if lwf_specific_name in self._lwfs:
            return self._lwfs[lwf_specific_name]
        return None

    def load_texture(self, filename, lwf_name):
        return self._texture_handlers[lwf_name](filename, self._paths[lwf_name])

    def update(self, dt):
        self._canvas.canvas.clear()
        for lwf in list(self._lwfs.values()):
            if lwf.visible:
                lwf.exec(dt)
                lwf.render()
        for lwf_name in self._destroy:
            lwf = self._lwfs.pop(lwf_name)
            self._paths.pop(lwf_name)
            if self._debug:
                Refs.log(f'Destroy {lwf_name}', tag='LwfRenderer')
            lwf.destroy()
        self._destroy.clear()
