from refs import END_OPT_C, OPT_C, Refs
from text.screens.screen_names import SAVE_SELECT


def get_screen(console, screen_data):
    console.header_callback = None
    font_size = f'{int(console.get_global_font_size() * 40 / 15)}pt'
    display_text = f'\n\n\n\t[color=#A35C7F][font=Precious][size={font_size}]Welcome to Coatirane Adventures![/size][/font][/color]\n\n\t{OPT_C}0:{END_OPT_C} Start Game\n\t{OPT_C}1:{END_OPT_C} Exit Game\n'

    _options = {'0': 0, '1': 1}
    return display_text, _options


def handle_action(console, action):
    if action == 0:
        console.set_screen(SAVE_SELECT)
    else:
        Refs.gc.save_game(None)
        Refs.app.stop()
