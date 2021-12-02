from random import randint

from game.battle_character import create_battle_character
from game.battle_data import BattleData
from game.floor import ENTRANCE, EXIT
from refs import Refs

N, S, E, W = 1, 2, 4, 8  # 0001 0010 0100 1000
DIRECTIONS = [N, S, E, W]
COORDS = {W: (-1, 0), N: (0, -1), E: (1, 0), S: (0, 1)}
STRING_DIRECTIONS = {N: 'North', E: 'East', S: 'South', W: 'West'}
DIRECTIONS_FROM_STRING = {'North': N, 'East': E, 'South': S, 'West': W}
OPPOSITE = {N: S, S: N, W: E, E: W}
RIGHT = {N: E, E: S, S: W, W: N}
LEFT = {N: W, W: S, S: E, E: N}
INDEX_TO_STRING = ['Surface', 'first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth', 'eleventh', 'twelfth', 'thirteenth', 'fourteenth', 'fifteenth', 'sixteenth', 'seventeenth', 'eighteenth', 'nineteenth',
                   'twentieth', 'twenty-first', 'twenty-second']
DIR_INDEX = {N: 0, E: 1, S: 2, W: 3}


class FloorData:
    def __init__(self, descend, current_floor, previous_floor_data=None):
        # Set the current floor and direction. Get the according spot in the node map.
        self._floor = Refs.gc['floors'][current_floor]
        print('Floor Data init', self._floor.get_id())

        # Check generated nodes
        # - If generated nodes are out of date, generate new ones
        self._floor.get_map().update_markers(*Refs.gc.load_floor_node_data(self._floor))

        # Keep track of which NEW nodes we have found
        self._explored = []
        # Initialize the floor map route tables and current node
        found = self._floor.get_map().set_start(descend)
        if found:
            self._explored.append(self._floor.get_map().get_current_node())

        # Set the directions we are facing
        self._current_direction = self._floor.get_map().get_directions()
        self._last_direction = None

        self._activated_safe_zones = {}
        self._rest_count = 0
        self._node_time = 0
        self._encounter_count = 1

        if not previous_floor_data:
            self._adventurers = None
            self._supporters = None
            self._get_supporters = None
            self._party_perks = []
            self._increases = None
            self._fam_bonus_increases = None
            # self._special_amount = 0
            self._gained_items = {}
            self._killed_monsters = {}
        else:
            self._adventurers = previous_floor_data.get_characters()
            self._supporters = previous_floor_data._supporters
            self._get_supporters = previous_floor_data._get_supporters
            self._party_perks = previous_floor_data.get_party_perks()
            # self._special_amount = previous_floor_data._special_amount
            self._increases, self._fam_bonus_increases = previous_floor_data.get_increases()
            self._gained_items = previous_floor_data.get_gained_items()
            self._killed_monsters = previous_floor_data.get_killed()

        self._battle_characters = []

        self._in_encounter = False
        self._battle_data = None
        self._beaten_boss = False
        self._next_floor = self._floor.get_id() + 1
        self._is_boss_fight = False
        if not previous_floor_data:
            self._generate_characters()

    # The characters keep the same special skill charge, health, mana, and status effects encounter to encounter
    def _generate_characters(self):
        party = Refs.gc.get_current_party()
        self._adventurers = []
        self._supporters = []
        self._get_supporters = {}
        self._increases = {}
        self._fam_bonus_increases = {}
        self._party_perks = []

        for index in range(8):
            char_index = party[index]
            if char_index == -1:
                continue
            support_index = party[index + 8]
            character = Refs.gc.get_char_by_index(char_index)
            support = Refs.gc.get_char_by_index(support_index)
            self._increases[char_index] = [0 for _ in range(7)]
            self._fam_bonus_increases[char_index] = {}
            if support:
                self._increases[support_index] = [0 for _ in range(7)]
                self._fam_bonus_increases[support_index] = {}
            self._adventurers.append(create_battle_character(character, support))
            self._party_perks += character.get_all_perks()
            self._supporters.append(support)
            self._get_supporters[char_index] = support_index

    # Basic getter functions
    def get_floor(self):
        return self._floor

    def set_next_floor(self, next_floor):
        self._next_floor = next_floor

    def get_next_floor(self):
        return self._next_floor

    def get_encounters(self):
        return self._encounter_count

    # Get every adventurer in the party
    def get_characters(self):
        return self._adventurers

    # Get non-dead and non-asleep adventurers
    def get_able_characters(self):
        characters = []
        for character in self._adventurers:
            if not character.is_dead() and not character.is_asleep():
                characters.append(character)
        return characters

    # Get non-dead characters
    def get_alive_characters(self):
        characters = []
        for character in self._adventurers:
            if not character.is_dead():
                characters.append(character)
        return characters

    # Get dead characters
    def get_dead_characters(self):
        characters = []
        for character in self._adventurers:
            if character.is_dead():
                characters.append(character)
        return characters

    # Get asleep characters
    def get_asleep_characters(self):
        characters = []
        for character in self._adventurers:
            if character.is_asleep():
                characters.append(character)
        return characters

    def get_explored(self):
        return self._explored

    def get_increases(self):
        return self._increases, self._fam_bonus_increases

    def increase_stat(self, char_index, index, amount):
        support_index = self._get_supporters[char_index]
        if support_index != -1:
            self._increases[support_index][index] += amount
        self._increases[char_index][index] += amount

    def have_beaten_boss(self):
        return self._beaten_boss

    def get_gained_items(self):
        return self._gained_items

    def add_gained_items(self, item_id, count):
        if item_id not in self._gained_items:
            self._gained_items[item_id] = 0
        self._gained_items[item_id] += count

    def get_killed(self):
        return self._killed_monsters

    def get_party_perks(self):
        return self._party_perks

    def party_has_perk(self, perk_id):
        return perk_id in self._party_perks

    # Movement functions
    def get_directions(self):
        options = self._floor.get_map().get_directions()
        directions = []
        for direction in DIRECTIONS:
            if options & direction == direction:
                directions.append(STRING_DIRECTIONS[direction])
        return self._current_direction, directions

    def get_basic_direction(self, direction):
        directions = [
            ['forwards', 'rightwards', 'backwards', 'leftwards'],
            ['leftwards', 'forwards', 'rightwards', 'backwards'],
            ['backwards', 'leftwards', 'forwards', 'rightwards'],
            ['rightwards', 'backwards', 'leftwards', 'forwards']]
        return directions[DIR_INDEX[self._current_direction]][DIR_INDEX[DIRECTIONS_FROM_STRING[direction]]]

    def is_activated_safe_zone(self):
        return self._floor.get_map().get_current_node() in self._activated_safe_zones.keys()

    def activate_safe_zone(self):
        self._activated_safe_zones[self._floor.get_map().get_current_node()] = 5

    def get_activated_safe_zones(self):
        return self._activated_safe_zones

    def increase_rest_count(self, count=1):
        self._rest_count += count

    def decrease_safe_zones(self):
        remove_keys = []
        for key in self._activated_safe_zones.keys():
            self._activated_safe_zones[key] -= 1
            if self._activated_safe_zones[key] == 0:
                remove_keys.append(key)
        for key in remove_keys:
            self._activated_safe_zones.pop(key)

    def get_floor_map(self):
        return self._floor.get_map()

    def get_rest_count(self):
        return self._rest_count

    def progress_by_direction(self, direction):
        floor_map = self._floor.get_map()
        dx, dy = COORDS[direction]
        x, y = floor_map.get_current_node()
        next_node = (x + dx, y + dy)

        self._last_direction = self._current_direction
        self._current_direction = direction
        self._rest_count = 0

        # Do map exploration
        if floor_map.set_current_node(next_node, self.party_has_perk('mapping')):
            self._explored.append(next_node)

        # Detract from safe zone times
        self.decrease_safe_zones()

        # Progress Character stamina. Check for incapacitation.

        # for character in self._adventurers:
        #     if not character.is_dead() and character.get_stamina() > 0:
        #         self.increase_stat(character.get_id(), 5, Refs.gc.get_random_stat_increase())
        #         character.walk(Refs.gc.get_stamina_weight() + 1)
        #
        # all_asleep = True
        # for character in self._adventurers:
        #     if character.is_dead():
        #         continue
        #     all_asleep &= character.get_stamina() <= 0
        #
        # if not all_asleep:
        #     if (x, y) not in self._activated_safe_zones and not floor_map.is_marker(EXIT):
        #         chance = 15
        #         node = None
        #         for enemy_id in self._floor.get_enemies().keys():
        #             if floor_map.is_marker(enemy_id):
        #                 node = enemy_id
        #                 chance += 50
        #                 break
        #         chance += 20 * self._rest_count
        #         self._rest_count = 0
        #         print('Chance is ', chance)
        #         if randint(1, 100) <= min(100, chance):
        #             self.generate_encounter(node, int(max(0, 100 - chance) / 50))
        #             if node is not None:
        #                 # If we are standing on a node, and we get that enemy generated, reduce positions counter
        #                 for enemy in self._battle_data.get_enemies():
        #                     if enemy.get_id() == node:
        #                         if self.party_has_perk('hunter'):
        #                             floor_map.decrease_node_counter(2)
        #                         else:
        #                             floor_map.decrease_node_counter(1)
        #                         break

    def generate_time_encounter(self, time):
        self._node_time = time
        if self.is_in_encounter():
            return
        node = None
        chance = 30
        floor_map = self._floor.get_map()
        for enemy_id in self._floor.get_enemies().keys():
            if floor_map.is_marker(enemy_id):
                node = enemy_id
                chance += 50
                break
        if randint(1, 100) <= min(100, chance):
            self.generate_encounter(node, int(max(0, 100 - chance) / 50))
            if node is not None:
                # If we are standing on a node, and we get that enemy generated, reduce positions counter
                for enemy in self._battle_data.get_enemies():
                    if enemy.get_id() == node:
                        if self.party_has_perk('hunter'):
                            floor_map.decrease_node_counter(2)
                        else:
                            floor_map.decrease_node_counter(1)
                        break

    def get_node_time(self):
        return self._node_time

    def set_node_time(self, node_time):
        self._node_time = node_time

    def get_descriptions(self):
        last_node, current_node = self._floor.get_map().get_saved_nodes()
        if last_node is None:
            return f'{self.get_starting_node_description()} The hallway stretches into the distance.'
        return f'{self.get_last_node_description(last_node)} {self.get_node_description(current_node)}'

    def get_last_direction(self):
        return STRING_DIRECTIONS[self._last_direction]

    def get_starting_node_description(self):
        if self._floor.get_map().is_marker(ENTRANCE):
            return f'You emerge from the stairs to the {INDEX_TO_STRING[self._floor.get_id()]} floor.'
        return f'You emerge from the stairs to the {INDEX_TO_STRING[self._floor.get_id() + 1]} floor.'

    def get_last_node_description(self, node):
        char = self._floor.get_map().get_node_char(node)
        compass = Refs.gc.get_inventory().has_item('compass')
        # Get the direction that we may have turned
        if self._last_direction == self._current_direction:
            if not compass:
                if char in ['┼', '├', '┤', '┬', '┴']:
                    return 'You continue forward through the intersection and down the hallway.'
                else:
                    return 'You continue down the hallway.'
            else:
                if char in ['┼', '├', '┤', '┬', '┴']:
                    return f'You continue {STRING_DIRECTIONS[self._current_direction]} through the intersection and down the hallway.'
                else:
                    return f'You continue {STRING_DIRECTIONS[self._current_direction]} down the hallway.'
        elif self._last_direction == OPPOSITE[self._current_direction]:
            # This means that we turned around.
            if node in ['╵', '╷', '╶', '╴']:
                return 'You turn back from the dead end and backtrack down the hallway.'
            else:
                return 'You backtrack down the hallway.'
        else:
            if not compass:
                if self._last_direction == S and self._current_direction == E or self._last_direction == E and self._current_direction == N or self._last_direction == N and self._current_direction == W or self._last_direction == W and \
                        self._current_direction == S:
                    return 'You turn left and continue down the ensuing hallway.'
                if self._last_direction == S and self._current_direction == W or self._last_direction == W and self._current_direction == N or self._last_direction == N and self._current_direction == E or self._last_direction == E and \
                        self._current_direction == S:
                    return 'You turn right and continue down the ensuing hallway.'
            else:
                return f'You turn {STRING_DIRECTIONS[self._current_direction]} and continue down the hallway.'
        return 'Unknown Last Path'

    def get_node_description(self, node):
        char = self._floor.get_map().get_node_char(node)
        compass = Refs.gc.get_inventory().has_item('compass')

        if self._floor.get_map().is_marker(ENTRANCE):
            return f'You encounter the stairs to the {INDEX_TO_STRING[self._floor.get_id()]} floor.'
        elif self._floor.get_map().is_marker(EXIT):
            return f'You encounter the stairs to the {INDEX_TO_STRING[self._floor.get_id() + 1]} floor.'
        elif char == '┼':
            return 'The tunnel branches into three directions. To the left, right, and forward.'
        elif char == '│':
            return 'The tunnel extends into the distance.'
        elif char == '─':
            return 'The tunnel extends into the distance.'
        elif char == '┌':
            if self._current_direction == W:
                if not compass:
                    return 'The tunnel curves to the left.'
                else:
                    return 'The tunnel curves to the South.'
            else:
                if not compass:
                    return 'The tunnel curves to the right.'
                else:
                    return 'The tunnel curves to the East.'
        elif char == '┐':
            if self._current_direction == E:
                if not compass:
                    return 'The tunnel curves to the right.'
                else:
                    return 'The tunnel curves to the South.'
            else:
                if not compass:
                    return 'The tunnel curves to the left.'
                else:
                    return 'The tunnel curves to the West.'
        elif char == '└':
            if self._current_direction == S:
                if not compass:
                    return 'The tunnel curves to the left.'
                else:
                    return 'The tunnel curves to the East.'
            else:
                if not compass:
                    return 'The tunnel curves to the right.'
                else:
                    return 'The tunnel curves to the North.'
        elif char == '┘':
            if self._current_direction == E:
                if not compass:
                    return 'The tunnel curves to the left.'
                else:
                    return 'The tunnel curves to the North.'
            else:
                if not compass:
                    return 'The tunnel curves to the right.'
                else:
                    return 'The tunnel curves to the West.'
        elif char == '├':
            if self._current_direction == N:
                if not compass:
                    return 'The tunnel continues forward and branches to the right.'
                else:
                    return 'The tunnel continues North and branches to the East.'
            elif self._current_direction == S:
                if not compass:
                    return 'The tunnel continues forward and branches to the left.'
                else:
                    return 'The tunnel continues South and branches to the East.'
            else:
                if not compass:
                    return 'The tunnel ends and branches to the left and right.'
                else:
                    return 'The tunnel ends and branches to the North and South.'
        elif char == '┤':
            if self._current_direction == N:
                if not compass:
                    return 'The tunnel continues forward and branches to the left.'
                else:
                    return 'The tunnel continues North and branches to the West.'
            elif self._current_direction == S:
                if not compass:
                    return 'The tunnel continues forward and branches to the right.'
                else:
                    return 'The tunnel continues South and branches to the West.'
            else:
                if not compass:
                    return 'The tunnel ends and branches to the left and right.'
                else:
                    return 'The tunnel ends and branches to the North and South.'
        elif char == '┬':
            if self._current_direction == E:
                if not compass:
                    return 'The tunnel continues forward and branches to the right.'
                else:
                    return 'The tunnel continues East and branches to the South.'
            elif self._current_direction == W:
                if not compass:
                    return 'The tunnel continues forward and branches to the left.'
                else:
                    return 'The tunnel continues West and branches to the South.'
            else:
                if not compass:
                    return 'The tunnel ends and branches to the left and right.'
                else:
                    return 'The tunnel ends and branches to the East and West.'
        elif char == '┴':
            if self._current_direction == E:
                if not compass:
                    return 'The tunnel continues forward and branches to the left.'
                else:
                    return 'The tunnel continues East and branches to the North.'
            elif self._current_direction == W:
                if not compass:
                    return 'The tunnel continues forward and branches to the right.'
                else:
                    return 'The tunnel continues West and branches to the North.'
            else:
                if not compass:
                    return 'The tunnel ends and branches to the left and right.'
                else:
                    return 'The tunnel ends and branches to the East and West.'
        elif char == '╵' or char == '╷' or char == '╶' or char == '╴':
            return 'The tunnel ends in a dead end.'
        else:
            return 'Unknown current path'

    def is_in_encounter(self):
        return self._in_encounter

    def get_encounter_state(self):
        return self._battle_data.get_state()

    def _generate_battle_characters(self):
        adventurers = self.get_able_characters()[:4]
        supporters = []

        for adventurer in adventurers:
            index = self._adventurers.index(adventurer)
            supporters.append(self._supporters[index])
        return adventurers, supporters

    def generate_encounter(self, node_type, extra_boost):
        self._in_encounter = True
        self._encounter_count += 1
        self._battle_data = BattleData(self, *self._generate_battle_characters())
        self._battle_data.set_state('start')
        enemies = self._floor.generate_enemies(node_type, extra_boost)
        self._battle_data.set_enemies(enemies)

    def generate_boss_encounter(self):
        self._is_boss_fight = True
        self._in_encounter = True
        self._encounter_count += 1
        self._battle_data = BattleData(self, *self._generate_battle_characters(), True)
        self._battle_data.set_state('battle')
        self._battle_data.set_enemies(self._floor.generate_boss())

    def end_encounter(self):
        self._in_encounter = False
        for item, count in self._battle_data.get_dropped_items().items():
            if item not in self._gained_items:
                self._gained_items[item] = 0
            self._gained_items[item] += count
        for enemy in self._battle_data.get_enemies():
            if enemy.get_name() not in self._killed_monsters:
                self._killed_monsters[enemy.get_name()] = 0
            self._killed_monsters[enemy.get_name()] += 1
        # self._special_amount = self._battle_data.get_special_amount()
        self._battle_data = None
        if not self._beaten_boss and self._is_boss_fight:
            self._beaten_boss = self._is_boss_fight
        # Clear status effects from characters
        for character in self._adventurers:
            character.clear_effects()
        # Award Fam Bonus
        bonuses = Refs.gc.generate_familiarity_bonuses(Refs.gc.get_current_party())
        for char_index, increases in bonuses.items():
            for partner_index, amount in increases.items():
                if partner_index not in self._fam_bonus_increases[char_index]:
                    self._fam_bonus_increases[char_index][partner_index] = 0
                self._fam_bonus_increases[char_index][partner_index] += amount

    def get_battle_data(self):
        return self._battle_data

    def replace_character(self, battle_characters, index):
        replaced = False
        for character in self.get_able_characters():
            if character in battle_characters:
                continue
            replaced = True
            battle_characters[index] = character
            break
        if not replaced:
            battle_characters[index] = None
        return battle_characters

    def swap_character_order(self, character, other_character):
        index = self._adventurers.index(character)
        other_index = self._adventurers.index(other_character)
        self._adventurers[index] = other_character
        self._adventurers[other_index] = character
