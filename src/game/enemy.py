from copy import copy
from random import choices, randint, uniform

from game.battle_enemy import BattleEnemy
from refs import Refs

LEVEL_MULTIPLIER = [1, 1.5, 2, 2.75, 3.5, 4.75, 6, 8, 10]
NICKNAMES = ['', 'Uncommon ', 'Abnormal ', 'Scary ', 'Freaky ', 'Menacing ', 'Nightmarish ', 'Titan ', 'World Devourer ']

STAT_INDEX = [0.75, 1, 1.25, 1.5, 1.75, 2, 2.5, 3, 4, 6, 8, 12]
HEALTH, STR, MAG, END, AGI, DEX = 0, 1, 2, 3, 4, 5


class Enemy:
    def __init__(self, identifier, name, skeleton_id, program_type, attack_type, min_hsmead, max_hsmead, elements, harvest_hardness, skills, skill_probabilities, drops):
        self._id = identifier
        self._name = name
        self._skel_id = skeleton_id
        self._skel_path = f'res/enemies/{program_type}/{name.lower()}/{skeleton_id}.skel'

        self._skills = skills
        self._skill_probabilities = skill_probabilities
        self._attack_type = attack_type
        self._harvest_hardness = harvest_hardness

        self._min_hsmead = min_hsmead
        self._max_hsmead = max_hsmead

        self._element = elements[0]
        self._sub_element = elements[1]

        self._drops = {'guaranteed': drops['guaranteed']}

        for index, key in enumerate(['crystal', 'falna', 'drop']):
            rarity_list = []
            for rarity in range(1, 6):
                drop_list = []
                if rarity == 1:
                    drop_list = [None]
                for (item_id, rarity) in drops[key]:
                    if rarity <= rarity:
                        drop_list += (item_id, rarity + 1 - int(rarity))
                rarity_list.append(drop_list)
            self._drops[key] = rarity_list

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def generate_drop(self, boost, hardness):
        if hardness < self._harvest_hardness:
            return []
        drops = []
        rarities = choices([1, 2, 3, 4, 5], [1 / (2 ** (x + 1)) for x in range(5)], k=3)
        # Generate guaranteed drops
        for item_id in self._drops['guaranteed']:
            drops.append((item_id, 1))
        # Generate other drops
        for index, key in enumerate(['crystal', 'falna', 'drop']):
            drop_list = copy(self._drops[key][rarities[index]])
            # TODO Remove Materials if hardness not enough
            if key == 'drop':
                remove = []
                for (drop_id, count) in drop_list:
                    if Refs.gc['materials'][drop_id].get_hardness() > hardness:
                        remove.append((drop_id, count))
                for id in remove:
                    drop_list.remove(id)

            if boost > 2:
                for sub_boost in [randint(2, int(boost / 2)), randint(2, int(boost / 2))]:
                    drop_id, count = drop_list[randint(0, len(drop_list) - 1)]
                    drops.append((drop_id, count * sub_boost))
            else:
                drop_id, count = drop_list[randint(0, len(drop_list) - 1)]
                drops.append((drop_id, count * boost))
        return drops

    def get_score(self, boost):
        return (sum(self._min_hsmead) + (sum(self._max_hsmead) - sum(self._min_hsmead)) / 2) / 5 * LEVEL_MULTIPLIER[boost]

    def new_instance(self, boost):
        multiplier = LEVEL_MULTIPLIER[boost]
        nickname = NICKNAMES[boost]

        hmsmead = [0.0 for _ in range(DEX + 1)]
        for stat in range(DEX + 1):
            hmsmead[stat] = uniform(self._min_hsmead[stat] * multiplier, self._max_hsmead[stat] * multiplier)

        return BattleEnemy(self._id, f'{nickname}{self._name}', self._skel_path, self._attack_type, hmsmead[HEALTH], 0, hmsmead[STR], hmsmead[MAG], hmsmead[END], hmsmead[AGI], hmsmead[DEX], boost, self._element, self._sub_element, self._skills, self._skill_probabilities)
