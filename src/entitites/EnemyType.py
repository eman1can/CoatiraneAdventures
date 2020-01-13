class EnemyType:

    def __init__(self, name, attackType, healthMin, healthMax, strMin, strMax, magMin, magMax, agiMin, agiMax, dexMin,
                 dexMax, endMin, endMax, moves, movesPropabilities):
        self.name = name
        self.moves = moves
        self.movePropabilities = movesPropabilities
        self.attackType = attackType
        self.healthMin = healthMin
        self.healthMax = healthMax
        self.strMin = strMin
        self.strMax = strMax
        self.magMin = magMin
        self.magMax = magMax
        self.agiMin = agiMin
        self.agiMax = agiMax
        self.dexMin = dexMin
        self.dexMax = dexMax
        self.endMin = endMin
        self.endMax = endMax

    def new_instance(self, statMultiplier):
        return Enemy(self.name, self.attackType,
                     random.randint(self.healthMin * statMultiplier, self.healthMax * statMultiplier),
                     random.randint(self.strMin * statMultiplier, self.strMax * statMultiplier),
                     random.randint(self.magMin * statMultiplier,
                                    self.magMax * statMultiplier),
                     random.randint(self.agiMin * statMultiplier, self.agiMax * statMultiplier),
                     random.randint(self.dexMin * statMultiplier, self.dexMax * statMultiplier),
                     random.randint(self.endMin * statMultiplier, self.endMax * statMultiplier), self.moves,
                     self.movePropabilities)