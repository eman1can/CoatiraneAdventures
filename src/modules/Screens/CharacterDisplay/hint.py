from src.modules.KivyBase.Hoverable import RelativeLayoutBase as RelativeLayout, LabelBase
from kivy.properties import DictProperty


class Hint(RelativeLayout):
    hint_text = DictProperty({})

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

    def on_hint_text(self, *args):
        self.update_labels()

    def update_labels(self):
        self.ids.grid.clear_widgets()
        d = {k: v for k, v in sorted(self.hint_text.items(), key=lambda item: item[1], reverse=True)}
        for k in d:
            self.ids.grid.add_widget(HintNameWords(text=k, font_size=self.height * 0.075))
            self.ids.grid.add_widget(HintNameNumbers(text=str(round(d[k], 2)), font_size=self.height * 0.075))


class HintNameWords(LabelBase):
    pass


class HintNameNumbers(LabelBase):
    pass


