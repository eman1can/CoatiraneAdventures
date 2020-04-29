from src.modules.KivyBase.Hoverable import RelativeLayoutBase as RelativeLayout
from kivy.properties import StringProperty


class Hint(RelativeLayout):
    hint_text_words = StringProperty('')
    hint_text_numbers = StringProperty('')

    def on_touch_down(self, touch):
        if self.disabled:
            return False
        if not self.collide_point(*touch.pos):
            return False
        if self.ids.scroll.viewport_size[1] <= self.ids.scroll.height:
            return False
        touch.push()
        touch.apply_transform_2d(self.to_local)
        for child in self.children[:]:
            if child.on_touch_down(touch):
                touch.pop()
                return True
        touch.pop()
        return False
