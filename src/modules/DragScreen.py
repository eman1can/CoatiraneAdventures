from kivy.properties import ObjectProperty, BooleanProperty
from src.modules.KivyBase.Hoverable import CarouselBase as Carousel, HoverBehaviour


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

    def update_lock(self, locked):
        self.locked = locked
        self.current_slide.update_lock(locked)

    def close_hints(self):
        self.current_slide.close_hints()

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
