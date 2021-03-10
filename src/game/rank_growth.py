from game.hmpmd import HMPMD
from game.smead import SMEAD

SMEAD_RANK_MAX = 99
HEALTH_RANK_MAX = 300
MANA_RANK_MAX = 150


class RankGrowth(SMEAD, HMPMD):
    def __init__(self, hp=0, mp=0, s=0, m=0, e=0, a=0, d=0):
        self._initialized = False
        SMEAD.__init__(self, s, m, e, a, d)
        HMPMD.__init__(self, hp, mp, 0, 0, 0)
        self._initialized = True
        self.refresh_stats()

    def refresh_stats(self):
        if not self._initialized:
            return
        SMEAD.refresh_stats(self)
        HMPMD.refresh_stats(self)

    def increase_health(self, delta):
        if self._health + delta < HEALTH_RANK_MAX:
            self._health += delta
        else:
            self._health = HEALTH_RANK_MAX
        self.update_health()

    def increase_mana(self, delta):
        if self._mana + delta < MANA_RANK_MAX:
            self._mana += delta
        else:
            self._mana = MANA_RANK_MAX
        self.update_mana()

    def increase_strength(self, delta):
        if self._strength + delta < SMEAD_RANK_MAX:
            self._strength += delta
        else:
            self._strength = SMEAD_RANK_MAX
        self.update_strength()

    def increase_magic(self, delta):
        if self._magic + delta < SMEAD_RANK_MAX:
            self._magic += delta
        else:
            self._magic = SMEAD_RANK_MAX
        self.update_magic()

    def increase_endurance(self, delta):
        if self._endurance + delta < SMEAD_RANK_MAX:
            self._endurance += delta
        else:
            self._endurance = SMEAD_RANK_MAX
        self.update_endurance()

    def increase_agility(self, delta):
        if self._agility + delta < SMEAD_RANK_MAX:
            self._agility += delta
        else:
            self._agility = SMEAD_RANK_MAX
        self.update_agility()

    def increase_dexterity(self, delta):
        if self._dexterity + delta < SMEAD_RANK_MAX:
            self._dexterity += delta
        else:
            self._dexterity = SMEAD_RANK_MAX
        self.update_dexterity()
