from game.hmpmd import HMPMD
from game.smead import SMEAD


class Entity(SMEAD, HMPMD):
    def __init__(self, name, skeleton_path, health, mana, physical_attack, magical_attack, defense, strength, magic, endurance, dexterity, agility, element, moves):
        self._initialized = False
        SMEAD.__init__(self, strength, magic, endurance, agility, dexterity)
        HMPMD.__init__(self, health, mana, physical_attack, magical_attack, defense)
        self._name = name
        self._skeleton_path = skeleton_path

        self._element = element
        self._moves = moves
        self._initialized = True
        self.refresh_stats()

    def get_skeleton_path(self):
        return self._skeleton_path

    def get_name(self):
        return self._name

    def get_element(self):
        return self._element

    def refresh_stats(self):
        if not self._initialized:
            return
        SMEAD.refresh_stats(self)
        HMPMD.refresh_stats(self)
        # self.update_health()
        # self.update_mana()
        # self.update_physical_attack()
        # self.update_magical_attack()
        # self.update_defense()

    def get_skill(self, skill_index):
        # Characters: Basic Move, Counter Move, Block Move
        #             Skill 1 Move 1, Skill 2 Move 2, Skill 3 Move 3
        #             Special Move 5, Combo Move 1 7, Combo Move 2 8, Combo Move 3 9
        # Enemies: Basic Attack, Counter Move, Block Move, Skill 1 Move, Skill 2 Move
        return self._moves[skill_index]

    def get_counter_skill(self):
        return self._moves[1]

    def get_block_skill(self):
        return self._moves[2]

    def get_skills(self):
        return self._moves
