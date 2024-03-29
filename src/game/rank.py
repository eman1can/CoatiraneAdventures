from math import floor

from game.board import Board
from game.hmpmd import HMPMD
from game.rank_growth import HEALTH_RANK_MAX, MANA_RANK_MAX, RankGrowth, SMEAD_RANK_MAX
from game.smead import SMEAD

RANK_BREAK_INCREASE = 0.25
MAX_RANK = 10


class Rank(SMEAD, HMPMD):
    def __init__(self, index, rank_growth, board, unlocked, broken, hp=1, mp=1, s=1, m=1, e=1, a=1, d=1):
        self._initialized = False
        SMEAD.__init__(self, s, m, e, a, d)
        HMPMD.__init__(self, hp, mp, 0, 0, 0)
        self._rank_growth = rank_growth
        self._board = board
        self._unlocked = unlocked
        self._broken = broken
        self._index = index
        self._initialized = True

    def __str__(self):
        return f"<Rank - {self._index} - {'Unlocked' if self._unlocked else 'Locked'} - {'Broken' if self._broken else 'Un-Broken'}>"

    def refresh_stats(self):
        if not self._initialized:
            return
        self._rank_growth.refresh_stats()
        self._board.refresh_stats()
        SMEAD.refresh_stats(self)
        HMPMD.refresh_stats(self)

    def get_board(self):
        return self._board

    def get_growth(self):
        return self._rank_growth

    def get_index(self):
        return self._index

    def max_stats(self):
        self.increase_health(HEALTH_RANK_MAX)
        self.increase_mana(MANA_RANK_MAX)
        self.increase_strength(SMEAD_RANK_MAX)
        self.increase_magic(SMEAD_RANK_MAX)
        self.increase_endurance(SMEAD_RANK_MAX)
        self.increase_agility(SMEAD_RANK_MAX)
        self.increase_dexterity(SMEAD_RANK_MAX)
        self._board.unlock_all()

    def break_rank(self, attack_type):
        self._health = 1 + RANK_BREAK_INCREASE
        self._agility = 1 + RANK_BREAK_INCREASE * 0.9
        self._dexterity = 1 + RANK_BREAK_INCREASE * 0.9
        weights = [[0.75, 1, 0.75, 0.75], [1, 0.75, 1, 0.75], [0.75, 0.9, 0.9, 0.75], [0.75, 0.9, 0.75, 1], [0.9, 0.75, 0.9, 0.75]]
        weight_set = weights[attack_type]
        self._mana = 1 + RANK_BREAK_INCREASE * weight_set[0]
        self._strength = 1 + RANK_BREAK_INCREASE * weight_set[1]
        self._magic = 1 + RANK_BREAK_INCREASE * weight_set[2]
        self._endurance = 1 + RANK_BREAK_INCREASE * weight_set[3]

    def unlock(self):
        self._unlocked = True

    def is_unlocked(self):
        return self._unlocked

    def is_broken(self):
        return self._broken

    def increase_health(self, delta):
        self._rank_growth.increase_health(delta)
        self.update_health()

    def increase_mana(self, delta):
        self._rank_growth.increase_mana(delta)
        self.update_mana()

    def increase_strength(self, delta):
        self._rank_growth.increase_strength(delta)
        self.update_strength()

    def increase_magic(self, delta):
        self._rank_growth.increase_magic(delta)
        self.update_magic()

    def increase_endurance(self, delta):
        self._rank_growth.increase_endurance(delta)
        self.update_endurance()

    def increase_agility(self, delta):
        self._rank_growth.increase_agility(delta)
        self.update_agility()

    def increase_dexterity(self, delta):
        self._rank_growth.increase_dexterity(delta)
        self.update_dexterity()

    def update_health(self):
        self.health = floor(self._rank_growth.get_health() * self._health)

    def update_mana(self):
        self.mana = floor(self._rank_growth.get_mana() * self._mana)

    def update_strength(self):
        self.strength = floor((self._rank_growth.get_strength() + self._board.get_strength()) * self._strength)

    def update_magic(self):
        self.magic = floor((self._rank_growth.get_magic() + self._board.get_magic()) * self._magic)

    def update_endurance(self):
        self.endurance = floor((self._rank_growth.get_endurance() + self._board.get_endurance()) * self._endurance)

    def update_agility(self):
        self.agility = floor((self._rank_growth.get_agility() + self._board.get_agility()) * self._agility)

    def update_dexterity(self):
        self.dexterity = floor((self._rank_growth.get_dexterity() + self._board.get_dexterity()) * self._dexterity)

    @staticmethod
    def load_ranks(rank_path, character_development):
        file = open(rank_path, 'r')
        ranks = []
        level = 0
        while level != MAX_RANK:
            line = file.readline()
            if line[0] == "#":
                continue
            values = list(line.split(' '))
            for index in range(len(values)):
                values[index] = int(values[index].strip())

            if character_development is None:
                growth = RankGrowth()
                board = Board(values[9], values[8], values[7], values[6], values[5], values[4], values[3], values[2], values[1], values[0])
                unlocked = level == 0
                broken = False
            else:
                growth = RankGrowth(*character_development['growth'][level])
                board = Board(values[9], values[8], values[7], values[6], values[5], values[4], values[3], values[2], values[1], values[0], character_development['boards'][level])
                unlocked = character_development['unlocked'][level]
                broken = character_development['broken'][level]
            ranks.append(Rank(level, growth, board, unlocked, broken))
            level += 1
        return ranks
