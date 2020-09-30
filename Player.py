from Weapon import *

class Player():
    def __init__(self):
        global PLAYERDEAD
        PLAYERDEAD = False
        self.life = True
        self.maxHealth = 20
        self.health = 20
        self.hpCharges = 1
        self.weaponList = []
        self.activeWep = 0
        
        #STATS
        self.spe = 5
        self.dex = 5
        self.spd = 5
        self.psi = 0
        
    def printStats(self):
        print("")
        print("Speech: {0}\nDexterity: {1}\nSpeed: {2}\nPsionics: {3}\n".format(self.spe, self.dex, self.spd, self.psi))
        
    def giveWeapon(self, weapon):
        self.weaponList.append(weapon)
        
    def getActiveWep(self):
        return self.weaponList[self.activeWep]
    
    def setActiveWep(self, newActive):
        try:
            traysh = self.weaponList[newActive]
            self.activeWep = newActive
        except:
            print("Weapon not available")
        
    def playerHeal(self):
        if self.hpCharges > 0:
            self.hpCharges -= 1
            self.health += 5
            if self.health > self.maxHealth:
                self.health = self.maxHealth
            print("You healed to {0} health".format(self.health))
        else:
            print("No health charges left")
        
    def playerHurt(self, damage):
        self.health -= damage
        print("You take {0} damage".format(damage))
        return self.checkHealth()
    
    #returns True when player is alive, but false otherwise. Also kills the player.
    def checkHealth(self):
        if self.health <= 0:
            self.kill()
            return False
        else:
            return True
        
    def kill(self):
        PLAYERDEAD = True
        
        
        