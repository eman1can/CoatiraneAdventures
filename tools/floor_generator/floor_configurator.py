from kivy.lang.builder import Builder
from kivy.app import App
from kivy.properties import DictProperty, ListProperty, NumericProperty, ObjectProperty, StringProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.utils import rgba
from loading.floor import load_array, load_dict
from tools.floor_generator.floor_generator import generate_maze, get_box_from_string, solve_path, wrap_box

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
            default_size: root.height / root.maze_size, root.height / root.maze_size

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
    'Iron Spawn': '#FF5733',
    'Goblin Spawn': '#91CA75'
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
        for marker_name, marker_list in self.marker_lists.items():
            if marker_name == 'Entrance':
                marker_lists[marker_name] = [path_array[0]]
            elif marker_name == 'Exit':
                marker_lists[marker_name] = [path_array[-1]]
            else:
                marker_lists[marker_name] = load_array(file.readline()[:-1])
        box = get_box_from_string(file.read())
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
