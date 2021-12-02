from game.market import PriceTracker

STATIC_PRICE = 'PS'
DYNAMIC_PRICE = 'PD'
PRICE_TEMPLATE = 'T'


def get_item(loader, item_id):
    if item_id in loader.get('items'):
        return loader.get('items')[item_id]
    else:
        raise Exception(f"The Item {item_id} could not be located")


def load_market_price_chunk(chunk, loader, program_type, callbacks):
    parts = chunk.split(',')
    for index in range(len(parts)):
        parts[index] = parts[index].strip()
    type = parts[0]

    if type == PRICE_TEMPLATE:
        base_id, min_price, base_price, max_price, elasticity = parts[1:]
        for item in loader.get('items').values():
            if base_id not in item.get_id():
                continue
            tracker = PriceTracker(item.get_category(), float(min_price), float(base_price), float(max_price), elasticity)
            loader.append('market_prices', item.get_id(), tracker)
    elif type == STATIC_PRICE:
        item_id, price = parts[1:]
        item = get_item(loader, item_id)
        tracker = PriceTracker(item.get_category(), float(price), float(price), float(price))
        loader.append('market_prices', item_id, tracker)
    elif type == DYNAMIC_PRICE:
        item_id, min_price, base_price, max_price, elasticity = parts[1:]
        item = get_item(loader, item_id)
        tracker = PriceTracker(item.get_category(), float(min_price), float(base_price), float(max_price), elasticity)
        loader.append('market_prices', item_id, tracker)
    else:
        raise Exception(f"This Market Price Type does not exist: {type}")

    for callback in callbacks:
        if callback is not None:
            callback()
