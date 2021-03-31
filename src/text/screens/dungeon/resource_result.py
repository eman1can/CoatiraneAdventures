from refs import END_OPT_C, OPT_C, Refs
from text.screens.screen_names import BACK


def get_screen(console, screen_data):
    display_string, _options = '', {}

    skew_type, character_id = screen_data.split('#')
    character = Refs.gc.get_char_by_id(character_id)
    floor = Refs.gc.get_floor_data().get_floor()

    node = None
    for resource_type, resource_list in floor.get_resources().items():
        for resource in resource_list:
            if floor.get_map().is_marker(resource):
                node = resource

    if skew_type == 'mine':
        resource, count = floor.generate_resource(node, True)
    else:
        resource, count = floor.generate_resource(node, False)

    if count == 0:
        if skew_type == 'mine':
            display_string += '\n\t' + character.get_name() + ' mined as hard as they could but found nothing.'
        else:
            display_string += '\n\t' + character.get_name() + ' dug as hard as they could but found nothing.'
    else:
        # We found something!
        if resource in floor.get_resources()['metals']:
            if skew_type == 'mine':
                display_string += '\n\t' + character.get_name() + f' mined as hard as they could and found {resource.title()} Ore!'
            else:
                display_string += '\n\t' + character.get_name() + f' dug as hard as they could and found {resource.title()} Ore!'
            display_string += '\n\n\tItems Gained:'
            display_string += f'\n\t\tRaw {resource.title()} Ore x {count}'
            Refs.gc.get_floor_data().add_gained_items(f'{resource}_ore', count)
        else:
            if skew_type == 'dig':
                display_string += '\n\t' + character.get_name() + f' mined as hard as they could and found {resource.title()} Gems!'
            else:
                display_string += '\n\t' + character.get_name() + f' dug as hard as they could and found {resource.title()} Gems!'
            display_string += '\n\n\tItems Gained:'
            display_string += f'\n\t\tRaw {resource.title()} Gems x {count}'
            Refs.gc.get_floor_data().add_gained_items(f'raw_{resource}', count)
    display_string += f'\n\n\t{OPT_C}0:{END_OPT_C} Continue\n'
    return display_string, {'0': BACK}


def handle_action(console, action):
    pass
