# Kivy Imports
from kivy.properties import BooleanProperty, DictProperty, ListProperty, NumericProperty, ObjectProperty, OptionProperty, StringProperty

from kivy.uix.relativelayout import RelativeLayout
# KV Import
from loading.kv_loader import load_kv
from refs import Refs

load_kv(__name__)


class SquareCharacterPreview(RelativeLayout):
    preview = ObjectProperty(None)

    is_select = BooleanProperty(False)
    has_screen = BooleanProperty(False)
    is_support = BooleanProperty(False)
    new_image_instance = BooleanProperty(False)

    event = ObjectProperty(None)
    has_tag = BooleanProperty(False)
    tag = ObjectProperty(None)

    has_stat = BooleanProperty(False)
    stat_type = OptionProperty('Strength', options=['Strength', 'Magic', 'Endurance', 'Dexterity', 'Agility',
                                           'Phy. Atk', 'Mag. Atk', 'Defense', 'Health', 'Mana',
                                           'Party', 'Rank', 'Name', 'Score', 'Worth'])
    stat_image_source = StringProperty('icons/str.png')
    stat_text = StringProperty('Str: ')
    stat_number = NumericProperty(19.99)

    character = ObjectProperty(None)
    support = ObjectProperty(None)

    char_button_source = StringProperty('buttons/char_button_square')
    char_button_collide_image = StringProperty('')

    background_source = StringProperty('preview_square_background.png')
    char_image_source = StringProperty('')
    overlay_source = StringProperty('')

    star_data = DictProperty({})
    star_list_data = ListProperty([])

    def __init__(self, **kwargs):
        self.update_overlay()
        super().__init__(**kwargs)

    def on_stat_type(self, *args):
        if self.character == -1:
            return
        character = Refs.gc.get_char_by_index(self.character)
        if self.stat_type == 'Strength':
            self.stat_image_source = 'icons/str.png'
            self.stat_text = 'Str.'
            self.stat_number = character.get_strength()
        elif self.stat_type == 'Magic':
            self.stat_image_source = 'icons/mag.png'
            self.stat_text = 'Mag.'
            self.stat_number = character.get_magic()
        elif self.stat_type == 'Endurance':
            self.stat_image_source = 'icons/end.png'
            self.stat_text = 'End.'
            self.stat_number = character.get_endurance()
        elif self.stat_type == 'Dexterity':
            self.stat_image_source = 'icons/dex.png'
            self.stat_text = 'Dex.'
            self.stat_number = character.get_dexterity()
        elif self.stat_type == 'Agility':
            self.stat_image_source = 'icons/agi.png'
            self.stat_text = 'Agi.'
            self.stat_number = character.get_agility()
        elif self.stat_type == 'Health':
            self.stat_image_source = 'icons/hea.png'
            self.stat_text = 'Hp.'
            self.stat_number = character.get_health()
        elif self.stat_type == 'Mana':
            self.stat_image_source = 'icons/mna.png'
            self.stat_text = 'Mana'
            self.stat_number = character.get_mana()
        elif self.stat_type == 'Phy. Atk':
            self.stat_image_source = 'icons/patk.png'
            self.stat_text = 'Phy. Atk'
            self.stat_number = character.get_phyatk()
        elif self.stat_type == 'Mag. Atk':
            self.stat_image_source = 'icons/matk.png'
            self.stat_text = 'Mag. Atk'
            self.stat_number = character.get_magatk()
        elif self.stat_type == 'Defense':
            self.stat_image_source = 'icons/def.png'
            self.stat_text = 'Def.'
            self.stat_number = character.get_defense()
        elif self.stat_type == 'Party':
            self.stat_text = ''
            self.stat_number = 0.0
            self.stat_image_source = ''
        elif self.stat_type == 'Rank':
            self.stat_text = ''
            self.stat_number = 0.0
            self.stat_image_source = ''
        elif self.stat_type == 'Name':
            self.stat_image_source = ''
            self.stat_text = character.get_name()
            self.stat_number = 0.0
        elif self.stat_type == 'Score':
            self.stat_text = 'Score'
            self.stat_image_source = ''
            self.stat_number = character.get_score()
        elif self.stat_type == 'Worth':
            self.stat_text = 'Worth'
            self.stat_image_source = ''
            self.stat_number = character.get_worth()
        self.update_overlay()

    def update_stars(self):
        if self.character is not None:
            for index in range(1, 11):
                if not self.make_star(self.character, index, index):
                    break
        self.star_list_data = self.star_data.values()

    def make_star(self, character, rank, index):
        if f'star_{index}' in self.star_data:
            if self.star_data[f'star_{index}']['broken']:
                return True
            if character.get_rank(rank).broken:
                self.star_data[f'star_{index}']['broken'] = True
                self.star_data[f'star_{index}']['source'] = 'icons/rankbrk.png'
                return True
        if character.get_rank(rank).unlocked:
            star = {'id': f'star_{index}',
                    'source': 'icons/star.png',
                    'size_hint': Refs.app.get_dkey(f'scp.star_{index} s_h'),
                    'pos_hint': Refs.app.get_dkey(f'scp.star_{index} p_h')}
            if character.get_rank(rank).broken:
                star['source'] = 'icons/rankbrk.png'
                star['broken'] = True
            else:
                star['broken'] = False
            self.star_data[f'star_{index}'] = star
            return True
        else:
            return False

    def on_character(self, *args):
        character = Refs.gc.get_char_by_index(self.character)
        self.char_image_source = character.get_image('preview')
        self.on_stat_type()
        self.update_overlay()

    def update_overlay(self):
        if self.has_stat and self.stat_type != 'Party' and self.stat_type != 'Rank':
            self.overlay_source = 'preview_overlay_square_stat.png'
        else:
            self.overlay_source = 'preview_overlay_square_empty.png'

    def on_has_stat(self, *args):
        self.update_overlay()
        self.on_stat_type()

    def reload(self):
        self.on_stat_type()
        self.update_stars()

    def handle_preview_click(self):
        if self.is_support:
            self.preview.set_char_screen(True, self.preview.char, self.character)
        else:
            self.preview.set_char_screen(True, self.character, self.preview.support)
        Refs.gs.get_screen('dungeon_main').update_party_score()
        Refs.gs.display_screen(None, False, False)
