from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from src.modules.Screens.SinglePreview import SinglePreview
from src.modules.Screens.ScrollPreview import ScrollPreview
# from src.modules.Screens.GridPreview import GridPreview

class CharacterSelector(Screen):
    def __init__(self, main_screen, preview, isSupport, **kwargs):
        size = main_screen.size
        super().__init__(size=size)

        self.background = Image(source="../res/screens/backgrounds/background.png", size=size, pos=(0, 0), keep_ratio=True, allow_stretch=True)
        self.add_widget(self.background)

        hasLeft = preview.char is not None and not isSupport or isSupport and preview.support is not None
        if not isSupport:
            characters = main_screen.obtained_characters_a.copy()
        else:
            characters = main_screen.obtained_characters_s.copy()

        for x in range(len(characters)):
            characters[x] = main_screen.characters[characters[x]]

        self.slot_size = (size[1] * .6 * (250 / 935), size[1] * .6)
        self.grid_size = (self.slot_size[0], self.slot_size[0])
        if hasLeft:
            self.single_window_size = size[0] * .15, self.size[1] * .85
            self.multi_window_size = size[0] - self.single_window_size[0], self.single_window_size[1]
            self.multi_window_pos = self.single_window_size[0], 0
            if isSupport:
                char = preview.support
            else:
                char = preview.char
            self.single = SinglePreview(main_screen, preview, self.single_window_size, (self.width * .05, self.height * .05), self.slot_size, char, isSupport)
            self.add_widget(self.single)
        else:
            self.single_window_size = (0, 0)
            self.single = None
            self.multi_window_size = size[0], size[1] * .85
            self.multi_window_pos = 0, 0
        self.scroll = ScrollPreview(main_screen, preview, self.multi_window_size, self.multi_window_pos, self.slot_size, characters, isSupport)
        self.add_widget(self.scroll)
        if self.single is not None:
            self.single.reload()
        # self.grid = GridPreview(self.multi_window_size, self.multi_window_pos, self.grid_size, characters, main_screen)
