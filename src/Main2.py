from kivy.config import Config
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from src.entitites.Character.Character import Character, Move
Config.set('input', 'mouse', 'mouse, multitouch_on_demand')
from src.modules.Screens.NewGameScreen import NewGameScreen
from src.modules.Screens.SelectScreen import SelectScreen
from src.modules.Screens.TownScreen import TownScreen
from src.modules.Screens.Dungeon.DungeonMain import DungeonMain
from src.modules.Screens.TavernMain import TavernMain
from src.modules.Screens.CharacterSelector import CharacterSelector
from src.modules.Screens.Dungeon.Floor import Floor
from src.entitites.EnemyType import EnemyType

class Root(ScreenManager):

    def __init__(self, moves, enemies, floors, chars, **kwargs):
        super().__init__(**kwargs)
        self.list = []
        self.children = []

        self.characters = chars
        self.floors = floors
        self.enemies = enemies
        self.moves = moves
        self.parties = []
        self.parties.append(0)
        for x in range(10):
            self.parties.append([None, None, None, None, None, None, None, None,
                                 None, None, None, None, None, None, None, None])
        self.obtained_characters = []
        self.obtained_characters_a = []
        self.obtained_characters_s = []

        self.tavern_unlocked = True

        App.root = self
        self.create_screen('new_game')

    def display_screen(self, next_screen, direction, track):
        if direction == True:
            if isinstance(next_screen, Screen):
                old_screen = None
                if len(self.children) > 0:
                    old_screen = self.children[0]

                self.add_widget(next_screen)
                self.current = next_screen.name

                if old_screen is not None:
                    self.remove_widget(old_screen)
                    if track:
                        self.list.append(old_screen)
            else:
                raise Exception("Going forward only works with Screen Objects!")
        else:
            if self.list:
                old_screen = self.children[0]
                next_screen = self.list.pop()
                next_screen.reload()
                self.add_widget(next_screen)
                self.current = next_screen.name
                self.remove_widget(old_screen)
                return True
            print("No more screens to backtrack.")

    def create_screen(self, screen_name, *args):
        track = True
        if screen_name == 'select':
            screen = SelectScreen(self)
            track = False
        elif screen_name == 'new_game':
            screen = NewGameScreen(self)
            track = False
        elif screen_name == 'town':
            screen = TownScreen(self)
            track = False
        elif screen_name == 'dungeon_main':
            screen = DungeonMain(self, self.size)
            track = True
        elif screen_name == 'tavern_main':
            screen = TavernMain(self)
            screen.check_unlock()
            track = True
        elif screen_name == 'select_char':
            screen = CharacterSelector(self, args[0], args[1])
        else:
            raise Exception("Unsupported Screen type", screen_name)
        self.display_screen(screen, True, track)


    def display_attribute_screen(self, character):
        attr_screen = character.get_attr_screen()
        attr_screen.size = self.size
        #Remove from old parent
        if attr_screen.parent is not None:
            print(attr_screen.parent.children)


    # def select(self, screen):

    def on_size(self, *args):
        print("Fix Root Size")
        for child in self.children:
            child.size = self.size

    def on_pos(self, *args):
        print("Fix root pos")
        for child in self.children:
            child.pos = self.pos


class GameApp(App):
    title = 'Coatirane Adventures'

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.maxWidth = 4830
        self.maxHeight = 2160
        self.program_type = "test"

    def build(self):
        App.tavern_unlocked = False
        # Only works for windows machines!
        # user32 = ctypes.windll.user32
        # width = math.floor(user32.GetSystemMetrics(0) * 2 / 3)
        # height = math.floor(user32.GetSystemMetrics(1) * 2 / 3)

        width = 1920
        height = 1080
        if width > self.maxWidth:
            width = self.maxWidth
        if height > self.maxHeight:
            height = self.maxHeight
        self.background = Image(source="../res/screens/game_bounds.png", allow_stretch=True, keep_ratio=True, size=(width, height))
        App.width = width
        App.height = height
        self.old_size = (width, height)
        Window.size = (width, height)
        self.ratio = width, height
        self.no_trigger = False

        Window.bind(on_resize=self.on_resize)
        Window.minimum_width = 960
        Window.minimum_height = 540
        Window.left = 256
        Window.top = 256
        self.size = (width, height)
        # Window.left = math.floor((user32.GetSystemMetrics(0) - width) / 2)
        # Window.top = math.floor((user32.GetSystemMetrics(1) - height) / 2)
        Window.borderless = 0
        self.loading_screen = Image(source="../res/screens/splash.bmp", allow_stretch=True, keep_ratio=True, size=(width, height))
        self.background.add_widget(self.loading_screen)
        return self.background

    def load_game(self, dt):
        moves = self.build_moves()
        enemies = self.build_enemies(moves)
        chars = self.build_chars(moves)
        floors = self.build_floors(enemies)

        self.root = Root(moves, enemies, floors, chars)
        self.root.size = self.size

        self.background.remove_widget(self.loading_screen)
        self.background.add_widget(self.root)

    def on_resize(self, *args):
        Clock.unschedule(self.fix_size)
        Clock.schedule_once(self.fix_size, .25)

    def fix_size(self, *args):
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
                    print("Loaded: " + str(values))
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
                    print("Loaded: " + str(values))
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

    def build_chars(self, moves):
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
                    # print("Loaded: " + str(values))
                    # Type Name,Type Name,Id,Rank(0 - 10),Health,Defense PhysicalAttack MagicalAttack MagicalPoints Strength Magic Endurance Dexterity Agility BasicAtkPwr Atk Type
                    rank = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                    # for x in range(len(values)):
                    #     print("%d : %s" % (x, str(values[x]))
                    res_path = '../res/characters/' + self.program_type + "/" + values[1] + "/" + values[3] + "/" + values[3]
                    move = None
                    print(values)
                    if values[0] == 'A':
                        move = Move.getmove(moves, values[15]), Move.getmove(moves, values[16]), Move.getmove(moves, values[17]), Move.getmove(moves, values[18]), Move.getmove(moves, values[19])
                    char = Character(count, values[0] == 'S', values[1], values[2], values[3], rank, values[4],
                              int(values[5]), int(values[6]),
                              int(values[7]), int(values[8]), int(values[9]), int(values[10]), int(values[11]),
                              int(values[12]), int(values[13]), int(values[14]),
                              res_path + '_slide.png', res_path + '_preview.png',
                              res_path + '_full.png', move, self.program_type)
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
                    print("Loaded: " + str(values))
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
    Clock.schedule_once(game.load_game, 2)
    game.run()
