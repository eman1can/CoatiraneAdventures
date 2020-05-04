from functools import partial

from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.button import Button
from kivy.uix.carousel import Carousel
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import AsyncImage, Image
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.stencilview import StencilView
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView


class HoverBehaviour(object):
    def __init__(self, **kwargs):
        self.register_event_type('on_touch_hover')
        super().__init__(**kwargs)

    def on_touch_hover(self, touch):
        return False

    def dispatch_to_children(self, touch):
        for child in self.children[:]:
            if child.dispatch('on_touch_hover', touch):
                return True
        return False

    def dispatch_to_relative_children(self, touch):
        touch.push()
        touch.apply_transform_2d(self.to_local)
        for child in self.children[:]:
            if child.dispatch('on_touch_hover', touch):
                touch.pop()
                return True
        touch.pop()
        return False


class GameBounds(HoverBehaviour, Image):
    def on_touch_hover(self, touch):
        return self.dispatch_to_children(touch)


class WidgetBase(HoverBehaviour, Widget):
    pass


class ButtonBase(HoverBehaviour, Button):
    pass


class ImageBase(HoverBehaviour, Image):
    pass


class AsyncImageBase(HoverBehaviour, AsyncImage):
    pass


class LabelBase(HoverBehaviour, Label):
    pass


class CarouselBase(HoverBehaviour, Carousel):
    def on_touch_hover(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        if self.current_slide.dispatch('on_touch_hover', touch):
            return True
        return False

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            touch.ud[self._get_uid('cavoid')] = True
            return
        if self.disabled:
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

    def on_touch_up(self, touch):
        if self._get_uid('cavoid') in touch.ud:
            return
        if self in [x() for x in touch.grab_list]:
            touch.ungrab(self)
            self._touch = None
            ud = touch.ud[self._get_uid()]
            if ud['mode'] == 'unknown':
                ev = self._change_touch_mode_ev
                if ev is not None:
                    ev.cancel()
                if not super(Carousel, self).on_touch_down(touch):
                    if 'button' in touch.profile:
                        if touch.button.startswith('scroll'):
                            if touch.button == 'scrollright' or touch.button == 'scrolldown':
                                self.load_previous()
                                return True
                            elif touch.button == 'scrollleft' or touch.button == 'scrollup':
                                self.load_next()
                                return True
                            return False
                Clock.schedule_once(partial(self._do_touch_up, touch), .1)
            else:
                self._start_animation()

        else:
            if self._touch is not touch and self.uid not in touch.ud:
                super(Carousel, self).on_touch_up(touch)
        return self._get_uid() in touch.ud


class ScreenManagerBase(HoverBehaviour, ScreenManager):
    def on_touch_hover(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        return self.dispatch_to_children(touch)


class ScreenBase(HoverBehaviour, Screen):
    background_source = StringProperty("../res/screens/backgrounds/background.png")
    background = BooleanProperty(True)

    def on_touch_hover(self, touch):
        return self.dispatch_to_relative_children(touch)

    def reload(self):
        pass

    def on_back_press(self):
        root = App.get_running_app().main
        if root is not None:
            root.display_screen(None, False, False)
            return True
        return False


class RelativeLayoutBase(HoverBehaviour, RelativeLayout):
    def on_touch_hover(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        return self.dispatch_to_relative_children(touch)


class GridLayoutBase(HoverBehaviour, GridLayout):
    def on_touch_hover(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        return self.dispatch_to_relative_children(touch)


class StencilViewBase(HoverBehaviour, StencilView):
    def on_touch_hover(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        return self.dispatch_to_children(touch)


class ScrollViewBase(HoverBehaviour, ScrollView):
    def on_touch_down(self, touch):
        if self.disabled:
            return False
        if not self.collide_point(*touch.pos):
            return False
        if self.dispatch('on_scroll_start', touch):
            self._touch = touch
            touch.grab(self)
            return True

    def on_touch_hover(self, touch):
        if self.disabled:
            return False
        if not self.collide_point(*touch.pos):
            return False
        return self.dispatch_to_relative_children(touch)


class ModalViewBase(HoverBehaviour, ModalView):
    def on_touch_hover(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        return self.dispatch_to_children(touch)
