__all__ = ('Builder',)

from kivy.lang import Builder as BaseBuilder
from kivy.logger import Logger


class Builder:
    _instance = None

    def __init__(self):
        self.loaded = []

    @staticmethod
    def load_file(filename):
        self = Builder
        if self._instance is None:
            self._instance = self()
        if filename in self._instance.loaded:
            return
        self._instance.loaded.append(filename)
        BaseBuilder.load_file(filename)
        Logger.info(f'SBuilder: loaded {filename}')
