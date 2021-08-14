# Internal Imports
# External Imports
# import random
from kivy.clock import Clock
from kivy.graphics import Color, PopMatrix, PushMatrix, Rectangle, Rotate, Translate, MatrixInstruction
from kivy.graphics.transformation import Matrix
from lwf.filelogger import log, logToFile
from src.lwf.kivy.node import LWFNode

from kivy import Config

# from kivy.graphics.instructions import RenderContext

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

        logToFile()

        # with self.canvas.before:
        #     PushMatrix()
        #     # Rotate(angle=45, origin=(20, 20))
        #     Translate(100, 100)
        #     self.mat = Matrix()
        #     # self.mat = self.mat.translate(100, 100, 0)
        #     self.mat = self.mat.set(flat=[1, 2.17, 0, 0,
        #                        0, 1, 0, 0,
        #                        0, 0, 1, 0,
        #                        100, 100, 0, 1])
        #     MatrixInstruction(matrix=self.mat)
        #
        # with self.canvas.after:
        #     PopMatrix()

        node = LWFNode.create('../../res/lwf/character_active.lwf')
        node.pos = (200, 200)
        # node.size = (200, 200)
        # node.lwf.fit_for_height(20, 20)

        # node.update(1)

        # node.visit(None, node._transform, None)

        self.add_widget(node)


        # node.visit(None, node._transform, None)

        # update_deltas = [0.042423, 0.044783, 0.031518, 0.034307, 0.028448, 0.031584, 0.032400, 0.041404, 0.041656, 0.041068, 0.045171, 0.044048, 0.036450, 0.030402, 0.024911, 0.025063, 0.024154, 0.013213, 0.030207, 0.026824, 0.014666, 0.025708, 0.022744, 0.014492, 0.023680, 0.013483, 0.021602, 0.012371, 0.025569, 0.021310, 0.020283, 0.040956, 0.034402, 0.034646, 0.035027, 0.032585, 0.029650, 0.032364, 0.031493, 0.031000, 0.030388, 0.029674, 0.026630, 0.013514, 0.024741, 0.034577, 0.031327, 0.023804, 0.018322, 0.031243, 0.030348, 0.029123, 0.023793, 0.016090, 0.023338, 0.013178, 0.026939, 0.021660, 0.018905, 0.023179, 0.023418, 0.011298, 0.024697, 0.014165, 0.029901, 0.028813, 0.010884, 0.024726, 0.027376, 0.009450, 0.024820, 0.012599, 0.022810, 0.013167, 0.028998, 0.027670, 0.021240, 0.013907, 0.024154, 0.011042, 0.023091, 0.012888, 0.022795, 0.015262, 0.025739, 0.027654, 0.011398, 0.024839, 0.024632, 0.011037, 0.023530, 0.014359, 0.000000, 0.055242, 0.050352, 0.032543, 0.028998, 0.029755, 0.022728, 0.047053, 0.039190, 0.037550, 0.023630, 0.032431, 0.029830, 0.014586, 0.030123, 0.029281, 0.028304, 0.031263, 0.019409, 0.029487, 0.029779, 0.029234, 0.053103, 0.054284, 0.044794, 0.034039, 0.033459, 0.036899, 0.034971, 0.039775, 0.034534, 0.037194, 0.038869, 0.034722, 0.026871, 0.025512, 0.029378, 0.020020, 0.029259, 0.025305, 0.032184, 0.038013, 0.031717, 0.023663, 0.013650, 0.025227, 0.030558, 0.028358, 0.014156, 0.032767, 0.030197, 0.029608, 0.023887, 0.013029, 0.025854, 0.012253, 0.023666, 0.025880, 0.016094]

        # update_deltas = [1.030973]

        # for delta in update_deltas:
        #     node.update(delta)

        Clock.schedule_interval(lambda dt: node.update(dt), 1 / 30)
        # Clock.schedule_interval(30, )

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
