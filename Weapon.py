import json

def wepLoad(filename, weapontitle):
    with open("{0}.json".format(filename)) as file:
        weaponsData = json.load(file)
    try:
        newWeapon = Weapon(weaponsData[weapontitle])
        return newWeapon
    except KeyError:
        print("Weapon does not exist in file")

class Weapon():
    def __init__(self, wepData = "None"):
        if (wepData == "none"):
            self.name = "Nothing I guess"
            self.range = 1
            self.aim = 0
            self.damage = 0
        else:
            self.name = wepData["name"]
            self.range = wepData["range"]
            self.aim = wepData["aim"]
            self.damage = wepData["damage"]

# class Fists(Weapon):
#     def __init__(self):
#         self.name = "Just your fists"
#         self.range = 1
#         self.aim = 10
#         self.damage = 1
#         
# class Sword1(Weapon):
#     def __init__(self):
#         self.name = "Shortsword"
#         self.range = 1
#         self.aim = 6
#         self.damage = 5
#         
# class Sword2(Weapon):
#     def __init__(self):
#         self.name = "Serrated Blade"
#         self.range = 1
#         self.aim = 6
#         self.damage = 8
#         
# class Rifle1(Weapon):
#     def __init__(self):
#         self.name = "Bolt-Action Rifle"
#         self.range = 20
#         self.aim = 2
#         self.damage = 20