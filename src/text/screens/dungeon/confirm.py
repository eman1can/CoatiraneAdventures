from kivy.clock import Clock
from refs import END_OPT_C, OPT_C, Refs
from text.screens.screen_names import BACK, DUNGEON_BATTLE


def get_screen(console, screen_data):
    descend = screen_data == 'down'
    floor_score, party_score = Refs.gc.get_floor_score(descend), Refs.gc.get_current_party_score()

    display_text = f'\n\tThe recommended score for this floor is: {floor_score}'
    display_text += f'\n\tYour party score is: {party_score}'

    if party_score < floor_score:
        display_text += '\n\n\tWhile the floor score is recommended as to be able to easily clear the floor,'
        display_text += '\n\tyou might take the time to level your characters, add a supporter or equip a weapon.'
        display_text += '\n\tThe dungeon can be unpredictable, and it would be sad to see you go.'

    display_text += f'\n\n\tWould you like to continue?\n\n\t{OPT_C}0:{END_OPT_C} No\n\t{OPT_C}1:{END_OPT_C} Yes\n'
    _options = {'0': BACK, '1': descend}
    return display_text, _options


def handle_action(console, action):
    character_count = 0
    for character in Refs.gc.get_current_party()[:8]:
        if character is not None:
            character_count += 1
    if character_count == 0:
        console.error_time = 2.5
        console.error_text = 'You need to have adventurers to delve!'
    else:
        Refs.gc.set_next_floor(bool(action))
        console.text = '\n\tSaving Game...'
        Clock.schedule_once(lambda dt: Refs.gc.save_game(lambda: console.set_screen(DUNGEON_BATTLE)), 0.5)
