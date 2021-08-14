# Project Imports
from kivy.resources import resource_find
from modules.builder import Builder


def load_kv(module):
    try:
        Builder.load_file(resource_find(module.replace('.', '/') + '.kv'))
    except TypeError as e:
        print('Failed to load kv file.', module.replace('.', '/') + '.kv')
        raise Exception('Failed to load kv file.')
