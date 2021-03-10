# Project Imports
from modules.ca_gestures import left, right

# Kivy Libraries
from kivy.uix.widget import Widget
from kivy.graphics import Line
from kivy.properties import NumericProperty
from kivy.gesture import Gesture, GestureDatabase

# Standard Library Imports
import math


class GesturePad(Widget):
    minimum_x_distance = NumericProperty(0.0)
    minimum_y_distance = NumericProperty(0.0)

    def __init__(self, **kwargs):
        self.register_event_type('on_left')
        self.register_event_type('on_right')
        self.gdb = GestureDatabase()
        self.gdb.add_gesture(left)
        self.gdb.add_gesture(right)
        super().__init__(**kwargs)

    def simple_gesture(self, name, point_list):
        g = Gesture()
        g.add_stroke(point_list)
        g.normalize()
        g.name = name
        return g

    def on_touch_down(self, touch):
        touch.ud['start'] = (touch.x, touch.y)
        touch.ud['line'] = Line(points=(touch.x, touch.y))
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        try:
            touch.ud['line'].points += [touch.x, touch.y]
        except (KeyError) as e:
            pass
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if 'start' in touch.ud:
            if math.fabs(touch.x - touch.ud['start'][0]) <= self.minimum_x_distance:
                return super().on_touch_up(touch)
            if math.fabs(touch.y - touch.ud['start'][1]) <= self.minimum_y_distance:
                return super().on_touch_up(touch)
        else:
            return super().on_touch_up(touch)

        g = self.simple_gesture('', list(zip(touch.ud['line'].points[::2], touch.ud['line'].points[1::2])))
        # print("gesture representation:", self.gdb.gesture_to_str(g))
        # print("left:", g.get_score(left))
        # print("right:", g.get_score(right))
        g2 = self.gdb.find(g, minscore=0.70)
        if g2:
            if g2[1] == left:
                self.dispatch('on_left')
            if g2[1] == right:
                self.dispatch('on_right')
        return super().on_touch_up(touch)

    def on_left(self, *args):
        pass

    def on_right(self, *args):
        pass
