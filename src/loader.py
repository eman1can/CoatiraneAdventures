from kivy.app import App
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.storage.jsonstore import JsonStore
from kivy.uix.widget import Widget
from kivy.properties import ListProperty
from kivy.clock import Clock
from kivy.event import EventDispatcher
import time

from src.RootManager import Root
from src.entitites.Character.Character import Move, Character
from src.entitites.Character.Familia import Familia
from src.entitites.EnemyType import EnemyType
from src.modules.Screens.Dungeon.Floor import Floor


class CALoader(Widget):
    max_values = ListProperty([])
    curr_values = ListProperty([])
    messages = ListProperty([])

    def __init__(self, program_type, **kwargs):
        Builder.load_file('../res/screens/loading_screen.kv')
        self.program_type = program_type
        super().__init__(**kwargs)

    def loadBaseValues(self):
        file = open("../save/loading_" + self.program_type + ".txt", "r")
        index = 0
        for x in file:
            if index == 0:
                opt = x[:-1].split(',')
                self.max_values.append(int(opt[0]))
                self.curr_values.append(1)
                for y in range(1, int(opt[0]) + 1):
                    self.messages.append(opt[y])
            else:
                if x.startswith('#'):
                    break
                self.max_values.append(int(x))
                self.curr_values.append(0)
            index += 1
        self.ids.outer_progress.opacity = 0
        self.ids.inner_progress.opacity = 0
        self.ids.outer_progress.max = self.max_values[0]
        self.ids.outer_progress.value = self.curr_values[0]
        self.ids.inner_progress.max = self.max_values[self.curr_values[0]]
        self.ids.inner_progress.value = self.curr_values[self.curr_values[0]]

    def show_bars(self):
        self.ids.outer_progress.opacity = 1
        self.ids.inner_progress.opacity = 1

    def updateOuter(self):
        self.ids.outer_label.text = f'Loading Data {self.curr_values[0]} / {self.max_values[0]}'
        self.ids.outer_progress.max = self.max_values[0]
        self.ids.outer_progress.value = self.curr_values[0]
        self.updateInner()

    def updateInner(self):
        if self.curr_values[0] <= self.max_values[0]:
            self.ids.inner_label.text = f'{self.messages[self.curr_values[0] - 1]} {self.curr_values[self.curr_values[0]]} / {self.max_values[self.curr_values[0]]}'
            self.ids.inner_progress.max = self.max_values[self.curr_values[0]]
            self.ids.inner_progress.value = self.curr_values[self.curr_values[0]]

    def incTot(self, *args):
        self.curr_values[0] += 1
        self.updateOuter()
        self.updateInner()

    def incCurr(self, *args):
        self.curr_values[self.curr_values[0]] += 1
        self.updateInner()

    def done_loading(self, loader):
        if loader.triggers_finished == loader.triggers_total:
            app = App.get_running_app()
            app.background.remove_widget(self)
            app.background.add_widget(self.main)
            print("Done loading!")
            self.initialized = True

    def load_game(self, dt):
        #Show 1 & 0 on the first screen
        self.show_bars()
        self.updateOuter()
        self.updateInner()

        #Define a finished "Block"
        def finished_block(subloader, callbacks):
            if subloader.triggers_finished == subloader.triggers_total:
                print("<< Loaded Block")
                for callback in callbacks:
                    if callback is not None:
                        callback()

        #Ratio functions
        def load_ratio_block(callbacks):
            print(">> Loading 1 ratio file")
            triggers = [Clock.create_trigger(lambda dt: load_ratio_chunk([self.incCurr, subloader.inc_triggers, lambda: subloader.start(), lambda: finished_block(subloader, callbacks)]))]
            subloader = GameLoader(triggers)
            subloader.triggers_total = len(triggers)
            subloader.start()

        def load_ratio_chunk(callbacks):
            print("\t>> Loading Ratio Chunk")
            self.ratios = JsonStore('ratios.json')
            print("\t<< Loaded Ratio Chunk ")
            for callback in callbacks:
                if callback is not None:
                    callback()

        # Move functions
        def load_move_block(callbacks):
            self.moves = []
            self.move_lines = []
            triggers = []

            file = open("../save/char_load_data/" + self.program_type + "/Moves.txt", "r")
            if file.mode == 'r':
                for x in file:
                    self.move_lines.append(x)
                file.close()
            else:
                raise Exception("Failed to open Move Definition file!")

            print(f">> Loading {len(self.move_lines)} moves")

            for x in range(len(self.move_lines)):
                triggers.append(Clock.create_trigger(lambda dt: load_move_chunk([self.incCurr, subloader.inc_triggers, lambda: subloader.start(), lambda: finished_block(subloader, callbacks)])))
            subloader = GameLoader(triggers)
            subloader.triggers_total = len(triggers)
            subloader.start()

        def load_move_chunk(callbacks):
            print("\t>> Loading Move Chunk")
            line = self.move_lines.pop(0)
            if line[0] != '/':
                values = line[:-1].split(",", -1)
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
                if bool(values[1] == "True"):
                    covername = values[2]
                # MoveName, MoveCover, CoverName, MoveType, MovePower, Stun, Charm, Poision, Burn, Sleep, Seal, Taunt
                self.moves.append(Move(values[0], bool(values[1] == "True"), covername, int(values[3]), values[4], effects))
            print("\t<< Loaded Move Chunk ")
            for callback in callbacks:
                if callback is not None:
                    callback()

        # Enemy functions
        def load_enemy_block(callbacks):
            self.enemies = []
            self.enemy_lines = []
            triggers = []

            file = open("../save/enemy_load_data/" + self.program_type + "/Enemies.txt", "r")
            if file.mode == 'r':
                for x in file:
                    self.enemy_lines.append(x)
                file.close()
            else:
                raise Exception("Failed to open Enemy Definition file!")

            print(f">> Loading {len(self.enemy_lines)} Enemies")

            for x in range(len(self.enemy_lines)):
                triggers.append(Clock.create_trigger(lambda dt: load_enemy_chunk([self.incCurr, subloader.inc_triggers, lambda: subloader.start(), lambda: finished_block(subloader, callbacks)])))

            subloader = GameLoader(triggers)
            subloader.triggers_total = len(triggers)
            subloader.start()

        def load_enemy_chunk(callbacks):
            print("\t>> Loading Enemy Chunk")
            line = self.enemy_lines.pop(0)
            if line[0] != '/':
                values = line[:-1].split(",", -1)
                EnemyMoves = []
                movePropabilities = []
                for x in range(int(values[14])):
                    EnemyMoves.append(Move.getmove(self.moves, values[15 + (2 * x)]))
                    movePropabilities.append(values[16 + (2 * x)])
                self.enemies.append(
                    EnemyType(values[0], int(values[3]), int(values[1]), int(values[2]), int(values[4]),
                              int(values[5]), int(values[6]), int(values[7]), int(values[8]), int(values[9]),
                              int(values[10]), int(values[11]), int(values[12]), int(values[13]), EnemyMoves,
                              movePropabilities))
                # // EnemyName, HealthMin, HealthMax, AttackType, StrMin, StrMax, MagMin, MagMax, AgiMin, AgiMax, DexMin, DexMax, EndMin, EndMax
            print("\t<< Loaded Enemy Chunk ")
            for callback in callbacks:
                if callback is not None:
                    callback()

        # Family functions
        def load_family_block(callbacks):
            self.familias = []
            self.familia_lines = []
            triggers = []

            file = open("../save/familia_load_data/" + self.program_type + "/Familias.txt", "r")
            if file.mode == 'r':
                for x in file:
                    self.familia_lines.append(x)
            file.close()
            print(f">> Loading {len(self.familia_lines)} Familias!")

            for x in range(len(self.familia_lines)):
                triggers.append(Clock.create_trigger(lambda dt: load_family_chunk([self.incCurr, subloader.inc_triggers, lambda: subloader.start(), lambda: finished_block(subloader, callbacks)])))

            subloader = GameLoader(triggers)
            subloader.triggers_total = len(triggers)
            subloader.start()

        def load_family_chunk(callbacks):
            print("\t>> Loading Family Chunk")
            line = self.familia_lines.pop(0)
            self.familias.append(Familia(line[:-1]))
            print("\t<< Loaded Family Chunk ")
            for callback in callbacks:
                if callback is not None:
                    callback()

        #Char block functions
        def load_char_block(callbacks):
            self.chars = []
            self.char_lines = []
            self.char_count = 0
            triggers = []

            file = open("../save/char_load_data/" + self.program_type + "/CharacterDefinitions.txt", "r")
            if file.mode == 'r':
                for x in file:
                    self.char_lines.append(x)
            file.close()
            print(f">> Loading {len(self.char_lines)} Characters!")

            for x in range(len(self.char_lines)):
                triggers.append(Clock.create_trigger(lambda dt: load_char_chunk([self.incCurr, subloader.inc_triggers, lambda: subloader.start(), lambda: finished_block(subloader, callbacks)])))

            subloader = GameLoader(triggers)
            subloader.triggers_total = len(triggers)
            subloader.start()

        def load_char_chunk(callbacks):
            print("\t>> Loading Char Chunk")
            line = self.char_lines.pop(0)
            if line[0] != '/':
                values = line[:-1].split(",", -1)
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
                    move = Move.getmove(self.moves, values[13]), Move.getmove(self.moves, values[14]), Move.getmove(self.moves, values[15]), Move.getmove(self.moves, values[16]), Move.getmove(self.moves, values[17])
                char = Character(rank, int(values[1]), int(values[2]), move, self.familias, index=self.char_count, _is_support=values[0] == 'S', name=values[10], display_name=values[11], id=values[12],
                                 slide_image_source=res_path + '_slide.png', slide_support_image_source=res_path + '_slide_support.png', preview_image_source=res_path + '_preview.png', full_image_source=res_path + '_full.png', program_type=self.program_type,
                                 health_base=int(values[3]),
                                 mana_base=int(values[4]),
                                 strength_base=int(values[5]),
                                 magic_base=int(values[6]),
                                 endurance_base=int(values[7]),
                                 dexterity_base=int(values[8]),
                                 agility_base=int(values[9]))
                char.load_elements(self.size)
                self.chars.append(char)
                self.char_count += 1
            print("\t<< Loaded Char Chunk ")
            for callback in callbacks:
                if callback is not None:
                    callback()

        # Floor functions
        def load_floor_block(callbacks):
            self.floors = []
            self.floor_lines = []
            triggers = []

            file = open("../save/floor_load_data/" + self.program_type + "/Floors.txt", "r")
            if file.mode == 'r':
                for x in file:
                    self.floor_lines.append(x)
                file.close()
            else:
                raise Exception("Failed to open Floor Definition file!")

            print(f">> Loading {len(self.floor_lines)} Floors!")

            for x in range(len(self.floor_lines)):
                triggers.append(Clock.create_trigger(lambda dt: load_floor_chunk([self.incCurr, subloader.inc_triggers, lambda: subloader.start(), lambda: finished_block(subloader, callbacks)])))

            subloader = GameLoader(triggers)
            subloader.triggers_total = len(triggers)
            subloader.start()

        def load_floor_chunk(callbacks):
            print("\tLoading floor Chunk")
            line = self.floor_lines.pop(0)
            if line[0] != '/':
                values = line[:-1].split(",", -1)
                propabilities = []
                floorEnemies = []
                boss = None
                for x in range(int(values[2])):
                    currStr = values[6 + (x * 2)]
                    temp = None
                    for y in self.enemies:
                        if y.name == currStr:
                            floorEnemies.append(y)
                            temp = y
                            break
                    if values[6 + (x * 2)] == "BOSS":
                        boss = temp
                    else:
                        propabilities.append(float(values[7 + (x * 2)]))
                # // FloorNum, MaxEnemies, MinEncounters, MaxEncounters, BossType, ArrayNum, [EnemyName, EnemyProbability]
                self.floors.append(Floor(int(values[0]), int(values[1]), int(values[2]), int(values[3]), int(values[4]),
                                    boss, floorEnemies, propabilities))
            print("\t<< Loaded floor Chunk ")
            for callback in callbacks:
                if callback is not None:
                    callback()

        # Screens functions
        def load_screen_block(callbacks):
            print("Loading 1 screens")

            triggers = [Clock.create_trigger(lambda dt: load_screen_chunk([self.incCurr, subloader.inc_triggers, lambda: subloader.start(), lambda: finished_block(subloader, callbacks)]))
                        ]

            subloader = GameLoader(triggers)
            subloader.triggers_total = len(triggers)
            subloader.start()

        def load_screen_chunk(callbacks):
            print("\tLoading Screen Chunk")
            self.main = Root(self.moves, self.enemies, self.floors, self.familias, self.chars)
            App.get_running_app().main = self.main
            self.main.make_screens()
            self.main.size = self.size
            print("\t<< Loaded Screen Chunk ")
            for callback in callbacks:
                if callback is not None:
                    callback()

        triggers = [
            Clock.create_trigger(lambda dt: load_ratio_block([self.incTot, loader.inc_triggers, lambda: loader.start(), lambda: self.done_loading(loader)])),
            Clock.create_trigger(lambda dt: load_move_block([self.incTot, loader.inc_triggers, lambda: loader.start(), lambda: self.done_loading(loader)])),
            Clock.create_trigger(lambda dt: load_enemy_block([self.incTot, loader.inc_triggers, lambda: loader.start(), lambda: self.done_loading(loader)])),
            Clock.create_trigger(lambda dt: load_family_block([self.incTot, loader.inc_triggers, lambda: loader.start(), lambda: self.done_loading(loader)])),
            Clock.create_trigger(lambda dt: load_char_block([self.incTot, loader.inc_triggers, lambda: loader.start(), lambda: self.done_loading(loader)])),
            Clock.create_trigger(lambda dt: load_floor_block([self.incTot, loader.inc_triggers, lambda: loader.start(), lambda: self.done_loading(loader)])),
            Clock.create_trigger(lambda dt: load_screen_block([self.incTot, loader.inc_triggers, lambda: loader.start(), lambda: self.done_loading(loader)]))
        ]
        loader = GameLoader(triggers)
        loader.triggers_total = len(triggers)
        loader.start()


class GameLoader(EventDispatcher):
    def __init__(self, triggers, **kwargs):
        self.triggers = triggers
        self.triggers_finished = 0
        self.triggers_total = 0
        super().__init__(**kwargs)

    def inc_triggers(self):
        self.triggers_finished += 1

    def start(self):
        if len(self.triggers) > 0:
            trigger = self.triggers.pop(0)
            # print("Executing trigger: ", trigger)
            trigger()