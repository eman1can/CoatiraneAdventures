from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView


class ScrollPanel(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.smooth_scroll_end = 15

    def on_scroll_start(self, touch, check_children=True):
        # Makes Scrolling up and down into left and right
        if check_children:
            touch.push()
            touch.apply_transform_2d(self.to_local)
            if self.dispatch_children('on_scroll_start', touch):
                touch.pop()
                return True
            touch.pop()

        if not self.collide_point(*touch.pos):
            touch.ud[self._get_uid('svavoid')] = True
            return
        if self.disabled:
            return True
        if self._touch or (not (self.do_scroll_x or self.do_scroll_y)):
            return self.simulate_touch_down(touch)

        # handle mouse scrolling, only if the viewport size is bigger than the
        # scrollview size, and if the user allowed to do it
        vp = self._viewport
        if not vp:
            return True
        scroll_type = self.scroll_type
        ud = touch.ud
        scroll_bar = 'bars' in scroll_type

        # check if touch is in bar_x(horizontal) or bar_y(vertical)
        width_scrollable = vp.width > self.width
        height_scrollable = vp.height > self.height

        d = {'bottom': touch.y - self.y - self.bar_margin,
             'top': self.top - touch.y - self.bar_margin,
             'left': touch.x - self.x - self.bar_margin,
             'right': self.right - touch.x - self.bar_margin}

        ud['in_bar_x'] = (scroll_bar and width_scrollable and
                          (0 <= d[self.bar_pos_x] <= self.bar_width))
        ud['in_bar_y'] = (scroll_bar and height_scrollable and
                          (0 <= d[self.bar_pos_y] <= self.bar_width))

        if vp and 'button' in touch.profile and touch.button.startswith('scroll'):
            btn = touch.button
            m = self.scroll_wheel_distance
            e = None

            if self.do_scroll_x:
                if ((btn in ('scrolldown', 'scrollleft') and self.scroll_x <= 0) or
                        (btn in ('scrollup', 'scrollright') and self.scroll_x >= 1)):
                    return False
                if self.effect_y and width_scrollable:
                    e = self.effect_y if ud['in_bar_y'] else self.effect_x
                if e:
                    if btn in ('scrollup', 'scrollleft'):
                        if self.smooth_scroll_end:
                            e.velocity -= m * self.smooth_scroll_end
                        else:
                            e.value = max(e.value - m, e.min)
                            e.velocity = 0
                    elif btn in ('scrolldown', 'scrollright'):
                        if self.smooth_scroll_end:
                            e.velocity += m * self.smooth_scroll_end
                        else:
                            e.value = min(e.value + m, e.max)
                            e.velocity = 0
                    touch.ud[self._get_uid('svavoid')] = True
                    e.trigger_velocity_update()
            elif self.do_scroll_y:
                if ((btn in ('scrolldown', 'scrollleft') and self.scroll_y <= 0) or
                  (btn in ('scrollup', 'scrollright') and self.scroll_y >= 1)):
                    return False
                if self.effect_x and height_scrollable:
                    e = self.effect_x if ud['in_bar_x'] else self.effect_y
                if e:
                    if btn in ('scrolldown', 'scrollleft'):
                        if self.smooth_scroll_end:
                            e.velocity -= m * self.smooth_scroll_end
                        else:
                            e.value = max(e.value - m, e.min)
                            e.velocity = 0
                    elif btn in ('scrollup', 'scrollright'):
                        if self.smooth_scroll_end:
                            e.velocity += m * self.smooth_scroll_end
                        else:
                            e.value = min(e.value + m, e.max)
                            e.velocity = 0
                    touch.ud[self._get_uid('svavoid')] = True
                    e.trigger_velocity_update()
            return True

        in_bar = ud['in_bar_x'] or ud['in_bar_y']
        if scroll_type == ['bars'] and not in_bar:
            return self.simulate_touch_down(touch)

        if in_bar:
            if ud['in_bar_y'] and not self._touch_in_handle(self._handle_y_pos, self._handle_y_size, touch):
                self.scroll_y = (touch.y - self.y) / self.height
            elif ud['in_bar_x'] and not self._touch_in_handle(self._handle_x_pos, self._handle_x_size, touch):
                self.scroll_x = (touch.x - self.x) / self.width

        # no mouse scrolling, so the user is going to drag the scrollview with
        # this touch.
        self._touch = touch
        uid = self._get_uid()

        ud[uid] = {
            'mode': 'unknown',
            'dx': 0,
            'dy': 0,
            'user_stopped': in_bar,
            'frames': Clock.frames,
            'time': touch.time_start}

        if self.do_scroll_x and self.effect_x and not ud['in_bar_x']:
            self._effect_x_start_width = self.width
            self.effect_x.start(touch.x)
            self._scroll_x_mouse = self.scroll_x
        if self.do_scroll_y and self.effect_y and not ud['in_bar_y']:
            self._effect_y_start_height = self.height
            self.effect_y.start(touch.y)
            self._scroll_y_mouse = self.scroll_y

        if not in_bar:
            Clock.schedule_once(self._change_touch_mode,
                                self.scroll_timeout / 1000.)
        return True
