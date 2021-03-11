from game.save_load import load_save_info
from game.skill import ATTACK_TYPE_INDEX_TO_STRING, ELEMENT_INDEX_TO_STRING
from loading.family import load_domains
from refs import Refs


OPT_C = '[color=#CA353E]'
END_OPT_C = '[/color]'


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
            display_text += f"\n\t\tSkill Level - {info.get('skill_level')}"
        else:
            display_text += 'New Game[/b]'
            _options[str(save_slot)] = f'new_game_{save_slot}'
    display_text += '\n'
    return display_text, _options


def intro_domain_name(console):
    display_text = '\n\t0: cancel\n\n\tOh almighty Deity, bless us with your name.\n'
    _options = {'0': 'back'}
    return display_text, _options


def intro_domain_gender(console):
    display_text = f'\n\t0: back\n\n\tOh almighty {console.memory.game_info["name"]}, what is your gender?\n'
    display_text += '\n\t1: God\n\t2: Goddess\n\t3: Goddex\n'
    _options = {'0': 'back', '1': 'gender_male', '2': 'gender_female', '3': 'gender_neither'}
    return display_text, _options


def intro_domain(console):
    display_text = f'\n\t0: back\n\n\tOh almighty {console.memory.game_info["name"]}, what is your domain?\n'
    _options = {'0': 'back'}
    if console.memory.domains is None:
        console.memory.domains = load_domains(Refs.gc.get_program_type())

    if console.memory.current_domain == -1:
        # print('-1 →', len(_domains) - 1)
        console.memory.current_domain = len(console.memory.domains) - 1
    if console.memory.current_domain == len(console.memory.domains):
        # print(len(console.memory.domains), '→ 0')
        console.memory.current_domain = 0

    desc = console.memory.domains[console.memory.current_domain].get_large_description().replace('\n', '\n\t\t')
    display_text += f'\n\t{1}: {console.memory.domains[console.memory.current_domain].title}\n\t\t{desc}\n'
    _options[str(1)] = f'domain_{console.memory.domains[console.memory.current_domain].title}'
    display_text += f'\n\n\t< {2} - {console.memory.domains[console.memory.current_domain - 1].title} | {console.memory.domains[len(console.memory.domains) % (console.memory.current_domain + 1)].title} - {3} >\n'
    _options[str(2)] = 'domain_prev'
    _options[str(3)] = 'domain_next'
    return display_text, _options


def intro_select(console):
    display_text = f'\n\t0: back\n\n\tOh almighty {console.memory.game_info["name"]}, you have two adventurers interested in your fledgling family.\n\tYou only have the finances to support yourself and one adventurer. Which one do you choose?\n'
    _options = {'0': 'back'}

    with open(f'../save/char_load_data/{Refs.gc.get_program_type()}/CharacterDefinitions.txt', 'r') as file:
        ais = file.readline().split(',')
        bell = file.readline().split(',')

    display_text += '\n\t1: Ais Wallenstein'

    def print_char_stuff(char):
        string = f'\n\t\t{ATTACK_TYPE_INDEX_TO_STRING[int(char[1].strip())]} - {ELEMENT_INDEX_TO_STRING[int(char[2].strip())]}'
        string += f'\n\t\tHealth - {char[3].strip()}'
        string += f'\n\t\tMana - {char[4].strip()}'
        string += f'\n\t\tStrength - {char[5].strip()}'
        string += f'\n\t\tMagic - {char[6].strip()}'
        string += f'\n\t\tEndurance - {char[7].strip()}'
        string += f'\n\t\tAgility - {char[8].strip()}'
        string += f'\n\t\tDexterity - {char[9].strip()}\n'
        return string

    display_text += print_char_stuff(ais)
    display_text += '\n\t2: Bell Cranel'
    display_text += print_char_stuff(bell)
    _options['1'] = 'select_ais'
    _options['2'] = 'select_bell'
    return display_text, _options


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
