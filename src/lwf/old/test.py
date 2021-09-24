from kivy.app import App
from kivy.graphics import MatrixInstruction, PopMatrix, PushMatrix, Rectangle
from kivy.graphics.transformation import Matrix
from kivy.uix.widget import Widget


class Window(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            PushMatrix()
            mi = MatrixInstruction()
            matrix = Matrix()
            matrix.translate(200, 200, 0)
            matrix.scale(1.4, 0.75, 1)
            print(matrix[0])
            matrix[0] = 2
            print(matrix[0])
            mi.matrix = matrix

        with self.canvas:
            Rectangle(size=(100, 100))

        with self.canvas.after:
            PopMatrix()


class MatrixTest(App):
    def build(self):
        widget = Widget()
        other = Widget()
        widget.add_widget(other)
        widget.remove_widget(other)


        return Window()


if __name__ == "__main__":
    MatrixTest().run()

#######################################

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder


class Window(Widget):
    pass


root = """
#:import Matrix kivy.graphics.transformation.Matrix
Window:
    canvas.before:
        PushMatrix:
        MatrixInstruction:
            matrix: Matrix().translate(200, 200, 0)
    canvas:
        Rectangle:
            size: 100, 100
    canvas.after:
        PopMatrix:
"""


class MatrixTest(App):
    def build(self):
        return Builder.load_string(root)


if __name__ == "__main__":
    MatrixTest().run()
