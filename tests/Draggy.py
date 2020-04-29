# # from kivy.app import App
# # from kivy.uix.widget import Widget
# # from kivy.uix.image import Image
# # from src.modules.DragScreen import DragSnapWidget, DragWidgetObject
# #
# #
# # class Main(Widget):
# #     def __init__(self, **kwargs):
# #         super().__init__(**kwargs)
# #         root = DragSnapWidget()
# #         self.add_widget(root)
# #         for index in range(0, 5):
# #             drag = DragWidgetObject()
# #             drag.root = Image(source="../res/screens/backgrounds/background.png", allow_stretch=True, keep_ratio=False, size_hint=(None, None))
# #             root.add_object(drag)
# #         root.pos = (20, 20)
# #         root.size = (750, 750)
# #
# #
# # class TestApp(App):
# #     def build(self):
# #         return Main()
# #
# # if __name__ == '__main__':
# #     app = TestApp()
# #     app.run()
#
# from kivy.app import App
# from kivy.uix.widget import Widget
# from kivy.lang.builder import Builder
# from kivy.uix.image import Image
# from kivy.uix.label import Label
# from kivy.uix.behaviors import ToggleButtonBehavior, TouchRippleBehavior
#
# Builder.load_string('''
# <MyWidget>:
#     RelativeLayout:
#         size: root.size
#         Widget:
#             size_hint: 0.5031, 0.8896
#             pos_hint: {'center_x': 0.7145, 'y': 0.05}
#             canvas:
#                 Color:
#                     rgba: 0, 1, 0, 0.3
#                 Rectangle:
#                     size: self.size
#                     pos: self.pos
#             RelativeLayout:
#                 size: self.parent.size
#                 pos: self.parent.pos
#                 GridLayout:
#                     cols: 1
#                     rows: 4
#                     size_hint: 1, 0.85
#                     canvas:
#                         Color:
#                             rgba: 0.5, 0.2, 0, 0.3
#                         Rectangle:
#                             size: self.size
#                             pos: self.pos
#                     GridLayout:
#                         rows: 3
#                         cols: 1
#                         # padding: self.parent.height * 0.01
#                         # canvas:
#                         #     Color:
#                         #         rgba: 1, 0, 0.5, 0.3
#                         #     Rectangle:
#                         #         size: self.size
#                         #         pos: self.pos
#                         Label:
#                             text: 'Alexis & Emilia'
#                             color: 0, 0, 0, 1
#                             font_name: '../res/fnt/Precious.ttf'
#                             font_size: self.parent.parent.width * 0.1
#                             size_hint: 1, None
#                             height: self.texture_size[1]
#                         AsyncImage:
#                             source: '../res/screens/stats/overlay_bar.png'
#                             allow_stretch: True
#                             size_hint: 0.6, 0.02
#                         GridLayout:
#                             cols: 3
#                             rows: 1
#                             Label:
#                                 text: 'Total Stats'
#                                 color: 1, 1, 1, 1
#                                 font_name: '../res/fnt/Precious.ttf'
#                                 font_size: root.width * 0.0175
#                                 size_hint: 0.25, None
#                                 height: self.texture_size[1]
#                             Label:
#                                 text: 'Total Abilities'
#                                 color: 1, 1, 1, 1
#                                 font_name: '../res/fnt/Precious.ttf'
#                                 font_size: root.width * 0.0175
#                                 size_hint: 0.25, None
#                                 height: self.texture_size[1]
#                             Label:
#                                 text: 'Rank Abilities'
#                                 color: 1, 1, 1, 1
#                                 font_name: '../res/fnt/Precious.ttf'
#                                 font_size: root.width * 0.0175
#                                 size_hint: 0.25, None
#                                 height: self.texture_size[1]
#                     GridLayout:
#                         rows: 1
#                         cols: 3
#                         AsyncImage:
#                             source: '../res/screens/attribute/ability_overlay.png'
#                             allow_stretch: True
#                             size_hint: 0.2, 0.3
#                         AsyncImage:
#                             source: '../res/screens/attribute/ability_overlay.png'
#                             allow_stretch: True
#                             size_hint: 0.25, 0.3
#                         AsyncImage:
#                             source: '../res/screens/attribute/ability_overlay.png'
#                             allow_stretch: True
#                             size_hint: 0.25, 0.3
#                     AsyncImage:
#                         source: '../res/screens/attribute/stat_overlay.png'
#                         allow_stretch: True
#                         size_hint: 0.8, 0.2
#                     GridLayout:
#                         rows: 3
#                         cols: 3
#                         AsyncImage:
#                             source: '../res/screens/attribute/equipment.png'
#                             allow_stretch: True
#                             size_hint: 0.25, 0.2
#                         AsyncImage:
#                             source: '../res/screens/attribute/equipment.png'
#                             allow_stretch: True
#                             size_hint: 0.25, 0.2
#                         AsyncImage:
#                             source: '../res/screens/attribute/equipment.png'
#                             allow_stretch: True
#                             size_hint: 0.25, 0.2
#                         AsyncImage:
#                             source: '../res/screens/attribute/equipment.png'
#                             allow_stretch: True
#                             size_hint: 0.25, 0.2
#                         AsyncImage:
#                             source: '../res/screens/attribute/equipment.png'
#                             allow_stretch: True
#                             size_hint: 0.25, 0.2
#                         AsyncImage:
#                             source: '../res/screens/attribute/equipment.png'
#                             allow_stretch: True
#                             size_hint: 0.25, 0.2
#                         AsyncImage:
#                             source: '../res/screens/attribute/equipment.png'
#                             allow_stretch: True
#                             size_hint: 0.25, 0.2
#                         AsyncImage:
#                             source: '../res/screens/attribute/equipment.png'
#                             allow_stretch: True
#                             size_hint: 0.25, 0.2
#                         AsyncImage:
#                             source: '../res/screens/attribute/equipment.png'
#                             allow_stretch: True
#                             size_hint: 0.2, 0.2
#
#
# ''')
#
# class MyWidget(Widget):
#     pass
#
# # class RippleLabel(TouchRippleBehavior, Label):
# #     def __init__(self, **kwargs):
# #         super(RippleLabel, self).__init__(**kwargs)
# #
# #     def on_touch_down(self, touch):
# #         collide_point = self.collide_point(touch.x, touch.y)
# #         if collide_point:
# #             touch.grab(self)
# #             self.ripple_show(touch)
# #             return True
# #         return False
# #
# #     def on_touch_up(self, touch):
# #         if touch.grab_current is self:
# #             touch.ungrab(self)
# #             self.ripple_fade()
# #             return True
# #         return False
# #
# #
# # class MyButton(ToggleButtonBehavior, Image):
# #     def __init__(self, **kwargs):
# #         super(MyButton, self).__init__(**kwargs)
# #         self.source = 'atlas://data/images/defaulttheme/checkbox_off'
# #     def on_state(self, widget, value):
# #         if value == 'down':
# #             self.source = 'atlas://data/images/defaulttheme/checkbox_on'
# #         else:
# #             self.source = 'atlas://data/images/defaulttheme/checkbox_off'
#
# class SampleApp(App):
#     def build(self):
#         return MyWidget()
#         # return RippleLabel()
#
# if __name__ == '__main__':
#     SampleApp().run()

from kivy.app import App
from kivy.properties import NumericProperty, StringProperty
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.relativelayout import RelativeLayout


class Kayout(RelativeLayout):
    words = StringProperty('Sexy Wanderers\nIt\nCave Dwellers\nBombshell\nDusk Sparkles\nStar Gazer\nTriwiz Champion\nSunny Day\nSterling\nSchool Girls\nSante Ynez\nBeach Celebrity\nCandy Cane\nCelebretaunt\nCertified Organic\nEnchanting Glamour')
    numbers = StringProperty('25.43%\n100.00%\n45.23%\n16.68%\n18.81%\n25.43%\n100.00%\n45.23%\n16.68%\n18.81%\n25.43%\n100.00%\n45.23%\n16.68%\n18.81%\n25.43%')
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

kv = """
<Kayout>:
    id: hint
    opacity: 1
    # size_hint: 0.92, 0.3434
    # pos_hint: {'center_x': 0.5, 'top': 0.9273}
    Image:
        source: '../res/screens/stats/hint_background.png'
        keep_ratio: False
        allow_stretch: True
    ScrollView:
        do_scroll_y: True
        do_scroll_x: False
        GridLayout:
            cols: 2
            size_hint_y: None
            cols_minimum: {0: hint.width * 0.65 - hint.height * 0.05, 1: hint.width * 0.35 - hint.height * 0.05}
            height: hint_text.height
            padding: hint.height * 0.05
            Label:
                id: hint_text
                size_hint: None, None
                color: 0, 0, 0, 1
                font_size: hint.height * 0.1625
                font_name: '../res/fnt/Gabriola.ttf'
                text: root.words
                text_size: self.width, None
                halign: 'left'
                size: self.texture_size
            Label:
                id: hint_numbers
                size_hint: None, None
                color: 0, 0, 0, 1
                font_size: hint.height * 0.0625
                font_name: '../res/fnt/Gabriola.ttf'
                text: root.numbers
                halign: 'right'
                text_size: self.width, None
                height: self.texture_size[1]
# BoxLayout:
    # Widget:
    #     Scatter:
    #         center: self.parent.center
    #         size: text.size
    #         do_rotation: False
    #         do_translation: False
    #         do_scale: False
    #         rotation: app.angle
    #         Label:
    #             id: text
    #             size: self.texture_size
    #             text: "test with scatter"
    # Widget:
    #     Label:
    #         center: self.parent.center
    #         size: self.texture_size
    #         canvas.before:
    #             PushMatrix
    #             Rotate:
    #                 angle: app.angle
    #                 origin: self.center
    #         canvas.after:
    #             PopMatrix
    #         text: "test with matrix transformation"
"""


class TextVerticalApp(App):
    # angle = NumericProperty(-90)


    def build(self):
        # Clock.schedule_interval(self.update_angle, 0)
        Builder.load_string(kv)
        return Kayout()

    # def update_angle(self, dt, *args):
    #     self.angle += dt * 100

if __name__ == '__main__':
    TextVerticalApp().run()