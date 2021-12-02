from kivy.properties import BooleanProperty

from kivy.uix.carousel import Carousel
from loading.kv_loader import load_kv

load_kv(__name__)


class SnapCarousel(Carousel):
    locked = BooleanProperty(False)
    relative = BooleanProperty(False)

    def __init__(self, **kwargs):
        self.register_event_type('on_index_update')
        super().__init__(**kwargs)

    def reload(self, **kwargs):
        self.load_kwargs(kwargs)
        if self.current_slide is not None:
            self.current_slide.reload(locked=self.locked)

    def on_locked(self, *args):
        self.current_slide.locked = self.locked

    def close_hints(self):
        self.current_slide.close_hints()

    def on_current_slide(self, *args):
        self.current_slide.current = True
        self.current_slide.locked = self.locked

    def on_index(self, instance, index):
        super().on_index(instance, index)
        self.dispatch('on_index_update', self.index)

    def on_index_update(self, index):
        pass

    def on_touch_down(self, touch):
        if self.locked or self.disabled:
            return False
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.locked or self.disabled:
            return False
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.locked or self.disabled:
            return False
        if touch.button == 'scrollup':
            self.load_next()
            return True
        if touch.button == 'scrolldown':
            self.load_next('prev')
            return True
        return super().on_touch_up(touch)

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
        self.current_slide.current = False
        super().load_next(mode)

    def load_index(self, index):
        if index >= len(self.slides):
            return
        self.load_slide(self.slides[index])

    def replace_widget(self, index, widget):
        if index >= len(self.slides):
            return False
        slide = self.slides[index]
        container = slide.parent
        container.remove_widget(slide)
        container.add_widget(widget)
        self.slides[index] = widget
        return True
