# Project Imports
# Kivy Imports
from kivy.properties import BooleanProperty, NumericProperty, ObjectProperty

from kivy.cache import Cache
from kivy.uix.screenmanager import NoTransition, ScreenManager, SlideTransition
from refs import Refs
# UIX Imports
from uix.screens.character_display.empty_preview import EmptyCharacterPreviewScreen
from uix.screens.character_display.filled_preview import FilledCharacterPreviewScreen


class CharacterPreview(ScreenManager):
    is_select = BooleanProperty(False)
    locked = BooleanProperty(False)
    index = NumericProperty(-1)

    displayed = BooleanProperty(True)
    support_displayed = BooleanProperty(True)

    def __init__(self, **kwargs):
        self.register_event_type('on_party_change')
        self.register_event_type('on_resolve')
        self._old_slides = []
        self._displayed_character = -1
        self._displayed_support = -1
        super().__init__(**kwargs)
        self.transition = NoTransition()
        self.set_empty()
        self.transition = SlideTransition()
        self.transition.direction = 'left'

    def reload(self, **kwargs):
        self.load_kwargs(kwargs)
        if self.current_screen is not None:
            self.current_screen.reload(locked=self.locked, displayed=self.displayed, support_displayed=self.support_displayed)

    def on_locked(self, *args):
        if self.current_screen is not None:
            self.current_screen.locked = self.locked

    def close_hints(self):
        if self.current_screen is not None:
            self.current_screen.close_hints()

    def on_displayed(self, *args):
        if self.current_screen is not None:
            self.current_screen.displayed = self.displayed

    def on_support_displayed(self, *args):
        if self.current_screen is not None:
            self.current_screen.support_displayed = self.support_displayed

    def on_size(self, instance, size):
        if self.current_screen is not None:
            self.current_screen.size = self.size

    def on_select_screen(self, preview, is_support):
        Refs.gs.display_screen('select_char', True, True, self, is_support)

    def on_attr_screen(self, preview, is_support):
        if is_support:
            character = Refs.gc.get_char_by_index(self._displayed_support)
        else:
            character = Refs.gc.get_char_by_index(self._displayed_character)
        Refs.gs.display_screen('char_attr_' + character.get_id(), True, True, character.get_index(), self)

    def on_remove(self, preview, is_support):
        if is_support:
            self.set_char_screen(self._displayed_character, -1, False)
        else:
            self.set_empty()

    def on_current(self, instance, value):
        super().on_current(instance, value)
        if self.current_screen is not None:
            self.current_screen.locked = self.locked
            self.current_screen.displayed = self.displayed
            self.current_screen.support_displayed = self.support_displayed

    def get_character(self):
        return self._displayed_character

    def get_support(self):
        return self._displayed_support

    def set_empty(self, direction='left'):
        self._displayed_character = self._displayed_support = -1
        if not self.is_select:
            self.dispatch('on_party_change', -1, -1)

        self.transition.direction = direction

        old_screen = self.current_screen
        if 'empty' in self.screens:
            self.current = 'empty'
        else:
            empty = EmptyCharacterPreviewScreen(size_hint=(None, None))
            empty.bind(on_select=self.on_select_screen)
            empty.size = self.size
            self.switch_to(empty)

        if old_screen is not None:
            self.remove_widget(old_screen)

    def set_char_screen(self, character, support, resolve, direction='right'):
        if character == self._displayed_character and support == self._displayed_support:
            return

        if resolve:
            self.dispatch('on_resolve', character, support)
            return

        self._displayed_character, self._displayed_support = character, support

        if not self.is_select:
            self.dispatch('on_party_change', character, support)

        char = Refs.gc.get_char_by_index(character)
        supt = Refs.gc.get_char_by_index(support)

        name = char.get_id()
        if supt is not None:
            name += '_' + supt.get_id()

        screen = Cache.get('preview.slides', name)
        in_cache = screen is not None
        if in_cache and screen.parent is not None:
            screen = None

        old_screen = self.current_screen

        if screen is None:
            screen = FilledCharacterPreviewScreen(is_support=False, character=character, support=support, size_hint=(None, None))
            preview = screen.get_root()
            preview.bind(on_select=self.on_select_screen)
            preview.bind(on_attr=self.on_attr_screen)
            preview.bind(on_empty=self.on_remove)
            screen.size = self.size
            if not in_cache:
                Cache.append('preview.slides', name, screen)

        screen.locked = self.locked
        screen.displayed = self.displayed
        screen.support_displayed = self.support_displayed

        if direction is None:
            self.transition = NoTransition()
        else:
            self.transition = SlideTransition()
            self.transition.direction = direction
        self.switch_to(screen)

        if old_screen and old_screen != 'empty':
            self.remove_widget(old_screen)

    def on_party_change(self, char, support):
        pass

    def on_resolve(self, character, support):
        pass
