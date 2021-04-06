__all__ = ('CALoader',)

from kivy.resources import resource_find
from kivy.storage.jsonstore import JsonStore
from kivy.uix.widget import Widget
from kivy.properties import ListProperty
from kivy.clock import Clock
from kivy.event import EventDispatcher

from loading.char import load_char_chunk
from loading.config_loader import PROGRAM_TYPE
from loading.crafting_recipe import load_crafting_recipe_chunk
from loading.data import load_screen_chunk
from loading.enemy import load_enemy_chunk
from loading.equipment import load_equipment_chunk
from loading.family import load_family_chunk
from loading.housing import load_housing_chunk
from loading.floor import load_floor_chunk
from loading.material import load_material_chunk
from loading.move import load_move_chunk
from loading.perks import load_perk_chunk
from loading.save import load_save_chunk
from loading.shop import load_shop_item_chunk
from refs import Refs
from modules.builder import Builder

CURRENT_INDEX = 0
TRANSPARENT = 0
STARTING_TOTAL_INDEX = 1
STARTING_CURRENT_INDEX = 0

OPAQUE = 1

LOADING_LAYERS = [
    'skills',
    'abilities',
    'enemies',
    'families',
    'chars',
    'perks',
    'floors',
    'items',
    'drop_items',
    'equipment',
    'save',
    'housing',
    'materials',
    'recipes'
]
LOADING_SECTIONS = [
    'Skills and Abilities',
    'Materials',
    'Crafting Recipes',
    'Items',
    'Equipment Types',
    'Enemies',
    'Floors',
    'Housing Options',
    'Skill Trees',
    'Game Data',
    'Families',
    'Chars',
    'Game Data'
]
LOADING_FUNCTIONS = [
    load_move_chunk,
    load_material_chunk,
    load_crafting_recipe_chunk,
    load_shop_item_chunk,
    load_equipment_chunk,
    load_enemy_chunk,
    load_floor_chunk,
    load_housing_chunk,
    load_perk_chunk,
    load_save_chunk,
    load_family_chunk,
    load_char_chunk,
    load_screen_chunk
]
LOADING_FILES = [True for _ in range(9)] + [False] + [True for _ in range(2)] + [False]
LOADING_FILENAMES = [
    f"data/{PROGRAM_TYPE}/SA.txt",
    f"data/{PROGRAM_TYPE}/Materials.txt",
    f"data/{PROGRAM_TYPE}/CraftingRecipes.txt",
    f"data/{PROGRAM_TYPE}/items.txt",
    f"data/{PROGRAM_TYPE}/Equipment.txt",
    f"data/{PROGRAM_TYPE}/Enemies.txt",
    f"data/{PROGRAM_TYPE}/Floors.txt",
    f"data/{PROGRAM_TYPE}/Housing.txt",
    f"data/{PROGRAM_TYPE}/Perks.txt",
    f'',
    f"data/{PROGRAM_TYPE}/Families.txt",
    f"data/{PROGRAM_TYPE}/CharacterDefinitions.txt"
]

DELIMITERS = [
    '\n',     # Skills/Abilities
    '\n#\n',  # Materials
    '\n#\n',  # Crafting Recipes
    '\n\n',   # Shop Items
    '\n#\n',  # Equipment
    '#\n',    # Enemies
    '\n#\n',  # Floors
    '\n#\n',  # Housing
    '\n#\n',  # Perks
    '',       # Save Data
    '\n',     # Families
    '\n\n',   # Chars
]


class CALoader(Widget):
    max_values = ListProperty([])
    curr_values = ListProperty([])
    messages = ListProperty([])

    def __init__(self, program_type, **kwargs):
        Builder.load_file(resource_find('loading_screen.kv'))
        self.program_type = program_type
        self.layers = {key: {} for key in LOADING_LAYERS}
        super().__init__(**kwargs)

    def load_base_values(self):
        self.max_values.append(len(LOADING_SECTIONS))
        self.curr_values.append(STARTING_TOTAL_INDEX)
        for index in range(len(LOADING_SECTIONS)):
            self.messages.append(f'Loading {LOADING_SECTIONS[index]}')
            self.curr_values.append(STARTING_CURRENT_INDEX)
            self.max_values.append(1)
        self.ids.outer_progress.opacity = TRANSPARENT
        self.ids.inner_progress.opacity = TRANSPARENT
        self.ids.outer_progress.max = self.max_values[CURRENT_INDEX]
        self.ids.outer_progress.value = self.curr_values[CURRENT_INDEX]
        self.ids.inner_progress.max = self.max_values[self.curr_values[CURRENT_INDEX]]
        self.ids.inner_progress.value = self.curr_values[self.curr_values[CURRENT_INDEX]]

    def reset(self):
        self.curr_values = []
        self.layers = {key: {} for key in LOADING_LAYERS}
        self.messages = []
        self.max_values = []
        self.load_base_values()

    def show_bars(self):
        self.ids.outer_progress.opacity = OPAQUE
        self.ids.inner_progress.opacity = OPAQUE

    def update_outer(self):
        self.ids.outer_label.text = f'Loading Data {self.curr_values[CURRENT_INDEX]} / {self.max_values[CURRENT_INDEX]}'
        self.ids.outer_progress.max = self.max_values[CURRENT_INDEX]
        self.ids.outer_progress.value = self.curr_values[CURRENT_INDEX]
        self.update_inner()

    def update_inner(self):
        if self.curr_values[CURRENT_INDEX] <= self.max_values[CURRENT_INDEX]:
            self.ids.inner_label.text = f'{self.messages[self.curr_values[CURRENT_INDEX] - STARTING_TOTAL_INDEX]} {self.curr_values[self.curr_values[CURRENT_INDEX]]} / {self.max_values[self.curr_values[CURRENT_INDEX]]}'
            self.ids.inner_progress.max = self.max_values[self.curr_values[CURRENT_INDEX]]
            self.ids.inner_progress.value = self.curr_values[self.curr_values[CURRENT_INDEX]]

    def increase_total(self, *args):
        self.curr_values[CURRENT_INDEX] += 1
        self.update_outer()
        self.update_inner()

    def increase_current(self, *args):
        self.curr_values[self.curr_values[CURRENT_INDEX]] += 1
        self.update_inner()

    def done_loading(self, loader):
        Refs.log(f"{loader.triggers_finished} / {loader.triggers_total}")
        if loader.triggers_finished == loader.triggers_total:
            Refs.app.finished_loading()

    def load_ratios(self):
        return JsonStore(resource_find('src/uix/ratios.json'))

    def get(self, layer):
        return self.layers[layer]

    def append(self, layer, key, value):
        self.layers[layer][key] = value

    def set(self, layer, value):
        self.layers[layer] = value

    def load_game(self, save_slot):
        #Show 1 & 0 on the first screen
        self.show_bars()
        self.update_outer()
        self.update_inner()

        #Define a finished "Block"
        def finished_block(sub_loader, callbacks):
            if sub_loader.triggers_finished == sub_loader.triggers_total:
                for callback in callbacks:
                    if callback is not None:
                        callback()

        def load_block(trigger_index, callbacks):
            block_triggers = []

            block_loader = LOADING_FUNCTIONS[trigger_index]

            filename = None
            if trigger_index == 9:
                filename = f'{save_slot}'

            if LOADING_FILES[trigger_index]:
                filename = LOADING_FILENAMES[trigger_index]

                print(filename)

                with open(resource_find(filename), 'r', encoding='utf-8') as file:
                    chunks = file.read().split(DELIMITERS[self.curr_values[CURRENT_INDEX] - 1])
                self.max_values[self.curr_values[CURRENT_INDEX]] = len(chunks)

                for chunk in chunks:
                    block_triggers.append(Clock.create_trigger(lambda dt, c=chunk: block_loader(c, self, self.program_type, [self.increase_current, sub_loader.inc_triggers, lambda: sub_loader.start(), lambda: finished_block(sub_loader, callbacks)])))
            else:
                block_triggers.append(Clock.create_trigger(lambda dt: block_loader(self, self.program_type, filename, [self.increase_current, sub_loader.inc_triggers, lambda: sub_loader.start(), lambda: finished_block(sub_loader, callbacks)])))
            sub_loader = GameLoader(block_triggers)
            sub_loader.triggers_total = len(block_triggers)
            sub_loader.start()

        triggers = [Clock.create_trigger(lambda dt, xindex=index: load_block(xindex, [self.increase_total, loader.inc_triggers, lambda: loader.start(), lambda: self.done_loading(loader)])) for index in range(len(LOADING_SECTIONS))]
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
