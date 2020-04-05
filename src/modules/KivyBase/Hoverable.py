from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.carousel import Carousel
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import AsyncImage, Image
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.stencilview import StencilView
from kivy.uix.widget import Widget


class HoverEvent(object):
    def __init__(self, x=0, y=0, current=None):
        self.grab_current = current
        self.pos = (x, y)

    def grab(self, widget):
        if self.grab_current is None:
            self.grab_current = widget
            return True
        return False

    def ungrab(self, widget):
        if self.grab_current == widget:
            self.grab_current = None
            return True
        return False


class ScreenManagerH(ScreenManager):
    def __init__(self, **kwargs):
        self.register_event_type('on_mouse_pos')
        super().__init__(**kwargs)

    def on_mouse_pos(self, hover):
        if len(self.children) > 0:
            if self.children[0].dispatch('on_mouse_pos', hover):
                return True


class ScreenH(Screen):
    def __init__(self, **kwargs):
        self.register_event_type('on_mouse_pos')
        super().__init__(**kwargs)

    def on_mouse_pos(self, hover):
        for child in self.children:
            if child.dispatch('on_mouse_pos', hover):
                return True


class StencilViewH(StencilView):
    def __init__(self, **kwargs):
        self.register_event_type('on_mouse_pos')
        super().__init__(**kwargs)

    def on_mouse_pos(self, hover):
        if not self.collide_point(*hover.pos):
            return False
        for child in self.children:
            if child.dispatch('on_mouse_pos', hover):
                return True


class FloatLayoutH(FloatLayout):
    def __init__(self, **kwargs):
        self.register_event_type('on_mouse_pos')
        super().__init__(**kwargs)

    def on_mouse_pos(self, hover):
        if not self.collide_point(*hover.pos):
            return False
        for child in self.children:
            if child.dispatch('on_mouse_pos', hover):
                return True


class GridLayoutH(GridLayout):
    def __init__(self, **kwargs):
        self.register_event_type('on_mouse_pos')
        super().__init__(**kwargs)

    def on_mouse_pos(self, hover):
        if not self.collide_point(*hover.pos):
            return False
        for child in self.children:
            if child.dispatch('on_mouse_pos', hover):
                return True


class RecycleGridLayoutH(RecycleGridLayout):
    def __init__(self, **kwargs):
        self.register_event_type('on_mouse_pos')
        super().__init__(**kwargs)

    def on_mouse_pos(self, hover):
        if not self.collide_point(*hover.pos):
            return False
        for child in self.children:
            if child.dispatch('on_mouse_pos', hover):
                return True


class RecycleViewH(RecycleView):
    def __init__(self, **kwargs):
        self.register_event_type('on_mouse_pos')
        super().__init__(**kwargs)

    def on_mouse_pos(self, hover):
        if not self.collide_point(*hover.pos):
            return False
        for child in self.children:
            if child.dispatch('on_mouse_pos', hover):
                return True


class ImageH(Image):
    def __init__(self, **kwargs):
        self.register_event_type('on_mouse_pos')
        super().__init__(**kwargs)

    def on_mouse_pos(self, hover):
        if not self.collide_point(*hover.pos):
            return False
        for child in self.children:
            if child.dispatch('on_mouse_pos', hover):
                return True


class AsyncImageH(AsyncImage):
    def __init__(self, **kwargs):
        self.register_event_type('on_mouse_pos')
        super().__init__(**kwargs)

    def on_mouse_pos(self, hover):
        if not self.collide_point(*hover.pos):
            return False
        for child in self.children:
            if child.dispatch('on_mouse_pos', hover):
                return True


class WidgetH(Widget):
    def __init__(self, **kwargs):
        self.register_event_type('on_mouse_pos')
        super().__init__(**kwargs)

    def on_mouse_pos(self, hover):
        if not self.collide_point(*hover.pos):
            return False


class LabelH(Label):
    def __init__(self, **kwargs):
        self.register_event_type('on_mouse_pos')
        super().__init__(**kwargs)

    def on_mouse_pos(self, hover):
        if not self.collide_point(*hover.pos):
            return False


class ButtonH(Button):
    def __init__(self, **kwargs):
        self.register_event_type('on_mouse_pos')
        super().__init__(**kwargs)

    def on_mouse_pos(self, hover):
        if not self.collide_point(*hover.pos):
            return False


class ModalViewH(ModalView):
    def __init__(self, **kwargs):
        self.register_event_type('on_mouse_pos')
        super().__init__(**kwargs)

    def on_mouse_pos(self, hover):
        for child in self.children:
            if child.dispatch('on_mouse_pos', hover):
                return True


class CarouselH(Carousel):
    def __init__(self, **kwargs):
        self.register_event_type('on_mouse_pos')
        super().__init__(**kwargs)

    def on_mouse_pos(self, hover):
        if not self.collide_point(*hover.pos):
            return False
        for child in self.children:
            if child.dispatch('on_mouse_pos', hover):
                return True


class RelativeLayoutH(RelativeLayout):
    def __init__(self, **kwargs):
        self.register_event_type('on_mouse_pos')
        super().__init__(**kwargs)

    def on_mouse_pos(self, hover):
        if not self.collide_point(*hover.pos):
            return False
        for child in self.children:
            if child.dispatch('on_mouse_pos', hover):
                return True


class BoxLayoutH(BoxLayout):
    def __init__(self, **kwargs):
        self.register_event_type('on_mouse_pos')
        super().__init__(**kwargs)

    def on_mouse_pos(self, hover):
        if not self.collide_point(*hover.pos):
            return False
        for child in self.children:
            if child.dispatch('on_mouse_pos', hover):
                return True