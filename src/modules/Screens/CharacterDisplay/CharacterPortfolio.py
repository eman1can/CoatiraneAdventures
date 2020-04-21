from kivy.app import App
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, BooleanProperty

from src.modules.KivyBase.Hoverable import RelativeLayoutH as RelativeLayout
from src.modules.Screens.CharacterPreview import CharacterPreview


class CharacterPortfolio(RelativeLayout):
    dungeon = ObjectProperty(None)
    party = ListProperty(None)
    party_index = NumericProperty(None)
    previews = ListProperty([])
    locked = BooleanProperty(False)

    slot_x = NumericProperty(0)
    slot_size = ListProperty([0, 0])
    spacer_x = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        for x in range(0, 8):
            char = self.party[x]
            support = self.party[x + 8]
            preview = CharacterPreview(dungeon=self.dungeon, portfolio=self, is_select=False, char=char, support=support,
                                       index=x, id='char_preview - ' + str(x), size_hint=(0.1069, 0.9), pos_hint=({'y': 0, 'center_x': 0.10625 + 0.1125 * x}))
            self.previews.append(preview)
            self.add_widget(preview)

    def update_lock(self, locked):
        self.locked = int(locked)
        for preview in self.previews:
            preview.update_lock(locked)

    def on_mouse_pos(self, hover):
        if not self.collide_point(*hover.pos):
            return False
        for preview in self.previews:
            if preview.dispatch('on_mouse_pos', hover):
                return True

    def get_party_score(self):
        party_score = 0
        for preview in self.previews:
            party_score += preview.get_score()
        return round(party_score, 1)

    def party_change(self, preview, char, support):
        self.party[preview.index] = char
        self.party[preview.index + 8] = support
        App.get_running_app().main.parties[self.party_index] = self.party

    def is_current(self):
        return self.parent.parent.check_current(self)

    def resolve(self, dest, character, support):
        # if selecting a support that is already selected
        # -> move support
        # if selecting a character that ios already selected that has no support
        # -> move character
        # if selecting a character that is already selected and has a support
        # -> move character and support
        for preview in self.previews:
            if preview != dest:
                if preview.char == character:
                    if dest.char is not None:
                        support = preview.support
                        preview.set_char_screen(False, dest.char, dest.support)
                        return support
                    else:
                        preview.set_empty()
                        return None
                elif support is not None and preview.support == support:
                    preview.set_char_screen(False, preview.char, dest.support)
                    return None

    def reload(self):
        for preview in self.previews:
            preview.reload()
