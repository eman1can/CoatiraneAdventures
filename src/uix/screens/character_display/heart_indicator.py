# Kivy Imports
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import NumericProperty, BooleanProperty, OptionProperty

# KV Import
from loading.kv_loader import load_kv
load_kv(__name__)


class HeartIndicator(RelativeLayout):
    is_visible = BooleanProperty(False)
    familiarity = NumericProperty(0.0)
    familiarity_gold = NumericProperty(0.0)

    how_opened = OptionProperty('Closed', options=['Closed', 'Hover', 'Button'])

    def __init__(self, **kwargs):
        self.register_event_type('on_hint_open')
        self.register_event_type('on_hint_close')
        super().__init__(**kwargs)

    def on_mouse_pos(self, hover):
        return self.ids.button.dispatch('on_mouse_pos', hover)

    def on_touch_down(self, touch):
        if self.disabled:
            return False
        if not self.collide_point(*touch.pos):
            return False
        touch.push()
        touch.apply_transform_2d(self.to_local)

        for child in self.children[:]:
            if child.on_touch_down(touch):
                touch.pop()
                return True
        touch.pop()
        return False

    def toggle_hint(self):
        if self.opacity > 0:
            if self.how_opened == 'Hover':
                self.how_opened = 'Button'
                return
            if self.how_opened == 'Closed':
                self.dispatch('on_hint_open')
                self.how_opened = 'Button'
            else:
                self.dispatch('on_hint_close')
                self.how_opened = 'Closed'

    def show_hint(self):
        if self.opacity > 0:
            print(self.how_opened)
            if self.how_opened == 'Closed':
                self.dispatch('on_hint_open')
                self.how_opened = 'Hover'

    def hide_hint(self):
        if self.opacity > 0:
            if self.how_opened == 'Hover':
                self.dispatch('on_hint_close')
                self.how_opened = 'Closed'

    def reset_open(self):
        self.how_opened = 'Closed'

    def on_hint_open(self):
        pass

    def on_hint_close(self):
        pass
