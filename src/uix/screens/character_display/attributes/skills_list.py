# Kivy Imports
from kivy.properties import NumericProperty

from kivy.uix.scrollview import ScrollView
# KV Import
from game.skill import ELEMENTS
from loading.kv_loader import load_kv
from uix.screens.character_display.attributes.status_label import AttackLabel

load_kv(__name__)


class SkillsList(ScrollView):
    height_unit = NumericProperty(0)

    def __init__(self, **kwargs):
        self._skills = None
        self._abilites = None
        super().__init__(**kwargs)

    def on_height_unit(self, *args):
        if self._skills is not None:
            for skill in self._skills:
                skill.height = 0.15 * self.height_unit

    def set_combat_skills(self, support, skills):
        if self._skills is not None:
            for skill in self._skills:
                self.ids.combat_skills.remove_widget(skill)

        self._skills = []
        if not support:
            # Add Basic Attack
            basic_attack = skills[0]
            label = AttackLabel(
                size_hint=(1, None),
                type_source=f'icons/{ELEMENTS[basic_attack.get_element()]}.png',
                title=basic_attack.get_name(),
                body=basic_attack.get_description()
            )
            self._skills.append(label)

            # Move 1 - 3
            for index in [1, 3, 5]:
                skill = skills[index]
                mana_cost = skills[index + 1]
                description = skill.get_description()
                if '-' in description:
                    description = description.split('-')[0]
                label = AttackLabel(
                    size_hint=(1, None),
                    type_source=f'icons/{ELEMENTS[skill.get_element()]}.png',
                    title=skill.get_name(),
                    cost=f'MP {mana_cost}',
                    body=description
                )
                self._skills.append(label)

            # Special Move, Counter, Block
            special = skills[7]
            counter = skills[-2]
            block = skills[-1]

            special_label = AttackLabel(
                size_hint=(1, None),
                type_source=f'icons/{ELEMENTS[special.get_element()]}.png',
                title=special.get_name(),
                body=special.get_description()
            )
            self._skills.append(special_label)

            if counter is not None:
                counter_label = AttackLabel(
                    size_hint=(1, None),
                    type_source=f'icons/{ELEMENTS[counter.get_element()]}.png',
                    title=f'Counter: {counter.get_name()}',
                    body=counter.get_description()
                )
                self._skills.append(counter_label)

            if block is not None:
                block_label = AttackLabel(
                    size_hint=(1, None),
                    type_source=f'icons/{ELEMENTS[block.get_element()]}.png',
                    title=f'Block: {block.get_name()}',
                    body=block.get_description()
                )
                self._skills.append(block_label)
        else:
            for skill in skills:
                label = AttackLabel(
                    size_hint=(1, None),
                    type_source=f'icons/{ELEMENTS[skill.get_element()]}.png',
                    title=skill.get_name(),
                    body=skill.get_description()
                )
                self._skills.append(label)
        for skill in self._skills:
            skill.height = 0.15 * self.height_unit
            self.ids.combat_skills.add_widget(skill)

    def set_abilities(self, abilities):
        pass
