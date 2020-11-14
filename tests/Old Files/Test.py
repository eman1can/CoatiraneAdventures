from kivy.app import App
from kivy.uix.widget import Widget
import ctypes
import math
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition

class filledcharacterpreview(Screen):
    pass
class emptycharacterpreview(Screen):
    pass
class scrollcharacterpreview(Screen):
    pass
class characterpreview(Widget):
    pass
class characterpreviewbox(ScreenManager):
    pass
class blankscreen(Screen):
    pass
class myscreenmanager(ScreenManager):
    transition = FadeTransition(duration=0.15)

class AdventureApp(App):
    title = 'Coatirane Adventures'

    def build(self):
        user32 = ctypes.windll.user32
        width = math.floor(user32.GetSystemMetrics(0) * 2 / 3)
        height = math.floor(user32.GetSystemMetrics(1) * 2 / 3)
        Window.size = (width, height)
        Window.left = math.floor((user32.GetSystemMetrics(0) - width) / 2)
        Window.top = math.floor((user32.GetSystemMetrics(1) - height) / 2)
        Window.borderless = 0
        return myscreenmanager()


if __name__ == '__main__':
    AdventureApp().run()