from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle
from functools import partial
from kivy.uix.stencilview import StencilView
from kivy.uix.behaviors import DragBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.metrics import sp
from src.modules.HTButton import HTButton
from src.modules.Screens.CharacterPortfolio import CharacterPortfolio
class PartyPortfolio(DragBehavior, Widget):
    def __init__(self, main_screen, size, pos, dungeon):
        self.initalized = False
        super().__init__(size=size, pos=pos, size_hint=(None, None))
        self.main_screen = main_screen

        self.layout = FloatStencil(main_screen, size, pos)

        self.portfolios = []

        for x in range(0, len(self.main_screen.parties) - 1):
            party_label = Label(text="Party " + str(x + 1), color=(0, 0, 0, 1), font_name="../res/fnt/Precious.ttf", font_size=150 * size[1] / self.main_screen.width)
            party_label._label.refresh()
            party_label.size = party_label._label.texture.size
            party_label.pos = pos[0] + size[0] * 0.025, pos[1] + size[1] - party_label.height

            drag = DragWidget(size, pos)
            portfolio = CharacterPortfolio(self.main_screen, drag.wid_size, drag.wid_pos, self.main_screen.parties[x + 1])

            drag.root = portfolio
            drag.title = party_label

            self.portfolios.append(portfolio)
            drag.add_widget(portfolio)
            drag.add_widget(party_label)
            self.layout.add_object(drag)

        self.arrow_size = size[0] * 0.05, size[0] * 0.05 * 120 / 72
        self.animate_distance = size[0] * .025
        self.left_arrow = HTButton(path='../res/screens/buttons/ArrowLeft', background_hover='../res/screens/buttons/ArrowLeft.normal.png', size=self.arrow_size, pos=(pos[0] + size[0] * .05 - self.arrow_size[0], pos[1] + (size[1] * 0.8) / 2 - self.arrow_size[1] / 2))
        self.left_arrow.bind(on_touch_up = lambda instance, touch: self.on_arrow_touch(instance, touch, True))
        self.right_arrow = HTButton(path='../res/screens/buttons/ArrowRight', background_hover='../res/screens/buttons/ArrowRight.normal.png', size=self.arrow_size, pos=(pos[0] + size[0] * .95, pos[1] + (size[1] * 0.8) / 2 - self.arrow_size[1] / 2))
        self.right_arrow.bind(on_touch_up = lambda instance, touch: self.on_arrow_touch(instance, touch, False))

        self.pos_a = True
        self.add_widget(self.left_arrow)
        self.add_widget(self.right_arrow)
        self.layout.dungeon = dungeon
        self.layout.show_index(self.main_screen.parties[0])
        self.add_widget(self.layout)

        self.initalized = True

    def reload(self):
        self.layout.slots[self.layout.get_index()].root.reload()

    def on_arrow_touch(self, instance, touch, direction):
        if instance.collide_point(*touch.pos):
            if direction:
                self.layout.decrease_index()
            else:
                self.layout.increase_index()
            return True
        return False

    def animate_arrows(self):
        if self.pos_a:
            Animation(x=self.left_arrow.x - self.animate_distance).start(self.left_arrow)
            Animation(x=self.right_arrow.x + self.animate_distance).start(self.right_arrow)
        else:
            Animation(x=self.left_arrow.x + self.animate_distance, duration=.25).start(self.left_arrow)
            Animation(x=self.right_arrow.x - self.animate_distance, duration=.25).start(self.right_arrow)
        self.pos_a = not self.pos_a

    def on_size(self, instance, size):
        if not self.initalized:
            return

        self.layout.size = size
        self.arrow_size = size[0] * 0.05, size[0] * 0.05 * 120 / 72
        self.left_arrow.size = self.arrow_size
        self.right_arrow.size = self.arrow_size

    def get_party_score(self):
        if not self.initalized:
            return 0
        return self.layout.slots[self.layout.index].root.get_party_score()

class FloatStencil(StencilView):
    def __init__(self, main_screen, size, pos, **kwargs):
        self.initalized = False
        self.main_screen = main_screen
        self.dungeon = None
        self.fpos = pos[0] - size[0] * 2, pos[1]
        self.fsize = size[0] * 5, size[1]

        super().__init__(size=size, pos=pos, size_hint=(None, None), **kwargs)

        self.root = FloatLayout(size=self.fsize, pos=self.fpos)
        self.add_widget(self.root)

        self.slots = []
        self.index = -1

        self.initalized = True

    def on_size(self, instance, size):
        if not self.initalized:
            return

        self.fsize = size[0] * 5, size[1]
        self.fpos = self.pos[0] - size[0] * 2, self.pos[1]
        self.root.size = self.fsize
        self.root.pos = self.fpos

        for slot in self.slots:
            slot.size = size

        self.slots[(self.index - 1) % len(self.slots)].pos = (self.x - self.width, self.pos[1])
        self.slots[self.index].pos = (self.x, self.pos[1])
        self.slots[(self.index + 1) % len(self.slots)].pos = (self.x + self.width, self.pos[1])



    def add_object(self, object):
        # 0 Is the Current
        # 1 Is the Right
        # -1 is the Left
        if len(self.slots) > 2:
            # We want to change the left obj to the last obj
            last_obj = self.slots[-1]
            object.x = self.x - self.width# The Left Posistion
            self.remove_widget(last_obj)
        elif len(self.slots) == 2:
            # Put the object in the left
            object.x = self.x - self.width
        elif len(self.slots) == 1:
            # Put the object in the right
            object.x = self.x + self.width
        else:
            #Zero Objects
            self.index = 0
            object.x = self.x
        self.slots.append(object)
        self.add_widget(object)
        return True

    def on_touch_down(self, touch):
        x, y = touch.pos
        if self.x <= x < self.x + self.width and self.y <= y < self.y + self.height:
            return self.slots[self.index].dispatch('on_touch_down', touch)
        return super().on_touch_down(touch)


    def add_widget(self, widget, index=0, canvas=None):
        if widget == self.root:
            return super().add_widget(widget, index, canvas)
        else:
            widget._parent = self
            return self.root.add_widget(widget, index, canvas)

    def get_index(self):
        return self.index

    def move_neighbors(self, obj, x):
        self.slots[(self.index + 1) % len(self.slots)].x += x
        self.slots[(self.index - 1) % len(self.slots)].x += x

    def is_current(self, obj):
        return self.slots[self.index] == obj

    def increase_index(self):
        # Keep non-display objects out of loading order
        left_obj = self.slots[(self.index - 1) % len(self.slots)]
        current_obj = self.slots[self.index]
        right_obj = self.slots[(self.index + 1) % len(self.slots)]
        next_obj = self.slots[(self.index + 2) % len(self.slots)]

        self.remove_widget(left_obj)

        next_obj.x = self.x + self.width * 2

        anim = Animation(x=self.x - self.width, duration=.25)
        anim.start(current_obj)
        anim = Animation(x=self.x, duration=.25)
        anim.start(right_obj)
        anim = Animation(x=self.x + self.width, duration=.25)
        anim.start(next_obj)

        self.add_widget(next_obj)

        self.index += 1


        self.main_screen.parties[0] = self.index
        if self.index >= len(self.slots):
            self.index -= len(self.slots)
        self.slots[self.index].root.reload()
        if self.dungeon is not None:
            self.dungeon.update_party_score()
        return self.index

    def decrease_index(self):
        next_obj = self.slots[(self.index - 2) % len(self.slots)]
        left_obj = self.slots[(self.index - 1) % len(self.slots)]
        current_obj = self.slots[self.index]
        right_obj = self.slots[(self.index + 1) % len(self.slots)]

        self.remove_widget(right_obj)

        next_obj.x = self.x - self.width * 2

        anim = Animation(x=self.x + self.width, duration=.25)
        anim.start(current_obj)
        anim = Animation(x=self.x, duration=.25)
        anim.start(left_obj)
        anim = Animation(x=self.x - self.width, duration=.25)
        anim.start(next_obj)

        self.add_widget(next_obj)

        self.index -= 1


        self.main_screen.parties[0] = self.index
        if self.index <= -len(self.slots):
            self.index += len(self.slots)
        self.slots[self.index].root.reload()
        if self.dungeon is not None:
            self.dungeon.update_party_score()
        return self.index

    def nocrease_index(self):
        left_obj = self.slots[(self.index - 1)  % len(self.slots)]
        current_obj = self.slots[self.index]
        right_obj = self.slots[(self.index + 1)  % len(self.slots)]

        anim = Animation(x=self.x - self.width, duration=.25)
        anim.start(left_obj)
        anim = Animation(x=self.x, duration=.25)
        anim.start(current_obj)
        anim = Animation(x=self.x + self.width, duration=.25)
        anim.start(right_obj)

        return self.index

    def show_index(self, index):
        left_obj = self.slots[(self.index - 1) % len(self.slots)]
        current_obj = self.slots[self.index]
        right_obj = self.slots[(self.index + 1) % len(self.slots)]

        left_next_obj = self.slots[(index - 1) % len(self.slots)]
        left_next_obj.x = self.x - self.width
        current_next_obj = self.slots[index]
        current_next_obj.x = self.x
        right_next_obj = self.slots[(index + 1) % len(self.slots)]
        right_next_obj.x = self.x + self.width

        src_array = [left_obj, current_obj, right_obj]
        dest_array = [left_next_obj, current_next_obj, right_next_obj]
        for widget in src_array:
            if widget in dest_array:
                dest_array.remove(widget)
            else:
                self.remove_widget(widget)

        for widget in dest_array:
            self.add_widget(widget)

        self.index = index
        if self.dungeon is not None:
            self.dungeon.update_party_score()

    def remove_widget(self, widget):
        self.root.remove_widget(widget)

class DragWidget(Widget):
    def __init__(self, size, pos, **kwargs):
        self.initalized = False
        super().__init__(size=size, pos=pos, size_hint=(None, None), **kwargs)
        self.drag_distance = 0
        self.drag_timeout = 250
        self.root = None
        self._parent = None
        self._pos = pos

        self.wid_size = size[0] * 0.95, size[1] * .9
        self.wid_pos = pos[0] + size[0] * 0.025, pos[1]

        self._drag_touch = None

        self.callback = lambda : self.after_end()
        self.initalized = True

    def on_size(self, instance, size):
        if not self.initalized:
            return False
        if self.root is not None:
            self.wid_size = size[0] * 0.95, size[1] * .9
            self.root.size = self.wid_size
        if self.title is not None:
            self.title.font_size=150 * size[1] / 1920
            self.title._label.refresh()
            self.title.size = self.title._label.texture.size
            self.title.pos = (self.pos[0] + size[0] * 0.025, self.pos[1] + self.size[1] - self.title.size[1])

    def on_pos(self, instance, pos):
        if not self.initalized:
            return False
        if self.root is not None:
            self.wid_pos = pos[0] + self.size[0] * 0.025, pos[1]
            self.root.pos = self.wid_pos
        if self.title is not None:
            self.title.pos = (pos[0] + self.size[0] * 0.025, pos[1] + self.size[1] - self.title.size[1])

    def collide_point(self, x, y):
        if self._parent.is_current(self):
            if self.x <= x < self.x + self.width and self.y <= y < self.y + self.height:
                return True
        return False

    def _get_uid(self, prefix='sv'):
        return '{0}.{1}'.format(prefix, self.uid)

    def on_touch_down(self, touch):
        #If outside bounds
        if not self.collide_point(*touch.pos):
            return True

        #If already have a drag touch that is propigating, ignore others
        if self._drag_touch:
            return True

        if 'button' in touch.profile and touch.button.startswith('scroll'):
            if touch.button in ('scrolldown', 'scrollleft'):
                self._parent.increase_index()
            elif touch.button in ('scrollup', 'scrollright'):
                self._parent.decrease_index()
            return True


        self._drag_touch = touch
        touch.grab(self)
        touch.ud[self._get_uid()] = {
            'mode': 'unknown',
            'dx': 0,
            'dy': 0
        }
        Clock.schedule_once(self._change_touch_mode,
                            self.drag_timeout / 1000)
        return True

    def _change_touch_mode(self, *args):
        if not self._drag_touch:
            return

        uid = self._get_uid()
        touch = self._drag_touch

        ud = touch.ud[uid]
        if ud['mode'] != 'unknown':
            return

        touch.ungrab(self)
        self._drag_touch = None

        for child in self.children:
            child.dispatch('on_touch_down', touch)

        return

    def on_touch_move(self, touch):
        #If not the same touch, kill it
        if touch.grab_current is not self:
            return True

        uid = self._get_uid()
        ud = touch.ud[uid]
        mode = ud['mode']

        if mode == 'unknown':
            ud['dx'] += abs(touch.dx)
            ud['dy'] += abs(touch.dy)

            if ud['dx'] > sp(self.drag_distance):
                mode = 'drag'
            if ud['dy'] > sp(self.drag_distance):
                mode = 'drag'

            ud['mode'] = mode

        if mode == 'drag':
            self.x += touch.dx
            self._parent.move_neighbors(self, touch.dx)
        return True

    def on_touch_up(self, touch):
        if self._drag_touch and self in [x() for x in touch.grab_list]:
            touch.ungrab(self)
            self._drag_touch = None
            ud = touch.ud[self._get_uid()]
            if self.callback is not None:
                self.callback()
            if ud['mode'] == 'unknown':
                for child in self.children:
                    child.dispatch('on_touch_down', touch)
        else:
            if self._drag_touch is not touch:
                super().on_touch_up(touch)
        return self._get_uid() in touch.ud

    def after_end(self):
        if self._parent.is_current(self):
            if abs(self.x - self._pos[0]) > self.width * 5 / 8:
                if min(self.x - self._pos[0], self._pos[0] + self.width - (self.x + self.width)) == \
                        self.x - self._pos[0]:
                    # Go Left
                    self._parent.increase_index()
                else:
                    self._parent.decrease_index()
            else:
                self._parent.nocrease_index()



