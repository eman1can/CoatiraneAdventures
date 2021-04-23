ITEM      = 0
EQUIPMENT = 1

PROCESS_MATERIALS = 'process_materials'
CRAFT_ALLOYS = 'crafting_alloys'


class Recipe:
    def __init__(self, type, output_id, output_count, ingredients):
        self._type = type
        self._output_id = output_id
        self._output_count = output_count
        self._ingredients = ingredients

    def get_type(self):
        return self._type

    def get_item_id(self):
        return self._output_id

    def get_item_count(self):
        return self._output_count

    def get_ingredients(self):
        return self._ingredients


class EquipmentRecipe(Recipe):
    def __init__(self, output_id, ingredients):
        super().__init__(EQUIPMENT, output_id, 1, ingredients)


class ItemRecipe(Recipe):
    def __init__(self, output_id, output_count, perk_requirement, sub_type, ingredients):
        super().__init__(ITEM, output_id, output_count, ingredients)

        self._perk_requirement = perk_requirement
        self._sub_type = sub_type

    def get_sub_type(self):
        return self._sub_type

    def get_perk_requirement(self):
        return self._perk_requirement
