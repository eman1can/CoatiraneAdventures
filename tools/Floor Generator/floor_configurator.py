from kivy.lang.builder import Builder
from kivy.app import App
from kivy.properties import DictProperty, ListProperty, NumericProperty, ObjectProperty, StringProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.utils import rgba
from loading.floor import load_array, load_dict
from random import randint, shuffle

# Use Recursive Backtracking to generate maze
N, S, E, W = 1, 2, 4, 8  # 0001 0010 0100 1000
NONE = 0
NS = N | S
NE = N | E
NW = N | W
EW = E | W
ES = E | S
SW = S | W
NSW = NS | W
NSE = NS | E
NEW = NE | W
SEW = ES | W
NSEW = NS | EW


DIR = {(1, 0): W, (0, 1): N, (-1, 0): E, (0, -1): S}


def connections_to_char(connects):
    if connects == NSEW:
        return '┼'
    elif connects == NS:
        return '│'
    elif connects == EW:
        return '─'
    elif connects == ES:
        return '┌'
    elif connects == SW:
        return '┐'
    elif connects == NE:
        return '└'
    elif connects == NW:
        return '┘'
    elif connects == NSE:
        return '├'
    elif connects == NSW:
        return '┤'
    elif connects == SEW:
        return '┬'
    elif connects == NEW:
        return '┴'
    elif connects == N:
        return '╵'
    elif connects == S:
        return '╷'
    elif connects == E:
        return '╶'
    elif connects == W:
        return '╴'


def format_output(b, c):
    directions = {}
    for y in range(len(b)):
        for x in range(len(b[y])):
            if len(c[(x, y)]) == 0:
                continue
            connects = NONE
            for (dx, dy) in c[(x, y)]:
                connects |= DIR[(x - dx, y - dy)]
            b[y][x] = expand_char(connections_to_char(connects))
            directions[(x, y)] = connects
    return b, directions


def walk(v, conn, x, y, s, w, h):
    v[y][x] = 1

    d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]  # Directions
    shuffle(d)

    ds = []
    for (xx, yy) in d:
        if xx < 0 or xx >= w or yy < 0 or yy >= h:
            continue
        if v[yy][xx]:
            continue
        conn[(x, y)].append((xx, yy))
        conn[(xx, yy)].append((x, y))
        return xx, yy
    return False


def expand_char(char):
    if char in ['┼', '─', '┐', '┘', '┤', '┬', '┴', '╴']:
        return '─' + char
    else:
        return ' ' + char


def generate_maze(w):
    h=w

    box = [[' ' for _ in range(w)] for _ in range(h)]

    vis = [[0 for _ in range(w)] for _ in range(h)]

    connections = {}
    for y in range(h):
        for x in range(w):
            connections[(x, y)] = []

    stack = [(randint(0, w - 1), randint(0, h - 1))]
    while len(stack) > 0:
        (x, y) = stack.pop()
        node = walk(vis, connections, x, y, stack, w, h)
        if node:
            stack.append((x, y))
            stack.append(node)
    return format_output(box, connections)


def wrap_box(box):
    new_box = [['' for _ in range(len(box[0]) + 2)] for _ in range(len(box) + 2)]
    for y in range(len(new_box)):
        for x in range(len(new_box[y])):
            if y == 0 and x == 0:
                new_box[y][x] = '┌'
            elif y == 0 and x == len(new_box[y]) - 1:
                new_box[y][x] = '─┐'
            elif y == len(new_box) - 1 and x == 0:
                new_box[y][x] = '└'
            elif y == len(new_box) - 1 and x == len(new_box) - 1:
                new_box[y][x] = '─┘'
            elif y == 0 or y == len(new_box[y]) - 1:
                new_box[y][x] = '──'
            elif x == 0:
                new_box[y][x] = '│'
            elif x == len(new_box) - 1:
                new_box[y][x] = ' │'
            else:
                new_box[y][x] = box[y - 1][x - 1]
    return new_box


def strip_box(box_string):
    rows = box_string.split('\n')[1:-1]
    for index in range(len(rows)):
        rows[index] = rows[index][1:-2]
    return rows


def get_box_from_string(box_string):
    rows = strip_box(box_string)
    size = len(rows)
    box = []
    for y in range(size):
        box.append([])
        for x in range(size):
            box[y].append(rows[y][x * 2:(x + 1) * 2])
    return box


def solve_path(last, start, end, nodes):
    if start == end:
        return [end]
    node = nodes[start]
    if (node & N) == N and last != S:
        path = solve_path(N, (start[0], start[1] - 1), end, nodes)
        if path:
            return [start] + path
    if (node & E) == E and last != W:
        path = solve_path(E, (start[0] + 1, start[1]), end, nodes)
        if path:
            return [start] + path
    if (node & S) == S and last != N:
        path = solve_path(S, (start[0], start[1] + 1), end, nodes)
        if path:
            return [start] + path
    if (node & W) == W and last != E:
        path = solve_path(W, (start[0] - 1, start[1]), end, nodes)
        if path:
            return [start] + path
    return False


kv_string = """
RelativeLayout:
    MazePreview:
        id: maze_preview
        size_hint: 0.7, 1
    RelativeLayout:
        size_hint: 0.3, 1
        pos_hint: {'right': 1}
        RelativeLayout:
            size_hint: 0.9, 0.9
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            Button:
                size_hint: 0.5, 0.05
                pos_hint: {'top': 1}
                text: 'Import'
                on_release: maze_preview.import_maze()
            Button:
                size_hint: 0.5, 0.05
                pos_hint: {'top': 1, 'right': 1}
                text: 'Export'
                on_release: maze_preview.export_maze()
            Label:
                size_hint: 0.5, 0.05
                pos_hint: {'top': 0.95}
                text: 'Size:'
                font_size: '20pt'
            TextInput:
                id: maze_size_input
                size_hint: 0.5, 0.05
                pos_hint: {'top': 0.95, 'right': 1}
                multiline: False
                hint_text: 'size'
                font_size: '20pt'
                text: '18'
            Button:
                size_hint: 1, 0.05
                pos_hint: {'top': 0.9}
                text: 'Generate Maze'
                on_release:
                    maze_preview.data = []
                    maze_preview.maze_size = int(maze_size_input.text)
                    maze_preview.generate_tile_data()
            Label:
                size_hint: 0.5, 0.05
                pos_hint: {'top': 0.85}
                text: 'Entrance:'
                font_size: '20pt'
            Label:
                size_hint: 0.5, 0.05
                pos_hint: {'top': 0.8}
                text: 'Exit:'
                font_size: '20pt'
            TextInput:
                id: entrance_preview
                size_hint: 0.5, 0.05
                pos_hint: {'top': 0.85, 'right': 1}
                multiline: False
                disabled: True
                hint_text: '(x, y)'
                font_size: '20pt'
                text: str(maze_preview.marker_lists['Entrance'])
            TextInput:
                id: exit_preview
                size_hint: 0.5, 0.05
                pos_hint: {'top': 0.8, 'right': 1}
                multiline: False
                disabled: True
                hint_text: '(x, y)'
                font_size: '20pt'
                text: str(maze_preview.marker_lists['Exit'])
            Button:
                size_hint: 1, 0.05
                pos_hint: {'top': 0.75}
                text: 'Generate Path'
                on_release: maze_preview.generate_path()
            RecycleView:
                id: marker_list
                size_hint: 1, 0.7
                viewclass: 'MarkerPreview'
                effect_cls: 'ScrollEffect'
                RecycleGridLayout:
                    size_hint: 1, None
                    height: self.minimum_height
                    cols: 1
                    default_size_hint: 1, None
                    default_height: '25dp'
<MarkerPreview>:
    canvas:
        Color:
            rgba: root.marker_color
        Rectangle:
            size: root.width * 0.25, root.height
            pos: root.width * 0.5, 0
    Label:
        size_hint: 0.5, 1
        text: root.marker_name
    Label:
        size_hint: 0.25, 1
        pos_hint: {'right': 1}
        text: root.marker_count

<MazePreview>:
    RecycleView:
        id: marker_list
        size_hint: 1, 1
        viewclass: 'MazeTile'
        effect_cls: 'ScrollEffect'
        data: root.tile_data
        RecycleGridLayout:
            cols: root.maze_size
            rows: root.maze_size
            default_size_hint: None, None
            default_size: root.height / min(root.maze_size, 30), root.height / min(root.maze_size, 30)
            size_hint: (1, 1) if root.maze_size < 30 else (None, None)
            size: self.minimum_size

<MazeTile>:
    Button:
        opacity: 0.1
        on_release: root.change_marker()
    Label:
        font_size: self.height * 0.7
        font_name: '../../res/fnt/CourierNew'
        text: root.tile
        color: root.color
"""


class MarkerPreview(RelativeLayout):
    marker_color = ListProperty(rgba('#F05F40'))
    marker_name = StringProperty('Marker Name')
    marker_count = StringProperty('')


class MazeTile(RelativeLayout):
    coords = ListProperty([0, 0])
    color = ListProperty(rgba('#FFFFFF'))
    current_marker = StringProperty('None')
    tile = StringProperty('┼')

    update_callback = ObjectProperty(None)

    def change_marker(self):
        markers = ['None'] + list(MARKERS.keys())
        current_index = markers.index(self.current_marker)
        if current_index == len(markers) - 1:
            next_marker = 'None'
        else:
            next_marker = markers[current_index + 1]

        self.update_callback(self.current_marker, next_marker, self.coords)

        self.current_marker = next_marker
        if next_marker == 'None':
            self.color = rgba('#FFFFFF')
        else:
            self.color = rgba(MARKERS[next_marker])


MARKERS = {
    'Entrance': '#0000FF',
    'Exit': '#FF0000',
    'Safe Zone': '#FEDE00',
    'Goblin Spawn': '#91CA75',
    'Kobold Spawn': '#75AC19',
    'Jack Bird Spawn': '#FECA34'
}
PATH_COLOR = '#DA8FBE'


class MazePreview(RelativeLayout):
    nodes = DictProperty({})
    path_nodes = ListProperty([])
    marker_lists = DictProperty({key: [] for key in MARKERS.keys()})

    maze_size = NumericProperty(18)
    tile_data = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._generated_data = None

        self.generate_tile_data()

    def generate_tile_data(self):
        self._generated_data, self.nodes = generate_maze(self.maze_size)

        # Reset path nodes
        self.path_nodes = []
        # Reset marker lists
        self.marker_lists = {key: [] for key in MARKERS.keys()}
        self.update_tile_data()

    def update_tile_data(self):
        tile_data = []
        for row in range(self.maze_size):
            for col in range(self.maze_size):
                new_tile = {'coords': [col, row], 'tile': self._generated_data[row][col], 'update_callback': self.update_marker_list}
                if tuple(new_tile['coords']) in self.path_nodes:
                    new_tile['color'] = rgba(PATH_COLOR)
                for marker_name, marker_list in self.marker_lists.items():
                    if tuple(new_tile['coords']) in marker_list:
                        new_tile['color'] = rgba(MARKERS[marker_name])
                if 'color' not in new_tile:
                    new_tile['color'] = rgba('#FFFFFF')
                tile_data.append(new_tile)
        self.tile_data = tile_data

    def update_marker_list(self, current_list, next_list, node):
        if current_list != 'None':
            self.marker_lists[current_list].remove(tuple(node))
        if next_list != 'None':
            self.marker_lists[next_list].append(tuple(node))
        if next_list in ['Entrance', 'Exit'] or current_list in ['Entrance', 'Exit']:
            self.refresh_stair_list()
        self.refresh_marker_list()

    def refresh_stair_list(self):
        self.parent.ids.entrance_preview.text = str(self.marker_lists['Entrance'])
        self.parent.ids.exit_preview.text = str(self.marker_lists['Exit'])

    def refresh_marker_list(self):
        marker_data = []
        for marker_name, marker_color in MARKERS.items():
            if marker_name == 'Entrance' or marker_name == 'Exit':
                continue
            marker_data.append({'marker_name': marker_name, 'marker_color': rgba(marker_color), 'marker_count': str(len(self.marker_lists[marker_name]))})
        self.parent.ids.marker_list.data = marker_data

    def generate_path(self):
        if len(self.marker_lists['Entrance']) != 1 or len(self.marker_lists['Exit']) != 1:
            print('Too many or too little Entrances or exits')
            return
        entrance_node = tuple(self.marker_lists['Entrance'][0])
        exit_node = tuple(self.marker_lists['Exit'][0])
        self.path_nodes = solve_path(0, entrance_node, exit_node, self.nodes)

        self.update_tile_data()

    def export_maze(self):
        file = open('output.txt', 'w', encoding='utf-8')
        file.write(str(self.nodes) + '\n')
        file.write(str(self.path_nodes) + '\n')
        for marker_name, marker_list in self.marker_lists.items():
            if marker_name == 'Entrance' or marker_name == 'Exit':
                continue
            file.write(str(marker_list) + '\n')
        for row in wrap_box(self._generated_data):
            file.write(''.join(row) + '\n')
        file.close()

    def import_maze(self):
        file = open('input.txt', 'r', encoding='utf-8')
        node_dict = load_dict(file.readline()[:-1])
        path_array = load_array(file.readline()[:-1])
        marker_lists = {}
        marker_lists['Entrance'] = [path_array[0]]
        marker_lists['Exit'] = [path_array[-1]]
        line = file.readline()
        not_map = not line.startswith('┌')
        while not_map:
            marker_name, marker_list = line[:-1].split('#')
            marker_lists[marker_name] = load_array(marker_list)
            line = file.readline()
            not_map = not line.startswith('┌')
        box = get_box_from_string(line + file.read())
        file.close()
        self.nodes = node_dict
        self.path_nodes = path_array
        self.marker_lists = marker_lists
        self._generated_data = box
        self.maze_size = len(box)
        self.parent.ids.maze_size_input.text = str(self.maze_size)
        self.update_tile_data()
        self.refresh_marker_list()
        self.refresh_stair_list()


class FloorConfigurator(App):
    def build(self):
        floor_configurator = Builder.load_string(kv_string)
        marker_data = []
        for marker_name, marker_color in MARKERS.items():
            if marker_name == 'Entrance' or marker_name == 'Exit':
                continue
            marker_data.append({'marker_name': marker_name, 'marker_color': rgba(marker_color), 'marker_count': str(0)})
        floor_configurator.ids.marker_list.data = marker_data
        return floor_configurator


if __name__ == '__main__':
    FloorConfigurator().run()
