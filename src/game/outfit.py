from game.equipment import WEAPON
from game.hmpmd import HMPMD


class Outfit(HMPMD):
    def __init__(self, **kwargs):
        # Definitions

        self.items = [None for _ in range(10)]

        HMPMD.__init__(self, 0, 0, 0, 0, 0)

    def get_equipment(self, equipment_type):
        return self.items[equipment_type - WEAPON]

    def set_equipment(self, equipment_type, item):
        self.items[equipment_type - WEAPON] = item

    def refresh_stats(self, favorite_weapon=None, favorite_sub_weapon=None):
        self.update_health(favorite_weapon, favorite_sub_weapon)
        self.update_mana(favorite_weapon, favorite_sub_weapon)
        self.update_physical_attack(favorite_weapon, favorite_sub_weapon)
        self.update_magical_attack(favorite_weapon, favorite_sub_weapon)
        self.update_defense(favorite_weapon, favorite_sub_weapon)
        self.update_score(favorite_weapon, favorite_sub_weapon)
        self.update_value(favorite_weapon, favorite_sub_weapon)
        self.update_weight(favorite_weapon, favorite_sub_weapon)

    def update_health(self, favorite_weapon=None, favorite_sub_weapon=None):
        health = 0
        for item in self.items:
            if item is not None:
                if item.get_type() == WEAPON and item.get_sub_type() in [favorite_weapon, favorite_sub_weapon]:
                    health += item.get_health() * 1.25
                else:
                    health += item.get_health()
        self.health = health

    def update_mana(self, favorite_weapon=None, favorite_sub_weapon=None):
        mana = 0
        for item in self.items:
            if item is not None:
                if item.get_type() == WEAPON and item.get_sub_type() in [favorite_weapon, favorite_sub_weapon]:
                    mana += item.get_mana() * 1.25
                else:
                    mana += item.get_mana()
        self.mana = mana

    def update_physical_attack(self, favorite_weapon=None, favorite_sub_weapon=None):
        physical_attack = 0
        for item in self.items:
            if item is not None:
                if item.get_type() == WEAPON and item.get_sub_type() in [favorite_weapon, favorite_sub_weapon]:
                    physical_attack += item.get_physical_attack() * 1.25
                else:
                    physical_attack += item.get_physical_attack()
        self.physical_attack = physical_attack

    def update_magical_attack(self, favorite_weapon=None, favorite_sub_weapon=None):
        magical_attack = 0
        for item in self.items:
            if item is not None:
                if item.get_type() == WEAPON and item.get_sub_type() in [favorite_weapon, favorite_sub_weapon]:
                    magical_attack += item.get_magical_attack() * 1.25
                else:
                    magical_attack += item.get_magical_attack()
        self.magical_attack = magical_attack

    def update_defense(self, favorite_weapon=None, favorite_sub_weapon=None):
        defense = 0
        for item in self.items:
            if item is not None:
                if item.get_type() == WEAPON and item.get_sub_type() in [favorite_weapon, favorite_sub_weapon]:
                    defense += item.get_defense() * 1.25
                else:
                    defense += item.get_defense()
        self.defense = defense

    def get_score(self):
        return self.score

    def update_score(self, favorite_weapon=None, favorite_sub_weapon=None):
        score = 0
        for item in self.items:
            if item is not None:
                score += item.get_score()
        self.score = score

    def get_value(self):
        return self.value

    def update_value(self, favorite_weapon=None, favorite_sub_weapon=None):
        value = 0
        for item in self.items:
            if item is not None:
                value += item.get_value()
        self.value = value

    def get_weight(self):
        return self.weight

    def update_weight(self, favorite_weapon=None, favorite_sub_weapon=None):
        weight = 0
        for item in self.items:
            if item is not None:
                if item.get_type() == WEAPON and item.get_sub_type() in [favorite_weapon, favorite_sub_weapon]:
                    weight += item.get_weight() * 0.75
                else:
                    weight += item.get_weight()
        self.weight = weight
