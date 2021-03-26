from game.crafting_recipe import EQUIPMENT, EquipmentRecipe, ITEM, ItemRecipe


def load_crafting_recipe_chunk(chunk, loader, program_type, callbacks):
    recipe_info, ingredients = chunk.split('\n')
    if recipe_info.startswith('item'):
        output_id, perk_requirement, craft_type, output_count = recipe_info[len('item,'):].split(',')
        type = ITEM
    elif recipe_info.startswith('equipment'):
        output_id = recipe_info[len('equipment,'):]
        type = EQUIPMENT
    ingredient_list = ingredients.split(',')
    list = {}
    for ingredient in ingredient_list:
        item_id, count = ingredient.split('#')
        list[item_id] = int(count)
    if type == ITEM:
        recipe = ItemRecipe(output_id, output_count, perk_requirement, craft_type, list)
    elif type == EQUIPMENT:
        recipe = EquipmentRecipe(output_id, list)

    loader.append('recipes', output_id, recipe)
    for callback in callbacks:
        if callback is not None:
            callback()
