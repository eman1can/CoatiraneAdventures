# Element Types
from random import choices

from game.battle_entity import BattleEntity
from game.entity import Entity


class BattleEnemy(BattleEntity, Entity):
    def __init__(self, level, id, name, skeleton_path, attack_type, health, mana, strength, magic, endurance, dexterity, agility, element, moves, move_chances):
        print(strength, magic, endurance, dexterity, agility)
        Entity.__init__(self, name, skeleton_path, health, mana, strength, magic, endurance, strength, magic, endurance, dexterity, agility, element, moves)
        BattleEntity.__init__(self)
        self._level = level
        self._id = id
        self._move_chances = move_chances
        self._attack_type = attack_type
        self._bhealth = self.get_health()

    def get_id(self):
        return self._id

    def get_idle_animation(self):
        return 'idle'

    def get_level(self):
        return self._level

    def get_selected_skill(self):
        return choices(self.get_skills(), self.get_skill_chances(), k=1)[0]

    def get_skills(self):
        return self._moves[0:1] + self._moves[3:]

    def get_skill_chances(self):
        return self._move_chances[0:1] + self._move_chances[3:]

    def is_character(self):
        return False

    def is_enemy(self):
        return True

    # def generateSpeed(self):
    #     return random.randint(int(self.agi * .85 * 21), int(self.agi * 21))
    #
    # def processDamage(self, damage, char):
    #     print("Damage is " + str(damage))
    #     # base damage calculation
    #
    #     # Penetration
    #     pen = random.randint(0, 100) <= 20 * (1 + (Scale.getScale_as_number(char.totalStrength, char.ranks[
    #         char.currentRank - 1].StrengthMax) + Scale.getScale_as_number(char.totalDexterity, char.ranks[
    #         char.currentRank - 1].dexterityMax) / 2))
    #     if pen:
    #         print("Penetration.")
    #         damage *= 1.5
    #     # Guarding
    #     guard = random.randint(0, 100) <= 20 * (1 + (Scale.getScale_as_number(char.totalAgility, char.ranks[
    #         char.currentRank - 1].agilityMax) + Scale.getScale_as_number(char.totalDexterity, char.ranks[
    #         char.currentRank - 1].dexterityMax) / 2))
    #     if guard and not pen:
    #         print("Guard.")
    #         damage *= 0.5
    #     # Calculating Critical dex & agi
    #     crit = random.randint(0, 100) <= 20 * (1 + (Scale.getScale_as_number(char.totalAgility, char.ranks[
    #         char.currentRank - 1].agilityMax) + Scale.getScale_as_number(char.totalDexterity, char.ranks[
    #         char.currentRank - 1].dexterityMax) / 2))
    #
    #     if crit:
    #         print("Critical hit.")
    #         damage *= 1.5
    #
    #     # Penetration
    #     if agi > self.dex:
    #         topShelf = 0
    #         print("No Miss. Damage mult 2.4")
    #         damage *= 2.4
    #     else:
    #         topShelf = agi / self.dex
    #     print("Hit Chance is " + str((topShelf * 100) - 20))
    #     if not topShelf == 0:
    #         hit = random.randint(0, int(topShelf * 100)) > 20
    #     else:
    #         hit = True
    #     print("Hit: " + str(hit) + " for " + str(damage))
    #     if hit:
    #         self.health -= damage
    #     else:
    #         damage = 0
    #     return damage