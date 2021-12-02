from game.item import DropItem, FloorMap, Item, Ingredient, ShopItem
from refs import Refs

GENERAL_ITEM = 'G'
SHOP_ITEM = 'S'
FLOOR_MAP_TYPE = 'F'
DROP_ITEM = 'D'
ITEM_TYPE = 'T'
INGREDIENT = 'I'
PROCESSED = 'P'


def load_item_chunk(chunk, loader, program_type, callbacks):
    if chunk.startswith('#'):
        for callback in callbacks:
            if callback is not None:
                callback()
        return

    metadata, data = chunk.split('\n', 1)

    if metadata.startswith(GENERAL_ITEM):
        item_id, visible_after_floor, name = metadata[3:].split(', ')

        item = Item(item_id, name, data, int(visible_after_floor))
        loader.append('items', item_id, item)
    elif metadata.startswith(SHOP_ITEM):
        item_id, visible_after_floor, name, shop_category, can_own_multiple = metadata[3:].split(', ')
        can_own_multiple = can_own_multiple != 'single'
        unlock_requirement, description = data.split('\n', 1)

        item = ShopItem(item_id, name, description, int(visible_after_floor), shop_category, can_own_multiple)
        item.set_unlock_requirement(unlock_requirement)
        loader.append('items', item_id, item)
    elif metadata.startswith(DROP_ITEM):
        item_id, visible_after_floor, name = metadata[3:].split(', ')

        item = DropItem(item_id, name, data, int(visible_after_floor))
        loader.append('items', item_id, item)
    elif metadata.startswith(INGREDIENT):
        item_id, visible_after_floor, name = metadata[3:].split(', ')

        item = Ingredient(item_id, name, data, int(visible_after_floor))
        loader.append('items', item_id, item)
    elif metadata.startswith(FLOOR_MAP_TYPE):
        for floor_id in range(1, len(loader.get('floors')) + 1):
            item_id_base, name = metadata[3:].split(', ')
            unlock_requirement, description_base = data.split('\n', 1)

            visible_after_floor = floor_id
            shop_category = f'floor_{floor_id}'
            item_id = f'{item_id_base}_{shop_category}'
            if unlock_requirement != 'none':
                unlock_requirement += f'_{shop_category}'
            string = Refs.gc.number_to_name(floor_id)
            description = description_base.format(string)

            item = FloorMap(item_id, name, description, int(visible_after_floor), shop_category)
            item.set_unlock_requirement(unlock_requirement)
            loader.append('items', item_id, item)
    elif metadata.startswith(ITEM_TYPE):
        output_type, material_type = metadata[3:].split(', ')
        material_type = int(material_type)
        id_parts, name_parts, description_base = data.split('\n', 2)
        id_prefix, id_base, id_suffix = id_parts.split(',')
        id_prefix, id_base, id_suffix = id_prefix.strip(), id_base.strip(), id_suffix.strip()
        name_prefix, name_suffix = name_parts.split(',')
        name_prefix, name_suffix = name_prefix.strip(), name_suffix.strip()

        for material in loader.get('materials').values():
            if not material.is_type(material_type):
                continue

            if id_base not in material.get_id():
                continue

            item_id = f'{material.get_id()}'
            if id_prefix != '':
                item_id = f'{id_prefix}_{item_id}'
            if id_suffix != '':
                item_id += f'_{id_suffix}'

            name = f'{material.get_name()}'
            if name_prefix != '':
                name = f'{name_prefix} {name}'
            if name_suffix != '':
                name += f' {name_suffix}'
            description = description_base.format(material.get_name())

            if output_type == DROP_ITEM:
                item = DropItem(item_id, name, description, int(1))
                loader.append('items', item_id, item)
            elif output_type == PROCESSED:
                item = DropItem(item_id, name, description, int(1))
                loader.append('items', item_id, item)
            elif output_type == INGREDIENT:
                item = Ingredient(item_id, name, description, int(1))
                loader.append('items', item_id, item)
            else:
                raise Exception(f"UnImplemented - Item Type: {output_type}")
    else:
        raise Exception(f"UnImplemented - {metadata}")

    for callback in callbacks:
        if callback is not None:
            callback()
