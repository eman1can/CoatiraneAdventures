from kivy.properties import ListProperty, NumericProperty, StringProperty

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from uix.screens.intro.domain_display import SmallDomainDisplay


class CarouselWheel(FloatLayout):
    rows = NumericProperty(5)
    padding = NumericProperty(0)

    data = ListProperty([])

    view_class = StringProperty('Button')

    def __init__(self, **kwargs):
        self.register_event_type('on_widget')
        self._widget_height = 100
        self._widget_width = 100
        self._widget_offset = 25
        super().__init__(**kwargs)

        self._event = None
        self._next_animation = None
        self._in_animation = False
        self._duration = 0.5
        self._animations = {}
        self._touch_pos = 0, 0
        self.widgets = []
        self._dirty_widgets = []

    def on_height(self, *args):
        self._widget_height = (self.height - self.padding) / self.rows

    def on_padding(self, *args):
        self._widget_height = (self.height - self.padding) / self.rows
        self.refresh_widget_locations()

    def on_rows(self, *args):
        if self.rows % 2 == 0:
            self.rows += 1
        self._widget_height = self.height / self.rows
        self._widget_offset = (self.width - self._widget_width) / (self.rows - 1) / 2
        self.refresh_widget_locations()

    def on_width(self, *args):
        self._widget_width = self.width / 2
        self._widget_offset = (self.width - self._widget_width) / ((self.rows - 1) / 2)

    def on_pos(self, *args):
        self.refresh_widget_locations()

    def on_size(self, *args):
        self.refresh_widget_locations()

    def on_data(self, *args):
        if len(self.data) < self.rows:
            return
        for x in range(len(self.data)):
            widget = eval(self.view_class)(**self.data[x])
            widget.size_hint = None, None
            self.widgets.append(widget)
            self.add_widget(widget)
        self.refresh_widget_locations()

    def refresh_widget_locations(self):
        self.spots = []
        for index, widget in enumerate(self.widgets):
            widget.size = self._widget_width, self._widget_height
            # If the widget < half widgets
            if index < len(self.widgets) / 2:  # Go up and right 0-6
                x = self.x + self._widget_offset * index
                y = self.y + self.height / 2 - self._widget_height / 2 + self._widget_height * index
            else:  # index - len(self.widgets) -> -1 "up" and left
                x = self.x + self._widget_offset * abs(index - len(self.widgets))
                y = self.y + self.height / 2 - self._widget_height / 2 + self._widget_height * (index - len(self.widgets))
            widget.pos = x, y
            self.spots.append((x, y))

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return
        if self.disabled:
            return True
        if self._in_animation:
            return
        # Check a child for a on_touch_down, but only give it if on_touch move is not called
        self._event = None
        for widget in self.widgets:
            # touch.push()
            # touch.apply_transform_2d(self.to_local)
            if widget.collide_point(*touch.pos):
                self._event = Clock.schedule_once(lambda dt: self.on_child_touch(widget, touch), 0.02)
                break
            # touch.pop()
        touch.grab(self)
        if touch.is_mouse_scrolling:
            if self._event is not None:
                self._event.cancel()
            if self._in_animation:
                return
            if touch.button == 'scrolldown':
                self.widgets = self.widgets[-1:] + self.widgets[:-1]
            else:
                self.widgets = self.widgets[1:] + self.widgets[:1]
            self.animate()
            self._touch_pos = None
            return True
        self._touch_pos = touch.pos

    def on_child_touch(self, widget, touch):
        touch.ungrab(self)
        widget.on_touch_down(touch)

    def on_touch_move(self, touch):
        if not self.collide_point(*touch.pos):
            return
        if self is not touch.grab_current:
            return
        if self._in_animation:
            return
        if self._event is not None:
            self._event.cancel()
        diffx, diffy = self._touch_pos[0] - touch.x, self._touch_pos[1] - touch.y
        if abs(diffy) > self._widget_height:
            if diffy > 0:
                self.widgets = self.widgets[1:] + self.widgets[:1]
            else:
                self.widgets = self.widgets[-1:] + self.widgets[:-1]
            self._touch_pos = touch.pos
            return
        for index, widget in enumerate(self.widgets):
            start_x, start_y = self.spots[index]
            widget.y = start_y - diffy
            if 0 < index < len(self.widgets) / 2:
                widget.x = start_x - diffy * self._widget_offset / self._widget_height
            elif index == 0:
                if diffy > 0:
                    widget.x = start_x + diffy * self._widget_offset / self._widget_height
                else:
                    widget.x = start_x - diffy * self._widget_offset / self._widget_height
            else:
                widget.x = start_x + diffy * self._widget_offset / self._widget_height

    def on_touch_up(self, touch):
        if self._touch_pos is None:
            return
        if self is not touch.grab_current:
            return
        if self._in_animation:
            return
        if abs(self._touch_pos[1] - touch.y) > self._widget_height / 2:# or self._touch_pos[1] - touch.y > 0:
            if self._touch_pos[1] - touch.y < 0:
                self.widgets = self.widgets[-1:] + self.widgets[:-1]
            else:
                self.widgets = self.widgets[1:] + self.widgets[:1]
        self.animate()

    def anim_done(self, widget):
        if widget in self._animations:
            self._animations.pop(widget)
        if len(self._animations) == 0:
            self._in_animation = False
            if self._next_animation is not None:
                widget = self._next_animation
                self.goto_widget(widget)
                return
            self.dispatch('on_widget', self.widgets[0])

    def animate(self):
        if self._in_animation:
            return
        self._in_animation = True
        for index, widget in enumerate(self.widgets):
            opacity = 0.5
            if index == 0:
                opacity = 1
            if self._next_animation is None:
                anim = Animation(x=self.spots[index][0], y=self.spots[index][1], opacity=opacity, duration=self._duration, t='out_quad')
            else:
                anim = Animation(x=self.spots[index][0], y=self.spots[index][1], opacity=opacity, duration=self._duration / 2)
            anim.bind(on_complete=lambda a, w: self.anim_done(w))
            anim.start(widget)
            self._animations[widget] = anim

    def goto_widget(self, widget):
        index = self.widgets.index(widget)
        if index == 0:
            return
        if index > len(self.widgets) / 2:
            index -= len(self.widgets)
        if abs(index) > 1:
            self._next_animation = widget
            index -= int(index / abs(index))
        else:
            self._next_animation = None
        self.widgets = self.widgets[index:] + self.widgets[:index]
        self.animate()

    def on_widget(self, widget):
        pass
