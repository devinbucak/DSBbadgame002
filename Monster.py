from Player import Player

class MonsterAI():
    def __init__(self):
        self.hasAI = False

class Monster():
    def __init__(self):
        self.life = True
        self.name = "basic monster"
        self.health = 1
        self.attack = 0
        self.damage = 0
        self.dodge = 0
        self.intent = 0
        
    def printStats(self):
        print("")
        print("Health: {0}\nDamage: {1}\nSpeed: {2}\n".format(self.health, self.attack, self.dodge))
        
    def getIntent(self, player):
        intention = ""
        if self.intent == 0:
            self.intent += 1
            intention = "attack"
        self.intent = 0
        return intention
    
    def kill(self):
        self.life = False
        
class Knight_Type1(Monster):
    def __init__(self):
        self.life = True
        self.intent = 0
        self.name = "Hwacka Soldier"
        self.health = 30
        self.attack = 10
        self.damage = 10
        self.dodge = 14
        
class Shambler(Monster):
    def __init__(self):
        self.life = True
        self.intent = 0
        self.name = "Shambler"
        self.health = 16
        self.attack = 12
        self.damage = 4
        self.dodge = 12
        
class Spooder(Monster):
    def __init__(self):
        self.life = True
        self.intent = 0
        self.name = "Spooder"
        self.health = 12
        self.attack = 8
        self.damage = 6
        self.dodge = 18
        
def generateMonster(typeName):
    if typeName == "Knight_Type1":
        return Knight_Type1()
    elif typeName == "Shambler":
        return Shambler()
    elif typeName == "Spooder":
        return Spooder()