from kivy.properties import BooleanProperty, ListProperty, NumericProperty, ObjectProperty, StringProperty

from game.floor import ENTRANCE, EXIT, SAFE_ZONES
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.togglebutton import ToggleButton
from loading.kv_loader import load_kv
from refs import Refs
from uix.popups.view import View

load_kv(__name__)


class SwitchButton(RelativeLayout):
    enabled_text = StringProperty('ON')
    disabled_text = StringProperty('OFF')

    enabled = BooleanProperty(True)

    def __init__(self, **kwargs):
        self.register_event_type('on_toggle')
        super().__init__(**kwargs)

    def toggle(self):
        self.enabled = not self.enabled
        self.dispatch('on_toggle', self.enabled)

    def on_toggle(self, enabled):
        pass


class CallbackButton(Button):
    callback = ObjectProperty(None, allownone=True)

    def on_release(self):
        if self.callback is not None:
            self.callback(self.text)


class LayerOption(RelativeLayout):
    layer_name = StringProperty('Unknown')
    enabled = BooleanProperty(True)
    callback = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enabled(self, instance, enabled):
        self.ids.button.enabled = self.enabled
        if self.callback is not None:
            self.callback(self.layer_name.replace(' ', '_').lower(), self.enabled)


class OptionList(RecycleView):
    def collide_point(self, x, y):
        if self.opacity == 0 or self.disabled:
            return False
        return super().collide_point(x, y)
        # print(x, y)
        # if self.opacity == 1:
        #     return self.x <= x <= self.right and self.y <= y <= self.top
        # else:
        #     return self.x <= x <= self.right and self.top - self.button_height <= y <= self.top


class SelectionButton(RelativeLayout):
    current_selection = StringProperty(None, allownone=True)
    options = ListProperty([])
    button_height = NumericProperty(100)

    def __init__(self, **kwargs):
        self.register_event_type('on_update')
        self.register_event_type('on_current_selection')
        super().__init__(**kwargs)

    def toggle(self):
        self.ids.options.opacity = 1 - self.ids.options.opacity
        self.ids.options.disabled = not self.ids.options.disabled

    def on_options(self, instance, options):
        self.refresh_options()

    def on_current_selection(self, instance, selection):
        self.refresh_options()

    def select(self, option):
        self.current_selection = option
        self.dispatch('on_update', self.current_selection)
        self.toggle()

    def on_update(self, selection):
        pass

    def refresh_options(self):
        data = []
        for option in self.options:
            if option == self.current_selection:
                continue
            data.append({'text': option, 'callback': self.select})
        self.ids.options.data = data
        self.ids.options.refresh_from_data()


class MapOptions(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        floor_map = Refs.gc.get_floor_data().get_floor().get_map()
        explored_nodes, explored_counters = floor_map.get_node_exploration()
        layers = []
        for layer, nodes in floor_map.get_markers().items():
            layer_title = layer.replace('_', ' ').title()
            layer_item = {'layer_name': layer_title, 'enabled': floor_map.layer_active(layer), 'callback': floor_map.set_layer_active}
            if layer in [ENTRANCE, EXIT, SAFE_ZONES]:
                layers.append(layer_item)
                continue
            for node in nodes:
                if explored_nodes[node]:
                    layers.append(layer_item)
                    break
        self.ids.layers.data = layers
        self.ids.layers.refresh_from_data()

        self.ids.map_enabled.enabled = floor_map.get_enabled()
        self.ids.map_enabled.bind(on_toggle=lambda i, enabled: floor_map.set_enabled(enabled))
        self.ids.path_enabled.enabled = floor_map.layer_active('path')
        self.ids.path_enabled.bind(on_toggle=lambda i, enabled: floor_map.set_layer_active('path', enabled))
        self.ids.map_radius.bind(on_update=lambda i, radius: floor_map.set_radius(int(radius)))
        self.ids.map_radius.current_selection = str(floor_map.get_radius())
        self.ids.map_radius.options = [str(x) for x in range(5, 10)]
        self.ids.map_destination.current_selection = floor_map.get_current_path().replace('_', ' ').title()
        self.ids.map_destination.options = [layer['layer_name'] for layer in layers]
        self.ids.map_destination.bind(on_update=lambda i, path: floor_map.set_current_path(path.replace(' ', '_').lower()))

    def on_pre_dismiss(self):
        self.manager.previous.refresh_map()
