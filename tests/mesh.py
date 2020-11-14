'''
Mesh test
=========

This demonstrates the use of a mesh mode to distort an image. You should see
a line of buttons across the bottom of a canvas. Pressing them displays
the mesh, a small circle of points, with different mesh.mode settings.
'''

from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.graphics import Mesh
from functools import partial
from math import cos, sin, pi


class MeshTestApp(App):

    def change_mode(self, mode, *largs):
        self.mesh.mode = 'triangle_fan'

    def build_mesh(self):
        """ returns a Mesh of a rough circle. """
        vertices = [200,100,0,0,400,100,0,0,400,300,0,0,300,375,0,0,200,300,0,0]
        indices = [0,1,2,3,4]
        return Mesh(vertices=vertices, indices=indices)

    def build(self):
        wid = Widget()
        with wid.canvas:
            self.mesh = self.build_mesh()

        layout = BoxLayout(size_hint=(1, None), height=50)
        for mode in ('triangle_fan', 'points', 'line_strip', 'line_loop', 'lines',
                'triangle_strip'):
            button = Button(text=mode)
            button.bind(on_release=partial(self.change_mode, mode))
            layout.add_widget(button)

        root = BoxLayout(orientation='vertical')
        root.add_widget(wid)
        root.add_widget(layout)

        return root


if __name__ == '__main__':
    MeshTestApp().run()