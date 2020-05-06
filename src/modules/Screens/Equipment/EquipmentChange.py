from kivy.animation import Animation

from src.modules.KivyBase.Hoverable import ScreenBase as Screen, GridLayoutBase as GridLayout, RelativeLayoutBase as RelativeLayout
from kivy.properties import ObjectProperty, NumericProperty
from kivy.app import App

from kivy.graphics import Line
from kivy.gesture import Gesture, GestureDatabase
from src.modules.ca_gestures import left, right
import math


class EquipmentChange(Screen):
    char = ObjectProperty()

    weapon = ObjectProperty(None, allownone=True)
    helmet = ObjectProperty(None, allownone=True)
    chest = ObjectProperty(None, allownone=True)
    grieves = ObjectProperty(None, allownone=True)
    boots = ObjectProperty(None, allownone=True)
    vambraces = ObjectProperty(None, allownone=True)
    gloves = ObjectProperty(None, allownone=True)
    necklace = ObjectProperty(None, allownone=True)
    ring = ObjectProperty(None, allownone=True)

    minimum_x_distance = NumericProperty(0.0)
    minimum_y_distance = NumericProperty(0.0)

    def __init__(self, **kwargs):
        self.gdb = GestureDatabase()
        self.gdb.add_gesture(left)
        self.gdb.add_gesture(right)
        super().__init__(**kwargs)

    def simplegesture(self, name, point_list):
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

        g = self.simplegesture('', list(zip(touch.ud['line'].points[::2],
                                            touch.ud['line'].points[1::2])))
        # print("gesture representation:", self.gdb.gesture_to_str(g))
        # print("left:", g.get_score(left))
        # print("right:", g.get_score(right))
        g2 = self.gdb.find(g, minscore=0.70)
        if g2:
            if g2[1] == left:
                self.goto_left()
            if g2[1] == right:
                self.goto_right()
        return super().on_touch_up(touch)

    def goto_left(self):
        root = App.get_running_app().main
        party = root.parties[root.parties[0] + 1]
        if self.char in party:
            index = party.index(self.char)
            next = None
            for x in range(index - 1, -1, -1):
                if party[x] is not None:
                    next = party[x]
                    break
            if next is None:
                for x in range(len(party) - 1, index, -1):
                    if party[x] is not None:
                        next = party[x]
                        break
            if next is not None:
                screen, made = root.create_screen('equipment_change_' + next.get_id(), next)
                root.display_screen(screen, True, False)
        else:
            for screen in root.screens:
                if screen.name == 'select_char':
                    index = 0
                    for char in screen.multi.data:
                        if char['id'] == self.char.get_id():
                            if index == 0:
                                next = screen.multi.data[len(screen.multi.data) - 1]
                            else:
                                next = screen.multi.data[index - 1]
                            screen, made = root.create_screen('equipment_change_' + next['id'], next['character'])
                            root.display_screen(screen, True, False)
                            break
                        index += 1
                    break

    def goto_right(self):
        root = App.get_running_app().main
        party = root.parties[root.parties[0] + 1]
        if self.char in party:
            index = party.index(self.char)
            next = None
            for x in range(index + 1, len(party)):
                if party[x] is not None:
                    next = party[x]
                    break
            if next is None:
                for x in range(0, index):
                    if party[x] is not None:
                        next = party[x]
                        break
            if next is not None:
                screen, made = root.create_screen('equipment_change_' + next.get_id(), next)
                root.display_screen(screen, True, False)
        else:
            for screen in root.screens:
                if screen.name == 'select_char':
                    index = 0
                    for char in screen.multi.data:
                        if char['id'] == self.char.get_id():
                            if index == len(screen.multi.data) - 1:
                                next = screen.multi.data[0]
                            else:
                                next = screen.multi.data[index + 1]
                            screen, made = root.create_screen('equipment_change_' + next['id'], next['character'])
                            root.display_screen(screen, True, False)
                            break
                        index += 1
                    break


class MultiEquipmentChange(GridLayout):
    char = ObjectProperty(None, allownone=True)


class CharEquipButton(RelativeLayout):
    char = ObjectProperty(None, allownone=True)

    def on_char_equip(self, *args):
        if self.char is not None:
            screen, made = App.get_running_app().main.create_screen('equipment_change_' + self.char.get_id(), self.char)
            App.get_running_app().main.display_screen(screen, True, True)


class MissingEquip(RelativeLayout):
    pass


class GearChange(Screen):
    animate_distance = NumericProperty(0.0)
    animation_start_down = NumericProperty(0.0)
    animation_start_up = NumericProperty(0.0)
    animation_down = ObjectProperty(None, allownone=True)
    animation_up = ObjectProperty(None, allownone=True)

    def on_enter(self, *args):
        self.animate_arrows()

    def on_leave(self, *args):
        self.unanimate_arrows()

    def animate_arrows(self):
        self.ensure_creation()
        self.animation_down.start(self.ids.arrow_down)
        self.animation_up.start(self.ids.arrow_up)

    def ensure_creation(self):
        if self.animation_down is None or self.animation_up is None:
            self.animation_down = Animation(y=self.animation_start_down - self.animate_distance, duration=1) + Animation(y=self.animation_start_down, duration=0.25)
            self.animation_up = Animation(y=self.animation_start_up + self.animate_distance, duration=1) + Animation(y=self.animation_start_up, duration=0.25)
        self.animation_down.repeat = True
        self.animation_up.repeat = True

    def unanimate_arrows(self):
        if self.animation_down is not None:
            self.animation_down.repeat = False
        if self.animation_up is not None:
            self.animation_up.repeat = False
