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
    displayed = BooleanProperty(True)
    locked = BooleanProperty(False)
    index = NumericProperty(-1)

    character = NumericProperty(-1)
    support = NumericProperty(-1)

    def __init__(self, **kwargs):
        self.register_event_type('on_party_change')
        self.register_event_type('on_resolve')
        self._old_slides = []
        super().__init__(**kwargs)
        self.transition.direction = 'left'

    def on_kv_post(self, base_widget):
        if self.character == -1:
            self.set_empty()
        else:
            self.set_char_screen(self.character, self.support, False)

    def on_locked(self, instance, locked):
        if self.current_screen is not None:
            self.current_screen.update_lock()

    def close_hints(self):
        if self.current_screen is not None:
            self.current_screen.close_hints()

    def on_displayed(self, instance, displayed):
        if self.current_screen is not None:
            self.current_screen.current = displayed

    def on_size(self, instance, size):
        if self.current_screen is not None:
            self.current_screen.size = self.size

    def on_select_screen(self, preview, is_support):
        Refs.gs.display_screen('select_char', True, True, self, is_support)

    def on_attr_screen(self, preview, is_support):
        if is_support:
            character = Refs.gc.get_char_by_index(self.support)
        else:
            character = Refs.gc.get_char_by_index(self.character)
        Refs.gs.display_screen('char_attr_' + character.get_id(), True, True, character.get_index(), self)

    def on_remove(self, preview, is_support):
        if is_support:
            self.set_char_screen(self.character, -1, False)
        else:
            self.set_empty()

    def reload(self):
        if self.current_screen is not None and self.current_screen != 'empty':
            self.current_screen.reload()

    def set_empty(self, direction='left'):
        self.character = self.support = -1

        if not self.is_select:
            self.dispatch('on_party_change', -1, -1)

        # if skip_transition:
        #     self.transition = NoTransition()
        # else:
        #     self.transition = SlideTransition()

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
        if character == self.character and support == self.support:
            return

        if resolve:
            self.dispatch('on_resolve', character, support)
            return

        self.character, self.support = character, support
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
