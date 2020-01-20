from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.properties import BooleanProperty, NumericProperty, ReferenceListProperty, StringProperty, ListProperty, OptionProperty, ObjectProperty
from kivy.graphics import PushMatrix, PopMatrix, Rotate

from time import time


class HTButton(Widget):
    initialized = BooleanProperty(False)

    # Label Properties
    text = StringProperty('')
    font_size = NumericProperty(0.0)
    font_name = StringProperty(Config.get('graphics', 'default_font'))
    label_padding = ListProperty([0, 0, 0, 0])
    label_color = ListProperty([0, 0, 0, 1])

    # Hover Properties
    hovered = BooleanProperty(False)
    do_hover = BooleanProperty(True)
    hover_rect = ListProperty([0, 0, 0, 0])
    _static_hover = BooleanProperty(False)

    # Toggle Properties
    toggle_enabled = BooleanProperty(False)
    toggle_state = BooleanProperty(False)

    # Button Properties
    angle = NumericProperty(0.0)
    allow_stretch = BooleanProperty(True)

    state = OptionProperty('normal', options=('normal', 'down', 'hover_normal', 'hover_down'))
    last_touch = ObjectProperty(None)
    min_state_time = NumericProperty(0)
    always_release = BooleanProperty(False)

    path = StringProperty('')
    collide_image = StringProperty('')
    background_normal = StringProperty('')
    background_disabled_normal = StringProperty('')
    background_down = StringProperty('')
    background_disabled_down = StringProperty('')
    background_hover = StringProperty('')
    background_hover_down = StringProperty('')

    def __init__(self, **kwargs):
        self.register_event_type('on_press')
        self.register_event_type('on_release')
        self.register_event_type('on_toggle_down')
        self.register_event_type('on_toggle_up')

        if 'min_state_time' not in kwargs:
            self.min_state_time = float(Config.get('graphics', 'min_state_time'))
        Window.bind(mouse_pos=self.on_mouse_pos)
        super().__init__(**kwargs)

        self._size = (0, 0)
        self._pos = (-1, -1)

        self.rotate = Rotate(angle=self.angle)

        if self.hover_rect != [0, 0, 0, 0]:
            self._static_hover = True

        if self.collide_image == '':
            self.collide_image = self.path + ".collision.png"
        if self.background_normal == '':
            self.background_normal = self.path + ".normal.png"
        if self.background_down == '':
            self.background_down = self.path + ".down.png"
        if self.background_hover == '':
            self.background_hover = self.path + ".hover.png"
        if self.background_hover_down == '':
            self.background_hover_down = self.path + '.hover.down.png'
        if self.background_disabled_normal == '':
            self.background_disabled_normal = self.path + '.disabled.normal.png'
        if self.background_disabled_down == '':
            self.background_disabled_down = self.path + '.disabled.down.png'

        self.disabled = False

        self._collide_image = Image(source=self.collide_image, keep_data=True)._coreimage
        self.image = Image(source=self.background_normal, allow_stretch=self.allow_stretch)
        self.label = Label(text=self.text, font_size=self.font_size, font_name=self.font_name, color=self.label_color, size_hint=(None, None))

        self.add_widget(self.image)
        self.add_widget(self.label)
        if self.toggle_enabled and self.toggle_state:
            self.state = 'down'
        self.initialized = True

    # def update_canvas(self, *args):
    #     self.rotate.origin = self.center

    def on_size(self, instance, size):
        if not self.initialized or self._size == size:
            return
        self._size = size.copy()

        self.image.size = self.size
        if not self._static_hover:
            self.hover_rect[2] = self.width
            self.hover_rect[3] = self.height
        self.label.size = self.width - self.label_padding[0] - self.label_padding[2], self.height - self.label_padding[1] - self.label_padding[3]
        self.label.pos = self.x + self.label_padding[0], self.y + self.label_padding[3]

    def on_pos(self, instance, pos):
        if not self.initialized or self._pos == pos:
            return
        self._pos = pos.copy()

        self.on_mouse_pos(instance, pos)

        self.image.pos = self.pos
        if not self._static_hover:
            self.hover_rect[0] = self.x
            self.hover_rect[1] = self.y
        self.label.pos = self.x + self.label_padding[0], self.y + self.label_padding[3]

    def collide_point(self, x, y):
        if self.x <= x <= self.right and self.y <= y <= self.top:
            scale = (self._collide_image.width / (self.right - self.x))
            try:
                color = self._collide_image.read_pixel((x - self.x) * scale, (self.height - (y - self.y)) * scale)
            except:
                color = 0, 0, 0, 0
            if color[-1] > 0:
                return True
        return False

    def on_state(self, instance, state):
        if state == 'normal':
            if not self.disabled:
                self.image.source = self.background_normal
            else:
                self.image.source = self.background_disabled_normal
        elif state == 'down':
            if not self.disabled:
                self.image.source = self.background_down
            else:
                self.image.source = self.background_disabled_normal
        elif state == 'hover_normal':
            self.image.source = self.background_hover
        elif state == 'hover_down':
            self.image.source = self.background_hover_down

    def on_disabled(self, instance, disabled):
        if self.state == 'hover_normal' or self.state == 'hover_down':
            raise Exception("Change ya timing dude!")
        else:
            if self.state == 'normal':
                self.image.source = self.background_disabled_normal if self.disabled else self.background_normal
            else:
                self.image.source = self.background_disabled_down if self.disabled else self.background_down

    def on_mouse_pos(self, instance, pos):
        if not self.get_root_window() or not self.do_hover:
            return
        # do proceed if I'm not displayed <=> If have no parent
        x, y = pos if self._static_hover else self.to_widget(*pos)
        inside = self.collide_point(*self.to_widget(*pos))
        inside &= self.hover_rect[0] <= x <= self.hover_rect[0] + self.hover_rect[2] \
             and self.hover_rect[1] <= y <= self.hover_rect[1] + self.hover_rect[3]
        if self.hovered == inside or self.disabled:
            return
        self.hovered = inside

        if not inside and self.state.startswith('hover'):
            self.state = self.state[6:]
        elif inside and not self.state.startswith('hover'):
            self.state = 'hover_' + self.state

    def _do_press(self):
        if self.toggle_enabled:
            self.toggle_state = not self.toggle_state
            if not self.state.startswith('hover'):
                self.state = 'down' if self.toggle_state else 'normal'
            else:
                if self.do_hover:
                    self.state = 'hover_down' if self.toggle_state else 'hover_normal'
        else:
            self.state = 'down'

    def _do_release(self, *args):
        if not self.toggle_enabled:
            self.state = 'normal'

    def cancel_event(self, *args):
        if self.__state_event:
            self.__state_event.cancel()
            self.__state_event = None

    def on_touch_down(self, touch):
        if 'button' in touch.profile and touch.button.startswith('scroll'):
            return False
        if super().on_touch_down(touch):
            return True
        if self.disabled:
            return False
        if touch.is_mouse_scrolling:
            return False
        if not self.collide_point(touch.x, touch.y):
            return False
        if self in touch.ud:
            return False
        touch.grab(self)
        touch.ud[self] = True
        self.last_touch = touch
        self.__touch_time = time()
        self._do_press()
        self.dispatch('on_press')
        return True

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            return True
        if super().on_touch_move(touch):
            return True
        return self in touch.ud

    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            return super().on_touch_up(touch)
        assert(self in touch.ud)
        touch.ungrab(self)
        self.last_touch = touch

        if (not self.always_release and not self.collide_point(*touch.pos)):
            self._do_release()
            return

        touchtime = time() - self.__touch_time
        if touchtime < self.min_state_time:
            self.__state_event = Clock.schedule_once(self._do_release, self.min_state_time - touchtime)
        else:
            self._do_release()
        self.dispatch('on_release')
        if self.toggle_enabled:
            if self.toggle_state:
                self.dispatch('on_toggle_down')
            else:
                self.dispatch('on_toggle_up')
        return True

    def on_press(self):
        pass

    def on_release(self):
        pass

    def on_toggle_down(self):
        pass

    def on_toggle_up(self):
        pass

    def trigger_action(self, duration=0.1):
        '''Trigger whatever action(s) have been bound to the button by calling
        both the on_press and on_release callbacks.

        This simulates a quick button press without using any touch events.

        Duration is the length of the press in seconds. Pass 0 if you want
        the action to happen instantly.

        .. versionadded:: 1.8.0
        '''
        self._do_press()
        self.dispatch('on_press')

        def trigger_release(dt):
            self._do_release()
            self.dispatch('on_release')
        if not duration:
            trigger_release(0)
        else:
            Clock.schedule_once(trigger_release, duration)

    # Label Events
    def on_text(self, instance, text):
        if not self.initialized:
            return

        self.label.text = self.text

    def on_font_name(self, instance, font_name):
        if not self.initialized:
            return

        self.label.font_name = self.font_name

    def on_font_size(self, instance, font_size):
        if not self.initialized:
            return

        self.label.font_size = self.font_size

    def on_label_color(self, instance, label_color):
        if not self.initialized:
            return

        self.label.color = self.label_color

    def on_label_padding(self, instance, label_padding):
        if not self.initialized:
            return

        self.label.size = self.width - self.label_padding[0] - self.label_padding[2], self.height - self.label_padding[1] - self.label_padding[3]
        self.label.pos = self.x + self.label_padding[0], self.y + self.label_padding[3]