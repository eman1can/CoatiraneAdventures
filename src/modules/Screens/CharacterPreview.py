from kivy.properties import BooleanProperty, ObjectProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager

from src.modules.Screens.EmptyCharacterPreview import EmptyCharacterPreviewScreen
from src.modules.Screens.FilledCharacterPreview import FilledCharacterPreviewScreen


class CharacterPreview(ScreenManager):
    initialized = BooleanProperty(False)
    main_screen = ObjectProperty(None)
    is_select = BooleanProperty(False)
    is_disabled = BooleanProperty(False)
    index = NumericProperty(-1)

    char = ObjectProperty(None, allownone=True)
    support = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._size = (0, 0)

        if self.char is None:
            self.set_empty()
        else:
            self.set_char_screen(False, self.char, self.support)
        self.initialized = True

    def on_size(self, instance, size):
        if not self.initialized or self._size == size:
            return
        self._size = size.copy()

        for screen in self.screens:
            screen.size = self.size

    def get_score(self):
        if self.char is None:
            return 0
        else:
            score = self.char.get_score()
            if self.support is not None:
                score += self.support.get_score()
            return score

    def set_empty(self, *args):
        # Want to make an Empty Character Preview and display it
        old_screen = None
        if len(self.children) > 0:
            old_screen = self.children[0]

        emptied = False
        for screen in self.screens:
            if screen.name == 'empty':
                self.current = 'empty'
                emptied = True
                break
        self.char = None
        self.support = None

        if not self.is_select and self.initialized:
            self.parent.party_change(self, self.char, self.support)

        if not emptied:
            preview = EmptyCharacterPreviewScreen(main_screen=self.main_screen, preview=self)
            preview.size = self.size
            self.add_widget(preview)
            self.current = preview.name

        if old_screen is not None:
            self.remove_widget(old_screen)

    def set_char_screen(self, resolve, character, support):
        # Want to set the char screen using the correct overlay
        old_screen = None
        if len(self.children) > 0 and (self.char != character or self.support != support):
            old_screen = self.children[0]
        if resolve:
            spt = self.parent.resolve(self, character, support)
            if spt is not None:
                support = spt
        self.char = character
        self.support = support
        name = self.char.get_name()
        if self.support is not None:
            name += '_' + self.support.get_name()
        for child in self.screens:
            if child.name == name:
                self.transition.direction = 'left'
                self.current = child.name
                if old_screen is not None:
                    if old_screen.name != 'empty':
                        self.remove_widget(old_screen)
                return True
        if not self.is_select and self.initialized:
            self.parent.party_change(self, self.char, self.support)
        preview = FilledCharacterPreviewScreen(self.main_screen, self, False, character, support)
        preview.size = self.size
        preview.preview.pos = (0, 0)# Force update pos, since the screen will never update pos after initialization. Only needed for new screens.
        self.add_widget(preview)
        self.transition.direction = 'left'
        self.current = preview.name
        if old_screen is not None:
            if old_screen.name != 'empty':
                self.remove_widget(old_screen)

    def show_select_screen(self, return_screen, is_support):
        self.main_screen.create_screen('select_char', self, is_support)
        self.main_screen.display_screen('select_char', True, True)

    def reload(self):
        if not isinstance(self.children[0], EmptyCharacterPreviewScreen):
            self.children[0].reload()
