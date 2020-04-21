from kivy.app import App
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.properties import ObjectProperty, BooleanProperty

from src.modules.KivyBase.Hoverable import CarouselH as Carousel


class DragSnapWidget(Carousel):
    dungeon = ObjectProperty(None)
    locked = BooleanProperty(False)

    def __init__(self, **kwargs):
        self.register_event_type('on_change')
        super().__init__(**kwargs)

    def check_current(self, instance):
        if self.current_slide == instance:
            return True
        return False

    def on_mouse_pos(self, hover):
        if not self.collide_point(*hover.pos):
            return False
        if self.current_slide.dispatch('on_mouse_pos', hover):
            return True
        return False

    def update_lock(self, locked):
        self.locked = locked
        self.current_slide.update_lock(locked)

    def reload(self):
        if self.current_slide is None:
            return
        self.current_slide.reload()

    def get_party_score(self):
        if self.current_slide is None:
            return 0
        return self.current_slide.get_party_score()

    def on_current_slide(self, *args):
        self.dispatch('on_change', self.index)

    def on_change(self, *args):
        pass

    def load_next(self, mode='next'):
        '''Animate to the next slide.

        .. versionadded:: 1.7.0
        '''

        if self.index is not None and not self.locked:
            w, h = self.size
            _direction = {
                'top': -h / 2,
                'bottom': h / 2,
                'left': w / 2,
                'right': -w / 2}
            _offset = _direction[self.direction]
            if mode == 'prev':
                _offset = -_offset

            self._start_animation(min_move=0, offset=_offset)

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            touch.ud[self._get_uid('cavoid')] = True
            return
        if self.disabled or self.locked:
            return True
        if self._touch:
            return super(Carousel, self).on_touch_down(touch)
        Animation.cancel_all(self)
        self._touch = touch
        uid = self._get_uid()
        touch.grab(self)
        touch.ud[uid] = {
            'mode': 'unknown',
            'time': touch.time_start}
        self._change_touch_mode_ev = Clock.schedule_once(
            self._change_touch_mode, self.scroll_timeout / 1000.)
        self.touch_mode_change = False
        return True
