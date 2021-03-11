# Project Imports
from kivy.resources import resource_find
from modules.builder import Builder


def load_kv(module):
    Builder.load_file(resource_find(module.replace('.', '/') + '.kv'))
