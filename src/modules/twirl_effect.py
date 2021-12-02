from kivy.clock import Clock
from kivy.properties import BooleanProperty, NumericProperty
from kivy.uix.effectwidget import EffectBase, shader_footer_effect, shader_header

uniforms = '''
uniform float alpha;
uniform float red;
uniform float blue;
uniform float green;
uniform float time;
uniform float strength;
'''

effect_twirl = '''
vec4 effect(vec4 color, sampler2D texture, vec2 tex_coords, vec2 coords) {{
    vec2 delta = tex_coords - vec2(0.5, 0.5);
    float angle = strength * length(delta);
    
    float x = cos(angle) * delta.x - sin(angle) * delta.y;
    float y = sin(angle) * delta.x + cos(angle) * delta.y;
    
    vec2 uv = vec2(x + 0.5, y + 0.5);
    
    vec3 col = texture2D(texture, uv).rgb;
    
    return vec4(col.x, col.y * red, col.z * red, alpha);
}}
'''


class TwirlEffect(EffectBase):
    length = NumericProperty(1.5)
    strength = NumericProperty(20)
    tintr = BooleanProperty(False)

    def __init__(self, *args, **kwargs):
        self.register_event_type('on_update')
        self.register_event_type('on_end')
        super(TwirlEffect, self).__init__(*args, **kwargs)
        self.do_glsl()

        self.time = 0
        self.direction = 1
        self.time_scale = 1

    def on_size(self, *args):
        self.do_glsl()

    def do_glsl(self):
        self.glsl = effect_twirl

    def play(self, time_scale):
        self.time = 0
        self.direction = 1
        self.time_scale = time_scale
        Clock.schedule_interval(self.update_variables, 1 / 30)

    def pause(self):
        Clock.unschedule(self.update_variables)

    def resume(self):
        Clock.schedule_interval(self.update_variables, 1 / 30)

    def on_update(self):
        pass

    def on_end(self):
        pass

    def update_variables(self, dt):
        if self.fbo is None:
            return
        self.time += dt * self.direction * self.time_scale
        if self.time > self.length:
            self.dispatch('on_update')
            self.direction = -1
        if self.time < 0:
            Clock.unschedule(self.update_variables)
            self.dispatch('on_end')
            self.time = 0

        self.fbo['alpha'] = 1.0 - self.time / self.length
        if self.tintr:
            self.fbo['red'] = 1.0 - self.time / self.length
        self.fbo['strength'] = self.time / self.length * self.strength

    def set_fbo_shader(self, *args):
        if self.fbo is None:
            return
        self.fbo['alpha'] = 1.0
        self.fbo['red'] = 1.0
        self.fbo['strength'] = 0.0
        self.fbo.set_fs(shader_header + uniforms + self.glsl + shader_footer_effect)
