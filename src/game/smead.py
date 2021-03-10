class SMEAD:
    def __init__(self, s, m, e, a, d):
        self._strength = s
        self.strength = 0
        self._magic = m
        self.magic = 0
        self._endurance = e
        self.endurance = 0
        self._agility = a
        self.agility = 0
        self._dexterity = d
        self.dexterity = 0
        self.refresh_stats()

    def refresh_stats(self):
        self.update_strength()
        self.update_magic()
        self.update_endurance()
        self.update_agility()
        self.update_dexterity()

    def update_strength(self):
        self.strength = self._strength

    def update_magic(self):
        self.magic = self._magic

    def update_endurance(self):
        self.endurance = self._endurance

    def update_agility(self):
        self.agility = self._agility

    def update_dexterity(self):
        self.dexterity = self._dexterity

    def get_strength(self):
        return self.strength

    def get_magic(self):
        return self.magic

    def get_endurance(self):
        return self.endurance

    def get_agility(self):
        return self.agility

    def get_dexterity(self):
        return self.dexterity
