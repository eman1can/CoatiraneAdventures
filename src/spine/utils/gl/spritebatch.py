from kivy.graphics.shader import Shader

from src.spine.utils.gl.vertexattribute import ShaderProgram


class SpriteBatch:
    @staticmethod
    def createDefaultShader():
        fragmentShader = '''
#ifdef GL_ES
#define LOWP lowp
precision mediump float;
#else
#define LOWP 
#endif
varying LOWP vec4 v_color;
varying vec2 v_texCoords;
uniform sampler2D u_texture;
void main(){
    gl_FragColor = v_color * texture2D(u_texture, v_texCoords);
}
'''
        vertexShader = '''
attribute vec4 a_position;
attribute vec4 a_color;
attribute vec2 a_texCoord0;

uniform mat4 u_projTrans;
varying vec4 v_color;
varying vec2 v_texCoords;
void main(){
    v_color = a_color;
    v_color.a = v_color.a * (255.0 / 254.0);
    v_texCoords = a_texCoord0;
    gl_Position = u_projTrans * a_position;
}
'''
        shader = ShaderProgram(vertexShader, fragmentShader)
        if not shader.isCompiled():
            raise Exception("Error compiling shader!", shader.getLog())
        return shader