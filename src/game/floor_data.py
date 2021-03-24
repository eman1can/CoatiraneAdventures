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
    def __init__(self, descend, current_floor):
        # Set the current floor and direction. Get the according spot in the node map.
        self._floor = Refs.gc['floors'][current_floor]

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

        self._in_encounter = False
        self._battle_data = None
        self._adventurers = None
        self._supporters = None
        self._increases = None
        self._special_amount = 0
        self._gained_items = {}
        self._killed_monsters = {}
        self._party_perks = []
        self._generate_characters()

    # Basic getter functions
    def get_floor(self):
        return self._floor

    def get_characters(self):
        return self._adventurers

    def get_explored(self):
        return self._explored

    def get_increases(self):
        return self._increases

    def get_gained_items(self):
        return self._gained_items

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

    def progress_by_direction(self, direction):
        floor_map = self._floor.get_map()
        dx, dy = COORDS[direction]
        x, y = floor_map.get_current_node()
        next_node = (x + dx, y + dy)

        self._last_direction = self._current_direction
        self._current_direction = direction

        # Do map exploration
        if floor_map.set_current_node(next_node, self.party_has_perk('mapping')):
            self._explored.append(next_node)

        # Detract from safe zone times
        self.decrease_safe_zones()

        # Progress Character stamina. Check for incapacitation.
        for character in self._adventurers:
            character.walk()

        # for character in self._adventurers:
        #     print(character.get_name(), 'Stamina is', character.get_stamina())

        # On movement, 15% chance for encounter
        # On node, chance +50%
        # For every rest count, chance + 20%
        # For every time you mine / dig, chance +40%
        if (x, y) not in self._activated_safe_zones:
            chance = 15
            node = None
            for enemy_id in self._floor.get_enemies().keys():
                if floor_map.is_marker(enemy_id):
                    node = enemy_id
                    chance += 50
                    break
            chance += 20 * self._rest_count
            self._rest_count = 0
            if randint(1, 100) < min(100, chance):
                self.generate_encounter(node)
                if node is not None:
                    # If we are standing on a node, and we get that enemy generated, reduce positions counter
                    for enemy in self._battle_data.get_enemies():
                        if enemy.get_id() == node:
                            if self.party_has_perk('hunter'):
                                floor_map.decrease_node_counter(2)
                            else:
                                floor_map.decrease_node_counter(1)
                            break

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
        compass = Refs.gc.in_inventory('compass')
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
        compass = Refs.gc.in_inventory('compass')

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

    def end_encounter(self):
        self._in_encounter = False
        for key, count in self._battle_data.get_dropped_items().items():
            if key not in self._gained_items:
                self._gained_items[key] = 0
            self._gained_items[key] += count
        for enemy in self._battle_data.get_enemies():
            if enemy.get_name() not in self._killed_monsters:
                self._killed_monsters[enemy.get_name()] = 0
            self._killed_monsters[enemy.get_name()] += 1
        self._special_amount = self._battle_data.get_special_amount()
        self._battle_data = None
        # Clear status effects from characters

    def generate_encounter(self, node_type):
        self._in_encounter = True
        adventurers = []
        supporters = []
        for index, adventurer in enumerate(self._adventurers):
            if not adventurer.is_dead():
                adventurers.append(adventurer)
                if index < len(supporters):
                    supporters.append(self._supporters[index])
        self._battle_data = BattleData(adventurers, supporters, self._special_amount)
        self._battle_data.set_state('start')
        self._battle_data.set_enemies(self._floor.generate_enemies(node_type))

    # The characters keep the same special skill charge, health, mana, and status effects encounter to encounter
    def _generate_characters(self):
        party = Refs.gc.get_current_party()
        self._adventurers = []
        self._supporters = []
        self._increases = {}
        self._party_perks = []

        for index in range(16):
            character = party[index]
            if character is None:
                continue
            self._increases[character.get_id()] = [5 for _ in range(7)]
            if index < 8:
                support = party[index + 8]
                self._adventurers.append(create_battle_character(character, support))
                self._party_perks += character.get_perks()
            else:
                self._supporters.append(character)

    def get_battle_data(self):
        return self._battle_data
