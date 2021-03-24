from game.hmpmd import HMPMD
from game.smead import SMEAD

DAGGER                    = 0
CURVED_DAGGER             = 1
KUKRI                     = 2
CUTLASS                   = 3
SHORT_SWORD               = 4
KATANA                    = 5
LONGSWORD                 = 6
BROADSWORD                = 7
DOUBLE_ENDED_BROADSWORD   = 8
RAPIER                    = 9
KNUCKLEDUSTER             = 10
CLAWS                     = 11
GAUNTLETS                 = 12
AXE                       = 13
DOUBLE_HEADED_AXE         = 14
GIANT_AXE                 = 15
DOUBLE_HEADED_GIANT_AXE   = 16
MACE                      = 17
HAMMER                    = 18
DOUBLE_HEADED_HAMMER      = 19
GIANT_HAMMER              = 20
DOUBLE_ENDED_GIANT_HAMMER = 21
SPEAR                     = 22
PIKE                      = 23
HALBERD                   = 24
SHORT_STAFF               = 25
STAFF                     = 26

WEAPON_TYPES = {
    DAGGER: 'Dagger',
    CURVED_DAGGER: 'Curved Dagger',
    KUKRI: 'Kukri',
    CUTLASS: 'Cutlass',
    SHORT_SWORD: 'Short Sword',
    KATANA: 'Katana',
    LONGSWORD: 'Longsword',
    BROADSWORD: 'Broadsword',
    DOUBLE_ENDED_BROADSWORD: 'Double-Ended Broadsword',
    RAPIER: 'Rapier',
    KNUCKLEDUSTER: 'Knuckleduster',
    CLAWS: 'Claws',
    GAUNTLETS: 'Fists',
    AXE: 'Axe',
    DOUBLE_HEADED_AXE: 'Double-Headed Axe',
    GIANT_AXE: 'Giant Axe',
    DOUBLE_HEADED_GIANT_AXE: 'Double-Headed Giant Axe',
    MACE: 'Maxe',
    HAMMER: 'Hammer',
    DOUBLE_HEADED_HAMMER: 'Double-Headed Hammer',
    GIANT_HAMMER: 'Giant-Hammer',
    DOUBLE_ENDED_GIANT_HAMMER: 'Double-Ended Giant Hammer',
    SPEAR: 'Spear',
    PIKE: 'Pike',
    HALBERD: 'Halberd',
    SHORT_STAFF: 'Short Staff',
    STAFF: 'Staff'
}

CAN_DUAL_WIELD: {
    DAGGER: True,
    CURVED_DAGGER: True,
    KUKRI: True,
    CUTLASS: True,
    SHORT_SWORD: True,
    KATANA: False,
    LONGSWORD: False,
    BROADSWORD: False,
    DOUBLE_ENDED_BROADSWORD: False,
    RAPIER: False,
    KNUCKLEDUSTER: True,
    CLAWS: True,
    GAUNTLETS: True,
    AXE: True,
    DOUBLE_HEADED_AXE: False,
    GIANT_AXE: False,
    DOUBLE_HEADED_GIANT_AXE: False,
    MACE: True,
    HAMMER: True,
    DOUBLE_HEADED_HAMMER: False,
    GIANT_HAMMER: False,
    DOUBLE_ENDED_GIANT_HAMMER: False,
    SPEAR: False,
    PIKE: False,
    HALBERD: False,
    SHORT_STAFF: True,
    STAFF: False
}


class EquipmentPattern:
    def __init__(self, name, description, one_handed, material_list):
        self._name = name
        self._description = description
        self._one_handed = one_handed
        self._material_list = material_list

    def get_name(self):
        return self._name

    def get_description(self):
        return self._description

    def is_one_handed(self):
        return self._one_handed


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
