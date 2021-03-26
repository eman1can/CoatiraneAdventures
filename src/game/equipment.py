from random import uniform
from time import time_ns

from game.hmpmd import HMPMD
from game.skill import NONE
from game.smead import SMEAD
from refs import Refs

EQUIPMENT_TOOL   = 0
EQUIPMENT_WEAPON = 1
EQUIPMENT_ARMOR  = 2
EQUIPMENT_TYPES = {EQUIPMENT_TOOL: 'Tool', EQUIPMENT_WEAPON: 'Weapon', EQUIPMENT_ARMOR: 'Armor'}

DAGGER                    = 0
KUKRI                     = 1
CUTLASS                   = 2
SHORT_SWORD               = 3
KATANA                    = 4
LONGSWORD                 = 5
BROADSWORD                = 6
DOUBLE_ENDED_BROADSWORD   = 7
RAPIER                    = 8
KNUCKLEDUSTER             = 9
CLAWS                     = 10
GAUNTLETS                 = 11
AXE                       = 12
DOUBLE_HEADED_AXE         = 13
GIANT_AXE                 = 14
DOUBLE_HEADED_GIANT_AXE   = 15
MACE                      = 16
HAMMER                    = 17
DOUBLE_HEADED_HAMMER      = 18
GIANT_HAMMER              = 19
DOUBLE_ENDED_GIANT_HAMMER = 20
SPEAR                     = 21
PIKE                      = 22
HALBERD                   = 23
SHORT_STAFF               = 24
STAFF                     = 25

WEAPON_TYPES = {
    DAGGER: 'Dagger',
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
    STAFF: 'Staff',
}

CAN_DUAL_WIELD: {
    DAGGER: True,
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

# Armor
WEAPON          = 0
OFF_HAND_WEAPON = 1
NECKLACE        = 2
RING            = 3
HELMET          = 4
VAMBRACES       = 5
GLOVES          = 6
CHEST           = 7
GRIEVES         = 8
BOOTS           = 9

EQUIPMENT_CATEGORIES = {
    WEAPON: 'Weapon',
    OFF_HAND_WEAPON: 'Off-Hand Weapon',
    NECKLACE: 'Necklace',
    RING: 'Ring',
    HELMET: 'Helmet',
    VAMBRACES: 'Vambraces',
    GLOVES: 'Gloves',
    CHEST: 'Chest',
    GRIEVES: 'Grieves',
    BOOTS: 'Boots'
}


# Tools
PICKAXE                   = 0
SHOVEL                    = 1
HARVESTING_KNIFE          = 2

TOOL_TYPES = {
    PICKAXE: 'Pickaxe',
    SHOVEL: 'Shovel',
    HARVESTING_KNIFE: 'Harvesting Knife'
}

# Modifier Weights
DURABILITY = 0
HEALTH     = 1
MANA       = 2
PHY_ATK    = 3
MAG_ATK    = 4
DEF        = 5
WEIGHT     = 6


class EquipmentClass:
    def __init__(self, item_id, name, equipment_type, description):
        super().__init__()
        self._type = equipment_type
        self._item_id = item_id
        self._name = name
        self._description = description

        self._weights = None

    def get_id(self):
        return self._item_id

    def get_name(self):
        return self._name

    def get_type(self):
        return self._type

    def generate_hash(self):
        return time_ns()

    # TODO Add success weighting to generation
    def gen_min_max(self, minimum, maximum):
        return uniform(minimum, maximum)

    def gen_hardness(self, modifier, material):
        return self.gen_min_max(material.get_hardness() * modifier, material.get_max_hardness() * modifier)

    def gen_durability(self, modifier, material):
        material_durability = material.get_durability() * self._weights[DURABILITY]
        return self.gen_min_max(material_durability * modifier * material.get_hardness(), material_durability * modifier * material.get_max_hardness())

    def gen_health(self, modifier, material):
        material_health = material.get_health() * self._weights[HEALTH]
        return self.gen_min_max(material_health * modifier * material.get_hardness(), material_health * modifier * material.get_max_hardness())

    def gen_mana(self, modifier, material):
        material_mana = material.get_mana() * self._weights[MANA]
        return self.gen_min_max(material_mana * modifier * material.get_hardness(), material_mana * modifier * material.get_max_hardness())

    def gen_phy_atk(self, modifier, material):
        material_phy_atk = material.get_physical_attack() * self._weights[PHY_ATK]
        return self.gen_min_max(material_phy_atk * modifier * material.get_hardness(), material_phy_atk * modifier * material.get_max_hardness())

    def gen_mag_atk(self, modifier, material):
        material_mag_atk = material.get_magical_attack() * self._weights[MAG_ATK]
        return self.gen_min_max(material_mag_atk * modifier * material.get_hardness(), material_mag_atk * modifier * material.get_max_hardness())

    def gen_defense(self, modifier, material):
        material_defense = material.get_defense() * self._weights[DEF]
        return self.gen_min_max(material_defense * modifier * material.get_hardness(), material_defense * modifier * material.get_max_hardness())

    def gen_weight(self, modifier, material):
        material_weight = material.get_weight() * self._weights[WEIGHT]
        return self.gen_min_max(material_weight * modifier * material.get_hardness(), material_weight * modifier * material.get_max_hardness())


class ToolClass(EquipmentClass):
    def __init__(self, item_id, name, tool_type, description, durability_weight):
        super().__init__(item_id, name, EQUIPMENT_TOOL, description)
        self._tool_type = tool_type
        self._weights = [durability_weight]

    def get_tool_type(self):
        return self._tool_type

    def new_instance(self, metadata):
        material = Refs.gc['materials'][metadata['material_id']]

        if metadata['hash'] is None:
            item_hash = self.generate_hash()
            modifier = Refs.gc.get_random_modifier()
            hardness = self.gen_hardness(modifier, material)
            durability = durability_current = self.gen_durability(modifier, material)
        else:
            item_hash = metadata['hash']
            hardness = metadata['hardness']
            durability = metadata['durability']
            durability_current = metadata['durability_current']
        return Tool(self, item_hash, hardness, durability, durability_current, material)


class UngeneratedTool:
    def __init__(self, tool_class, material):
        self._tool_class = tool_class
        self._material = material

    def get_name(self):
        return f'{self._material.get_name()} {self._tool_class.get_name()}'


class WeaponClass(EquipmentClass):
    def __init__(self, item_id, name, weapon_type, description, weights):
        super().__init__(item_id, name, EQUIPMENT_WEAPON, description)
        self._weapon_type = weapon_type
        self._weights = weights

    def get_weapon_type(self):
        return self._weapon_type

    def new_instance(self, metadata):
        material = Refs.gc['materials'][metadata['material_id']]
        sub_material1 = sub_material2 = None
        if metadata['sub_material1_id'] is not None:
            sub_material1 = Refs.gc['materials'][metadata['sub_material1_id']]
        if metadata['sub_material2_id'] is not None:
            sub_material2 = Refs.gc['materials'][metadata['sub_material2_id']]

        if metadata['hash'] is None:
            item_hash = self.generate_hash()
            modifier = Refs.gc.get_random_modifier()
            # Get Hardness
            hardness = self.gen_hardness(modifier, material)
            if sub_material1:
                hardness += self.gen_hardness(modifier, sub_material1)
            if sub_material2:
                hardness += self.gen_hardness(modifier, sub_material2)
            # Get durability
            durability = durability_current = self.gen_durability(modifier, material)
            if sub_material1:
                durability += self.gen_durability(modifier, sub_material1)
            if sub_material2:
                durability += self.gen_durability(modifier, sub_material2)
            # Get weight
            weight = self.gen_weight(modifier, material)
            if sub_material1:
                weight += self.gen_weight(modifier, sub_material1)
            if sub_material2:
                weight += self.gen_weight(modifier, sub_material2)
            # Get health
            health = self.gen_health(modifier, material)
            if sub_material1:
                health += self.gen_health(modifier, sub_material1)
            if sub_material2:
                health += self.gen_health(modifier, sub_material2)
            # Get Mana
            mana = self.gen_mana(modifier, material)
            if sub_material1:
                mana += self.gen_mana(modifier, sub_material1)
            if sub_material2:
                mana += self.gen_mana(modifier, sub_material2)
            # Get Physical Attack
            phy_atk = self.gen_phy_atk(modifier, material)
            if sub_material1:
                phy_atk += self.gen_phy_atk(modifier, sub_material1)
            if sub_material2:
                phy_atk += self.gen_phy_atk(modifier, sub_material2)
            # Get magical Attack
            mag_atk = self.gen_mag_atk(modifier, material)
            if sub_material1:
                mag_atk += self.gen_mag_atk(modifier, sub_material1)
            if sub_material2:
                mag_atk += self.gen_mag_atk(modifier, sub_material2)
            # Get Defense
            defense = self.gen_defense(modifier, material)
            if sub_material1:
                defense += self.gen_defense(modifier, sub_material1)
            if sub_material2:
                defense += self.gen_defense(modifier, sub_material2)
        else:
            item_hash = metadata['hash']
            hardness = metadata['hardness']
            durability = metadata['durability']
            durability_current = metadata['durability_current']
            weight = metadata['weight']
            health = metadata['health']
            mana = metadata['mana']
            phy_atk = metadata['physical_attack']
            mag_atk = metadata['magical_attack']
            defense = metadata['defense']
        return Weapon(self, item_hash, hardness, durability, durability_current, material, sub_material1, sub_material2, weight, health, mana, phy_atk, mag_atk, defense)


class UngeneratedWeapon:
    def __init__(self, weapon_class, material, sub_material1, sub_material2):
        self._weapon_class = weapon_class
        self._material = material
        self._sub_material1 = sub_material1
        self._sub_material2 = sub_material2

    def get_name(self):
        if self._sub_material1 is None:
            return f'{self._material.get_name()} {self._weapon_class.get_name()}'
        else:
            return f'{self._material.get_name()}-{self._sub_material1.get_name()} {self._weapon_class.get_name()}'


class ArmorClass(EquipmentClass):
    def __init__(self, item_id, name, armor_type, description, weights):
        super().__init__(item_id, name, EQUIPMENT_ARMOR, description)
        self._armor_type = armor_type
        self._weights = weights

    def get_armor_type(self):
        return self._armor_type

    def new_instance(self, metadata):
        material = Refs.gc['materials'][metadata['material_id']]
        sub_material1 = sub_material2 = None
        if metadata['sub_material1_id'] is not None:
            sub_material1 = Refs.gc['materials'][metadata['sub_material1_id']]
        if metadata['sub_material2_id'] is not None:
            sub_material2 = Refs.gc['materials'][metadata['sub_material2_id']]

        if metadata['hash'] is None:
            item_hash = self.generate_hash()
            modifier = Refs.gc.get_random_modifier()
            # Get Hardness
            hardness = self.gen_hardness(modifier, material)
            if sub_material1:
                hardness += self.gen_hardness(modifier, sub_material1)
            if sub_material2:
                hardness += self.gen_hardness(modifier, sub_material2)
            # Get durability
            durability = durability_current = self.gen_durability(modifier, material)
            if sub_material1:
                durability += self.gen_durability(modifier, sub_material1)
            if sub_material2:
                durability += self.gen_durability(modifier, sub_material2)
            # Get weight
            weight = self.gen_weight(modifier, material)
            if sub_material1:
                weight += self.gen_weight(modifier, sub_material1)
            if sub_material2:
                weight += self.gen_weight(modifier, sub_material2)
            # Get health
            health = self.gen_health(modifier, material)
            if sub_material1:
                health += self.gen_health(modifier, sub_material1)
            if sub_material2:
                health += self.gen_health(modifier, sub_material2)
            # Get Mana
            mana = self.gen_mana(modifier, material)
            if sub_material1:
                mana += self.gen_mana(modifier, sub_material1)
            if sub_material2:
                mana += self.gen_mana(modifier, sub_material2)
            # Get Physical Attack
            phy_atk = self.gen_phy_atk(modifier, material)
            if sub_material1:
                phy_atk += self.gen_phy_atk(modifier, sub_material1)
            if sub_material2:
                phy_atk += self.gen_phy_atk(modifier, sub_material2)
            # Get magical Attack
            mag_atk = self.gen_mag_atk(modifier, material)
            if sub_material1:
                mag_atk += self.gen_mag_atk(modifier, sub_material1)
            if sub_material2:
                mag_atk += self.gen_mag_atk(modifier, sub_material2)
            # Get Defense
            defense = self.gen_defense(modifier, material)
            if sub_material1:
                defense += self.gen_defense(modifier, sub_material1)
            if sub_material2:
                defense += self.gen_defense(modifier, sub_material2)
        else:
            item_hash = metadata['hash']
            hardness = metadata['hardness']
            durability = metadata['durability']
            durability_current = metadata['durability_current']
            weight = metadata['weight']
            health = metadata['health']
            mana = metadata['mana']
            phy_atk = metadata['physical_attack']
            mag_atk = metadata['magical_attack']
            defense = metadata['defense']
        return Armor(self, item_hash, hardness, durability, durability_current, material, sub_material1, sub_material2, weight, health, mana, phy_atk, mag_atk, defense)


class UngeneratedArmor:
    def __init__(self, armor_class, material, sub_material1, sub_material2):
        self._armor_class = armor_class
        self._material = material
        self._sub_material1 = sub_material1
        self._sub_material2 = sub_material2

    def get_name(self):
        if self._sub_material1 is None:
            return f'{self._material.get_name()} {self._armor_class.get_name()}'
        else:
            return f'{self._material.get_name()}-{self._sub_material1.get_name()} {self._armor_class.get_name()}'


class Equipment(HMPMD):
    def __init__(self, equipment_class, item_hash, hardness, durability, durability_current):
        super().__init__(0, 0, 0, 0, 0)
        self._class = equipment_class
        self._hash = item_hash

        self._hardness = hardness
        self._durability = durability
        self._durability_current = durability_current

        self._rank = 'I'
        self._element = NONE
        self._score = 0
        self._worth = 0

    def get_id(self):
        return self._class.get_id()

    def get_full_id(self):
        return self._class.get_id() + '#' + str(self._hash)

    def get_hash(self):
        return self._hash

    def get_metadata(self):
        return {
            'hash': self._hash,
            'hardness': self._hardness,
            'durability': self._durability,
            'durability_current': self._durability_current
        }

    def get_type(self):
        return self._class.get_type()

    def get_name(self):
        return f'{self.get_durability_string()} {self._class.get_name()}'

    def get_hardnesss(self):
        return self._hardness

    def get_durability_string(self):
        lifespan = self._durability_current / self._durability
        if lifespan > 0.9:
            return 'Pristine'
        elif lifespan > 0.5:
            return 'Well-Used'
        elif lifespan > 0.2:
            return 'Worn'
        else:
            return 'Crumbling'

    def get_durability(self):
        return self._durability

    def get_current_durability(self):
        return self._durability_current

    def remove_durability(self, wear_value):
        self._durability_current -= wear_value

    def get_element(self):
        return self._element

    def get_score(self):
        return self._score

    def get_value(self):
        return self._worth

    def get_rank(self):
        return self._rank


class Tool(Equipment):
    def __init__(self, tool_class, item_hash, hardness, durability, durability_current, material):
        super().__init__(tool_class, item_hash, hardness, durability, durability_current)

        self._material = material

    def get_name(self):
        return f'{self.get_durability_string()} {self._material.get_name()} {self._class.get_name()}'

    def get_metadata(self):
        return {
            'hash': self._hash,
            'hardness': self._hardness,
            'durability': self._durability,
            'durability_current': self._durability_current,
            'material_id': self._material.get_id()
        }


class Weapon(Equipment):
    def __init__(self, weapon_class, item_hash, hardness, durability, durability_current, material, sub_material1, sub_material2, weight, hp, mp, p, m, d):
        super().__init__(weapon_class, item_hash, hardness, durability, durability_current)

        self._material = material
        self._sub_material1 = sub_material1
        self._sub_material2 = sub_material2

        # TODO Implement material effects

        self._weight = weight

        self._health = hp
        self._mana = mp
        self._physical_attack = p
        self._magical_attack = m
        self._defense = d
        self.refresh_stats()

    def get_name(self):
        if self._sub_material1 is None:
            return f'{self.get_durability_string()} {self._material.get_name()} {self._class.get_name()}'
        else:
            return f'{self.get_durability_string()} {self._material.get_name()}-{self._sub_material1.get_name()} {self._class.get_name()}'

    def get_metadata(self):
        metadata = super().get_metadata()
        metadata.update({
            'weight': self._weight,
            'health': self._health,
            'mana': self._mana,
            'physical_attack': self._physical_attack,
            'magical_attack': self._magical_attack,
            'defense': self._defense,
            'material_id': self._material.get_id(),
            'sub_material1_id': self._sub_material1.get_id(),
            'sub_material2_id': self._sub_material2.get_id()
        })
        return metadata


class Armor(Equipment):
    def __init__(self, armor_class, item_hash, hardness, durability, durability_current, material, sub_material1, sub_material2, weight, hp, mp, p, m, d):
        super().__init__(armor_class, item_hash, hardness, durability, durability_current)

        self._material = material
        self._sub_material1 = sub_material1
        self._sub_material2 = sub_material2

        # TODO Implement material effects

        self._weight = weight

        self._health = hp
        self._mana = mp
        self._physical_attack = p
        self._magical_attack = m
        self._defense = d
        self.refresh_stats()

    def get_name(self):
        if self._sub_material1 is None:
            return f'{self.get_durability_string()} {self._material.get_name()} {self._class.get_name()}'
        else:
            return f'{self.get_durability_string()} {self._material.get_name()}-{self._sub_material1.get_name()} {self._class.get_name()}'

    def get_metadata(self):
        metadata = super().get_metadata()
        metadata.update({
            'weight': self._weight,
            'health': self._health,
            'mana': self._mana,
            'physical_attack': self._physical_attack,
            'magical_attack': self._magical_attack,
            'defense': self._defense,
            'material_id': self._material.get_id(),
            'sub_material1_id': self._sub_material1.get_id(),
            'sub_material2_id': self._sub_material2.get_id()
        })
        return metadata
