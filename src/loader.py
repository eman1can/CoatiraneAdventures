from kivy.app import App
from kivy.lang.builder import Builder
from kivy.storage.jsonstore import JsonStore
from kivy.uix.widget import Widget
from kivy.properties import ListProperty
from kivy.clock import Clock
from kivy.event import EventDispatcher

from src.RootManager import Root
from src.entitites.Character.Character import Move, Character
from src.entitites.Character.Familia import Familia
from src.entitites.EnemyType import EnemyType
from src.modules.KivyBase.Hoverable import HoverBehaviour
from src.modules.Screens.Dungeon.Floor import Floor

CURRENT_INDEX = 0
TRANSPARENT = 0
STARTING_TOTAL_INDEX = 1
STARTING_CURRENT_INDEX = 0

OPAQUE = 1


class CALoader(HoverBehaviour, Widget):
    max_values = ListProperty([])
    curr_values = ListProperty([])
    messages = ListProperty([])

    def __init__(self, program_type, **kwargs):
        Builder.load_file('../res/screens/loading_screen.kv')
        self.program_type = program_type
        self.moves = []
        self.enemies = []
        self.familias = []
        self.chars = []
        self.char_count = 0
        self.floors = []
        self.initialized = False
        super().__init__(**kwargs)

    def loadBaseValues(self):
        file = open("../save/loading_" + self.program_type + ".txt", "r")
        index = 0
        for x in file:
            if index == 0:
                opt = x[:-1].split(',')
                self.max_values.append(int(opt[CURRENT_INDEX]))
                self.curr_values.append(STARTING_TOTAL_INDEX)
                for y in range(STARTING_TOTAL_INDEX, int(opt[CURRENT_INDEX]) + STARTING_TOTAL_INDEX):
                    self.messages.append(opt[y])
            else:
                if x.startswith('#'):
                    break
                self.max_values.append(int(x))
                self.curr_values.append(STARTING_CURRENT_INDEX)
            index += 1
        self.ids.outer_progress.opacity = TRANSPARENT
        self.ids.inner_progress.opacity = TRANSPARENT
        self.ids.outer_progress.max = self.max_values[CURRENT_INDEX]
        self.ids.outer_progress.value = self.curr_values[CURRENT_INDEX]
        self.ids.inner_progress.max = self.max_values[self.curr_values[CURRENT_INDEX]]
        self.ids.inner_progress.value = self.curr_values[self.curr_values[CURRENT_INDEX]]

    def show_bars(self):
        self.ids.outer_progress.opacity = OPAQUE
        self.ids.inner_progress.opacity = OPAQUE

    def updateOuter(self):
        self.ids.outer_label.text = f'Loading Data {self.curr_values[CURRENT_INDEX]} / {self.max_values[CURRENT_INDEX]}'
        self.ids.outer_progress.max = self.max_values[CURRENT_INDEX]
        self.ids.outer_progress.value = self.curr_values[CURRENT_INDEX]
        self.updateInner()

    def updateInner(self):
        if self.curr_values[CURRENT_INDEX] <= self.max_values[CURRENT_INDEX]:
            self.ids.inner_label.text = f'{self.messages[self.curr_values[CURRENT_INDEX] - STARTING_TOTAL_INDEX]} {self.curr_values[self.curr_values[CURRENT_INDEX]]} / {self.max_values[self.curr_values[CURRENT_INDEX]]}'
            self.ids.inner_progress.max = self.max_values[self.curr_values[CURRENT_INDEX]]
            self.ids.inner_progress.value = self.curr_values[self.curr_values[CURRENT_INDEX]]

    def incTot(self, *args):
        self.curr_values[CURRENT_INDEX] += 1
        self.updateOuter()
        self.updateInner()

    def incCurr(self, *args):
        self.curr_values[self.curr_values[CURRENT_INDEX]] += 1
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
                for callback in callbacks:
                    if callback is not None:
                        callback()

        def load_block(loader, isfile, filename, callbacks):
            triggers = []
            if isfile:
                self.lines = []
                file = open(filename, "r")
                if file.mode == 'r':
                    for x in file:
                        if x != '':
                            self.lines.append(x)
                    file.close()
                else:
                    raise Exception(f"Failed to open {filename}!")

                if len(self.lines) != self.max_values[self.curr_values[CURRENT_INDEX]]:
                    raise Exception("Wrong initalization numbers!")

                for x in range(len(self.lines)):
                    triggers.append(Clock.create_trigger(lambda dt: loader([self.incCurr, subloader.inc_triggers, lambda: subloader.start(), lambda: finished_block(subloader, callbacks)])))
            else:
                triggers.append(Clock.create_trigger(lambda dt: loader([self.incCurr, subloader.inc_triggers, lambda: subloader.start(), lambda: finished_block(subloader, callbacks)])))
            subloader = GameLoader(triggers)
            subloader.triggers_total = len(triggers)
            subloader.start()

        def load_ratio_chunk(callbacks):
            self.ratios = JsonStore('ratios.json')
            for callback in callbacks:
                if callback is not None:
                    callback()

        # Move functions
        MOVE_NAME = 0
        MOVE_COVER = 1
        MOVE_COVER_NAME = 2
        MOVE_TYPE = 3
        MOVE_POWER = 4
        EFFECT_NUMBER = 5
        NUM_NORMAL_VALUES = 5
        EFFECT_VALUES = 2
        EFFECT_NAME = 0
        EFFECT_PROBABLITY = 1

        def load_move_chunk(callbacks):
            line = self.lines.pop(0)
            if line[0] != '/':
                values = line[:-1].split(",", -1)
                # moveName, MoveCover, MoveCoverName, MoveType, MovePower, EffectNum, MoveEffects
                effects = []
                effects.append(["Stun", 0])
                effects.append(["Sleep", 0])
                effects.append(["Poison", 0])
                effects.append(["Burn", 0])
                effects.append(["Charm", 0])
                effects.append(["Seal", 0])
                effects.append(["Taunt", 0])
                for x in range(int(values[EFFECT_NUMBER])):
                    for y in effects:
                        if values[NUM_NORMAL_VALUES + (x * EFFECT_VALUES)] == y[EFFECT_NAME]:
                            y[EFFECT_PROBABLITY] = float(values[NUM_NORMAL_VALUES + 1 + (x * EFFECT_VALUES)])
                covername = None
                if bool(values[MOVE_COVER] == "True"):
                    covername = values[MOVE_COVER_NAME]
                # MoveName, MoveCover, CoverName, MoveType, MovePower, Stun, Charm, Poision, Burn, Sleep, Seal, Taunt
                self.moves.append(Move(values[MOVE_NAME], bool(values[MOVE_COVER] == "True"), covername, int(values[MOVE_TYPE]), values[MOVE_POWER], effects))
            for callback in callbacks:
                if callback is not None:
                    callback()

        def load_enemy_chunk(callbacks):
            line = self.lines.pop(0)
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
            for callback in callbacks:
                if callback is not None:
                    callback()

        def load_family_chunk(callbacks):
            line = self.lines.pop(0)
            self.familias.append(Familia(line[:-1]))
            for callback in callbacks:
                if callback is not None:
                    callback()

        #Char block functions
        ATTACK_TYPE = 0
        TYPE = 1
        ELEMENT = 2
        HEALTH_BASE = 3
        MANA_BASE = 4
        STRENGTH_BASE = 5
        MAGIC_BASE = 6
        ENDURANCE_BASE = 7
        DEXTERITY_BASE = 8
        AGILITY_BASE = 9
        NAME = 10
        NICK_NAME = 11
        ID = 12
        MOVE_1 = 13
        MOVE_2 = 14
        MOVE_3 = 15
        MOVE_4 = 16
        MOVE_SPECIAL = 17
        UNLOCKED = 1
        LOCKED = 0

        def load_char_chunk(callbacks):
            line = self.lines.pop(0)
            if line[0] != '/':
                values = line[:-1].split(",", -1)
                for index in range(len(values)):
                    values[index] = values[index].strip()

                ranks = [UNLOCKED, LOCKED, LOCKED, LOCKED, LOCKED, LOCKED, LOCKED, LOCKED, LOCKED, LOCKED]
                res_path = '../res/characters/' + self.program_type + "/" + values[ID] + "/" + values[ID]
                move = None
                if values[ATTACK_TYPE] == 'A':
                    move = Move.getmove(self.moves, values[MOVE_1]), Move.getmove(self.moves, values[MOVE_2]), Move.getmove(self.moves, values[MOVE_3]), Move.getmove(self.moves, values[MOVE_4]), Move.getmove(self.moves, values[MOVE_SPECIAL])
                char = Character(ranks, int(values[TYPE]), int(values[ELEMENT]), move, self.familias, index=self.char_count, _is_support=values[ATTACK_TYPE] == 'S', name=values[NAME], display_name=values[NICK_NAME], id=values[ID],
                                 slide_image_source=res_path + '_slide.png', slide_support_image_source=res_path + '_slide_support.png', preview_image_source=res_path + '_preview.png', full_image_source=res_path + '_full.png', program_type=self.program_type,
                                 health_base=int(values[HEALTH_BASE]),
                                 mana_base=int(values[MANA_BASE]),
                                 strength_base=int(values[STRENGTH_BASE]),
                                 magic_base=int(values[MAGIC_BASE]),
                                 endurance_base=int(values[ENDURANCE_BASE]),
                                 dexterity_base=int(values[DEXTERITY_BASE]),
                                 agility_base=int(values[AGILITY_BASE]))
                self.chars.append(char)
                self.char_count += 1
            for callback in callbacks:
                if callback is not None:
                    callback()

        # Floor functions
        FLOOR_ID = 0
        MIN_ENCOUNTERS = 1
        MAX_ENCOUNTERS = 2
        BOSS_TYPE = 3
        ARRAY_NUM = 4
        END_OF_VALUES = 6
        NUMBER_OF_VALUES = 2

        def load_floor_chunk(callbacks):
            line = self.lines.pop(0)
            if line[0] != '/':
                values = line[:-1].split(",", -1)
                propabilities = []
                floorEnemies = []
                boss = None
                for x in range(int(values[NUMBER_OF_VALUES])):
                    currStr = values[END_OF_VALUES + (x * NUMBER_OF_VALUES)]
                    temp = None
                    for y in self.enemies:
                        if y.name == currStr:
                            floorEnemies.append(y)
                            temp = y
                            break
                    if values[END_OF_VALUES + (x * NUMBER_OF_VALUES)] == "BOSS":
                        boss = temp
                    else:
                        propabilities.append(float(values[END_OF_VALUES + 1 + (x * NUMBER_OF_VALUES)]))
                # // FloorID, MaxEnemies, MinEncounters, MaxEncounters, BossType, ArrayNum, [EnemyName, EnemyProbability]
                self.floors.append(Floor(values[FLOOR_ID], int(values[MIN_ENCOUNTERS]), int(values[MAX_ENCOUNTERS]), int(values[BOSS_TYPE]), int(values[ARRAY_NUM]),
                                    boss, floorEnemies, propabilities))
            for callback in callbacks:
                if callback is not None:
                    callback()

        def load_screen_chunk(callbacks):
            self.main = Root(self.moves, self.enemies, self.floors, self.familias, self.chars)
            App.get_running_app().main = self.main
            self.main.make_screens()
            self.main.size = self.size
            App.get_running_app().initialized = True
            for callback in callbacks:
                if callback is not None:
                    callback()

        triggers = [
            Clock.create_trigger(lambda dt: load_block(load_ratio_chunk, False, "", [self.incTot, loader.inc_triggers, lambda: loader.start(), lambda: self.done_loading(loader)])),
            Clock.create_trigger(lambda dt: load_block(load_move_chunk, True, f"../save/char_load_data/{self.program_type}/Moves.txt", [self.incTot, loader.inc_triggers, lambda: loader.start(), lambda: self.done_loading(loader)])),
            Clock.create_trigger(lambda dt: load_block(load_enemy_chunk, True, f"../save/enemy_load_data/{self.program_type}/Enemies.txt", [self.incTot, loader.inc_triggers, lambda: loader.start(), lambda: self.done_loading(loader)])),
            Clock.create_trigger(lambda dt: load_block(load_family_chunk, True, f"../save/familia_load_data/{self.program_type}/Familias.txt", [self.incTot, loader.inc_triggers, lambda: loader.start(), lambda: self.done_loading(loader)])),
            Clock.create_trigger(lambda dt: load_block(load_char_chunk, True, f"../save/char_load_data/{self.program_type}/CharacterDefinitions.txt", [self.incTot, loader.inc_triggers, lambda: loader.start(), lambda: self.done_loading(loader)])),
            Clock.create_trigger(lambda dt: load_block(load_floor_chunk, True, f"../save/floor_load_data/{self.program_type}/Floors.txt", [self.incTot, loader.inc_triggers, lambda: loader.start(), lambda: self.done_loading(loader)])),
            Clock.create_trigger(lambda dt: load_block(load_screen_chunk, False, "", [self.incTot, loader.inc_triggers, lambda: loader.start(), lambda: self.done_loading(loader)]))
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
            trigger()
