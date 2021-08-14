from os import getcwd, listdir

from kivy import Config
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout

from lwf.lwf import LWF
from lwf.format.data import Data
from lwf.renderer import RendererFactory

Config.set('graphics', 'width', 1706)
Config.set('graphics', 'height', 960)

from kivy.cache import Cache
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.core.image import Image as CoreImage


from kivy.app import App
from kivy.uix.widget import Widget


root = '''
<WindowObject>:
    RelativeLayout:
        id: gui
        opacity: 1
        Button:
            font_size: '15pt'
            font_name: 'Gabriola'
            text: 'Stop / Start'
            size_hint: 0.1, 0.05
            pos_hint: {'top': 1}
            on_release: root.stop_start()
        TextInput:
            hint_text: 'Size'
            size_hint: 0.05, 0.05
            pos_hint: {'top': 0.95}
            font_size: '15pt'
            font_name: 'Gabriola'
            multiline: False
            write_tab: False
            on_text_validate: root.change_size(self.text)
        TextInput:
            font_size: '15pt'
            font_name: 'Gabriola'
            hint_text: 'Pos'
            size_hint: 0.05, 0.05
            pos_hint: {'top': 0.95, 'x': 0.05}
            multiline: False
            write_tab: False
            on_text_validate: root.change_pos(self.text)
        Label:
            id: playing
            text: 'Playing: None'
            font_size: '15pt'
            font_name: 'Gabriola'
            size_hint: 0.1, None
            width: self.texture_size[0]
            pos_hint: {'top': 0.9}
        RecycleView:
            id: list
            size_hint: 0.1, 0.8
            viewclass: 'Button'
            RecycleBoxLayout:
                default_size: None, dp(56)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
    Image:
        source: '../res/characters/clumsy_cassandra/clumsy_cassandra_preview.png'
        size_hint: None, None
        size: 170, 170
        pos: root.width * 0.1 + 10, 10
    Widget:
        id: display
        size_hint: 0.9, 1
        pos_hint: {'x': 0.1}
'''


class WindowObject(RelativeLayout):
    def __init__(self, **kwargs):
        Builder.load_string(root)
        super().__init__(**kwargs)
        Clock.schedule_interval(lambda dt: self.update(dt), 1 / 60)

        self.lwfs = []
        self.factory = RendererFactory(self.ids.display, '', self.load_texture)

        self.files = []
        for file in listdir('../res/lwf/test/'):
            if file.startswith('812') and file > '812200100':
                continue
            item = {'text': file, 'on_release': lambda name=file: self.select_item(name), 'font_name': 'Gabriola', 'font_size': '15pt'}
            self.files.append(item)
        self.ids.list.data = self.files

        # Special battle attack animation sequence
        # wscale = 10 * 1706 / 1920
        # hscale = 10 * 960 / 1080
        # animation_1 = LWF(Data('../res/lwf/test/812200202/812200202.lwf'), self.factory, '812200202')
        # animation_1.property.move(1706 * 0.2, 960 * 0.5)
        # animation_1.scale_for_width(wscale, hscale)
        # animation_1.add_event_handler('end', lambda movie, button: self.lwfs.remove(animation_1))
        #
        # animation_12 = LWF(Data('../res/lwf/test/812200206/812200206.lwf'), self.factory, '812200206')
        # animation_12.property.move(1706 * 0.2, 960 * 0.5)
        # animation_12.scale_for_width(wscale, hscale)
        # animation_12.add_event_handler('end', lambda movie, button: self.lwfs.remove(animation_12))
        #
        # animation_2 = LWF(Data('../res/lwf/test/812200203/812200203.lwf'), self.factory, '812200203')
        # animation_2.property.move(1706 * 0.4, 960 * 0.5)
        # animation_2.scale_for_width(wscale, hscale)
        # animation_2.add_event_handler('end', lambda movie, button: self.lwfs.remove(animation_2))
        #
        # special_scene = LWF(Data('../res/lwf/test/812200200/812200200.lwf'), self.factory, '812200200')
        # special_scene.property.set_alpha(0.0)
        # special_scene.add_event_handler('play_special_attack_animation_1', lambda movie, button: self.lwfs.append(animation_1))
        # special_scene.add_event_handler('play_special_attack_animation_1', lambda movie, button: self.lwfs.append(animation_12))
        # special_scene.add_event_handler('play_special_attack_animation_2', lambda movie, button: self.lwfs.append(animation_2))
        # special_scene.add_event_handler('end', lambda movie, button: self.lwfs.remove(special_scene))
        # special_scene.add_event_handler('end', lambda movie, button: self.lwfs.remove(animation_1))
        # special_scene.add_event_handler('end', lambda movie, button: self.lwfs.remove(animation_12))
        # special_scene.add_event_handler('end', lambda movie, button: self.lwfs.remove(animation_2))
        #
        #
        # special_intro = LWF(Data('../res/lwf/test/810000005/810000005.lwf'), self.factory, '810000005')
        # special_intro.scale_for_width(1706, 960)
        # special_intro.property.move(0, 960)
        # special_intro.add_event_handler('end', lambda movie, button: self.lwfs.append(special_scene))
        # self.lwfs.append(special_intro)


        # self.lwfs.append(lwf)
        # ../res/lwf/test/812200200/812200200.lwf
        # lwf = LWF(Data('../res/lwf/810000001/810000001.lwf'), self.factory, '810000001')
        # lwf.property.move(96, 96)
        # lwf.play_animation(0, lwf.root_movie)
        # self.lwfs.append(lwf)
        # ais_special_attack = LWF(data, self.factory, 'special_attack')
        # ais_special_attack.add_event_handler()
        # self.select_item('817000331')

    def select_item(self, name):
        print('Playing: ', name)
        self.ids.playing.text = f'Playing: {name}'
        self.display_lwf(name)

    def change_size(self, size_text):
        pass

    def change_pos(self, pos_text):
        pass

    def display_lwf(self, name):
        self.lwfs.clear()
        data = Data(f'../res/lwf/test/{name}/{name}.lwf')
        lwf = LWF(data, self.factory, name)
        for event_id, event in enumerate(lwf.data.events):
            lwf.add_event_handler(event_id, lambda button, movie, e=event: print(str(e)))
        if lwf.width == 1920 and lwf.height == 1080:
            lwf.scale_for_width(910, 540)
            # lwf.property.move(1706 * 0.1, 960)
        else:
            width, height = 1706 * 0.9, 960
            lwf.property.move_to(width * 0.5, height * 0.5)
            scale = (1706 * 0.9) / 1920 * 10
            lwf.scale_for_width(scale, scale)
        self.lwfs.append(lwf)

    def load_texture(self, filename, lwf_name):
        if filename == 'lwf_img_replace_chara.png':
            filename = f'../res/lwf/test/{lwf_name}/all_rectangle.png'
        elif filename == 'lwf_img_replace_chara_w.png':
            filename = f'../res/lwf/test/{lwf_name}/white.png'
        elif filename == 'lwf_img_replace_combo.png':
            filename = f'../res/lwf/test/{lwf_name}/2.png'
        elif filename == 'lwf_img_replace_skill_name.png':
            filename = f'../res/lwf/test/{lwf_name}/109200201.png'
        # elif 'replace' in filename:
        #     print(filename, 'Needs to be replaced')
        #     filename = f'../res/lwf/test/{lwf_name}/109200201.png'
        else:
            filename = f'../res/lwf/test/{lwf_name}/{filename}'

        texture = CoreImage(filename).texture
        return texture

    def update(self, dt):
        self.ids.display.canvas.clear()
        for lwf in self.lwfs:
            if lwf.root_movie.playing:
                if lwf.exec(dt) > 0:
                    pass
                lwf.render()

    def stop_start(self):
        for lwf in self.lwfs:
            # if lwf.root_movie.playing:
            #     lwf.root_movie.stop()
            # else:
            lwf.root_movie.play()


class Player(App):
    def build(self):
        return WindowObject()


if __name__ == "__main__":
    window = Player().run()
