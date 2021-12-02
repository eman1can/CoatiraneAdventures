from game.crafting_queue import CRAFTING_LEVELS, CRAFT_SOFT_ALLOY, CRAFT_HARD_ALLOY, LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4, PROCESS_HARD_MATERIAL, PROCESS_SOFT_MATERIAL
from game.crafting_recipe import ALLOY, EQUIPMENT, ITEM, PROCESS, Recipe

ITEM_DESIGNATION = 'I'
PROCESS_DESIGNATION = 'P'
ALLOY_DESIGNATION = 'A'
EQUIPMENT_DESIGNATION = 'E'

DESIGNATIONS = [
    ITEM_DESIGNATION,
    PROCESS_DESIGNATION,
    ALLOY_DESIGNATION,
    EQUIPMENT_DESIGNATION
]


def print_crafting_type(crafting_type):
    crafting_type |= 1 << 21
    bin_string = bin(crafting_type)[-21:]
    type_string = bin_string[-7:]
    for x in range(7):
        print(bin_string[x * 2:(x + 1) * 2], end=' ')
    print(type_string)


def load_crafting_recipe_chunk(chunk, loader, program_type, callbacks):
    recipe_info, ingredients = chunk.split('\n')
    recipe_designation, recipe_info = recipe_info.split(',', 1)
    recipe_type = DESIGNATIONS.index(recipe_designation)

    ingredients_list = {}
    for ingredient in ingredients.split(','):
        item_id, count = ingredient.split('#')
        ingredients_list[item_id] = int(count)

    output_id, recipe_parts = recipe_info.split(',', 1)

    if recipe_type == ITEM:
        output_count, crafting_level, crafting_time = recipe_parts.split(',')
        crafting_level, crafting_time = int(crafting_level), float(crafting_time)
        crafting_type = (1 << ITEM) | crafting_level
    elif recipe_type == PROCESS or recipe_type == ALLOY:
        output_count, crafting_time = recipe_parts.split(',')
        crafting_time = float(crafting_time)
        crafting_type = 0
        craft_type = 0

        recipe_material = None
        for material in loader.get('materials').values():
            if material.get_processed_id() == output_id:
                recipe_material = material
                break
        if recipe_material == None:
            raise Exception('Cannot find recipe material!')

        if recipe_type == PROCESS:
            if recipe_material.is_soft():
                craft_type = PROCESS_SOFT_MATERIAL
                crafting_type |= 1 << craft_type
            else:
                craft_type = PROCESS_HARD_MATERIAL
                crafting_type |= 1 << craft_type
        elif recipe_type == ALLOY:
            if recipe_material.is_soft():
                craft_type = CRAFT_SOFT_ALLOY
                crafting_type |= 1 << craft_type
            else:
                craft_type = CRAFT_HARD_ALLOY
                crafting_type |= 1 << craft_type

        material_hardness = recipe_material.get_hardness()
        if recipe_material.is_soft():
            if material_hardness <= 2.0:
                crafting_type |= LEVEL_1 << CRAFTING_LEVELS[craft_type]
            elif 2.0 < material_hardness <= 5.5:
                crafting_type |= LEVEL_2 << CRAFTING_LEVELS[craft_type]
            elif 5.5 < material_hardness <= 8.75:
                crafting_type |= LEVEL_3 << CRAFTING_LEVELS[craft_type]
            else:
                crafting_type |= LEVEL_4 << CRAFTING_LEVELS[craft_type]
        elif recipe_material.is_hard():
            if material_hardness <= 3.0:
                crafting_type |= LEVEL_1 << CRAFTING_LEVELS[craft_type]
            elif 3.0 < material_hardness <= 8.0:
                crafting_type |= LEVEL_2 << CRAFTING_LEVELS[craft_type]
            elif 8.0 < material_hardness <= 10.5:
                crafting_type |= LEVEL_3 << CRAFTING_LEVELS[craft_type]
            else:
                crafting_type |= LEVEL_4 << CRAFTING_LEVELS[craft_type]
    elif recipe_type == EQUIPMENT:
        crafting_time = float(recipe_parts)
        crafting_type, output_count = 0, 1
    else:
        raise Exception('Invalid Recipe type!')

    print(output_id, end=' ')
    print_crafting_type(crafting_type)

    recipe = Recipe(recipe_type, output_id, output_count, crafting_type, crafting_time, ingredients_list)
    loader.append('recipes', output_id, recipe)

    for callback in callbacks:
        if callback is not None:
            callback()
