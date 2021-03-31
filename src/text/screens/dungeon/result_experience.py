from kivy.clock import Clock
from refs import END_OPT_C, OPT_C, Refs
from text.screens.screen_names import DUNGEON_MAIN

STAT_WIDTH = 11
LABELS = ['    ', 'HP. ', 'MP. ', 'Str.', 'Mag.', 'End.', 'Agi.', 'Dex.']


def get_screen(console, screen_data):
    display_text, _options = '', {'0': 0}
    console.header_callback = None
    char_rows = {}

    display_text += '\n\tYou successfully escaped the dungeon!\n\n'
    increases = Refs.gc.get_floor_data().get_increases()

    for character in Refs.gc.get_current_party():
        if character is None:
            continue
        rows = [character.get_name().split(' ')[0]]
        char_increases = increases[character.get_id()]

        stats = [character.get_health(), character.get_mana(), character.get_strength(), character.get_magic(), character.get_endurance(), character.get_agility(), character.get_dexterity()]
        increase_functions = [character.increase_health, character.increase_mana, character.increase_strength, character.increase_magic, character.increase_endurance, character.increase_agility, character.increase_dexterity]
        for index, function in enumerate(increase_functions):
            function(char_increases[index])
        new_stats = [character.get_health(), character.get_mana(), character.get_strength(), character.get_magic(), character.get_endurance(), character.get_agility(), character.get_dexterity()]

        for index in range(7):
            if new_stats[index] - stats[index] == 0:
                rows.append(f'{int(stats[index])}')
            else:
                rows.append(f'{int(stats[index])} → {int(new_stats[index])}')
        char_rows[character.get_id()] = rows

    for index in range(8):
        display_text += f'\t{LABELS[index]} '
        for character_id in list(char_rows.keys())[:8]:
            display_text += char_rows[character_id][index].center(STAT_WIDTH)
        display_text += '\n'
    if len(char_rows.keys()) > 8:
        for index in range(8):
            display_text += f'\t{LABELS[index]} '
            for character_id in list(char_rows.keys())[8:]:
                display_text += char_rows[character_id][index].center(STAT_WIDTH)
            display_text += '\n'

    Refs.gc.reset_floor_data()

    display_text += f'\n\n\t{OPT_C}{0}:{END_OPT_C} Continue\n'
    return display_text, _options


def handle_action(console, action):
    console.text = '\n\tSaving Game...'
    Clock.schedule_once(lambda dt: Refs.gc.save_game(lambda: console.set_screen(DUNGEON_MAIN)), 0.5)
