from random import randint

from refs import END_OPT_C, OPT_C, Refs
from text.screens.screen_names import DUNGEON_BATTLE


def get_screen(console, screen_data):
    display_text, _options = '', {'0': 'end_encounter'}
    counts = {}
    item_counts = {}

    floor_data = Refs.gc.get_floor_data()
    battle_data = floor_data.get_battle_data()
    display_text += '\n\tMaterial Harvest Result:'

    for enemy in battle_data.get_enemies():
        if enemy not in counts:
            counts[enemy] = 0
        counts[enemy] += 1

    knife = Refs.gc.get_inventory().get_current_harvesting_knife()
    knife.remove_durability(Refs.gc.get_random_wear_amount())

    character = floor_data.get_able_characters()[randint(0, len(floor_data.get_able_characters()) - 1)]
    character.take_action(Refs.gc.get_stamina_weight() + 1)
    floor_data.increase_stat(character.get_id(), 2, Refs.gc.get_random_stat_increase())

    for enemy, count in counts.items():
        display_text += f'\n\t\t{enemy.get_name()} x {count}:'
        for _ in range(count):
            drops = Refs.gc['enemies'][enemy.get_id()].generate_drop(enemy.get_boost(), knife.get_hardness())
            if len(drops) == 0:
                display_text += f'\n\t\t\tNo items were dropped.'
            for (drop_id, drop_count) in drops:
                item = Refs.gc.find_item(drop_id)
                if item not in item_counts:
                    item_counts[item] = 0
                item_counts[item] += drop_count
                display_text += f'\n\t\t\t{item.get_name()} x {drop_count}'

    display_text += '\n\n\tAll Items Dropped:'
    for item, count in item_counts.items():
        display_text += f'\n\t\t{item.get_name()} x {count}'
    battle_data.set_dropped_items(item_counts)
    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} Continue\n'

    return display_text, _options


def handle_action(console, action):
    Refs.gc.get_floor_data().end_encounter()
    Refs.app.scroll_widget.opacity = 0
    console.set_screen(DUNGEON_BATTLE)

