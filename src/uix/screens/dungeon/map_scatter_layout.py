from kivy.graphics.transformation import Matrix

from kivy.properties import AliasProperty, NumericProperty

from kivy.uix.scatterlayout import ScatterLayout
from loading.kv_loader import load_kv

load_kv(__name__)


class MapScatterLayout(ScatterLayout):
    zoom_delta = NumericProperty(0.05)

    def __init__(self, **kwargs):
        self._map_size = (100, 100)
        self.gap_h = self.gap_v = 0
        super().__init__(**kwargs)

    def set_text(self, text):
        self.ids.full_screen_map.text = text

    def set_map_size(self, map_size):
        self._map_size = map_size

    map_size = AliasProperty(None, set_map_size)

    def collide_point(self, x, y):
        return 0 <= x <= self.width and 0 <= y <= self.height

    def on_touch_down(self, touch):
        if self.opacity == 0:
            return False
        if touch.button == 'scrollup':
            if self.scale > self.scale_min:
                self.apply_zoom(1 - self.zoom_delta, touch)
        elif touch.button == 'scrolldown':
            if self.scale < self.scale_max:
                self.apply_zoom(1 + self.zoom_delta, touch)
        else:
            return super().on_touch_down(touch)
        return True

    def apply_zoom(self, zoom, touch):
        self.apply_transform(Matrix().scale(zoom, zoom, zoom), post_multiply=True, anchor=self.to_local(*touch.pos))
        width, height = self._map_size

        bottom = height * self.scale / 2
        top = bottom - (height * self.scale - self.height)
        left = width * self.scale / 2
        right = left - (width * self.scale - self.width)

        if height * self.scale > self.height:
            if top > self.center_y:
                self.center_y = top
            elif self.center_y > bottom:
                self.center_y = bottom
        else:
            self.center_y = (top + bottom) / 2

        if width * self.scale > self.width:
            if left < self.center_x:
                self.center_x = left
            elif self.center_x < right:
                self.center_x = right
        else:
            self.center_x = (left + right) / 2

    def transform_with_touch(self, touch):
        super().transform_with_touch(touch)
        dx = (touch.x - self._last_touch_pos[touch][0])
        dy = (touch.y - self._last_touch_pos[touch][1])
        dx = dx / self.translation_touches
        dy = dy / self.translation_touches

        width, height = self._map_size
        left = width * self.scale / 2
        right = left - (width * self.scale - self.width)
        bottom = height * self.scale / 2
        top = bottom - (height * self.scale - self.height)

        if right < self.center_x + dx < left:
            self.apply_transform(Matrix().translate(dx, 0, 0))
        if top < self.center_y + dy < bottom:
            self.apply_transform(Matrix().translate(0, dy, 0))
