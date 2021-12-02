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
        # Color:
        #     rgba: 1, 1, 1, 1
        # Rectangle:
        #     size: root.size
        # Background
        # Color:
        #     rgba: 1, 1, 1, 1
        # Rectangle:
        #     size: 1706, 960
        #     pos: 0, 0
        #     source: 'C:/Users/Zoe/Documents/Megascans Library/Downloaded/surface/rock_jagged_vczkdailw/vczkdailw_8K_Albedo.jpg'
        # Background Left
        Color:
            rgba: 1, 1, 1, 1 * root.left * root.background
        Rectangle:
            size: 553, 525
            pos: 0, 435
            source: 'C:/Users/Zoe/Documents/Megascans Library/Downloaded/surface/rock_jagged_vczkdailw/vczkdailw_8K_Albedo.jpg'
        # Background Center
        Color:
            rgba: 1, 1, 1, 1 * (1 - root.up) * root.background
        Rectangle:
            size: 600, 525
            pos: 553, 435
            source: 'C:/Users/Zoe/Documents/Megascans Library/Downloaded/surface/rock_jagged_vczkdailw/vczkdailw_8K_Albedo.jpg'
        # Background Right
        Color:
            rgba: 1, 1, 1, 1 * root.right * root.background
        Rectangle:
            size: 553, 525
            pos: 1153, 435
            source: 'C:/Users/Zoe/Documents/Megascans Library/Downloaded/surface/rock_jagged_vczkdailw/vczkdailw_8K_Albedo.jpg'
        # Movement Layer - Horizontal Left
        Color:
            rgba: 1, 1, 1, 1 * root.left * root.background
        Rectangle:
            size: 553, 350
            pos: 0, 85
            source: 'C:/Users/Zoe/Documents/Megascans Library/Downloaded/surface/concrete_rough_vjctbag/vjctbag_8K_Albedo.jpg'
        # Movement Layer - Horizontal Center
        Color:
            rgba: 1, 1, 1, 1 * root.background
        Rectangle:
            size: 600, 350
            pos: 553, 85
            source: 'C:/Users/Zoe/Documents/Megascans Library/Downloaded/surface/concrete_rough_vjctbag/vjctbag_8K_Albedo.jpg'
        # Movement Layer - Horizontal Right
        Color:
            rgba: 1, 1, 1, 1 * root.right * root.background
        Rectangle:
            size: 553, 350
            pos: 1153, 85
            source: 'C:/Users/Zoe/Documents/Megascans Library/Downloaded/surface/concrete_rough_vjctbag/vjctbag_8K_Albedo.jpg'
        # Movement Layer - Vertical Top
        Color:
            rgba: 1, 1, 1, 1 * root.up * root.background
        Rectangle:
            size: 600, 525
            pos: 553, 435
            source: 'C:/Users/Zoe/Documents/Megascans Library/Downloaded/surface/concrete_rough_vjctbag/vjctbag_8K_Albedo.jpg'
        # Movement Layer - Vertical Bottom
        Color:
            rgba: 1, 1, 1, 1 * root.down * root.background
        Rectangle:
            size: 600, 85
            pos: 553, 0
            source: 'C:/Users/Zoe/Documents/Megascans Library/Downloaded/surface/concrete_rough_vjctbag/vjctbag_8K_Albedo.jpg'
        # Foreground Left
        Color:
            rgba: 1, 1, 1, 1 * root.left * root.foreground
        Rectangle:
            size: 553, 175
            pos: 0, 0
            source: 'C:/Users/Zoe/Documents/Megascans Library/Downloaded/surface/rock_jagged_vczkdailw/vczkdailw_8K_Albedo.jpg'
        # Foreground Right
        Color:
            rgba: 1, 1, 1, 1 * root.right * root.foreground
        Rectangle:
            size: 553, 175
            pos: 1153, 0
            source: 'C:/Users/Zoe/Documents/Megascans Library/Downloaded/surface/rock_jagged_vczkdailw/vczkdailw_8K_Albedo.jpg'
        # Foreground Center
        Color:
            rgba: 1, 1, 1, 1 * (1 - root.down) * root.foreground
        Rectangle:
            size: 600, 175
            pos: 553, 0
            source: 'C:/Users/Zoe/Documents/Megascans Library/Downloaded/surface/rock_jagged_vczkdailw/vczkdailw_8K_Albedo.jpg'
        
        
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

    background = NumericProperty(1)
    foreground = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Blank Tile
        Clock.schedule_once(self.create_blank, 0)
        # Battle Tile
        Clock.schedule_once(self.create_battle_background, 2)
        Clock.schedule_once(self.create_battle_foreground, 4)
        # Directional Tiles
        Clock.schedule_once(self.create_tiles, 6)

    def create_blank(self, dt):
        self.down = self.up = self.left = self.right = 0
        self.background = 0
        self.foreground = 0
        Clock.schedule_once(lambda dt: self.save_image('tile_blank.png'), 1)

    def create_battle_background(self, dt):
        self.left = self.right = 1
        self.background = 1
        Clock.schedule_once(lambda dt: self.save_image('battle_background.png'), 1)

    def create_battle_foreground(self, dt):
        self.background = 0
        self.foreground = 1
        Clock.schedule_once(lambda dt: self.save_image('battle_foreground.png'), 1)

    def create_tiles(self, dt):
        for x in range(1, 32):
            Clock.schedule_once(lambda dt, x=x: self.create_tile_image(x), x)
            Clock.schedule_once(lambda dt, x=x: self.export_tile_image(x), x + 1)

    def create_tile_image(self, x):
        N = int(x & 1 == 1)
        S = int(x & 2 == 2)
        E = int(x & 4 == 4)
        W = int(x & 8 == 8)
        background = int(x & 16 == 16)
        self.down = S
        self.up = N
        self.left = W
        self.right = E
        self.background = background
        self.foreground = 1 - background

    def export_tile_image(self, x):
        N = 'N' if x & 1 == 1 else ''
        S = 'S' if x & 2 == 2 else ''
        E = 'E' if x & 4 == 4 else ''
        W = 'W' if x & 8 == 8 else ''
        suffix = '_background' if x & 16 == 16 else '_foreground'
        self.save_image(f'tile_{N}{S}{E}{W}{suffix}.png')

    def save_image(self, name):
        self.export_to_png(name)


class KApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        return Builder.load_string(root)


if __name__ == "__main__":
    KApp().run()
