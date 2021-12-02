# Project Imports
# Standard Library Imports
import random

# Kivy Imports
from kivy.properties import BooleanProperty, ListProperty, NumericProperty, StringProperty

# KV Import
from kivy.animation import Animation
from kivy.uix.relativelayout import RelativeLayout
from loading.kv_loader import load_kv
from refs import Refs
# UIX Imports
from uix.modules.screen import Screen

load_kv(__name__)


class DungeonResult(Screen):
    image_source = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        characters = [char for char in Refs.gc.get_current_party() if char != -1]
        character = Refs.gc.get_char_by_index(characters[random.randrange(0, len(characters))])
        self.image_source = character.get_image('full')

    def on_kv_post(self, base_widget):
        floor_data = Refs.gc.get_floor_data()
        items_gained = floor_data.get_gained_items()
        enemies_defeated = floor_data.get_killed()
        for item, count in floor_data.get_gained_items().items():
            Refs.gc.get_inventory().add_item(item.get_id(), count)
        self.ids.result_hud.set_enemies_defeated(enemies_defeated)
        self.ids.result_hud.set_items_obtained(items_gained)
        Refs.gc.reset_floor_data()

    def on_display_stats(self):
        anim = Animation(opacity=0, duration=0.2)
        anim.start(self.ids.character_image)
        anim.start(self.ids.result_hud)
        anim = anim + Animation(opacity=1, duration=0.2)
        anim.start(self.ids.stat_hud)
        self.ids.result_hud.disabled = True
        self.ids.stat_hud.disabled = False

    def on_stat_continue(self):
        if self.ids.stat_hud.disabled:
            return
        if self.ids.stat_hud_supports.characters == 0:
            Refs.gs.display_screen('dungeon_main', True, False, level=0)
            return
        anim = Animation(opacity=0, duration=0.2)
        anim.start(self.ids.stat_hud)
        anim = anim + Animation(opacity=1, duration=0.2)
        anim.start(self.ids.stat_hud_supports)
        self.ids.stat_hud.disabled = True
        self.ids.stat_hud_supports.disabled = False

    def on_support_stat_continue(self):
        if self.ids.stat_hud_supports.disabled:
            return
        Refs.gs.display_screen('dungeon_main', True, False, level=0)


class StatHud(RelativeLayout):
    supports = BooleanProperty(False)

    characters = NumericProperty(0)

    def on_kv_post(self, base_widget):
        self.display_characters(self.supports)

    def display_characters(self, supports=False):
        self.characters = 0
        increases, fam_bonus_increases = Refs.gc.get_floor_data().get_increases()
        party = Refs.gc.get_current_party()[8:] if supports else Refs.gc.get_current_party()[:8]
        print(increases, fam_bonus_increases)
        for index, char_index in enumerate(party):
            character = Refs.gc.get_char_by_index(char_index)
            if character is None:
                continue
            self.characters += 1
            self.add_widget(CharacterStatPreview(character, increases[char_index], fam_bonus_increases[char_index], size_hint=(0.109, 0.75), pos_hint={'x': 0.0142 + index * 0.1232, 'y': 0.125}))


class CharacterStatPreview(RelativeLayout):
    image_source = StringProperty('')
    text = StringProperty('')

    has_fam_increases = BooleanProperty(False)

    stat_list_data = ListProperty([])

    def __init__(self, character, increases, fam_bonus_increases, **kwargs):
        super().__init__(**kwargs)
        self.image_source = character.get_image('preview')

        self.stat_list_data = [
            {'id':        'health_image',
             'source':    'icons/Hea Black.png',
             'size_hint': (1, 0.1428),
             'pos_hint': {'center_y': 0.9282}},
            {'id':        'mana_image',
             'source':    'icons/Mna Black.png',
             'size_hint': (1, 0.1428),
             'pos_hint':  {'center_y': 0.7854}},
            {'id':        'strength_image',
             'source':    'icons/Str Black.png',
             'size_hint': (1, 0.1428),
             'pos_hint':  {'center_y': 0.6426}},
            {'id':        'magic_image',
             'source':    'icons/Mag Black.png',
             'size_hint': (1, 0.1428),
             'pos_hint':  {'center_y': 0.4998}},
            {'id':        'endurance_image',
             'source':    'icons/End Black.png',
             'size_hint': (1, 0.1428),
             'pos_hint':  {'center_y': 0.357}},
            {'id':        'dexterity_image',
             'source':    'icons/Agi Black.png',
             'size_hint': (1, 0.1428),
             'pos_hint':  {'center_y': 0.2142}},
            {'id':        'agility_image',
             'source':    'icons/Dex Black.png',
             'size_hint': (1, 0.1428),
             'pos_hint': {'center_y': 0.0714}},
        ]

        health = character.get_health()
        mana = character.get_mana()
        strength = character.get_strength()
        magic = character.get_magic()
        endurance = character.get_endurance()
        agility = character.get_agility()
        dexterity = character.get_dexterity()

        character.increase_health(increases[0])
        character.increase_mana(increases[1])
        character.increase_strength(increases[2])
        character.increase_magic(increases[3])
        character.increase_endurance(increases[4])
        character.increase_agility(increases[5])
        character.increase_dexterity(increases[6])

        new_health = character.get_health()
        new_mana = character.get_mana()
        new_strength = character.get_strength()
        new_magic = character.get_magic()
        new_endurance = character.get_endurance()
        new_agility = character.get_agility()
        new_dexterity = character.get_dexterity()

        self.text = ''
        if health == new_health:
            self.text += f'{health}'
        else:
            self.text += f'{health} -> {new_health}'
        if mana == new_mana:
            self.text += f'\n{mana}'
        else:
            self.text += f'\n{mana} -> {new_mana}'
        if strength == new_strength:
            self.text += f'\n{strength}'
        else:
            self.text += f'\n{strength} -> {new_strength}'
        if magic == new_magic:
            self.text += f'\n{magic}'
        else:
            self.text += f'\n{magic} -> {new_magic}'
        if endurance == new_endurance:
            self.text += f'\n{endurance}'
        else:
            self.text += f'\n{endurance} -> {new_endurance}'
        if agility == new_agility:
            self.text += f'\n{agility}'
        else:
            self.text += f'\n{agility} -> {new_agility}'
        if dexterity == new_dexterity:
            self.text += f'\n{dexterity}'
        else:
            self.text += f'\n{dexterity} -> {new_dexterity}'

        print(fam_bonus_increases)
        if character.get_id() in fam_bonus_increases:
            char_fam_increases = fam_bonus_increases[character.get_id()]
            self.has_fam_increases = len(char_fam_increases) > 0
            for index, (partner_id, amount) in enumerate(char_fam_increases.items()):
                character.add_familiarity(partner_id, amount)
                if amount > 0.004:
                    partner = Refs.gc.get_char_by_id(partner_id)
                    self.add_widget(FamiliarityIncrease(character, partner, amount, size_hint=(1, 0.09), pos_hint={'top': 0.508 - 0.09 * index}))


class FamiliarityIncrease(RelativeLayout):
    image_source = StringProperty('')
    amount = NumericProperty(0)
    new_amount = NumericProperty(0)

    def __init__(self, character, partner, increase, **kwargs):
        super().__init__(**kwargs)
        self.image_source = partner.get_image('preview')
        self.amount = round(character.get_familiarity(partner.get_id()), 2)
        character.add_familiarity(partner.get_id(), increase)
        self.new_amount = round(self.amount + increase, 2)
