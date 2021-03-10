class Ability:
    def __init__(self, id=0, name='', description='', has_effect=False, effects=None, rank=0, points=0.0):
        self.id = id
        self.name = name
        self.description = description
        self.has_effect = has_effect
        if effects is None:
            effects = []
        self.effects = effects
        self.rank = rank
        self.points = points

    def get_name(self):
        return self.name