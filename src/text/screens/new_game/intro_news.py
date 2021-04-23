from refs import END_OPT_C, OPT_C, Refs
from text.screens.screen_names import TOWN_MAIN


def get_screen(console, screen_data):
    chosen_char = Refs.gc.get_obtained_characters(False)[0]
    display_text = f'\n\tWelcome {Refs.gc.get_name()} to the town of Coatirane!'
    display_text += f'\n\n\t{chosen_char.get_name()} is excited to be a part of your budding family!'
    display_text += f'\n\tYou have decided to pool your money and have 3000 Varenth.'
    display_text += f'\n\tAdventure into the dungeon with {chosen_char.get_name()} to get more money!'
    display_text += '\n\n\tYou talked to a friend and they have set you up in a small two room flat and paid the housing bills for 36 days.'
    display_text += '\n\tIt will cost 50,000 Varenth to rent the two room flat for 36 days after your current pay runs out.'
    display_text += '\n\tGood luck in your adventures!\n'
    display_text += f'\n\t{OPT_C}0:{END_OPT_C} Continue\n'
    return display_text, {'0': TOWN_MAIN}


def handle_action(console, action):
    console.set_screen(action, False)
