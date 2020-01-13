class Enemy:

    def __init__(self, name, attackType, health, str, mag, agi, dex, end, moves, movePropabilities):
        self.name, self.attackType, self.health, self.str, self.mag, self.agi, self.dex, self.end = name, attackType, health, str, mag, agi, dex, end
        self.moves = moves
        self.movePropabilities = movePropabilities

    def generateSpeed(self):
        return random.randint(int(self.agi * .85 * 21), int(self.agi * 21))

    def processDamage(self, damage, char):
        print("Damage is " + str(damage))
        # base damage calculation

        # Penetration
        pen = random.randint(0, 100) <= 20 * (1 + (Scale.getScale_as_number(char.totalStrength, char.ranks[
            char.currentRank - 1].StrengthMax) + Scale.getScale_as_number(char.totalDexterity, char.ranks[
            char.currentRank - 1].dexterityMax) / 2))
        if pen:
            print("Penetration.")
            damage *= 1.5
        # Guarding
        guard = random.randint(0, 100) <= 20 * (1 + (Scale.getScale_as_number(char.totalAgility, char.ranks[
            char.currentRank - 1].agilityMax) + Scale.getScale_as_number(char.totalDexterity, char.ranks[
            char.currentRank - 1].dexterityMax) / 2))
        if guard and not pen:
            print("Guard.")
            damage *= 0.5
        # Calculating Critical dex & agi
        crit = random.randint(0, 100) <= 20 * (1 + (Scale.getScale_as_number(char.totalAgility, char.ranks[
            char.currentRank - 1].agilityMax) + Scale.getScale_as_number(char.totalDexterity, char.ranks[
            char.currentRank - 1].dexterityMax) / 2))

        if crit:
            print("Critical hit.")
            damage *= 1.5

        # Penetration
        if agi > self.dex:
            topShelf = 0
            print("No Miss. Damage mult 2.4")
            damage *= 2.4
        else:
            topShelf = agi / self.dex
        print("Hit Chance is " + str((topShelf * 100) - 20))
        if not topShelf == 0:
            hit = random.randint(0, int(topShelf * 100)) > 20
        else:
            hit = True
        print("Hit: " + str(hit) + " for " + str(damage))
        if hit:
            self.health -= damage
        else:
            damage = 0
        return damage