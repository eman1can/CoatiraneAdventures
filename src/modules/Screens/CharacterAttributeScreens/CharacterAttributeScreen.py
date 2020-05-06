from kivy.app import App
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from src.modules.KivyBase.Hoverable import ScreenBase as Screen
from kivy.graphics import Line
from kivy.gesture import Gesture, GestureDatabase
from src.modules.ca_gestures import left, right
import math


class CharacterAttributeScreen(Screen):
    preview = ObjectProperty(None, allownone=True)
    char = ObjectProperty(None, allownone=True)

    overlay_background_source = StringProperty("../res/screens/attribute/stat_background.png")
    overlay_source = StringProperty("../res/screens/attribute/stat_background_overlay.png")
    flag_source = StringProperty("../res/screens/attribute/char_type_flag.png")
    overlay_bar_source = StringProperty("../res/screens/stats/overlay_bar.png")
    neat_stat_overlay_source = StringProperty("../res/screens/attribute/stat_overlay.png")
    skills_switch_text = StringProperty('Skills')

    minimum_x_distance = NumericProperty(0.0)
    minimum_y_distance = NumericProperty(0.0)

    def __init__(self, **kwargs):
        self.gdb = GestureDatabase()
        self.gdb.add_gesture(left)
        self.gdb.add_gesture(right)
        super().__init__(**kwargs)

    def on_touch_hover(self, touch):
        if self.ids.image_preview.dispatch('on_touch_hover', touch):
            return True
        if self.ids.change_equip.dispatch('on_touch_hover', touch):
            return True
        if self.ids.status_board.dispatch('on_touch_hover', touch):
            return True
        return False

    def on_image_preview(self):
        screen, made = App.get_running_app().main.create_screen('image_preview_' + self.char.get_id(), self.char)
        App.get_running_app().main.display_screen(screen, True, True)

    def on_leave(self, *args):
        if self.skills_switch_text == 'Status':
            self.on_skills_switch()

    def on_status_board(self):
        screen, made = App.get_running_app().main.create_screen('status_board_' + self.char.get_id(), self.char)
        App.get_running_app().main.display_screen(screen, True, True)

    def on_skills_switch(self):
        if self.skills_switch_text == 'Skills':
            self.skills_switch_text = 'Status'
        else:
            self.skills_switch_text = 'Skills'
        self.ids.normal_layout.opacity = int(not bool(int(self.ids.normal_layout.opacity)))
        self.ids.skill_layout.opacity = int(not bool(int(self.ids.skill_layout.opacity)))
        self.ids.skillslist.scroll_y = 1
        self.ids.skillslist.update_from_scroll()

    def on_change_equip(self):
        screen, made = App.get_running_app().main.create_screen('equipment_change_' + self.char.get_id(), self.char)
        App.get_running_app().main.display_screen(screen, True, True)

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
                screen, made = root.create_screen('char_attr_' + next.get_id(), next, self.preview)
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
                            screen, made = root.create_screen('char_attr_' + next['id'], next['character'], self.preview)
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
                screen, made = root.create_screen('char_attr_' + next.get_id(), next, self.preview)
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
                            screen, made = root.create_screen('char_attr_' + next['id'], next['character'], self.preview)
                            root.display_screen(screen, True, False)
                            break
                        index += 1
                    break
