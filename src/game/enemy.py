from copy import copy
from math import ceil
from random import choices, randint, uniform

from game.battle_enemy import BattleEnemy
from game.entity import Entity
from refs import Refs

LEVEL_MULTIPLIER = [1, 1.5, 2, 2.75, 3.5, 4.75, 6, 8, 10]
NICKNAMES = ['', 'Uncommon ', 'Abnormal ', 'Scary ', 'Freaky ', 'Beastly ', 'Menacing ', 'Nightmarish ', 'World Devouring ']

# - - 1 1 Common - Bronze Background
# 0 0 2 2 Uncommon - Bronze Background w/ bloody background
# 1 0 3 3 Abnormal - Bronze Background w/ chaos background
# 2 0 4 4 Scary - Silver background w/ 2nd stage monster
# 3 1 5 5 Freaky - Silver background w/ 2nd stage monster and bloody background
# 4 1 6 0 Beastly - Silver Background w/ 2nd stage monster and chaos background
# 5 1 4 Menacing - Gold background w/ 2nd stage monster
# 6 2 5 Nightmarish - Gold background w/ 2nd stage background and bloody background
# 7 2 6 World Devouring - Gold background w/ 2nd stage background and chaos background

STAT_INDEX = [0.75, 1, 1.25, 1.5, 1.75, 2, 2.5, 3, 4, 6, 8, 12]
HEALTH, STR, MAG, END, AGI, DEX = 0, 1, 2, 3, 4, 5


class Enemy:
    def __init__(self, identifier, name, skeleton_id, program_type, attack_type, min_hsmead, max_hsmead, elements, harvest_hardness, skills, skill_probabilities, drops):
        self._id = identifier
        self._name = name
        self._skel_id = skeleton_id
        self._skel_path = f'res/enemies/{name.lower().replace(" ", "_")}/{skeleton_id}.skel'

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
                for (item_id, item_rarity) in drops[key]:
                    if item_rarity <= rarity:
                        drop_list.append((item_id, rarity + 1 - int(item_rarity)))
                rarity_list.append(drop_list)
            self._drops[key] = rarity_list

        self._drops_list = []
        for index, key in enumerate(['crystal', 'falna', 'drop']):
            for (item_id, rarity) in drops[key]:
                self._drops_list.append(item_id)
        self._drops_list += drops['guaranteed']

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
            drop_list = copy(self._drops[key][rarities[index] - 1])
            if key == 'drop':
                remove = []
                for drop in drop_list:
                    if drop is not None:
                        (drop_id, count) = drop
                        for material in Refs.gc['materials'].values():
                            if material.get_raw_id() == drop_id and material.get_hardness() > hardness:
                                remove.append(drop)
                                break
                    else:
                        remove.append(drop)
                for drop in remove:
                    drop_list.remove(drop)

            if len(drop_list) == 0:
                continue

            if boost >= 2:  # Boost goes from 0 → 4
                for sub_boost in [randint(0, ceil(boost / 2)), randint(0, ceil(boost / 2))]:
                    drop = drop_list[randint(0, len(drop_list) - 1)]
                    if drop is None:
                        continue
                    drop_id, count = drop
                    drops.append((drop_id, count * (sub_boost + 1)))
            else:
                drop = drop_list[randint(0, len(drop_list) - 1)]
                if drop is None:
                    continue
                drop_id, count = drop
                drops.append((drop_id, count * (boost + 1)))
        return drops

    def get_drop_items(self):
        return self._drops

    def get_unqiue_drop_items(self):
        return self._drops_list

    def get_score(self, boost):
        return (sum(self._min_hsmead) + (sum(self._max_hsmead) - sum(self._min_hsmead)) / 2) / 5 * LEVEL_MULTIPLIER[boost]

    def new_instance(self, boost):
        multiplier = LEVEL_MULTIPLIER[boost]
        nickname = NICKNAMES[boost]

        hmsmead = [0.0 for _ in range(DEX + 1)]
        for stat in range(DEX + 1):
            hmsmead[stat] = uniform(self._min_hsmead[stat] * multiplier, self._max_hsmead[stat] * multiplier)
        entity = Entity(self._id, f'{nickname}{self._name}', self._skel_path, hmsmead[HEALTH], 0, hmsmead[STR], hmsmead[MAG], hmsmead[END], hmsmead[STR], hmsmead[MAG], hmsmead[END], hmsmead[AGI], hmsmead[DEX], self._element, self._skills)
        return BattleEnemy(entity, boost, self._skill_probabilities, self._sub_element, self._id + str(randint(0, 1000000)))
