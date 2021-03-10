# Standard Library Imports
from random import randint, choices

ENTRANCE_COLOR = '#0000FF'
EXIT_COLOR = '#FF0000'
CURRENT_COLOR = '#93E9BE'
PATH_COLOR = '#DA8FBE'
SAFE_ZONE_COLOR = '#FEDE00'


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

    def __init__(self, floor_id, max_enemies, boss_type, enemies, probabilities, floor_data, path_data, floor_map):
        self._floor_id = floor_id
        self._max_enemies = max_enemies
        self._boss_type = boss_type
        self._enemies = enemies
        self._probabilities = probabilities

        self._floor_data = floor_data
        self._path_data = path_data
        self._entrance = path_data[0]
        self._exit = path_data[-1]

        self._map = Map(floor_map, list(floor_data.keys()), path_data)

    def get_score(self):
        # Floor 1 rec score should be ~ 7
        score = 0
        for enemy in self._enemies:
            print(enemy.get_id(), enemy.get_score())
            score += enemy.get_score()
        return round(score, 0)

    def get_entrance(self):
        return self._entrance

    def get_exit(self):
        return self._exit

    def get_node(self, node):
        return self._floor_data[node]

    def get_node_by_index(self, index):
        return self._path_data[index]

    def get_node_path_index(self, node):
        return self._path_data.index(node)

    def get_nodes(self):
        return self._floor_data

    def get_map_char(self, node):
        return self._map.get_node(self._map.get_full_map(), node)

    def get_floor_map(self):
        return self._map

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

    def generate_enemies(self):
        minimum = int(self._max_enemies * 0.25)
        if not minimum >= 1:
            minimum = 1
        enemies = []
        weights = self._probabilities
        for x in range(randint(minimum, self._max_enemies)):
            enemy = choices(self._enemies, list(weights.values()), k=1)[0]
            enemies.append(enemy.new_instance(self._floor_id))
        return enemies


class Map:
    def __init__(self, full_map, nodes, path_nodes):
        self._width = full_map.index('\n')
        self._size = int((self._width - 4) / 2)

        self._full_map = MapData().create_from_string(full_map.strip())
        self._nodes = nodes
        self._path_nodes = path_nodes

        # Current map progress
        self._explored = {}
        for node in self._nodes:
            self._explored[node] = False
        self._current_map = MapData().create_from_explored_array(self._full_map, self._explored)

        self._entrance = path_nodes[0]
        self._exit = path_nodes[-1]
        self._current = None
        self._current_prev_color = None
        self._safe_zones = []

    def color_entrance(self):
        self.color_node(self._entrance, ENTRANCE_COLOR)

    def color_exit(self):
        self.color_node(self._exit, EXIT_COLOR)

    def set_current(self, node):
        if self._current:
            if self._current_prev_color:
                self.modify_color(self._current, self._current_prev_color)
            else:
                self.color_node(self._current, None)
        self._current_prev_color = self._has_color(node)
        print(node, self._current_prev_color, '→', CURRENT_COLOR)
        if self._current_prev_color:
            self.modify_color(node, CURRENT_COLOR)
        else:
            self.color_node(node, CURRENT_COLOR)
        self._current = node

    def _has_color(self, node):
        x, y = self._current_map.relative_to_abs(*node)
        current = self._current_map.get_node_abs(x, y)
        if '[' in current:
            return current[7:14]
        return None

    def modify_color(self, node, color):
        x, y = self._current_map.relative_to_abs(*node)
        current = self._current_map.get_node_abs(x, y)
        current2 = self._current_map.get_node_abs(x - 1, y)

        current = f'[color={color}' + current[14:]
        current2 = f'[color={color}' + current2[14:]

        self._current_map.set_node_abs(x, y, current)
        self._current_map.set_node_abs(x - 1, y, current2)

    def clear_current(self):
        self._current = None

    def color_node(self, node, color=None):
        # If have color, then modify
        if color is not None and self._has_color(node):
            return self.modify_color(node, color)
        x, y = self._current_map.relative_to_abs(*node)
        current = self._current_map.get_node_abs(x, y)
        current2 = self._current_map.get_node_abs(x - 1, y)
        if color is None:
            current = current[current.index(']') + 1]
            current2 = current2[current2.index(']') + 1]
        else:
            current = f'[color={color}]{current}[/color]'
            current2 = f'[color={color}]{current2}[/color]'

        self._current_map.set_node_abs(x, y, current)
        self._current_map.set_node_abs(x - 1, y, current2)

    def get_full_map(self):
        return self._full_map

    def get_map(self):
        return self._current_map

    def get_map_section(self, node, radius):
        return self.get_map().get_section(*node, radius)

    def get_node(self, map, node):
        return map.get_node(*node)

    def set_node(self, map, node, new_char):
        map.set_node(*node, new_char)

    def unlock_path_map(self):
        for node in self._path_nodes:
            self.show_node(node)
            self.color_node(node, PATH_COLOR)
        self.color_entrance()
        self.color_exit()

    def unlock_full_map(self):
        for node in self._nodes:
            self.show_node(node)
        for node in self._path_nodes:
            self.color_node(node, PATH_COLOR)
        self.color_entrance()
        self.color_exit()

    def show_node(self, node):
        if not self._explored[node]:
            self._explored[node] = True
            self._show_node(node)
            if node == self._entrance:
                self.color_entrance()
            if node == self._exit:
                self.color_exit()
            return True
        return False

    def hide_node(self, node):
        self._explored[node] = False
        self._hide_node(node)

    def _show_node(self, node):
        x, y = self._current_map.relative_to_abs(*node)
        self._current_map.set_node_abs(x, y, self._full_map.get_node_abs(x, y))
        self._current_map.set_node_abs(x - 1, y, self._full_map.get_node_abs(x - 1, y))

    def _hide_node(self, node):
        x, y = self._current_map.relative_to_abs(*node)
        self._current_map.set_node_abs(x, y, ' ')
        self._current_map.set_node_abs(x - 1, y, ' ')


class MapData:
    def __init__(self):
        self._data = []
        self._width = None
        self._size = None

    def create_from_string(self, string):
        self._width = string.index('\n')
        self._size = int((self._width - 4) / 2)

        if string is not None:
            for row_string in string.split('\n'):
                row = []
                for char in row_string:
                    row.append(char)
                self._data.append(row)
        return self

    def get_size(self):
        return self._width, self._size

    def create_from_explored_array(self, full_map, explored):
        self._width, self._size = full_map.get_size()

        # Copy the outline
        for y in range(self._size + 3):
            row = []
            for x in range(self._width):
                if x == 0 or y == 0 or x == self._width - 1 or y == self._size + 2:
                    row.append(full_map.get_node_abs(x, y))
                else:
                    row.append(' ')
            self._data.append(row)
        # Copy the explored sections
        for y in range(self._size):
            for x in range(self._size):
                if explored[(x, y)]:
                    ax, ay = self.relative_to_abs(x, y)
                    self.set_node_abs(ax, ay, full_map.get_node_abs(ax, ay))
                    self.set_node_abs(ax-1, ay, full_map.get_node_abs(ax-1, ay))
        return self

    def get_node(self, x, y):
        x, y = self.relative_to_abs(x, y)
        return self.get_node_abs(x, y)

    def get_node_abs(self, x, y):
        return self._data[y][x]

    def set_node(self, x, y, new_char):
        x, y = self.relative_to_abs(x, y)
        self.set_node_abs(x, y, new_char)

    def set_node_abs(self, x, y, new_char):
        self._data[y][x] = new_char

    def __str__(self):
        string = ''
        for row in self._data:
            for char in row:
                string += char
            string += '\n'
        return string[:-1]

    def get_rows(self, node, radius=5):
        rows = []
        for row in self.get_section(*node, radius).split('\n'):
            rows.append(''.join(row) + '\n')
        return rows

    def relative_to_abs(self, x, y):
        return x * 2 + 2, y + 1

    def relative_size_to_abs(self, x, y):
        return x * 2, y

    def get_section(self, x, y, radius):
        x, y = self.relative_to_abs(x, y)
        rx, ry = self.relative_size_to_abs(radius, radius)

        left, top = max(1, x - rx), max(1, y - ry)
        right, bottom = min(self._width - 1, x + rx), min(self._size + 2, y + ry)
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

        print(x, y, rx, ry, radius)
        print('TB', top, '→', bottom)
        print('LR', left, '→', right)

        string = '\n┌'
        for x in range(dx):
            string += '─'
        string += '┐\n'
        for row in self._data[top:bottom]:
            string += '│'
            for char in row[left:right]:
                string += char
            string += '│\n'
        string += '└'
        for x in range(dx):
            string += '─'
        string += '┘'
        return string
