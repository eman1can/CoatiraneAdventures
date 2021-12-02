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
from loading.market import load_market_price_chunk
from loading.material import load_material_chunk
from loading.move import load_skill_chunk
from loading.perks import load_perk_chunk
from loading.save import load_save_chunk
from loading.item import load_item_chunk
from refs import Refs
from modules.builder import Builder

COMMENT_CHARACTER = '#'
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
    'market_prices',
    'equipment',
    'save',
    'housing',
    'materials',
    'recipes'
]

LOADING_DEFINITIONS = [
    # Load Order, Display Title, Has File, Filename, Delimiter, Loading Function
    [0,  'Skills and Abilities', True , 'SA.txt'                  , '\n'   , load_skill_chunk          ],
    [1,  'Enemies'             , True , 'Enemies.txt'             , '#\n'  , load_enemy_chunk          ],
    [2,  'Materials'           , True , 'Materials.txt'           , '\n#\n', load_material_chunk       ],
    [3,  'Floors'              , True , 'Floors.txt'              , '\n#\n', load_floor_chunk          ],
    [4,  'Items'               , True , 'items.txt'               , '\n\n' , load_item_chunk           ],
    [5,  'Crafting Recipes'    , True , 'CraftingRecipes.txt'     , '\n#\n', load_crafting_recipe_chunk],
    [6,  'Market Prices'       , True , 'market_prices.txt'       , '\n'   , load_market_price_chunk   ],
    [7,  'Equipment Types'     , True , 'Equipment.txt'           , '\n#\n', load_equipment_chunk      ],
    [8,  'Housing Options'     , True , 'Housing.txt'             , '\n#\n', load_housing_chunk        ],
    [9,  'Skill Trees'         , True , 'Perks.txt'               , '\n#\n', load_perk_chunk           ],
    [10, 'Save Data'           , False, ''                        , ''     , load_save_chunk           ],
    [11, 'Families'            , True , 'Families.txt'            , '\n'   , load_family_chunk         ],
    [12, 'Chars'               , True , 'CharacterDefinitions.txt', '\n\n' , load_char_chunk           ],
    [13, 'Game Data'           , False, ''                        , ''     , load_screen_chunk         ],
]

LOADING_SECTIONS   = [None for _ in range(len(LOADING_DEFINITIONS))]
LOADING_FUNCTIONS  = [None for _ in range(len(LOADING_DEFINITIONS))]
LOADING_FILES      = [None for _ in range(len(LOADING_DEFINITIONS))]
LOADING_FILENAMES  = [None for _ in range(len(LOADING_DEFINITIONS))] # [f"data/{PROGRAM_TYPE}/{x}" for x in LOADING_DEFINITIONS]
LOADING_DELIMITERS = [None for _ in range(len(LOADING_DEFINITIONS))]

for (load_order, display_title, has_file, filename, delimiter, loading_function) in LOADING_DEFINITIONS:
    LOADING_SECTIONS[load_order]   = display_title
    LOADING_FILES[load_order]      = has_file
    LOADING_FILENAMES[load_order]  = f'data/{PROGRAM_TYPE}/{filename}'
    LOADING_DELIMITERS[load_order] = delimiter
    LOADING_FUNCTIONS[load_order]  = loading_function

SAVE_INDEX = LOADING_SECTIONS.index('Save Data')


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
        Refs.log(f"{loader.triggers_finished} / {loader.triggers_total} - {LOADING_SECTIONS[loader.triggers_finished - 1]}")
        if loader.triggers_finished == loader.triggers_total:
            Refs.app.finished_loading()

    def load_ratios(self):
        return JsonStore(resource_find('src/uix/ratios.json'))

    def get(self, layer):
        return self.layers[layer]

    def append(self, layer, key, value, debug=False):
        if debug:
            Refs.log(f'Loader Add {key} - {value}')
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
            if trigger_index == SAVE_INDEX:
                filename = f'{save_slot}'

            if LOADING_FILES[trigger_index]:
                filename = LOADING_FILENAMES[trigger_index]

                filepath = resource_find(filename)
                if filepath is None:
                    raise Exception(f"Cannot find file: {filename}")

                with open(filepath, 'r', encoding='utf-8') as file:
                    chunks = file.read().split(LOADING_DELIMITERS[self.curr_values[CURRENT_INDEX] - 1])
                self.max_values[self.curr_values[CURRENT_INDEX]] = len(chunks)

                for chunk in chunks:
                    if chunk.startswith(COMMENT_CHARACTER):
                        continue
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
