from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.properties import BooleanProperty
from src.modules.Screens.SinglePreview import SinglePreview
from src.modules.Screens.ScrollPreview import ScrollPreview
from src.modules.Screens.GridPreview import GridPreview
from src.modules.HTButton import HTButton

class CharacterSelector(Screen):
    toggle = BooleanProperty(False)  # When False, Is Slots
    def __init__(self, main_screen, preview, isSupport, **kwargs):
        size = main_screen.size
        super().__init__(size=size)
        self.name = 'select_char'

        self.background = Image(source="../res/screens/backgrounds/background.png", size=size, pos=(0, 0), keep_ratio=True, allow_stretch=True)

        if not isSupport:
            characters = main_screen.obtained_characters_a.copy()
        else:
            characters = main_screen.obtained_characters_s.copy()

        for x in range(len(characters)):
            characters[x] = main_screen.characters[characters[x]]

        has_left = preview.char is not None and not isSupport or isSupport and preview.support is not None
        self.slot_size = (size[1] * .6 * (250 / 935), size[1] * .6)
        self.grid_size = (self.slot_size[0], self.slot_size[0])
        if has_left:
            self.single_window_size = size[0] * .15, self.size[1] * .85
            self.single_window_pos = (0, 0)
            self.multi_window_size = size[0] - self.single_window_size[0], self.single_window_size[1]
            self.multi_window_pos = self.single_window_size[0], 0
            if isSupport:
                char = preview.support
            else:
                char = preview.char
            self.single = SinglePreview(main_screen, preview, self.single_window_size, self.single_window_pos, self.slot_size, char, isSupport)
        else:
            self.single_window_size = (0, 0)
            self.single = None
            self.multi_window_size = size[0], size[1] * .85
            self.multi_window_pos = 0, 0

        self.scroll = ScrollPreview(main_screen, preview, self.multi_window_size, self.multi_window_pos, self.slot_size, characters, isSupport)
        self.grid = GridPreview(main_screen, preview, self.multi_window_size, self.multi_window_pos, self.grid_size, characters, isSupport)

        button_size = size[0] * 0.075 * 475 / 125, size[1] * 0.075
        self.toggle_button = HTButton(size=button_size, pos=((size[0] - button_size[0] * 3) * 2/3 + button_size[0] * 2, size[1] * 0.8875), size_hint=(None, None), color=(0,0,0,1), border=[0, 0, 0, 0], text="Switch Display", font_size=button_size[1] * 0.8, font_name="../res/fnt/Gabriola.ttf", path='../res/screens/buttons/long_stat', toggle_enabled=True, on_state_one=self.on_scroll, on_state_two=self.on_grid)

        self.add_widget(self.background)
        if has_left:
            self.add_widget(self.single)

        if self.toggle:
            self.add_widget(self.grid)
        else:
            self.add_widget(self.scroll)

        self.add_widget(self.toggle_button)

        if self.single is not None:
            self.single.reload()

    def reload(self):
        pass

    def on_scroll(self, instance):
        self.remove_widget(self.grid)
        self.add_widget(self.scroll)

    def on_grid(self, instance):
        self.remove_widget(self.scroll)
        self.add_widget(self.grid)
