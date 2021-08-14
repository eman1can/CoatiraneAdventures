from kivy.config import Config
Config.set('graphics', 'width', '1706')
Config.set('graphics', 'height', '960')
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.uix.floatlayout import FloatLayout

root = """
CustomLayout:
    canvas:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            size: root.size
        # Background
        Color:
            rgba: 0, 0, 0, 1
        Rectangle:
            size: 1706, 960
            pos: 0, 0
        # Background Left
        Color:
            rgba: 0, 0, 1, 1 * root.left
        Rectangle:
            size: 553, 525
            pos: 0, 435
        # Background Center
        Color:
            rgba: 0, 0, 1, 1 * (1 - root.up)
        Rectangle:
            size: 600, 525
            pos: 553, 435
        # Background Right
        Color:
            rgba: 0, 0, 1, 1 * root.right
        Rectangle:
            size: 553, 525
            pos: 1153, 435
        # Movement Layer - Horizontal Left
        Color:
            rgba: 1, 0, 0, 1 * root.left
        Rectangle:
            size: 553, 350
            pos: 0, 85
        # Movement Layer - Horizontal Center
        Color:
            rgba: 1, 0, 0, 1
        Rectangle:
            size: 600, 350
            pos: 553, 85
        # Movement Layer - Horizontal Right
        Color:
            rgba: 1, 0, 0, 1 * root.right
        Rectangle:
            size: 553, 350
            pos: 1153, 85
        # Movement Layer - Vertical Top
        Color:
            rgba: 1, 0, 0, 1 * root.up
        Rectangle:
            size: 600, 525
            pos: 553, 435
        # Movement Layer - Vertical Bottom
        Color:
            rgba: 1, 0, 0, 1 * root.down
        Rectangle:
            size: 600, 85
            pos: 553, 0
        # Foreground Left
        Color:
            rgba: 0, 1, 0, 0.5 * root.left
        Rectangle:
            size: 553, 175
            pos: 0, 0
        # Foreground Right
        Color:
            rgba: 0, 1, 0, 0.5 * root.right
        Rectangle:
            size: 553, 175
            pos: 1153, 0
        # Foreground Center
        Color:
            rgba: 0, 1, 0, 0.5 * (1 - root.down)
        Rectangle:
            size: 600, 175
            pos: 553, 0
        
        
"""
# Background Information
# Background Layer - p 0, 385 s 1706, 575
# Movement Layer - p 0, 75 s 1706, 300
# Foreground Layer - p 0, 0 s 1706, 175
# Left Block - 0 -> 553
# Right Block - 1153 -> 1706


class CustomLayout(FloatLayout):
    down = NumericProperty(1)
    up = NumericProperty(1)
    left = NumericProperty(1)
    right = NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for x in range(1, 16):
            Clock.schedule_once(lambda dt, x=x: self.create_images(x), x * 2)
            Clock.schedule_once(lambda dt, x=x: self.export_images(x), x * 2 + 1)

    def create_images(self, x):
        N = int(x & 1 == 1)
        S = int(x & 2 == 2)
        E = int(x & 4 == 4)
        W = int(x & 8 == 8)
        self.down = S
        self.up = N
        self.left = W
        self.right = E
        print(N, S, E, W)

    def export_images(self, x):
        N = 'N' if x & 1 == 1 else ''
        S = 'S' if x & 2 == 2 else ''
        E = 'E' if x & 4 == 4 else ''
        W = 'W' if x & 8 == 8 else ''
        print('Image name is ', f'tile_{N}{S}{E}{W}')
        self.export_to_png(f'tile_{N}{S}{E}{W}.png')

class KApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        return Builder.load_string(root)


if __name__ == "__main__":
    KApp().run()
