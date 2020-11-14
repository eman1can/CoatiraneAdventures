from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import *
from kivy.graphics.opengl import *
from kivy.graphics.transformation import Matrix
from kivy.logger import Logger
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget


class World(Widget) :
    def __init__(self, **kwargs):
        Logger.debug('world.init()')

        # Parent RenderContext for subsuming all other render contexts
        self.prc=RenderContext()
        proj_mat = Matrix()
        proj_mat.look_at(0.,0.,1., # eye position coords
                         0.,0.,0.,  # looking at these coords
                         0,1.,0)    # a vector that points up

        if Window.height > Window.width :
            self.xRadius = float(Window.width)/Window.height
            self.yRadius = 1.0
            proj_mat.scale(1.0/self.xRadius,1.0,1.0)
        else :
            self.xRadius = 1.0
            self.yRadius = float(Window.height)/Window.width
            proj_mat.scale(1.0,1.0/self.yRadius,1.0)

        self.prc['projection_mat'] = proj_mat

        ## an effect shader used to make objects monochromatic (grayscale)
        self.prc.shader.fs = """
#ifdef GL_ES
precision highp float;
#endif

/* Outputs from the vertex shader */
varying vec4 frag_color;
varying vec2 vTexCoords0;

/* uniform texture samplers */
uniform sampler2D texture0;

uniform vec2 resolution;
uniform float time;

void main() {
  vec4 rgb = texture2D(texture0, vTexCoords0);
  float c = (rgb.x + rgb.y + rgb.z) * 0.3333;
  gl_FragColor = vec4(c, c, c, 1.0);
}
"""

        if not self.prc.shader.success :
            raise Exception('Effect shader compile failed.')

        self.canvas = self.prc

        m = Matrix()
        m2 = Matrix()
        m2.set(array=[
    [1.0, 1.0, 0.0, 0.0],
    [1.0, 1.0, 0.0, 0.0],
    [0.0, 0.0, 1.0, 0.0],
    [0.0, 0.0, 0.0, 1.0]])
        m.multiply(m2)


        ## Left Rectangle drawn with its own RenderContext
        ## this is not affected by the effect shader (if it were, it would be drawn as white)
        ## but it is affected by the parent's projection matrix
        self.spriteRC = RenderContext(use_parent_projection=True)
        # self.spriteRC.us
        self.spriteRC.add(Color(1,0,0,1))
        self.spriteRC.add(Rectangle(pos=(-0.25,0.0),size=(0.1,0.1)))

        ## Right Rectangle object drawn directly to the canvas
        ## this **is** affected by the effect shader
        self.canvas.add(Color(1,0,0,1))
        self.canvas.add(Rectangle(pos=(0.25,0),size=(0.1,0.1)))
        self.canvas.add(self.spriteRC)



        super(World, self).__init__(**kwargs)

class GameApp(App):
    def build(self):
        w = World()
        fl = FloatLayout()
        fl.add_widget(w)
        return fl

if __name__ == '__main__':
    GameApp().run()