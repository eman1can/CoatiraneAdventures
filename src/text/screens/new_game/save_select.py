from game.save_load import load_save_info
from refs import END_OPT_C, OPT_C, Refs
from text.screens.screen_names import BACK, GAME_LOADING, INTRO_DOMAIN_NAME, TOWN_MAIN


def get_screen(console, screen_data):
    display_text = f'\n\t{OPT_C}0:{END_OPT_C} back\n\n\tSelect a save slot to load!'
    _options = {'0': BACK}
    for save_slot in range(1, 4):
        display_text += f'\n\n\t[b]{OPT_C}{save_slot}:{END_OPT_C} Save Slot {save_slot} - '
        info = load_save_info(save_slot)
        _options[str(save_slot)] = f'{save_slot}'
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
            _options[str(save_slot)] = f'new{save_slot}'
    display_text += '\n'
    return display_text, _options


def handle_action(console, action):
    save_slot = int(action[-1])
    if action.startswith('new'):
        console.new_game_info['save_slot'] = save_slot
        console.set_screen(INTRO_DOMAIN_NAME, True)
    else:
        console.set_screen(GAME_LOADING, False)
        Refs.app.start_loading(console, save_slot, TOWN_MAIN)
