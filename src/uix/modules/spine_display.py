from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.relativelayout import RelativeLayout
from loading.kv_loader import load_kv
from spine.animation.animationstate import AnimationState
from spine.animation.animationstatedata import AnimationStateData
from spine.skeleton.skeletonloader import SkeletonLoader
from spine.skeleton.skeletonrenderer import SkeletonRenderer

# Expression Skins
DEFAULT = 'default'
ANGRY = 'expression_angry'
CONFUSE = 'expression_confuse'
JOY = 'expression_joy'
NORMAL = 'expression_normal'
SAD = 'expression_sad'
SURPISE = 'expression_surprise'
expressions = [DEFAULT, ANGRY, CONFUSE, JOY, NORMAL, SAD, SURPISE]

# Animations
IDLE = 'idle'
IDLE_TALK = 'idle_talk'
TOUCH = 'touch'
TOUCH_talk = 'touch_talk'


class SpineDisplay(RelativeLayout):
    skeleton_path = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._canvas = self.canvas
        self._skeleton = None
        self._animation_state = None
        self._skeleton_loader = SkeletonLoader()
        self._skeleton_renderer = SkeletonRenderer()

        if self.skeleton_path != '':
            self.display_skeleton()

    def on_size(self, *args):
        if self._skeleton is None:
            return
        skeleton_height = self._skeleton.getHeight()
        self._skeleton.setPosition(self.width * 0.2, self.height - skeleton_height)

    def on_skeleton_path(self, *args):
        self.display_skeleton()

    def display_skeleton(self, scale=0.5):
        self._skeleton = self._skeleton_loader.load_skeleton(self.skeleton_path, False, scale)
        self._skeleton.setSkin(JOY)
        self._skeleton.setWidth(self._skeleton.getData().getWidth() * scale)
        self._skeleton.setHeight(self._skeleton.getData().getHeight() * scale)

        self._animation_state = AnimationState(AnimationStateData(self._skeleton.getData()))
        self._animation_state.setAnimation(0, IDLE, True)

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
