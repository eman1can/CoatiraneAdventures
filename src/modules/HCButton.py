from src.modules.HTButton import HoverBehavior, ToggleBehavior
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.properties import NumericProperty, ReferenceListProperty, StringProperty, BooleanProperty

class HCButton(Button, ToggleBehavior, HoverBehavior):
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
    background_hover_down = StringProperty(None)

    background_disabled_normal_use = BooleanProperty(False)
    background_disabled_normal = StringProperty(None)
    background_disabled_down_use = BooleanProperty(False)
    background_disabled_down = StringProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.toggle_enabled = True
        self.bind(on_touch_down=self.on_click)

        if self.path is not None:
            if self.collide_image is None:
                self.collide_image = self.path + ".collision.png"
            if self.background_normal is None:
                self.background_normal = self.path + ".normal.png"
            if self.background_down is None:
                self.background_down = self.path + ".down.png"
            if self.background_hover is None:
                self.background_hover = self.path + ".hover.png"
            if self.background_hover_down is None:
                self.background_hover_down = self.path + ".down.hover.png"
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
        self.background_down_temp = self.background_down

        if self.toggle_state:
            self.background_normal = self.background_down


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
        if self.background_hover is not None and not self.toggle_state:
            self.background_normal = self.background_hover
        elif self.background_hover_down is not None and self.toggle_state:
            self.background_normal = self.background_hover_down

    def on_leave(self):
        if self.background_hover is not None and not self.toggle_state:
            self.background_normal = self.background_normal_temp
        elif self.background_hover_down is not None and self.toggle_state:
            self.background_normal = self.background_down_temp

    def on_state_one(self):
        self.background_normal = self.background_normal_temp

    def on_state_two(self):
        self.background_normal = self.background_down_temp
