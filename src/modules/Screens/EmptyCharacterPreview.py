from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from src.modules.HTButton import HTButton
from kivy.input.providers.wm_touch import WM_MotionEvent

class EmptyCharacterPreviewScreen(Screen):

    def __init__(self, main_screen, preview, size, pos):
        pos = (0, 0) # Because this is a screen, the pos gets reset to 0, 0
        self.initalized = False
        super().__init__(size=size, pos=pos)
        self.main_screen = main_screen
        self.preview = preview
        self._touch = None
        self.name = 'empty'

        self.button = HTButton(size=size, pos=pos, size_hint=(None, None), border=[0, 0, 0, 0], path='../res/screens/buttons/empty_overlay', on_touch_down=self.on_button_touch_down, on_touch_up=self.on_button_touch_up)
        self.add_widget(self.button)

        self.initalized = True

    def on_size(self, instance, size):
        if not self.initalized:
            return
        self.button.size = size

    def is_valid_touch(self, instance, touch):
        current = self.preview.parent.parent._parent.slots[self.preview.parent.parent._parent.index]
        if current == self.preview.parent.parent:
            return True
        return False

    def on_button_touch_down(self, instance, touch):
        if instance.collide_point(*touch.pos):
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