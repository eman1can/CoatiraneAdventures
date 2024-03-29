from refs import END_OPT_C, OPT_C, Refs
from text.screens.screen_names import BACK, CHANGE_EQUIP, STATUS_BOARD


ABILITIES_HEADER_SIZE = 10
RANK_CHAR_SIZE = 5
STATS_HEADER_SIZE = ABILITIES_HEADER_SIZE + RANK_CHAR_SIZE
NUMBER_SIZE = 6
BOX_SIZE = ABILITIES_HEADER_SIZE + RANK_CHAR_SIZE + NUMBER_SIZE
LARGE_EQUIPMENT_BOX = 33
ELEMENT_COLORS = ['#FFFFFF', '#80C0FF', '#FF9090', '#E8E880', '#80C080', '#CCA078', '#FFFFFF', '#D094D0']
TYPE_COLORS = ['#550000', '#050054', '#00460C', '#7F3300', '#7F006E']
RANK_COLORS = {'I': '#FFFFFF', 'H': '#FFFFFF', 'G': '#FFFFFF',
               'F': '#AF5113', 'E': '#AF5113',
               'D': '#CCCCCC', 'C': '#CCCCCC', 'B': '#FFD400', 'A': '#FFD400',
               'S': '#00BBFF', 'SS': '#00BBFF', 'SSS': '#00BBFF'}


def get_screen(console, screen_data):
    display_string, _options = '', {}
    character = Refs.gc.get_char_by_id(screen_data)

    display_string += '\n'
    display_string += '\t  ' + character.get_name().ljust(BOX_SIZE) + '   ' + character.get_display_name().rjust(BOX_SIZE) + '   '

    star_string = ''
    for index in range(character.get_current_rank()):
        star_string += '☆ '
    display_string += '[font=NanumGothic]' + star_string[:-1].ljust(BOX_SIZE) + '[/font]'

    if not character.is_support():
        display_string += f'\n\t  [color={TYPE_COLORS[character.get_attack_type()]}]' + (character.get_attack_type_string() + ' Type').ljust(BOX_SIZE) + '[/color]'
    else:
        display_string += f'\n\t  ' + ''.ljust(BOX_SIZE)
    if not character.is_support():
        display_string += f'   [color={ELEMENT_COLORS[character.get_element()]}]' + character.get_element_string().rjust(BOX_SIZE) + '[/color]   '
    else:
        display_string += f'   ' + ''.rjust(BOX_SIZE) + '   '

    star_string = ''
    for index in range(character.get_current_rank()):
        if character.get_rank(index + 1).is_broken():
            star_string += '★ '
    display_string += '[font=NanumGothic]' + star_string[:-1].ljust(BOX_SIZE) + '[/font]\n\t'

    # Create the first row of the box
    display_string += '┌'
    for _ in range(3):
        for _ in range(BOX_SIZE + 2):
            display_string += '─'
        display_string += '┬'
    display_string = display_string[:-1] + '┐'

    display_string += '\n\t│ [b]' + 'Total Stats'.center(BOX_SIZE)
    display_string += '[/b] │ [b]' + 'Total Abilities'.center(BOX_SIZE)
    display_string += '[/b] │ [b]' + 'Rank Abilities'.center(BOX_SIZE)

    display_string += '[/b] │\n\t│ ' + 'Health'.ljust(STATS_HEADER_SIZE) + f'{Refs.gc.format_number(int(character.get_health()))}'.rjust(NUMBER_SIZE)
    display_string += ' │ ' + 'Strength'.ljust(ABILITIES_HEADER_SIZE)
    display_string += f'[color={RANK_COLORS[character.get_strength_rank()]}]' + character.get_strength_rank().center(RANK_CHAR_SIZE) + '[/color]'
    display_string += f'{character.get_strength()}'.rjust(NUMBER_SIZE)

    display_string += ' │ ' + 'Strength'.ljust(ABILITIES_HEADER_SIZE)
    display_string += f'[color={RANK_COLORS[character.get_strength_rank(character.get_current_rank())]}]' + character.get_strength_rank(character.get_current_rank()).center(RANK_CHAR_SIZE) + '[/color]'
    display_string += f'{character.get_strength(character.get_current_rank())}'.rjust(NUMBER_SIZE)

    display_string += ' │\n\t│ ' + 'Mana'.ljust(STATS_HEADER_SIZE) + f'{Refs.gc.format_number(int(character.get_mana()))}'.rjust(NUMBER_SIZE)
    display_string += ' │ ' + 'Magic'.ljust(ABILITIES_HEADER_SIZE)
    display_string += f'[color={RANK_COLORS[character.get_magic_rank()]}]' + character.get_magic_rank().center(RANK_CHAR_SIZE) + '[/color]'
    display_string += f'{character.get_magic()}'.rjust(NUMBER_SIZE)

    display_string += ' │ ' + 'Magic'.ljust(ABILITIES_HEADER_SIZE)
    display_string += f'[color={RANK_COLORS[character.get_magic_rank(character.get_current_rank())]}]' + character.get_magic_rank(character.get_current_rank()).center(RANK_CHAR_SIZE) + '[/color]'
    display_string += f'{character.get_magic(character.get_current_rank())}'.rjust(NUMBER_SIZE)

    display_string += ' │\n\t│ ' + 'P.Attack'.ljust(STATS_HEADER_SIZE) + f'{Refs.gc.format_number(int(character.get_physical_attack()))}'.rjust(NUMBER_SIZE)
    display_string += ' │ ' + 'Endurance'.ljust(ABILITIES_HEADER_SIZE)
    display_string += f'[color={RANK_COLORS[character.get_endurance_rank()]}]' + character.get_endurance_rank().center(RANK_CHAR_SIZE) + '[/color]'
    display_string += f'{character.get_endurance()}'.rjust(NUMBER_SIZE)

    display_string += ' │ ' + 'Endurance'.ljust(ABILITIES_HEADER_SIZE)
    display_string += f'[color={RANK_COLORS[character.get_endurance_rank(character.get_current_rank())]}]' + character.get_endurance_rank(character.get_current_rank()).center(RANK_CHAR_SIZE) + '[/color]'
    display_string += f'{character.get_endurance(character.get_current_rank())}'.rjust(NUMBER_SIZE)

    display_string += ' │\n\t│ ' + 'M.Attack'.ljust(STATS_HEADER_SIZE) + f'{Refs.gc.format_number(int(character.get_magical_attack()))}'.rjust(NUMBER_SIZE)
    display_string += ' │ ' + 'Dexterity'.ljust(ABILITIES_HEADER_SIZE)
    display_string += f'[color={RANK_COLORS[character.get_dexterity_rank()]}]' + character.get_dexterity_rank().center(RANK_CHAR_SIZE) + '[/color]'
    display_string += f'{character.get_dexterity()}'.rjust(NUMBER_SIZE)

    display_string += ' │ ' + 'Dexterity'.ljust(ABILITIES_HEADER_SIZE)
    display_string += f'[color={RANK_COLORS[character.get_dexterity_rank(character.get_current_rank())]}]' + character.get_dexterity_rank(character.get_current_rank()).center(RANK_CHAR_SIZE) + '[/color]'
    display_string += f'{character.get_dexterity(character.get_current_rank())}'.rjust(NUMBER_SIZE)

    display_string += ' │\n\t│ ' + 'Defense'.ljust(STATS_HEADER_SIZE) + f'{Refs.gc.format_number(int(character.get_defense()))}'.rjust(NUMBER_SIZE)
    display_string += ' │ ' + 'Agility'.ljust(ABILITIES_HEADER_SIZE)
    display_string += f'[color={RANK_COLORS[character.get_agility_rank()]}]' + character.get_agility_rank().center(RANK_CHAR_SIZE) + '[/color]'
    display_string += f'{character.get_agility()}'.rjust(NUMBER_SIZE)

    display_string += ' │ ' + 'Agility'.ljust(ABILITIES_HEADER_SIZE)
    display_string += f'[color={RANK_COLORS[character.get_agility_rank(character.get_current_rank())]}]' + character.get_agility_rank(character.get_current_rank()).center(RANK_CHAR_SIZE) + '[/color]'
    display_string += f'{character.get_agility(character.get_current_rank())}'.rjust(NUMBER_SIZE)

    display_string += ' │\n\t'

    display_string += '├'
    for _ in range(3):
        for _ in range(BOX_SIZE + 2):
            display_string += '─'
        display_string += '┴'
    display_string = display_string[:-1] + '┤'

    display_string += '\n\t│ ' + (character.get_family() + ' Family').ljust(BOX_SIZE)
    display_string += '   ' + ('Score: ' + str(character.get_score())).ljust(BOX_SIZE)
    display_string += '   ' + ('Floor Depth: ' + str(character.get_floor_depth())).ljust(BOX_SIZE)
    display_string += ' │\n\t│ ' + ('Race: ' + str(character.get_race())).ljust(BOX_SIZE)
    display_string += '   ' + ('Worth: ' + str(character.get_worth())).ljust(BOX_SIZE)
    display_string += '   ' + ('Monsters Slain: ' + str(character.get_monsters_killed())).ljust(BOX_SIZE)
    display_string += ' │\n\t│ ' + ('Gender: ' + str(character.get_gender())).ljust(BOX_SIZE)
    display_string += '   ' + ('High Dmg: ' + str(character.get_high_damage())).ljust(BOX_SIZE)
    display_string += '   ' + ('People Slain: ' + str(character.get_people_killed())).ljust(BOX_SIZE)
    display_string += ' │'

    if not character.is_support():
        display_string += '\n\t├'
        for _ in range(2):
            for _ in range(LARGE_EQUIPMENT_BOX + 2):
                display_string += '─'
            display_string += '┬'
        display_string = display_string[:-1] + '┤'

        names = []
        durabilities = []
        for index, item in enumerate(character.get_outfit().items):
            if item is None:
                names.append('Not Equipped')
                durabilities.append(None)
            else:
                names.append(item.get_name())
                durabilities.append(item.get_current_durability() / item.get_durability())

        def get_durability_bar(durability_value, size):
            if durability_value is None:
                return ''.center(size + 2)
            else:
                string = '['
                for _ in range(int(size * durability_value)):
                    string += '='
                for _ in range(int(size * durability_value), size):
                    string += ' '
                return string + ']'

        display_string += '\n\t│ ' + names[0].center(LARGE_EQUIPMENT_BOX) + ' │ ' + names[1].center(LARGE_EQUIPMENT_BOX) + ' │'
        display_string += '\n\t│ ' + get_durability_bar(durabilities[0], LARGE_EQUIPMENT_BOX - 2) + ' │ ' + get_durability_bar(durabilities[1], LARGE_EQUIPMENT_BOX - 2) + ' │'

        display_string += '\n\t├'
        for _ in range(2):
            for _ in range(LARGE_EQUIPMENT_BOX + 2):
                display_string += '─'
            display_string += '┼'
        display_string = display_string[:-1] + '┤'

        display_string += '\n\t│ ' + names[2].center(LARGE_EQUIPMENT_BOX) + ' │ ' + names[3].center(LARGE_EQUIPMENT_BOX) + ' │'
        display_string += '\n\t│ ' + get_durability_bar(durabilities[2], LARGE_EQUIPMENT_BOX - 2) + ' │ ' + get_durability_bar(durabilities[3], LARGE_EQUIPMENT_BOX - 2) + ' │'

        display_string += '\n\t├'
        for _ in range(BOX_SIZE + 2):
            display_string += '─'
        display_string += '┬'
        for _ in range((LARGE_EQUIPMENT_BOX + 2) - (BOX_SIZE + 3)):
            display_string += '─'
        display_string += '┴'
        for _ in range((LARGE_EQUIPMENT_BOX + 2) - (BOX_SIZE + 3)):
            display_string += '─'
        display_string += '┬'
        for _ in range(BOX_SIZE + 2):
            display_string += '─'
        display_string += '┤'

        display_string += '\n\t│ ' + names[4].center(BOX_SIZE) + ' │ ' + names[5].center(BOX_SIZE) + ' │ ' + names[6].center(BOX_SIZE) + ' │'
        display_string += '\n\t│ ' + get_durability_bar(durabilities[4], BOX_SIZE - 2) + ' │ ' + get_durability_bar(durabilities[5], BOX_SIZE - 2) + ' │ ' + get_durability_bar(durabilities[6], BOX_SIZE - 2) + ' │'

        display_string += '\n\t├'
        for _ in range(3):
            for _ in range(BOX_SIZE + 2):
                display_string += '─'
            display_string += '┼'
        display_string = display_string[:-1] + '┤'

        display_string += '\n\t│ ' + names[7].center(BOX_SIZE) + ' │ ' + names[8].center(BOX_SIZE) + ' │ ' + names[9].center(BOX_SIZE) + ' │'
        display_string += '\n\t│ ' + get_durability_bar(durabilities[7], BOX_SIZE - 2) + ' │ ' + get_durability_bar(durabilities[8], BOX_SIZE - 2) + ' │ ' + get_durability_bar(durabilities[9], BOX_SIZE - 2) + ' │'

        display_string += '\n\t└'
        for _ in range(3):
            for _ in range(BOX_SIZE + 2):
                display_string += '─'
            display_string += '┴'
        display_string = display_string[:-1] + '┘'
    else:
        display_string += '\n\t└'
        for _ in range((BOX_SIZE + 3) * 3):
            display_string += '─'
        display_string = display_string[:-1] + '┘'

    if Refs.gc.get_floor_data() is None:
        index = 1
        display_string += '\n'
        if not character.is_support():
            display_string += f'\n\t{OPT_C}{index}:{END_OPT_C} Change Equip'
            _options[str(index)] = f'{CHANGE_EQUIP}:{screen_data}'
            index += 1
        display_string += f'\n\t{OPT_C}{index}:{END_OPT_C} Status Board'
        _options[str(index)] = f'{STATUS_BOARD}:{character.get_current_rank()}#{screen_data}'
    display_string += f'\n\n\t{OPT_C}0:{END_OPT_C} Back\n'

    _options['0'] = BACK

    return display_string, _options


def handle_action(console, action):
    console.set_screen(action, True)
