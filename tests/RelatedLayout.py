from kivy.app import App
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivy.lang.builder import Builder


class Main(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class EquipmentDisplay(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MainApp(App):
    def build(self):
        print(Window.size)
        Builder.load_file('equip.kv')
        return Main()


if __name__ == '__main__':
    MainApp().run()