import random

class Floor:
    """
    Boss Type:
    0 - Boss is a single Enemy and has been passed in the boss parameter
    1 - Boss is multiple of the passed boss parameter with maxCounts
    2 - Boss is multiple of the passed boss parameter with maxCounts upped by 40%
    3 - Boss is multiple of normally passed enemies - maxCounts upped by 40%
    4 - Boss is multiple of normally passed enemies - maxCounts upped by 40% & stats upped by 30%
    """

    def __init__(self, floorid, maxEnemies, minEncounters, maxEncounters, bossType, boss, Enemies, propabilities):
        self.floorid, self.maxEnemies = floorid, maxEnemies
        self.minEncounters, self.maxEncounters = minEncounters, maxEncounters
        self.bossType, self.boss = bossType, boss
        self.enemies = Enemies
        self.propabilities = propabilities
        self.PERCENT100 = 100
        self.BOSSMULTIPLIER = .4
        self.BOSSSTATMULTIPLIER = .3
        self.MINMAXENEMIES = .25

    def generateEncounterNumber(self):
        return random.randint(self.minEncounters, self.maxEncounters)

    def generateBoss(self):
        if self.bossType == 0:
            return [self.boss]
        elif self.bossType == 1:
            min = int(self.maxEnemies * self.MINMAXENEMIES)
            if not min > 1:
                min = 1
            num = random.randint(min, self.maxEnemies)
            enemies = []
            for x in range(num):
                enemies.append(self.boss)
            return enemies
        elif self.bossType == 2:
            min = int(self.maxEnemies * (self.MINMAXENEMIES + self.BOSSMULTIPLIER))
            if not min > 1:
                min = 1
            num = random.randint(min,
                                 int(self.maxEnemies * (1 + self.BOSSMULTIPLIER)))
            enemies = []
            for x in range(num):
                enemies.append(self.boss)
            return enemies
        elif self.bossType == 3:
            min = int(self.maxEnemies * (self.MINMAXENEMIES + self.BOSSMULTIPLIER))
            if not min > 1:
                min = 1
            num = random.randint(min, int(self.maxEnemies * (1 + self.BOSSMULTIPLIER)))
            enemies = []
            for x in range(num):
                num = random.randint(0, self.PERCENT100)
                for y in range(len(self.propabilities)):
                    if num < (self.propabilities[y] * self.PERCENT100):
                        enemies.append(self.enemies[y].new_instance(1))
                        break
                    else:
                        num -= (self.propabilities[y] * self.PERCENT100)
            return enemies
        elif self.bossType == 4:
            min = int(self.maxEnemies * (self.MINMAXENEMIES + self.BOSSMULTIPLIER))
            if not min > 1:
                min = 1
            num = random.randint(min, int(self.maxEnemies * (1 + self.BOSSMULTIPLIER)))
            enemies = []
            for x in range(num):
                num = random.randint(0, self.PERCENT100)
                for y in range(len(self.propabilities)):
                    if num < (self.propabilities[y] * self.PERCENT100):
                        enemies.append(self.enemies[y].new_instance(1 + self.BOSSSTATMULTIPLIER))
                        break
                    else:
                        num -= (self.propabilities[y] * self.PERCENT100)
            return enemies

    def generateEnemies(self):
        min = int(self.maxEnemies * self.MINMAXENEMIES)
        if not min > 1:
            min = 1
        num = random.randint(min, self.maxEnemies)
        enemies = []
        for x in range(num):
            num = random.randint(0, self.PERCENT100)
            for y in range(len(self.propabilities)):
                if num < (self.propabilities[y] * self.PERCENT100):
                    enemies.append(self.enemies[y].new_instance(1))
                    break
                else:
                    num -= (self.propabilities[y] * self.PERCENT100)
        return enemies