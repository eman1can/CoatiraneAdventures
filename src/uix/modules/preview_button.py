from time import time

from kivy.clock import Clock
from kivy.input.providers.wm_touch import WM_MotionEvent
from kivy.properties import NumericProperty
from kivy.uix.buttonversions import PPCHoverPathButton


class PreviewButton(PPCHoverPathButton):
    hold_time = NumericProperty(0.25)
    double_tap_time = NumericProperty(0.175)

    def __init__(self, **kwargs):
        self.register_event_type('on_right_click')
        self.register_event_type('on_left_click')
        self.register_event_type('on_hold')
        self._hold = None
        self._click_event = None
        super().__init__(**kwargs)

    def on_touch_down(self, touch):
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
        self._hold = Clock.schedule_once(lambda dt: self.hold(touch), self.hold_time)
        self.dispatch('on_press')
        return True

    def hold(self, touch):
        touch.ungrab(self)
        self.dispatch('on_hold')

    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            return False
        assert(self in touch.ud)
        touch.ungrab(self)
        self.last_touch = touch

        if not self.always_release and not self.collide_point(*touch.pos):
            self._do_release()
            return

        touch_time = time() - self.__touch_time
        if touch_time < self.min_state_time:
            self.__state_event = Clock.schedule_once(self._do_release, self.min_state_time - touch_time)
        else:
            self._do_release()
            if touch_time > self.hold_time:
                self.dispatch('on_hold')
                self.dispatch('on_release')
                return True
        self._hold.cancel()
        self.dispatch('on_release')
        if isinstance(touch, WM_MotionEvent) or touch.button == 'left':
            if self._click_event is None:
                self._click_event = Clock.schedule_once(lambda dt: self.do_left_click(), self.double_tap_time)
                return True
            else:
                self._click_event.cancel()
                self._click_event = None
                self.dispatch('on_right_click')
                return True
        if touch.button == 'right':
            self.dispatch('on_right_click')
        return True

    def do_left_click(self):
        self._click_event = None
        self.dispatch('on_left_click')

    def on_left_click(self):
        pass

    def on_right_click(self):
        pass

    def on_hold(self):
        pass
