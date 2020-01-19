from kivy.metrics import sp
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, BooleanProperty
from kivy.uix.stencilview import StencilView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import DragBehavior
from kivy.uix.widget import Widget
from kivy.uix.label import Label

from src.modules.Screens.CharacterPortfolio import CharacterPortfolio
from src.modules.HTButton import HTButton


class PartyPortfolio(DragBehavior, Widget):
    initialized = BooleanProperty(False)
    dungeon = ObjectProperty(None)
    main_screen = ObjectProperty(None)
    drag_widgets = ListProperty([])
    animate_distance = NumericProperty(0)
    pos_a = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._size = (0, 0)
        self._pos = (-1, -1)

        self.layout = FloatStencil(main_screen=self.main_screen, dungeon=self.dungeon, size_hint=(None, None))

        for x in range(0, len(self.main_screen.parties) - 1):
            portfolio = CharacterPortfolio(party=self.main_screen.parties[x + 1], main_screen=self.main_screen, size_hint=(None, None))
            party_label = Label(text="Party " + str(x + 1), color=(0, 0, 0, 1), font_name="../res/fnt/Precious.ttf")

            drag = DragWidget(root=portfolio, title=party_label, size_hint=(None, None))
            self.drag_widgets.append(drag)

            drag.add_widget(portfolio)
            drag.add_widget(party_label)
            self.layout.add_object(drag)

        self.left_arrow = HTButton(path='../res/screens/buttons/ArrowLeft', background_hover='../res/screens/buttons/ArrowLeft.normal.png', on_touch_down=lambda instance, touch: self.on_arrow_touch(instance, touch, True))
        self.right_arrow = HTButton(path='../res/screens/buttons/ArrowRight', background_hover='../res/screens/buttons/ArrowRight.normal.png', on_touch_down=lambda instance, touch: self.on_arrow_touch(instance, touch, False))

        self.add_widget(self.left_arrow)
        self.add_widget(self.right_arrow)
        self.add_widget(self.layout)
        self.layout.show_index(self.main_screen.parties[0])
        self.initialized = True

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
        if not self.initialized or self._size == size:
            return
        self._size = size.copy()

        self.layout.size = size
        self.arrow_size = self.width * 0.05, self.width * 0.05 * 120 / 72
        self.left_arrow.size = self.arrow_size
        self.right_arrow.size = self.arrow_size

    def on_pos(self, isntance, pos):
        if not self.initialized or self._pos == pos:
            return
        self._pos = pos.copy()

        self.layout.pos = self.pos
        self.left_arrow.pos = self.x, self.y + self.height / 2 - self.arrow_size[1] / 2
        self.right_arrow.pos = self.x + self.width - self.arrow_size[0], self.y + self.height / 2 - self.arrow_size[1] / 2

    def get_party_score(self):
        if not self.initialized:
            return 0
        return self.layout.slots[self.layout.index].root.get_party_score()


class FloatStencil(StencilView):
    initialized = BooleanProperty(False)
    dungeon = ObjectProperty(None)
    main_screen = ObjectProperty(None)
    slots = ListProperty([])
    index = NumericProperty(-1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._size = (0, 0)
        self._pos = (-1, -1)

        self.root = FloatLayout()

        self.add_widget(self.root)
        self.initialized = True

    def on_size(self, instance, size):
        if not self.initialized or self._size == size:
            return
        self._size = size.copy()

        self.root.size = self.width * 5, self.height

        for slot in self.slots:
            slot.size = size

        self.slots[(self.index - 1) % len(self.slots)].pos = (self.x - self.width, self.y)
        self.slots[self.index].pos = self.pos
        self.slots[(self.index + 1) % len(self.slots)].pos = (self.x + self.width, self.y)

    def on_pos(self, isntance, pos):
        if not self.initialized or self._pos == pos:
            return
        self._pos = pos.copy()

        self.root.pos = self.x - self.width * 2, self.y

        self.slots[(self.index - 1) % len(self.slots)].pos = (self.x - self.width, self.y)
        self.slots[self.index].pos = self.pos
        self.slots[(self.index + 1) % len(self.slots)].pos = (self.x + self.width, self.y)

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
        self.add_widget(next_obj)

        next_obj.x = self.x + self.width * 2

        self.animate(current_obj, right_obj, next_obj)

        self.index += 1
        if self.index >= len(self.slots):
            self.index -= len(self.slots)

        self.main_screen.parties[0] = self.index
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
        self.add_widget(next_obj)

        next_obj.x = self.x - self.width * 2

        self.animate(next_obj, left_obj, current_obj)

        self.index -= 1
        if self.index <= -len(self.slots):
            self.index += len(self.slots)

        self.main_screen.parties[0] = self.index
        self.slots[self.index].root.reload()
        if self.dungeon is not None:
            self.dungeon.update_party_score()
        return self.index

    def nocrease_index(self):
        left_obj = self.slots[(self.index - 1) % len(self.slots)]
        current_obj = self.slots[self.index]
        right_obj = self.slots[(self.index + 1) % len(self.slots)]

        self.animate(left_obj, current_obj, right_obj)

        return self.index

    def animate(self, left, middle, right):
        Animation(x=self.x - self.width, duration=.25).start(left)
        Animation(x=self.x, duration=.25).start(middle)
        Animation(x=self.x + self.width, duration=.25).start(right)

    def show_index(self, index):
        left_obj = self.slots[(self.index - 1) % len(self.slots)]
        current_obj = self.slots[self.index]
        right_obj = self.slots[(self.index + 1) % len(self.slots)]

        left_next_obj = self.slots[(index - 1) % len(self.slots)]
        current_next_obj = self.slots[index]
        right_next_obj = self.slots[(index + 1) % len(self.slots)]

        left_next_obj.x = self.x - self.width
        current_next_obj.x = self.x
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
    initialized = BooleanProperty(False)
    root = ObjectProperty(None)
    title = ObjectProperty(None)
    reset_pos = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.drag_distance = 0
        self.drag_timeout = 250
        self._parent = None
        self._drag_touch = None

        self._pos = (0, 0)
        self._size = (0, 0)

        self.callback = lambda : self.after_end()
        self.initialized = True

    def on_size(self, instance, size):
        if not self.initialized or self._size == size:
            return False
        self._size = size.copy()

        if self.root is not None:
            self.root.size = self.width * 0.95, self.height * .9
        if self.title is not None:
            self.title.font_size = 150 * size[1] / 1920
            self.title.texture_update()
            self.title.size = self.title.texture_size
            self.title.pos = (self.x + self.width * 0.025, self.y + self.y - self.title.height)

    def on_pos(self, instance, pos):
        if not self.initialized or self._pos == pos:
            return False
        self._pos = pos.copy()

        if self.root is not None:
            self.root.pos = self.x + self.width * 0.025, self.y
        if self.title is not None:
            self.title.pos = (self.x + self.width * 0.025, self.y + self.height - self.title.height)

    def collide_point(self, x, y):
        if self._parent.is_current(self):
            if self.x <= x < self.x + self.width and self.y <= y < self.y + self.height:
                return True
        return False

    def _get_uid(self, prefix='sv'):
        return '{0}.{1}'.format(prefix, self.uid)

    def on_touch_down(self, touch):
        # If outside bounds
        if not self.collide_point(*touch.pos):
            return True

        # If already have a drag touch that is propigating, ignore others
        if self._drag_touch:
            return True

        if 'button' in touch.profile and touch.button.startswith('scroll'):
            if touch.button in ('scrolldown', 'scrollleft'):
                self._parent.increase_index()
            elif touch.button in ('scrollup', 'scrollright'):
                self._parent.decrease_index()
            return True

        self.reset_pos = self.pos.copy()
        self._drag_touch = touch
        touch.grab(self)
        touch.ud[self._get_uid()] = {
            'mode': 'unknown',
            'dx': 0,
            'dy': 0
        }
        Clock.schedule_once(self._change_touch_mode, self.drag_timeout / 1000)
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
        # If not the same touch, kill it
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
            if abs(self.x - self.reset_pos[0]) > self.width * 5 / 8:
                if min(self.x - self.reset_pos[0], self.reset_pos[0] + self.width - (self.x + self.width)) == \
                        self.x - self.reset_pos[0]:
                    # Go Left
                    self._parent.increase_index()
                else:
                    self._parent.decrease_index()
            else:
                self._parent.nocrease_index()



