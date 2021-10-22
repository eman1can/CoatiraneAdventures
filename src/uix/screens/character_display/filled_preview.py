# Project Imports
# Kivy Imports
from kivy.properties import BooleanProperty, DictProperty, ListProperty, NumericProperty, ObjectProperty, StringProperty

from kivy.uix.relativelayout import RelativeLayout
# KV Import
from loading.kv_loader import load_kv
from refs import Refs
# UIX Imports
from uix.modules.screen import Screen
from uix.modules.star import Star

# from uix.screens.character_display.heart_indicator import HeartIndicator
load_kv(__name__)


class FilledCharacterPreviewScreen(Screen):
    is_support = BooleanProperty(False)
    locked = BooleanProperty(False)
    current = BooleanProperty(True)

    character = NumericProperty(-1)
    support = NumericProperty(-1)

    def __init__(self, **kwargs):
        # self._post_kv = False
        super().__init__(**kwargs)
    #
    # def on_kv_post(self, base_widget):
    #     self._post_kv = True
    #     self.ids.filled_preview.character = self.character
    #     self.ids.filled_preview.support = self.support

    def get_root(self):
        return self.ids.filled_preview

    def on_character(self, instance, character):
        self.update_name()

    def on_support(self, instance, support):
        self.update_name()

    def update_name(self):
        if self.character == -1:
            return
        char = Refs.gc.get_char_by_index(self.character)
        supt = Refs.gc.get_char_by_index(self.support)
        self.name = char.get_id()
        if supt is not None:
            self.name += '_' + supt.get_id()

    def on_locked(self, instance, locked):
        self.ids.filled_preview.locked = locked

    def on_current(self, instance, current):
        self.ids.filled_preview.current = current

    def close_hints(self):
        self.ids.filled_preview.close_hints()

    def reload(self):
        self.ids.filled_preview.reload()


class FilledCharacterPreview(RelativeLayout):
    is_select = BooleanProperty(False)
    is_support = BooleanProperty(False)
    locked = BooleanProperty(False)
    current = BooleanProperty(True)
    do_hover = BooleanProperty(True)

    character = NumericProperty(-1)
    support = NumericProperty(-1)

    attack_type = StringProperty('')
    element_type = StringProperty('')

    text_color = ListProperty([0.796, 0.773, 0.678, 1])
    font_name = StringProperty('Gabriola')

    new_image_instance = BooleanProperty(False)
    has_screen = BooleanProperty(False)
    has_tag = BooleanProperty(False)
    has_stat = BooleanProperty(False)

    preview_wgap = NumericProperty(0)
    preview_hgap = NumericProperty(0)
    image_width = NumericProperty(0)

    char_hint_showing = BooleanProperty(False)
    support_hint_showing = BooleanProperty(False)
    hint_text = DictProperty({})
    char_hint_text = DictProperty({})
    support_hint_text = DictProperty({})

    char_button_source = StringProperty('')
    support_button_source = StringProperty('')
    char_button_collide_image = StringProperty('')
    support_button_collide_image = StringProperty('')

    background_source = StringProperty('preview_background.png')
    support_background_source = StringProperty('preview_support_background.png')
    char_image_source = StringProperty('')
    support_image_source = StringProperty('')
    overlay_source = StringProperty('')
    support_overlay_source = StringProperty('preview_support_background_overlay.png')

    number_text = StringProperty('0\n0\n0\n0\n0\n0\n0\n0\n0\n0')

    star_list_data = ListProperty([])
    stat_list_data = ListProperty([])

    def __init__(self, **kwargs):
        self.register_event_type('on_select')
        self.register_event_type('on_return')
        self.register_event_type('on_attr')
        self.register_event_type('on_empty')
        self.stat_list_data = [
            {'id': 'phy_atk_image',
             'source': 'icons/PAtk.png',
             'size_hint': Refs.app.get_dkey('fcp.img s_h'),
             'pos_hint': Refs.app.get_dkey('fcp.img.phy_atk p_h')},
            {'id':        'mag_atk_image',
             'source':    'icons/MAtk.png',
             'size_hint': Refs.app.get_dkey('fcp.img s_h'),
             'pos_hint':  Refs.app.get_dkey('fcp.img.mag_atk p_h')},
            {'id':        'health_image',
             'source':    'icons/Hea.png',
             'size_hint': Refs.app.get_dkey('fcp.img s_h'),
             'pos_hint':  Refs.app.get_dkey('fcp.img.health p_h')},
            {'id':        'mana_image',
             'source':    'icons/Mna.png',
             'size_hint': Refs.app.get_dkey('fcp.img s_h'),
             'pos_hint':  Refs.app.get_dkey('fcp.img.mana p_h')},
            {'id':        'defense_image',
             'source':    'icons/Def.png',
             'size_hint': Refs.app.get_dkey('fcp.img s_h'),
             'pos_hint':  Refs.app.get_dkey('fcp.img.defense p_h')},
            {'id':        'strength_image',
             'source':    'icons/Str.png',
             'size_hint': Refs.app.get_dkey('fcp.img s_h'),
             'pos_hint':  Refs.app.get_dkey('fcp.img.strength p_h')},
            {'id':        'magic_image',
             'source':    'icons/Mag.png',
             'size_hint': Refs.app.get_dkey('fcp.img s_h'),
             'pos_hint':  Refs.app.get_dkey('fcp.img.magic p_h')},
            {'id':        'endurance_image',
             'source':    'icons/End.png',
             'size_hint': Refs.app.get_dkey('fcp.img s_h'),
             'pos_hint':  Refs.app.get_dkey('fcp.img.endurance p_h')},
            {'id':        'dexterity_image',
             'source':    'icons/Agi.png',
             'size_hint': Refs.app.get_dkey('fcp.img s_h'),
             'pos_hint':  Refs.app.get_dkey('fcp.img.dexterity p_h')},
            {'id':        'agility_image',
             'source':    'icons/Dex.png',
             'size_hint': Refs.app.get_dkey('fcp.img s_h'),
             'pos_hint':  Refs.app.get_dkey('fcp.img.agility p_h')},
        ]
        self.update_overlay()
        self.update_buttons()
        self.update_labels()
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        if not self.is_select:
            self.update_familiarity()
        self.update_stars()
        self.ids.stars.force_reload()

    def reload(self):
        self.update_overlay()
        self.update_buttons()
        self.update_labels()
        if not self.is_select:
            self.update_familiarity()
        self.update_stars()
        self.ids.stars.force_reload()

    # Update functions for reloading the data based on updates

    def update_familiarity(self):
        total, gold, bonus, hint_text = Refs.gc.calculate_familiarity_bonus(self.character)
        self.ids.character_heart.is_visible = total != -1
        self.ids.support_heart.is_visible = False
        if total != -1:
            self.ids.character_heart.familiarity = total
            self.ids.character_heart.familiarity_gold = gold
            self.char_hint_text = hint_text
            if self.char_hint_showing:
                self.hint_text = self.char_hint_text
            if self.support != -1:
                total, gold, bonus, hint_text = Refs.gc.calculate_familiarity_bonus(self.support)
                # support calculation will never return false. Base char will always be there
                self.ids.support_heart.is_visible = True
                self.ids.support_heart.familiarity = total
                self.ids.support_heart.familiarity_gold = gold
                self.support_hint_text = hint_text
                if self.support_hint_showing:
                    self.hint_text = self.support_hint_text

    def update_overlay(self):
        if self.support != -1:
            self.overlay_source = "preview_overlay_full.png"
        elif not self.is_select and not self.locked:
            self.overlay_source = "preview_overlay_empty_add.png"
        else:
            self.overlay_source = "preview_overlay_empty.png"

    def get_label_values(self, character, values):
        values[0] += character.get_physical_attack()
        values[1] += character.get_magical_attack()
        values[2] += character.get_health()
        values[3] += character.get_mana()
        values[4] += character.get_defense()
        values[5] += character.get_strength()
        values[6] += character.get_magic()
        values[7] += character.get_endurance()
        values[8] += character.get_agility()
        values[9] += character.get_dexterity()
        return values

    def update_labels(self):
        values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        if self.character != -1:
            character = Refs.gc.get_char_by_index(self.character)
            self.get_label_values(character, values)

        if self.support != -1:
            support = Refs.gc.get_char_by_index(self.support)
            self.get_label_values(support, values)

        for index in range(len(values)):
            values[index] = round(values[index], 2)
        self.number_text = str(values[0])
        for x in range(1, 10):
            self.number_text += f'\n{values[x]}'

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
        character = Refs.gc.get_char_by_index(self.character)
        support = Refs.gc.get_char_by_index(self.support)
        star_list_data = Star.update_stars_from_character(character, character_size, character_poses)
        star_list_data = star_list_data + Star.update_stars_from_character(support, support_size, support_poses)
        self.star_list_data = star_list_data

    def update_buttons(self):
        if self.support != -1:
            self.char_button_source = 'buttons/char_button_full'
            self.support_button_source = 'buttons/support_button_full'
            self.support_button_collide_image = 'buttons/support_button_full.collision.png'
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

    # Update functions based on callbacks

    def on_is_select(self, instance, select):
        self.update_overlay()
        self.update_buttons()
        self.update_labels()

    def on_character(self, instance, char_index):
        character = Refs.gc.get_char_by_index(char_index)
        self.char_image_source = character.get_image('slide')
        if not self.is_support:
            self.attack_type = character.get_attack_type_string()
            self.element_type = character.get_element_string()
        self.reload()

    def on_support(self, instance, support_index):
        support = Refs.gc.get_char_by_index(support_index)
        self.support_image_source = support.get_image('slide_support')
        self.reload()

    def on_locked(self, instance, locked):
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

    # Handling methods

    def close_hints(self):
        self.on_char_hint_close()
        self.on_support_hint_close()
        self.ids.character_heart.reset_open()
        self.ids.support_heart.reset_open()

    def is_click_valid(self):
        valid = True
        valid &= not self.locked
        valid &= not self.disabled
        valid &= self.current
        return valid

    def handle_left_click(self, is_support):
        if not self.is_click_valid():
            return
        if not self.is_select:
            self.dispatch('on_select', is_support)
            return
        if is_support:
            return
        self.dispatch('on_return', self.character)

    def handle_right_click(self, is_support):
        if not self.is_click_valid() or self.is_select:
            return
        self.dispatch('on_attr', is_support)

    def handle_long_click(self, is_support):
        if self.is_select:
            return
        self.dispatch('on_empty', is_support)

    # Empty callback methods
    def on_select(self, is_support):
        pass

    def on_return(self, character):
        pass

    def on_attr(self, is_support):
        pass

    def on_empty(self, is_support):
        pass
