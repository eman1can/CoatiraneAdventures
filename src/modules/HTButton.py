import weakref
from time import time
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.image import Image
from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty, NumericProperty, StringProperty, ListProperty, OptionProperty, ObjectProperty

from src.modules.KivyBase.Hoverable import HoverBehaviour


class HTButton(HoverBehaviour, Widget):
    initialized = BooleanProperty(False)

    # Label Properties
    text = StringProperty('')
    font_size = NumericProperty(0.0)
    font_name = StringProperty(Config.get('graphics', 'default_font'))
    label_padding = ListProperty([0, 0, 0, 0])
    label_color = ListProperty([0, 0, 0, 1])
    label_halign = StringProperty('left')
    label_valign = StringProperty('middle')

    # Hover Properties
    hovered = BooleanProperty(False)
    do_hover = BooleanProperty(True)
    hover_rect = ListProperty([0, 0, 0, 0])
    _static_hover = BooleanProperty(False)

    # Toggle Properties
    toggle_enabled = BooleanProperty(False)
    toggle_state = BooleanProperty(False)

    # Button Properties
    texture = ObjectProperty(None, allownone=True)
    state = OptionProperty('normal', options=('normal', 'down', 'hover_normal', 'hover_down'))
    last_touch = ObjectProperty(None)
    min_state_time = NumericProperty(0)
    always_release = BooleanProperty(False)

    path_set = BooleanProperty(False)
    path = StringProperty('')
    collide_image = StringProperty('')
    background_normal = StringProperty('')
    background_disabled_normal = StringProperty('')
    background_down = StringProperty('')
    background_disabled_down = StringProperty('')
    background_hover = StringProperty('')
    background_hover_down = StringProperty('')

    background_normal_texture = ObjectProperty(None)
    background_disabled_normal_texture = ObjectProperty(None)
    background_down_texture = ObjectProperty(None)
    background_disabled_down_texture = ObjectProperty(None)
    background_hover_texture = ObjectProperty(None)
    background_hover_down_texture = ObjectProperty(None)

    def __init__(self, **kwargs):
        self.register_event_type('on_press')
        self.register_event_type('on_release')
        self.register_event_type('on_toggle_down')
        self.register_event_type('on_toggle_up')
        self.register_event_type('on_hover_enter')
        self.register_event_type('on_hover_exit')

        if 'min_state_time' not in kwargs:
            self.min_state_time = float(Config.get('graphics', 'min_state_time'))
        self._collide_image = None
        self.theoretical_children = None
        super().__init__(**kwargs)

    def on_toggle_enabled(self, instance, value):
        if self.toggle_state:
            self.state = 'down'

    def on_toggle_state(self, instance,  value):
        if value is not None:
            if self.state.startswith('hover_'):
                if self.state == 'hover_normal':
                    self.state = 'hover_down'
                else:
                    self.state = 'hover_normal'
            elif self.state == 'normal':
                self.state = 'down'
            else:
                self.state = 'normal'

        else:
            self.state = 'normal'

    def on_path(self, instance, path):
        if not self.path_set:
            self.path_set = True
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
        else:
            if self.collide_image != '':
                self.collide_image = self.path + ".collision.png"
            if self.background_normal != '':
                self.background_normal = self.path + ".normal.png"
            if self.background_down != '':
                self.background_down = self.path + ".down.png"
            if self.background_hover != '':
                self.background_hover = self.path + ".hover.png"
            if self.background_hover_down != '':
                self.background_hover_down = self.path + '.hover.down.png'
            if self.background_disabled_normal != '':
                self.background_disabled_normal = self.path + '.disabled.normal.png'
            if self.background_disabled_down != '':
                self.background_disabled_down = self.path + '.disabled.down.png'

    def on_collide_image(self, instance, collide_image):
        if self.collide_image != '' and self.collide_image is not None:
            try:
                self._collide_image = Image(self.collide_image)
            except:
                self._collide_image = None

    def on_background_normal(self, instance, value):
        if self.background_normal != '':
            self.texture = Image(self.background_normal).texture

    def on_hover_rect(self, instance, value):
        if self.hover_rect != [self.x, self.y, self.width, self.height]:
            self._static_hover = True

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
        old_texture = self.texture
        try:
            if state == 'normal':
                if not self.disabled:
                    if self.background_normal_texture is None:
                        self.background_normal_texture = Image(self.background_normal).texture
                    self.texture = self.background_normal_texture
                else:
                    if self.background_disabled_normal_texture is None:
                        self.background_disabled_normal_texture = Image(self.background_disabled_normal).texture
                    self.texture = self.background_disabled_normal_texture
            elif state == 'down':
                if not self.disabled:
                    if self.background_down_texture is None:
                        self.background_down_texture = Image(self.background_down).texture
                    self.texture = self.background_down_texture
                else:
                    if self.background_disabled_down_texture is None:
                        self.background_disabled_down_texture = Image(self.background_disabled_down).texture
                    self.texture = self.background_disabled_down_texture
            elif state == 'hover_normal':
                if self.background_hover_texture is None:
                    self.background_hover_texture = Image(self.background_hover).texture
                self.texture = self.background_hover_texture
            elif state == 'hover_down':
                if self.background_hover_down_texture is None:
                    self.background_hover_down_texture = Image(self.background_hover_down).texture
                self.texture = self.background_hover_down_texture
        except:
            self.texture = old_texture

    def on_disabled(self, instance, disabled):
        if not self.initialized:
            return
        if self.state == 'hover_normal' or self.state == 'hover_down':
            raise Exception("Change ya timing dude!")
        else:
            if self.state == 'normal':
                self.texture = Image(self.background_disabled_normal).texture if self.disabled else Image(self.background_normal).texture
            else:
                self.texture = Image(self.background_disabled_down).texture if self.disabled else Image(self.background_down).texture

    def _do_press(self):
        if not self.toggle_enabled:
                self.state = 'down'
        else:
            self.toggle_state = not self.toggle_state

    def _do_release(self, *args):
        if not self.toggle_enabled:
            self.state = 'normal'

    def cancel_event(self, *args):
        if self.__state_event:
            self.__state_event.cancel()
            self.__state_event = None

    def on_touch_down(self, touch):
        if super().on_touch_down(touch):
            return True
        if touch.is_mouse_scrolling:
            return False
        if not self.collide_point(touch.x, touch.y):
            return False
        if self in touch.ud:
            return False
        if self.disabled:
            return False
        if 'button' in touch.profile and touch.button.startswith('scroll'):
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

    def on_touch_hover(self, touch):
        if touch.grab_current is not None:
            if touch.grab_current == self:
                if self.collide_point(*touch.pos):
                    if self.hover_rect[0] <= touch.x <= self.hover_rect[0] + self.hover_rect[2] and self.hover_rect[1] <= touch.y <= self.hover_rect[1] + self.hover_rect[3]:
                        if len(touch.grab_list) == 1:
                            return True
                self.dispatch('on_hover_exit')
                touch.ungrab(self)
                if self.state.startswith('hover_'):
                    self.state = self.state[6:]
        else:
            if self.disabled:
                return False

            if not self.do_hover:
                return False

            if self.collide_point(*touch.pos):
                if self.hover_rect[0] <= touch.x <= self.hover_rect[0] + self.hover_rect[2] and self.hover_rect[1] <= touch.y <= self.hover_rect[1] + self.hover_rect[3]:
                    if not self.state.startswith('hover_'):
                        self.state = 'hover_' + self.state
                    class_instance = weakref.ref(self.__self__)
                    if class_instance not in touch.grab_list:
                        self.dispatch('on_hover_enter')
                        touch.grab(self)
                    return True
        return False

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

    def on_hover_enter(self):
        pass

    def on_hover_exit(self):
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