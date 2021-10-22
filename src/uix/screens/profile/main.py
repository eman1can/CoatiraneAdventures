from math import floor

from kivy.properties import BooleanProperty, ListProperty, NumericProperty, StringProperty

from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from loading.kv_loader import load_kv
from refs import Refs
from uix.modules.screen import Screen

load_kv(__name__)


class ProfileMain(Screen):
    name_string = StringProperty('')
    gender_source = StringProperty('')
    domain_source = StringProperty('')
    domain_desc = StringProperty('')
    domain_stats = StringProperty('')
    about_desc = StringProperty('')
    renown_source = StringProperty('')
    info_desc = StringProperty('')
    perks_visible = BooleanProperty(False)

    def __init__(self, **kwargs):
        self.perks = {}
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        self.name_string = Refs.gc.get_name()
        self.gender_source = f'family/{Refs.gc.get_gender()}.png'
        self.domain_source = f'family/domains/{Refs.gc.get_domain()}.png'

        domain = Refs.gc.get_domain_info()
        domain_desc = domain.get_large_description()
        if Refs.gc.get_gender() == 'female':
            domain_desc.replace('diety', 'goddess')
        elif Refs.gc.get_gender() == 'male':
            domain_desc.replace('diety', 'god')

        self.domain_desc, self.domain_stats = domain_desc.split('\n\n')
        about_desc = f'Renown - {Refs.gc.get_renown()}'
        about_desc += f'\nCurrent Perk Points - {Refs.gc.get_perk_points()}'
        about_desc += f'\nPerks Unlocked {Refs.gc.get_skill_level()}'
        about_desc += f'\nYou have {Refs.gc.format_number(Refs.gc.get_varenth())} Varenth'
        self.about_desc = about_desc
        self.renown_source = f'icons/{Refs.gc.get_renown()}.png'
        self.info_desc = f'Current Perk Points - {Refs.gc.get_perk_points()}'
        self.info_desc += f'\nPerks Unlocked - {Refs.gc.get_skill_level()}'
        self.info_desc += f'\nYou have {Refs.gc.format_number(Refs.gc.get_varenth())} Varenth'
        self.perks_visible = Refs.gc.get_skill_level() > 0
        if self.perks_visible:
            indexes = Refs.gc.get_all_obtained_character_indexes()
            for index in indexes:
                char = Refs.gc.get_char_by_index(index)
                for perk_id in char.get_perks():
                    tree = Refs.gc['perks'][perk_id].get_tree()
                    if tree not in self.perks:
                        self.perks[tree] = {}
                    if perk_id not in self.perks[tree]:
                        self.perks[tree][perk_id] = []
                    self.perks[tree][perk_id].append(char)

            for tree, perk_list in self.perks.items():
                tree_title = TreeLabel(text=tree.title())
                self.ids.scroll.add_widget(tree_title)
                for perk_id, char_list in perk_list.items():
                    perk = Refs.gc['perks'][perk_id]
                    perk_title = PerkLabel(text=perk.get_name())
                    self.ids.scroll.add_widget(perk_title)
                    perk_display = CharacterList(char_list)
                    perk_display.height = self.height * 0.05
                    self.ids.scroll.add_widget(perk_display)

    def on_height(self, instance, new_height):
        for child in self.ids.scroll.children:
            if isinstance(child, CharacterList):
                child.height = self.height * 0.05

    def on_skill_tree(self):
        Refs.gs.display_screen('skill_tree_main', True, True, self.perks)


class TreeLabel(Label):
    pass


class PerkLabel(Label):
    pass


class CharacterList(RelativeLayout):
    def __init__(self, char_list, **kwargs):
        self.char_list = char_list
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        size = self.height
        for char in self.char_list:
            self.ids.images.add_widget(Image(source=char.get_image('preview'), size_hint=(None, None), size=(size, size)))

    def on_height(self, instance, new_height):
        size = self.height
        for image in self.ids.images.children:
            image.size = (size, size)
