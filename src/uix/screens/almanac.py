from kivy.properties import BooleanProperty, ListProperty, NumericProperty, StringProperty
from kivy.uix.relativelayout import RelativeLayout

from loading.kv_loader import load_kv
from refs import Refs
from uix.modules.screen import Screen

load_kv(__name__)


class Almanac(Screen):
    def __init__(self, **kwargs):
        self.headers = ['characters', 'enemies', 'domains', 'perks', 'floors', 'materials', 'housing']
        self.header_to_string = {
            'characters': 'Characters',
            'enemies':    'Enemies',
            'domains':    'Domains',
            'perks':      'Perks',
            'floors':     'Floors',
            'materials':  'Materials',
            'housing':    'Housing'
        }
        self.header_to_image = {
            'characters': 'Characters',
            'enemies':    'Enemies',
            'domains':    'Domains',
            'perks':      'Perks',
            'floors':     'Floors',
            'materials':  'Materials',
            'housing':    'Housing'
        }

        self._displayed_type = None
        self._displayed_obj = None

        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        panel = self.ids.browser
        for header in self.headers:
            child = AlmanacHeader()
            child.header = self.header_to_string[header]
            child.image_source = self.header_to_image[header]
            child.base_height = self.height * 0.0772

            self.get_almanac_objects(child, header)
            panel.add_widget(child)

    def on_height(self, *args):
        if 'browser' not in self.ids:
            return
        for child in self.ids.browser.children:
            child.base_height = self.height * 0.0772

    def get_almanac_objects(self, parent, header):
        if header == 'characters':
            chars = Refs.gc.get_characters()
            for char in chars:
                child = AlmanacObject()
                child.header = char.get_name()
                child.image_source = char.get_image('preview')
                child.set_object(self, char, 'char')
                parent.add_child(child)
        else:
            pass

    def display_almanac(self, type, object):
        if self._displayed_type == type:
            if self._displayed_obj == object:
                if self._displayed_obj is not None:
                    self.ids.panel_parent.remove_widget(self.ids.almanac_panel)
                self._displayed_obj = None
                self._displayed_type = None
                return
            self._displayed_obj = object
            self.ids.almanac_panel.reload(object)
        else:
            self.replace_almanac(type, object)

    def replace_almanac(self, type, object):
        if type == 'char':
            panel = AlmanacCharacterPanel()
        else:
            panel = None

        if self._displayed_obj is not None:
            self.ids.panel_parent.remove_widget(self.ids.almanac_panel)
        self.ids.panel_parent.add_widget(panel)
        self.ids['almanac_panel'] = panel
        self.ids.almanac_panel.reload(object)

        self._displayed_type = type
        self._displayed_obj = object




class AlmanacHeader(RelativeLayout):
    header = StringProperty('')
    image_source = StringProperty('')

    base_height = NumericProperty(0)
    panel_height = NumericProperty(0)
    children_displayed = BooleanProperty(False)

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.on_panel_height()

    def on_panel_height(self, *args):
        if self.children_displayed:
            self.ids.child_layout.height = self.panel_height
            self.ids.child_layout.opacity = 1
        else:
            self.ids.child_layout.height = 0
            self.ids.child_layout.opacity = 0

    def on_base_height(self, *args):
        if 'child_layout' not in self.ids:
            return
        for child in self.ids.child_layout.children:
            child.height = self.base_height

    def add_child(self, object):
        object.height = self.base_height
        self.ids.child_layout.add_widget(object)

    def do_callback(self):
        self.children_displayed = not self.children_displayed
        self.on_panel_height()


class AlmanacObject(RelativeLayout):
    header = StringProperty('')
    image_source = StringProperty('')

    def __init__(self, **kwargs):
        self._screen = None
        self._object = None
        self._type = type
        super().__init__(**kwargs)

    def set_object(self, screen, object, type):
        self._screen = screen
        self._object = object
        self._type = type

    def do_callback(self):
        self._screen.display_almanac(self._type, self._object)


class AlmanacCharacterPanel(RelativeLayout):
    character_source = StringProperty('')
    display_name = StringProperty('')
    full_name = StringProperty('')

    char_type = StringProperty('')
    attack_type = StringProperty('')
    element = StringProperty('')

    race = StringProperty('')
    gender = StringProperty('')
    age = StringProperty('')
    description = StringProperty('')

    favorite_weapon = StringProperty('')
    favorite_sub_weapon = StringProperty('')

    recruitment_items = ListProperty([])
    starting_stats = ListProperty([])

    def __init__(self, **kwargs):
        self._skills_list = None
        super().__init__(**kwargs)

    def reload(self, char):
        self.character_source = char.get_image('full')
        self.display_name = char.get_display_name()
        self.full_name = char.get_name()

        if char.is_support():
            self.char_type = 'Supporter'
        else:
            self.char_type = 'Adventurer'
            self.attack_type = char.get_attack_type_string()
            self.element = char.get_element_string()

        self.race = char.get_race()
        self.gender = char.get_gender()
        self.age = str(char.get_age())
        self.description = char.get_description()

        self.favorite_weapon = ''
        self.favorite_sub_weapon = ''
        if not char.is_support():
            self.favorite_weapon = f'Favorite weapon is a {char.get_favorite_weapon()}'
            if char.get_favorite_sub_weapon() is not None:
                self.favorite_sub_weapon = f'Favorite sub-weapon is a {char.get_favorite_sub_weapon()}'

        self.recruitment_items = []
        for (recruitment_item_id, item_count) in char.get_recruitment_items().items():
            item = Refs.gc.find_item(recruitment_item_id)
            if item is None:
                print(f'Can\'t locate {recruitment_item_id}')
                continue
            data = {'title': item.get_name(), 'count': f'x{item_count}', 'image_source': item.get_image()}
            self.recruitment_items.append(data)

        self.starting_stats = []
        icons = {'Health': 'icons/Hea.png', 'Mana': 'icons/Mna.png', 'Strength': 'icons/Str.png', 'Magic': 'icons/Mag.png', 'Endurance': 'icons/End.png', 'Agility': 'icons/Agi.png', 'Dexterity': 'icons/Dex.png'}
        for title, value in char.get_base_stats().items():
            data = {'title': title, 'value': value, 'image_source': icons[title]}
            self.starting_stats.append(data)

        if char.is_support():
            skills = [char.get_support_skill()]
        else:
            skills = char.get_all_skills()

        self.ids.skills_list.set_combat_skills(char.is_support(), skills)
        self.ids.skills_list.do_scroll_y = False
        self.ids.skills_list.do_scroll_x = False

    def on_size(self, *args):
        print(f'Panel Size: {self.size}')


class RecruitmentItem(RelativeLayout):
    image_source = StringProperty('')
    title = StringProperty('')
    count = StringProperty('')


class StatItem(RelativeLayout):
    title = StringProperty('')
    value = NumericProperty(0)
    image_source = StringProperty('')


#
# class StatBox(RelativeLayout):
#     color = ListProperty([0, 0, 0, 1])
#     number_color = ListProperty([0, 0, 0, 1])
#     font = StringProperty('')
#
#     char = ObjectProperty(None)
#
#     health = NumericProperty(0.0)
#     mana = NumericProperty(0.0)
#     phy_attack = NumericProperty(0.0)
#     mag_attack = NumericProperty(0.0)
#     defense = NumericProperty(0.0)
#
#     stat_bar_source = StringProperty('')
#     health_source = StringProperty('')
#     mana_source = StringProperty('')
#     phy_attack_source = StringProperty('')
#     mag_attack_source = StringProperty('')
#     defense_source = StringProperty('')
#
#     def __init__(self, **kwargs):
#         self.stat_bar_source = 'stat_bar.png'
#         self.health_source = 'icons/Hea.png'
#         self.mana_source = 'icons/Mna.png'
#         self.phy_attack_source = 'icons/PAtk.png'
#         self.mag_attack_source = 'icons/MAtk.png'
#         self.defense_source = 'icons/Def.png'
#         super().__init__(**kwargs)
#
#     def on_char(self, *args):
#         self.reload()
#
#     def reload(self):
#         if self.char == -1:
#             return
#         char = Refs.gc.get_char_by_index(self.char)
#         self.health = char.get_health()
#         self.mana = char.get_mana()
#         self.phy_attack = char.get_physical_attack()
#         self.mag_attack = char.get_magical_attack()
#         self.defense = char.get_defense()