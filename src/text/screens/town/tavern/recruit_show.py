from random import randint

from refs import END_OPT_C, OPT_C, Refs
from text.screens.screen_names import BACK, TAVERN_RECRUIT, TAVERN_RECRUIT_SHOW


def get_character_string(character):
    string = f'\n\t\t{character.get_display_name()} - {character.get_name()} - {character.get_age()} - {character.get_gender()} - {character.get_race()}'
    if not character.is_support():
        string += f'\n\t\tFavorite Weapons: {character.get_favorite_weapon()}'
        sub_weapon = character.get_favorite_sub_weapon()
        if sub_weapon is not None:
            string += f', {sub_weapon}'
    string += f'\n\t\t{character.get_description()}'
    if not character.is_support():
        string += f'\n\n\t\tAdventurer - {character.get_attack_type_string()} - {character.get_element_string()}'
    else:
        string += f'\n\n\t\tSupporter'
    string += f'\n\n\t\tHealth    - {character.get_health()}'
    string += f'\n\t\tMana      - {character.get_mana()}'
    string += f'\n\t\tStrength  - {character.get_strength()}'
    string += f'\n\t\tMagic     - {character.get_magic()}'
    string += f'\n\t\tEndurance - {character.get_endurance()}'
    string += f'\n\t\tAgility   - {character.get_agility()}'
    string += f'\n\t\tDexterity - {character.get_dexterity()}\n'
    return string


def get_screen(console, screen_data):
    character_ids = screen_data.split('#')
    text = character_ids.pop(0)

    fail_texts = ['Lots of people showed up! They only came for the food though.',
                  'You talked to many people, but they all found you boring.',
                  'Next time, try increasing your charm.',
                  'You get slapped in the face after you "flirt" with the locals.',
                  'You got so drunk, you passed out before talking to anybody.',
                  'The shame of explaining the boot print on your face will last a lifetime.',
                  'You were amazing! Wonderful! Still nobody liked you.',
                  'Your as interesting as a rock.',
                  'If I had been at your party, I would have cried.',
                  'Here, have some tissues.',
                  'You call that a party? You only had two chicken wings.',
                  'Next time, order more booze!',
                  'You suck. Go home.',
                  'A cute girl liked you. Sadly she already has a family.',
                  'The buffest guy vibed with you. He\'s already in a family.']

    success_texts = ['They loved your hair!',
                     'You are so cool!',
                     'Foooooooooooood!',
                     'Your party will be the talk of the town for the next month!',
                     'You forgot to mention it was a casual party, but people still loved you.',
                     'When you next throw a party, everybody will be interested.',
                     '*dance*, *dance*, *dance*']
    _options = {'0': BACK}
    if text == '':
        if 'failure' in character_ids:
            text = fail_texts[randint(0, len(fail_texts) - 1)] + '\n\tBetter luck next time!\n'
        else:
            text = success_texts[randint(0, len(success_texts) - 1)] + '\n\tYou got a potential recruit!\n'

    display_text = f'\n\t{text}\n\t'
    if 'failure' not in character_ids:
        character_id = character_ids[0]
        character = Refs.gc.get_char_by_id(character_id)

        display_text += get_character_string(character)
        display_text += f'\n\tIt will cost you '

        recruitment_items = character.get_recruitment_items()
        list = len(recruitment_items) >= 3
        for index, (item_id, count) in enumerate(recruitment_items.items()):
            print(item_id, count)
            if index == len(recruitment_items) - 1:
                if not list:
                    display_text += ' '
                display_text += 'and '
            if item_id == 'varenth':
                display_text += f'{count} Varenth'
            else:
                item = Refs.gc.find_item(item_id)
                if item is None:
                    continue
                display_text += f'{count} {item.get_name()}'
            if list and index != len(recruitment_items) - 1:
                display_text += ', '

        display_text += f' to convince this person to join your family.\n'

        next_screen = f'{TAVERN_RECRUIT_SHOW}:{text}#'
        _options['1'] = f'{character_id}'
        for char_id in character_ids[1:]:
            next_screen += char_id + '#'
        display_text += f'\n\t{OPT_C}1:{END_OPT_C} Recruit this person\n'
        if len(character_ids) > 1:
            display_text += f'\t{OPT_C}2:{END_OPT_C} Continue the party'
            _options['2'] = next_screen[:-1]
        display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} Cancel\n'
    else:
        display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} Continue\n'
    return display_text, _options


def handle_action(console, action):
    if '#' in action:
        console.set_screen(action)
    else:
        character = Refs.gc.get_char_by_id(action)
        for item_id, count in character.get_recruitment_items().items():
            material_ids = item_id.split('/')
            item_id = material_ids.pop(-1)
            if len(material_ids) > 0:
                metadata = {'material_id': material_ids[0]}
                if len(material_ids) > 1:
                    metadata['sub_material1_id'] = material_ids[1]
                    if len(material_ids) > 2:
                        metadata['sub_material2_id'] = material_ids[2]
            else:
                metadata = None

            if Refs.gc.get_inventory().get_item_count(item_id, metadata) < count:
                console.error_time = 2.5
                console.error_text = 'You don\'t have the required items!'
            else:
                Refs.gc.obtain_character(character.get_index(), character.is_support())
                console.set_screen(TAVERN_RECRUIT)
