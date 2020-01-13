from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.properties import BooleanProperty

class HoverBehavior(object):
    """Hover behavior.
    :Events:
        `on_enter`
            Fired when mouse enter the bbox of the widget.
        `on_leave`
            Fired when the mouse exit the widget
    """

    hovered = BooleanProperty(False)
    '''Contains the last relevant point received by the Hoverable. This can
    be used in `on_enter` or `on_leave` in order to know where was dispatched the event.
    '''

    def __init__(self, **kwargs):
        self.register_event_type('on_enter')
        self.register_event_type('on_leave')
        Window.bind(mouse_pos=self.on_mouse_pos)
        super(HoverBehavior, self).__init__(**kwargs)

    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return  # do proceed if I'm not displayed <=> If have no parent
        pos = args[1]
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

class CustomHoverableButton(Button, HoverBehavior):

    def __init__(self, **kwargs):
        kwargs.setdefault('size', (0, 0))
        kwargs.setdefault('pos', (0, 0))
        kwargs.setdefault('size_hint', (None, None))
        kwargs.setdefault('background_disabled_down', '')
        if kwargs is not None:
            if kwargs.get('size'):
                self.size = kwargs.get('size')
            if kwargs.get('pos'):
                self.pos = kwargs.get('pos')
            if kwargs.get('path'):
                self.path = kwargs.pop('path')
                self.collide_image = self.path + ".collision.png"
                self.background_normal = self.path + ".normal.png"
                self.background_down = self.path + ".down.png"
                self.background_hover = self.path + ".hover.png"
                if (kwargs.get('background_disabled_normal') is not None):
                    if (kwargs.pop('background_disabled_normal')):
                        self.background_disabled_normal = self.path + ".disabled.normal.png"
                if (kwargs.get('background_disabled_down') is not None):
                    if (kwargs.pop('background_disabled_down')):
                        self.background_disabled_down = self.path + ".disabled.down.png"
                if kwargs.get('normal'):
                    self.background_normal = kwargs.pop('normal')
                if kwargs.get('hover'):
                    self.background_hover = kwargs.pop('hover')
                if kwargs.get('collision'):
                    self.collide_image = kwargs.pop('collision')
            else:
                self.path = None
                if kwargs.get('collide_image'):
                    self.collide_image = kwargs.pop('collide_image')
                if kwargs.get('background_normal'):
                    self.background_normal = kwargs.pop('background_normal')
                if kwargs.get('background_disabled_normal'):
                    self.background_disabled_normal = kwargs.pop('background_disabled_normal')
                if kwargs.get('background_disabled_down'):
                    self.background_disabled_down = kwargs.pop('background_disabled_down')
                if kwargs.get('background_down'):
                    self.background_down = kwargs.pop('background_down')
                if kwargs.get('background_hover'):
                    self.background_hover = kwargs.pop('background_hover')
                else:
                    self.background_hover = None
        super().__init__(**kwargs)
        self.size_hint = (None, None)
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