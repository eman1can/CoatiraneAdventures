from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.input.providers.wm_touch import WM_MotionEvent
from kivy.graphics import Color, Rectangle

class removeSlot(Screen):

    def __init__(self, managerPass, char, message, **kwargs):
        super(removeSlot, self).__init__(**kwargs)
        self.managerObject = managerPass
        self.button = Button(on_touch_down=self.onPressed, size=(250, 650), pos=(0, 0), size_hint=(None, None))
        image = Image(source='res/removeSlot.png', allow_stretch=True, keep_ratio=True, size_hint=(None, None),
                      size=(250, 650))
        label = Label(text=message, font_size=40, pos=(75, 175), color=(0, 0, 0, 1))
        image.add_widget(label)
        self.char = char
        self.button.add_widget(image)
        self.add_widget(self.button)

    def onPressed(self, instance, touch):
        if self.button.collide_point(*touch.pos):
            if touch.is_touch:
                if touch.button == 'left':
                    self.managerObject.setEmpty()
            else:
                self.managerObject.setEmpty()

class EmptyCharacterPreviewScreen(Screen):

    def __init__(self, main_screen, preview, size, pos):
        pos = (0, 0) # Because this is a screen, the pos gets reset to 0, 0
        super().__init__(size=size, pos=pos)
        # print("Make Empty Char Screen: ", size, pos)
        self.main_screen = main_screen
        self.preview = preview
        self._touch = None

        self.button = Button(size=size, pos=pos, size_hint=(None, None), background_normal='',
                             background_down='', background_color=(0, 0, 0, 0))
        self.button.bind(on_touch_down=self.on_button_touch_down, on_touch_up=self.on_button_touch_up)

        self.image = Image(source='../res/screens/stats/empty_overlay.png', allow_stretch=True, keep_ratio=True, size_hint=(None, None), size=size, pos=pos)
        self.name = 'empty'

        self.add_widget(self.image)
        self.add_widget(self.button)

    def is_valid_touch(self, instance, touch):
        current = self.preview.parent.parent._parent.slots[self.preview.parent.parent._parent.index]
        if current == self.preview.parent.parent:
            return True
        return False

    def on_button_touch_down(self, instance, touch):
        if self.button.collide_point(*touch.pos):
            touch.grab(self)

    def on_button_touch_up(self, instance, touch):
        if touch.grab_current == self:
            touch.ungrab(self)
            if self.is_valid_touch(instance, touch):
                if isinstance(touch, WM_MotionEvent):
                    touch.button = 'left'
                if touch.button != 'left' or self.preview.isDisabled:
                    return True
                self.preview.show_select_screen(self, False)
                return True