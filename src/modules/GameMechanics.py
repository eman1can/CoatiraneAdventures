import random


class GameMechanics:


    """
    Name: Familiarity Bonus
    A bonus value that goes from 0-100
    and generates a 0-48% increase in base stats for characters

    Every Encounter which will call this method will give between a
    0.01 to 0.05 with a round of 3 digits
    """
    @staticmethod
    def generateFamiliarityBonuses(party):
        visited = []
        for char in party:
            if char is None:
                continue
            for partner_char in party:
                if partner_char is None:
                    continue
                if char == partner_char:
                    continue
                if (char, partner_char) in visited or (partner_char, char) in visited:
                    continue
                visited.append((char, partner_char))
                bonus = round(random.uniform(0.01, 0.05), 3)
                # print("Add between ", char.get_id(), partner_char.get_id(), bonus)
                char.add_familiarity(partner_char.get_id(), bonus)
                partner_char.add_familiarity(char.get_id(), bonus)
