from random import randint

from game.floor import ENTRANCE, EXIT, SAFE_ZONES
from game.floor_data import DIRECTIONS_FROM_STRING, E, LEFT, N, OPPOSITE, RIGHT, S, STRING_DIRECTIONS, W
from refs import BLUE_C, END_OPT_C, OPT_C, RED_C, Refs, SEA_FOAM_C

COUNT_TO_STRING = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']


def get_plain_size(string):
    parts = string.split('[')
    size = 0
    for part in parts:
        if ']' in part:
            size += len(part.split(']')[1])
        else:
            size += len(part)
    return size


def center(string, length, size):
    count = size - length
    for x in range(count):
        if x % 2 == 0:
            string += ' '
        else:
            string = ' ' + string
    return string


def ljust(string, length, size):
    count = size - length
    for x in range(count):
        string += ' '
    return string


def rjust(string, length, size):
    count = size - length
    for x in range(count):
        string = ' ' + string
    return string


def get_tunnel_descriptions(floor_data):
    floor_map = floor_data.get_floor().get_map()
    facing, options = floor_data.get_directions()
    display_string, _options = '', {}

    compass = Refs.gc.in_inventory('compass')

    # Currently facing direction
    if compass:
        if facing == N:
            display_string = f'\n\tCurrently facing: North\n'
        elif facing == E:
            display_string = f'\n\tCurrently facing: East\n'
        elif facing == S:
            display_string = f'\n\tCurrently facing: South\n'
        elif facing == W:
            display_string = f'\n\tCurrently facing: West\n'
    # Get possible options
    display_string += '\n\t' + floor_data.get_descriptions()
    display_string += '\n\tWhat do you choose to do?'

    # Ascend or descend
    if floor_map.is_marker(EXIT):
        display_string += f'\n\n\t{OPT_C}0:{END_OPT_C} Descend to the next floor'
        _options['0'] = 'dungeon_battle_descend'
    elif floor_map.is_marker(ENTRANCE):
        display_string += f'\n\n\t{OPT_C}0:{END_OPT_C} Turn back and ascend.'
        _options['0'] = 'dungeon_battle_ascend'

    # Walk in different directions
    display_string += '\n'

    # If we have compass, order = N E S W
    # Else, order = FACING, !FACING, LEFT, RIGHT
    if compass:
        for index, direction in {8: 'North', 4: 'West', 6: 'East', 2: 'South'}.items():
            if direction in options:
                display_string += f'\n\t{OPT_C}{index}:{END_OPT_C} Proceed {direction}, {floor_data.get_basic_direction(direction)} down the hallway.'
                _options[str(index)] = f'dungeon_battle_{direction}'
    else:
        for index, direction_number in {3: facing, 4: OPPOSITE[facing], 5: LEFT[facing], 6: RIGHT[facing]}.items():
            direction = STRING_DIRECTIONS[direction_number]
            if direction in options:
                display_string += f'\n\t{OPT_C}{index}:{END_OPT_C} Proceed {floor_data.get_basic_direction(direction)} down the hallway.'
                _options[str(index)] = f'dungeon_battle_{direction}'
    display_string += '\n'
    return display_string, _options


def get_extra_actions(floor_data):
    text, options = '', {}

    compass = Refs.gc.in_inventory('compass')

    if compass:
        inventory_index = 5
        safe_zone_index = 1
        action_index1 = 7
        action_index2 = 9
    else:
        inventory_index = 1
        safe_zone_index = 7
        action_index1 = 8
        action_index2 = 9

    text += f'\n\t{OPT_C}{inventory_index}:{END_OPT_C} Inventory\n'
    options[str(inventory_index)] = 'inventory_battle'

    safe_zone = floor_data.get_floor().get_map().is_marker(SAFE_ZONES)
    activated_safe_zone = floor_data.is_activated_safe_zone()

    if safe_zone and not activated_safe_zone:
        text += f'\n\n\t{OPT_C}{safe_zone_index}:{END_OPT_C} Create Safe Zone'
        options[str(safe_zone_index)] = 'dungeon_battle_create_safe_zone'

    if activated_safe_zone:
        text += f'\n\n\t{OPT_C}{safe_zone_index}:{END_OPT_C} Rest'
        options[str(safe_zone_index)] = 'dungeon_battle_rest'

    adventurers_able = False
    for character in floor_data.get_characters():
        if character.can_take_action():
            adventurers_able = True

    pickaxe = False  # Refs.gc.has_pickaxe()
    shovel = False  # Refs.gc.has_shovel()
    if adventurers_able:
        if pickaxe:
            text += f'\n\n\t{OPT_C}{action_index1}:{END_OPT_C} Inspect the dungeon walls. (Mine for resource)'
            options[str(action_index1)] = 'dungeon_battle_mine'
        if shovel:
            text += f'\n\n\t{OPT_C}{action_index2}:{END_OPT_C} Inspect the dungeon environment. (Dig and Scrounge for resource)'
            options[str(action_index2)] = 'dungeon_battle_dig'

    return text, options


def get_battle_display(floor_data):
    battle_data = floor_data.get_battle_data()

    option_index = 1
    _options = {}

    enemy_rows = []
    character_rows = []
    effect_rows = []

    # Display Enemies
    for enemy in battle_data.get_enemies():
        name = enemy.get_name()
        level = f'Level {enemy.get_level()}'
        count = 18 * enemy.get_battle_health() / enemy.get_health()
        health_string = ''
        for index in range(18):
            if index < count:
                health_string += '='
            else:
                health_string += ' '
        health_string = f'[{health_string}]'
        if enemy.is_dead():
            enemy_rows.append((f'[s]{name}[/s]', len(name)))
            enemy_rows.append((f'[s]{level}[/s]', len(level)))
            enemy_rows.append((f'[s]{RED_C}{health_string}{END_OPT_C}[/s]', len(health_string)))
        else:
            enemy_rows.append((name, len(name)))
            enemy_rows.append((level, len(level)))
            enemy_rows.append((f'{RED_C}{health_string}{END_OPT_C}', len(health_string)))
        enemy_rows.append(('', 0))
        enemy_rows.append(('', 0))

    # Display Characters
    # Make sure that if we don't have enough special moves, to reduce the amount
    special_count = 0
    special_possible = battle_data.get_special_count()
    for character in battle_data.get_characters():
        if character.get_selected_skill().is_special():
            special_count += 1
            if special_count > special_possible:
                character.select_skill(0)

    for character in battle_data.get_characters():
        name = character.get_name()
        count = 18 * character.get_battle_health() / character.get_health()
        health_string = ''
        for index in range(18):
            if index < count:
                health_string += '='
            else:
                health_string += ' '
        health_string = f'[{health_string}]'
        mana_string = ''
        count = 18 * character.get_battle_mana() / character.get_mana()
        for index in range(18):
            if index < count:
                mana_string += '='
            else:
                mana_string += ' '
        mana_string = f'[{mana_string}]'
        skill_name = f'Sel. Skill: {character.get_selected_skill().get_name()}'
        if not battle_data.get_state().startswith('battle_select') and not character.is_dead():
            character_rows.append((f'{OPT_C}{option_index}:{END_OPT_C} {name}', len(name) + 3))
            _options[str(option_index)] = f'dungeon_battle_encounter_select_show_{option_index - 1}'
            option_index += 1
        else:
            if character.is_dead():
                character_rows.append((f'[s]{name}[/s]', len(name)))
            else:
                character_rows.append((f'{name}', len(name)))
        if character.is_dead():
            character_rows.append((f'[s]{RED_C}{health_string}{END_OPT_C}[/s]', 20))
            character_rows.append((f'[s]{BLUE_C}{mana_string}{END_OPT_C}[/s]', 20))
            character_rows.append(('', 0))
            character_rows.append((f'[s]{skill_name}[/s]', len(skill_name)))
        else:
            character_rows.append((f'{RED_C}{health_string}{END_OPT_C}', 20))
            character_rows.append((f'{BLUE_C}{mana_string}{END_OPT_C}', 20))
            character_rows.append(('', 0))
            character_rows.append((skill_name, len(skill_name)))
        character_rows.append(('', 0))
        character_rows.append(('', 0))
    # Display Status Effects
    for character in battle_data.get_characters():
        status_effects = character.get_status_effects()
        for effect_list in status_effects.values():
            for effect in effect_list:
                pass

    # Combine all of the rows into one string
    goblin_center, goblin_justify, character_center, character_justify, effect_center, effect_justify = 25, 30, 35, 40, 20, 25

    screen_string = '\n'

    special_string = ''
    special_width = goblin_justify + character_justify + effect_justify - 2
    if battle_data.get_special_amount() > 0:
        special_amount = special_width * battle_data.get_special_amount() / 25
    else:
        special_amount = battle_data.get_special_amount()

    for index in range(special_width, 0, -1):
        if index % 19 == 0 and index != 0:
            special_string += '|'
            continue
        if index < special_amount:
            special_string += '='
        else:
            special_string += ' '
    screen_string += f'\t{SEA_FOAM_C}[b][{special_string}] {battle_data.get_special_count()}[/b]{END_OPT_C}\n\n'

    for index in range(max(len(enemy_rows), len(character_rows), len(effect_rows))):
        screen_string += '\t'
        # Add the enemy strings
        if index < len(enemy_rows) - 1:
            string, string_length = enemy_rows[index]
            screen_string += ljust(center(string, string_length, goblin_center), max(goblin_center, string_length), goblin_justify)
        else:
            screen_string += ''.center(goblin_center).ljust(goblin_justify)
        # Add the character strings
        if index < len(character_rows) - 1:
            string, string_length = character_rows[index]
            screen_string += rjust(center(string, string_length, character_center), max(character_center, string_length), character_justify)
        else:
            screen_string += ''.center(character_center).ljust(character_justify)
        # Add the effect strings
        if index < len(effect_rows) - 1:
            string, string_length = effect_rows[index]
            screen_string += ljust(center(string, string_length, effect_center), max(effect_center, string_length), effect_justify)
        else:
            screen_string += ''.center(effect_center).ljust(effect_justify)
        screen_string += '\n'

    # Add Actions
    screen_string += '\n'
    if battle_data.get_state().startswith('battle_select'):
        index = int(battle_data.get_state()[len('battle_select_'):])
        character = battle_data.get_characters()[index]
        selected_skill = character.get_selected_skill()
        for skill in character.get_skills():
            print(skill.get_name(), skill.is_special())
            if skill == selected_skill:
                screen_string += f'\n\t{OPT_C}[s]{option_index}: {skill.get_name()}[/s]{END_OPT_C}'
                option_index += 1
                continue
            if skill.is_special():
                # Do we have any special gauge points?
                special_blocked = battle_data.get_special_count() < 0
                if not special_blocked:
                    # If we have gauge points, are they selected already?
                    possible = battle_data.get_special_count()
                    for character in battle_data.get_characters():
                        if character.get_selected_skill().is_special():
                            possible -= 1
                    if possible == 0:
                        special_blocked = True
                if special_blocked:
                    screen_string += f'\n\t{OPT_C}[s]{option_index}: {skill.get_name()}[/s]{END_OPT_C}'
                    option_index += 1
                    continue
            screen_string += f'\n\t{OPT_C}{option_index}:{END_OPT_C} {skill.get_name()}'
            _options[str(option_index)] = f'dungeon_battle_encounter_select_{index}_{option_index}'
            option_index += 1
    else:
        _options['0'] = 'dungeon_battle_encounter_attack'
        _options[str(option_index)] = 'inventory0page'
        screen_string += f'\n\t{OPT_C}{0}:{END_OPT_C} Attack'
        screen_string += f'\n\t{OPT_C}{option_index}:{END_OPT_C} Inventory'
    screen_string += '\n'
    # Display Battle Log - Will be on a separate scroll
    Refs.app.scroll_widget.ids.label.text = battle_data.get_battle_log()
    Refs.app.scroll_widget.opacity = 1

    return screen_string, _options


def dungeon_battle(console):
    """
    Dungeon Battle will consist of a few main screens.
    The first is the mvoement screen, that will display the current position,
    the options available for movement and the action options.
    For an action option, a user can inspect the local enviroment and the walls for ore.
    They should both reduce the health just a tiny bit. (1-2 pooints) to discurage from
    an inspection at every node.
    Aside from that, you have an encounter screen that will show the enemies showing up,
    and the activation of assist skills.
    Then you have the main fight screen which will show enemy healths, character healths
    and ability and skill options.
    You also have the battle result screen that will show xp and items gained
    from fights, and the final result screens which will show all items gained on the floor.
    You also have the boss transition screen, although that will go back through dungeon main.

    """
    # The first thing to do during the dungeon battle would be to get the current status
    # From the floor data
    # If we are in an encounter, show battle screen, else show movement screen based on current position

    floor_data = Refs.gc.get_floor_data()

    if not floor_data.is_in_encounter():
        display_string, _options = get_tunnel_descriptions(floor_data)
        tool_string, tool_options = get_extra_actions(floor_data)

        _options.update(tool_options)

        compass = Refs.gc.in_inventory('compass')

        if compass:
            map_index = 3
        else:
            map_index = 2

        # If we have compass, then
        # 0 - Ascend / Descend
        # 2 - South
        # 4 - West
        # 6 - East
        # 8 - North
        # 3 - Map Options
        # 5 - Inventory
        # 1 - Create Safe Zone / Rest
        # 7 - Mine
        # 9 - Dig
        # Else
        # 0 - Ascend / Descend
        # 3 - Forwards
        # 4 - Backwards
        # 5 - Left
        # 6 - Right
        # 2 - Map Options
        # 1 - Inventory
        # 7 - Extra Action 1
        # 8 - Extra Action 2
        # 9 - Extra Action 3

        # Get map and display it
        floor_map = floor_data.get_floor().get_map()
        if floor_map.get_enabled():
            display_string_rows = (display_string + tool_string).split('\n')
            map_rows = floor_map.get_rows()
            display_string = ''

            for x in range(len(display_string_rows)):
                if x < len(map_rows):
                    row = display_string_rows[x].replace('\t', '    ')
                    display_string += ljust(row, get_plain_size(row), 140) + '[font=CourierNew]' + map_rows[x] + '\n'
                else:
                    display_string += display_string_rows[x] + '\n'

            if len(display_string_rows) < len(map_rows):
                for x in range(len(display_string_rows), len(map_rows)):
                    display_string += ljust('', 0, 140) + '[font=CourierNew]' + map_rows[x] + '\n'
                display_string += ljust('', 0, 140) + f'       {OPT_C}{map_index}:{END_OPT_C} Map Options'
            else:
                display_string += ljust('', 0, 140) + f'       {OPT_C}{map_index}:{END_OPT_C} Map Options'
        else:
            display_string = display_string + f'\n\t{OPT_C}{map_index}:{END_OPT_C} Map Options\n' + tool_string
        _options[str(map_index)] = 'dungeon_battle_map_options'
        return display_string, _options
    else:
        display_string = '\n\t' + floor_data.get_descriptions()
        _options = {}

        if floor_data.get_encounter_state() == 'start':
            display_string += f'\n\n\tYou have encountered {COUNT_TO_STRING[len(floor_data.get_battle_data().get_enemies())]} enemies.\n\tYou need to fight!\n\n\t{OPT_C}0:{END_OPT_C} Start fight!\n'
            _options['0'] = 'dungeon_battle_encounter_start'
            return display_string, _options
        elif floor_data.get_encounter_state().startswith('battle'):
            return get_battle_display(floor_data)
        # In encounter options
    display_string += '\n'
    return display_string, _options


def dungeon_result(console):
    """
    List all of the defeated enemies
    List the dropped items
    Show the decreases in health & mana
    """
    if console.get_current_screen().endswith('win'):
        floor_data = Refs.gc.get_floor_data()
        battle_data = floor_data.get_battle_data()

        display_string = '\n\tYou survived the encounter!\n\tDefeated:'
        counts = {}
        for enemy in battle_data.get_enemies():
            if enemy.get_name() not in counts:
                counts[enemy.get_name()] = 0
            counts[enemy.get_name()] += 1
        for enemy, count in counts.items():
            display_string += f'\n\t\t{enemy} x {count}'
        display_string += '\n\n\tItems Dropped:'
        for item, count in battle_data.get_dropped_items().items():
            display_string += f'\n\t\t{item.get_name()} x {count}'

        display_string += '\n\n'
        pre_battle = battle_data.get_pre_battle_status()
        for character in battle_data.get_characters():
            char_id = character.get_id()
            health = character.get_health()
            mana = character.get_mana()
            if not character.is_dead():
                display_string += f'\t{character.get_name()} - Health: {pre_battle[char_id + "_health"]} / {health} → {character.get_battle_health()} / {health} - Mana: {pre_battle[char_id + "_mana"]} / {mana} → {character.get_battle_mana()} / {mana}\n'
            else:
                display_string += f'\t{character.get_name()} - Health: {pre_battle[char_id + "_health"]} / {health} - Mana: {pre_battle[char_id + "_mana"]} / {mana} → Incapacitated\n'
        display_string += f'\n\t{OPT_C}{0}:{END_OPT_C} Continue\n'
        _options = {'0': 'dungeon_battle_end_encounter'}

        Refs.app.scroll_widget.ids.label.text = battle_data.get_battle_log()
        Refs.app.scroll_widget.opacity = 1
    elif console.get_current_screen().endswith('loss'):
        # floor_data = Refs.gc.get_floor_data()
        # battle_data = floor_data.get_battle_data()

        display_string = '\n\tYou were defeated!\n\tYou will be restored to your last save point at the start of the dungeon.\n\tSupport characters are an excellent way to boost your strength as well as giving your characters\n\tequipment and ' \
                         'upgrading their status boards.\n\n\tBetter luck next time, my friend.\n'
        display_string += f'\n\t{OPT_C}{0}:{END_OPT_C} Continue\n'
        _options = {'0': 'dungeon_battle_restore_save'}
    elif console.get_current_screen().endswith('ascend'):
        floor_data = Refs.gc.get_floor_data()
        if floor_data.get_floor().get_id() > 1:
            return show_locked_dungeon_main()
        else:
            display_string = '\n\tYou successfully escaped the dungeon!\n\n\t'
            enemy_rows = []
            items_gained = []
            for enemy, count in floor_data.get_killed().items():
                enemy_rows.append(f'{enemy} x {count}')
            for item, count in floor_data.get_gained_items().items():
                items_gained.append(f'{item.get_name()} x {count}')
            if len(enemy_rows) == 0:
                enemy_rows.append('None'.center(25))
            if len(items_gained) == 0:
                items_gained.append('None'.center(25))
            display_string += 'Monsters Killed'.center(25) + 'Items Gained'.center(25) + '\n'
            for x in range(max(len(enemy_rows), len(items_gained))):
                if x < len(enemy_rows):
                    display_string += '\t' + enemy_rows[x].ljust(25)
                else:
                    display_string += '\t' + ''.ljust(25)
                if x < len(items_gained):
                    display_string += items_gained[x]
                display_string += '\n'
            display_string += f'\n\n\t{OPT_C}{0}:{END_OPT_C} Continue\n'
            _options = {'0': 'dungeon_result_experience'}
    elif console.get_current_screen().endswith('experience'):
        display_string = '\n\tYou successfully escaped the dungeon!\n\n'
        char_rows = {}
        increases = Refs.gc.get_floor_data().get_increases()
        STAT_WIDTH = 11
        for character in Refs.gc.get_current_party():
            if character is None:
                continue
            rows = [character.get_name().split(' ')[0]]
            char_increases = increases[character.get_id()]
            if char_increases[0] == 0:
                rows.append(f'{character.get_health()}')
            else:
                rows.append(f'{character.get_health()} → {character.get_health() + char_increases[0]}')
            if char_increases[1] == 0:
                rows.append(f'{character.get_mana()}')
            else:
                rows.append(f'{character.get_mana()} → {character.get_mana() + char_increases[1]}')
            if char_increases[2] == 0:
                rows.append(f'{character.get_strength()}')
            else:
                rows.append(f'{character.get_strength()} → {character.get_strength() + char_increases[2]}')
            if char_increases[3] == 0:
                rows.append(f'{character.get_magic()}')
            else:
                rows.append(f'{character.get_magic()} → {character.get_magic() + char_increases[3]}')
            if char_increases[4] == 0:
                rows.append(f'{character.get_endurance()}')
            else:
                rows.append(f'{character.get_endurance()} → {character.get_endurance() + char_increases[4]}')
            if char_increases[5] == 0:
                rows.append(f'{character.get_agility()}')
            else:
                rows.append(f'{character.get_agility()} → {character.get_agility() + char_increases[5]}')
            if char_increases[6] == 0:
                rows.append(f'{character.get_dexterity()}')
            else:
                rows.append(f'{character.get_dexterity()} → {character.get_dexterity() + char_increases[6]}')
            char_rows[character.get_id()] = rows
            character.increase_health(char_increases[0])
            character.increase_mana(char_increases[1])
            character.increase_strength(char_increases[2])
            character.increase_magic(char_increases[3])
            character.increase_endurance(char_increases[4])
            character.increase_agility(char_increases[5])
            character.increase_dexterity(char_increases[6])
        labels = ['    ', 'HP. ', 'MP. ', 'Str.', 'Mag.', 'End.', 'Agi.', 'Dex.']
        for index in range(8):
            display_string += f'\t{labels[index]} '
            for character_id in list(char_rows.keys())[:8]:
                display_string += char_rows[character_id][index].center(STAT_WIDTH)
            display_string += '\n'
        if len(char_rows.keys()) > 8:
            for index in range(8):
                display_string += f'\t{labels[index]} '
                for character_id in list(char_rows.keys())[8:]:
                    display_string += char_rows[character_id][index].center(STAT_WIDTH)
                display_string += '\n'
        display_string += f'\n\n\t{OPT_C}{0}:{END_OPT_C} Continue\n'
        _options = {'0': 'dungeon_main'}
    else:
        return show_locked_dungeon_main()
    return display_string, _options


def dungeon_battle_action(console, action):
    """
    The logistics behind the action processing for dungeon battle is likely immense, so we call this function.

    - We can proceed down a hallway and check for events
    -   We need to check for encounter trigger every movement
    -   Upon reaching the exit node, trigger a boss preparation screen and battle.
    - We can handle a harvesting action, and is likely to cause a larger encounter
    - We can handle an ascend or descend action, which call the result screen and display results
    - We can handle a battle action, a battle result
    """
    action = action[len('dungeon_battle_'):]
    if action.startswith('start'):
        Refs.gc.set_next_floor(bool(action[6:]))
        Refs.gc.save_game()
    if action == 'ascend':
        Refs.gc.get_floor_data().get_floor().get_map().clear_current_node()
        # Keep items in inventory
        # Keep items used
        # Keep exploration
        # Clear the current value on the map
        console.set_screen('dungeon_result_ascend')
        return
    elif action == 'descend':
        pass
    elif action == 'end_encounter':
        Refs.gc.get_floor_data().end_encounter()
        Refs.app.scroll_widget.opacity = 0
    elif action == 'restore_save':
        # Remove gained items from inventory
        floor_data = Refs.gc.get_floor_data()
        for item, count in floor_data.get_gained_items().items():
            Refs.gc.remove_from_inventory(item.get_id(), count)
        for item, count in floor_data.get_battle_data().get_dropped_items().items():
            Refs.gc.remove_from_inventory(item.get_id(), count)
        # Remove gained status points from characters
        # Add back used items to inventory
        # Remove explored map data
        floor_map = floor_data.get_floor().get_map()
        for node in floor_data.get_explored():
            floor_map.hide_node(node)
        floor_map.clear_current_node()
        console.set_screen('dungeon_main')
        return
    elif action == 'North' or action == 'East' or action == 'South' or action == 'West':
        floor_data = Refs.gc.get_floor_data()
        # print('Go ', action)
        floor_data.progress_by_direction(DIRECTIONS_FROM_STRING[action])

        # On floor 1, there are 47 nodes to the next floor.
        # I want people to encounter maybe 5-6 roaving hordes of monsters.
        # Therefore, a 0.15% Chance is decent, I think

        # if randint(1, 100) <= 15:
        #     floor_data.generate_encounter()

    elif action.startswith('encounter'):
        action = action[len('encounter_'):]
        if action == 'start':
            Refs.gc.get_floor_data().get_battle_data().progress_encounter()
        elif action == 'battle':
            Refs.gc.get_floor_data().get_battle_data().progress_encounter()
        elif action == 'attack':
            result = Refs.gc.get_floor_data().get_battle_data().make_turn()
            if result is not None:
                Refs.app.scroll_widget.opacity = 0
                Refs.gc.get_floor_data().get_battle_data().progress_encounter()
                if result:
                    console.set_screen('dungeon_result_win')
                else:
                    console.set_screen('dungeon_result_loss')
                return
        elif action.startswith('select_'):
            if action.startswith('select_show_'):
                Refs.gc.get_floor_data().get_battle_data().set_state(f'battle_select_{action[len("select_show_"):]}')
            else:
                character_index, select_index = action[len("select_"):].split('_')
                battle_data = Refs.gc.get_floor_data().get_battle_data()
                skill_index = int(select_index)
                if skill_index == 1:
                    skill_index = 0
                else:
                    skill_index += 1
                battle_data.get_characters()[int(character_index)].select_skill(skill_index)
                battle_data.set_state('battle')
    elif action == 'create_safe_zone':
        floor_data = Refs.gc.get_floor_data()
        floor_data.activate_safe_zone()

        # Random character takes the action
        index = randint(0, len(floor_data.get_characters()) - 1)
        character = floor_data.get_characters()[index]
        character.take_action()
    elif action == 'rest':
        floor_data = Refs.gc.get_floor_data()
        for character in floor_data.get_characters():
            character.rest()
        floor_data.decrease_safe_zones()
    elif action == 'mine':
        floor_data = Refs.gc.get_floor_data()
        index = randint(0, len(floor_data.get_characters()) - 1)
        character = floor_data.get_characters()[index]
        character.take_action()
        console.set_screen(f'dungeon_mine_result_{character.get_id()}')
        return
    elif action == 'dig':
        floor_data = Refs.gc.get_floor_data()
        index = randint(0, len(floor_data.get_characters()) - 1)
        character = floor_data.get_characters()[index]
        character.take_action()
        console.set_screen(f'dungeon_dig_result_{character.get_id()}')
        return
    elif action == 'map_options':
        console.set_screen('map_options')
        return
    console.set_screen('dungeon_battle')


def dungeon_mine_result(console):
    display_string, _options = '', {}
    character_id = console.get_current_screen()[len('dungeon_mine_result_'):]
    character = Refs.gc.get_char_by_id(character_id)

    display_string += '\n\t' + character.get_name() + ' mined as hard as they could '
