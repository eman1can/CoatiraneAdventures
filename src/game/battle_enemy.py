# Element Types
from random import choices

from game.battle_entity import BattleEntity
from game.skill import element_modifier
from refs import Refs


class BattleEnemy(BattleEntity):
    def __init__(self, entity, boost, move_chances, sub_element, hashed_id):  # identifier, name, skeleton_path, attack_type, health, mana, strength, magic, endurance, agility, dexterity, boost, element, sub_element, moves, move_chances):
        super().__init__(entity)

        self._move_chances = move_chances
        self._boost = boost
        self._sub_element = sub_element
        self._id = hashed_id

        self._battle_health = self.get_health()

    def get_id(self):
        return self._id

    def get_base_id(self):
        return self._base.get_id()

    def load_skeleton(self, skeleton_loader, scale=1):
        super().load_skeleton(skeleton_loader, Refs.gc.get_skeleton_scale() * scale * 2)

    def get_boost(self):
        return self._boost

    def get_idle_animation(self):
        return 'idle'

    def get_image(self, image_type):
        return f'icons/{self._name}.png'

    def select_skill(self):
        self._selected_skill = choices([x for x in range(len(self._move_chances))], self._move_chances, k=1)[0]

    def get_selected_skill(self):
        return self.get_skills()[self._selected_skill]

    def get_attack_animation(self, skill):
        if skill == 1:
           return 'skill1'
        elif skill == 2:
            return 'skill2'
        else:
            return 'attack'

    def get_skills(self):  # Exclude counter and block, which are last 2
        return self._moves[:-2]

    def get_counter_skill(self):
        return self._moves[-2]

    def get_block_skill(self):
        return self._moves[-1]

    def get_skill_chances(self):
        return self._move_chances

    def get_mana_cost(self, skill):
        return 0

    def is_character(self):
        return False

    def is_enemy(self):
        return True

    def get_sub_element(self):
        return self._sub_element

    def element_modifier(self, element):
        bonus = super().element_modifier(element)
        if bonus in (2.0, 0.5):
            return bonus
        return max(0.75, min(1.5, element_modifier(self._sub_element, element)))
