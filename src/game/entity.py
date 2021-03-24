from game.hmpmd import HMPMD
from game.skill import DARK, EARTH, FIRE, LIGHT, THUNDER, WATER, WIND
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
        #       Effect Level 1, Effect Level 2, Effect Level 3, Effect Level 4, Effect Level 5
        # Enemies:
        #    Basic Move, Skill 1, Skill x - 1, Skill x, Counter Move, Block Move
        return self._moves[skill_index]

    def get_counter_skill(self):
        return self._moves[1]

    def get_block_skill(self):
        return self._moves[2]

    def get_skills(self):
        return self._moves

    def element_modifier(self, element):
        if element == WATER:
            if self._element == FIRE:
                return 2.0
            elif self._element == THUNDER:
                return 0.5
        if element == FIRE:
            if self._element == WIND:
                return 2.0
            elif self._element == WATER:
                return 0.5
        if element == THUNDER:
            if self._element == WATER:
                return 2.0
            elif self._element == THUNDER:
                return 0.5
        if element == WIND:
            if self._element == EARTH:
                return 2.0
            elif self._element == FIRE:
                return 0.5
        if element == EARTH:
            if self._element == THUNDER:
                return 2.0
            elif self._element == WIND:
                return 0.5
        if element == LIGHT:
            if self._element == DARK:
                return 2.0
        if element == DARK:
            if self._element == LIGHT:
                return 2.0