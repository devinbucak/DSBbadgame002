import random
from Monster import Monster, Spooder, Shambler
from Player import Player
import Weapon
import Room
from GamWin import GamWin
import json

def gameStart(player, gameDisplay):
    
    roomList = Room.roomsLoad("rooms")
    
    giveWeapon(player, Weapon.wepLoad("weapons", "Fists"))
    giveWeapon(player, Weapon.wepLoad("weapons", "Sword2"))
    
    currentRoom = roomList[0]
    while True:
        #print("CURRENT ROOM :", currentRoom)
        nextRoomName = roomEncounter(player, currentRoom, roomList)
        #print("nextRoomName :", nextRoomName)
        for newRoom in roomList:
            #print("newRoom.name :", newRoom.name)
            if newRoom.name == nextRoomName:
                currentRoom = newRoom
        
    
def roomEncounter(player, room, roomList):
    if len(room.monsterList) > 0:
        newCombat = CombatEncounter(player, room.monsterList)
        newCombat.combatLoop()
    
    collectItems(player, room)
    
    roomChoices = []
    for otherRoom in room.connections:
        roomChoices.append(otherRoom)
    choice = chooser("Pick a room to enter", roomChoices, player)
    #print("CHOSEN ROOM:", room.connections[choice - 1])
    return (room.connections[choice - 1]) #returns the name of the room chosen to enter next

def collectItems(player, room):
    items = room.itemNames
    #print(items)
    if "hpCharge" in items:
        player.hpCharges += items["hpCharge"]
        print("You collected {0} health charges.".format(items["hpCharge"]))
    if "weapon" in items:
       giveWeapon(player, Weapon.wepLoad("weapons", items["weapon"]))
       print("You collected a new weapon")
    room.itemNames.clear()
    
def waitForInput():
    wait = input()
    return True

def chooser(choiceName, choiceList, player):
    print(choiceName)
    if len(choiceList) < 1:
        print("Nothing to pick")
        return -1
    i = 1
    while True:
        for choice in choiceList:
            print("{0}: {1}".format(i, choiceList[i - 1]))
            i += 1
        choice = int(playerInput(len(choiceList), player))
        if choice > 0:
            return choice
        else:
            i = 1
            
def giveWeapon(player, weapon):
    player.weaponList.append(weapon)
        
#returns an integer from 1 to choiceCount, which the user chooses
def playerInput(choiceCount, player):
    while True:
        try:
            choice = input()
            if choice.lower() == "skills":
                player.printStats()
                return -1
            if choice.lower() == "heal":
                player.playerHeal()
            elif int(choice) > 0 and int(choice) <= choiceCount:
                return choice
            else:
                print("Input Invalid")
        except ValueError:
            print("Input Invalid. Or I don't know how to code. One of the two.")
            
            
class CombatEncounter():
    def __init__(self, player, monsterList):
        self.player = player
        self.monsterList = monsterList
        
    def combatLoop(self):
        allDead = True
        for monst in self.monsterList:
            if monst.life == True:
                allDead = False
        #Attack Loop
        while allDead == False:
            allDead = True
            i = 1
            monsterChoices = []
            #print(self.monsterList)
            for monst in self.monsterList:
                if monst.life == True:
                    monsterChoices.append("{0} ({1} HP)".format(monst.name, monst.health))
            choice = chooser("Choose monster to fight", monsterChoices, self.player)
            print()
            #Calls indivual monster fight
            self.fightMonster(self.monsterList[choice - 1], self.player)
            if self.monsterList[choice - 1].life == False:
                self.monsterList.pop(choice - 1)
            
            for monst in self.monsterList:
                if monst.life == True:
                    allDead = False
        print("You are victorious.\n")
            
    def fightMonster(self, monst, player):
        if monst.life == False:
            print("You have already defeated this monster.")
        while monst.life == True and player.life == True:
            result = self.getPlayerAttack(monst, player)
            if result == "victory":
                monst.kill()
            elif result == "retreat":
                print(":(")
                return False
        print("You killed the {0}\n".format(monst.name))
        return True
        
    def getPlayerAttack(self, monster, player):
        attackComplete = False
        chosenWep = player.getActiveWep()
        #player attack loop (I know I'm bad at naming things)
        while attackComplete == False:
            playerOptions1 = ["Choose Weapon", "Attack Monster", "Retreat"]
            choice = int(chooser("", playerOptions1, player))
            if choice == 1:
                chosenWep = self.pickWeapon(player) 
            elif choice == 3:
                print("I guess you can leave...")
                return "retreat"
            else: #Player attacks
                check = self.playerAttackCheck(monster, player, chosenWep)
                if check:
                    monster.health -= chosenWep.damage
                    print("You managed to hit with your {0}.".format(chosenWep.name))
                    if monster.health <= 0:
                        print("{0} has been killed.".format(monster.name))
                        attackComplete = True
                    else: #Monster is not yet dead
                        print("{0} still has {1} health.".format(monster.name, monster.health))
                        waitForInput()
                        self.monsterAttack(monster, player)
                else:
                    print("You failed to hit the monster. D:")
                    waitForInput()
                    self.monsterAttack(monster, player)
                
        return "victory"
    
    def pickWeapon(self, player):
        wepOptions = []
        for wep in player.weaponList:
            #print(wep)
            wepOptions.append(wep.name)
        choice = int(chooser("", wepOptions, player))
        if choice == -1:
            chosenWep = Weapon()
        else:
            player.setActiveWep(choice - 1)
            chosenWep = player.getActiveWep()
        print("You are attacking with the {0}.\n  Range:{1} Aim:{2} Damage:{3}".format(chosenWep.name, chosenWep.range, chosenWep.aim, chosenWep.damage))
        return chosenWep
    
    def monsterAttack(self, monster, player):
        print("The {0} makes it's move.".format(monster.name))
        intent = monster.getIntent(player)
        playerAlive = True
        if intent == "attack":
            if self.monsterAttackCheck(monster, player):
                playerAlive = player.playerHurt(monster.damage)
                #print("debug   playerAlive:", playerAlive)
                
        if playerAlive == False:
            death()
                
    
    def monsterAttackCheck(self, monster, player):
        monsterTotal = monsterRoll(monster.attack)
        playerTotal = skillRoll(player.spd)
        if playerTotal <= monsterTotal:
            print("{0}'s attack total of {1} beats your speed roll of {2}".format(monster.name, monsterTotal, playerTotal))
            return True
        else:
            print("{0}'s attack total of {1} is less than your speed roll of {2}".format(monster.name, monsterTotal, playerTotal))
            return False
            
    #checks player's dexterity plus weapon aim against monster's dodge
    def playerAttackCheck(self, monster, player, weapon):
        playerTotal = weapon.aim + skillRoll(player.dex)
        if playerTotal >= monster.dodge:
            print("Your total of {0} beats {1}'s speed of {2}".format(playerTotal, monster.name, monster.dodge))
            return True
        else:
            print("Your total of {0} is less than {1}'s speed of {2}".format(playerTotal, monster.name, monster.dodge))
            return False
        


#I'm just making a worse Disco Elysium I suppose
def skillRoll(skillVal):
    roll1 = random.randint(1, 6)
    roll2 = random.randint(1, 6)
    print("You rolled {0} and {1}".format(roll1, roll2), end="\n")
    return skillVal + roll1 + roll2

def monsterRoll(skillVal):
    roll = random.randint(1, 6)
    print("The enemy rolled a {0}".format(roll), end="\n")
    return skillVal + roll

def death():
    print("You have been murdered. Wah")
    exit(0)
    
    
thePlayer = Player()
gameDisplay = GamWin()
gameStart(thePlayer, gameDisplay)