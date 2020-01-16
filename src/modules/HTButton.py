from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.properties import BooleanProperty, NumericProperty, ReferenceListProperty, StringProperty


class HoverBehavior(object):
    """Hover behavior.
    :Events:
        `on_enter`
            Fired when mouse enter the bbox of the widget.
        `on_leave`
            Fired when the mouse exit the widget
    """

    hovered = BooleanProperty(False)
    do_hover = BooleanProperty(True)
    '''Contains the last relevant point received by the Hoverable. This can
    be used in `on_enter` or `on_leave` in order to know where was dispatched the event.
    '''

    def __init__(self, **kwargs):
        self.register_event_type('on_enter')
        self.register_event_type('on_leave')
        Window.bind(mouse_pos=self.on_mouse_pos)
        super(HoverBehavior, self).__init__(**kwargs)

    def on_mouse_pos(self, instance, pos):
        if not self.get_root_window() or not self.do_hover:
            return
        # do proceed if I'm not displayed <=> If have no parent
        # Next line to_widget allow to compensate for relative layout
        inside = self.collide_point(*self.to_widget(*pos))
        if self.hovered == inside:
            # We have already done what was needed
            return
        self.hovered = inside
        if inside:
            self.dispatch('on_enter')
        else:
            self.dispatch('on_leave')

    def on_enter(self):
        pass

    def on_leave(self):
        pass


class ToggleBehavior(object):
    """Toggle Behaviour
    :Events:
        `on_state_one`
            Fired when the first state is entered
        `on_state_two`
            First when the second state is entered
    """
    toggle_enabled = BooleanProperty(False)
    toggle_state = BooleanProperty(False)
    width = NumericProperty(100.0)
    height = NumericProperty(100.0)
    x = NumericProperty(0.0)
    y = NumericProperty(0.0)
    size = ReferenceListProperty(width, height)
    pos = ReferenceListProperty(x, y)
    '''Contains the current state of the toggle
    False - State one
    True - State two
    '''

    def __init__(self, **kwargs):
        self.register_event_type('on_state_one')
        self.register_event_type('on_state_two')
        Window.bind(on_touch_down=self.on_click)
        super().__init__(**kwargs)

    def on_click(self, instance, touch):
        if not self.toggle_enabled:
            return
        if not self.get_root_window():
            return
        x, y = touch.pos
        if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
            self.toggle_state = not self.toggle_state
            if self.toggle_state:
                self.dispatch('on_state_two')
            else:
                self.dispatch('on_state_one')

    def on_state_one(self):
        pass

    def on_state_two(self):
        pass


class HTButton(Button, ToggleBehavior, HoverBehavior):
    width = NumericProperty(100.0)
    height = NumericProperty(100.0)
    x = NumericProperty(0.0)
    y = NumericProperty(0.0)
    size = ReferenceListProperty(width, height)
    pos = ReferenceListProperty(x, y)

    path = StringProperty(None)
    collide_image = StringProperty(None)
    background_normal = StringProperty(None)
    background_down = StringProperty(None)
    background_hover = StringProperty(None)

    background_disabled_normal_use = BooleanProperty(False)
    background_disabled_normal = StringProperty(None)
    background_disabled_down_use = BooleanProperty(False)
    background_disabled_down = StringProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.path is not None:
            if self.collide_image is None:
                self.collide_image = self.path + ".collision.png"
            if self.background_normal is None:
                self.background_normal = self.path + ".normal.png"
            if self.background_down is None:
                self.background_down = self.path + ".down.png"
            if self.background_hover is None:
                self.background_hover = self.path + ".hover.png"
            if self.background_disabled_normal is None:
                if self.background_disabled_normal_use:
                    self.background_disabled_normal = self.path + '.disabled.normal.png'
                else:
                    self.background_disabled_normal = ''
            if self.background_disabled_down is None:
                if self.background_disabled_down_use:
                    self.background_disabled_down = self.path + '.disabled.down.png'
                else:
                    self.background_disabled_down = ''

        self.disabled = False
        self._collide_image = Image(source=self.collide_image, keep_data=True)._coreimage
        self.background_normal_temp = self.background_normal

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

    def on_enter(self):
        if self.background_hover is not None:
            self.background_normal = self.background_hover

    def on_leave(self):
        if self.background_hover is not None:
            self.background_normal = self.background_normal_temp
