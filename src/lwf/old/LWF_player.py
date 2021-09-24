# Internal Imports
# External Imports
# import random
import threading

from time import time

from kivy.cache import Cache
from kivy.clock import Clock
from kivy.graphics import Color, Mesh, PopMatrix, PushMatrix, Rectangle, Rotate, Translate, MatrixInstruction
from kivy.graphics.transformation import Matrix

from kivy.properties import NumericProperty

from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.uix.label import Label

from lwf.core import Data, LWF
from lwf.filelogger import log, logToFile
from lwf.kivy.kivy_factory import KivyRendererFactory
from src.lwf.kivy.node import LWFNode

from kivy import Config

# from kivy.graphics.instructions import RenderContext

Config.set('graphics', 'width', 1920)
Config.set('graphics', 'height', 1080)

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


class Character(Widget):
    def __init__(self, name, offset):
        super().__init__()

        player = Image(source=f'../../res/characters/{name}/{name}_preview.png', keep_ratio=False, allow_stretch=True)
        player.size = (200, 200)
        player.pos = (200 + offset, 45)

        self.add_widget(player)

        frame = Image(source='../../res/uix/screens/dungeon_battle/special_background.png', keep_ratio=False, allow_stretch=True)
        frame.size = (200, 220)
        frame.pos = (200 + offset, 25)
        self.add_widget(frame)

        health = Image(source='../../res/uix/screens/dungeon_battle/special_background.png', keep_ratio=False, allow_stretch=True)
        health.size = (200, 220)
        health.pos = (200 + offset, 25)
        self.add_widget(health)

        mana = Image(source='../../res/uix/screens/dungeon_battle/special_foreground.png', keep_ratio=False, allow_stretch=True)
        mana.size = (200, 220)
        mana.pos = (200 + offset, 25)
        self.add_widget(mana)

        self.node = LWFNode.create('../../res/lwf/character_active.lwf')
        self.node.pos = (300 + offset, 145)
        self.node.lwf.scale_for_width(10 * 200 / 180, 10 * 200 / 180)
        self.add_widget(self.node)


class WindowObject(Widget):
    def __init__(self):
        super().__init__()

        def load_LWF_data(path):
            try:
                file = open(path, 'rb')
                binary = file.read()
                data = Data(binary, len(binary))
                file.close()
                return data
            except Exception:
                return None

        self.display = Widget()
        # display.pos = (0, 250)
        self.add_widget(self.display)

        factory = KivyRendererFactory(self.display, '../../res/lwf', self.load_texture)

        self.lwfs = []

        data = load_LWF_data('../../res/lwf/character_active.lwf')
        cutin1 = LWF(data, factory)
        cutin1.property.move(150, 150)
        self.lwfs.append(cutin1)
        # cutin4 = LWF(data, factory)

        # cutin1.set_preferred_frame_rate(30)
        # cutin2 = LWF(data, factory)
        # cutin3 = LWF(data, factory)
        # self.lwfs.append(cutin2)
        # self.lwfs.append(cutin3)
        # self.lwfs.append(cutin4)

        # cutin2.property.move(0, 861)
        # cutin3.property.move(0, 668)
        # cutin4.property.move(0, 475)

        # self.node = LWFNode.create('../../res/lwf/assist_cutin.lwf', factory)
        # self.node.pos = (0, 1054)
        # self.node.
        # self.node2 = LWFNode.create('../../res/lwf/assist_cutin.lwf')
        # self.node2.pos = (0, 861)
        # self.node3 = LWFNode.create('../../res/lwf/assist_cutin.lwf')
        # self.node3.pos = (0, 668)
        # self.node4 = LWFNode.create('../../res/lwf/assist_cutin.lwf')
        # self.node4.pos = (0, 475)

        # self.node.lwf.scale_for_width(1706, 960)
        # self.add_widget(self.node)
        # self.add_widget(self.node2)
        # self.add_widget(self.node3)
        # self.add_widget(self.node4)

        self.add_widget(Button(on_release=lambda button: self.stop_start(), pos=(0, 750)))

        # background = Image(source='../../res/uix/screens/dungeon_battle/background.png', keep_ratio=False, allow_stretch=True)
        # background.size = (1920, 1080)
        # self.add_widget(background)
        #
        # names = ['hero_bell', 'catty_chloe', 'badass_ais', 'siren_song_riveria']
        # self.characters = []
        # for x, name in enumerate(names):
        #     character = Character(name, x * 250)
        #     self.characters.append(character)
        #     self.add_widget(character)

        Clock.schedule_interval(lambda dt: self.update(dt), 1 / 30)
        Clock.schedule_interval(lambda dt: self.render(), 1 / 30)

        Cache.register('textures')

    def load_texture(self, filename):
        texture = Cache.get('textures', filename)
        if texture is not None:
            return texture
        if filename == 'lwf_img_replace_character_01.png':
            texture = CoreImage('../../res/characters/washed_out_cassandra/washed_out_cassandra_bustup.png').texture
        else:
            texture = CoreImage('../../res/lwf/' + filename).texture
        Cache.append('textures', filename, texture)
        return texture

    def update(self, dt):
        for lwf in self.lwfs:
            if lwf.root_movie.playing:
                lwf.exec(dt)

    def render(self):
        self.display.canvas.clear()
        for lwf in self.lwfs:
            lwf.render()


    def stop_start(self):
        for lwf in self.lwfs:
            if lwf.root_movie.playing:
                lwf.root_movie.stop()
            else:
                lwf.root_movie.play()


class LWFPlayer(App):
    def build(self):
        return WindowObject()


if __name__ == "__main__":
    window = LWFPlayer().run()
