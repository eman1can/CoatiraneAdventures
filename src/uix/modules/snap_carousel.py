from kivy.animation import Animation
from kivy.clock import Clock
from kivy.properties import ObjectProperty, BooleanProperty, NumericProperty
from kivy.uix.carousel import Carousel

from loading.kv_loader import load_kv
load_kv(__name__)


class SnapCarousel(Carousel):
    #dungeon = ObjectProperty(None)
    locked = BooleanProperty(False)

    relative = BooleanProperty(False)

    def __init__(self, **kwargs):
        self.register_event_type('on_change')
        self.register_event_type('on_load_next')
        self.register_event_type('on_load_previous')
        super().__init__(**kwargs)

    def check_current(self, instance):
        if self.current_slide == instance:
            return True
        return False

    def update_lock(self, locked):
        self.locked = locked
        self.current_slide.update_lock(locked)

    def close_hints(self):
        self.current_slide.close_hints()

    def reload(self):
        if self.current_slide is None:
            return
        self.current_slide.reload()

    #def get_party_score(self):
    #    if self.current_slide is None:
    #        return 0
    #   return self.current_slide.get_party_score()

    def on_current_slide(self, *args):
        self.dispatch('on_change', self.index)

    def replace_widget(self, index, widget):
        if index >= len(self.slides):
            return False
        slide = self.slides[index]
        container = slide.parent
        container.remove_widget(slide)
        container.add_widget(widget)
        self.slides[index] = widget
        return True

    def on_change(self, *args):
        pass

    def on_load_next(self):
        pass

    def on_load_previous(self):
        pass

    def on_touch_down(self, touch):
        if self.locked:
            return False
        if not self.collide_point(*touch.pos):
            touch.ud[self._get_uid('cavoid')] = True
            return
        if self.disabled:
            return False
        if self._touch:
            touch.push()
            touch.apply_transform_2d(lambda x, y: self.to_local(x, y, self.relative))
            ret = super(Carousel, self).on_touch_down(touch)
            touch.pop()
            return ret
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

    def on_touch_hover(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        touch.push()
        touch.apply_transform_2d(lambda x, y: self.to_local(x, y, self.relative))
        if self.current_slide.dispatch('on_touch_hover', touch):
            touch.pop()
            return True
        touch.pop()
        return False

    def load_next(self, mode='next'):
        '''Animate to the next slide.

        .. versionadded:: 1.7.0
        '''

        if self.index is not None and not self.locked:
            # self.current_slide.dispatch('on_leave')
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
            # self.current_slide.dispatch('on_enter')
