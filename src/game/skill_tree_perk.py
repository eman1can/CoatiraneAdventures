class Perk:
    def __init__(self, perk_id, name, tree, level, description, requirements):
        self._id = perk_id
        self._name = name
        self._tree = tree
        self._level = int(level)
        self._description = description
        self._requirements = requirements

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_cost(self):
        return {4: 105, 3: 21, 2: 3, 1: 1}[self._level]

    def get_tree(self):
        return self._tree

    def get_level(self):
        return self._level

    def get_description(self):
        return self._description

    def get_requirements(self):
        return self._requirements