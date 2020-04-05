from kivy.app import App
from kivy.clock import Clock
from kivy.input.providers.wm_touch import WM_MotionEvent
from kivy.properties import BooleanProperty, ObjectProperty, NumericProperty, StringProperty, ListProperty

from src.modules.KivyBase.Hoverable import ScreenH as Screen, WidgetH as Widget


class FilledCharacterPreviewScreen(Screen):
    preview = ObjectProperty(None)
    character = ObjectProperty(None)
    support = ObjectProperty(None)

    is_support = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_character(self, *args):
        self.name = self.character.get_id()

    def on_support(self, *args):
        if self.support is not None:
            self.name += "_" + self.support.get_id()

    def update_lock(self, locked):
        self.ids.filledPreview.update_lock(locked)

    def reload(self):
        pass


class FilledCharacterPreview(Widget):

    text_color = ListProperty([0.796, 0.773, 0.678, 1])
    font_name = StringProperty('../res/fnt/Gabriola.ttf')

    preview = ObjectProperty(None, allownone=True)

    new_image_instance = BooleanProperty(False)
    has_screen = BooleanProperty(False)
    emptied = BooleanProperty(False)
    event = ObjectProperty(None, allownone=True)
    has_tag = BooleanProperty(False)

    preview_wgap = NumericProperty(0)
    preview_hgap = NumericProperty(0)
    image_width = NumericProperty(0)

    is_select = BooleanProperty(False)
    is_support = BooleanProperty(False)
    character = ObjectProperty(None, allownone=True)
    support = ObjectProperty(None, allownone=True)

    locked = BooleanProperty(False)
    do_hover = BooleanProperty(True)

    char_button_source = StringProperty('')
    support_button_source = StringProperty('')
    char_button_collide_image = StringProperty('')
    support_button_collide_image = StringProperty('')

    background_source = StringProperty('../res/screens/stats/preview_background.png')
    char_image_source = StringProperty('')
    support_image_source = StringProperty('')
    overlay_source = StringProperty('')

    def __init__(self, **kwargs):
        self.update_overlay()
        self.update_buttons()
        super().__init__(**kwargs)

    def on_is_select(self, *args):
        self.update_overlay()
        self.update_buttons()

    def on_character(self, *args):
        self.char_image_source = self.character.slide_image_source
        self.update_overlay()
        self.update_buttons()

    def on_support(self, *args):
        self.support_image_source = self.support.slide_support_image_source
        self.update_overlay()
        self.update_buttons()

    def update_overlay(self):
        if self.support is not None:
            self.overlay_source = "../res/screens/stats/preview_overlay_full.png"
        elif not self.is_select and not self.locked:
            self.overlay_source = "../res/screens/stats/preview_overlay_empty_add.png"
        else:
            self.overlay_source = "../res/screens/stats/preview_overlay_empty.png"

    def update_buttons(self):
        if self.support is not None:
            self.char_button_source = '../res/screens/buttons/char_button_full'
            self.support_button_source = '../res/screens/buttons/support_button_full'
            self.char_button_collide_image = '../res/screens/buttons/char_button_full.collision.png'
        else:
            self.char_button_source = '../res/screens/buttons/char_button'
            self.support_button_source = '../res/screens/buttons/support_button'
            if self.is_select or self.locked:
                self.support_button_collide_image = '../res/screens/buttons/support_button.normal.png'
                self.char_button_collide_image = '../res/screens/buttons/char_button_select.collision.png'
            else:
                self.support_button_collide_image = '../res/screens/buttons/support_button.collision.png'
                self.char_button_collide_image = '../res/screens/buttons/char_button.collision.png'

    def reload(self):
        pass

    def on_locked(self, *args):
        self.update_overlay()
        self.update_buttons()

    def on_mouse_pos(self, hover):
        if not self.collide_point(*self.to_widget(*hover.pos)):
            return False
        if not self.do_hover:
            return False
        if self.ids.char_button.dispatch('on_mouse_pos', hover):
            return True
        if not self.is_select:
            if self.ids.support_button.dispatch('on_mouse_pos', hover):
                return True
        return False

    def update_lock(self, locked):
        self.locked = locked

    def is_valid_touch(self, *args):
        if not self.has_screen:
            return True
        else:
            current = self.preview.portfolio.parent.parent.current_slide
            if current == self.preview.portfolio:
                return True
        return False

    def on_char_touch_down(self, instance, touch):
        if instance.collide_point(*touch.pos):
            if self.is_valid_touch(instance, touch) and not self.locked:
                if isinstance(touch, WM_MotionEvent):
                    touch.button = 'left'
                touch.grab(self)
                self.emptied = False
                if touch.button == 'left':
                    if not self.is_select:
                        self.event = Clock.schedule_once(lambda dt: self.on_char_empty(instance, touch), .25)
                        return True

    def on_char_empty(self, instance, touch):
        touch.ungrab(self)
        self.emptied = True
        self.preview.set_empty()

    def on_support_touch_down(self, instance, touch):
        if instance.collide_point(*touch.pos):
            if self.is_valid_touch(instance, touch) and not self.locked:
                if isinstance(touch, WM_MotionEvent):
                    touch.button = 'left'
                touch.grab(self)
                self.emptied = False
                if touch.button == 'left':
                    if not self.is_select:
                        self.event = Clock.schedule_once(lambda dt: self.on_support_empty(instance, touch), .25)
                        return True

    def on_support_empty(self, instance, touch):
        touch.ungrab(self)
        self.emptied = True
        self.preview.set_char_screen(False, self.character, None)

    def on_support_touch_up(self, instance, touch):
        if instance.collide_point(*touch.pos):
            if touch.grab_current == self and not self.emptied and not self.locked:
                touch.ungrab(self)
                if isinstance(touch, WM_MotionEvent):
                    touch.button = 'left'
                if touch.button == 'left':
                    if self.event is not None:
                        self.event.cancel()
                    self.preview.show_select_screen(self, True)
                    return True
                elif touch.button == 'right':
                    screen = self.support.get_attr_screen()
                    screen.preview = self.preview
                    screen.reload()
                    App.get_running_app().main.display_screen(screen, True, True)
                    return True
            return False

    def on_char_touch_up(self, instance, touch):
        if instance.collide_point(*touch.pos):
            if touch.grab_current == self and not self.emptied and not self.locked:
                touch.ungrab(self)
                if isinstance(touch, WM_MotionEvent):
                    touch.button = 'left'
                if touch.button == 'left':
                    if self.event is not None:
                        self.event.cancel()
                    if self.is_select:
                        if self.is_support:
                            self.preview.set_char_screen(True, self.preview.char, self.character)
                        else:
                            self.preview.set_char_screen(True, self.character, None)
                        App.get_running_app().main.display_screen(None, False, False)
                        for screen in App.get_running_app().main.screens:
                            if screen.name == 'dungeon_main':
                                screen.update_party_score()
                                break
                    else:
                        self.preview.show_select_screen(self, False)
                    return True
                elif touch.button == 'right':
                    screen = self.character.get_attr_screen()
                    screen.preview = self.preview
                    screen.reload()
                    App.get_running_app().main.display_screen(screen, True, True)
                    return True
            return False
