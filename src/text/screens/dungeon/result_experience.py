from kivy.clock import Clock
from refs import END_OPT_C, OPT_C, Refs
from text.screens.screen_names import DUNGEON_MAIN

STAT_WIDTH = 17
LABELS = ['    ', 'HP. ', 'MP. ', 'Str.', 'Mag.', 'End.', 'Agi.', 'Dex.']


def get_screen(console, screen_data):
    display_text, _options = '', {'0': 0}
    console.header_callback = None
    char_rows = {}
    rows_lengths = []

    display_text += '\n\tYou successfully escaped the dungeon!\n\n'
    increases, fam_bonus_increases = Refs.gc.get_floor_data().get_increases()

    for character in Refs.gc.get_current_party():
        if character is None:
            continue
        rows = [character.get_name().split(' ')[0]]
        char_increases = increases[character.get_index()]
        char_fam_increases = fam_bonus_increases[character.get_index()]

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
        rows.append('')
        for partner_index, amount in char_fam_increases.items():
            partner = Refs.gc.get_char_by_index(partner_index)
            character.add_familiarity(partner.get_id(), amount)
            if amount > 0.004:
                partner_name = partner.get_name()
                if ' ' in partner_name:
                    partner_name = partner_name.split(' ')[0]
                rows.append(f'{partner_name} +{round(amount, 2)}%')
        rows_lengths.append(len(rows))
        char_rows[character.get_id()] = rows

    for index in range(max(rows_lengths[:8])):
        if index < 8:
            display_text += f'\t{LABELS[index]} '
        elif index == 8:
            display_text += '\tFam. Bonuses'
        else:
            display_text += '\t     '
        for character_id in list(char_rows.keys())[:8]:
            if index < len(char_rows[character_id]):
                display_text += char_rows[character_id][index].center(STAT_WIDTH)
            else:
                display_text += ''.ljust(STAT_WIDTH)
        display_text += '\n'
    if len(char_rows.keys()) > 8:
        for index in range(max(rows_lengths[8:])):
            if index < 8:
                display_text += f'\t{LABELS[index]} '
            elif index == 8:
                display_text += '\t Famil. Bonuses  '
            else:
                display_text += '\t     '
            for character_id in list(char_rows.keys())[8:]:
                if index < len(char_rows[character_id]):
                    display_text += char_rows[character_id][index].center(STAT_WIDTH)
                else:
                    display_text += ''.ljust(STAT_WIDTH)
            display_text += '\n'

    Refs.gc.reset_floor_data()

    display_text += f'\n\n\t{OPT_C}{0}:{END_OPT_C} Continue\n'
    return display_text, _options


def handle_action(console, action):
    console.text = '\n\tSaving Game...'
    Clock.schedule_once(lambda dt: Refs.gc.save_game(lambda: console.set_screen(DUNGEON_MAIN, False)), 0.5)
