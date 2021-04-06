from random import randint

from refs import END_OPT_C, OPT_C, Refs
from text.screens.screen_names import DUNGEON_BATTLE, DUNGEON_EXPERIENCE_RESULT, DUNGEON_HARVEST_RESULT, DUNGEON_MAIN, DUNGEON_RESULT, INVENTORY_BATTLE


def get_screen(console, screen_data):
    display_text, _options = '', {}

    if screen_data == 'loss':
        display_text += '\n\tYou were defeated!\n\tYou will be restored to your last save point at the start of the dungeon.\n\tSupport characters are an excellent way to boost your strength as well as giving your characters\n\tequipment and ' \
                         'upgrading their status boards.\n\n\tBetter luck next time, my friend.\n'
        display_text += f'\n\t{OPT_C}{0}:{END_OPT_C} Continue\n'
        _options['0'] = 'restore_save'
        return display_text, _options

    floor_data = Refs.gc.get_floor_data()
    battle_data = floor_data.get_battle_data()

    if screen_data == 'win':
        display_text += '\n\tYou survived the encounter!\n\tDefeated:'

        counts = {}
        for enemy in battle_data.get_enemies():
            if enemy.get_name() not in counts:
                counts[enemy.get_name()] = 0
            counts[enemy.get_name()] += 1
        for enemy, count in counts.items():
            display_text += f'\n\t\t{enemy} x {count}'

        display_text += '\n\n'
        pre_battle = battle_data.get_pre_battle_status()

        for character in battle_data.get_characters():
            character.take_action(Refs.gc.get_stamina_weight() + 1)
            char_id = character.get_id()
            health = character.get_health()
            mana = character.get_mana()
            if not character.is_dead():
                display_text += f'\t{character.get_name()} - Health: {pre_battle[char_id + "_health"]} / {health} → {round(character.get_battle_health(), 0)} / {health} - Mana: {pre_battle[char_id + "_mana"]} / {mana} → {character.get_battle_mana()} / {mana}\n'
            else:
                display_text += f'\t{character.get_name()} - Health: {pre_battle[char_id + "_health"]} / {health} - Mana: {pre_battle[char_id + "_mana"]} / {mana} → Incapacitated\n'

        _options['0'] = 'end_encounter'
        display_text += f'\n\t{OPT_C}0:{END_OPT_C} Continue\n'

        if Refs.gc.get_inventory().has_harvesting_knife():
            display_text += f'\n\t{OPT_C}1:{END_OPT_C} Harvest Materials'
            display_text += f'\n\t{OPT_C}2:{END_OPT_C} Inventory\n'

            _options['1'] = DUNGEON_HARVEST_RESULT
            _options['2'] = f'{INVENTORY_BATTLE}:0'
        else:
            display_text += f'\n\t[s]{OPT_C}1:{END_OPT_C} Harvest Materials[/s]\n'

        Refs.app.scroll_widget.ids.label.text = battle_data.get_battle_log()
        Refs.app.scroll_widget.opacity = 1
    elif screen_data == 'ascend':
        display_text += '\n\tYou successfully escaped the dungeon!\n\n\t'
        enemy_rows = []
        items_gained = []
        for enemy, count in floor_data.get_killed().items():
            enemy_rows.append(f'{enemy} x {count}')
        for item, count in floor_data.get_gained_items().items():
            items_gained.append(f'{item.get_name()} x {count}')
            Refs.gc.get_inventory().add_item(item.get_id(), count)
        if len(enemy_rows) == 0:
            enemy_rows.append('None'.center(25))
        if len(items_gained) == 0:
            items_gained.append('None'.center(25))
        items_gained.sort()
        enemy_rows.sort()
        display_text += 'Monsters Killed'.center(25) + 'Items Gained'.center(25) + '\n'
        for x in range(max(len(enemy_rows), len(items_gained))):
            if x < len(enemy_rows):
                display_text += '\t' + enemy_rows[x].ljust(25)
            else:
                display_text += '\t' + ''.ljust(25)
            if x < len(items_gained):
                display_text += items_gained[x]
            display_text += '\n'
        display_text += f'\n\n\t{OPT_C}{0}:{END_OPT_C} Continue\n'
        _options['0'] = DUNGEON_EXPERIENCE_RESULT
    return display_text, _options


def handle_action(console, action):
    floor_data = Refs.gc.get_floor_data()

    if action == 'end_encounter':
        floor_data.end_encounter()
        Refs.app.scroll_widget.opacity = 0
        console.set_screen(DUNGEON_BATTLE)
        return
    elif action == 'restore_save':
        floor_map = floor_data.get_floor().get_map()

        for node in floor_data.get_explored():
            floor_map.hide_node(node)

        floor_id = str(floor_data.get_floor().get_id())
        save = Refs.gc['save']
        floor_map.load_node_exploration(save['map_node_data'][floor_id], save['map_node_counters'][floor_id])

        floor_map.clear_current_node()
        Refs.app.scroll_widget.opacity = 0
        Refs.gc.reset_floor_data()
        console.set_screen(DUNGEON_MAIN)
        return
    elif action == DUNGEON_HARVEST_RESULT:
        current_harvesting_knife = Refs.gc.get_inventory().get_current_harvesting_knife()
        if current_harvesting_knife is None:
            console.error_time = 2.5
            console.error_text = 'You have no harvesting knife selected!'
            return
    console.set_screen(action)
