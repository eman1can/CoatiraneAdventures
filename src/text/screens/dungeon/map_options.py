from game.floor import ENTRANCE, EXIT, SAFE_ZONES
from refs import END_OPT_C, OPT_C, Refs
from text.screens.screen_names import BACK, MAP_OPTIONS


def get_screen(console, screen_data):
    display_text, _options = '', {}

    floor_map = Refs.gc.get_floor_data().get_floor().get_map()
    enabled = floor_map.get_enabled()
    path = floor_map.layer_active('path')
    current_path = floor_map.get_current_path()

    layers = []
    explored_nodes, explored_counters = floor_map.get_node_exploration()
    for layer, nodes in floor_map.get_markers().items():
        if layer in [ENTRANCE, EXIT, SAFE_ZONES]:
            layers.append(layer)
            continue
        count = 0
        for node in nodes:
            if explored_nodes[node]:
                count += 1
        if count > 0:
            layers.append(layer)

    if screen_data == 'change_destination':
        display_text += '\n\tChoose a destination to map to.\n'
        for index, layer in enumerate(list(layers)):
            name = layer.replace('_', ' ').title()
            if name == current_path:
                display_text += f'\n\t[s]{OPT_C}{index + 1}:{END_OPT_C}[/s] {name} - Current'
            else:
                display_text += f'\n\t{OPT_C}{index + 1}:{END_OPT_C} {name}'
                _options[str(index + 1)] = 'change_destination#' + layer
        display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} Back\n'
        _options['0'] = BACK
        return display_text, _options
    elif screen_data == 'change_radius':
        display_text += '\n\tChoose a radius.\n'
        for index, radius in enumerate(range(5, 9)):
            if radius == floor_map.get_radius():
                display_text += f'\n\t[s]{OPT_C}{index + 1}:{END_OPT_C}[/s] {radius} - Current'
            else:
                display_text += f'\n\t{OPT_C}{index + 1}:{END_OPT_C} {radius}'
                _options[str(index + 1)] = f'change_radius#{radius}'
        display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} Back\n'
        _options['0'] = BACK
        return display_text, _options

    display_text += '\n\tMap Options\n'
    display_text += f'\n\t{OPT_C}1:{END_OPT_C} Map Enabled'
    display_text += ' - TRUE' if enabled else ' - FALSE'
    display_text += f'\n\t{OPT_C}2:{END_OPT_C} Map Radius - {floor_map.get_radius()}'
    display_text += f'\n\t{OPT_C}3:{END_OPT_C} Path to Destination'
    display_text += ' - ON' if path else ' - OFF'
    display_text += f'\n\t{OPT_C}4:{END_OPT_C} Current Destination - '
    display_text += current_path.replace('_', ' ').upper()
    display_text += '\n\n\tMap Layers'

    for index, layer in enumerate(layers):
        name = layer.replace('_', ' ').title()
        display_text += f'\n\t\t{OPT_C}{index + 5}:{END_OPT_C} {name}'
        active = floor_map.layer_active(layer)
        display_text += ' - ON' if active else ' - OFF'
        _options[str(index + 4)] = f'toggle#{layer}#{not active}'

    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} Back\n'
    _options['0'] = BACK
    _options['1'] = f'toggle#map#{not enabled}'
    _options['2'] = 'change_radius'
    _options['3'] = f'toggle#path#{not path}'
    _options['4'] = 'change_destination'

    return display_text, _options


def handle_action(console, action):
    floor_map = Refs.gc.get_floor_data().get_floor().get_map()

    if action.startswith('toggle#'):
        layer, active = action.split('#')[1:]
        if layer == 'map':
            floor_map.set_enabled(active)
        else:
            floor_map.set_layer_active(layer, active)
    elif action.startswith('change_destination#'):
        new_path = action.split('#')[1]
        floor_map.set_current_path(new_path)
    elif action.startswith('change_radius#'):
        new_radius = action.split('#')
        floor_map.set_radius(int(new_radius))
    else:
        console.set_screen(f'{MAP_OPTIONS}:{action}', True)
        return
    console.set_screen(MAP_OPTIONS, False)
