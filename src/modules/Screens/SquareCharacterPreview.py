from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.widget import Widget

from kivy.uix.label import Label
from kivy.input.providers.wm_touch import WM_MotionEvent
from kivy.clock import Clock

from src.modules.HTButton import HTButton

class SquareCharacterPreview(Widget):
    def __init__(self, main_screen, preview, size, pos, isSelect, has_screen, character, support, isSupport, new_image_instance, **kwargs):
        self.initalized = False
        if pos == (-1, -1):
            super().__init__(size=size, **kwargs)
        else:
            super().__init__(size=size, pos=pos)

        self.main_screen = main_screen
        self.has_screen = has_screen
        self.preview = preview
        self.character = character
        self.support = support
        self.isSelect = isSelect  # Will Alaways be True
        self.isSupport = isSupport
        self.event = None

        self.preview_width = 250
        self.preview_height = 250

        self.preview_wgap = 5 * size[0] / self.preview_width
        self.preview_hgap = 5 * size[1] / self.preview_height
        self.image_width = size[0] - self.preview_wgap * 2
        self.image_height = self.image_width

        self.background = Image(source="../res/screens/stats/preview_square_background.png", size=size, pos=pos, allow_stretch=True)

        self.char_image = character.get_preview_image(new_image_instance)
        self.preview_image_loaded = True
        self.char_image.width = self.image_width
        self.char_image.height = self.image_height
        self.char_image.pos = pos[0] + self.preview_wgap, pos[1] + self.preview_hgap

        self.char_button = Button(background_color=(0, 0, 0, 0), size=size, pos=pos, on_touch_down=self.on_char_touch_down, on_touch_up=self.on_char_touch_up)

        self.char_button = None

        self.char_button = HTButton(size=size, pos=pos, size_hint=(None, None), border=[0, 0, 0, 0], path='../res/screens/buttons/char_button_square')
        self.overlay = Image(source="../res/screens/stats/preview_overlay_square_empty.png", size=size, pos=pos, allow_stretch=True)

        self.add_widget(self.background)
        self.add_widget(self.char_image)
        self.add_widget(self.overlay)

        self.initalized = True

    def reload(self):
        if not self.initalized:
            return
        if not self.preview_image_loaded:
            self.char_image = self.character.get_preview_image(False)
            index = 0
            for child in self.children:
                if child.id == 'image_standin_preview':
                    self.children[index] = self.char_image
                    self.char_image.parent = self
                index += 1
            self.slide_image_loaded = True
            self.char_image.width = self.image_width
            self.char_image.height = self.image_height
            self.char_image.pos = self.pos[0] + self.preview_wgap, self.pos[1] + self.preview_hgap

    def on_size(self, instance, size):
        if not self.initalized:
            return False
        self.background.size = size
        self.overlay.size = size

        self.preview_wgap = 5 * size[0] / self.preview_width
        self.preview_hgap = 5 * size[1] / self.preview_height
        self.image_width = size[0] - self.preview_wgap * 2
        self.image_height = size[1] - self.preview_hgap * 2

        self.char_image.width = self.image_width
        self.char_image.height = self.image_width

        self.char_button.size = size

    def on_pos(self, instance, pos):
        if not self.initalized:
            return False
        self.background.pos = pos
        self.overlay.pos = pos
        self.char_image.pos = pos[0] + self.preview_wgap, pos[1] + self.preview_hgap

        self.char_button.pos = pos

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
                    if self.isSupport:
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