from kivy.uix.widget import Widget

from src.modules.Screens.FilledCharacterPreview import FilledCharacterPreview

class SinglePreview(Widget):
    def __init__(self, main_screen, preview, size, pos, slot_size, character, isSupport):
        super().__init__(size=size, pos=pos)
        self.slot_size = slot_size
        self.main_screen = main_screen
        self.slot_pos = pos[0] + (size[0] - slot_size[0]) / 2, pos[1] + (size[1] - slot_size[1]) / 2
        self.char = FilledCharacterPreview(main_screen, preview, slot_size, self.slot_pos, True, False, character, None, isSupport, True)
        self.add_widget(self.char)

    def reload(self):
        self.char.reload()
