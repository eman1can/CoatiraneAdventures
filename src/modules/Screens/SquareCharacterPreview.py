from kivy.app import App
from kivy.input.providers.wm_touch import WM_MotionEvent
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty

from src.modules.KivyBase.Hoverable import RelativeLayoutH as RelativeLayout


class SquareCharacterPreview(RelativeLayout):
    main_screen = ObjectProperty(None)
    preview = ObjectProperty(None)

    is_select = BooleanProperty(False)
    has_screen = BooleanProperty(False)
    is_support = BooleanProperty(False)
    new_image_instance = BooleanProperty(False)

    event = ObjectProperty(None)
    has_tag = BooleanProperty(False)
    has_stat = BooleanProperty(False)
    tag = ObjectProperty(None)

    character = ObjectProperty(None)
    support = ObjectProperty(None)

    char_button_source = StringProperty('../res/screens/buttons/char_button_square')
    char_button_collide_image = StringProperty('')

    background_source = StringProperty('../res/screens/stats/preview_square_background.png')
    char_image_source = StringProperty('')
    overlay_source = StringProperty('')

    def __init__(self, **kwargs):
        self.register_event_type('on_mouse_pos')
        self.update_overlay()
        super().__init__(**kwargs)

    def on_character(self, *args):
        self.char_image_source = self.character.preview_image_source
        self.update_overlay()

    def update_overlay(self):
        if self.has_stat:
            self.overlay_source = '../res/screens/stats/preview_overlay_square_stat.png'
        else:
            self.overlay_source = '../res/screens/stats/preview_overlay_square_empty.png'

    def reload(self):
        pass

    def on_mouse_pos(self, hover):
        if not self.collide_point(*self.to_widget(*hover.pos)):
            return False
        if self.ids.char_button.dispatch('on_mouse_pos', hover):
            return True
        return False

    def on_char_touch_down(self, instance, touch):
        if instance.collide_point(*touch.pos):
            touch.grab(self)
            self.emptied = False

    def on_char_touch_up(self, instance, touch):
        root = App.get_running_app().main
        if instance.collide_point(*touch.pos):
            if touch.grab_current == self and not self.emptied:
                touch.ungrab(self)
                if isinstance(touch, WM_MotionEvent):
                    touch.button = 'left'
                if touch.button == 'left':
                    if self.event is not None:
                        self.event.cancel()
                    if self.is_support:
                        self.preview.set_char_screen(True, self.preview.char, self.character)
                    else:
                        self.preview.set_char_screen(True, self.character, None)
                    root.display_screen(None, False, False)
                    for screen in root.screens:
                        if screen.name == 'dungeon_main':
                            screen.update_party_score()
                            break
                    return True
                elif touch.button == 'right':
                    screen = self.character.get_attr_screen()
                    screen.preview = self.preview
                    root.display_screen(screen, True, True)
                    return True
            return False
