'''
Mesh test
=========

This demonstrates the use of a mesh mode to distort an image. You should see
a line of buttons across the bottom of a canvas. Pressing them displays
the mesh, a small circle of points, with different mesh.mode settings.
'''

from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.graphics import Mesh, Color, Rectangle
from kivy.core.image import Image
from functools import partial
from math import cos, sin, pi


class MeshTestApp(App):

    def change_mode(self, mode, *largs):
        self.mesh.mode = mode

    def build_mesh(self):
        """ returns a Mesh of a rough circle. """
        self.mesh = None
        self.x = 500
        self.y = 500
        self.width = 400
        self.height = 400
        self.amount = 10
        vertices = []
        indices = []
        step = self.amount
        istep = (pi * 2) / float(step)
        for i in range(step):
            x = self.x + cos(istep * i) * self.width
            y = self.y + sin(istep * i) * self.height
            vertices.extend([x, y, 0, 0])
            indices.append(i)
        return Mesh(vertices=vertices, indices=indices)

    def OnSliderAmount(self, slider, *largs):
        self.amount = int(slider.value)
        self.update()

    def OnSliderX(self, slider, *largs):
        self.x = int(slider.value)
        self.update()

    def OnSliderY(self, slider, *largs):
        self.y = int(slider.value)
        self.update()

    def OnSliderWidth(self, slider, *largs):
        self.width = int(slider.value)
        self.update()

    def OnSliderHeight(self, slider, *largs):
        self.height = int(slider.value)
        self.update()

    def update(self):
        vertices = []
        indices = []
        step = self.amount
        istep = (pi * 2) / float(step)
        for i in range(step):
            x = self.x + cos(istep * i) * self.width
            y = self.y + sin(istep * i) * self.height
            vertices.extend([x, y, 0, 0])
            indices.append(i)
        print("Mesh(vertices=", vertices, ", indices=", indices, ")")
        self.mesh.vertices = vertices
        self.mesh.indices = indices


    def build(self):
        wid = Widget()
        texture = Image('data/1041042001.png').texture
        texture.flip_vertical()
        # with wid.canvas:

            # self.mesh = self.build_mesh()

        layout = BoxLayout(size_hint=(1, None), height=50)
        for mode in ('points', 'line_strip', 'line_loop', 'lines',
                'triangle_strip', 'triangle_fan'):
            button = Button(text=mode)
            button.bind(on_release=partial(self.change_mode, mode))
            layout.add_widget(button)
        slider = Slider(min = 1, max = 50, value = 2)
        slider.bind(value=self.OnSliderAmount)
        layout.add_widget(slider)
        slider = Slider(min=400, max=1000, value=500)
        slider.bind(value=self.OnSliderX)
        layout.add_widget(slider)
        slider = Slider(min=400, max=1000, value=500)
        slider.bind(value=self.OnSliderY)
        layout.add_widget(slider)
        slider = Slider(min=1, max=1000, value=100)
        slider.bind(value=self.OnSliderWidth)
        layout.add_widget(slider)
        slider = Slider(min=1, max=1000, value=100)
        slider.bind(value=self.OnSliderHeight)
        layout.add_widget(slider)

        root = BoxLayout(orientation='vertical')
        root.add_widget(wid)
        root.add_widget(layout)

        return root

if __name__ == '__main__':
    MeshTestApp().run()