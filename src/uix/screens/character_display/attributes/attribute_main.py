# Project Imports
# Kivy Imports
from kivy.properties import DictProperty, ListProperty, NumericProperty, ObjectProperty, StringProperty

# KV Import
from game.equipment import BOOTS, CHEST, GLOVES, GRIEVES, HELMET, NECKLACE, RING, VAMBRACES, WEAPON
from loading.kv_loader import load_kv
from refs import Refs
# UIX Imports
from uix.modules.screen import Screen

load_kv(__name__)


class CharacterAttributeScreen(Screen):
    preview = ObjectProperty(None, allownone=True)
    char = NumericProperty(-1)

    overlay_background_source = StringProperty('stat_background.png')
    overlay_source = StringProperty('stat_background_overlay.png')
    flag_source = StringProperty('flags/char_type_flag.png')
    overlay_bar_source = StringProperty('overlay_bar.png')
    neat_stat_overlay_source = StringProperty('stat_overlay.png')
    skills_switch_text = StringProperty('Skills')

    star_data = DictProperty({})
    star_list_data = ListProperty([])

    char_name = StringProperty('')
    char_display_name = StringProperty('')
    char_type_flag = StringProperty('')
    char_attack_flag = StringProperty('')
    char_element_flag = StringProperty('')

    char_image_source = StringProperty('')
    char_symbol_source = StringProperty('')

    family_name = StringProperty('No Family')
    score = StringProperty('Score: 0')
    floor_depth = StringProperty('Floor Depth: 0')
    race = StringProperty('Race: None')
    worth = StringProperty('Worth: 0')
    monsters_slain = StringProperty('Monsters Slain: 0')
    gender = StringProperty('Gender: None')
    high_dmg = StringProperty('High Dmg.: 0')
    people_slain = StringProperty('People Slain: 0')

    def __init__(self, character, preview, **kwargs):
        self.char = character
        char = Refs.gc.get_char_by_index(character)
        self.name = 'char_attr_' + char.get_id()
        self.char_name = char.get_name()
        self.char_display_name = char.get_display_name()
        self.char_type_flag = 'Supporter' if char.is_support() else 'Adventurer'
        self.char_attack_flag = char.get_attack_type_string()
        self.char_element_flag = char.get_element_string()
        self.char_image_source = char.get_image('full')
        self.char_symbol_source = char.get_image('symbol')
        self.preview = preview
        super().__init__(**kwargs)
        self.update_stars()
        self.update_info()
        self.update_skills()
        self.ids.total_abilities_box.reload()
        self.ids.rank_abilities_box.reload()

    # def on_touch_hover(self, touch):
    #     if self.ids.image_preview.dispatch('on_touch_hover', touch):
    #         return True
    #     if self.ids.change_equip.dispatch('on_touch_hover', touch):
    #         return True
    #     if self.ids.status_board.dispatch('on_touch_hover', touch):
    #         return True
    #     return False

    def on_image_preview(self):
        char = Refs.gc.get_char_by_index(self.char)
        Refs.gs.display_screen('image_preview_' + char.get_id(), True, True, self.char)

    def on_leave(self, *args):
        if self.skills_switch_text == 'Status':
            self.on_skills_switch()

    def on_status_board(self):
        char = Refs.gc.get_char_by_index(self.char)
        Refs.gs.display_screen('status_board_' + char.get_id(), True, True, self.char)

    def on_skills_switch(self):
        if self.skills_switch_text == 'Skills':
            self.skills_switch_text = 'Status'
        else:
            self.skills_switch_text = 'Skills'
        self.ids.normal_layout.opacity = int(not bool(int(self.ids.normal_layout.opacity)))
        self.ids.skill_layout.opacity = int(not bool(int(self.ids.skill_layout.opacity)))
        self.ids.skills_list.scroll_y = 1
        self.ids.skills_list.update_from_scroll()

    def on_change_equip(self):
        char = Refs.gc.get_char_by_index(self.char)
        Refs.gs.display_screen('equipment_change_' + char.get_id(), True, True, char=self.char)

    def goto_char_attr(self, direction):
        next_char_index = Refs.gc.get_next_char(self.char, direction)
        next_char = Refs.gc.get_char_by_index(next_char_index)
        Refs.gs.display_screen('char_attr_' + next_char.get_id(), True, False, next_char_index, self.preview)

    def update_stars(self):
        if self.char != -1:
            char = Refs.gc.get_char_by_index(self.char)
            for index in range(1, 11):
                if not self.make_star(char, index, index):
                    break
        self.star_list_data = self.star_data.values()

    def make_star(self, character, rank, index):
        if f'star_{index}' in self.star_data:
            if self.star_data[f'star_{index}']['broken']:
                return True
            if character.get_rank(rank).is_broken():
                self.star_data[f'star_{index}']['broken'] = True
                self.star_data[f'star_{index}']['source'] = 'icons/rankbrk.png'
                return True
        if character.get_rank(rank).is_unlocked():
            star = {'id': f'star_{index}',
                    'source': 'icons/star.png',
                    'size_hint': Refs.app.get_dkey(f'cas.star_{index} s_h'),
                    'pos_hint': Refs.app.get_dkey(f'cas.star_{index} p_h')}
            if character.get_rank(rank).is_broken():
                star['source'] = 'icons/rankbrk.png'
                star['broken'] = True
            else:
                star['broken'] = False
            self.star_data[f'star_{index}'] = star
            return True
        else:
            return False

    def update_info(self):
        if self.char == -1:
            return
        char = Refs.gc.get_char_by_index(self.char)
        self.family_name = str(char.get_family()) + " Family"
        self.score = "Score: " + str(char.get_score())
        self.floor_depth = "Floor Depth: " + str(char.get_floor_depth())
        self.race = "Race: " + str(char.get_race())
        self.worth = "Worth: " + str(char.get_worth())
        self.monsters_slain = "Monsters Slain: " + str(char.get_monsters_killed())
        self.gender = "Gender: " + str(char.get_gender())
        self.high_dmg = "High Dmg.: " + str(char.get_high_damage())
        self.people_slain = "People Slain: " + str(char.get_people_killed())

    def update_skills(self):
        char = Refs.gc.get_char_by_index(self.char)
        if char.is_support():
            skills = [char.get_support_skill()]
        else:
            skills = char.get_all_skills()

        self.ids.skills_list.set_combat_skills(char.is_support(), skills)

    def update_items(self):
        if self.char is None:
            return
        char = Refs.gc.get_char_by_index(self.char)
        outfit = char.get_equipment()
        self.ids.weapon.item = outfit.get_equipment(WEAPON)
        self.ids.necklace = outfit.get_equipment(NECKLACE)
        self.ids.ring = outfit.get_equipment(RING)
        self.ids.helmet = outfit.get_equipment(HELMET)
        self.ids.vambraces = outfit.get_equipment(VAMBRACES)
        self.ids.gloves = outfit.get_equipment(GLOVES)
        self.ids.chest = outfit.get_equipment(CHEST)
        self.ids.grieves = outfit.get_equipment(GRIEVES)
        self.ids.boots = outfit.get_equipment(BOOTS)

    def reload(self, *args):
        #TODO: Reload stars
        self.update_stars()
        self.ids.stars.force_reload()
        #TODO: Reload stats & abilities
        self.ids.stats.reload()
        self.ids.total_abilities_box.reload()
        self.ids.rank_abilities_box.reload()
        #TODO: Reload info
        self.update_info()
        #TODO: Reload equipment?
        self.update_items()
        #TODO: Call Dungeon Main Reload
        dungeon_main = Refs.gs.get_screen('dungeon_main')
        if dungeon_main is not None:
            dungeon_main.reload()
        select = Refs.gs.get_screen('select_char')
        if select is not None:
            select.reload()
