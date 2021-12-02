from kivy.properties import BooleanProperty, NumericProperty, StringProperty

from game.housing import Housing
from loading.kv_loader import load_kv
from refs import Refs
from uix.modules.screen import Screen

load_kv(__name__)


class HousingMain(Screen):
    housing_source = StringProperty('')

    housing_name = StringProperty('')
    renting = BooleanProperty(False)
    description = StringProperty('')
    bill_description = StringProperty('')
    cost = StringProperty('')
    time = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        housing = Housing('two_room_flat', 'Two Room Flat', 'A small two room flat, with enough room for a living room and kitchen combo and a bedroom.', 2, [], [], 1000000)

        # housing = Refs.gc.get_housing()
        self.housing_source = f'housing/{housing.get_id()}.png'
        self.housing_name = housing.get_name()
        self.description = housing.get_description() + housing.get_info()
        self.renting = housing.is_renting()
        if housing.get_bill_count() > 0:
            self.cost = 'Next Bill: ' + Refs.gc.format_number(housing.get_bill_cost())
            if housing.get_bill_due() > 0:
                self.time = f'Bill due in {housing.get_bill_due()} days'
            elif housing.get_bill_due() < 0:
                self.time = f'Bill due {housing.get_bill_due()} days ago'
            else:
                self.time = f'Bill due today'
        else:
            self.cost = 'Paid Off'
            self.time = f''

