from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty
from kivy.graphics import Color, Rectangle

from src.modules.Screens.EmptyCharacterPreview import EmptyCharacterPreviewScreen
from src.modules.Screens.FilledCharacterPreview import FilledCharacterPreviewScreen

class CharacterPreview(ScreenManager):
        number = NumericProperty(0)

        def __init__(self, main_screen, size, pos, isSelect, **kwargs):
            self.initalized = False
            self.char = None
            self.support = None
            if kwargs.get('char') or kwargs.get('char') is None:
                self.char = kwargs.pop('char')
                if kwargs.get('support') or kwargs.get('support') is None:
                    self.support = kwargs.pop('support')


            if pos == (-1, -1):
                super().__init__(size=size, **kwargs)
            else:
                super().__init__(size=size, pos=pos, **kwargs)

            self.main_screen = main_screen
            self.isSelect = isSelect
            self.isDisabled = False

            if self.char is None:
                self.set_empty()
            else:
                self.set_char_screen(False, self.char, self.support)
            self.initalized = True

        def on_size(self, instance, size):
            if not self.initalized:
                return
            for screen in self.screens:
                screen.size = size
                screen.pos = (0, 0)

        def on_pos(self, *args):
            if not self.initalized:
                return

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
            self.old_screen = None
            if len(self.children) > 0:
                self.old_screen = self.children[0]

            emptied = False
            for screen in self.screens:
                print(screen.name)
                if screen.name == 'empty':
                    self.current = 'empty'
                    emptied = True
                    break
            self.char = None
            self.support = None

            if not self.isSelect and self.initalized:
                self.parent.party_change(self, self.char, self.support)

            if not emptied:
                self.preview = EmptyCharacterPreviewScreen(self.main_screen, self, self.size, self.pos)
                self.add_widget(self.preview)
                self.current = self.preview.name

            if self.old_screen is not None:
                self.remove_widget(self.old_screen)

        def set_char_screen(self, resolve, character, support):
            #Want to set the char screen using the correct overlay
            self.old_screen = None
            if len(self.children) > 0:
                self.old_screen = self.children[0]
            if resolve:
                spt = self.parent.resolve(self, character, support)
                if spt is not None:
                    support = spt
            self.char = character
            self.support = support
            name = self.char.get_name()
            if self.support is not None:
                name += '_' + self.support.get_name()
            for child in self.children:
                if child.name == name:
                    self.transition.direction = 'left'
                    self.current = self.preview.name
                    if self.old_screen != None:
                        if self.old_screen.name != 'empty':
                            self.remove_widget(self.old_screen)
                    return True
            if not self.isSelect and self.initalized:
                self.parent.party_change(self, self.char, self.support)
            self.preview = FilledCharacterPreviewScreen(self.main_screen, self, self.size, self.pos, self.isSelect, character, support, False) #size, pos, Character, Support
            self.add_widget(self.preview)
            self.transition.direction = 'left'
            self.current = self.preview.name
            if self.old_screen != None:
                if self.old_screen.name != 'empty':
                    self.remove_widget(self.old_screen)


        def show_select_screen(self, return_screen, isSupport):
            self.main_screen.create_screen('select_char', self, isSupport)

        def reload(self):
            if not isinstance(self.preview, EmptyCharacterPreviewScreen):
                self.preview.reload()
