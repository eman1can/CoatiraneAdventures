from game.battle_character import create_battle_character
from game.battle_data import BattleData
from refs import Refs

N, S, E, W = 1, 2, 4, 8  # 0001 0010 0100 1000
DIRECTIONS = [N, S, E, W]
COORDS = {W: (-1, 0), N: (0, -1), E: (1, 0), S: (0, 1)}
STRING_DIRECTIONS = {N: 'North', E: 'East', S: 'South', W: 'West'}
DIRECTIONS_FROM_STRING = {'North': N, 'East': E, 'South': S, 'West': W}
OPPOSITE = {N: S, S: N, W: E, E: W}
INDEX_TO_STRING = ['Surface', 'first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth', 'eleventh', 'twelfth', 'thirteenth', 'fourteenth', 'fifteenth', 'sixteenth', 'seventeenth', 'eighteenth', 'nineteenth',
                   'twentieth', 'twenty-first', 'twenty-second']
DIR_INDEX = {N: 0, E: 1, S: 2, W: 3}


class FloorData:
    def __init__(self, descend, current_floor):
        # Set the current floor and direction. Get the according spot in the node map.
        self._floor_id = current_floor
        self._current_node = None
        self._last_node = None
        self._current_direction = None
        self._last_direction = None
        self._floor = Refs.gc['floors'][current_floor]
        if descend:
            # Grab the entrance as the current node and grab any map data depending on inventory
            self._current_node = self._floor.get_entrance()
        else:
            # Grab the exit as the current node and grab any map data depending on inventory
            self._current_node = self._floor.get_exit()
        # The only direction for the entrance and exit will always be the direction we are facing.
        # We would also be facing the direction of our progression
        # or the opposite of the direction we arrive at a node
        self._current_direction = self.get_node_options(self._current_node)

        self._explored = []
        if self._floor.get_floor_map().show_node(self._current_node):
            self._explored.append(self._current_node)
        self._floor.get_floor_map().set_current(self._current_node)

        self._in_encounter = False
        self._battle_data = None
        self._adventurers = None
        self._supporters = None
        self._increases = None
        self._special_amount = 0
        self._gained_items = {}
        self._killed_monsters = {}
        self._generate_characters()

    def get_id(self):
        return self._floor_id

    def get_explored(self):
        return self._explored

    def get_increases(self):
        return self._increases

    def clear_current(self):
        self._floor.get_floor_map().clear_current()

    def get_node_options(self, node):
        return self._floor.get_node(node)

    def get_gained_items(self):
        return self._gained_items

    def get_killed(self):
        return self._killed_monsters

    def get_directions(self):
        options = self.get_node_options(self._current_node)
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
            ['rightwards', 'backwards', 'leftwards', 'forwards']
        ]
        return directions[DIR_INDEX[self._current_direction]][DIR_INDEX[DIRECTIONS_FROM_STRING[direction]]]

    def at_entrance(self):
        return self._current_node == self._floor.get_entrance()

    def at_exit(self):
        return self._current_node == self._floor.get_exit()

    def get_next_node_in_path(self, node):
        index = self._floor.get_node_path_index(node)
        if index == -1:
            return None
        else:
            return self._floor.get_node_by_index(index + 1)

    def progress_by_direction(self, direction):
        x, y = COORDS[direction]
        self._last_direction = self._current_direction
        self._current_direction = direction
        next_node = (self._current_node[0] + x, self._current_node[1] + y)

        # Do map exploration
        if self._floor.get_floor_map().show_node(next_node):
            self._explored.append(next_node)
        self._floor.get_floor_map().set_current(next_node)

        if next_node not in self._floor.get_nodes():
            raise Exception('Invalid progression!')
        self._last_node = self._current_node
        self._current_node = next_node

    def get_current_node(self):
        return self._current_node

    def get_map(self):
        return self._floor.get_floor_map().get_map()

    def hide_node(self, node):
        self._floor.get_floor_map().hide_node(node)

    def get_descriptions(self):
        if self._last_node is None:
            return f'{self.get_node_description(self._current_node, True)} The hallway stretches into the distance.'
        return f'{self.get_node_description(self._last_node, True)} {self.get_node_description(self._current_node)}'

    def get_last_direction(self):
        return STRING_DIRECTIONS[self._last_direction]

    def get_node_description(self, node, last=False):
        char = self._floor.get_map_char(node)
        compass = False

        if last:
            if self._last_node is None:
                if node == self._floor.get_entrance():
                    return f'You emerge from the stairs to the {INDEX_TO_STRING[self._floor_id]} floor.'
                elif node == self._floor.get_exit():
                    return f'You emerge from the stairs to the {INDEX_TO_STRING[self._floor_id + 1]} floor.'
            else:
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
        else:
            if node == self._floor.get_entrance():
                return f'You encounter the stairs to the {INDEX_TO_STRING[self._floor_id]} floor.'
            elif node == self._floor.get_exit():
                return f'You encounter the stairs to the {INDEX_TO_STRING[self._floor_id + 1]} floor.'
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

    def generate_encounter(self):
        self._in_encounter = True
        adventurers = []
        supporters = []
        for index, adventurer in enumerate(self._adventurers):
            if not adventurer.is_dead():
                adventurers.append(adventurer)
                supporters.append(self._supporters[index])
        self._battle_data = BattleData(adventurers, supporters, self._special_amount)
        self._battle_data.set_state('start')
        self._battle_data.set_enemies(self._floor.generate_enemies())

    # The characters keep the same special skill charge, health, mana, and status effects encounter to encounter
    def _generate_characters(self):
        party = Refs.gc.get_current_party()
        self._adventurers = []
        self._supporters = []
        self._increases = {}

        for index in range(16):
            character = party[index]
            if character is None:
                continue
            self._increases[character.get_id()] = [5 for _ in range(7)]
            if index < 8:
                support = party[index + 8]
                self._adventurers.append(create_battle_character(character, support))
            else:
                self._supporters.append(character)

    def get_battle_data(self):
        return self._battle_data
