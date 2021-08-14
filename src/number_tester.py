from kivy.config import Config

Config.set('graphics', 'width', 1000)
Config.set('graphics', 'height', 725)


from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder

root = """

RelativeLayout:
    size: 500, 500
    Label:
        font_name: '../res/fnt/Fantasque.ttf'
        font_size: 72
        color: 144 / 255, 255 / 255, 122 / 255, 1
        outline_width: 5
        outline_color: 27 / 255, 61 / 255, 11 / 255, 1
        text: '0 1 2 3 4 5 6 7 8 9'
        size_hint: 1, 0.1
        pos_hint: {'top': 1}
    Label:
        font_name: '../res/fnt/Fantasque.ttf'
        font_size: 72
        color: 1, 1, 1, 1
        outline_width: 5
        outline_color: 0, 0, 0, 1
        text: '0 1 2 3 4 5 6 7 8 9'
        size_hint: 1, 0.1
        pos_hint: {'top': 0.9}
    Label:
        font_name: '../res/fnt/Fantasque.ttf'
        font_size: 72
        color: 122 / 255, 171 / 255, 255 / 255, 1
        outline_width: 5
        outline_color: 11 / 255, 24 / 255, 61 / 255, 1
        text: '0 1 2 3 4 5 6 7 8 9'
        size_hint: 1, 0.1
        pos_hint: {'top': 0.8}
    Label:
        font_name: '../res/fnt/Fantasque.ttf'
        font_size: 72
        color: 1, 1, 1, 1
        outline_width: 5
        outline_color: 255 / 255, 81 / 255, 81 / 255, 1
        text: 'Penetration'
        size_hint: 0.5, 0.2
        pos_hint: {'top': 0.7}
    Label:
        font_name: '../res/fnt/Fantasque.ttf'
        font_size: 72
        color: 1, 1, 1, 1
        outline_width: 5
        outline_color: 255 / 255, 92 / 255, 33 / 255, 1
        text: 'Critical'
        size_hint: 0.5, 0.2
        pos_hint: {'top': 0.7, 'x': 0.5}
    Label:
        font_name: '../res/fnt/Fantasque.ttf'
        font_size: 72
        color: 1, 1, 1, 1
        outline_width: 5
        outline_color: 255 / 255, 230 / 255, 20 / 255, 1
        text: 'Evade'
        size_hint: 0.5, 0.2
        pos_hint: {'top': 0.6}
    Label:
        font_name: '../res/fnt/Fantasque.ttf'
        font_size: 72
        color: 1, 1, 1, 1
        outline_width: 5
        outline_color: 55 / 255, 63 / 255, 63 / 255, 1
        text: 'Block'
        size_hint: 0.5, 0.2
        pos_hint: {'top': 0.6, 'x': 0.5}
    Label:
        font_name: '../res/fnt/Fantasque.ttf'
        font_size: 72
        color: 1, 1, 1, 1
        outline_width: 5
        outline_color: 82 / 255, 196 / 255, 143 / 255, 1
        text: 'Weak'
        size_hint: 0.5, 0.2
        pos_hint: {'top': 0.5}
    Label:
        font_name: '../res/fnt/Fantasque.ttf'
        font_size: 72
        color: 1, 1, 1, 1
        outline_width: 5
        outline_color: 0 / 255, 19 / 255, 197 / 255, 1
        text: 'Counter'
        size_hint: 0.5, 0.2
        pos_hint: {'top': 0.5, 'x': 0.5}
    Label:
        font_name: '../res/fnt/Fantasque.ttf'
        font_size: 72
        color: 1, 1, 1, 1
        outline_width: 5
        outline_color: 196 / 255, 90 / 255, 90 / 255, 1
        text: 'Resist'
        size_hint: 0.5, 0.2
        pos_hint: {'top': 0.4}
    Label:
        font_name: '../res/fnt/Fantasque.ttf'
        font_size: 72
        color: 1, 1, 1, 1
        outline_width: 5
        outline_color: 40 / 255, 40 / 255, 40 / 255, 1
        text: 'Null'
        size_hint: 0.5, 0.2
        pos_hint: {'top': 0.4, 'x': 0.5}
"""


class NumberApp(App):
    def build(self):
        rootw = Builder.load_string(root)
        Clock.schedule_once(lambda dt: rootw.export_to_png('Atlas.png'), 2)
        return rootw

NumberApp().run()