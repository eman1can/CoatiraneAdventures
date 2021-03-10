# Project Imports
from modules.builder import Builder


def load_kv(module):
    # kv_path = 'uix/' + module[4:].replace('.', '/') + '.kv'
    Builder.load_file(module.replace('.', '/') + '.kv')
