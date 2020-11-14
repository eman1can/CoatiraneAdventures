from kivy.app import App
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Color as KivyColor, Rectangle
from kivy.clock import Clock


Builder.load_string('''
<RV>:
    bar_width: dp(20)
    viewclass: 'MyLabel'
    MyBoxLayout:
        id: layout
        default_size: dp(30), None
        default_size_hint: None, 1
        size_hint_x: None
        width: self.minimum_width
        orientation: 'horizontal'
        spacing: 30
        padding: 20, 20
<Base>:
    canvas:
        Color:
            rgba: 0, 1, 0, 0.5
        Rectangle:
            size: self.size
            pos: self.pos
    RelativeLayout:
        size: self.parent.size
        Image:
            source: '../res/screens/backgrounds/background.png'
            allow_stretch: True
            keep_ratio: False
            size_hint: 1, 1
        Button:
            size_hint: 1, 0.2
            text: 'Push Me!'
            pos_hint: {'center_x': 0.5, 'top': 1}
            on_release: recycle.sort_me()
        RV:
            id: recycle
            size_hint: 1, 0.8
<MyLabel>:
    color: 1, 0, 0, 1
    canvas:
        Color: 
            rgba: 0, 0, 0.5, 0.4
        Rectangle:
            size: self.size
            pos: self.pos
''')


class RV(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = [{'id': str(x), 'text': str(x)} for x in range(100)]
        self.sorted = 0

    def on_scroll_start(self, touch, check_children=True):
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

        if vp and 'button' in touch.profile and \
                touch.button.startswith('scroll'):
            btn = touch.button
            m = self.scroll_wheel_distance
            e = None

            if ((btn == 'scrolldown' and self.scroll_x >= 1) or (btn == 'scrollup' and self.scroll_x <= 0) or (btn == 'scrollleft' and self.scroll_x >= 1) or (btn == 'scrollright' and self.scroll_x <= 0)):
                return False

            if (self.effect_x and self.do_scroll_y and height_scrollable and
                    btn in ('scrolldown', 'scrollup')):
                e = self.effect_x if ud['in_bar_x'] else self.effect_y

            elif (self.effect_y and self.do_scroll_x and width_scrollable and
                    btn in ('scrollleft', 'scrollright', 'scrollup', 'scrolldown')):
                e = self.effect_y if ud['in_bar_y'] else self.effect_x

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
            if (ud['in_bar_y'] and not
                    self._touch_in_handle(
                        self._handle_y_pos, self._handle_y_size, touch)):
                self.scroll_y = (touch.y - self.y) / self.height
            elif (ud['in_bar_x'] and not
                    self._touch_in_handle(
                        self._handle_x_pos, self._handle_x_size, touch)):
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

    def sort_me(self):
        item = self.data[self.sorted]
        self.sorted += 1
        if self.sorted < len(self.data):
            self.data[self.sorted - 1] = self.data[self.sorted]
            self.data[self.sorted] = item

class MyBoxLayout(RecycleBoxLayout):
    def get_size(self):
        return len(self.children)


class MyLabel(Label):
    pass


class Base(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class TestApp(App):
    def build(self):
        return Base()


if __name__ == '__main__':
    TestApp().run()
