from kivy.properties import StringProperty

from loading.kv_loader import load_kv
from refs import Refs
from uix.modules.screen import Screen

load_kv(__name__)


class IntroNews(Screen):
    title = StringProperty('')
    description = StringProperty('')
    inspiration = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        chosen_char = Refs.gc.get_obtained_characters(False)[0]
        self.title = f'Welcome {Refs.gc.get_name()} to the town of Coatirane!'
        self.description = f'{chosen_char.get_name()} is excited to be a part of your budding family!' \
                           f'\nYou have decided to pool your money and have 3000 Varenth.' \
                           f' \nAdventure into the dungeon with {chosen_char.get_name()} to get more money!' \
                           f'\nYou talked to a friend and they have set you up in a small two room flat and paid the housing bills for 36 days.' \
                           f'\nIt will cost 50,000 Varenth to rent the two room flat for an additional 36 days after your current pay runs out.'
        self.inspiration = 'Good luck in your adventures!'

    def goto_next(self):
        Refs.gs.display_screen('town_main', True, False)
