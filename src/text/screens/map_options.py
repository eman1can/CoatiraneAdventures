from refs import END_OPT_C, OPT_C, Refs


def map_options(console):
    display_text, _options = '', {}

    floor_map = Refs.gc.get_floor_data().get_floor().get_map()
    enabled = floor_map.get_enabled()
    path = floor_map.layer_active('path')
    current_path = floor_map.get_current_path()
    layers = floor_map.get_markers().keys()

    if console.get_current_screen() == 'map_options_change_destination':
        display_text += '\n\tChoose a destination to map to.\n'
        for index, layer in enumerate(['exit', 'entrance'] + list(layers)):
            name = layer.replace('_', ' ').title()
            if name == current_path:
                display_text += f'\n\t[s]{OPT_C}{index + 3}:{END_OPT_C}[/s] {name} - Current'
            else:
                display_text += f'\n\t{OPT_C}{index + 3}:{END_OPT_C} {name}'
                _options[str(index + 3)] = 'map_options_change_destination_' + layer
        display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} Back\n'
        _options['0'] = 'back'
        return display_text, _options

    display_text += '\n\tMap Options\n'
    display_text += f'\n\t{OPT_C}1:{END_OPT_C} Map Enabled'
    display_text += ' - TRUE' if enabled else ' - FALSE'
    display_text += f'\n\t{OPT_C}2:{END_OPT_C} Path to Destination'
    display_text += ' - ON' if path else ' - OFF'
    display_text += f'\n\t{OPT_C}3:{END_OPT_C} Current Destination - '
    display_text += current_path.replace('_', ' ').upper()
    display_text += '\n\n\tMap Layers'

    if len(layers) == 0:
        display_text += '\n\t\tNo Layers'
    else:
        for index, layer in enumerate(layers):
            name = layer.replace('_', ' ').title()
            display_text += f'\n\t\t{OPT_C}{index + 4}:{END_OPT_C} {name}'
            active = floor_map.layer_active(layer)
            display_text += ' - ON' if active else ' - OFF'
            _options[str(index + 4)] = f'map_options_toggle_{layer}_{not active}'

    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} Back\n'
    _options['0'] = 'back'
    _options['1'] = f'map_options_toggle_map_{not enabled}'
    _options['2'] = f'map_options_toggle_path_{not path}'
    _options['3'] = 'map_options_change_destination'

    return display_text, _options
