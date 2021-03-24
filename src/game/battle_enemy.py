# Element Types
from random import choices

from game.battle_entity import BattleEntity
from game.entity import Entity
from game.skill import DARK, EARTH, FIRE, LIGHT, THUNDER, WATER, WIND


class BattleEnemy(BattleEntity, Entity):
    def __init__(self, identifier, name, skeleton_path, attack_type, health, mana, strength, magic, endurance, agility, dexterity, boost, element, sub_element, moves, move_chances):
        Entity.__init__(self, name, skeleton_path, health, mana, strength, magic, endurance, strength, magic, endurance, agility, dexterity, element, moves)
        BattleEntity.__init__(self)
        self._id = identifier
        self._move_chances = move_chances
        self._attack_type = attack_type
        self._boost = boost

        self._element = element
        self._sub_element = sub_element

        self._bhealth = self.get_health()

    def get_id(self):
        return self._id

    def get_boost(self):
        return self._boost

    def get_idle_animation(self):
        return 'idle'

    def get_selected_skill(self):
        return choices(self.get_skills(), self.get_skill_chances(), k=1)[0]

    def get_skills(self):  # Exclude counter and block, which are last 2
        return self._moves[:-2]

    def get_counter_skill(self):
        return self._moves[-2]

    def get_block_skill(self):
        return self._moves[-1]

    def get_skill_chances(self):
        return self._move_chances

    def is_character(self):
        return False

    def is_enemy(self):
        return True

    def element_modifier(self, element):
        if element == WATER:
            if self._element == FIRE:
                return 2.0
            elif self._sub_element == FIRE:
                return 1.5
            elif self._element == THUNDER:
                return 0.5
            elif self._sub_element == THUNDER:
                return 0.75
        if element == FIRE:
            if self._element == WIND:
                return 2.0
            elif self._sub_element == WIND:
                return 1.5
            elif self._element == WATER:
                return 0.5
            elif self._sub_element == WATER:
                return 0.75
        if element == THUNDER:
            if self._element == WATER:
                return 2.0
            elif self._sub_element == WATER:
                return 1.5
            elif self._element == THUNDER:
                return 0.5
            elif self._sub_element == THUNDER:
                return 0.75
        if element == WIND:
            if self._element == EARTH:
                return 2.0
            elif self._sub_element == EARTH:
                return 1.5
            elif self._element == FIRE:
                return 0.5
            elif self._sub_element == FIRE:
                return 0.75
        if element == EARTH:
            if self._element == THUNDER:
                return 2.0
            elif self._sub_element == THUNDER:
                return 1.5
            elif self._element == WIND:
                return 0.5
            elif self._sub_element == WIND:
                return 0.75
        if element == LIGHT:
            if self._element == DARK:
                return 2.0
            elif self._sub_element == DARK:
                return 1.5
        if element == DARK:
            if self._element == LIGHT:
                return 2.0
            elif self._sub_element == LIGHT:
                return 1.5
