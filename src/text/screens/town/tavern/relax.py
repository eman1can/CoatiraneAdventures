from random import randint

from refs import END_OPT_C, OPT_C, Refs
from text.screens.screen_names import BACK
from text.screens.town import get_town_header


def get_screen(console, screen_data):
    console.header_callback = get_town_header
    display_text = ''

    texts = ['You enjoy a hearty ale and relax among the crowd.',
             'Good thing you aren\'t lactose intolerent, as you love cheese.',
             'Sitting in the corner like a weirdo, you devour a chicken leg.',
             'Om nom nom. Glug, glug, glug. *sigh*',
             'Yum. You love the food in Gekkai.',
             'Your family hates you because you spend all their money on booze.',
             'You get hit in the face by a wild skrimp!',
             'You catch up with an old friend.',
             'You watch as someone dips a fry in blood and then eats it. Gross.',
             'You run into the god of posterity. You hate that dude.',
             'Your friend introduces you to a new wine. You get very drunk.',
             'Blonde, brunette, where are all the redheads?',
             'Someone dropped their sandwich. Poor sandwich.',
             'Coffee or booze? Why not both? Welcome to irish coffee.',
             'The only way to ignore the annoying goddess of gems is to drink more.',
             'You get chased by a cross-dressing shrimp in a fedora. Oh, wait. You were asleep.',
             'You run into a wild cannibalistic penguin. They\'re a great drinking buddy.',
             'Dodo birds are the long lost cousin of the Jack Bird. I wonder if they pooped gold too?',
             'Ow! You got nailed by a smiling orange.']
    
    cost = randint(100, 300)
    if cost > Refs.gc.get_varenth():
        display_text += '\n\tYou don\'t have enough money to buy any refreshments!'
    else:
        Refs.gc.update_varenth(-cost)
        text = texts[randint(0, len(texts) - 1)]
        point = randint(1, 100) > 95
        point_text = 'You gain 1 skill point.' if point else ''
        if point:
            Refs.gc.add_skill_point()
        display_text += f'\n\t{text}\n\t{point_text}'

    _options = {'0': BACK}
    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} Continue\n'
    return display_text, _options


def handle_action(console, action):
    pass
