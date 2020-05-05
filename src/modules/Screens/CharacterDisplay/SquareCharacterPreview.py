from kivy.app import App
from kivy.input.providers.wm_touch import WM_MotionEvent
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty, OptionProperty, NumericProperty

from src.modules.KivyBase.Hoverable import RelativeLayoutBase as RelativeLayout


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
    stat_image_source = StringProperty('../res/screens/stats/str.png')
    stat_text = StringProperty('Str: ')
    stat_number = NumericProperty(19.99)

    character = ObjectProperty(None)
    support = ObjectProperty(None)

    char_button_source = StringProperty('../res/screens/buttons/char_button_square')
    char_button_collide_image = StringProperty('')

    background_source = StringProperty('../res/screens/stats/preview_square_background.png')
    char_image_source = StringProperty('')
    overlay_source = StringProperty('')

    def __init__(self, **kwargs):
        self.update_overlay()
        super().__init__(**kwargs)

    def on_stat_type(self, *args):
        if self.character is None:
            return
        if self.stat_type == 'Strength':
            self.stat_image_source = '../res/screens/stats/str.png'
            self.stat_text = 'Str.'
            self.stat_number = self.character.get_strength()
        elif self.stat_type == 'Magic':
            self.stat_image_source = '../res/screens/stats/mag.png'
            self.stat_text = 'Mag.'
            self.stat_number = self.character.get_magic()
        elif self.stat_type == 'Endurance':
            self.stat_image_source = '../res/screens/stats/end.png'
            self.stat_text = 'End.'
            self.stat_number = self.character.get_endurance()
        elif self.stat_type == 'Dexterity':
            self.stat_image_source = '../res/screens/stats/dex.png'
            self.stat_text = 'Dex.'
            self.stat_number = self.character.get_dexterity()
        elif self.stat_type == 'Agility':
            self.stat_image_source = '../res/screens/stats/agi.png'
            self.stat_text = 'Agi.'
            self.stat_number = self.character.get_agility()
        elif self.stat_type == 'Health':
            self.stat_image_source = '../res/screens/stats/health.png'
            self.stat_text = 'Hp.'
            self.stat_number = self.character.get_health()
        elif self.stat_type == 'Mana':
            self.stat_image_source = '../res/screens/stats/mana.png'
            self.stat_text = 'Mana'
            self.stat_number = self.character.get_mana()
        elif self.stat_type == 'Phy. Atk':
            self.stat_image_source = '../res/screens/stats/physicalattack.png'
            self.stat_text = 'Phy. Atk'
            self.stat_number = self.character.get_phyatk()
        elif self.stat_type == 'Mag. Atk':
            self.stat_image_source = '../res/screens/stats/magicalattack.png'
            self.stat_text = 'Mag. Atk'
            self.stat_number = self.character.get_magatk()
        elif self.stat_type == 'Defense':
            self.stat_image_source = '../res/screens/stats/defense.png'
            self.stat_text = 'Def.'
            self.stat_number = self.character.get_defense()
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
            self.stat_text = self.character.get_name()
            self.stat_number = 0.0
        elif self.stat_type == 'Score':
            self.stat_text = 'Score'
            self.stat_image_source = ''
            self.stat_number = self.character.get_score()
        elif self.stat_type == 'Worth':
            self.stat_text = 'Worth'
            self.stat_image_source = ''
            self.stat_number = self.character.get_worth()
        self.update_overlay()

    def on_character(self, *args):
        self.char_image_source = self.character.preview_image_source
        self.on_stat_type()
        self.update_overlay()

    def update_overlay(self):
        if self.has_stat and self.stat_type != 'Party' and self.stat_type != 'Rank':
            self.overlay_source = '../res/screens/stats/preview_overlay_square_stat.png'
        else:
            self.overlay_source = '../res/screens/stats/preview_overlay_square_empty.png'

    def on_has_stat(self, *args):
        self.update_overlay()
        self.on_stat_type()

    def reload(self):
        self.on_stat_type()

    def on_char_touch_down(self, instance, touch):
        if instance.collide_point(*touch.pos):
            touch.grab(self)
            self.emptied = False

    def on_char_touch_up(self, instance, touch):
        root = App.get_running_app().main
        if instance.collide_point(*touch.pos):
            if touch.grab_current == self and not self.emptied:
                touch.ungrab(self)
                if isinstance(touch, WM_MotionEvent):
                    touch.button = 'left'
                if touch.button == 'left':
                    if self.event is not None:
                        self.event.cancel()
                    if self.is_support:
                        self.preview.set_char_screen(True, self.preview.char, self.character)
                    else:
                        self.preview.set_char_screen(True, self.character, None)
                    root.display_screen(None, False, False)
                    for screen in root.screens:
                        if screen.name == 'dungeon_main':
                            screen.update_party_score()
                            break
                    return True
                elif touch.button == 'right':
                    screen, made = root.create_screen('char_attr', self.character, self.preview)
                    root.display_screen(screen, True, True)
                    return True
            return False
