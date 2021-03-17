class Material:
    def __init__(self, name, min_hardness, max_hardness, effect, sub_effect):
        self._name = name
        self._min_hardness = min_hardness
        self._max_hardness = max_hardness
        self._effect = effect
        self._sub_effect = sub_effect

    def get_name(self):
        return self._name
