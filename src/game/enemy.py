from random import choices, randint

from game.battle_enemy import BattleEnemy

STAT_INDEX = [0.75, 1, 1.25, 1.5, 1.75, 2, 2.5, 3, 4, 6, 8, 12]


class Enemy:
    def __init__(self, eid, name, skeleton_id, program_type, attack_type, min_health, max_health, min_strength, max_strength, min_magic, max_magic, min_agility, max_agility, min_dexterity,
                 max_dexterity, min_endurance, max_endurance, moves, move_probabilities):
        self.id = eid
        self.name = name
        self.skel_id = skeleton_id
        self.skel_path = f'res/enemies/{program_type}/{name.lower()}/{skeleton_id}.skel'
        self.moves = moves
        self.move_probabilities = move_probabilities
        self.attack_type = attack_type
        self.min_health = min_health
        self.max_health = max_health
        self.min_strength = min_strength
        self.max_strength = max_strength
        self.min_magic = min_magic
        self.max_magic = max_magic
        self.min_agility = min_agility
        self.max_agility = max_agility
        self.min_dexterity = min_dexterity
        self.max_dexterity = max_dexterity
        self.min_endurance = min_endurance
        self.max_endurance = max_endurance
        self.element = None
        self._crystal_chance = None
        self._crystal_drops = None
        self._optional_drops = None

    def set_drops(self, crystal_drop_chance, crystal_drops, optional_drops):
        self._crystal_chance = crystal_drop_chance
        self._crystal_drops = crystal_drops
        self._optional_drops = optional_drops

    def generate_drop(self):
        drops = []
        if randint(1, 100) <= self._crystal_chance * 100:
            drops += choices(list(self._crystal_drops.keys()), list(self._crystal_drops.values()))
        drops += choices(list(self._optional_drops.keys()), list(self._optional_drops.values()), k=choices([1, 2, 3], [3, 2, 1])[0])
        return drops

    def get_id(self):
        return self.id

    def get_score(self):
        return (self.max_strength + self.max_magic + self.max_agility + self.max_dexterity + self.max_endurance) / 15

    def new_instance(self, level):
        stat_multiplier = STAT_INDEX[level - 1]
        return BattleEnemy(level, self.id, self.name, self.skel_path, self.attack_type,
                           randint(int(self.min_health * stat_multiplier), int(self.max_health * stat_multiplier)),
                           0,
                           randint(int(self.min_strength * stat_multiplier), int(self.max_strength * stat_multiplier)),
                           randint(int(self.min_magic * stat_multiplier), int(self.max_magic * stat_multiplier)),
                           randint(int(self.min_endurance * stat_multiplier), int(self.max_endurance * stat_multiplier)),
                           randint(int(self.min_dexterity * stat_multiplier), int(self.max_dexterity * stat_multiplier)),
                           randint(int(self.min_agility * stat_multiplier), int(self.max_agility * stat_multiplier)),
                           self.element, self.moves, self.move_probabilities)
