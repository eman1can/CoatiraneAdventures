# Kivy Imports
from kivy.animation import Animation
from kivy.properties import DictProperty, ListProperty, NumericProperty, ObjectProperty
from kivy.uix.relativelayout import RelativeLayout

# KV Import
from loading.kv_loader import load_kv
load_kv(__name__)


class NavigationArrows(RelativeLayout):
    animation_first = ObjectProperty(None, allownone=True)
    animation_second = ObjectProperty(None, allownone=True)

    animate_distance = NumericProperty(100)

    animate_start_first = NumericProperty(5)
    animate_start_second = NumericProperty(95)

    arrow_sh = ListProperty([1, 1])
    arrow_first_ph = DictProperty({'x': 0, 'y': 0})
    arrow_second_ph = DictProperty({'x': 0, 'y': 0})

    animate_out_time = NumericProperty(1)
    animate_in_time = NumericProperty(0.25)

    animate_first_max_index = NumericProperty(-1)
    animate_second_max_index = NumericProperty(-1)

    def __init__(self, **kwargs):
        self.register_event_type('on_first')
        self.register_event_type('on_second')
        super().__init__(**kwargs)

    def on_arrow_touch(self, direction):
        if direction:
            self.dispatch('on_first')
        else:
            self.dispatch('on_second')

    def animate_arrows(self, index=-1):
        self.ensure_creation()
        if index == -1:
            self.animate_first()
            self.animate_second()
        else:
            if index > self.animate_first_max_index:
                self.animate_first()
            if index < self.animate_second_max_index:
                self.animate_second()

    def ensure_creation(self):
        pass

    def un_animate_first(self):
        if self.animation_first is None:
            return
        self.animation_first.cancel(self.ids.first_arrow)
        self.ids.first_arrow.disabled = True
        self.animation_first.repeat = False

    def animate_first(self):
        if self.animation_first is None:
            return
        self.ids.first_arrow.disabled = False
        self.animation_first.repeat = True
        self.animation_first.start(self.ids.first_arrow)

    def un_animate_second(self):
        if self.animation_second is None:
            return
        self.animation_second.cancel(self.ids.second_arrow)
        self.ids.second_arrow.disabled = True
        self.animation_second.repeat = False

    def animate_second(self):
        if self.animation_second is None:
            return
        self.ids.second_arrow.disabled = False
        self.animation_second.repeat = True
        self.animation_second.start(self.ids.second_arrow)

    def un_animate_arrows(self):
        self.un_animate_first()
        self.un_animate_second()

    def on_first(self):
        pass

    def on_second(self):
        pass


class LeftRightNavigationArrows(NavigationArrows):
    def __init__(self, **kwargs):
        self.register_event_type('on_left')
        self.register_event_type('on_right')
        super().__init__(**kwargs)

    def ensure_creation(self):
        if self.animation_first is None:
            # self.ids.first_arrow.disabled = True
            self.animation_first = Animation(x=self.animate_start_first - self.animate_distance, duration=self.animate_out_time) + Animation(x=self.animate_start_first, duration=self.animate_in_time)
        if self.animation_second is None:
            # self.ids.second_arrow.disabled = True
            self.animation_second = Animation(x=self.animate_start_second + self.animate_distance, duration=self.animate_out_time) + Animation(x=self.animate_start_second, duration=self.animate_in_time)

    def on_first(self, *args):
        self.dispatch('on_left')

    def on_left(self, *args):
        pass

    def on_second(self, *args):
        self.dispatch('on_right')

    def on_right(self, *args):
        pass


class UpDownNavigationArrows(NavigationArrows):
    def __init__(self, **kwargs):
        self.register_event_type('on_up')
        self.register_event_type('on_down')
        super().__init__(**kwargs)

    def ensure_creation(self):
        if self.animation_first is None:
            self.ids.first_arrow.disabled = True
            self.animation_first = Animation(y=self.animate_start_first - self.animate_distance, duration=self.animate_out_time) + Animation(y=self.animate_start_first, duration=self.animate_in_time)
        if self.animation_second is None:
            self.ids.second_arrow.disabled = True
            self.animation_second = Animation(y=self.animate_start_second + self.animate_distance, duration=self.animate_out_time) + Animation(y=self.animate_start_second, duration=self.animate_in_time)

    def on_first(self, *args):
        self.dispatch('on_up')

    def on_up(self):
        pass

    def on_second(self, *args):
        self.dispatch('on_down')

    def on_down(self):
        pass
