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

    def on_kv_post(self, base_widget):
        party = Refs.gc.get_party(self.party_index)
        for x in range(8):
            preview = CharacterPreview(is_select=False, displayed=True, locked=self.locked, index=x, size_hint=(0.1069, 0.9), pos_hint=({'y': 0, 'center_x': 0.10625 + 0.1125 * x}))
            preview.bind(on_party_change=self.on_party_change)
            preview.bind(on_resolve=self.on_resolve)
            # preview.disabled = not party[x - 1]
            preview.set_char_screen(party[x], party[x + 8], False, None)
            self._previews.append(preview)
            self.add_widget(preview)

    def __str__(self):
        return f"<CharacterPortfolio  - {self.party_index}>"

    # def hover_subscribe(self, widget=None, layer=0, adjust=None, blockin):
        # self._slide_widgets.append((widget, layer))
        # if self.party_index == self._init_party_index:
        # super().hover_subscribe(widget, layer, adjust)

    # def on_enter(self):
        # print(self, 'enter')
        # for widget in self._slide_widgets:
        #     super().hover_subscribe(widget)

    # def on_leave(self):
        # print(self, 'leave')
        # for widget in self._slide_widgets:
        #     super().hover_unsubscribe(widget)

    def on_touch_down(self, touch):
        if self.locked:
            return False
        return super().on_touch_down(touch)

    # def on_touch_hover(self, touch):
    #     if not self.collide_point(*touch.pos):
    #         return False
    #     touch.push()
    #     touch.apply_transform_2d(self.to_widget)
    #     for child in self.children[:]:
    #         if child.dispatch('on_touch_hover', touch):
    #             touch.pop()
    #             return True
    #     touch.pop()
    #     return False

    def on_locked(self, instance, locked):
        for preview in self._previews:
            preview.locked = locked

    def on_current(self, instance, current):
        for preview in self._previews:
            preview.displayed = current

    def close_hints(self):
        for preview in self._previews:
            preview.close_hints()

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
            if preview.character == character:
                start = preview
                break
            elif support != -1 and preview.support == support:
                start = preview
                moving_support = True
                break

        if start is not None:
            if start.support != -1:
                support = start.support
            if not moving_support:
                if destination.character != -1:
                    if before:
                        start.set_char_screen(destination.character, destination.support, False, 'left')
                    else:
                        start.set_char_screen(destination.character, destination.support, False)
                else:
                    if before:
                        start.set_empty('right')
                    else:
                        start.set_empty()
            else:
                if destination.support != -1:
                    if before:
                        start.set_char_screen(start.character, destination.support, False, 'left')
                    else:
                        start.set_char_screen(start.character, destination.support, False)
                else:
                    if before:
                        start.set_char_screen(start.character, -1, False)
                    else:
                        start.set_char_screen(start.character, -1, False, 'left')
        if before:
            destination.set_char_screen(character, support, False)
        else:
            destination.set_char_screen(character, support, False, 'left')

    def reload(self):
        for preview in self._previews:
            preview.reload()
