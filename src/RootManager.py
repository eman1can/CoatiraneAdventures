from src.modules.KivyBase.Hoverable import ScreenManagerH as ScreenManager, ScreenH as Screen
from kivy.uix.screenmanager import FadeTransition

from src.modules.Screens.Equipment.EquipmentChange import EquipmentChange, GearChange
from src.modules.Screens.NewGameScreen import NewGameScreen
from src.modules.Screens.SelectScreen import SelectScreen
from src.modules.Screens.TownScreen import TownScreen
from src.modules.Screens.Dungeon.DungeonMain import DungeonMain
from src.modules.Screens.TavernMain import TavernMain
from src.modules.Screens.RecruitPreview import RecruitPreview
from src.modules.Screens.CharacterDisplay.CharacterSelector import CharacterSelector
from src.modules.Screens.CharacterAttributeScreens.StatusBoard import StatusBoardManager
from src.modules.Screens.ImagePreview import ImagePreview


class Root(ScreenManager):
    def __init__(self, moves, enemies, floors, familias, chars, **kwargs):
        self.initalized = False
        super().__init__(**kwargs)

        self.familias = familias
        self.characters = chars
        self.floors = floors
        self.enemies = enemies
        self.moves = moves

        self.transition = FadeTransition(duration=0.25)
        self.obtained_characters = []
        self.obtained_characters_a = []
        self.obtained_characters_s = []
        self.tavern_locked = False
        self.crafting_locked = True
        self.whitelist = ['dungeon_main', 'tavern_main', 'town_screen', 'select_char']
        self.children = []
        self.parties = [0]
        self.list = []
        self._size = (0, 0)

        for x in range(10):
            self.parties.append([None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None])

        self.create_screen('new_game')
        self.current = 'new_game'
        self.initalized = True

    def make_screens(self):
        self.create_screen('select_screen')
        for screen in self.whitelist:
            self.create_screen(screen)

    def display_screen(self, next_screen, direction, track):
        old_screen = None
        if not isinstance(next_screen, Screen) and next_screen is not None:
            for screen in self.screens:
                if screen.name == next_screen:
                    next_screen = screen
                    break
        if len(self.children) > 0:
            old_screen = self.children[0]
        if not direction:
            if len(self.list) > 0:
                next_screen = self.list.pop()
                next_screen.reload()
            else:
                print("No more screens to backtrack.")
                return
        if next_screen not in self.screens:
            self.add_widget(next_screen)
        self.current = next_screen.name
        if old_screen is not None:
            if old_screen.name not in self.whitelist:
                self.remove_widget(old_screen)
            if track:
                self.list.append(old_screen)

    def create_screen(self, screen_name, *args):
        for screen_current in self.screens:
            if screen_current.name == screen_name:
                return screen_current, False
        if screen_name == 'select_screen':
            screen = SelectScreen()
        elif screen_name == 'new_game':
            screen = NewGameScreen()
        elif screen_name == 'town_screen':
            screen = TownScreen()
        elif screen_name == 'dungeon_main':
            screen = DungeonMain()
        elif screen_name == 'tavern_main':
            screen = TavernMain()
        elif screen_name == 'select_char':
            screen = CharacterSelector()
        elif screen_name == 'recruit':
            screen = RecruitPreview(character=args[0], viewed_characters=args[1])
        elif screen_name.startswith('status_board'):
            self.whitelist.append(screen_name)
            screen = StatusBoardManager(char=args[0])
        elif screen_name.startswith('image_preview'):
            self.whitelist.append(screen_name)
            screen = ImagePreview(char=args[0])
        elif screen_name.startswith('equipment_change'):
            self.whitelist.append(screen_name)
            screen = EquipmentChange(char=args[0])
        elif screen_name == 'gear_change':
            screen = GearChange()
        else:
            raise Exception("Unsupported Screen type", screen_name)
        screen.size = self.size
        self.add_widget(screen)
        return screen, True

    def on_size(self, instance, size):
        if not self.initalized or self._size == size:
            return
        self._size = size

        for child in self.screens:
            # print(child, self.size)
            child.size = self.size