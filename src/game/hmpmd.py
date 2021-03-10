class HMPMD:
    def __init__(self, h, m, pa, ma, d):
        self._health = h
        self.health = 0
        self._mana = m
        self.mana = 0

        self._physical_attack = pa
        self.physical_attack = 0
        self._magical_attack = ma
        self.magical_attack = 0
        self._defense = d
        self.defense = 0
        self.refresh_stats()

    def refresh_stats(self):
        self.update_health()
        self.update_mana()
        self.update_physical_attack()
        self.update_magical_attack()
        self.update_defense()

    def update_health(self):
        self.health = self._health

    def update_mana(self):
        self.mana = self._mana

    def update_physical_attack(self):
        self.physical_attack = self._physical_attack

    def update_magical_attack(self):
        self.magical_attack = self._magical_attack

    def update_defense(self):
        self.defense = self._defense

    def get_health(self):
        return self.health

    def get_mana(self):
        return self.mana

    def get_physical_attack(self):
        return self.physical_attack

    def get_magical_attack(self):
        return self.magical_attack

    def get_defense(self):
        return self.defense
