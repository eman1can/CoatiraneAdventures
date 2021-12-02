from kivy.properties import BooleanProperty, ListProperty, NumericProperty

from kivy.uix.relativelayout import RelativeLayout
from loading.kv_loader import load_kv
from refs import Refs
from uix.screens.character_display.preview import CharacterPreview

load_kv(__name__)


class CharacterPortfolio(RelativeLayout):
    party_index = NumericProperty(None)
    locked = BooleanProperty(False)
    current = BooleanProperty(True)

    def __init__(self, **kwargs):
        self.register_event_type('on_party_update')
        self._previews = []
        super().__init__(**kwargs)

    def reload(self, **kwargs):
        self.load_kwargs(kwargs)

        party = Refs.gc.get_party(self.party_index)
        for x, preview in enumerate(self._previews):
            displayed = x == 0 or party[x - 1] != -1
            support_displayed = x == 0 or party[x + 7] != -1
            preview.reload(displayed=displayed, support_displayed=support_displayed, locked=self.locked, is_select=False)

    def on_kv_post(self, base_widget):
        party = Refs.gc.get_party(self.party_index)
        for x in range(8):
            displayed = x == 0 or party[x - 1] != -1
            support_displayed = x == 0 or party[x + 7] != -1
            preview = CharacterPreview(is_select=False, displayed=displayed, support_displayed=support_displayed, locked=self.locked, index=x, size_hint=(0.1069, 0.9), pos_hint=({'y': 0, 'center_x': 0.10625 + 0.1125 * x}))
            preview.bind(on_party_change=self.on_party_change)
            preview.bind(on_resolve=self.on_resolve)
            preview.set_char_screen(party[x], party[x + 8], False, None)
            self._previews.append(preview)
            self.add_widget(preview)

    def on_locked(self, instance, locked):
        for preview in self._previews:
            preview.locked = locked

    # def on_current(self, instance, current):
    #     for preview in self._previews:
    #         preview.displayed = current

    def close_hints(self):
        for preview in self._previews:
            preview.close_hints()

    def on_touch_down(self, touch):
        if self.locked or self.disabled:
            return False
        return super().on_touch_down(touch)

    def on_party_change(self, preview, char, support):
        party = Refs.gc.get_party(self.party_index)
        party[preview.index] = char
        party[preview.index + 8] = support
        Refs.gc.set_party(party, self.party_index)
        self.dispatch('on_party_update')

    def on_party_update(self):
        pass

    # If only character
    # → Not in party
    #   Put in destination
    # → In party before destination
    #   Animate destination from right
    #   Animate start from right
    # → In party after destination
    #   Animate destination from left
    #   Animate start from left
    # If
    def on_resolve(self, destination, character, support):
        before = True
        moving_support = False

        start = None
        for preview in self._previews:
            if preview == destination:
                before = False
                continue
            if preview.get_character() == character:
                start = preview
                break
            elif support != -1 and preview.get_support() == support:
                start = preview
                moving_support = True
                break

        if start is not None:
            if start.get_support() != -1:
                support = start.get_support()
            if not moving_support:
                if destination.get_character() != -1:
                    if before:
                        start.set_char_screen(destination.get_character(), destination.get_support(), False, 'left')
                    else:
                        start.set_char_screen(destination.get_character(), destination.get_support(), False)
                else:
                    if before:
                        start.set_empty('right')
                    else:
                        start.set_empty()
            else:
                if destination.get_support() != -1:
                    if before:
                        start.set_char_screen(start.get_character(), destination.get_support(), False, 'left')
                    else:
                        start.set_char_screen(start.get_character(), destination.get_support(), False)
                else:
                    if before:
                        start.set_char_screen(start.get_character(), -1, False)
                    else:
                        start.set_char_screen(start.get_character(), -1, False, 'left')
        if before:
            destination.set_char_screen(character, support, False)
        else:
            destination.set_char_screen(character, support, False, 'left')


