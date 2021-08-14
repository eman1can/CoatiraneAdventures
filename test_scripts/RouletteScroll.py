from kivy.properties import BooleanProperty

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.carousel import Carousel
from kivy.uix.relativelayout import RelativeLayout


class RouletteScrollScreen(RelativeLayout):
    current = BooleanProperty(False)

    def __init__(self, **kwargs):
        self.register_event_type('on_enter')
        self.register_event_type('on_exit')
        super().__init__(**kwargs)

    def on_enter(self):
        pass

    def on_exit(self):
        pass


class RouletteScroll(Carousel):
    def on_touch_down(self, touch):
        if self.disabled:
            return False

        if touch.button == 'scrollup':
            self.load_next()
            return True

        if touch.button == 'scrolldown':
            self.load_next('prev')
            return True

        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        return False



root = """
RouletteScroll:
    loop: True
    RouletteScrollScreen:
        on_enter: print('You have moved to screen 1!')
        on_exit: print('You have left screen 1!')
        Button:
            text: 'I am screen 1!'
            on_release: print(self.text)
    RouletteScrollScreen:
        on_enter: print('You have moved to screen 2!')
        on_exit: print('You have left screen 2!')
        Button:
            text: 'I am screen 2!'
            on_release: print(self.text)
    RouletteScrollScreen:
        on_enter: print('You have moved to screen 3!')
        on_exit: print('You have left screen 3!')
        Button:
            text: 'I am screen 3!'
            on_release: print(self.text)
    RouletteScrollScreen:
        on_enter: print('You have moved to screen 4!')
        on_exit: print('You have left screen 4!')
        Button:
            text: 'I am screen 4!'
            on_release: print(self.text)
"""


class RouletteScrollApp(App):
    def build(self):
        return Builder.load_string(root)


if __name__ == "__main__":
    RouletteScrollApp().run()