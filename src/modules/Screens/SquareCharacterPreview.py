from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.widget import Widget

from kivy.uix.label import Label
from kivy.input.providers.wm_touch import WM_MotionEvent
from kivy.clock import Clock

from src.modules.HTButton import HTButton

class SquareCharacterPreview(Widget):
    initialized = BooleanProperty(False)
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

    def __init__(self, **kwargs):
        super().__init__(size_hint=(None, None), **kwargs)

        self._size = (0, 0)
        self._pos = (-1, -1)

        self.background = Image(source="../res/screens/stats/preview_square_background.png", allow_stretch=True)

        self.char_image = self.character.get_preview_image(self.new_image_instance)
        self.preview_image_loaded = True

        self.char_button = HTButton(path='../res/screens/buttons/char_button_square')
        self.char_button.bind(on_touch_down=self.on_char_touch_down, on_touch_up=self.on_char_touch_up)

        if self.has_stat:
            self.overlay = Image(source="../res/screens/stats/preview_overlay_square_stat.png", allow_stretch=True)
        else:
            self.overlay = Image(source="../res/screens/stats/preview_overlay_square_empty.png", allow_stretch=True)

        self.add_widget(self.background)
        self.add_widget(self.char_image)
        self.add_widget(self.char_button)
        self.add_widget(self.overlay)

        self.stars = []
        for level in self.character.ranks:
            if level.unlocked:
                if not level.broken:
                    star = Image(source="../res/screens/stats/star.png", size_hint=(None, None), opacity=1)
                else:
                    star = Image(source="../res/screens/stats/rankbrk.png", size_hint=(None, None), opacity=1)
            else:
                star = Image(source='../res/screens/stats/star.png', size_hint=(None, None), opacity=0)
            self.stars.append(star)
            self.add_widget(star)

        self.initialized = True

    def reload(self):
        if not self.initialized:
            return
        if not self.preview_image_loaded:
            self.char_image = self.character.get_preview_image(False)
            index = 0
            for child in self.children:
                if child.id == 'image_standin_preview':
                    self.children[index] = self.char_image
                    self.char_image.parent = self
                index += 1
            self.preview_image_loaded = True

    def on_size(self, instance, size):
        if not self.initialized or self._size == size:
            return False
        self._size = size.copy()
        self.background.size = self.size
        self.overlay.size = self.size
        self.char_image.size = self.size
        self.char_button.size = self.size

        if self.has_tag:
            self.tag.font_size = size[0] * 0.125
            self.tag.texture_update()
            self.tag.size = self.width, self.tag.texture_size[1]

        star_width = (self.height * 62 / 250) / 2.5
        for star in self.stars:
            star.size = star_width, star_width

    def on_pos(self, instance, pos):
        if not self.initialized or self._pos == pos:
            return False
        self._pos = pos.copy()

        self.background.pos = self.pos
        self.overlay.pos = self.pos
        self.char_image.pos = self.pos
        self.char_button.pos = self.pos

        if self.has_tag:
            self.tag.pos = self.x + self.width / 2 - self.tag.width / 2, self.height - self.tag.height

        preview_wgap = self.width * 5 / 250
        preview_hgap = self.height * 5 / 250

        star_width = (self.height * 62 / 250) / 2.5
        dist = ((self.width - preview_wgap * 2) - star_width * 10) / 2
        start = (self.width - preview_wgap * 2 - (star_width * 10 + dist * 10)) / 4
        count = 0
        for star in self.stars:
            star.pos = self.x + preview_wgap + star_width * count + dist * count + start, self.y + preview_hgap
            count += 1

    def on_char_touch_down(self, instance, touch):
        if instance.collide_point(*touch.pos):
            touch.grab(self)
            self.emptied = False

    def on_char_touch_up(self, instance, touch):
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
                    self.main_screen.display_screen(None, False, False)
                    for screen in self.main_screen.screens:
                        if screen.name == 'dungeon_main':
                            screen.update_party_score()
                            break
                    return True
                elif touch.button == 'right':
                    screen = self.character.get_attr_screen()
                    screen.main_screen = self.main_screen
                    screen.preview = self.preview
                    screen.reload()
                    self.main_screen.display_screen(screen, True, True)
                    return True
            return False