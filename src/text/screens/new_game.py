from game.save_load import load_save_info
from game.skill import ATTACK_TYPE_INDEX_TO_STRING, ELEMENT_INDEX_TO_STRING
from loading.family import load_domains
from refs import END_OPT_C, OPT_C, Refs


def new_game(console):
    font_size = f'{int(console.get_global_font_size() * 40 / 15)}pt'
    display_text = f'\n\n\n\t[color=#A35C7F][font=Precious][size={font_size}]Welcome to Coatirane Adventures![/size][/font][/color]\n\n\t{OPT_C}0:{END_OPT_C} Start Game\n\t{OPT_C}1:{END_OPT_C} Exit Game\n'
    _options = {'0': 'start_game', '1': 'exit_game'}
    return display_text, _options


def save_select(console):
    display_text = f'\n\t{OPT_C}0:{END_OPT_C} back\n\n\tSelect a save slot to load!'
    _options = {'0': 'back'}
    for save_slot in range(1, 4):
        display_text += f'\n\n\t[b]{OPT_C}{save_slot}:{END_OPT_C} Save Slot {save_slot} - '
        info = load_save_info(save_slot)
        _options[str(save_slot)] = f'load_game_{save_slot}'
        if info is not None:
            display_text += f"{info.get('game_version')} - {info.get('last_save_time')}[/b]"
            display_text += f"\n\t\t{info.get('gender')[:1].upper()} - {info.get('save_name')} - {info.get('domain')}"
            display_text += f"\n\t\tFamily Renown - {info.get('rank')}"
            display_text += f"\n\t\tVarenth - {info.get('varenth')}"
            display_text += f"\n\t\tCharacters Obtained - {info.get('chars_collected')}"
            display_text += f"\n\t\tQuests Finished - {info.get('quests')}"
            display_text += f"\n\t\tLowest Floor - {info.get('lowest_floor')}"
            display_text += f"\n\t\tTotal Score - {info.get('total_character_score')}"
            display_text += f"\n\t\tPerks Unlocked - {info.get('skill_level')}"
        else:
            display_text += 'New Game[/b]'
            _options[str(save_slot)] = f'new_game_{save_slot}'
    display_text += '\n'
    return display_text, _options


def intro_domain_name(console):
    display_text = f'\n\t{OPT_C}0:{END_OPT_C} cancel\n\n\tOh almighty Deity, bless us with your name.\n'
    _options = {'0': 'back'}
    return display_text, _options


def intro_domain_gender(console):
    display_text = f'\n\t{OPT_C}0:{END_OPT_C} back\n\n\tOh almighty {console.memory.game_info["name"]}, what is your gender?\n'
    display_text += f'\n\t{OPT_C}1:{END_OPT_C} God\n\t{OPT_C}2:{END_OPT_C} Goddess\n\t{OPT_C}3:{END_OPT_C} Goddex\n'
    _options = {'0': 'back', '1': 'gender_male', '2': 'gender_female', '3': 'gender_neither'}
    return display_text, _options


def intro_domain(console):
    display_text = f'\n\t{OPT_C}0:{END_OPT_C} back\n\n\tOh almighty {console.memory.game_info["name"]}, what is your domain?\n'
    _options = {'0': 'back'}
    if console.memory.domains is None:
        console.memory.domains = load_domains(Refs.gc.get_program_type())

    if console.memory.current_domain == -1:
        console.memory.current_domain = len(console.memory.domains) - 1
    if console.memory.current_domain == len(console.memory.domains):
        console.memory.current_domain = 0

    desc = console.memory.domains[console.memory.current_domain].get_large_description().replace('\n', '\n\t\t')
    display_text += f'\n\t{OPT_C}1:{END_OPT_C} {console.memory.domains[console.memory.current_domain].title}\n\t\t{desc}\n'
    _options['1'] = f'domain_{console.memory.domains[console.memory.current_domain].title}'
    print(console.memory.current_domain, console.memory.current_domain - 1, (console.memory.current_domain + 2) % len(console.memory.domains))
    print(console.memory.domains)
    display_text += f'\n\n\t←────── {OPT_C}2{END_OPT_C} {console.memory.domains[console.memory.current_domain - 1].title} | {console.memory.domains[(console.memory.current_domain + 2) % len(console.memory.domains)].title} {OPT_C}3{END_OPT_C} ──────→\n'
    _options['2'] = 'domain_prev'
    _options['3'] = 'domain_next'
    return display_text, _options


def intro_select(console):
    display_text = f'\n\t{OPT_C}0:{END_OPT_C} back\n\n\tOh almighty {console.memory.game_info["name"]}, you have two adventurers interested in your fledgling family.\n\tYou only have the finances to support yourself and one adventurer. Which one do you choose?\n'
    _options = {'0': 'back'}

    with open(f'data/{Refs.gc.get_program_type()}/CharacterDefinitions.txt', 'r') as file:
        ais = file.readline().split(',')
        bell = file.readline().split(',')

    display_text += f'\n\t{OPT_C}1:{END_OPT_C} Ais Wallenstein'

    def print_char_stuff(char):
        string = f'\n\t\t{ATTACK_TYPE_INDEX_TO_STRING[int(char[1].strip())]} - {ELEMENT_INDEX_TO_STRING[int(char[2].strip())]}'
        string += f'\n\t\tHealth    - {char[3].strip()}'
        string += f'\n\t\tMana      - {char[4].strip()}'
        string += f'\n\t\tStrength  - {char[5].strip()}'
        string += f'\n\t\tMagic     - {char[6].strip()}'
        string += f'\n\t\tEndurance - {char[7].strip()}'
        string += f'\n\t\tAgility   - {char[8].strip()}'
        string += f'\n\t\tDexterity - {char[9].strip()}\n'
        return string

    display_text += print_char_stuff(ais)
    display_text += f'\n\t{OPT_C}2:{END_OPT_C} Bell Cranel'
    display_text += print_char_stuff(bell)
    _options['1'] = 'select_ais'
    _options['2'] = 'select_bell'
    return display_text, _options


def intro_news(console):
    chosen_char = Refs.gc.get_obtained_characters(False)[0]
    display_text = f'\n\tWelcome {Refs.gc.get_name()} to the town of Coatirane!'
    display_text += f'\n\n\t{chosen_char.get_name()} is excited to be a part of your budding family!'
    display_text += f'\n\tYou have decided to pool your money and have 3000 Varenth.'
    display_text += f'\n\tAdventure into the dungeon with {chosen_char.get_name()} to get more money!'
    display_text += '\n\n\tYou talked to a friend and they have set you up in a small two room flat and paid the housing bills for 36 days.'
    display_text += '\n\tIt will cost 50,000 Varenth to rent the two room flat for 36 days after your current pay runs out.'
    display_text += '\n\tGood luck in your adventures!\n'
    display_text += f'\n\t{OPT_C}0:{END_OPT_C} Continue\n'
    return display_text, {'0': 'town_main'}


def game_loading(console):
    display_text = '\n\tLOADING GAME DATA\n'

    def display_progress_bar(current, maximum):
        if current > maximum:
            current = maximum
        string = '['
        for x in range(int(30 / maximum * current)):
            string += '='
        for x in range(int(30 / maximum * current), 30):
            string += ' '
        return string + f'] {current} / {maximum}'

    for bar_name, bar_values in console.memory.loading_progress.items():
        display_text += '\n\t' + display_progress_bar(*bar_values) + ' ' + bar_name
    display_text += '\n'
    return display_text, None
