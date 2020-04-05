from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout

class Constraint:
    def torOf(self, object, object2, offset):
        pos_x = object2.pos_hint['x']
        return pos_x + 0.2

class Canvas(RelativeLayout):
    pass


class MainApp(App):
    def build(self):
        return Canvas()


if __name__ == '__main__':
    MainApp().run()