class Material:
    def __init__(self, material_type, identifier, name, min_hardness, max_hardness, raw_form, processed_form, effect, sub_effect):
        self._id = identifier
        self._name = name
        self._type = material_type
        self._min_hardness = min_hardness
        self._max_hardness = max_hardness
        self._effect = effect
        self._sub_effect = sub_effect

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def is_hard(self):
        return self._type == 'hard'

    def is_soft(self):
        return self._type == 'soft'
