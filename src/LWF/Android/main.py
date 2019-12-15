from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.gesture import Gesture, GestureDatabase
from kivy.utils import platform
from kivy.config import Config
from kivy.clock import Clock

if platform == "win":
    import ctypes
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screen_size_raw = (int(user32.GetSystemMetrics(0)), int(user32.GetSystemMetrics(1)))
    screen_size = (screen_size_raw[0] * 2 / 3, screen_size_raw[1] * 2 / 3)
    print('Size is %f %f' % screen_size)
    Config.set('graphics', 'width', int(screen_size[0]))
    Config.set('graphics', 'height', int(screen_size[1]))
    Config.set('graphics', 'resizable', False)
from kivy.core.window import Window
if platform == "android":
    screen_size = Window.size
    print('Size is %f %f' % screen_size)


def simplegesture(name, point_list):
    """
    A simple helper function
    """
    g = Gesture()
    g.add_stroke(point_list)
    g.normalize()
    g.name = name
    return g

class Screen(FloatLayout):
    def __init__(self):
        print(screen_size)
        self.size_hint = None, None
        self.size = (int(screen_size[0] * 2 / 3), int(screen_size[1] * 2 / 3))
        self.pos = (int((screen_size[0] - self.width) / 2) , int((screen_size[1] - self.height) / 2))
        print(self.size)
        print(self.pos)
        super().__init__()
        self.gdb = GestureDatabase()
        self.fps = Label(text="FPS: ", font_size =screen_size[0]/20, size_hint=(None, None), pos=(screen_size[0]*.5,screen_size[1]*.9))
        print(self.fps.pos)
        self.add_widget(self.fps)
        Clock.schedule_interval(self.update_label, .5)
        self.draw_canvas = Widget()
        self.add_widget(self.draw_canvas)
        with self.draw_canvas.canvas:
            Color(1, 0, 0, 1)
            Rectangle(size=self.size, pos=self.pos)

    def on_resize(self, *args):
        global screen_size
        screen_size = Window.size
        self.size = (int(screen_size[0] * 2 / 3), int(screen_size[1] * 2 / 3))
        self.pos = (int((screen_size[0] - self.width) / 2) , int((screen_size[1] - self.height) / 2))
        self.draw_canvas.canvas.clear()
        self.fps.pos = (screen_size[0]*.5,screen_size[1]*.9)
        self.fps.font_size = screen_size[0]/20
        with self.draw_canvas.canvas:
            Color(1, 0, 0, 1)
            Rectangle(size=self.size, pos=self.pos)

    def update_label(self, dt):
        self.fps.text = "FPS: " + str(Clock.get_fps())

    def collide_point(self, x, y):
        return (x >= self.pos[0] and y >= self.pos[1] and x <= self.width+self.pos[0] and y <= self.height+self.pos[1])

    def on_touch_down(self, touch):
        # start collecting points in touch.ud
        # create a line to display the points
        if self.collide_point(touch.x, touch.y):
            userdata = touch.ud
            with self.draw_canvas.canvas:
                Color(1, 1, 0)
                d = 30.
                Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
                userdata['line'] = Line(points=(touch.x, touch.y), width=5)
            return True

    def on_touch_move(self, touch):
        # store points of the touch movement
        if self.collide_point(touch.x, touch.y):
            try:
                touch.ud['line'].points += [touch.x, touch.y]
                return True
            except (KeyError) as e:
                pass

    def on_touch_up(self, touch):
        # touch is over, display informations, and check if it matches some
        # known gesture.
        try:
            g = simplegesture('', list(zip(touch.ud['line'].points[::2],
                                           touch.ud['line'].points[1::2])))
            # gestures to my_gestures.py
            print("gesture representation: ", self.gdb.gesture_to_str(g))
            print("Points: ", touch.ud['line'].points)
        except(KeyError) as e:
            pass
        self.draw_canvas.canvas.clear()
        with self.draw_canvas.canvas:
            Color(1, 0, 0, 1)
            Rectangle(size=self.size, pos=self.pos)


class TestAppApp(App):
    def build(self):
        print("Init My App!")
        Window.bind(on_resize=self.on_resize)
        self.screen = Screen()
        return self.screen

    def on_resize(self, *args):
        print("Window Resized")
        self.screen.on_resize()

if __name__ == "__main__":
    TestAppApp().run()
