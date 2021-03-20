# Standard Library Imports
from random import randint, choices

N, S, E, W = 1, 2, 4, 8  # 0001 0010 0100 1000

ENTRANCE_COLOR = '#0000FF'
EXIT_COLOR = '#FF0000'
CURRENT_COLOR = '#93E9BE'
PATH_COLOR = '#DA8FBE'
SAFE_ZONE_COLOR = '#FEDE00'

# ENEMIES
GOBLIN_COLOR = '#75AC19'
KOBOLD_COLOR = '#9FC8FF'
JACK_BIRD_COLOR = '#FECA34'

ENTRANCE = 'entrance'
EXIT = 'exit'
SAFE_ZONES = 'safe_zones'
MARKER_COLORS = {'safe_zones': SAFE_ZONE_COLOR, 'entrance': ENTRANCE_COLOR, 'exit': EXIT_COLOR,
                 'goblin': GOBLIN_COLOR, 'kobold': KOBOLD_COLOR, 'jack_bird': JACK_BIRD_COLOR}


class Floor:
    """
    Boss Type:
    0 - Boss is a single Enemy and has been passed in the boss parameter
    1 - Boss is multiple of the passed boss parameter with maxCounts
    2 - Boss is multiple of the passed boss parameter with maxCounts upped by 40%
    3 - Boss is multiple of normally passed enemies - maxCounts upped by 40%
    4 - Boss is multiple of normally passed enemies - maxCounts upped by 40% & stats upped by 30%


    Floor Information:
    For each floor, the MP will have a route that they can follow, and enery time they move along a 'node'
    they will have a chance to run into an encounter.
    The boss will be on the exit node, and going onto the exit node will trigger the screen before a boss battle.
    The boss battle will vary as above, and will be harder than other encounters on the floor.
    Once a boss battle has been cleared, the adventurers can go down to the next floor or turn back.

    The floor will have a map that can be purchased in town, and a path map that is only the map to the next floor.
    To be able to make a map as you progress through a floor you need to have a character who is a mapper in your party.

    Encounter generation will take into account bonuses from character abilities
    At the end of the encounter, item and falna drops are calculated and distributed
    Event status updates are taken care of inside encounter

    """

    def __init__(self, floor_id, max_enemies, boss_type, enemies, probabilities, floor_data, path_data, floor_map, save_zone_data):
        self._floor_id = floor_id
        self._max_enemies = max_enemies
        self._boss_type = boss_type
        self._enemies = enemies
        self._probabilities = probabilities

        self._resources = {}

        self._map = Map(floor_map, floor_data, path_data, {SAFE_ZONES: save_zone_data, ENTRANCE: [path_data[0]], EXIT: [path_data[-1]]})

    def get_id(self):
        return self._floor_id

    def get_map(self):
        return self._map

    def get_score(self):
        # Floor 1 rec score should be ~ 7
        score = 0
        for enemy in self._enemies:
            score += enemy.get_score()
        return round(score, 0)

    # def generateBoss(self):
    #     if self.bossType == 0:
    #         return [self.boss]
    #     elif self.bossType == 1:
    #         min = int(self.max_enemies * self.MINMAXENEMIES)
    #         if not min > 1:
    #             min = 1
    #         num = random.randint(min, self.max_enemies)
    #         enemies = []
    #         for x in range(num):
    #             enemies.append(self.boss)
    #         return enemies
    #     elif self.bossType == 2:
    #         min = int(self.max_enemies * (self.MINMAXENEMIES + self.BOSSMULTIPLIER))
    #         if not min > 1:
    #             min = 1
    #         num = random.randint(min,
    #                              int(self.max_enemies * (1 + self.BOSSMULTIPLIER)))
    #         enemies = []
    #         for x in range(num):
    #             enemies.append(self.boss)
    #         return enemies
    #     elif self.bossType == 3:
    #         min = int(self.max_enemies * (self.MINMAXENEMIES + self.BOSSMULTIPLIER))
    #         if not min > 1:
    #             min = 1
    #         num = random.randint(min, int(self.max_enemies * (1 + self.BOSSMULTIPLIER)))
    #         enemies = []
    #         for x in range(num):
    #             num = random.randint(0, self.PERCENT100)
    #             for y in range(len(self.probabilities)):
    #                 if num < (self.probabilities[y] * self.PERCENT100):
    #                     enemies.append(self.enemies[y].new_instance(1))
    #                     break
    #                 else:
    #                     num -= (self.probabilities[y] * self.PERCENT100)
    #         return enemies
    #     elif self.bossType == 4:
    #         min = int(self.max_enemies * (self.MINMAXENEMIES + self.BOSSMULTIPLIER))
    #         if not min > 1:
    #             min = 1
    #         num = random.randint(min, int(self.max_enemies * (1 + self.BOSSMULTIPLIER)))
    #         enemies = []
    #         for x in range(num):
    #             num = random.randint(0, self.PERCENT100)
    #             for y in range(len(self.probabilities)):
    #                 if num < (self.probabilities[y] * self.PERCENT100):
    #                     enemies.append(self.enemies[y].new_instance(1 + self.BOSSSTATMULTIPLIER))
    #                     break
    #                 else:
    #                     num -= (self.probabilities[y] * self.PERCENT100)
    #         return enemies

    def generate_enemies(self, node_type):
        #TODO Chance to 1-5 rarity
        minimum = int(self._max_enemies * 0.25)
        if not minimum >= 1:
            minimum = 1
        enemies = []
        weights = self._probabilities
        for x in range(randint(minimum, self._max_enemies)):
            enemy = choices(self._enemies, list(weights.values()), k=1)[0]
            enemies.append(enemy.new_instance(self._floor_id))
        return enemies

    def get_enemies(self):
        return self._enemies

    def get_resources(self):
        return self._resources


class Map:
    def __init__(self, full_map, nodes, path_nodes, markers):
        self._width = full_map.index('\n')
        self._size = int((self._width - 3) / 2)

        # Given Map Data
        self._full_map = full_map
        self._map_data = None
        self._nodes = nodes
        self._path_nodes = path_nodes
        self._map_radius = 5

        # Current Map Data
        self._current_node = None
        self._last_node = None
        self._current_prev_color = None
        self._enabled = True

        # Marker and path data
        self._current_path = None
        self._shortest_key = None
        self._path_solutions = {}
        # The path layer is the route to any selected route
        self._layers = {'path': True}
        self._markers = markers
        for layer in markers.keys():
            self._layers[layer] = True

        # Current map progress
        self._explored = {}
        for node in list(self._nodes.keys()):
            self._explored[node] = False

        # Explored nodes
        self._explored_nodes = {}
        self._explored_node_counters = {}

    def get_enabled(self):
        return self._enabled

    def set_enabled(self, enabled):
        self._enabled = enabled

    # Explored nodes
    def load_node_exploration(self, explored_nodes, explored_node_counters):
        self._explored_nodes = {}
        self._explored_node_counters = {}
        for node, shown in explored_nodes.items():
            x, y = node[1:-1].split(', ')
            self._explored_nodes[(int(x), int(y))] = shown
            if not shown:
                self._explored_node_counters[(int(x), int(y))] = explored_node_counters[node]

    def get_node_exploration(self):
        return self._explored_nodes, self._explored_node_counters

    # Create the map from an explored array
    def create_current_map(self, explored):
        self._explored = {}
        for node, shown in explored.items():
            x, y = node[1:-1].split(', ')
            self._explored[(int(x), int(y))] = shown
        # Create the current map
        self._map_data = MapData(self._width, self._size, self._full_map, self._explored)

    # Add node data marker to markers
    def update_markers(self, node_data, generated):
        if generated:
            self._explored_nodes = {}
            self._explored_node_counters = {}
            for marked_nodes in node_data.values():
                for marked_node in marked_nodes:
                    self._explored_nodes[marked_node] = False
                    self._explored_node_counters[marked_node] = 3
            # Clear bought / obtained node maps from inventory
        for marker, nodes in node_data.items():
            self._markers[marker] = nodes
            self._layers[marker] = True
        # Refresh marker color displays
        self._check_markers()

    def get_size(self):
        return self._size

    def get_radius(self):
        return self._map_radius

    def set_radius(self, radius):
        self._map_radius = radius

    def get_explored(self):
        return self._explored

    def get_current_node(self):
        return self._current_node

    def get_last_node(self):
        return self._last_node

    def get_saved_nodes(self):
        return self._last_node, self._current_node

    def get_node_char(self, node):
        return self._map_data.get_node(*node)

    # Is called at the creation of floor data
    def set_start(self, descend):
        self._shortest_key = None
        self._path_solutions = {ENTRANCE: {}, EXIT: {}}
        if descend:
            found = self.set_current_node(self._path_nodes[0])
            self._current_path = 'exit'
            # We KNOW that we are on the entrance, and the path to the exit is just the path
            self._path_solutions[ENTRANCE][self._path_nodes[0]] = [self._path_nodes[0]]
            self._path_solutions[EXIT][self._path_nodes[-1]] = list(reversed(self._path_nodes))
        else:
            found = self.set_current_node(self._path_nodes[-1])
            self._current_path = 'entrance'
            # We KNOW that we are on the exit, and the path to the entrance is just the reversed path
            self._path_solutions[ENTRANCE][self._path_nodes[0]] = list(self._path_nodes)
            self._path_solutions[EXIT][self._path_nodes[-1]] = [self._path_nodes[-1]]
        # Remove starting node from arrays
        self._update_path(self._current_node)
        # Color path
        self._calculate_path()
        return found

    def set_current_node(self, node):
        # Are we just discovering this node?
        found = not self._explored[node]
        if found:
            self._explored[node] = True
            self._map_data.show_node(*node)
        # Restore previous color
        if self._current_node is not None:
            self._map_data.color_node(*self._current_node, self._current_prev_color)
        self._update_path(node)
        # Set next current
        self._last_node = self._current_node
        self._current_node = node
        self._current_prev_color = self._map_data.color_node(*self._current_node, CURRENT_COLOR)
        # Don't save path color
        if self._current_prev_color == PATH_COLOR:
            self._current_prev_color = None
        return found

    def clear_current_node(self):
        # Restore color and blank values
        self._map_data.color_node(*self._current_node, self._current_prev_color)
        self._current_node = None
        self._last_node = None
        self._current_prev_color = None

    # Get rows of map for output
    def get_rows(self):
        return self._map_data.get_section(*self._current_node, self._map_radius)

    # Used for getting data from map data
    def get_directions(self):
        return self._nodes[self._current_node]

    def get_markers(self):
        return self._markers

    def layer_active(self, layer):
        return self._layers[layer]

    def set_layer_active(self, layer, active):
        self._layers[layer] = active
        self._check_markers()
        if not self._layers['path']:
            self._clear_path()

    # Get or set the current path objective
    def get_current_path(self):
        return self._current_path

    def set_current_path(self, dest_type):
        self._clear_path()
        self._current_path = dest_type
        self._check_path()

    def _show_node(self, node):
        found = not self._explored[node]
        if found:
            self._explored[node] = True
            self._map_data.show_node(*node)
        return found

    def hide_node(self, node):
        self._explored[node] = False
        self._map_data.hide_node(node)

    # Unlock versions of the map
    def unlock_path_map(self):
        for node in self._path_nodes:
            self._show_node(node)
        self._check_markers()
        self._calculate_path()

    def unlock_full_map(self):
        for node in list(self._nodes.keys()):
            self._show_node(node)
        self._check_markers()
        self._calculate_path()

    def _update_path(self, node):
        # Update the path arrays for every defined path
        for layer, layer_route in self._path_solutions.items():
            for route_end, route in layer_route.items():
                if layer == self._current_path and route_end == self._shortest_key:
                    if len(route) > 0 and node == route[-1]:
                        self._clear_path_node(self._current_node)
                    else:
                        self._color_path_node(self._current_node)
                if len(route) > 0 and node == route[-1]:
                    route.pop()
                else:
                    route.append(self._current_node)
                if layer == 'kobold':
                    print(route)

        self._calculate_path()

    # Check to see if any changes to explored or paths has changed the route
    def _calculate_path(self):
        if self._current_path is None:
            return

        # We have deactivated the path
        if not self._layers['path']:
            self._clear_path()
        else:
            shortest_key = list(self._path_solutions[self._current_path].keys())[0]
            shortest = len(self._path_solutions[self._current_path][shortest_key])
            for route_end, route in self._path_solutions[self._current_path].items():
                if self._explored[route_end] and (self._current_path in [EXIT, ENTRANCE, SAFE_ZONES] or self._explored_nodes[route_end]):
                    if len(route) < shortest:
                        shortest = len(route)
                        shortest_key = route_end
            if shortest_key is not None and shortest_key != self._shortest_key:
                self._clear_path()
                self._shortest_key = shortest_key
                self._color_path()

    def _clear_path(self):
        if self._shortest_key is not None:
            for node in self._path_solutions[self._current_path][self._shortest_key]:
                self._clear_path_node(node)
            self._shortest_key = None

    def _clear_path_node(self, node):
        if self._map_data.get_color(*node) == PATH_COLOR:
            self._map_data.color_node(*node, None)

    def _color_path(self):
        for node in self._path_solutions[self._current_path][self._shortest_key]:
            self._color_path_node(node)

    def _color_path_node(self, node):
        if not self._map_data.get_color(*node):
            self._map_data.color_node(*node, PATH_COLOR)

    # Make sure that path type has routes
    def _check_path(self):
        if self._current_path not in self._path_solutions:
            routes = {}
            for route_end in self._markers[self._current_path]:
                routes[route_end] = list(reversed(self.solve_path(0, self._current_node, route_end, self._nodes)[1:]))
                print(routes[route_end])
            self._path_solutions[self._current_path] = routes
        # Show the shortest route
        self._calculate_path()

    def is_marker(self, marker_type):
        return self._current_node in self._markers[marker_type]

    # Check markers for a specific node
    def _check_marker_color(self, node):
        for layer, routes in self._markers.items():
            if self._layers[layer] and node in routes and (layer in [EXIT, ENTRANCE, SAFE_ZONES] or self._explored_nodes[node]):
                self._set_marker_color(node, layer)

    # Color all markers
    def _check_markers(self):
        for layer, nodes in self._markers.items():
            for node in nodes:
                if not self._layers[layer]:
                    self._clear_marker_color(node)
                elif layer in [EXIT, ENTRANCE, SAFE_ZONES] or self._explored_nodes[node]:
                    self._set_marker_color(node, layer)

    def _set_marker_color(self, node, layer):
        if self._map_data.get_color(*node) != CURRENT_COLOR:
            self._map_data.color_node(*node, MARKER_COLORS[layer])
        else:
            self._current_prev_color = MARKER_COLORS[layer]

    def _clear_marker_color(self, node):
        # If a node is colored, clear if not path or current
        if self._map_data.get_color(*node) != PATH_COLOR:
            if self._map_data.get_color(*node) == CURRENT_COLOR:
                self._current_prev_color = None
                return
            # If node WAS a path coloring, restore color
            if self._shortest_key is not None and node in self._path_solutions[self._current_path][self._shortest_key]:
                self._map_data.color_node(*node, PATH_COLOR)
            else:
                self._map_data.color_node(*node, None)

    @staticmethod
    def solve_path(last, start, end, nodes):
        if start == end:
            return [end]
        node = nodes[start]
        if (node & N) == N and last != S:
            path = Map.solve_path(N, (start[0], start[1] - 1), end, nodes)
            if path:
                return [start] + path
        if (node & E) == E and last != W:
            path = Map.solve_path(E, (start[0] + 1, start[1]), end, nodes)
            if path:
                return [start] + path
        if (node & S) == S and last != N:
            path = Map.solve_path(S, (start[0], start[1] + 1), end, nodes)
            if path:
                return [start] + path
        if (node & W) == W and last != E:
            path = Map.solve_path(W, (start[0] - 1, start[1]), end, nodes)
            if path:
                return [start] + path
        return False


class MapData:
    def __init__(self, width, size, full_map, explored):
        self._width = width
        self._size = size

        self._colors = []

        # Copy the outline
        self._data = []
        self._visible_data = []
        self._colors = [[None for _ in range(size)] for _ in range(size)]
        string_width = width + 1
        for ay in range(self._size + 2):
            self._data.append([])
            self._visible_data.append([])
            for ax in range(self._width):
                if 0 < ax < self._width - 2 and 0 < ay < self._size + 1:
                    x, y = int((ax - 1) / 2), ay - 1
                    self._data[ay].append(full_map[ay * string_width + ax])
                    if (x, y) in explored and explored[(x, y)]:
                        self._visible_data[ay].append(full_map[ay * string_width + ax])
                    else:
                        self._visible_data[ay].append(' ')
                else:
                    self._data[ay].append(full_map[ay * string_width + ax])
                    self._visible_data[ay].append(full_map[ay * string_width + ax])

    def _abs(self, x, y):
        return x * 2 + 2, y + 1

    # Apply color, overwriting previous color and returning it
    def color_node(self, x, y, color):
        prev_color = self._colors[y][x]
        self._colors[y][x] = color
        return prev_color

    def get_color(self, x, y):
        return self._colors[y][x]

    # Will get the node from the full map
    def get_node(self, x, y):
        return self._data[y + 1][x * 2 + 2]

    # Transfer node from full map to visible map
    def show_node(self, x, y):
        ax, ay = self._abs(x, y)
        self._visible_data[ay][ax] = self._data[ay][ax]
        self._visible_data[ay][ax - 1] = self._data[ay][ax - 1]

    # Remove node from visible map
    def hide_node(self, x, y):
        ax, ay = self._abs(x, y)
        self._visible_data[ay][ax] = ' '
        self._visible_data[ay][ax - 1] = ' '

    def _insert_colors(self, dx, top, bottom, left, right):
        data = ['┌']
        for _ in range(dx):
            data[-1] += '─'
        data[-1] += '┐'
        for ay in range(top, bottom):
            data.append('│')
            for ax in range(left, right):
                x, y = int((ax - 1) / 2), ay - 1
                if self._colors[y][x]:
                    data[-1] += f'[color={self._colors[y][x]}]' + self._visible_data[ay][ax] + '[/color]'
                else:
                    data[-1] += self._visible_data[ay][ax]
            data[-1] += '│'
        data.append('└')
        for _ in range(dx):
            data[-1] += '─'
        data[-1] += '┘'
        return data

    # Will get the section of the visible map
    def get_section(self, x, y, radius):
        radius = int(min((self._size - 1) / 2, radius))
        x, y = self._abs(x, y)
        rx, ry = radius * 2, radius

        left, top = max(1, x - rx), max(1, y - ry)
        right, bottom = min(self._width - 2, x + rx), min(self._size + 1, y + ry)
        dx = rx * 2 + 1
        dy = ry * 2 + 1

        if right - left != dx:
            if left == 1:
                right = dx + 1
            else:
                left = right - dx
        if top - bottom != dy:
            if top == 1:
                bottom = dy + 1
            else:
                top = bottom - dy

        return self._insert_colors(dx, top, bottom, left, right), radius
