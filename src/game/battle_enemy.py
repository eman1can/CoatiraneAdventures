# Element Types
from random import choices

from game.battle_entity import BattleEntity
from game.entity import Entity


class BattleEnemy(BattleEntity, Entity):
    def __init__(self, identifier, name, skeleton_path, attack_type, health, mana, strength, magic, endurance, agility, dexterity, element, moves, move_chances):
        Entity.__init__(self, name, skeleton_path, health, mana, strength, magic, endurance, strength, magic, endurance, agility, dexterity, element, moves)
        BattleEntity.__init__(self)
        self._id = identifier
        self._move_chances = move_chances
        self._attack_type = attack_type
        self._bhealth = self.get_health()

    def get_id(self):
        return self._id

    def get_idle_animation(self):
        return 'idle'

    def get_selected_skill(self):
        return choices(self.get_skills(), self.get_skill_chances(), k=1)[0]

    def get_skills(self):
        return self._moves[0:1] + self._moves[3:]

    def get_skill_chances(self):
        return self._move_chances[0:1] + self._move_chances[3:]

    def is_character(self):
        return False

    def is_enemy(self):
        return True
