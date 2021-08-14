from random import randint, uniform

from kivy.animation import Animation
from kivy.config import Config
from kivy.properties import BooleanProperty, NumericProperty, OptionProperty

from kivy.graphics import InstructionGroup, MatrixInstruction, PopMatrix, PushMatrix, Rectangle
from kivy.graphics.transformation import Matrix

from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from uix.screens.dungeon.marker import Marker

Config.set('graphics', 'width', 1000)
Config.set('graphics', 'height', 725)


from kivy.app import App


class Display(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.markers = []
        self.add_widget(Button(on_release=lambda button: self.play_marker(0), size_hint=(0.1, 0.1)))
        self.canvas.add(Rectangle(size=(10, 10), pos=(195, 195)))

    def play_marker(self, dt):
        if self.markers is not None:
            for marker in self.markers:
                self.remove_widget(marker)
            self.markers = []
        for type in ['damage', 'crit_damage', 'health', 'mana', 'penetration', 'critical', 'counter', 'block', 'evade', 'resist', 'weak', 'null']:
            marker = Marker(100, 1, type=type, value=randint(1000, 100000), size_hint=(None, None), size=(200, 200), pos_hint={'center_x': 200 / self.width, 'y': 200 / self.height})
            self.markers.append(marker)
            self.add_widget(marker)


class NumberApp(App):
    def build(self):
        layout = Display()
        return layout


NumberApp().run()
