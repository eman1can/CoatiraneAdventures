from kivy.config import Config
Config.set('input', 'mouse', 'mouse, multitouch_on_demand')
Config.set('kivy', 'exit_on_escape', 0)
Config.set('kivy', 'window_icon', '../res/screens/icon.png')
Config.set('graphics', 'fbo', 'hardware')
Config.set('graphics', 'default_font', '../res/fnt/Gabriola.ttf')
from kivy.utils import platform
if platform == 'win':
    Config.set('kivy', 'pause_on_minimize', 1)

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

from src.entitites.Character.Character import Character, Move
from src.entitites.Character.Familia import Familia
from src.entitites.EnemyType import EnemyType
from src.modules.Screens.NewGameScreen import NewGameScreen
from src.modules.Screens.SelectScreen import SelectScreen
from src.modules.Screens.TownScreen import TownScreen
from src.modules.Screens.Dungeon.DungeonMain import DungeonMain
from src.modules.Screens.Dungeon.Floor import Floor
from src.modules.Screens.TavernMain import TavernMain
from src.modules.Screens.RecruitPreview import RecruitPreview
from src.modules.Screens.CharacterSelector import CharacterSelector
import math

class Root(ScreenManager):
    def __init__(self, moves, enemies, floors, familias, chars, **kwargs):
        self.initalized = False
        super().__init__(**kwargs)
        App.root = self

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
        self.create_screen('select_screen')
        for screen in self.whitelist:
            self.create_screen(screen)
        self.current = 'new_game'
        self.initalized = True

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
        screen = None
        for screen_current in self.screens:
            if screen_current.name == screen_name:
                return screen_current, False
        if screen_name == 'select_screen':
            screen = SelectScreen(main_screen=self)
        elif screen_name == 'new_game':
            screen = NewGameScreen(main_screen=self)
        elif screen_name == 'town_screen':
            screen = TownScreen(main_screen=self)
        elif screen_name == 'dungeon_main':
            screen = DungeonMain(main_screen=self)
        elif screen_name == 'tavern_main':
            screen = TavernMain(main_screen=self)
        elif screen_name == 'select_char':
            screen = CharacterSelector(main_screen=self)
        elif screen_name == 'recruit':
            screen = RecruitPreview(character=args[0], viewed_characters=args[1], main_screen=self)
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
            print(child, self.size)
            child.size = self.size


class GameApp(App):
    title = 'Coatirane Adventures - Alpha 0.1'

    def __init__(self, *args, **kwargs):
        Window.bind(on_resize=self.on_resize)
        Window.bind(on_request_close=self.close_window)
        self.initalized = False
        super().__init__(**kwargs)
        self.program_type = "test"
        self._size = (0, 0)

    def build(self):
        if platform == 'win':
            import ctypes
            user32 = ctypes.windll.user32
            width = math.floor(user32.GetSystemMetrics(0) * 2 / 3)
            height = math.floor(user32.GetSystemMetrics(1) * 2 / 3)
            Window.size = width, height
            Window.left = math.floor((user32.GetSystemMetrics(0) - width) / 2)
            Window.top = math.floor((user32.GetSystemMetrics(1) - height) / 2)
            Window.borderless = 0
        elif platform == 'android' or platform == 'ios':
            width, height = Window.size
        else:
            raise Exception("Running on unsupported Platform!")
        self._size = (width, height)
        self.background = Image(source="../res/screens/game_bounds.png", allow_stretch=True, size=(width, height))
        self.loading_screen = Image(source="../res/screens/splash.bmp", allow_stretch=True, keep_ratio=True, size=(width, height))
        self.background.add_widget(self.loading_screen)
        return self.background

    def load_game(self, dt):
        moves = self.build_moves()
        enemies = self.build_enemies(moves)
        familias = self.build_familias()
        chars = self.build_chars(moves, familias)
        floors = self.build_floors(enemies)

        self.root = Root(moves, enemies, floors, familias, chars)
        self.root.size = Window.size

        self.background.remove_widget(self.loading_screen)
        self.background.add_widget(self.root)
        self.initalized = True

    def close_window(self, *args):
        if platform == 'win':
            Window.close()


    def on_stop(self):
        # On IOS and Android, DO NOT programmically close; Let OS handle
        #Save game stuff
        print("Stop the App!")
        if platform == 'win':
            quit()

    def on_pause(self):
        pass  # Do Save game stuff


    def on_resize(self, *args):
        Clock.unschedule(self.fix_size)
        Clock.schedule_once(self.fix_size, .25)

    def fix_size(self, *args):
        if not self.initalized or self._size == Window.size:
            return
        self._size = Window.size

        self.background.size = Window.size
        offset = Window.width/2 - self.background.norm_image_size[0]/2, Window.height/2 - self.background.norm_image_size[1]/2

        self.root.size = self.background.norm_image_size
        self.root.pos = offset

    def build_moves(self):
        print("Loading Moves")
        moves = []
        file = open("../save/char_load_data/" + self.program_type + "/Moves.txt", "r")
        totalNum = 0
        if file.mode == 'r':
            count = 0
            for x in file:
                if x[0] != '/':
                    totalNum += 1
                    values = x[:-1].split(",", -1)
                    # MoveName, MovePower, EffectNum, MoveEffects
                    effects = []
                    effects.append(["Stun", 0])
                    effects.append(["Sleep", 0])
                    effects.append(["Poison", 0])
                    effects.append(["Burn", 0])
                    effects.append(["Charm", 0])
                    effects.append(["Seal", 0])
                    effects.append(["Taunt", 0])
                    for x in range(int(values[3])):
                        for y in effects:
                            if values[5 + (x * 2)] == y[0]:
                                y[1] = float(values[6 + (x * 2)])
                    covername = None
                    # print(str(bool(values[1] == "True")))
                    if bool(values[1] == "True"):
                        covername = values[2]
                    # MoveName, MoveCover, CoverName, MoveType, MovePower, Stun, Charm, Poision, Burn, Sleep, Seal, Taunt
                    moves.append(
                        Move(values[0], bool(values[1] == "True"), covername, int(values[3]), values[4], effects))
            file.close()
            print("Loaded %d moves." % totalNum)
        else:
            raise Exception("Failed to open Move Definition file!")
        return moves

    def build_enemies(self, moves):
        print("Loading Enemies")
        enemies = []
        file = open("../save/enemy_load_data/" + self.program_type + "/Enemies.txt", "r")
        totalNum = 0
        if file.mode == 'r':
            for x in file:
                if x[0] != '/':
                    totalNum += 1
                    values = x[:-1].split(",", -1)
                    EnemyMoves = []
                    movePropabilities = []
                    for x in range(int(values[14])):
                        EnemyMoves.append(Move.getmove(moves, values[15 + (2 * x)]))
                        movePropabilities.append(values[16 + (2 * x)])
                    enemies.append(
                        EnemyType(values[0], int(values[3]), int(values[1]), int(values[2]), int(values[4]),
                                  int(values[5]), int(values[6]), int(values[7]), int(values[8]), int(values[9]),
                                  int(values[10]), int(values[11]), int(values[12]), int(values[13]), EnemyMoves,
                                  movePropabilities))
                    # // EnemyName, HealthMin, HealthMax, AttackType, StrMin, StrMax, MagMin, MagMax, AgiMin, AgiMax, DexMin, DexMax, EndMin, EndMax
            file.close()
            print("Loaded %d enemies." % totalNum)
        else:
            raise Exception("Failed to open Enemy Definition file!")
        return enemies

    def build_familias(self):
        print("Loading Familias!")
        familia_array = []
        familia_array.append(Familia('Hestia'))
        return familia_array

    def build_chars(self, moves, familias):
        print("Loading Characters!")
        characterArray = []
        file = open("../save/char_load_data/" + self.program_type + "/CharacterDefinitions.txt", "r")
        totalNum = 0
        if file.mode == 'r':
            count = 0
            for x in file:
                if x[0] != '/':
                    totalNum += 1
                    values = x[:-1].split(",", -1)
                    for index in range(0, len(values)):
                        values[index] = values[index].strip()
                    # 0 Type (A | S)
                    # 1 Attack Type (0, 1, 2)
                    # 2 Health Base
                    # 3 Mana Base
                    # 4 Strength Base
                    # 5 Magic Base
                    # 6 Endurance Base
                    # 7 Dexterity Base
                    # 8 Agility Base
                    # 9 Name
                    # 10 NickName
                    # 11 id
                    # if 0 A:
                    #   12 Move 1
                    #   13 Move 2
                    #   14 Move 3
                    #   15 Move 4
                    #   16 Move Special
                    rank = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                    res_path = '../res/characters/' + self.program_type + "/" + values[12] + "/" + values[12]
                    move = None
                    if values[0] == 'A':
                        move = Move.getmove(moves, values[13]), Move.getmove(moves, values[14]), Move.getmove(moves, values[15]), Move.getmove(moves, values[16]), Move.getmove(moves, values[17])
                    char = Character(rank, int(values[1]), int(values[2]), move, familias, index=count, _is_support=values[0] == 'S', name=values[10], display_name=values[11], id=values[12],
                                     slide_image_source=res_path + '_slide.png', slide_support_image_source=res_path + '_slide_support.png', preview_image_source=res_path + '_preview.png', full_image_source=res_path + '_full.png', program_type=self.program_type,
                                     health_base=int(values[3]),
                                     mana_base=int(values[4]),
                                     strength_base=int(values[5]),
                                     magic_base=int(values[6]),
                                     endurance_base=int(values[7]),
                                     dexterity_base=int(values[8]),
                                     agility_base=int(values[9]))
                    char.load_elements()
                    characterArray.append(char)
                    count += 1
            file.close()
            print("Loaded %d characters." % totalNum)
        else:
            raise Exception("Failed to open Character Definition file!")
        return characterArray

    def build_floors(self, enemies):
        print("Loading Floors")
        floors = []
        file = open("../save/floor_load_data/" + self.program_type + "/Floors.txt", "r")
        totalNum = 0
        if file.mode == 'r':
            for x in file:
                if x[0] != '/':
                    totalNum += 1
                    values = x[:-1].split(",", -1)
                    propabilities = []
                    floorEnemies = []
                    boss = None
                    for x in range(int(values[2])):
                        currStr = values[6 + (x * 2)]
                        temp = None
                        for y in enemies:
                            if y.name == currStr:
                                floorEnemies.append(y)
                                temp = y
                                break
                        if values[6 + (x * 2)] == "BOSS":
                            boss = temp
                        else:
                            propabilities.append(float(values[7 + (x * 2)]))
                    # // FloorNum, MaxEnemies, MinEncounters, MaxEncounters, BossType, ArrayNum, [EnemyName, EnemyProbability]
                    floors.append(Floor(int(values[0]), int(values[1]), int(values[2]), int(values[3]), int(values[4]),
                                        boss, floorEnemies, propabilities))
            file.close()
            print("Loaded %d floors." % totalNum)
        else:
            raise Exception("Failed to open Floor Definition file!")
        return floors

if __name__ == "__main__":
    game = GameApp()
    #The main game loop must be running before loading can take place, but running main loop will cancel game load id placed after
    Clock.schedule_once(game.load_game, 2.5)
    game.run()
