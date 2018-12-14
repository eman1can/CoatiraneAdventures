class Entity:
    def __init__(self, name, health, damage, defense):
        self.name = name
        self.health = health
        self.damage = damage
        self.defense = defense

    def getname(self):
        return self.name


class Character(Entity):
    def __init__(self, name, health, damage, defense, image):
        Entity.__init__(self, name, health, damage, defense)
        self.image = image

    def getcharacter(self):
        return Entity.GetName() + self.image


x = Entity("Hell Hound", 40, 20, 20)
y = Character("Ais Wallenstein", 400, 200, 200, "Bell")

print(x.GetName())
print(y.GetCharacter())
