# Project Imports
# Standard Library Imports
import random

from kivy.properties import ObjectProperty

# Kivy Imports
from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import SwapTransition
# KV Import
from loading.kv_loader import load_kv
from refs import Refs
# UIX Imports
from uix.modules.screen import Screen

load_kv(__name__)


class TavernMain(Screen):
    def __init__(self, **kwargs):
        self.sound = SoundLoader.load('res/snd/recruit.wav')
        self.sound.seek(0)
        super().__init__(**kwargs)

    def on_recruit(self, *args):
        tt = 'Are you sure?'
        dt = 'Recruitment will cost 25,000V'
        cot = 'Recruit'
        cat = 'Return'
        Refs.gp.display_popup(self, 'tm_confirm', show_warning=False, on_confirm=self.do_recruit, title_text=tt, description_text=dt, confirm_text=cot, cancel_text=cat)

    def on_relax(self, *args):
        cost = random.randint(100, 300)
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
        text = texts[random.randint(0, len(texts) - 1)]
        tt = 'Are you sure?'
        dt = f'Refreshments will cost {cost}.'
        cot = 'Relax'
        cat = 'Return'
        Refs.gp.display_popup(self, 'tm_confirm', show_warning=False, on_confirm=lambda *args:self.do_relax(cost, text), title_text=tt, description_text=dt, confirm_text=cot, cancel_text=cat)

    def do_relax(self, cost, description):
        if Refs.gc.get_varenth() < cost:
            tt = 'Not enough varenth!'
            dt = 'You need to gain more varenth!'
            ct = 'Return'
            Refs.gp.display_popup(self, 'tm_confirm', show_warning=False, title_text=tt, description_text=dt, confirm_text=ct)
        else:
            Refs.gc.update_varenth(-cost)
            ct = 'Return'
            point = random.randint(1, 100) > 95
            point_text = '\nYou gain 1 skill point.'
            if point:
                Refs.gc.add_skill_point()
                description += point_text
            Refs.gp.display_popup(self, 'tm_confirm', show_warning=False, description_text=description, confirm_text=ct)

    def on_chat(self, *args):
        pass

    def do_recruit(self, *args):
        if Refs.gc.get_varenth() < 25000:
            tt = 'Not enough varenth!'
            dt = 'You need to gain more varenth!'
            ct = 'Return'
            Refs.gp.display_popup(self, 'tm_confirm', show_warning=False, title_text=tt, description_text=dt, confirm_text=ct)
        else:
            Refs.gc.update_varenth(-25000)

            characters = Refs.gc.get_characters()
            obtained_characters = Refs.gc.get_all_obtained_character_indexes()

            if len(obtained_characters) == len(characters):
                Refs.gp.display_popup(self, 'tm_no_recruit')
            else:
                unobtained_characters = [char for char in characters if char.get_index() not in obtained_characters]
                index = random.randint(0, len(unobtained_characters) - 1)
                viewed_characters = [unobtained_characters[index]]
                Refs.gs.transition = SwapTransition(duration=2)
                self.sound.play()
                Refs.gs.display_screen('recruit_' + unobtained_characters[index].get_id(), True, True, unobtained_characters[index], viewed_characters)
