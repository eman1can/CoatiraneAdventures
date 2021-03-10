# Project Imports
from refs import Refs

# UIX Imports
from uix.modules.screen import Screen
from uix.modules.star import Star
# from uix.screens.character_display.heart_indicator import HeartIndicator

# Kivy Imports
from kivy.properties import BooleanProperty, ObjectProperty, NumericProperty, StringProperty, ListProperty, DictProperty
from kivy.uix.relativelayout import RelativeLayout

# KV Import
from loading.kv_loader import load_kv
load_kv(__name__)


class FilledCharacterPreviewScreen(Screen):
    preview = ObjectProperty(None)
    character = ObjectProperty(None)
    support = ObjectProperty(None)

    is_support = BooleanProperty(False)

    def on_character(self, *args):
        self.name = self.character.get_id()

    def on_support(self, *args):
        if self.support is not None:
            self.name += "_" + self.support.get_id()

    def update_lock(self, locked):
        self.ids.filled_preview.update_lock(locked)

    def close_hints(self):
        self.ids.filled_preview.close_hints()

    def reload(self):
        self.ids.filled_preview.reload()


class FilledCharacterPreview(RelativeLayout):

    text_color = ListProperty([0.796, 0.773, 0.678, 1])
    font_name = StringProperty('Gabriola')

    preview = ObjectProperty(None, allownone=True)

    new_image_instance = BooleanProperty(False)
    has_screen = BooleanProperty(False)
    # event = ObjectProperty(None, allownone=True)
    has_tag = BooleanProperty(False)
    has_stat = BooleanProperty(False)

    preview_wgap = NumericProperty(0)
    preview_hgap = NumericProperty(0)
    image_width = NumericProperty(0)

    is_select = BooleanProperty(False)
    is_support = BooleanProperty(False)
    character = ObjectProperty(None, allownone=True)
    support = ObjectProperty(None, allownone=True)

    locked = BooleanProperty(False)
    do_hover = BooleanProperty(True)

    char_hint_showing = BooleanProperty(False)
    support_hint_showing = BooleanProperty(False)
    hint_text = DictProperty({})
    char_hint_text = DictProperty({})
    support_hint_text = DictProperty({})

    char_button_source = StringProperty('')
    support_button_source = StringProperty('')
    char_button_collide_image = StringProperty('')
    support_button_collide_image = StringProperty('')

    background_source = StringProperty('screens/stats/preview_background.png')
    support_background_source = StringProperty('screens/stats/preview_support_background.png')
    char_image_source = StringProperty('')
    support_image_source = StringProperty('')
    overlay_source = StringProperty('')
    support_overlay_source = StringProperty('screens/stats/preview_support_background_overlay.png')

    phy_atk_text = StringProperty('0.0')
    mag_atk_text = StringProperty('0.0')
    health_text = StringProperty('0.0')
    mana_text = StringProperty('0.0')
    defense_text = StringProperty('0.0')
    strength_text = StringProperty('0.0')
    magic_text = StringProperty('0.0')
    endurance_text = StringProperty('0.0')
    dexterity_text = StringProperty('0.0')
    agility_text = StringProperty('0.0')

    # star_data = DictProperty({})
    star_list_data = ListProperty([])

    stat_list_data = ListProperty([])

    def __init__(self, **kwargs):
        self.update_overlay()
        self.update_buttons()
        self.update_labels()
        super().__init__(**kwargs)

        self.stat_list_data = [
            {'id': 'phy_atk_image',
             'source': 'screens/stats/PhysicalAttack.png',
             'size_hint': Refs.app.get_dkey('fcp.img s_h'),
             'pos_hint': Refs.app.get_dkey('fcp.img.phy_atk p_h')},
            {'id':        'mag_atk_image',
             'source':    'screens/stats/MagicalAttack.png',
             'size_hint': Refs.app.get_dkey('fcp.img s_h'),
             'pos_hint':  Refs.app.get_dkey('fcp.img.mag_atk p_h')},
            {'id':        'health_image',
             'source':    'screens/stats/Health.png',
             'size_hint': Refs.app.get_dkey('fcp.img s_h'),
             'pos_hint':  Refs.app.get_dkey('fcp.img.health p_h')},
            {'id':        'mana_image',
             'source':    'screens/stats/Mana.png',
             'size_hint': Refs.app.get_dkey('fcp.img s_h'),
             'pos_hint':  Refs.app.get_dkey('fcp.img.mana p_h')},
            {'id':        'defense_image',
             'source':    'screens/stats/Defense.png',
             'size_hint': Refs.app.get_dkey('fcp.img s_h'),
             'pos_hint':  Refs.app.get_dkey('fcp.img.defense p_h')},
            {'id':        'strength_image',
             'source':    'screens/stats/Str.png',
             'size_hint': Refs.app.get_dkey('fcp.img s_h'),
             'pos_hint':  Refs.app.get_dkey('fcp.img.strength p_h')},
            {'id':        'magic_image',
             'source':    'screens/stats/Mag.png',
             'size_hint': Refs.app.get_dkey('fcp.img s_h'),
             'pos_hint':  Refs.app.get_dkey('fcp.img.magic p_h')},
            {'id':        'endurance_image',
             'source':    'screens/stats/End.png',
             'size_hint': Refs.app.get_dkey('fcp.img s_h'),
             'pos_hint':  Refs.app.get_dkey('fcp.img.endurance p_h')},
            {'id':        'dexterity_image',
             'source':    'screens/stats/Dex.png',
             'size_hint': Refs.app.get_dkey('fcp.img s_h'),
             'pos_hint':  Refs.app.get_dkey('fcp.img.dexterity p_h')},
            {'id':        'agility_image',
             'source':    'screens/stats/Agi.png',
             'size_hint': Refs.app.get_dkey('fcp.img s_h'),
             'pos_hint':  Refs.app.get_dkey('fcp.img.agility p_h')},
        ]
        # self.update_stars()

    def on_is_select(self, *args):
        self.update_overlay()
        self.update_buttons()
        self.update_labels()

    def on_character(self, *args):
        self.char_image_source = self.character.get_image('slide')
        self.update_overlay()
        self.update_buttons()
        self.reload()

    def on_support(self, *args):
        self.support_image_source = self.support.get_image('slide_support')
        self.update_overlay()
        self.update_buttons()
        self.reload()

    def update_overlay(self):
        if self.support is not None:
            self.overlay_source = "screens/stats/preview_overlay_full.png"
        elif not self.is_select and not self.locked:
            self.overlay_source = "screens/stats/preview_overlay_empty_add.png"
        else:
            self.overlay_source = "screens/stats/preview_overlay_empty.png"

    def close_hints(self):
        self.on_char_hint_close()
        self.on_support_hint_close()
        self.ids.character_heart.reset_open()
        self.ids.support_heart.reset_open()

    def update_labels(self):
        values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        if self.character is not None:
            if self.support is None:
                values = [
                    round(self.character.get_physical_attack(), 2),
                    round(self.character.get_magical_attack(), 2),
                    round(self.character.get_health(), 2),
                    round(self.character.get_mana(), 2),
                    round(self.character.get_defense(), 2),
                    round(self.character.get_strength(), 2),
                    round(self.character.get_magic(), 2),
                    round(self.character.get_endurance(), 2),
                    round(self.character.get_agility(), 2),
                    round(self.character.get_dexterity(), 2)
                ]
            else:
                values = [
                    round(self.character.get_physical_attack() + self.support.get_physical_attack(), 2),
                    round(self.character.get_magical_attack() + self.support.get_magical_attack(), 2),
                    round(self.character.get_health() + self.support.get_health(), 2),
                    round(self.character.get_mana() + self.support.get_mana(), 2),
                    round(self.character.get_defense() + self.support.get_defense(), 2),
                    round(self.character.get_strength() + self.support.get_strength(), 2),
                    round(self.character.get_magic() + self.support.get_magic(), 2),
                    round(self.character.get_endurance() + self.support.get_endurance(), 2),
                    round(self.character.get_agility() + self.support.get_agility(), 2),
                    round(self.character.get_dexterity() + self.support.get_dexterity(), 2)
                ]
        self.phy_atk_text = str(values[0])
        self.mag_atk_text = str(values[1])
        self.health_text = str(values[2])
        self.mana_text = str(values[3])
        self.defense_text = str(values[4])
        self.strength_text = str(values[5])
        self.magic_text = str(values[6])
        self.endurance_text = str(values[7])
        self.agility_text = str(values[8])
        self.dexterity_text = str(values[9])

    def update_stars(self):
        character_size = (0.228, 0.061)
        support_size = (0.204, 0.05136)
        character_poses = [{"center_x": 0.1440, "center_y": 0.962},
                           {"center_x": 0.2231, "center_y": 0.962},
                           {"center_x": 0.3022, "center_y": 0.962},
                           {"center_x": 0.3813, "center_y": 0.962},
                           {"center_x": 0.4604, "center_y": 0.962},
                           {"center_x": 0.5395, "center_y": 0.962},
                           {"center_x": 0.6186, "center_y": 0.962},
                           {"center_x": 0.6977, "center_y": 0.962},
                           {"center_x": 0.7768, "center_y": 0.962},
                           {"center_x": 0.8560, "center_y": 0.962}]
        if self.ids.character_heart.is_visible:
            character_poses = [{"center_x": 0.1440, "center_y": 0.962},
                               {"center_x": 0.1953, "center_y": 0.962},
                               {"center_x": 0.2467, "center_y": 0.962},
                               {"center_x": 0.2980, "center_y": 0.962},
                               {"center_x": 0.3493, "center_y": 0.962},
                               {"center_x": 0.4006, "center_y": 0.962},
                               {"center_x": 0.4520, "center_y": 0.962},
                               {"center_x": 0.5033, "center_y": 0.962},
                               {"center_x": 0.5547, "center_y": 0.962},
                               {"center_x": 0.6060, "center_y": 0.962}]
        support_poses = [{"center_x": 0.1220000, "center_y": 0.522360},
                         {"center_x": 0.1893925, "center_y": 0.540340},
                         {"center_x": 0.2567850, "center_y": 0.558320},
                         {"center_x": 0.8780000, "center_y": 0.398564},
                         {"center_x": 0.7960200, "center_y": 0.377622},
                         {"center_x": 0.7140400, "center_y": 0.356680},
                         {"center_x": 0.2826200, "center_y": 0.356680},
                         {"center_x": 0.2290800, "center_y": 0.370670},
                         {"center_x": 0.1755400, "center_y": 0.384660},
                         {"center_x": 0.1220000, "center_y": 0.398637}]
        star_list_data = Star.update_stars_from_character(self.character, character_size, character_poses)
        star_list_data = star_list_data + Star.update_stars_from_character(self.support, support_size, support_poses)
        # self.star_data = {}
        # if self.character is not None:
        #     for index in range(1, 11):
        #         if not self.make_star(self.character, index, index):
        #             break
        # if self.support is not None:
        #     for index in range(1, 11):
        #         if not self.make_star(self.support, index, index + 10):
        #             break
        self.star_list_data = star_list_data

    # def make_star(self, character, rank, index):
        # if f'star_{index}' in self.star_data:
        #     if self.star_data[f'star_{index}']['broken']:
        #         return True
        #     if character.get_rank(rank).broken:
        #         self.star_data[f'star_{index}']['broken'] = True
        #         self.star_data[f'star_{index}']['source'] = 'screens/stats/rankbrk.png'
        #         return True
        # if character.get_rank(rank).is_unlocked():
        #     sub = ""
        #     if 1 < index < 11:
        #         sub = ".one"
        #         if self.ids.character_heart.is_visible:
        #             sub = ".two"
        #     star = {'id': f'star_{index}',
        #             'source': 'screens/stats/star.png',
        #             'size_hint': Refs.app.get_dkey(f'fcp.star_{index} s_h'),
        #             'pos_hint': Refs.app.get_dkey(f'fcp.star_{index}{sub} p_h')}
        #     if character.get_rank(rank).is_broken():
        #         star['source'] = 'screens/stats/rankbrk.png'
        #         star['broken'] = True
        #     else:
        #         star['broken'] = False
        #     self.star_data[f'star_{index}'] = star
        #     return True
        # else:
        #     return False

    def update_buttons(self):
        if self.support is not None:
            self.char_button_source = 'buttons/char_button_full'
            self.support_button_source = 'buttons/support_button_full'
            self.char_button_collide_image = 'buttons/char_button_full.collision.png'
        else:
            self.char_button_source = 'buttons/char_button'
            self.support_button_source = 'buttons/support_button'
            if self.is_select or self.locked:
                self.support_button_collide_image = 'buttons/support_button.normal.png'
                self.char_button_collide_image = 'buttons/char_button_select.collision.png'
            else:
                self.support_button_collide_image = 'buttons/support_button.collision.png'
                self.char_button_collide_image = 'buttons/char_button.collision.png'

    def reload(self):
        total, gold, bonus, hint_text = Refs.gc.calculate_familiarity_bonus(self.character)
        self.ids.character_heart.is_visible = total != -1
        if total != -1:
            self.ids.character_heart.familiarity = total
            self.ids.character_heart.familiarity_gold = gold
            self.char_hint_text = hint_text
            if self.char_hint_showing:
                self.hint_text = self.char_hint_text
            self.character.familiarity_bonus = 1 + bonus / 100
        else:
            self.character.familiarity_bonus = 1
        if self.support is not None:
            total, gold, bonus, hint_text = Refs.gc.calculate_familiarity_bonus(self.support)
            # support calculation will never return false. Base char will always be there
            self.ids.support_heart.familiarity = total
            self.ids.support_heart.familiarity_gold = gold
            self.support_hint_text = hint_text
            if self.support_hint_showing:
                self.hint_text = self.support_hint_text
            self.support.familiarity_bonus = 1 + bonus / 100
        self.update_labels()
        self.update_stars()
        self.ids.stars.force_reload()

    def on_locked(self, *args):
        self.update_overlay()
        self.update_buttons()

    def on_char_hint_open(self, *args):
        if self.char_hint_showing or self.support_hint_showing:
            return
        self.hint_text = self.char_hint_text
        self.ids.hint.opacity = 1
        self.ids.hint.disabled = False
        self.char_hint_showing = True

    def on_char_hint_close(self, *args):
        if not self.char_hint_showing:
            return
        self.ids.hint.opacity = 0
        self.ids.hint.disabled = True
        self.char_hint_showing = False

    def on_support_hint_open(self, *args):
        if self.support_hint_showing or self.char_hint_showing:
            return
        self.hint_text = self.support_hint_text
        self.ids.hint.opacity = 1
        self.ids.hint.disabled = False
        self.support_hint_showing = True

    def on_support_hint_close(self, *args):
        if not self.support_hint_showing:
            return
        self.ids.hint.opacity = 0
        self.ids.hint.disabled = True
        self.support_hint_showing = False

    def update_lock(self, locked):
        self.locked = locked

    # def is_valid_touch(self, *args):
    #     if not self.has_screen:
    #         return True
    #     else:
    #         current = self.preview.portfolio.parent.parent.current_slide
    #         if current == self.preview.portfolio:
    #             return True
    #     return False

    def handle_preview_click(self):
        if not self.is_select:
            self.preview.show_select_screen(self, False)
            return
        if self.is_support:
            self.preview.set_char_screen(True, self.preview.char, self.character)
        else:
            self.preview.set_char_screen(True, self.character, self.preview.support)
        Refs.gs.get_screen('dungeon_main').update_party_score()
        Refs.gs.display_screen(None, False, False)
