from refs import END_OPT_C, OPT_C, Refs
from text.screens.screen_names import BACK, PERK_BESTOW, PERK_INFO
from text.screens.town import get_town_header


def get_screen(console, screen_data):
    console.header_callback = get_town_header
    _options, perk_id = {}, screen_data
    perk = Refs.gc['perks'][perk_id]

    display_text = f'\n\n\t{perk.get_name()} - {perk.get_tree().title()} - Level {perk.get_level()}'
    display_text += '\n\n\tEligible Adventurers:'
    characters = list(Refs.gc.get_obtained_characters(False))

    valid_characters = []
    for character in characters:
        meets_requirements = not character.has_perk(perk_id)

        for requirement in perk.get_requirements():
            if requirement == 'none':
                continue
            meets_requirements &= character.has_perk(requirement)

        for char_perk_id in character.get_all_perks():
            meets_requirements &= Refs.gc['perks'][char_perk_id].get_tree() == perk.get_tree()

        if meets_requirements:
            valid_characters.append(character)

    if len(valid_characters) == 0:
        display_text += f'\n\t\tNo Eligible Adventurers.'

    for index, character in enumerate(valid_characters):
        display_text += f'\n\t\t{OPT_C}{index + 1}:{END_OPT_C} {character.get_display_name()} {character.get_name()}'
        _options[str(index + 1)] = f'{perk_id}#{character.get_id()}'

    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} Back\n'
    _options['0'] = BACK
    return display_text, _options


def handle_action(console, action):
    perk_id, character_id = action.split("#")

    perk = Refs.gc['perks'][perk_id]
    character = Refs.gc.get_char_by_id(character_id)

    character.bestow_perk(perk.get_id())
    Refs.gc.unlock_perk(perk)

    console.set_screen(f'{PERK_INFO}:{perk_id}', True)
