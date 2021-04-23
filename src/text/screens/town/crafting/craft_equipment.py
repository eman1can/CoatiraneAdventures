from refs import END_OPT_C, OPT_C, Refs
from text.screens.screen_names import BACK, CRAFT_EQUIPMENT_MATERIAL, CRAFT_EQUIPMENT
from text.screens.town import get_town_header

NAMES = ['Durability', 'Health', 'Mana', 'Physical Attack', 'Magical Attack', 'Defense', 'Weight']


def get_screen(console, screen_data):
    console.header_callback = get_town_header
    _options = {'0': BACK}
    print(screen_data)
    recipe_id, material_ids = screen_data.split('#', 1)
    recipe = Refs.gc['recipes'][recipe_id]

    equipment = Refs.gc['equipment'][recipe.get_item_id()]
    display_text = f'\n\tWhat materials would you like to use in the {equipment.get_name()}?'

    materials = []
    for material_id in material_ids.split('#'):
        if material_id != 'none':
            materials.append(Refs.gc['materials'][material_id])
        else:
            materials.append(None)

    material_names = []
    can_craft = materials[0] is not None
    if materials[0] is not None:
        equipment_name = f'{materials[0].get_name()} {equipment.get_name()}'
    else:
        equipment_name = equipment.get_name()
    if not equipment.is_tool():
        material_names += ['Defining', 'First Sub Material', 'Second Sub Material']
        if materials[1] is not None:
            equipment_name = materials[1].get_name() + ' ' + equipment_name
            if materials[2] is not None:
                equipment_name = materials[2].get_name() + ' ' + equipment_name
        for material in materials[3:]:
            can_craft &= material is not None
    else:
        material_names += ['Defining']

    for material_type in list(recipe.get_ingredients().keys())[1:]:
        material_names.append(material_type.title())

    display_text += '\n'
    for index, material_name in enumerate(material_names):
        if materials[index] is None:
            display_text += f'\n\t{material_name}: None'
        else:
            display_text += f'\n\t{material_name}: {materials[index].get_name()}'

    display_text += f'\n\n\t{equipment_name}'
    if not equipment.is_tool():
        if materials[0] is None:
            display_text += f'\n\t\tElement: None\n'
        else:
            display_text += f'\n\t\tElement: {materials[0].get_element()}\n'
        weights = equipment.get_weights()
    else:
        weights = [1, 0, 0, 0, 0, 0, 0]

    names, minimums, maximums = [], [], []
    max_name_length = max_minimum_length = max_maximum_length = 0

    defining_material_count = list(recipe.get_ingredients().values())[0]

    material_counts = list(recipe.get_ingredients().values())
    minimum_hardness = 0
    maximum_hardness = 0
    if not equipment.is_tool():
        if materials[0] is not None:
            if materials[1] is not None:
                if materials[2] is not None:
                    material_counts.insert(1, int(material_counts[0] * 0.2))
                    material_counts.insert(1, int(material_counts[0] * 0.2))
                    material_counts[0] *= 0.6
                    minimum_hardness = materials[0].get_hardness() * defining_material_count * 0.6 + materials[1].get_hardness() * defining_material_count * 0.2 + materials[2].get_hardness() * defining_material_count * 0.2
                    maximum_hardness = materials[0].get_max_hardness() * defining_material_count * 0.6 + materials[1].get_max_hardness() * defining_material_count * 0.2 + materials[2].get_max_hardness() * defining_material_count * 0.2
                else:
                    material_counts.insert(1, int(material_counts[0] * 0.2))
                    material_counts[0] *= 0.8
                    minimum_hardness = materials[0].get_hardness() * defining_material_count * 0.8 + materials[1].get_hardness() * defining_material_count * 0.2
                    maximum_hardness = materials[0].get_max_hardness() * defining_material_count * 0.8 + materials[1].get_max_hardness() * defining_material_count * 0.2
            else:
                minimum_hardness = materials[0].get_hardness() * defining_material_count
                maximum_hardness = materials[0].get_max_hardness() * defining_material_count
    elif materials[0] is not None:
        minimum_hardness = materials[0].get_hardness() * defining_material_count
        maximum_hardness = materials[0].get_max_hardness() * defining_material_count

    minimum_hardness /= defining_material_count
    maximum_hardness /= defining_material_count
    maximum_hardness *= 1.5

    names.append('Hardness')
    max_name_length = len(names[-1])
    minimums.append(Refs.gc.format_number(round(minimum_hardness, 1)))
    max_minimum_length = len(minimums[-1])
    maximums.append(Refs.gc.format_number(round(maximum_hardness, 1)))
    max_maximum_length = len(maximums[-1])

    divider = 0
    for material_count in recipe.get_ingredients().values():
        divider += material_count

    for index, weight in enumerate(weights):
        if weight == 0:
            continue
        names.append(NAMES[index])
        if len(names[-1]) > max_name_length:
            max_name_length = len(names[-1])

        minimum = 0
        maximum = 0
        for material in materials:
            if material is None:
                continue
            minimum += material.get_all_weights()[index] * weight * minimum_hardness
            maximum += material.get_all_weights()[index] * weight * maximum_hardness
        minimum /= divider
        maximum /= divider
        maximum *= 1.5

        minimums.append(Refs.gc.format_number(round(minimum, 1)))
        if len(minimums[-1]) > max_minimum_length:
            max_minimum_length = len(minimums[-1])
        maximums.append(Refs.gc.format_number(round(maximum, 1)))
        if len(maximums[-1]) > max_maximum_length:
            max_maximum_length = len(maximums[-1])

    for index, name in enumerate(names):
        display_text += '\n\t\t' + f'{name}: '.ljust(max_name_length + 2) + minimums[index].ljust(max_minimum_length) + ' ~ ' + maximums[index].ljust(max_maximum_length)

    if not equipment.is_tool():
        display_text += '\n\t\tEffects:'
        printed_effect = False
        if materials[0] is not None and materials[0].get_effect() != 'none':
            printed_effect = True
            display_text += f'\n\t\t\t{materials[0].get_effect()}'
        for material in materials[1:]:
            if material is None:
                continue
            if material.get_effect() != 'none':
                display_text += f'\n\t\t\t{material.get_effect()}'
                printed_effect = True
        if not printed_effect:
            display_text += f'\n\t\t\tNo Effects'

    display_text += '\n'
    material_item_names = []
    material_item_numbers = []
    material_item_cost_numbers = []
    max_material_item_name = 0
    max_material_item_number = 0
    max_material_item_cost = 0
    for index, material in enumerate(materials):
        if material is None:
            continue
        material_count = Refs.gc.get_inventory().get_item_count(material.get_processed_id())
        item = Refs.gc.find_item(material.get_processed_id())
        need_count = material_counts[index]
        material_item_names.append(item.get_name() + ': ')
        if len(material_item_names[-1]) > max_material_item_name:
            max_material_item_name = len(material_item_names[-1])
        material_item_numbers.append(Refs.gc.format_number(int(material_count)))
        if len(material_item_numbers[-1]) > max_material_item_number:
            max_material_item_number = len(material_item_numbers[-1])
        material_item_cost_numbers.append(Refs.gc.format_number(int(material_count - need_count)))
        if len(material_item_cost_numbers[-1]) > max_material_item_cost:
            max_material_item_cost = len(material_item_cost_numbers[-1])

    for index, item_name in enumerate(material_item_names):
        display_text += '\n\t' + item_name.ljust(max_material_item_name) + material_item_numbers[index].ljust(max_material_item_number) + ' → ' + material_item_cost_numbers[index].ljust(max_material_item_cost)

    display_text += '\n'
    for index, material in enumerate(materials):
        if index == 2 and not equipment.is_tool():
            if materials[1] is None:
                continue
        if material is not None:
            display_text += f'\n\t{OPT_C}{index + 1}:{END_OPT_C} Change {material_names[index]}'
        else:
            display_text += f'\n\t{OPT_C}{index + 1}:{END_OPT_C} Add {material_names[index]}'
        _options[str(index + 1)] = f'{CRAFT_EQUIPMENT_MATERIAL}:{screen_data}#{index}'
    print(_options)
    display_text += '\n'

    if can_craft:
        display_text += f'\n\n\t{OPT_C}{len(materials) + 1}:{END_OPT_C} Craft item'
        _options[str(len(materials) + 1)] = f'craft_item#{screen_data}'
    else:
        display_text += f'\n\n\t[s]{OPT_C}{len(materials) + 1}:{END_OPT_C} Craft item[/s]'

    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} Back\n'
    return display_text, _options


def handle_action(console, action):
    if action.startswith('craft_item'):
        recipe_id, material_ids = action.split('#', 2)[1:]

        recipe = Refs.gc['recipes'][recipe_id]
        equipment = Refs.gc['equipment'][recipe.get_item_id()]
        materials = []
        material_items = []
        for material_id in material_ids.split('#'):
            if material_id != 'none':
                materials.append(Refs.gc['materials'][material_id])
                material_items.append(Refs.gc.find_item(materials[-1].get_processed_id()))
            else:
                material_items.append(None)
                materials.append(None)

        # Craft the item and add it to the inventory
        metadata = {'hash': None, 'material_id': materials[0].get_id()}
        if not equipment.is_tool():
            if materials[1] is not None:
                metadata['sub_material1_id'] = materials[1].get_id()
                if materials[2] is not None:
                    metadata['sub_material2_id'] = materials[2].get_id()
                else:
                    metadata['sub_material2_id'] = None
            else:
                metadata['sub_material1_id'] = None
                metadata['sub_material2_id'] = None

        equipment_item = equipment.new_instance(metadata)
        Refs.gc.get_inventory().add_item(equipment_item.get_id(), 1, equipment_item.get_metadata())

        # Remove Material costs from the inventory
        material_counts = list(recipe.get_ingredients().values())
        if not equipment.is_tool():
            if materials[0] is not None:
                if materials[1] is not None:
                    if materials[2] is not None:
                        material_counts.insert(1, int(material_counts[0] * 0.2))
                        material_counts.insert(1, int(material_counts[0] * 0.2))
                        material_counts[0] *= 0.6
                    else:
                        material_counts.insert(1, int(material_counts[0] * 0.2))
                        material_counts[0] *= 0.8
        for index, material_count in enumerate(material_counts):
            print(material_items[index].get_name(), material_count)
            Refs.gc.get_inventory().remove_item(material_items[index].get_id(), material_count)
    else:
        console.set_screen(action, True)


def get_craft_equipment_item(recipe, index, current_text, page_name, page_num):
    require_string = ''
    for ingredient, count in recipe.get_ingredients().items():
        require_string += f'{count}x {ingredient}\n\t\t'
    item = Refs.gc['equipment'][recipe.get_item_id()]

    action_string = f'{page_name}:{recipe.get_item_id()}'
    material_length = len(recipe.get_ingredients())
    if not item.is_tool():
        material_length += 2
    for _ in range(material_length):
        action_string += '#none'
    return f'\n\t{OPT_C}{index}:{END_OPT_C} {item.get_name()} x{recipe.get_item_count()}\n\t\t' + require_string[:-3], action_string
