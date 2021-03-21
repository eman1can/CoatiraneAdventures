from random import choices, randint

from game.battle_enemy import BattleEnemy

LEVEL_MULTIPLITER = [1, 1.5, 2, 2.75, 3.5, 4.75, 6, 8, 10]

STAT_INDEX = [0.75, 1, 1.25, 1.5, 1.75, 2, 2.5, 3, 4, 6, 8, 12]
HEALTH, MANA, STR, MAG, END, AGI, DEX = 0, 1, 2, 3, 4, 5, 6


class Enemy:
    def __init__(self, identifier, name, skeleton_id, program_type, attack_type, min_hmsmead, max_hmsmead, moves, move_probabilities, drops):
        self._id = identifier
        self._name = name
        self._skel_id = skeleton_id
        self._skel_path = f'res/enemies/{program_type}/{name.lower()}/{skeleton_id}.skel'
        self._moves = moves
        self._move_probabilities = move_probabilities
        self._attack_type = attack_type
        self._min_hmsmead = min_hmsmead
        self._max_hmsmead = max_hmsmead
        self._element = None
        self._drops = {'guaranteed': drops['guaranteed']}
        for index, key in enumerate(['crystal', 'falna', 'drop']):
            rarity_list = []
            for rarity in range(1, 6):
                drop_list = []
                if rarity == 1:
                    drop_list = [None]
                for (item_id, rarity) in self._drops[key]:
                    if rarity <= rarity:
                        drop_list += (item_id, rarity + 1 - int(rarity))
                rarity_list.append(drop_list)
            self._drops[key] = rarity_list

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def generate_drop(self, boost):
        drops = []
        rarities = choices([1, 2, 3, 4, 5], [1 / (2 ** (x + 1)) for x in range(5)], k=3)
        # Generate guaranteed drops
        for item_id in self._drops['guaranteed']:
            drops += (item_id, 1)
        # Generate other drops
        for index, key in enumerate(['crystal', 'falna', 'drop']):
            drop_list = self._drops[key][rarities[index]]
            drops += drop_list[randint(0, len(drop_list) - 1)]
        return drops

    def get_score(self, boost):
        return (sum(self._min_hmsmead) + (sum(self._max_hmsmead) - sum(self._min_hmsmead)) / 2) / 5 * LEVEL_MULTIPLITER[boost]

    def new_instance(self, boost):
        multiplier = LEVEL_MULTIPLITER[boost]

        hmsmead = [0, 0, 0, 0, 0]
        for stat in range(DEX + 1):
            hmsmead[stat] = randint(self._min_hmsmead[stat] * multiplier, self._max_hmsmead[stat] * multiplier)

        return BattleEnemy(self._id, self._name, self._skel_path, self._attack_type, hmsmead[HEALTH], hmsmead[MANA], hmsmead[STR], hmsmead[MAG], hmsmead[END], hmsmead[AGI], hmsmead[DEX], self.element, self.moves, self.move_probabilities)
