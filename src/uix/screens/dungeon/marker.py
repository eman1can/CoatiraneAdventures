from random import uniform

from kivy.properties import NumericProperty, OptionProperty

from kivy.animation import Animation
from kivy.graphics import MatrixInstruction, PopMatrix, PushMatrix
from kivy.graphics.transformation import Matrix

from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout


class Marker(RelativeLayout):
    type = OptionProperty('damage', options=['damage', 'crit_damage', 'health', 'mana', 'penetration', 'critical', 'counter', 'block', 'evade', 'resist', 'weak', 'null', 'dot'])
    value = NumericProperty(0)

    scale = NumericProperty(1)
    duration = NumericProperty(0)
    text_width = NumericProperty(280)

    def __init__(self, h, time_scale, **kwargs):
        super().__init__(**kwargs)

        str_value = str(self.value)

        self.opacity = 0.01

        self.canvas.before.add(PushMatrix())
        self.instruction = MatrixInstruction()
        self.instruction.matrix = Matrix()
        self.canvas.before.add(self.instruction)
        self.canvas.after.add(PopMatrix())

        if self.type in ('damage', 'dot', 'crit_damage', 'health', 'mana'):
            duration = (0.05 * len(str_value) + 0.35) / time_scale
            num_width = 21 * h / 56
            self.text_width = num_width * len(str_value)
            for index, char in enumerate(str_value):
                image = Image(size_hint=(num_width, 1), pos_hint={'center_x': (index) * num_width / self.text_width}, source=f'atlas://res/uix/markers/{self.type}_{char}')
                anim = Animation(duration=index * 0.05) + Animation(y=h / uniform(3, 5), t='out_expo', duration=0.05) + Animation(y=0, t='out_bounce', duration=0.1)
                anim.start(image)
                self.add_widget(image)

            if self.type == 'crit_damage':
                half = uniform(duration * 0.2, duration * 0.8)
                anim = Animation(scale=1 + uniform(0.25, 0.75), duration=half, t='out_expo') + Animation(scale=1, duration=duration - half, t='out_bounce')
                anim.start(self)
        else:
            image = Image(size_hint=(1, 1), pos_hint={'center_x': 0.5}, source=f'atlas://res/uix/markers/{self.type}')
            self.text_width = image.texture_size[0] * h / image.texture_size[1]
            self.add_widget(image)

            duration = (0.1 + 0.35) / time_scale

            half = uniform(duration * 0.2, duration * 0.8)
            anim = Animation(scale=1 + uniform(0.05, 0.25), duration=half, t='out_expo') + Animation(scale=1, duration=duration - half, t='out_bounce')
            anim.start(self)

        fade_in_duration = 0.1 / time_scale
        fade_out_duration = 0.2 / time_scale

        anim = Animation(opacity=1, duration=fade_in_duration) + Animation(duration=duration + fade_out_duration) + Animation(opacity=0, duration=fade_out_duration)
        anim.start(self)

        self.duration = duration
        self.width = self.text_width

    def on_scale(self, instance, scale):
        matrix = Matrix()
        matrix.scale(scale, scale, 1)
        matrix.translate((-scale + 1) * 0.5 * self.width, -scale * self.height / 4, 0)
        self.instruction.matrix = matrix

    def on_opacity(self, instance, value):
        if value == 0:
            self.parent.remove_widget(self)
        else:
            for child in self.children:
                child.opacity = self.opacity