# Crafting Type
from refs import Refs

ITEM                        = 0
PROCESS_SOFT_MATERIAL       = 1
PROCESS_HARD_MATERIAL       = 2
CRAFT_SOFT_ALLOY            = 3
CRAFT_HARD_ALLOY            = 4
CRAFT_SOFT_EQUIPMENT        = 5
CRAFT_HARD_EQUIPMENT        = 6
CRAFT_MASK                  = 127
CRAFTING_TYPES = [ITEM, PROCESS_SOFT_MATERIAL, PROCESS_HARD_MATERIAL, CRAFT_SOFT_ALLOY, CRAFT_HARD_ALLOY, CRAFT_SOFT_EQUIPMENT, CRAFT_HARD_EQUIPMENT]
CRAFTING_TYPE_STRINGS = ['Item', 'Process Soft Material', 'Process Hard Material', 'Craft Soft Alloy', 'Craft Hard Alloy', 'Craft Soft Equipment', 'Craft Hard Equipment']

ITEM_LEVEL                  = 7
PROCESS_SOFT_MATERIAL_LEVEL = 9
PROCESS_HARD_MATERIAL_LEVEL = 11
CRAFT_SOFT_ALLOY_LEVEL      = 13
CRAFT_HARD_ALLOY_LEVEL      = 15
CRAFT_SOFT_EQUIPMENT_LEVEL  = 17
CRAFT_HARD_EQUIPMENT_LEVEL  = 19
CRAFTING_LEVELS = [ITEM_LEVEL, PROCESS_SOFT_MATERIAL_LEVEL, PROCESS_HARD_MATERIAL_LEVEL, CRAFT_SOFT_ALLOY_LEVEL, CRAFT_HARD_ALLOY_LEVEL, CRAFT_SOFT_EQUIPMENT_LEVEL, CRAFT_HARD_EQUIPMENT_LEVEL]

LEVEL_1               = 0
LEVEL_2               = 1
LEVEL_3               = 2
LEVEL_4               = 3
LEVEL_MASK            = 255 << ITEM_LEVEL
LEVEL_SHIFTED_MASK    = 3
LEVEL_STRINGS = ['Level 1', 'Level 2', 'Level 3', 'Level 4']

QUEUE_TIME_MAX = 1000
WORKING_SLOT_COUNT = 3
DISPLAY_COUNT = 5
MULTIPLIERS = [1]
for index in range(1, WORKING_SLOT_COUNT):
    MULTIPLIERS.append(MULTIPLIERS[-1] / 2)
del index


class CraftingChar:
    def __init__(self, name, char_index, crafting_type, image_source):
        self.name = name
        self.char_index = char_index
        self.crafting_type = crafting_type
        self.image_source = image_source

    def can_craft(self, craft_type):
        return craft_type & self.crafting_type > 0

    def get_multiplier(self, crafting_type):
        craft_mask = self.crafting_type & crafting_type & CRAFT_MASK
        if craft_mask == 0:
            return 0
        craft_type = len(bin(craft_mask)[2:]) - 1
        craft_level = (self.crafting_type >> CRAFTING_LEVELS[craft_type]) & LEVEL_SHIFTED_MASK
        level = (crafting_type >> CRAFTING_LEVELS[craft_type]) & LEVEL_SHIFTED_MASK

        if craft_level == level:
            return 1
        if craft_level - level == 1:
            return 1.5
        return 2


class CraftingItem:
    def __init__(self, output_id, crafting_type, crafting_time):
        self.output_id = output_id
        self.crafting_type = crafting_type
        self._time = crafting_time
        self._current_time = crafting_time

        self.multipliers = [0 for _ in range(WORKING_SLOT_COUNT)]
        self.chars = [None for _ in range(WORKING_SLOT_COUNT)]
        self.char_indexes = [-1 for _ in range(WORKING_SLOT_COUNT)]

        self.tested_chars = []
        self.display = None
        self._image_source = None

    def __str__(self):
        string = f'<{self.output_id} '
        if self.chars is None:
            return string + ' - No chars >'
        for crafting_char in self.chars:
            if crafting_char is None:
                continue
            string += f'{crafting_char.output_id} '
        return string + '>'

    def set_image_source(self, image_source):
        self._image_source = image_source

    def set_display(self, display):
        self.display = display
        self.display.time = self._time
        self.display.current_time = self._current_time
        self.display.image_source = self._image_source
        for index, crafting_char in enumerate(self.chars):
            if crafting_char is None:
                continue
            self.display.images[index].source = crafting_char.image_source

    def remove_display(self):
        display = self.display
        self.display = None
        for index in range(WORKING_SLOT_COUNT):
            display.images[index].source = ''
        return display

    def save(self):
        save_data = {
            'crafting_type': self.crafting_type,
            'time': self._time,
            'primary': self.primary,
            'primary_char_index': self.primary_char_index,
            'secondary': self.secondary,
            'secondary_char_index': self.secondary_char_index,
            'tested_chars': self.tested_chars
        }
        return save_data

    def load(self, save_data):
        self.crafting_type = save_data['crafting_type']
        self._time = save_data['time']
        self.primary = save_data['primary']
        self.primary_char_index = save_data['primary_char_index']
        self.secondary = save_data['secondary']
        self.secondary_char_index = save_data['secondary_char_index']
        self.tested_chars = save_data['tested_chars']

    def assign_char(self, crafting_char, mult, index):
        self.multipliers[index] = mult
        self.chars[index] = crafting_char
        self.char_indexes[index] = crafting_char.char_index
        if self.display is not None:
            self.display.images[index].source = crafting_char.image_source

    def advance(self, delta):
        for index in range(WORKING_SLOT_COUNT):
            if self.multipliers[index] == 0:
                continue
            self._current_time -= delta * self.multipliers[index] * MULTIPLIERS[index]
        if self.display is not None:
            self.display.current_time = self._current_time
        return self._current_time < 0

    def get_time(self):
        return self._current_time

    def get_raw_time(self):
        return self._time


class CraftingQueue:
    def __init__(self):
        self._chars = {}
        self._unassigned_chars = []
        self._queue = []
        self._queue_time = 0
        self._queue_count = 0
        self._inventory = None

        self._display = None
        self._item_display = None
        self._unused_item_displays = None
        self._used_item_displays = None
        self._hidden = []
        self._displayed = []

    def set_inventory(self, inventory):
        self._inventory = inventory

    def save(self):
        save_data = {'unassigned_chars': self._unassigned_chars, 'queue': []}
        for crafting_item in self._queue:
            save_data['queue'].append(crafting_item.save())
        return save_data

    def load(self, save_data):
        self._unassigned_chars = save_data['unassigned_chars']
        self._queue = []
        for crafting_item_save_data in save_data['queue']:
            crafting_item = CraftingItem('', 0, 1)
            crafting_item.load(crafting_item_save_data)
            self._queue.append(crafting_item)

    def set_display(self, stack_layout, display_list):
        self._display = stack_layout
        self._item_display = stack_layout.ids.box_layout
        self._unused_item_displays = display_list
        self._used_item_displays = []
        print(self._displayed, self._hidden)

        for crafting_item in self._displayed:
            self.assign_item_display(crafting_item)

    def assign_item_display(self, crafting_item):
        display = self._unused_item_displays.pop()
        crafting_item.set_display(display)
        self._item_display.add_widget(display)
        self._used_item_displays.append(display)

    def remove_display(self):
        self._item_display.clear_widgets()
        self._item_display = None
        self._display = None
        for crafting_item in self._displayed:
            crafting_item.remove_display()
        self._used_item_displays = None
        self._unused_item_displays = None

    def unassign_item_display(self, crafting_item):
        display = crafting_item.remove_display()
        self._used_item_displays.remove(display)
        self._unused_item_displays.append(display)

    def init_char(self, name, char):
        crafting_type = self.perks_to_crafting_type(char.get_all_perks())
        print(name, end=' ')
        self.print_crafting_type(crafting_type)
        char_index = char.get_index()
        self._chars[char_index] = CraftingChar(name, char_index, crafting_type, char.get_image('preview'))
        if char_index not in self._unassigned_chars:
            self._unassigned_chars.append(char_index)
        # self.unassign_char(char_index)
        print(self._unassigned_chars)

    def add_char(self, char_index, crafting_char):
        self._chars[char_index] = crafting_char
        self.unassign_char(char_index)

    def add_perk_to_char(self, perk_id, char_index):
        crafting_type = self._chars[char_index].crafting_type
        crafting_type = self.apply_perk_to_crafting_type(crafting_type, perk_id)
        self._chars[char_index].crafting_type = crafting_type

    def perks_to_crafting_type(self, perks):
        crafting_type = 0
        for perk_id in perks:
            crafting_type = self.apply_perk_to_crafting_type(crafting_type, perk_id)
        return crafting_type

    def apply_perk_to_crafting_type(self, crafting_type, perk_id):
        levels = self.perk_to_craft_level(perk_id)
        for index, type in enumerate(self.perk_to_craft_type(perk_id)):
            if type == 0:
                continue
            type_mask = 1 << type
            if crafting_type & type_mask == type_mask:
                crafting_type &= ~(1 << CRAFTING_LEVELS[type])
            crafting_type |= type_mask
            crafting_type |= levels[index] << CRAFTING_LEVELS[type]
            # print(perk_id, end=' ')
            # self.print_crafting_type(crafting_type)
        return crafting_type

    def print_crafting_type(self, crafting_type):
        crafting_type |= 1 << 21
        bin_string = bin(crafting_type)[-21:]
        type_string = bin_string[-7:]
        for x in range(7):
            print(bin_string[x * 2:(x + 1) * 2], end=' ')
        print(type_string)

    def perk_to_craft_type(self, perk_id):
        if perk_id in ('daedalus_protege', 'beginning_of_enigma', 'truth_to_enigma'):
            return [ITEM]
        elif perk_id == 'basic_tailor':
            return PROCESS_SOFT_MATERIAL, CRAFT_SOFT_ALLOY
        elif perk_id in ('reputable_tailor', 'famous_tailor', 'master_tailor'):
            return PROCESS_SOFT_MATERIAL, CRAFT_SOFT_ALLOY, CRAFT_SOFT_EQUIPMENT
        elif perk_id == 'apprentice_blacksmith':
            return PROCESS_HARD_MATERIAL, CRAFT_HARD_ALLOY
        elif perk_id in ('skilled_blacksmith', 'famous_blacksmith', 'master_blacksmith'):
            return PROCESS_HARD_MATERIAL, CRAFT_HARD_ALLOY, CRAFT_HARD_EQUIPMENT
        return [0]

    def perk_to_craft_level(self, perk_id):
        if perk_id == 'daedalus_protege':
            return [LEVEL_1]
        elif perk_id == 'beginning_of_enigma':
            return [LEVEL_2]
        elif perk_id == 'truth_to_enigma':
            return [LEVEL_3]
        elif perk_id in ('basic_tailor', 'apprentice_blacksmith'):
            return LEVEL_1, LEVEL_1
        elif perk_id in ('reputable_tailor', 'skilled_blacksmith'):
            return LEVEL_2, LEVEL_2, LEVEL_1
        elif perk_id in ('famous_tailor', 'famous_blacksmith'):
            return LEVEL_3, LEVEL_3, LEVEL_2
        elif perk_id in ('master_tailor', 'master_blacksmith'):
            return LEVEL_4, LEVEL_4, LEVEL_3
        return [0]

    def add_recipe_to_queue(self, output_id, type, time, count):
        item = Refs.gc.find_item(output_id)
        for index in range(count):
            crafting_item = CraftingItem(output_id, type, time)
            crafting_item.set_image_source(item.get_image())
            self.add_item_to_queue(crafting_item)

    def add_item_to_queue(self, crafting_item):
        # Add item to end of queue
        self._queue.append(crafting_item)
        self._queue_time += crafting_item.get_time()
        self._queue_count += 1
        if self._queue_count is not None:
            self._display.queue_time = self._queue_time
            self._display.queue_count = self._queue_count

        if len(self._displayed) < DISPLAY_COUNT:
            if len(self._hidden) > 0:
                self._hidden.append(crafting_item)
                crafting_item = self._hidden.pop(0)

            self._displayed.append(crafting_item)
            if self._display is not None:
                self.assign_item_display(crafting_item)
        else:
            self._hidden.append(crafting_item)

        # Test unassigned chars
        maximum_multipliers = [0 for _ in range(WORKING_SLOT_COUNT)]
        indexes = [-1 for _ in range(WORKING_SLOT_COUNT)]

        for char_index in self._unassigned_chars:
            crafting_char = self._chars[char_index]
            if not crafting_char.can_craft(crafting_item.crafting_type):
                crafting_item.tested_chars.append(char_index)
                continue
            mult = crafting_char.get_multiplier(crafting_item.crafting_type)
            for index in range(WORKING_SLOT_COUNT):
                if mult > maximum_multipliers[index]:
                    maximum_multipliers[index] = mult
                    indexes[index] = char_index
                    break

            crafting_item.tested_chars.append(char_index)

            # We have fastest crafting
            if maximum_multipliers[-1] == 2:
                break

        # Assign resultant workers
        for index in range(WORKING_SLOT_COUNT):
            if indexes[index] != -1:
                self._unassigned_chars.remove(indexes[index])
                crafting_item.assign_char(self._chars[indexes[index]], maximum_multipliers[index], index)
            else:
                break

    def advance(self, delta):
        if len(self._queue) == 0:
            return False

        # Advance the time of each item
        item_index = 0
        while item_index < len(self._queue):
            crafting_item = self._queue[item_index]
            # If an item finished, then remove it from the queue
            if crafting_item.advance(delta):
                self._queue_time -= crafting_item.get_raw_time()
                self._queue_count -= 1

                if self._display is not None:
                    self._display.queue_time = self._queue_time
                    self._display.queue_count = self._queue_count

                self._queue.remove(crafting_item)
                have_count = self._inventory.add_item(crafting_item.output_id, 1)
                if crafting_item in self._displayed:
                    self._displayed.remove(crafting_item)
                    if self._display is not None:
                        self._display.dispatch('on_item_crafted', crafting_item.output_id, have_count)
                        self._item_display.remove_widget(crafting_item.display)
                        self.unassign_item_display(crafting_item)
                elif crafting_item in self._hidden:
                    self._hidden.remove(crafting_item)

                crafting_item.chars = None
                for char_index in crafting_item.char_indexes:
                    self.unassign_char(char_index)

                if len(self._displayed) < DISPLAY_COUNT and len(self._hidden) > 0:
                    crafting_item = self._hidden.pop(0)
                    self._displayed.append(crafting_item)
                    self._queue_time += crafting_item.get_raw_time()
                    self._queue_count += 1

                    if self._display is not None:
                        self._display.queue_time = self._queue_time
                        self._display.queue_count = self._queue_count
                        self.assign_item_display(crafting_item)
                        # self._item_display.add_widget(crafting_item.display)
                continue
            item_index += 1
        return len(self._queue) == 0

    def unassign_char(self, char_index):
        if char_index == -1:
            return
        # Try to assign char to item
        if len(self._queue) == 0:
            self._unassigned_chars.append(char_index)
            return
        crafting_char = self._chars[char_index]
        for crafting_item in self._queue:
            # This item won't take this char
            if char_index in crafting_item.tested_chars:
                continue
            # Character cant craft this
            if not crafting_char.can_craft(crafting_item.crafting_type):
                continue
            # This item already has fastest chars
            if crafting_item.multipliers[-1] == 2:
                crafting_item.tested_chars.append(char_index)
                continue

            mult = crafting_char.get_multiplier(crafting_item.crafting_type)
            crafting_item.tested_chars.append(char_index)

            # Not good enough for this item
            if mult <= crafting_item.multipliers[-1]:
                continue

            for index in range(WORKING_SLOT_COUNT):
                if crafting_item.char_indexes[index] == -1:
                    crafting_item.assign_char(crafting_char, mult, index)
                    return
                elif mult > crafting_item.multipliers[index]:
                    unassigned_char_index = crafting_item.char_indexes[index]
                    unassigned_mult = crafting_item.multipliers[index]
                    if index + 1 < WORKING_SLOT_COUNT:
                        crafting_item.assign_char(crafting_item.chars[index], unassigned_mult, index + 1)
                    else:
                        self.unassign_char(unassigned_char_index)

                    crafting_item.assign_char(crafting_char, mult, index)
                    return
        # If we reach this point, then no items wanted the char
        self._unassigned_chars.append(char_index)

    def print_queue(self):
        print('Queue:')
        for item in self._queue:
            print('\t' + str(item))
        print('Displayed:')
        for item in self._displayed:
            print('\t' + str(item))
        print('Hidden:')
        for item in self._hidden:
            print('\t' + str(item))
        print()

    def get_queue_time(self):
        return self._queue_time

    def get_queue_count(self):
        return self._queue_count
