from game.hmpmd import HMPMD
from game.smead import SMEAD


class Outfit(HMPMD, SMEAD):
    def __init__(self, **kwargs):
        # Definitions
        self.weapon = None  # type: Equipment or None
        self.off_hand_weapon = None  # type: Equipment or None

        self.necklace = None  # type: Equipment or None
        self.ring = None  # type: Equipment or None

        self.helmet = None  # type: Equipment or None
        self.vambraces = None  # type: Equipment or None
        self.gloves = None  # type: Equipment or None
        self.chest = None  # type: Equipment or None
        self.grieves = None  # type: Equipment or None
        self.boots = None  # type: Equipment or None

        self.items = [self.weapon, self.off_hand_weapon, self.necklace, self.ring, self.helmet, self.vambraces, self.gloves, self.chest, self.grieves, self.boots]  # type: list[Equipment or None]
        self.types = ['weapon', 'off hand weapon', 'necklace', 'ring', 'helmet', 'vambraces', 'gloves', 'chest', 'grieves', 'boots']  # type: list[str]

        SMEAD.__init__(self, 0, 0, 0, 0, 0)
        HMPMD.__init__(self, 0, 0, 0, 0, 0)

    def get_type(self, equipment_type):
        return self.items[self.types.index(equipment_type)]

    def set_type(self, equipment_type, item):
        self.items[self.types.index(equipment_type)] = item

    def update_type(self, equipment_type, stat):
        item = self.items[self.types.index(equipment_type)]

    def update_health(self):
        health = 0
        for item in self.items:
            if item is not None:
                health += item.get_health()
        self.health = health

    def update_mana(self):
        mana = 0
        for item in self.items:
            if item is not None:
                mana += item.get_mana()
        self.mana = mana

    def update_physical_attack(self):
        physical_attack = 0
        for item in self.items:
            if item is not None:
                physical_attack += item.get_physical_attack()
        self.physical_attack = physical_attack

    def update_magical_attack(self):
        magical_attack = 0
        for item in self.items:
            if item is not None:
                magical_attack += item.get_magical_attack()
        self.magical_attack = magical_attack

    def update_defense(self):
        defense = 0
        for item in self.items:
            if item is not None:
                defense += item.get_defense()
        self.defense = defense

    def update_strength(self):
        strength = 0
        for item in self.items:
            if item is not None:
                strength += item.get_strength()
        self.strength = strength

    def update_magic(self):
        magic = 0
        for item in self.items:
            if item is not None:
                magic += item.get_magic()
        self.magic = magic

    def update_endurance(self):
        endurance = 0
        for item in self.items:
            if item is not None:
                endurance += item.get_endurance()
        self.endurance = endurance

    def update_agility(self):
        agility = 0
        for item in self.items:
            if item is not None:
                agility += item.get_agility()
        self.agility = agility

    def update_dexterity(self):
        dexterity = 0
        for item in self.items:
            if item is not None:
                dexterity += item.get_dexterity()
        self.dexterity = dexterity
