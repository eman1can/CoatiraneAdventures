from kivy.properties import StringProperty
from loading.kv_loader import load_kv
from refs import Refs
from uix.modules.screen import Screen

load_kv(__name__)


class HousingMain(Screen):
    housing_source = StringProperty('')

    name = StringProperty('')
    description = StringProperty('')
    bill_description = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        housing = Refs.gc.get_housing()
        self.housing_source = housing.get_id() + '.png'
        self.name = housing.get_name()
        self.description = housing.get_description() + housing.get_info()
        if housing.get_bill_due() > 0:
            pass