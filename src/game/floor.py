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

# Boss Types
INDIVIDUAL_BOSS          = 0
MULTIPLE_BOSS            = 1
MULTIPLE_BOOSTED_BOSS    = 2
MULTIPLE_ENEMIES         = 3
MULTIPLE_BOOSTED_ENEMIES = 4


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

    def __init__(self, floor_id, hardness, max_enemies, boss_type, enemies, metals, gems, floor_data, path_data, floor_map, save_zone_data):
        self._floor_id = floor_id
        self._max_enemies = max_enemies
        self._boss_type = boss_type
        self._enemies = enemies
        self._hardness = hardness

        self._resources = {'metals': metals, 'gems': gems}

        self._map = Map(floor_map, floor_data, path_data, {SAFE_ZONES: save_zone_data, ENTRANCE: [path_data[0]], EXIT: [path_data[-1]]})

    def get_id(self):
        return self._floor_id

    def get_map(self):
        return self._map

    def get_hardness(self):
        return self._hardness

    def get_score(self):
        # Floor 1 rec score should be ~ 7
        score = 0
        for enemy, rarity in self._enemies.values():
            score += enemy.get_score(0)
        return round(score, 0)

    def get_enemies(self):
        return self._enemies

    def get_resources(self):
        return self._resources

    def get_boss_type(self):
        return self._boss_type

    def generate_boss(self):
        if self._boss_type == INDIVIDUAL_BOSS:
            pass
        elif self._boss_type == MULTIPLE_BOSS:
            pass
        elif self._boss_type == MULTIPLE_BOOSTED_BOSS:
            pass
        elif self._boss_type == MULTIPLE_ENEMIES:
            return self.generate_enemies(None, 0, boss=self._boss_type)
        elif self._boss_type == MULTIPLE_BOOSTED_ENEMIES:
            return self.generate_enemies(None, 0, boss=self._boss_type)

    def generate_enemies(self, node_type, extra_boost, boss=-1):
        if boss == -1:
            spawn_count = randint(max(1, int(self._max_enemies * 0.25)), self._max_enemies)
        else:
            spawn_count = self._max_enemies
        rarities = choices([1, 2, 3, 4, 5], [1 / (2 ** (x + 1)) for x in range(5)], k=spawn_count)
        enemies = []
        spawn_lists = {spawn_rarity: [] for spawn_rarity in set(rarities)}

        if node_type is None:
            rarity_adjustment = 0
        else:
            rarity_adjustment = 1
            for (enemy, rarity) in self._enemies.values():
                if enemy.get_id() == node_type and rarity == 1:
                    rarity_adjustment = 2
                    break

        for spawn_rarity in set(rarities):
            for (enemy, rarity) in self._enemies.values():
                if rarity_adjustment == 0:
                    if rarity <= spawn_rarity:
                        print('Rarity Adjustment 0', enemy.get_name(), spawn_rarity - rarity)
                        spawn_lists[spawn_rarity].append((enemy, spawn_rarity - rarity))
                elif rarity_adjustment == 1:
                    if enemy.get_id() == node_type:
                        if max(rarity - 1, 1) <= spawn_rarity:
                            print('Rarity Adjustment 1 - node', enemy.get_name(), spawn_rarity - (rarity - 1))
                            spawn_lists[spawn_rarity].append((enemy, spawn_rarity - (rarity - 1)))
                    else:
                        if rarity <= spawn_rarity:
                            print('Rarity Adjustment 1', enemy.get_name(), spawn_rarity - rarity)
                            spawn_lists[spawn_rarity].append((enemy, spawn_rarity - rarity))
                else:
                    if enemy.get_id() == node_type:
                        if rarity <= spawn_rarity:
                            print('Rarity Adjustment 2 - node', enemy.get_name(), spawn_rarity - rarity)
                            spawn_lists[spawn_rarity].append((enemy, spawn_rarity - rarity))
                    elif min(rarity + 1, 5) <= spawn_rarity:
                        print('Rarity Adjustment 2', enemy.get_name(), spawn_rarity - (rarity + 1))
                        spawn_lists[spawn_rarity].append((enemy, spawn_rarity - (rarity + 1)))
        for spawn_rarity in rarities:
            enemy, boost = spawn_lists[spawn_rarity][randint(0, len(spawn_lists[spawn_rarity]) - 1)]
            boost += extra_boost
            if boss == MULTIPLE_BOOSTED_ENEMIES:
                enemies.append(enemy.new_instance(boost + 1))
            else:
                enemies.append(enemy.new_instance(boost))
        return enemies

    def generate_resource(self, node_type, metal_skew=True):
        options, weights = [], [0]
        if metal_skew:
            for material, hard in self._resources['metals'].items():
                if material == node_type:
                    weights[0] += hard * 0.6
                    weights.append(hard * 2 * 0.6)
                else:
                    weights[0] += hard * 0.6
                    weights.append(hard * 0.6)
                options.append(material)
            for material, hard in self._resources['gems'].items():
                if material == node_type:
                    weights[0] += hard * 0.4
                    weights.append(hard * 2 * 0.4)
                else:
                    weights[0] += hard * 0.4
                    weights.append(hard * 0.4)
                options.append(material)
            weights[0] *= 3
        else:
            for material, hard in self._resources['metals'].items():
                if material == node_type:
                    weights[0] += hard * 0.4
                    weights.append(hard * 2 * 0.4)
                else:
                    weights[0] += hard * 0.4
                    weights.append(hard * 0.4)
                options.append(material)
            for material, hard in self._resources['gems'].items():
                if material == node_type:
                    weights[0] += hard * 0.6
                    weights.append(hard * 2 * 0.6)
                else:
                    weights[0] += hard * 0.6
                    weights.append(hard * 0.6)
                options.append(material)
            weights[0] *= 3
        if len(options) == 0:
            return None, 0
        return choices(options, weights)[0], choices([1, 2, 3], [3, 2, 1])[0]


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

    def decrease_node_counter(self, count):
        if self._current_node in self._explored_node_counters:
            self._explored_node_counters[self._current_node] -= count
            if self._explored_node_counters[self._current_node] <= 0:
                self._explored_node_counters.pop(self._current_node)
                self._explored_nodes[self._current_node] = True
                self._check_marker_color(self._current_node)

    # Create the map from an explored array
    def create_current_map(self, explored):
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
                    self._explored_node_counters[marked_node] = 4
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
            self._current_path = 'exit'
            # We KNOW that we are on the entrance, and the path to the exit is just the path
            self._path_solutions[ENTRANCE][self._path_nodes[0]] = [self._path_nodes[0]]
            self._path_solutions[EXIT][self._path_nodes[-1]] = list(reversed(self._path_nodes))
            found = self.set_current_node(self._path_nodes[0])
        else:
            self._current_path = 'entrance'
            # We KNOW that we are on the exit, and the path to the entrance is just the reversed path
            self._path_solutions[ENTRANCE][self._path_nodes[0]] = list(self._path_nodes)
            self._path_solutions[EXIT][self._path_nodes[-1]] = [self._path_nodes[-1]]
            found = self.set_current_node(self._path_nodes[-1])
        self._check_path()
        # Remove starting node from arrays
        # self._update_path(self._current_node)
        # Color path
        self._calculate_path()
        return found

    def set_current_node(self, node, show_node=True):
        # Are we just discovering this node?
        found = not self._explored[node]
        if found and show_node:
            self._explored[node] = True
            self._map_data.show_node(*node)
        # Restore previous color
        if self._current_node is not None:
            self._map_data.color_node(*self._current_node, self._current_prev_color)
        self._update_path(node)
        # Set next current
        self._last_node = self._current_node
        self._current_node = node
        if show_node or self._explored[node]:
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
        self._map_data.hide_node(*node)

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
            if not self._explored[shortest_key]:
                self._clear_path()
                return
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
                routes[route_end] = list(reversed(self.solve_path(self._nodes, self._current_node, route_end)))
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
    def solve_path(nodes, start, end):
        x, y = start
        visited = [start]
        travelled = [(0, 0)]

        while (x, y) != end:
            options = []
            if (nodes[(x, y)] & N) == N and travelled[-1] != S and (x, y - 1) not in visited:
                options.append((0, -1))
            if (nodes[(x, y)] & E) == E and travelled[-1] != W and (x + 1, y) not in visited:
                options.append((1, 0))
            if (nodes[(x, y)] & S) == S and travelled[-1] != N and (x, y + 1) not in visited:
                options.append((0, 1))
            if (nodes[(x, y)] & W) == W and travelled[-1] != E and (x - 1, y) not in visited:
                options.append((-1, 0))

            if len(options) == 0:
                dx, dy = travelled.pop()
                x, y = x - dx, y - dy
            else:
                dx, dy = options[randint(0, len(options) - 1)]
                travelled.append((dx, dy))
                x, y = x + dx, y + dy
                visited += [(x, y)]
        # Convert (dx, dy) to (x, y)
        x, y = start
        for index in range(len(travelled)):
            dx, dy = travelled[index]
            travelled[index] = (x + dx, y + dy)
        return travelled[1:-1]  # We don't want to color current node or ending node


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
