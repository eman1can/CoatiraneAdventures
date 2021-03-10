from game.hmpmd import HMPMD
from game.smead import SMEAD


class Equipment(SMEAD, HMPMD):
    def __init__(self, name, equipment_id, equipment_type, element, rank, values):
        HMPMD.__init__(self, values[0], values[1], values[2], values[3], values[4])
        SMEAD.__init__(self, values[5], values[6], values[7], values[8], values[9])
        self.name = name
        self.equipment_id = equipment_id
        self.equipment_type = equipment_type
        self.element = element
        self.rank = rank

        self._durability = values[10]
        self.durability = 0
        self._durability_current = values[11]
        self.durability_current = 0
        self._score = values[12]
        self.score = 0
        self._value = values[13]
        self.value = 0
        self.refresh_stats()

    def refresh_stats(self):
        SMEAD.refresh_stats(self)
        HMPMD.refresh_stats(self)
        self.update_durability()
        self.update_durability_current()
        self.update_score()
        self.update_value()

    def get_name(self):
        return self.name

    def get_id(self):
        return self.equipment_id

    def get_type(self):
        return self.equipment_type

    def get_element(self):
        return self.element

    def get_durability(self):
        return self.durability

    def get_durability_current(self):
        return self.durability_current

    def get_score(self):
        return self.score

    def get_value(self):
        return self.value

    def update_durability(self):
        self.durability = self._durability

    def remove_durability(self, wear_value):
        self._durability_current -= wear_value

    def update_durability_current(self):
        self.durability_current = self._durability_current

    def update_score(self):
        self.score = self._score

    def update_value(self):
        self.value = self._value

    def get_rank(self):
        return self.rank
