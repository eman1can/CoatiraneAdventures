from kivy.uix.widget import Widget
import math

class GridPreview(Widget):
    def __init__(self, size, pos, slot_size, characters, main_screen):
        super().__init__(size=size, pos=pos)
        self.main_screen = main_screen
        self.slot_width = math.floor(size[0] / slot_size[0]) - 1
        self.spacer_size = (size[0] - (slot_size[0] * self.slot_width)) / (self.slot_width + 1)
        offset_pos = pos[0] + self.spacer_size, pos[1] + size[1] - self.spacer_size
        index = 0
        for character in characters:
            slot_pos = offset_pos[0] + slot_size[0] * index + self.spacer_size * (index + 1), offset_pos[1] - (size[0] - (slot_size[1] * index + self.spacer_size * index))
            # char = CharacterPreview(slot_size, slot_pos, True, main_screen, char=character, square=True)
            index += 1
