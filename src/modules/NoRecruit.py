from kivy.properties import BooleanProperty
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from src.modules.HTButton import HTButton

class NoRecruitWidget(Widget):
    initialized = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._size = (0, 0)

        self.shadow = Image(source='../res/screens/backgrounds/shadow.png', allow_stretch=True)
        self.shadow.bind(on_touch_down=self.toss)
        self.background = Image(source="../res/screens/stats/sort_background.png", allow_stretch=True)

        self.label_large = Label(text="All Characters Recruited", font_name="../res/fnt/Gabriola.ttf", size_hint=(None, None), color=(0, 0, 0, 1))
        self.label_small = Label(text="More characters will be added\nin future updates", halign="center", font_name="../res/fnt/Gabriola.ttf", size_hint=(None, None), color=(0, 0, 0, 1))
        self.ok_button = HTButton(path="../res/screens/buttons/long_stat", on_release=self.on_ok, size_hint=(None, None), font_name="../res/fnt/Gabriola.ttf", text="Ok")

        self.add_widget(self.shadow)
        self.add_widget(self.background)
        self.add_widget(self.label_large)
        self.add_widget(self.label_small)
        self.add_widget(self.ok_button)
        self.initialized = True

    def on_size(self, instane, size):
        if not self.initialized or self._size == size:
            return
        self._size = size.copy()

        self.shadow.size = self.size

        width, height = self.height * 0.9 * 750 / 600, self.height * 0.9
        x, y = (self.width - width) / 2, (self.height - height) / 2
        self.background.size = width, height
        self.background.pos = x, y
        self.label_large.font_size = height * .15
        self.label_large.texture_update()
        self.label_small.font_size = height * .1
        self.label_small.texture_update()
        self.label_large.size = width, self.label_large.texture_size[1]
        self.label_large.pos = x, y + height - self.label_large.height * 1.25
        self.label_small.size = width, self.label_small.texture_size[1]
        self.label_small.pos = x, y + height - self.label_large.height * 1.25 - self.label_small.height * 1.25
        self.ok_button.font_size = height * .05
        self.ok_button.size = height * 0.15 * 570 / 215, height * 0.15
        self.ok_button.pos = x + (width - self.ok_button.width) / 2, y + self.ok_button.height / 2

    def toss(self, *args):
        return True

    def on_ok(self, instance):
        self.parent.remove_widget(self)