from Entities.Entity import *

class Character(Entity):
    def __init__(self, name, health, damage, defense, image):
        super().__init__(name, health, damage, defense)
        self.image = image

    def getcharacter(self):
        return self.name

    def getname(self):
        return self.name

    def getimage(self):
        return self.image
