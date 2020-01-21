from kivy.properties import ObjectProperty, ListProperty, NumericProperty, BooleanProperty
from kivy.uix.widget import Widget

from src.modules.Screens.CharacterPreview import CharacterPreview


class CharacterPortfolio(Widget):
    initialized = BooleanProperty(False)
    main_screen = ObjectProperty(None)
    dungeon = ObjectProperty(None)
    party = ListProperty(None)
    previews = ListProperty([])

    slot_x = NumericProperty(0)
    slot_size = ListProperty([0, 0])
    spacer_x = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._size = (0, 0)
        self._pos = (0, 0)

        for x in range(0, 8):
            char = self.party[x]
            support = self.party[x + 8]
            preview = CharacterPreview(main_screen=self.main_screen, dungeon=self.dungeon, is_select=False, char=char, support=support, index=x)

            self.previews.append(preview)
            self.add_widget(preview)
        self.initialized = True

    def on_size(self, instance, size):
        if not self.initialized or self._size == size:
            return
        self._size = size.copy()

        self.slot_x = self.height * 250 / 935
        self.slot_size = self.slot_x, self.height
        self.spacer_x = (self.width - self.slot_x * 8) / (8 + 1)

        current_pos = self.x + self.spacer_x
        for preview in self.previews:
            preview.size = self.slot_size
            preview.pos = current_pos, self.y
            current_pos += self.spacer_x + self.slot_x

    def update_lock(self, locked):
        for preview in self.previews:
            preview.update_lock(locked)

    def on_pos(self, instance, pos):
        if not self.initialized or self._pos == pos:
            return
        self._pos = pos.copy()

        current_pos = self.x + self.spacer_x
        for preview in self.previews:
            preview.pos = current_pos, self.y
            current_pos += self.spacer_x + self.slot_x

    def get_party_score(self):
        party_score = 0
        for preview in self.previews:
            party_score += preview.get_score()
        return party_score

    def party_change(self, preview, char, support):
                self.party[preview.index] = char
                self.party[preview.index + 8] = support

    def resolve(self, dest, character, support):
        # if selecting a support that is already selected
        # -> move support
        # if selectign a character that ios already selected that has no support
        # -> move character
        # if selectign a character that is already selected and has a support
        # -> move character and support
        for preview in self.previews:
            if preview != dest:
                if preview.char == character:
                    # print("Char: ", character.get_name(), " in a preview. Setting to: ", dest.char.get_name(), dest.support.get_name())
                    if dest.char is not None:
                        support = preview.support
                        preview.set_char_screen(False, dest.char, dest.support)
                        return support
                    else:
                        preview.set_empty()
                        return None
                elif support is not None and preview.support == support:
                    # move support
                    # print("Support: ", character.get_name(), " in a preview. Setting to: ", dest.support.get_name())
                    preview.set_char_screen(False, preview.char, dest.support)
                    return None

    def reload(self):
        for preview in self.previews:
            preview.reload()
