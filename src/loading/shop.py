from game.item import DropItem, Item, Ingredient


def load_shop_item_chunk(chunk, loader, program_type, callbacks):
    metadata, data = chunk.split('\n', 1)
    if metadata.startswith('S, '):
        # Shop items
        item_id, name, shop_category, purchase_type, price = metadata[3:].split(', ')
        unlock_requirement, description = data.split('\n', 1)

        item = Item(item_id, name, description, shop_category, purchase_type, price)
        item.set_unlock_requirement(unlock_requirement)
        loader.append('items', item_id, item)
    elif metadata.startswith('D, '):
        item_id, name, purchase_type, min_sell_price, max_sell_price = metadata[3:].split(', ')
        description = data

        item = DropItem(item_id, name, description, purchase_type, min_sell_price, max_sell_price)
        loader.append('drop_items', item_id, item)
    else:
        item_id, name, purchase_type, min_sell_price, max_sell_price = metadata[3:].split(', ')
        description = data

        item = Ingredient(item_id, name, description, purchase_type, min_sell_price, max_sell_price)
        loader.append('items', item_id, item)

    for callback in callbacks:
        if callback is not None:
            callback()
