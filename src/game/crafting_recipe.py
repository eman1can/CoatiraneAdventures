# Base Recipe Type; Determines which recipe class to use
from game.crafting_queue import CRAFT_HARD_ALLOY, CRAFT_HARD_ALLOY_LEVEL, CRAFT_SOFT_ALLOY, CRAFT_SOFT_ALLOY_LEVEL, ITEM_LEVEL, LEVEL_1, LEVEL_2, LEVEL_3, PROCESS_HARD_MATERIAL, PROCESS_HARD_MATERIAL_LEVEL, PROCESS_SOFT_MATERIAL, \
    PROCESS_SOFT_MATERIAL_LEVEL

ITEM      = 0
PROCESS   = 1
ALLOY     = 2
EQUIPMENT = 3


class Recipe:
    def __init__(self, recipe_type, output_id, output_count, crafting_type, crafting_time, ingredients):
        self._type = recipe_type
        self._crafting_type = crafting_type
        self._perk_requirement = self._get_perk_requirement()
        self._output_id = output_id
        self._output_count = output_count
        self._crafting_time = crafting_time
        self._ingredients = ingredients

    def get_type(self):
        return self._type

    def get_crafting_type(self):
        return self._crafting_type

    def get_output_id(self):
        return self._output_id

    def get_item_count(self):
        return self._output_count

    def get_ingredients(self):
        return self._ingredients

    def get_crafting_time(self):
        return self._crafting_time

    def get_perk_requirement(self):
        return self._perk_requirement

    def _get_perk_requirement(self):
        if self._type == EQUIPMENT:
            return 'Unknown'
        if self._crafting_type & ITEM == ITEM:
            if (self._crafting_type << ITEM_LEVEL) & LEVEL_1 == LEVEL_1:
                return 'daedalus_protege'
            elif (self._crafting_type << ITEM_LEVEL) & LEVEL_2 == LEVEL_2:
                return 'beginning_of_enigma'
            else:
                return 'truth_to_enigma'
        elif self._crafting_type & PROCESS_SOFT_MATERIAL:
            if(self._crafting_type << PROCESS_SOFT_MATERIAL_LEVEL) & LEVEL_1 == LEVEL_1:
                return 'basic_tailor'
            elif (self._crafting_type << PROCESS_SOFT_MATERIAL_LEVEL) & LEVEL_2 == LEVEL_2:
                return 'reputable_tailor'
            elif (self._crafting_type << PROCESS_SOFT_MATERIAL_LEVEL) & LEVEL_3 == LEVEL_2:
                return 'famous_tailor'
            else:
                return 'master_tailor'
        elif self._crafting_type & PROCESS_HARD_MATERIAL:
            if (self._crafting_type << PROCESS_HARD_MATERIAL_LEVEL) & LEVEL_1 == LEVEL_1:
                return 'apprentice_blacksmith'
            elif (self._crafting_type << PROCESS_HARD_MATERIAL_LEVEL) & LEVEL_2 == LEVEL_2:
                return 'skilled_blacksmith'
            elif (self._crafting_type << PROCESS_HARD_MATERIAL_LEVEL) & LEVEL_3 == LEVEL_2:
                return 'famous_blacksmith'
            else:
                return 'master_blacksmith'
        elif self._crafting_type & CRAFT_SOFT_ALLOY:
            if (self._crafting_type << CRAFT_SOFT_ALLOY_LEVEL) & LEVEL_1 == LEVEL_1:
                return 'basic_tailor'
            elif (self._crafting_type << CRAFT_SOFT_ALLOY_LEVEL) & LEVEL_2 == LEVEL_2:
                return 'reputable_tailor'
            elif (self._crafting_type << CRAFT_SOFT_ALLOY_LEVEL) & LEVEL_3 == LEVEL_2:
                return 'famous_tailor'
            else:
                return 'master_tailor'
        elif self._crafting_type & CRAFT_HARD_ALLOY:
            if (self._crafting_type << CRAFT_HARD_ALLOY_LEVEL) & LEVEL_1 == LEVEL_1:
                return 'basic_tailor'
            elif (self._crafting_type << CRAFT_HARD_ALLOY_LEVEL) & LEVEL_2 == LEVEL_2:
                return 'reputable_tailor'
            elif (self._crafting_type << CRAFT_HARD_ALLOY_LEVEL) & LEVEL_3 == LEVEL_2:
                return 'famous_tailor'
            else:
                return 'master_tailor'
