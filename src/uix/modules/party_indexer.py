# Kivy Imports
from kivy.properties import ListProperty

from kivy.uix.relativelayout import RelativeLayout
# KV Import
from loading.kv_loader import load_kv

load_kv(__name__)

FULL_PATH = 'buttons/party_full.png'
EMPTY_PATH = 'buttons/party_empty.png'


class PartyIndexer(RelativeLayout):
    sources = ListProperty([FULL_PATH,
                            EMPTY_PATH,
                            EMPTY_PATH,
                            EMPTY_PATH,
                            EMPTY_PATH,
                            EMPTY_PATH,
                            EMPTY_PATH,
                            EMPTY_PATH,
                            EMPTY_PATH,
                            EMPTY_PATH])

    def __init__(self, **kwargs):
        self.register_event_type('on_click')
        super().__init__(**kwargs)

    def update_sources(self, party_index):
        for index in range(0, 10):
            self.sources[index] = FULL_PATH if party_index == index else EMPTY_PATH

    def on_click(self, index):
        pass