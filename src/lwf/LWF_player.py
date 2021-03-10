# Internal Imports
# External Imports
# import random
from kivy import Config
# from kivy.graphics.instructions import RenderContext

from src.lwf.kivy.node import LWFNode

Config.set('graphics', 'width', 1706)
Config.set('graphics', 'height', 960)

from kivy.app import App
# from kivy.clock import Clock
# from kivy.graphics.context_instructions import Color
# from kivy.graphics.vertex_instructions import Rectangle
# from kivy.uix.button import Button
# from kivy.uix.floatlayout import FloatLayout
# from kivy.uix.image import Image
from kivy.uix.widget import Widget

# from src.lwf.core.data import Data
# from src.lwf.core.lwf import LWF
# from src.lwf.renderer import KivyFactory, ResourceCache


class WindowObject(Widget):
    def __init__(self):
        super().__init__()
        node = LWFNode('../../res/lwf/character_active.lwf')
        node.pos = (100, 100)
        node.lwf.fit_for_height(10, 10)
        self.add_widget(node)
    # def __init__(self):
    #     self.lwf = None
    #     self.playing = False
    #     self.count = 0
    #     super().__init__()
    #     with self.canvas:
    #         Color(0, 0, 0, 1)
    #         Rectangle(size=(5000, 5000))
    #
    #     # self.add_widget(Image(size_hint=(None, None), size=(173, 173), pos=(13, 13), source="C:/Users/ethan/PycharmProjects/CoatiraneAdventures/res/characters/test/bedtime_artemis/bedtime_artemis_preview.png"))
    #     # self.add_widget(Image(size_hint=(None, None), size=(1706, 960), pos=(0, 0), source="C:/Users/ethan/PycharmProjects/CoatiraneAdventures/res/screens/backgrounds/charattributebg.png", allow_stretch=True, keep_ratio=False))
    #
    #     layout = FloatLayout()
    #     button = Button(size_hint=(None, None), pos=(0, 600), size=(100, 100), text="Push me!", on_release=lambda instance: self.stop_start())
    #     layout.add_widget(button)
    #     self.add_widget(layout)
    #     self.play_lwf()
    #
    # def play_lwf(self):
    #     stage = Widget()
    #     stage.width = 200
    #     stage.height = 200
    #     # stage.canvas = RenderContext()
    #     self.add_widget(stage)
    #
    #     path = '../../res/lwf/'
    #     local_path = ''
    #     name = 'character_active.lwf'
    #     filename = path + local_path + name
    #     cache = ResourceCache.sharedLWFResourceCache()
    #     data = cache.loadLWFData(filename)
    #     data.set_path(path + local_path)
    #
    #     factory = KivyFactory(data, stage.canvas)
    #
    #     self.lwf = LWF(data, factory)
    #     if name == 'yellow_all.lwf':
    #         self.lwf.render_offset = 400, 100
    #         self.lwf.scaleX, self.lwf.scaleY = 10, 10
    #     elif name == 'light_all.lwf':
    #         self.lwf.render_offset = 400, 100
    #         self.lwf.scaleX, self.lwf.scaleY = 10, 10
    #     elif name == 'earth_all.lwf':
    #         self.lwf.render_offset = 400, 100
    #         self.lwf.scaleX, self.lwf.scaleY = 10, 10
    #     elif name == 'assist_cutin.lwf' or name == 'active_cutin.lwf':
    #         self.lwf.render_offset = 0, 0
    #         self.lwf.scaleX, self.lwf.scaleY = 1920, 1080
    #     else:
    #         self.lwf.render_offset = 100, 100
    #         self.lwf.scaleX, self.lwf.scaleY = 10, 10
    #
    #     self.lwf.SetFrameRate(30)
    #     width, height = self.lwf.width, self.lwf.height
    #     print("Size: ", width, height)
    #     print("Scale: ", self.lwf.scaleX, self.lwf.scaleY)
    #     # self.lwf.ScaleForWidth(width)
    #     # self.lwf.ScaleForWidth(height)
    #     self.lwf.FitForHeight(self.lwf.scaleX, self.lwf.scaleY)
    #     # self.lwf.ScaleForWidth(self.lwf.scaleY)
    #     # self.lwf.ScaleForWidth(1706)
    #     # self.lwf.ScaleForHeight(960)
    #     # self.lwf.rootMovie.MoveTo(256, 400)
    #     self.lwf.rootMovie.SetVisible(True)
    #     Clock.schedule_interval(self.update, 1 / 60)
    #
    # def update(self, dt):
    #     if self.lwf is not None:
    #         self.lwf.Exec(dt)
    #         self.lwf.Render()
    #
    # def stop_start(self):
    #     if self.lwf.rootMovie.playing:
    #         self.lwf.rootMovie.Stop()
    #     else:
    #         self.lwf.rootMovie.Play()


class LWFPlayer(App):
    def build(self):
        return WindowObject()

if __name__ == "__main__":
    window = LWFPlayer().run()