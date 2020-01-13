from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget

from spine.Skeleton.SkeletonRenderer import SkeletonRenderer
from spine.Atlas.Sprite import Sprite


class MainScreen(Widget):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.skeleton_renderer = renderer = SkeletonRenderer()
        renderer.scale = 2
        renderer.load('C:/Users/Zoe Wolfe/PycharmProjects/CoatiraneAdventures/lwfsrc/data/dragon')
        renderer.skeleton.x = 1200
        renderer.skeleton.y = 400
        renderer.state.setAnimation(0, 'flying', True)
        with self.canvas:
            Color(1,1,1,1)
            Rectangle(size=(2000,2000),pos=(0,0))
        renderer.draw(self.canvas, 0)




    def update(self, dt):
        self.canvas.clear()
        self.skeleton_renderer.draw(self.canvas, dt)


class SpineBoyApp(App):

    def build(self):
        return MainScreen()

    def on_start(self):
        super(SpineBoyApp, self).on_start()
        Clock.schedule_interval(self.root.update, 1 / 60)

    def on_stop(self):
        super(SpineBoyApp, self).on_stop()
        Clock.unschedule(self.root.update)


if __name__ == '__main__':
    SpineBoyApp().run()