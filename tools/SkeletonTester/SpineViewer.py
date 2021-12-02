from plyer import filechooser
from os import getcwd

from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.scatter import Scatter
from spine.animation.animationstate import AnimationState
from spine.animation.animationstatedata import AnimationStateData
from spine.skeleton.skeletonloader import SkeletonLoader
from spine.skeleton.skeletonrenderer import SkeletonRenderer

Config.set('graphics', 'height', 600)
Config.set('graphics', 'width', 800)
Config.set('graphics', 'left', 890)
Config.set('graphics', 'top', 450)

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout


root = """
RootWindow:
    canvas:
        Color:
            rgba: 112 / 255, 111 / 255, 118 / 255, 1
        Rectangle:
            size: self.size
    WindowScatter:
        RelativeLayout:
            id: skeleton_canvas
    RelativeLayout:
        size_hint: None, 1
        width: 300
        canvas:
            Color:
                rgba: 51 / 255, 51 / 255, 51 / 255, 1
            Rectangle:
                size: self.size
        RelativeLayout:
            size_hint: None, None
            width: self.parent.width - dp(10)
            height: dp(25)
            pos: dp(5), self.parent.height - dp(30)
            Label:
                id: filename
                size_hint: None, 1
                width: self.texture_size[0]
                text: 'Skeleton'
                font_size: '12sp'
            Button:
                id: open
                size_hint: None, 1
                width: dp(50)
                right: minimize.x - dp(5)
                text: 'Open'
                font_size: '12sp'
                on_release: root.open_skeleton()
            Button:
                id: minimize
                size_hint: None, 1
                width: self.height
                pos_hint: {'right': 1}
                text: '-'
                font_size: '12sp'
        RecycleView:
            id: skins
            size_hint: 1, 0.25
            pos_hint: {'y': 0.5}
            viewclass: 'ToggleButton'
            RecycleGridLayout:
                cols: 1
                size_hint: 1, None
                height: self.minimum_height
                default_size_hint: 1, None
                default_size: None, dp(20)
                row_default_height: dp(20)
                row_force_default: True
        RecycleView:
            id: animations
            size_hint: 1, 0.25
            pos_hint: {'y': 0.1}
            viewclass: 'ToggleButton'
            RecycleGridLayout:
                cols: 1
                size_hint: 1, None
                default_size_hint: 1, None
                default_size: None, dp(20)
                height: self.minimum_height
                row_default_height: dp(20)
                row_force_default: True
    
"""


class RootWindow(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._canvas = None
        self._skeleton = None
        self._animation_state = None
        self._skeleton_loader = SkeletonLoader()
        self._skeleton_renderer = SkeletonRenderer()

        self._load_scale = 1
        self._skins = []
        self._animations = []

    def on_kv_post(self, base_widget):
        self._canvas = self.ids.skeleton_canvas.canvas
        Clock.schedule_interval(self.update, 1 / 60)

    def open_skeleton(self):
        path = filechooser.open_file(path=getcwd(), title="Choose Skeleton File", filters=[("Spine Binary Skeleton", "*.skel"), ("Spine JSON Skeleton", "*.json")])[0]
        self.ids.filename.text = path[path.rindex('\\'):]

        self._skeleton = self._skeleton_loader.load_skeleton(path, False, self._load_scale)
        skeleton_data = self._skeleton.getData()

        skins = skeleton_data.getSkins()
        default_skin = None
        self._skins = []
        for skin in skins:
            if default_skin is None:
                default_skin = skin.getName()
                self._skins.append({'text': skin.getName(), 'on_release': lambda s=skin.getName(): self.update_skin(s), 'state': 'down', 'group': 'skins', 'allow_no_selection': False})
            else:
                self._skins.append({'text': skin.getName(), 'on_release': lambda s=skin.getName(): self.update_skin(s), 'group': 'skins', 'allow_no_selection': False})
        self.ids.skins.data = self._skins
        self._skeleton.setSkin(default_skin)

        default_animation = None
        self._animations = []
        for animation in skeleton_data.getAnimationNames():
            if default_animation is None:
                default_animation = animation
                self._animations.append({'text': animation, 'on_release': lambda anim=animation: self.update_animation(anim), 'state': 'down', 'group': 'animations', 'allow_no_selection': False})
            else:
                self._animations.append({'text': animation, 'on_release': lambda anim=animation: self.update_animation(anim), 'group': 'animations', 'allow_no_selection': False})
        self.ids.animations.data = self._animations

        self._skeleton.setWidth(self._skeleton.getData().getWidth() * self._load_scale)
        self._skeleton.setHeight(self._skeleton.getData().getHeight() * self._load_scale)

        self._animation_state = AnimationState(AnimationStateData(self._skeleton.getData()))
        self._animation_state.setAnimation(0, default_animation, True)

    def update_skin(self, skin, *args):
        self._skeleton.setSkin(skin)

    def update_animation(self, anim, *args):
        self._animation_state.setAnimation(0, anim, True)

    def update(self, delta):
        if self._skeleton is None:
            return
        self._skeleton.update(delta)
        self._animation_state.update(delta)
        self._animation_state.apply(self._skeleton)
        self._skeleton.updateWorldTransform()
        self.render()

    def render(self):
        if self._canvas is None:
            return
        if self._skeleton is None:
            return
        self._canvas.clear()
        self._skeleton_renderer.draw(self._canvas, self._skeleton)


class WindowScatter(Scatter):
    def on_kv_post(self, base_widget):
        self.scale_min = 0.1
        self.scale_max = 1000
        self.scale = 0.1

    def on_touch_down(self, touch):
        if touch.button == 'scrollup':
            print('Zoom Out')
            self._set_scale(self.scale - 0.1)
        elif touch.button == 'scrolldown':
            print('Zoom In')
            self._set_scale(self.scale + 0.1)
        else:
            if touch.x > 300:
                self._bring_to_front(touch)
                touch.grab(self)
                self._touches.append(touch)
                self._last_touch_pos[touch] = touch.pos

                return True
        return False


class SpineViewerApp(App):
    def build(self):
        return Builder.load_string(root)


if __name__ == "__main__":
    SpineViewerApp().run()
