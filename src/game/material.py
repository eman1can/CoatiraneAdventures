NATURAL_HARD = 0
NATURAL_SOFT = 1
ALLOY_HARD   = 2
MONSTER_HARD = 3
MONSTER_SOFT = 4
GEM          = 5
WOOD         = 6

# Material values
DURABILITY = 0
HEALTH     = 1
MANA       = 2
PHY_ATK    = 3
MAG_ATK    = 4
DEF        = 5
WEIGHT     = 6


class Material:
    def __init__(self, material_type, identifier, name, min_hardness, max_hardness, raw_form, processed_form, effect, sub_effect, material_values):
        self._id = identifier
        self._name = name
        self._type = material_type

        self._min_hardness = float(min_hardness)
        self._max_hardness = float(max_hardness)

        self._effect = effect
        self._sub_effect = sub_effect

        self._raw_id = raw_form
        self._processed_id = processed_form

        self._weights = material_values

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_hardness(self):
        return self._min_hardness

    def get_max_hardness(self):
        return self._max_hardness

    def get_raw_id(self):
        return self._raw_id

    def get_processed_id(self):
        return self._processed_id

    def get_defining_effect(self, is_weapon):
        if is_weapon:
            return self._effect[0]
        else:
            return self._effect[1]

    def get_sub_effect(self, is_weapon):
        if is_weapon:
            return self._sub_effect[0]
        else:
            return self._effect[1]

    def is_hard(self):
        return self._type in [NATURAL_HARD, ALLOY_HARD, MONSTER_HARD]

    def is_soft(self):
        return self._type in [NATURAL_SOFT, MONSTER_SOFT]

    def is_natural(self):
        return self._type in [NATURAL_HARD, NATURAL_SOFT, GEM, WOOD]

    def is_non_natural(self):
        return self._type in [MONSTER_SOFT, MONSTER_HARD, ALLOY_HARD]

    def is_wood(self):
        return self._type == WOOD

    def is_alloy(self):
        return self._type == ALLOY_HARD

    def is_gem(self):
        return self._type == GEM

    def get_durability(self):
        return self._weights[DURABILITY]

    def get_weight(self):
        return self._weights[WEIGHT]

    def get_health(self):
        return self._weights[HEALTH]

    def get_mana(self):
        return self._weights[MANA]

    def get_physical_attack(self):
        return self._weights[PHY_ATK]

    def get_magical_attack(self):
        return self._weights[MAG_ATK]

    def get_defense(self):
        return self._weights[DEF]

    def get_all_weights(self):
        return self._weights
