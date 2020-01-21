from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from src.modules.HTButton import HTButton
from kivy.input.providers.wm_touch import WM_MotionEvent

class EmptyCharacterPreviewScreen(Screen):
    initialized = BooleanProperty(False)
    main_screen = ObjectProperty(None)
    preview = ObjectProperty(None)

    locked = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'empty'

        self._touch = None
        self._size = (0, 0)

        self.button = HTButton(size_hint=(None, None), path='../res/screens/buttons/empty_overlay', on_touch_down=self.on_button_touch_down, on_touch_up=self.on_button_touch_up)

        self.lock = Image(source="../res/screens/stats/lock.png", allow_stretch=True, size_hint=(None, None), opacity=0)

        self.add_widget(self.button)
        self.add_widget(self.lock)
        self.initialized = True

    def on_size(self, instance, size):
        if not self.initialized or self._size == size:
            return
        self._size = size.copy()
        self.button.size = size

        self.lock.size = self.width * 0.3, self.width * 0.3
        self.lock.pos = self.width - self.width * 0.3, self.height - self.width * 0.3

    def is_valid_touch(self, instance, touch):
        current = self.preview.parent.parent._parent.slots[self.preview.parent.parent._parent.index]
        if current == self.preview.parent.parent:
            return True
        return False

    def update_lock(self, locked):
        self.locked = locked
        if self.locked:
            self.lock.opacity = 1
        else:
            self.lock.opacity = 0

    def on_button_touch_down(self, instance, touch):
        if instance.collide_point(*touch.pos):
            if not self.locked:
                touch.grab(self)

    def on_button_touch_up(self, instance, touch):
        if touch.grab_current == self and not self.locked:
            touch.ungrab(self)
            if self.is_valid_touch(instance, touch):
                if isinstance(touch, WM_MotionEvent):
                    touch.button = 'left'
                if touch.button != 'left' or self.preview.is_disabled:
                    return True
                self.preview.show_select_screen(self, False)
                return True