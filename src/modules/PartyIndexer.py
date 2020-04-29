from src.modules.KivyBase.Hoverable import RelativeLayoutBase as RelativeLayout
from kivy.properties import ListProperty
from kivy.app import App


class PartyIndexer(RelativeLayout):
    sources = ListProperty(['../res/screens/buttons/party_full.png',
                            '../res/screens/buttons/party_empty.png',
                            '../res/screens/buttons/party_empty.png',
                            '../res/screens/buttons/party_empty.png',
                            '../res/screens/buttons/party_empty.png',
                            '../res/screens/buttons/party_empty.png',
                            '../res/screens/buttons/party_empty.png',
                            '../res/screens/buttons/party_empty.png',
                            '../res/screens/buttons/party_empty.png',
                            '../res/screens/buttons/party_empty.png'])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_sources()

    def update_sources(self):
        party_index = App.get_running_app().main.parties[0]
        for index in range(0, 10):
            self.sources[index] = '../res/screens/buttons/party_full.png' if party_index == index else '../res/screens/buttons/party_empty.png'
