# Project Imports
# Kivy Imports
from kivy.properties import BooleanProperty, NumericProperty, ObjectProperty

from kivy.uix.screenmanager import ScreenManager
from refs import Refs
# UIX Imports
from uix.screens.character_display.empty_preview import EmptyCharacterPreviewScreen
from uix.screens.character_display.filled_preview import FilledCharacterPreviewScreen


class CharacterPreview(ScreenManager):
    is_select = BooleanProperty(False)
    is_disabled = BooleanProperty(False)
    index = NumericProperty(-1)

    char = ObjectProperty(None, allownone=True)
    support = ObjectProperty(None, allownone=True)

    def __init__(self, app, portfolio, **kwargs):
        self.app = app
        self.portfolio = portfolio
        super().__init__(**kwargs)
        self.transition.direction = 'left'

        if self.char is None:
            self.set_empty()
        else:
            self.set_char_screen(False, self.char, self.support)

    #def get_score(self):
    #    if self.char is None:
    #        return 0
    #    else:
    #        score = self.char.get_score()
    #        if self.support is not None:
    #            score += self.support.get_score()
    #        return round(score, 1)

    def update_lock(self, locked):
        if len(self.children) > 0:
            self.children[0].update_lock(locked)

    def close_hints(self):
        for child in self.children:
            if isinstance(child, FilledCharacterPreviewScreen):
                child.close_hints()

    def set_empty(self, *args):
        # Want to make an Empty character Preview and display it
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

        if not self.is_select:
            self.portfolio.party_change(self, self.char, self.support)

        if not emptied:
            preview = EmptyCharacterPreviewScreen(preview=self)
            preview.size = self.size
            self.add_widget(preview)
            self.current = preview.name
        Refs.gs.get_screen('dungeon_main').update_party_score()
        #if self.dungeon is not None:
        #    self.dungeon.update_party_score()
        if old_screen is not None:
            self.remove_widget(old_screen)
        if self.parent is not None:
            self.parent.reload()

    def on_size(self, *args):
        if self.current_screen is not None:
            self.current_screen.size = self.size

    def set_char_screen(self, resolve, character, support):
        # Want to set the char screen using the correct overlay
        # check to make sure that we need to change the screen
        old_screen = None
        if len(self.children) > 0 and (self.char != character or self.support != support):
            old_screen = self.children[0]
        # do we need to interface with another preview?
        if resolve:
            spt = self.parent.resolve(self, character, support)
            if spt is not None:
                support = spt
        # set new char, support and name values
        self.char = character
        self.support = support
        name = self.char.get_id()
        if self.support is not None:
            name += '_' + self.support.get_id()
        # update information
        if not self.is_select:
            self.portfolio.party_change(self, self.char, self.support)
            Refs.gs.get_screen('dungeon_main').update_party_score()
            #self.dungeon.update_party_score()

        # transition to existing screen if it exists
        for child in self.screens:
            if child.name == name:
                # self.transition.direction = 'left'
                self.current = child.name
                if old_screen is not None:
                    if old_screen.name != 'empty':
                        self.remove_widget(old_screen)
                return True
        # otherwise make new screen and use it
        preview = FilledCharacterPreviewScreen(preview=self, is_support=False, character=character, support=support, size_hint=(None, None))
        preview.size = self.size
        preview.preview.pos = (0, 0)# Force update pos, since the screen will never update pos after initialization. Only needed for new screens.
        self.add_widget(preview)
        self.transition.direction = 'left'
        self.current = preview.name
        if old_screen is not None:
            if old_screen.name != 'empty':
                self.remove_widget(old_screen)
        # self.parent.reload()

    def show_select_screen(self, return_screen, is_support):
        Refs.gs.display_screen('select_char', True, True, self, is_support)

    def reload(self):
        if not isinstance(self.children[0], EmptyCharacterPreviewScreen):
            self.children[0].reload()
