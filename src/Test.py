from kivy.uix.label import Label
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import NumericProperty
from kivy.uix.behaviors import DragBehavior
from kivy.lang import Builder

# # You could also put the following in your kv file...
# kv = '''
# <DragLabel>:
#     # Define the properties for the DragLabel
#     drag_rectangle: self.x, self.y, self.width, self.height
#     drag_timeout: 10000000
#     drag_distance: 0
#
# FloatLayout:
#     # Define the root widget
#     DragLabel:
#         size_hint: 0.25, 0.2
#         text: 'Drag me'
# '''
#
#
# class DragLabel(DragBehavior, Label):
#     pass
class Wid:
    a = NumericProperty(0)
    def __init__(self, **kwargs):
        super().__init__()
        # self.add_widget(Button(on_touch_down=self.on_down))
        Clock.schedule_once(self.on_down, 3)

    def on_down(self, dt):
        print(self.a)

class TestApp(App):
    def build(self):
        return Wid(a=100)

TestApp().run()