import json
from Monster import *
from Weapon import *

def roomsLoad(filename):
    with open("{0}.json".format(filename)) as file:
        roomsData = json.load(file)
    roomList = []
    startRoom = Room("startRoom", roomsData["startRoom"])
    roomList.append(startRoom)
    for i in range(1, 100):
        roomID = "room_" + str(i)
        try:
            newRoom = Room(roomID, roomsData[roomID])
            roomList.append(newRoom)
        except KeyError:
            #print("Generated new floor :)")
            return roomList
    return roomList
            

class Room():
    def __init__(self, roomID, roomData):
        self.roomID = roomID
        self.name = roomData["name"]
        self.connections = roomData["connections"]
        self.monsterList = self.monsterAdder(roomData["monsters"])
        self.itemNames = roomData["items"]
        
    def monsterAdder(self, monsterNames):
        monsterList = []
        for name in monsterNames:
            newMonster = generateMonster(name)
            monsterList.append(newMonster)
        return monsterList
        
        
    def printRoomData(self):
        print("{0}:".format(self.roomName))
        print("\tConnections: {0}, Monsters:{1}, Items:{2}".format(self.connections, self.monsterList, self.itemNames))