from game.smead import SMEAD


class Board(SMEAD):
    def __init__(self, s, m, e, a, d, sc, mc, ec, ac, dc, unlocked=None):
        self._initialized = False
        super().__init__(s, m, e, a, d)
        self._strength_count = sc
        self._magic_count = mc
        self._endurance_count = ec
        self._agility_count = ac
        self._dexterity_count = dc
        if unlocked is None:
            unlocked = [False for _ in range(sc + mc + ec + ac + dc)]
        self._unlocked = unlocked
        self._all_unlocked = False
        self._initialized = True
        self.refresh_stats()

    def refresh_stats(self):
        if not self._initialized:
            return
        super().refresh_stats()
        self.update_unlocked()

    def update_unlocked(self):
        self._all_unlocked = True
        for unlocked in self._unlocked:
            self._all_unlocked &= unlocked

    def get_unlocked(self, index=-1):
        if index == -1:
            return self._all_unlocked
        else:
            return self._unlocked[index]

    def unlock_all(self):
        for index in range(len(self._unlocked)):
            if not self._unlocked[index]:
                self._unlocked[index] = True

    def unlock_index(self, index):
        self._unlocked[index] = True

    def update_strength(self):
        sc = len([x for x in self._unlocked[:self._strength_count] if x])
        self.strength = self._strength * sc

    def update_magic(self):
        mc = len([x for x in self._unlocked[self._strength_count:self._magic_count] if x])
        self.magic = self._magic * mc

    def update_endurance(self):
        ec = len([x for x in self._unlocked[self._strength_count+self._magic_count:self._endurance_count] if x])
        self.endurance = self._endurance * ec

    def update_agility(self):
        ac = len([x for x in self._unlocked[self._strength_count + self._magic_count+self._endurance_count:self._agility_count] if x])
        self.agility = self._agility * ac

    def update_dexterity(self):
        dc = len([x for x in self._unlocked[self._strength_count + self._magic_count + self._endurance_count+self._agility_count:] if x])
        self.dexterity = self._dexterity * dc
