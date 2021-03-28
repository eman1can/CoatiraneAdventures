from game.hmpmd import HMPMD
from game.smead import SMEAD


class Entity(SMEAD, HMPMD):
    def __init__(self, name, skeleton_path, health, mana, physical_attack, magical_attack, defense, strength, magic, endurance, agility, dexterity, element, moves):
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

    def get_skill(self, skill_index):
        # Characters:
        #    Adventurers:
        #       Basic Move, Skill 1, Skill 1 Mana Cost, Skill 2, Skill 2 Mana Cost, Skill 3, Skill 3 Mana Cost, Special Move, Counter Move, Block Move
        #    Supporters:
        #       Effect Level 1, Effect Level 2, Effect Level 3, Effect Level 4, Effect Level 5  #  2 4 6 8 10
        # Enemies:
        #    Basic Move, Skill 1, Skill x - 1, Skill x, Counter Move, Block Move
        return self._moves[skill_index]

    def get_counter_skill(self):
        return self._moves[-2]

    def get_block_skill(self):
        return self._moves[-1]

    def get_skills(self):
        return self._moves
