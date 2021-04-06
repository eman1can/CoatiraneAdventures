from math import ceil, floor
from random import choices, randint

from game.effect import COUNTER_TYPES, STAT_TYPES
from game.floor import ENTRANCE, EXIT, SAFE_ZONES
from game.floor_data import DIRECTIONS_FROM_STRING, E, LEFT, N, OPPOSITE, RIGHT, S, STRING_DIRECTIONS, W
from refs import BLUE_C, END_OPT_C, OPT_C, RED_C, Refs, SEA_FOAM_C
from text.screens.common_functions import center, get_plain_size, ljust
from text.screens.screen_names import DUNGEON_BATTLE, DUNGEON_MAIN, DUNGEON_MAIN_LOCKED, DUNGEON_RESOURCE_RESULT, DUNGEON_RESULT, INVENTORY_BATTLE, MAP_OPTIONS

COUNT_TO_STRING = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']


def get_tunnel_descriptions(floor_data):
    floor_map = floor_data.get_floor().get_map()
    facing, options = floor_data.get_directions()
    display_string, _options = '', {}

    compass = Refs.gc.get_inventory().has_item('compass')

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
        _options['0'] = f'descend'
    elif floor_map.is_marker(ENTRANCE):
        display_string += f'\n\n\t{OPT_C}0:{END_OPT_C} Turn back and ascend.'
        _options['0'] = f'ascend'

    # Walk in different directions
    display_string += '\n'

    # If we have compass, order = N E S W
    # Else, order = FACING, !FACING, LEFT, RIGHT
    if compass:
        for index, direction in {8: 'North', 4: 'West', 6: 'East', 2: 'South'}.items():
            if direction in options:
                display_string += f'\n\t{OPT_C}{index}:{END_OPT_C} Proceed {direction}, {floor_data.get_basic_direction(direction)} down the hallway.'
                _options[str(index)] = f'{direction}'
    else:
        for index, direction_number in {3: facing, 4: OPPOSITE[facing], 5: LEFT[facing], 6: RIGHT[facing]}.items():
            direction = STRING_DIRECTIONS[direction_number]
            if direction in options:
                display_string += f'\n\t{OPT_C}{index}:{END_OPT_C} Proceed {floor_data.get_basic_direction(direction)} down the hallway.'
                _options[str(index)] = f'{direction}'
    display_string += '\n'
    return display_string, _options


def get_extra_actions(floor_data):
    text, options = '', {}

    compass = Refs.gc.get_inventory().has_item('compass')

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

    text += f'\n\t{OPT_C}{inventory_index}:{END_OPT_C} Inventory'
    options[str(inventory_index)] = f'{INVENTORY_BATTLE}:0'

    safe_zone = floor_data.get_floor().get_map().is_marker(SAFE_ZONES)
    activated_safe_zone = floor_data.is_activated_safe_zone()

    if safe_zone and not activated_safe_zone:
        text += f'\n\t{OPT_C}{safe_zone_index}:{END_OPT_C} Create Safe Zone'
        options[str(safe_zone_index)] = 'create_safe_zone'

    if activated_safe_zone:
        text += f'\n\t{OPT_C}{safe_zone_index}:{END_OPT_C} Rest'
        options[str(safe_zone_index)] = 'rest'

    adventurers_able = False
    for character in floor_data.get_characters():
        if character.can_take_action():
            adventurers_able = True

    if adventurers_able:
        if Refs.gc.get_inventory().has_pickaxe():
            text += f'\n\t{OPT_C}{action_index1}:{END_OPT_C} Inspect the dungeon walls. (Mine for resource)'
            options[str(action_index1)] = 'mine'
        if Refs.gc.get_inventory().has_shovel():
            text += f'\n\t{OPT_C}{action_index2}:{END_OPT_C} Inspect the dungeon environment. (Dig and Scrounge for resource)'
            options[str(action_index2)] = 'dig'
    text += '\n'
    return text, options


def get_bar_display(size, filled):
    string, count = '', (size - 2) * filled
    for index in range(size - 2):
        if index < count:
            string += '='
        else:
            string += ' '
    return f'[{string}]'


def _get_enemy_display(enemy, enemy_width, battle_data, enemy_index, option_index, _options):
    enemy_rows = []

    status_effects = enemy.get_effects()
    name = enemy.get_name()

    health_string = get_bar_display(int(enemy_width * 0.8), enemy.get_battle_health() / enemy.get_health())

    if status_effects:
        name += '*'

    if enemy.is_dead():
        enemy_rows.append((center(f'[s]{name}[/s]', len(name), enemy_width), enemy_width))
        enemy_rows.append((center(f'[s]{RED_C}{health_string}{END_OPT_C}[/s]', len(health_string), enemy_width), enemy_width))
    else:
        if not battle_data.get_state().startswith('battle_select'):
            enemy_rows.append((center(f'{OPT_C}{option_index}:{END_OPT_C} {name}', len(name) + len(f'{option_index}: '), enemy_width), enemy_width))
            _options[str(option_index)] = f'encounter#select#show#{enemy_index}'
        else:
            enemy_rows.append((name.center(enemy_width), enemy_width))
        enemy_rows.append((center(f'{RED_C}{health_string}{END_OPT_C}', len(health_string), enemy_width), enemy_width))
    enemy_rows.append(('', 0))
    return enemy_rows


def _get_character_display(character, character_width, battle_data, char_index, option_index, _options):
    character_rows = []

    status_effects = character.get_effects()

    if ' ' in character.get_name():
        name = character.get_name().split(' ')[0]
    else:
        name = character.get_name()

    health_string = get_bar_display(int(character_width * 0.8), character.get_battle_health() / character.get_health())
    mana_string = get_bar_display(int(character_width * 0.8), character.get_battle_mana() / character.get_mana())
    skill_name = f'S.S.: {character.get_selected_skill().get_name()}'

    if status_effects:
        name += '*'

    if character.is_dead():
        character_rows.append((center(f'[s]{name}[/s]', len(name), character_width), character_width))

        character_rows.append((center(f'[s]{skill_name}[/s]', len(skill_name), character_width), character_width))
        character_rows.append((center(f'[s]{RED_C}{health_string}{END_OPT_C}[/s]', len(health_string), character_width), character_width))
        character_rows.append((center(f'[s]{BLUE_C}{mana_string}{END_OPT_C}[/s]', len(mana_string), character_width), character_width))
    else:
        if not battle_data.get_state().startswith('battle_select'):
            character_rows.append((center(f'{OPT_C}{option_index}:{END_OPT_C} {name}', len(name) + len(f'{option_index}: '), character_width), character_width))
            _options[str(option_index)] = f'encounter#select#show#{char_index}'
        else:
            character_rows.append((f'{name.center(character_width)}', character_width))

        character_rows.append((skill_name.center(character_width), character_width))
        character_rows.append((f'{RED_C}{health_string.center(character_width)}{END_OPT_C}', character_width))
        character_rows.append((f'{BLUE_C}{mana_string.center(character_width)}{END_OPT_C}', character_width))
    character_rows.append(('', 0))
    return character_rows


def get_battle_display(console, floor_data, screen_data):
    battle_data = floor_data.get_battle_data()

    option_index = 1
    _options = {}

    enemy_width = character_width = floor(console.get_width() * 0.25)
    action_width = effect_width = floor(enemy_width * 2)

    screen_columns = [[], [], [], []]
    screen_string = '\n'

    enemies = battle_data.get_enemies()
    characters = battle_data.get_characters()

    first_col_enemies = enemies[:7]
    second_col_enemies = enemies[7:]

    first_col_characters = characters[:4]
    second_col_characters = characters[4:]

    # Display the special bar
    special_string, sides = '', floor(console.get_width() * 0.05)
    special_width = console.get_width() - (sides * 2) - 2

    special_amount = special_width * battle_data.get_special_amount() / 25

    for index in range(special_width, 0, -1):
        if index % ceil(special_width / 5) == 0 and index != 0:
            special_string += '|'
        elif index <= special_amount:
            special_string += '='
        else:
            special_string += ' '
    for _ in range(sides):
        screen_string += ' '
    screen_string += f'{SEA_FOAM_C}[b][{special_string}] {battle_data.get_special_count()}[/b]{END_OPT_C}\n\n'

    # Reset character skills if no special
    special_count = 0
    special_possible = battle_data.get_special_count()
    for character in battle_data.get_characters():
        if character.get_selected_skill().is_special():
            special_count += 1
            if special_count > special_possible:
                character.select_skill(0)

        mcost = character.get_mana_cost(character.get_selected_skill())
        if mcost > character.get_battle_mana():
            character.select_skill(0)

    # Create Actions
    effect_rows = []
    action_rows = []
    if battle_data.get_state().startswith('battle_select'):
        Refs.app.scroll_widget.opacity = 0
        entity_index = int(battle_data.get_state().split('#')[1])
        if entity_index <= len(battle_data.get_characters()) - 1:
            entity = battle_data.get_characters()[entity_index]
            selected_skill = entity.get_selected_skill()

            skills = entity.get_skills()
            skill_indexes = [0, 1, 3, 5, 7]
            for index, skill in enumerate(skills):
                skill_index = skill_indexes[index]
                mana_cost = entity.get_mana_cost(skill)

                skill_name = skill.get_name()
                if mana_cost > 0:
                    skill_name += f' - {mana_cost}'
                name_length = len(skill_name) + 3
                skill_description = skill.get_description()
                description_length = len(skill_description)

                special_blocked = False
                if skill.is_special():
                    special_blocked = battle_data.get_special_count() < 0
                    if not special_blocked:
                        # If we have gauge points, are they selected already?
                        possible = battle_data.get_special_count()
                        for character in battle_data.get_characters():
                            if character.get_selected_skill().is_special():
                                possible -= 1
                        if possible <= 0:
                            special_blocked = True

                if skill == selected_skill or (skill.is_special() and special_blocked) or (mana_cost > 0 and mana_cost > entity.get_battle_mana()):
                    skill_name = f'[s]{skill_name}[/s]'
                    skill_description = f'[s]{skill_description}[/s]'

                action_rows.append((f'{OPT_C}{option_index}:{END_OPT_C} {skill_name}', name_length))
                action_rows.append((f'    {skill_description}', description_length + 4))
                action_rows.append((f'', 0))

                if skill != selected_skill:
                    skill_option = str(option_index)
                else:
                    skill_option = '0'
                _options[skill_option] = f'encounter#select#{entity_index}#{skill_index}'
                option_index += 1
        else:
            # What do we display when we are the enemy?
            entity = battle_data.get_enemies()[entity_index - len(battle_data.get_characters())]
            _options['0'] = f'encounter#select#close'
        action_rows.append((f'{OPT_C}0:{END_OPT_C} Back', 7))

        # Create the Status Effect Rows
        name = f'{entity.get_name()} Status Effects'
        effect_rows.append((name, len(name)))
        effects = entity.get_effects()
        if len(effects) == 0:
            effect_rows.append(('', 0))
            effect_rows.append(('None', 4))
        else:
            for effect_type, effect_list in effects.items():
                for effect in effect_list.values():
                    if effect_type in STAT_TYPES:
                        if effect.get_duration() <= 0:
                            effect_string = f'{STAT_TYPES[effect_type]} {"+" if effect.get_amount() > 0 else ""}{effect.get_amount() * 100}%'
                        else:
                            effect_string = f'{STAT_TYPES[effect_type]} {"+" if effect.get_amount() > 0 else ""}{effect.get_amount() * 100}% - {effect.get_duration()} turn{"s" if effect.get_duration() > 1 else ""}'
                    elif effect_type in COUNTER_TYPES:
                        effect_string = f'{COUNTER_TYPES[effect_type]} x{effect.get_amount()}'
                    else:
                        effect_string = 'Not Implemented'
                    effect_rows.append((effect_string, len(effect_string)))
    else:
        Refs.app.scroll_widget.opacity = 1
        _options['0'] = 'encounter#attack'
        _options['1'] = f'{INVENTORY_BATTLE}:0'
        action_rows.append((f'{OPT_C}0:{END_OPT_C} Attack', 9))
        action_rows.append((f'{OPT_C}1:{END_OPT_C} Inventory', 12))
        option_index += 1

    # Create the character rows
    index = 0
    for character in first_col_characters:
        character_rows = _get_character_display(character, character_width, battle_data, index, option_index + index, _options)
        screen_columns[2] += character_rows
        index += 1

    for character in second_col_characters:
        character_rows = _get_character_display(character, character_width, battle_data, index, option_index + index, _options)
        screen_columns[3] += character_rows
        index += 1

    # Create the enemy rows
    for enemy in first_col_enemies:
        enemy_rows = _get_enemy_display(enemy, enemy_width, battle_data, index, option_index + index, _options)
        screen_columns[0] += enemy_rows
        index += 1

    for enemy in second_col_enemies:
        enemy_rows = _get_enemy_display(enemy, enemy_width, battle_data, index, option_index + index, _options)
        screen_columns[1] += enemy_rows
        index += 1

    option_index += len(first_col_characters)
    option_index += len(first_col_characters)
    option_index += len(first_col_enemies)
    option_index += len(second_col_enemies)

    # Pad the columns
    for col in screen_columns:
        for _ in range(len(col), 21):
            col.append(('', 0))

    # Combine all of the top rows into one string
    for index in range(21):
        for col in range(2):
            string, length = screen_columns[col][index]
            screen_string += ljust(string, length, enemy_width)

        for col in range(2, 4):
            string, length = screen_columns[col][index]
            screen_string += ljust(string, length, character_width)

        screen_string += '\n'

    screen_string += '\n'

    # Combine the action rows and the status effect rows
    for index in range(max(len(action_rows), len(effect_rows))):
        if index < len(action_rows):
            string, length = action_rows[index]
            screen_string += ''.ljust(4) + ljust(string, length, action_width - 4)
        else:
            screen_string += ''.ljust(action_width)
        if index < len(effect_rows):
            string, length = effect_rows[index]
            screen_string += center(string, length, effect_width)
        screen_string += '\n'

    # screen_string += '\n'
    # Display Battle Log - Will be on a separate scroll
    Refs.app.scroll_widget.ids.label.text = battle_data.get_battle_log()
    print(_options)
    return screen_string, _options


def get_dungeon_header(console):
    string = '\n\t'
    if Refs.gc.get_inventory().has_item('pocket_watch'):
        string += f'{Refs.gc.get_time()}'
        string += '\n\t'
    for character in Refs.gc.get_floor_data().get_characters()[:3]:
        string += character.get_name().split(' ')[0].ljust(9) + character.get_stamina_message().ljust(7) + f' - HP {round(character.get_battle_health()/character.get_health() * 100, 1)}%'.ljust(12) + f' - MP {round(character.get_battle_mana()/character.get_mana() * 100, 1)}%'.ljust(12) + ' | '
    string = string[:-3] + '\n\t'
    for character in Refs.gc.get_floor_data().get_characters()[3:6]:
        string += character.get_name().split(' ')[0].ljust(9) + character.get_stamina_message().ljust(7) + f' - HP {round(character.get_battle_health()/character.get_health() * 100, 1)}%'.ljust(12) + f' - MP {round(character.get_battle_mana()/character.get_mana() * 100, 1)}%'.ljust(12) + ' | '
    string = string[:-3] + '\n\t'
    for character in Refs.gc.get_floor_data().get_characters()[8:]:
        string += character.get_name().split(' ')[0].ljust(9) + character.get_stamina_message().ljust(7) + f' - HP {round(character.get_battle_health()/character.get_health() * 100, 1)}%'.ljust(12) + f' - MP {round(character.get_battle_mana()/character.get_mana() * 100, 1)}%'.ljust(12) + ' | '
    return string[:-3] + '\n'


def get_screen(console, screen_data):

    floor_data = Refs.gc.get_floor_data()

    print(screen_data, floor_data.is_in_encounter())
    if floor_data.get_battle_data() is not None:
        print(floor_data.get_battle_data().get_state())

    if screen_data == 'asleep':
        # All characters have fallen asleep.
        display_string = '\n\tAll your characters have fallen asleep! Oh no!\n\tWill they wake up or will they be eaten?\n'
        display_string += f'\n\t{OPT_C}0:{END_OPT_C} Fast Forward\n'
        _options = {'0': 'roll_sleep_chance'}
        return display_string, _options
    elif screen_data == 'woke_up':
        character = floor_data.get_alive_characters()[randint(0, len(floor_data.get_alive_characters()) - 1)]
        character.wake_up()
        floor_data.increase_stat(character.get_id(), 0, Refs.gc.get_random_stat_increase())
        display_string = f'\n\t{character.get_name()} woke up! Try to get to a safe zone to rest your other adventurers!\n'
        display_string += f'\n\t{OPT_C}0:{END_OPT_C} Continue\n'
        _options = {'0': None}
        return display_string, _options

    console.header_callback = None
    if not floor_data.is_in_encounter():
        console.header_callback = get_dungeon_header
        display_string, _options = get_tunnel_descriptions(floor_data)
        tool_string, tool_options = get_extra_actions(floor_data)

        _options.update(tool_options)

        compass = Refs.gc.get_inventory().has_item('compass')

        sleep_string = ''
        for character in floor_data.get_characters():
            if character.is_dead():
                sleep_string += f'\n\t{character.get_name()} is incapacitated! Stamina usage +35%'
            elif character.get_stamina() <= 0:
                sleep_string += f'\n\t{character.get_name()} has fallen asleep! Stamina usage +25%'

        display_string = sleep_string + '\n' + display_string

        if compass:
            map_index = 3
        else:
            map_index = 2

        # Get map and display it
        floor_map = floor_data.get_floor().get_map()
        floor_id = floor_data.get_floor().get_id()
        if floor_data.party_has_perk('mapping') or Refs.gc.get_inventory().has_item(f'path_map_floor_{floor_id}') or Refs.gc.get_inventory().has_item(f'full_map_floor_{floor_id}'):
            if floor_map.get_enabled():
                display_string_rows = (display_string + tool_string).split('\n')
                map_rows, radius = floor_map.get_rows()
                display_string = ''

                display_string_width = 140 - ((radius - 5) * 4)

                for x in range(len(display_string_rows)):
                    if x < len(map_rows):
                        row = display_string_rows[x].replace('\t', '    ')
                        display_string += ljust(row, get_plain_size(row), display_string_width) + '[font=CourierNew]' + map_rows[x] + '\n'
                    else:
                        display_string += display_string_rows[x] + '\n'

                if len(display_string_rows) < len(map_rows):
                    for x in range(len(display_string_rows), len(map_rows)):
                        display_string += ljust('', 0, display_string_width) + '[font=CourierNew]' + map_rows[x] + '\n'
                    display_string += ljust('', 0, display_string_width) + f'       {OPT_C}{map_index}:{END_OPT_C} Map Options'
                else:
                    display_string += ljust('', 0, display_string_width) + f'       {OPT_C}{map_index}:{END_OPT_C} Map Options'
            else:
                display_string = display_string + f'\n\t{OPT_C}{map_index}:{END_OPT_C} Map Options\n' + tool_string
            _options[str(map_index)] = MAP_OPTIONS
        else:
            display_string += tool_string
        return display_string, _options
    else:
        display_string = '\n\t' + floor_data.get_descriptions()
        _options = {}

        if floor_data.get_encounter_state() == 'start':
            display_string += f'\n\n\tYou have encountered {COUNT_TO_STRING[len(floor_data.get_battle_data().get_enemies())]} enemies.\n\tYou need to fight!\n\n\t{OPT_C}0:{END_OPT_C} Start fight!\n'
            _options['0'] = 'encounter#start'
            return display_string, _options
        elif floor_data.get_encounter_state().startswith('battle'):
            return get_battle_display(console, floor_data, screen_data)
        # In encounter options
    display_string += '\n'
    return display_string, _options


def handle_action(console, action):
    screen_data = None
    floor_data = Refs.gc.get_floor_data()
    if action is None:
        pass
    elif action == 'mine' or action == 'dig' or action == 'create_safe_zone':
        inventory = Refs.gc.get_inventory()

        if action == 'mine':
            tool = inventory.get_current_pickaxe()
            tool_name = 'pickaxe'
        elif action == 'dig':
            tool = inventory.get_current_shovel()
            tool_name = 'shovel'
        else:
            tool = inventory.get_current_harvesting_knife()
            tool_name = 'knife'

        if tool is None:
            console.error_time = 2.5
            console.error_text = f'You have no {tool_name} selected!'
            return
        elif tool.get_hardness() < floor_data.get_floor().get_hardness():
            console.error_time = 2.5
            console.error_text = f'Your {tool_name} is nto hard enough to affect this level!'
            return

        tool.remove_durability(Refs.gc.get_random_wear_amount() * 7.5)

        index = randint(0, len(floor_data.get_able_characters()) - 1)
        character = floor_data.get_able_characters()[index]
        character.take_action(Refs.gc.get_stamina_weight() + 1)

        floor_data.increase_stat(character.get_id(), 2, Refs.gc.get_random_stat_increase())

        if action == 'mine' or action == 'dig':
            floor_data.increase_rest_count(2)
            console.set_screen(f'{DUNGEON_RESOURCE_RESULT}:{action}#{character.get_id()}')
            return
        else:
            floor_data.activate_safe_zone()
    elif action == 'rest':
        for character in floor_data.get_characters():
            character.rest()
        Refs.gc.get_calendar().fast_forward(30)
        floor_data.decrease_safe_zones()
        floor_data.increase_rest_count()
    elif action == 'roll_sleep_chance':
        if Refs.gc.get_floor_data().is_activated_safe_zone():
            next_action = choices([f'asleep', 'woke_up'], [0.7, 0.3], k=1)[0]
        else:
            next_action = choices([f'asleep', 'loss', 'woke_up'], [0.4, 0.3, 0.3], k=1)[0]
        Refs.gc.get_calendar().fast_forward(60 * 6)
        if next_action == 'loss':
            console.set_screen(f'{DUNGEON_RESULT}:loss')
            return
        else:
            screen_data = next_action
    elif action == 'ascend' or action == 'descend':
        floor_id = floor_data.get_floor().get_id()
        floor_data.get_floor().get_map().clear_current_node()
        if action == 'ascend' and floor_id == 1:
            console.set_screen(f'{DUNGEON_RESULT}:ascend')
        else:
            if action == 'ascend':
                floor_data.set_next_floor(floor_id - 1)
            else:
                floor_data.set_next_floor(floor_id + 1)
            console.set_screen(f'{DUNGEON_MAIN_LOCKED}')
        return
    elif action == 'North' or action == 'East' or action == 'South' or action == 'West':
        floor_data.progress_by_direction(DIRECTIONS_FROM_STRING[action])
        all_asleep = True
        for character in floor_data.get_characters():
            all_asleep &= character.get_stamina() <= 0
        if all_asleep:
            screen_data = 'asleep'
        if not floor_data.is_in_encounter() and floor_data.get_floor().get_map().is_marker(EXIT):
            if not floor_data.have_beaten_boss():
                console.set_screen(DUNGEON_MAIN_LOCKED)
                return
    elif action.startswith('encounter'):
        encounter_action = action.split('#', 1)[1]
        battle_data = floor_data.get_battle_data()
        if encounter_action == 'start':
            battle_data.progress_encounter()
        elif encounter_action == 'attack':
            result = battle_data.make_turn()
            if result is not None:
                battle_data.progress_encounter()
                if result:
                    console.set_screen(f'{DUNGEON_RESULT}:win')
                    # Refs.app.scroll_widget.opacity = 1
                else:
                    console.set_screen(f'{DUNGEON_RESULT}:loss')
                Refs.app.scroll_widget.ids.label.text = battle_data.get_battle_log()
                # Refs.app.scroll_widget.opacity = 1
                return
        elif encounter_action.startswith('select'):
            select_action = action.split('#')[2]
            print(encounter_action, select_action)
            if select_action == 'close':
                battle_data.set_state('battle')
            elif select_action == 'show':
                entity_index = action.split('#')[3]
                battle_data.set_state(f'battle_select#{entity_index}')
            else:
                entity_index, select_index = action.split('#')[2:]
                battle_data.get_characters()[int(entity_index)].select_skill(int(select_index))
                battle_data.set_state('battle')
                    # char_index, select_index = action.split('#')[3:]
                    # if action == 'show':
                    #     battle_data.set_state(f'battle_select#{char_index}#{select_index}')
                    # else:
                    #     battle_data.get_characters()[int(char_index)].select_skill(int(select_index))
                    #     battle_data.set_state('battle')
    else:
        console.set_screen(action)
        return
    if screen_data is None:
        console.set_screen(DUNGEON_BATTLE)
    else:
        console.set_screen(f'{DUNGEON_BATTLE}:{screen_data}')
