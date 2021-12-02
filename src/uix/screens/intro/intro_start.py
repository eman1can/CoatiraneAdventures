from kivy.properties import BooleanProperty, NumericProperty

from kivy.uix.behaviors import FocusBehavior
from kivy.uix.image import Image
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.togglebutton import ToggleButton
# KV Import
from loading.kv_loader import load_kv
from refs import Refs
from uix.modules.screen import Screen

load_kv(__name__)


class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior, RecycleGridLayout):
    pass


class FamilySymbol(RecycleDataViewBehavior, Image):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super().refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super().on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected
        rv.data[index]['selected'] = is_selected


class GenderButton(ToggleButton):
    pass


class IntroStart(Screen):
    symbol_options = NumericProperty(0)

    def __init__(self, save_slot, **kwargs):
        super().__init__(**kwargs)
        self.save_slot = save_slot
        self.symbol_options = 26

    def on_home_press(self):
        self.manager.display_screen('save_select', True, False)

    def on_symbol_options(self, *args):
        path = 'family/symbols/'
        self.ids.symbol_list.data = [{'id': f'symbol_{index}', 'source': f'{path}{index}.png'} for index in range(1, self.symbol_options+1)]
        self.ids.symbol_grid.select_with_touch(0, None)

    def check_valid(self):
        self.ids.next.disabled = not (len(self.ids.name_input.text) >= 4)

    def goto_next(self):
        name = self.ids.name_input.text.strip().title()
        symbol = None
        for symbol_data in self.ids.symbol_list.data:
            if symbol_data['selected']:
                symbol = symbol_data['id']
        gender = None
        if self.ids.male.state == 'down':
            gender = 'male'
        elif self.ids.female.state == 'down':
            gender = 'female'
        else:
            gender = 'neither'
        self.manager.display_screen('intro_domain', True, True, self.save_slot, name, gender, symbol)
        Refs.app._bind_keyboard()