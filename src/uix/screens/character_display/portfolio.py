from kivy.properties import ListProperty, NumericProperty, BooleanProperty
from kivy.uix.relativelayout import RelativeLayout

from uix.screens.character_display.preview import CharacterPreview

from loading.kv_loader import load_kv
load_kv(__name__)


class CharacterPortfolio(RelativeLayout):
    #dungeon = ObjectProperty(None)
    party = ListProperty(None)
    party_index = NumericProperty(None)
    previews = ListProperty([])
    locked = BooleanProperty(False)

    #slot_x = NumericProperty(0)
    #slot_size = ListProperty([0, 0])
    #spacer_x = NumericProperty(0)

    def __init__(self, app, dungeon, current_party_index, **kwargs):
        self.app = app
        self.dungeon = dungeon
        self._slide_widgets = []
        self._init_party_index = current_party_index
        super().__init__(**kwargs)
        self.update_party()

    def __str__(self):
        return f"<CharacterPortfolio  - {self.party_index}>"

    def hover_subscribe(self, widget=None, layer=0, adjust=None):
        # self._slide_widgets.append((widget, layer))
        # if self.party_index == self._init_party_index:
        super().hover_subscribe(widget, layer, adjust)

    # def on_enter(self):
        # print(self, 'enter')
        # for widget in self._slide_widgets:
        #     super().hover_subscribe(widget)

    # def on_leave(self):
        # print(self, 'leave')
        # for widget in self._slide_widgets:
        #     super().hover_unsubscribe(widget)

    def update_party(self):
        self.previews.clear()
        self.clear_widgets()
        for x in range(0, 8):
            char = self.party[x]
            support = self.party[x + 8]
            preview = CharacterPreview(self.app, self, is_select=False, char=char, support=support, index=x, size_hint=(0.1069, 0.9), pos_hint=({'y': 0, 'center_x': 0.10625 + 0.1125 * x}))
            self.previews.append(preview)
            self.add_widget(preview)

    def on_touch_down(self, touch):
        if self.locked:
            return False
        return super().on_touch_down(touch)

    def update_lock(self, locked):
        self.locked = int(locked)
        for preview in self.previews:
            preview.update_lock(locked)

    def close_hints(self):
        for preview in self.previews:
            preview.close_hints()

    def on_touch_hover(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        touch.push()
        touch.apply_transform_2d(self.to_widget)
        for child in self.children[:]:
            if child.dispatch('on_touch_hover', touch):
                touch.pop()
                return True
        touch.pop()
        return False

    #def get_party_score(self):
    #    party_score = 0
    #    for preview in self.previews:
    #        party_score += preview.get_score()
    #    return round(party_score, 1)

    def party_change(self, preview, char, support):
        self.party[preview.index] = char
        self.party[preview.index + 8] = support
        self.dungeon.content.set_party(self.party, self.party_index)

    def is_current(self):
        return self.parent.parent.check_current(self)

    def resolve(self, dest, character, support):
        # if selecting a support that is already selected
        # -> move support
        # if selecting a character that ios already selected that has no support
        # -> move character
        # if selecting a character that is already selected and has a support
        # -> move character and support
        before = True
        for preview in self.previews:
            if preview != dest:
                if preview.char == character:
                    if before:
                        preview.transition.direction = 'right'
                        dest.transition.direction = 'right'
                    else:
                        preview.transition.direction = 'left'
                        dest.transition.direction = 'left'
                    if dest.char is not None:
                        support = preview.support
                        preview.set_char_screen(False, dest.char, dest.support)
                        return support
                    else:
                        preview.set_empty()
                        return None
                elif support is not None and preview.support == support:
                    if before:
                        preview.transition.direction = 'right'
                        dest.transition.direction = 'right'
                    else:
                        preview.transition.direction = 'left'
                        dest.transition.direction = 'left'
                    preview.set_char_screen(False, preview.char, dest.support)
                    return None
            else:
                before = False

    def reload(self):
        for preview in self.previews:
            preview.reload()
