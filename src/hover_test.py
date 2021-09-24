from kivy.app import App
from kivy.uix.hoverbutton import HoverButton
from kivy.uix.relativelayout import RelativeLayout


class TestObject(HoverButton):
    def __init__(self, name, **kwargs):
        self.name = name
        self.text = name
        super().__init__(**kwargs)

    def __str__(self):
        return f'{self.name}, {self.x}, {self.y}, {self.right}, {self.top}'

    def on_enter(self):
        self.background_color = 1, 0, 0, 1

    def on_exit(self):
        self.background_color = 1, 1, 1, 1


class HoverApp(App):
    def build(self):
        widget = RelativeLayout()
        test_button = TestObject('1', size_hint=(0.25, 0.2), pos_hint={'x': 0, 'y': 0})
        test_button2 = TestObject('2', size_hint=(0.2, 0.1), pos_hint={'x': 0.4, 'y': 0})
        test_button3 = TestObject('3', size_hint=(0.5, 0.5), pos_hint={'x': 0.5, 'y': 0.5})
        test_button4 = TestObject('4', size_hint=(0.2, 0.2), pos_hint={'x': 0.6, 'y': 0.6}, layer=1, blocking=False)
        test_button5 = TestObject('5', size_hint=(0.2, 0.1), pos=(0.6 * 1706, 0.75 * 960))
        test_button6 = TestObject('6', size_hint=(0.2, 0.2), pos_hint={'x': 0.65, 'y': 0.7}, layer=2, blocking=False)
        widget.add_widget(test_button)
        widget.add_widget(test_button2)
        widget.add_widget(test_button3)
        test_button3.add_widget(test_button5)
        widget.add_widget(test_button4)
        widget.add_widget(test_button6)
        return widget


if __name__ == "__main__":
    HoverApp().run()
