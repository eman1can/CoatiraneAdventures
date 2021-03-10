__all__ = ('Root',)

# Project Imports
from lists import SCREEN_LIST, SCREEN_NON_WHITELIST, SCREEN_WHITELIST

# Kivy Imports
from kivy.uix.screenmanager import ScreenManager, FadeTransition


class Root(ScreenManager):
    def __init__(self, app, **kwargs):
        self._initialized = False
        self.app = app
        super().__init__(**kwargs)

        self.transition = FadeTransition(duration=0.25)
        self.whitelist = []
        self.list = []

        self._create_screen('new_game')
        self.current = 'new_game'
        self._initialized = True

    def make_screens(self):
        # self._create_screen('select_start')
        for screen in self.whitelist:
            self._create_screen(screen)

    def clean_whitelist(self):
        remove = []
        for screen_name in self.whitelist:
            for non_whitelist in SCREEN_NON_WHITELIST:
                if screen_name.startswith(non_whitelist):
                    remove.append(screen_name)
                    break
        for screen_name in remove:
            if screen_name == self.current_screen.name:
                continue
            self.whitelist.remove(screen_name)
            screen_s = None
            for screen in self.screens:
                if screen.name == screen_name:
                    screen_s = screen
                    break
            self.remove_widget(screen_s)
        del remove

    def get_screen(self, screen_name):
        for screen in self.screens:
            if screen.name == screen_name:
                return screen
        for screen in self.list:
            if screen.name == screen_name:
                return screen
        return None

    def display_screen(self, next_screen, direction, track, *args, **kwargs):
        old_screen = None
        if isinstance(next_screen, str):
            for screen in self.screens:
                if screen.name == next_screen:
                    next_screen = screen
                    next_screen.reload(*args, **kwargs)
                    break
            if isinstance(next_screen, str):
                next_screen = self._create_screen(next_screen, *args, **kwargs)
        if len(self.children) > 0:
            old_screen = self.children[0]
        if not direction:
            if len(self.list) > 0:
                next_screen = self.list.pop()
                next_screen.reload(*args)
            else:
                print("No more screens to backtrack.")
                return
        if next_screen not in self.screens:
            self.add_widget(next_screen)
        self.current = next_screen.name
        if old_screen is not None:
            if old_screen.name not in self.whitelist and old_screen.name not in SCREEN_WHITELIST:
                self.remove_widget(old_screen)
            if track:
                self.list.append(old_screen)

    def _create_screen(self, screen_name, *args, **kwargs):
        # for screen_current in self.screens:
        #     if screen_current.name == screen_name:
        #         return screen_current, False
        found = False
        for screen_option, screen_class in SCREEN_LIST.items():
            if screen_name.startswith(screen_option):
                screen = screen_class(*args, **kwargs)
                found = True
                break
        # if screen_name == 'select_screen':
        #     screen = SelectScreen()
        # elif screen_name == 'new_game':
        #     screen = NewGameScreen()
        # elif screen_name == 'town_screen':
        #     screen = TownScreen()
        # elif screen_name == 'dungeon_main':
        #     screen = DungeonMain()
        # elif screen_name == 'tavern_main':
        #     screen = tavern()
        # elif screen_name == 'select_char':
        #     screen = CharacterSelector(self)
        # elif screen_name == 'recruit':
        #     screen = recruit_preview(character=args[0], viewed_characters=args[1])
        # elif screen_name.startswith('char_attr'):
        #     self.whitelist.append(screen_name)
        #     preview = None
        #     if len(args) > 1:
        #         preview = args[1]
        #     screen = CharacterAttributeScreen(char=args[0], preview=preview)
        # elif screen_name.startswith('status_board'):
        #     self.whitelist.append(screen_name)
        #     screen = StatusBoardManager(char=args[0])
        # elif screen_name.startswith('image_preview'):
        #     self.whitelist.append(screen_name)
        #     screen = ImagePreview(char=args[0])
        # elif screen_name.startswith('equipment_change.kv'):
        #     self.whitelist.append(screen_name)
        #     screen = EquipmentChange(char=args[0])
        # elif screen_name == 'gear_change':
        #     screen = GearChange()
        # elif screen_name == 'dungeon_battle':
        #     screen = DungeonBattle(level_num=args[0], is_boss=args[1])
        # elif screen_name == 'dungeon_result':
        #     screen = DungeonResult(args[0], args[1])
        # else:
        if not found:
            raise Exception("Unsupported Screen type", screen_name)
        screen.size = self.size
        self.add_widget(screen)
        return screen

    def on_size(self, instance, size):
        for child in self.screens:
            child.size = self.size
