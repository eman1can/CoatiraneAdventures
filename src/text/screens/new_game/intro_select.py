from kivy.resources import resource_find

from game.save_load import create_new_save
from game.skill import ELEMENTS
from game.character import CHARACTER_ATTACK_TYPES, RACES, GENDERS
from loading.char import ATTACK_TYPE, DISPLAY_NAME, ELEMENT, NAME, AGE, GENDER, RACE, HEALTH, MANA, STRENGTH, MAGIC, ENDURANCE, DEXTERITY, AGILITY
from refs import END_OPT_C, OPT_C, Refs
from text.screens.screen_names import BACK, GAME_LOADING, INTRO_NEWS


def get_screen(console, screen_data):
    display_text = f'\n\tOh almighty {console.new_game_info["name"]}, you have two adventurers interested in your fledgling family.'
    display_text += '\n\tYou only have the finances to support yourself and one adventurer. Which one do you choose?\n\n'

    with open(resource_find(f'data/{Refs.gc.get_program_type()}/CharacterDefinitions.txt'), 'r') as file:
        ais = file.readline().split(',')
        ais_description = file.readline()
        file.readline()
        bell = file.readline().split(',')
        bell_description = file.readline()

    ais_rows, bell_rows = [], []

    ais_rows.append((f'{OPT_C}1:{END_OPT_C} {ais[DISPLAY_NAME].strip()} - {ais[NAME].strip()}', len(ais[DISPLAY_NAME].strip()) + len(ais[NAME].strip()) + 6))
    bell_rows.append((f'{OPT_C}2:{END_OPT_C} {bell[DISPLAY_NAME].strip()} - {bell[NAME].strip()}', len(bell[DISPLAY_NAME].strip()) + len(bell[NAME].strip()) + 6))

    width = int(console.get_width() * 0.5)

    def print_char_stuff(char, description, rows):
        string = f'Age - {char[AGE].strip()}   Race - {RACES[int(char[RACE].strip())]}   Gender - {GENDERS[int(char[GENDER].strip())]}'
        rows.append((string, len(string)))
        rows.append(('', 0))
        dindex = description.rindex(' ', 0, int(width * 0.6))
        first_half, second_half = description[:dindex], description.strip()[dindex + 1:]
        rows.append((first_half, len(first_half)))
        rows.append((second_half, len(second_half)))
        rows.append(('', 0))
        string = f'{CHARACTER_ATTACK_TYPES[int(char[ATTACK_TYPE].strip())]} - {ELEMENTS[int(char[ELEMENT].strip())]}'
        rows.append((string, len(string)))
        string = f'Health    - {char[HEALTH].strip()}'
        rows.append((string, len(string)))
        string = f'Mana      - {char[MANA].strip()}'
        rows.append((string, len(string)))
        string = f'Strength  - {char[STRENGTH].strip()}'
        rows.append((string, len(string)))
        string = f'Magic     - {char[MAGIC].strip()}'
        rows.append((string, len(string)))
        string = f'Endurance - {char[ENDURANCE].strip()}'
        rows.append((string, len(string)))
        string = f'Agility   - {char[AGILITY].strip()}'
        rows.append((string, len(string)))
        string = f'Dexterity - {char[DEXTERITY].strip()}'
        rows.append((string, len(string)))
        return rows

    ais_rows = print_char_stuff(ais, ais_description, ais_rows)
    bell_rows = print_char_stuff(bell, bell_description, bell_rows)

    for index in range(len(ais_rows)):
        row_string, length = ais_rows[index]
        gap = len(row_string) - length
        display_text += row_string.ljust(int(width * 0.7) + gap).center(width + gap)
        row_string, length = bell_rows[index]
        gap = len(row_string) - length
        display_text += row_string.ljust(int(width * 0.7) + gap).center(width + gap) + '\n'

    display_text += f'\n\t{OPT_C}0:{END_OPT_C} back\n'
    _options = {'0': BACK, '1': 0, '2': 1}
    return display_text, _options


def handle_action(console, action):
    create_new_save(console.new_game_info['save_slot'], console.new_game_info['name'], console.new_game_info['gender'], 'symbol_1', console.new_game_info['domain'], action)
    console.set_screen(GAME_LOADING)
    Refs.app.start_loading(console, console.new_game_info['save_slot'], INTRO_NEWS)
