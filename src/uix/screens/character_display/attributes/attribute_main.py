# Project Imports
# Kivy Imports
from kivy.properties import DictProperty, ListProperty, ObjectProperty, StringProperty

# KV Import
from loading.kv_loader import load_kv
from refs import Refs
# UIX Imports
from uix.modules.screen import Screen

load_kv(__name__)


class CharacterAttributeScreen(Screen):
    preview = ObjectProperty(None, allownone=True)
    char = ObjectProperty(None, allownone=True)

    overlay_background_source = StringProperty('screens/attributes/stat_background.png')
    overlay_source = StringProperty('screens/attributse/stat_background_overlay.png')
    flag_source = StringProperty('screens/attributes/char_type_flag.png')
    overlay_bar_source = StringProperty('screens/stats/overlay_bar.png')
    neat_stat_overlay_source = StringProperty('screens/attributes/stat_overlay.png')
    skills_switch_text = StringProperty('Skills')

    star_data = DictProperty({})
    star_list_data = ListProperty([])

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
        self.preview = preview
        super().__init__(**kwargs)
        self.update_stars()
        self.update_info()
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
        Refs.gs.display_screen('image_preview_' + self.char.get_id(), True, True, char=self.char)

    def on_leave(self, *args):
        if self.skills_switch_text == 'Status':
            self.on_skills_switch()

    def on_status_board(self):
        Refs.gs.display_screen('status_board_' + self.char.get_id(), True, True, char=self.char)

    def on_skills_switch(self):
        if self.skills_switch_text == 'Skills':
            self.skills_switch_text = 'Status'
        else:
            self.skills_switch_text = 'Skills'
        self.ids.normal_layout.opacity = int(not bool(int(self.ids.normal_layout.opacity)))
        self.ids.skill_layout.opacity = int(not bool(int(self.ids.skill_layout.opacity)))
        self.ids.skillslist.scroll_y = 1
        self.ids.skillslist.update_from_scroll()

    def on_change_equip(self):
        Refs.gs.display_screen('equipment_change_' + self.char.get_id(), True, True, self.char)

    def goto_char_attr(self, direction):
        next_char = Refs.gc.get_next_char(self.char, direction)
        Refs.gs.display_screen('char_attr_' + next_char.get_id(), True, False, next_char, self.preview)

    def update_stars(self):
        if self.char is not None:
            for index in range(1, 11):
                if not self.make_star(self.char, index, index):
                    break
        self.star_list_data = self.star_data.values()

    def make_star(self, character, rank, index):
        if f'star_{index}' in self.star_data:
            if self.star_data[f'star_{index}']['broken']:
                return True
            if character.get_rank(rank).is_broken():
                self.star_data[f'star_{index}']['broken'] = True
                self.star_data[f'star_{index}']['source'] = 'screens/stats/rankbrk.png'
                return True
        if character.get_rank(rank).is_unlocked():
            star = {'id': f'star_{index}',
                    'source': 'screens/stats/star.png',
                    'size_hint': Refs.app.get_dkey(f'cas.star_{index} s_h'),
                    'pos_hint': Refs.app.get_dkey(f'cas.star_{index} p_h')}
            if character.get_rank(rank).is_broken():
                star['source'] = 'screens/stats/rankbrk.png'
                star['broken'] = True
            else:
                star['broken'] = False
            self.star_data[f'star_{index}'] = star
            return True
        else:
            return False

    def update_info(self):
        if self.char is None:
            return
        self.family_name = str(self.char.get_family()) + " Family"
        self.score = "Score: " + str(self.char.get_score())
        self.floor_depth = "Floor Depth: " + str(self.char.get_floor_depth())
        self.race = "Race: " + str(self.char.get_race())
        self.worth = "Worth: " + str(self.char.get_worth())
        self.monsters_slain = "Monsters Slain: " + str(self.char.get_monsters_killed())
        self.gender = "Gender: " + str(self.char.get_gender())
        self.high_dmg = "High Dmg.: " + str(self.char.get_high_damage())
        self.people_slain = "People Slain: " + str(self.char.get_people_killed())

    def update_items(self):
        if self.char is None:
            return
        equipment = self.char.get_equipment()
        self.ids.weapon.item = equipment.weapon
        self.ids.necklace = equipment.necklace
        self.ids.ring = equipment.ring
        self.ids.helmet = equipment.helmet
        self.ids.vambraces = equipment.vambraces
        self.ids.gloves = equipment.gloves
        self.ids.chest = equipment.chest
        self.ids.grieves = equipment.grieves
        self.ids.boots = equipment.boots

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
        Refs.gs.get_screen('dungeon_main').reload()
        Refs.gs.get_screen('select_char').reload()

