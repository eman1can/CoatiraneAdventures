from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from os.path import join

from kivy.uix.button import Button
from kivy.lang import Builder

class MainScreen(Widget):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        # self.skeleton_renderer = renderer = SkeletonRenderer()
        # renderer.scale = 1.0
        # renderer.load(join('assets', 'goblins-ffd'))
        # renderer.skeleton.set_skin_by_name('goblin')
        # renderer.skeleton.x = 320
        # renderer.skeleton.y = 100
        # self.skeleton_renderer.sprites = [Sprite() for _ in self.skeleton_renderer.skeleton.slots]
        # self.skeleton_renderer.state.set_animation_by_name(0, 'walk', True)
        # for sprite in self.skeleton_renderer.sprites:
        #     self.canvas.add(sprite)
        # for x in range(10):
        #     renderer.update(x)

    def update(self, dt):
        print("update", dt)
        self.skeleton_renderer.update(dt)

    def playanimation(self):
        print("animating")
        Clock.schedule_interval(self.update, 0)


        # self.canvas.clear()
        # for sprite in self.skeleton_renderer.sprites:
        #     self.canvas.add(sprite)


class GoblinsFFDApp(App):

    def build(self):
        screen = MainScreen()
        return screen

    def on_start(self):
        super(GoblinsFFDApp, self).on_start()
        

    def on_stop(self):
        super(GoblinsFFDApp, self).on_stop()
        Clock.unschedule(self.root.update)


if __name__ == '__main__':
    GoblinsFFDApp().run()
