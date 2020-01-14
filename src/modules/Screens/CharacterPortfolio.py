from kivy.uix.widget import Widget
from src.modules.Screens.CharacterPreview import CharacterPreview

class CharacterPortfolio(Widget):
    def __init__(self, main_screen, size, pos, party):
        self.initalized = False
        super().__init__(size=size, pos=pos)
        self.main_screen = main_screen
        self.party = party

        self.previews = []

        self.slot_x = size[1] * 250 / 935
        self.slot_size = (self.slot_x, size[1])
        self.spacer_x = (self.size[0] - self.slot_x * 8) / (8 + 1)

        current_pos = pos[0] + self.spacer_x

        for x in range(0, 8):
            char = party[x]
            support = party[x + 8]
            preview = CharacterPreview(main_screen, self.slot_size, (current_pos, pos[1]), False, char=char, support=support)
            current_pos += self.spacer_x + self.slot_x

            self.previews.append(preview)
            self.add_widget(preview)
        self.initalized = True

    def on_size(self, instance, size):
        if not self.initalized:
            return
        self.slot_x = size[1] * 250 / 935
        self.slot_size = (self.slot_x, size[1])
        self.spacer_x = (size[0] - self.slot_x * 8) / (8 + 1)

        current_pos = self.pos[0] + self.spacer_x
        for preview in self.previews:
            preview.size = self.slot_size
            preview.pos = current_pos, self.pos[1]
            current_pos += self.spacer_x + self.slot_x

    def on_pos(self, instance, pos):
        if not self.initalized:
            return
        current_pos = pos[0] + self.spacer_x
        for preview in self.previews:
            preview.size = self.slot_size
            preview.pos = current_pos, pos[1]
            current_pos += self.spacer_x + self.slot_x

    def get_party_score(self):
        party_score = 0
        for preview in self.previews:
            party_score += preview.get_score()
        return party_score

    def party_change(self, preview, char, support):
        if not self.initalized:
            return
        for x in range(len(self.previews)):
            if self.previews[x] == preview:
                self.party[x] = char
                self.party[x + 8] = support

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
