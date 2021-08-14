from os import listdir

from kivy import Config
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout

from lwf.lwf import LWF
from lwf.format.data import Data
from lwf.renderer import RendererFactory
from spine.animation.animationstate import AnimationState
from spine.animation.animationstatedata import AnimationStateData
from spine.skeleton.skeletonloader import SkeletonLoader
from spine.skeleton.skeletonrenderer import SkeletonRenderer

Config.set('graphics', 'width', 1706)
Config.set('graphics', 'height', 960)

from kivy.clock import Clock
from kivy.core.image import Image as CoreImage


from kivy.app import App


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
            size_hint: 0.1, 0.4
            pos_hint: {'y': 0.4}
            viewclass: 'Button'
            RecycleBoxLayout:
                default_size: None, dp(56)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
        RecycleView:
            id: animations
            size_hint: 0.1, 0.4
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

        self.skeletons = []
        self.animation_states = []
        self.factory = SkeletonRenderer()
        self.loader = SkeletonLoader()

        entities = []
        with open('../data/test/CharacterDefinitions.txt') as file:
            for line in file:
                if line.startswith('A,'):
                    entries = [x.strip() for x in line.split(', ')]
                    print(entries)
                    name = entries[3] + ' ' + entries[2]
                    skeleton = entries[4]
                    entities.append(('characters', entries[1], name, skeleton))
        with open('../data/test/Enemies.txt') as file:
            for line in file:
                if line[0] in ['#'] + [str(x) for x in range(10)]:
                    continue
                entries = [x.strip() for x in line.split(', ')]
                if entities[2] == '-':
                    continue
                entities.append(('enemies', entries[0], entries[1], entries[2]))

        self.files = []
        for (entity_type, identifier, name, skeleton) in entities:
            location = f'../res/{entity_type}/{identifier}'
            item = {'text': name, 'on_release': lambda name=name, skeleton=skeleton, location=location: self.select_item(name, location, skeleton), 'font_name': 'Gabriola', 'font_size': '15pt'}
            self.files.append(item)
        self.ids.list.data = self.files

        self.playing = True
        (entity_type, identifier, name, skeleton) = entities[0]
        self.select_item(name, f'../res/{entity_type}/{identifier}', skeleton)

    def select_item(self, name, location, skeleton):
        print('Playing: ', name)
        self.ids.playing.text = f'Playing: {name}'
        self.display_skeleton(location, skeleton)

    def change_size(self, size_text):
        pass

    def change_pos(self, pos_text):
        pass

    def display_skeleton(self, location, skeleton_name):
        self.skeletons.clear()
        scale = 0.125
        skeleton = self.loader.load_skeleton(f'{location}/{skeleton_name}.skel', False, scale)
        skeleton.setWidth(skeleton.getData().getWidth() * scale)
        skeleton.setHeight(skeleton.getData().getHeight() * scale)
        data = AnimationStateData(skeleton.getData())
        animation_state = AnimationState(data)
        animations = []
        for animation in animation_state.getAnimationList():
            animations.append({'text': animation, 'on_release': lambda animation_name=animation: animation_state.setAnimation(0, animation_name, loop=True), 'font_name': 'Gabriola', 'font_size': '15pt'})
        self.ids.animations.data = animations
        skeleton.setSkin(skeleton.getData().getSkins()[0].getName())
        animation_state.setAnimation(0, animation_state.getAnimationList()[0], loop=True)

        self.skeletons.append((skeleton, animation_state))

    def update(self, delta):
        self.ids.display.canvas.clear()
        for (skeleton, animation_state) in self.skeletons:
            if self.playing:
                skeleton.update(delta)
                animation_state.update(delta)
                animation_state.apply(skeleton)
                skeleton.setPosition(self.width / 2, self.height / 2)
                skeleton.updateWorldTransform()
            self.factory.draw(self.ids.display.canvas, skeleton)

    def stop_start(self):
        self.playing = not self.playing


class Player(App):
    def build(self):
        return WindowObject()


if __name__ == "__main__":
    window = Player().run()
