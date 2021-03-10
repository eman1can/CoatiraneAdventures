# Project Imports
from refs import Refs

# UIX Imports
from uix.screens.character_display.attributes.status_board.slot import CustomSlot
from uix.popups.status_board import SBAbilityUnlock, SBSkillUnlock

# Kivy Imports
from kivy.properties import ObjectProperty, BooleanProperty, NumericProperty, ListProperty, StringProperty
from kivy.uix.relativelayout import RelativeLayout

# KV Import
from loading.kv_loader import load_kv
load_kv(__name__)


class GridWidget(RelativeLayout):
    grid = ObjectProperty(None)
    manager = ObjectProperty(None)

    ability_slot = BooleanProperty(False)
    ability_slot_unlocked = BooleanProperty(False)
    ability = ObjectProperty(None, allownone=True)

    skill_slot = BooleanProperty(False)
    skill_slot_unlocked = BooleanProperty(False)
    skill = ObjectProperty(None, allownone=True)

    grid_locked = BooleanProperty(False)

    modal_open = BooleanProperty(False)

    rank = NumericProperty(0)
    slots = ListProperty([])

    overlay_background_source = StringProperty('screens/attributes/stat_background.png')
    overlay_source = StringProperty('screens/attributes/stat_background_overlay.png')

    def __init__(self, rank, index, grid, **kwargs):
        self.grid = grid
        self.rank = rank
        self.ability_modal = SBAbilityUnlock()
        self.skill_modal = SBSkillUnlock()
        super().__init__(**kwargs)
        self.ability_modal.bind(on_confirm=self.do_ability)
        self.ability_modal.bind(on_dismiss=self.dismiss_modal)
        self.skill_modal.bind(on_confirm=self.do_skill)
        self.skill_modal.bind(on_dismiss=self.dismiss_modal)

        # Adventurer Abilities
        if index > 0 and not self.manager.char.is_support():
            self.ability_slot = True
            self.ability = self.manager.char.get_ability(index - 1)
            if self.ability is not None:
                self.ability_slot_unlocked = True
            else:
                self.ability_modal.choices = self.manager.char.get_ability_options(Refs.gc.get_abilities())

        # Support Abilities
        if (index + 1) % 2 == 0 and self.manager.char.is_support():
            self.ability_slot = True
            self.ability = self.manager.char.get_ability(index / 2)
            if self.ability is not None:
                self.ability_slot_unlocked = True
            else:
                self.ability_modal.choices = self.manager.char.get_ability_options(Refs.gc.get_abilities())

        # First 3 skills
        if index in [1, 2, 3]:
            self.skill = self.manager.char.get_skill(index - 1)
            if self.skill is not None:
                self.skill_slot = True

        # Special and combos
        if not self.manager.char.is_support() and index in [5, 7, 8, 9]:
            self.skill = self.manager.char.get_skill(index - 5 if index == 5 else index - 6)
            if self.skill is not None:
                self.skill_slot = True

        index = 0
        y_i = len(self.grid.grid) - 1
        pos_hint_x, pos_hint_y = 0.5, 0.5 + y_i * 0.03125 + y_i * 0.00625
        for r, row in enumerate(self.grid.grid):
            list = []
            for c, column in enumerate(row):
                slot_unlocked = self.grid.unlocked[r][c]
                self.grid_locked = self.grid.index > rank
                if column == 'S':
                    slot = CustomSlot(pos_hint={'center_x': pos_hint_x, 'center_y': pos_hint_y}, size_hint=(0.07076, 0.0625), type='strength', locked=(not slot_unlocked), disabled=self.grid_locked, value=self.grid.amounts[0])
                    slot.bind(on_unlock=lambda instance: self.manager.on_release(instance, 'strength', self.grid.index))
                elif column == 'M':
                    slot = CustomSlot(pos_hint={'center_x': pos_hint_x, 'center_y': pos_hint_y}, size_hint=(0.07076, 0.0625),type='magic', locked=(not slot_unlocked), disabled=self.grid_locked, value=self.grid.amounts[1])
                    slot.bind(on_unlock=lambda instance: self.manager.on_release(instance, 'magic', self.grid.index))
                elif column == 'E':
                    slot = CustomSlot(pos_hint={'center_x': pos_hint_x, 'center_y': pos_hint_y}, size_hint=(0.07076, 0.0625), type='endurance', locked=(not slot_unlocked), disabled=self.grid_locked, value=self.grid.amounts[2])
                    slot.bind(on_unlock=lambda instance: self.manager.on_release(instance, 'endurance', self.grid.index))
                elif column == 'D':
                    slot = CustomSlot(pos_hint={'center_x': pos_hint_x, 'center_y': pos_hint_y}, size_hint=(0.07076, 0.0625),  type='dexterity', locked=(not slot_unlocked), disabled=self.grid_locked, value=self.grid.amounts[3])
                    slot.bind(on_unlock=lambda instance: self.manager.on_release(instance, 'dexterity', self.grid.index))
                else:
                    slot = CustomSlot(pos_hint={'center_x': pos_hint_x, 'center_y': pos_hint_y}, size_hint=(0.07076, 0.0625),  type='agility', locked=(not slot_unlocked), disabled=self.grid_locked, value=self.grid.amounts[4])
                    slot.bind(on_unlock=lambda instance: self.manager.on_release(instance, 'agility', self.grid.index))
                pos_hint_x += 0.007076 + 0.03538
                pos_hint_y -= 0.00625 + 0.03125
                list.append(slot)
                index += 1
                self.add_widget(slot)
            pos_hint_x -= (0.007076 + 0.03538) * (len(row) + 1)
            pos_hint_y += (0.00625 + 0.03125) * (len(row) - 1)
            self.slots.append(list)

    def on_touch_hover(self, touch):
        if self.modal_open:
            return False
        return self.dispatch_to_relative_children(touch)

    def dismiss_modal(self, *args):
        self.modal_open = False

    def on_ability_open(self, *args):
        self.modal_open = True
        self.ability_modal.open()

    def on_skill_open(self, *args):
        self.modal_open = True
        self.skill_modal.open()

    def do_ability(self, instance, choice):
        choice = self.ability_modal.choices[int(choice)]
        self.ability_slot_unlocked = True
        self.manager.char.add_ability(choice)
        self.ability_slot_unlocked = True
        self.ability = choice

    def do_skill(self, *args):
        self.skill_slot_unlocked = True