import random
import re

#BUILD CLASSES
class Player:
    def __init__(self):
        self.name = ""
        self.type = ""
        self.hp = 25
        self.fighting = False
        self.inventory = []
        self.coords = [1, 1]
    
    def pickUp(self, object):
        print("----------------------------------------")
        print(f"You pick up {object.name}.")
        self.inventory.append(object)
    
    def use(self, object, monster=None):
        print("----------------------------------------")
        match object.name:
                case "the sword":
                    if self.fighting:
                        dmg = random.randint(10, 12)
                        monster.hp -= dmg
                        print(f"You swing your sword, dealing {dmg} damage to it.")
                    else:
                        print("You aren't fighting anything.")
                case "the staff":
                    if self.fighting:
                        dmg = random.randint(2, 20)
                        monster.hp -= dmg
                        if dmg <= 7:
                            print(f"You shoot a few sparkles from your staff, doing {dmg} damage to it.")
                        elif dmg <= 14:
                            print(f"You point your staff and shoot a small fireball at it, doing {dmg} damage.")
                        else:
                            print(f"You brandish your staff and summon a giant bolt of lightning, striking it for {dmg} damage.")
                    else:
                        print("You aren't fighting anything.")
                case "a death potion":
                    if self.fighting:
                        monster.hp = 0
                        print(f"You throw the black potion at {monster.species}, and it crumbles to ashes.")
                    else:
                        self.hp = 0
                        print("You drink the black potion and instantly die.")
                    for x in self.inventory:
                        if x.name == "a death potion":
                            self.inventory.remove(x)
                            break
                case "a health potion":
                    self.hp += 5
                    healed = 5
                    if self.hp > 25:
                        healed = 30 - self.hp
                        self.hp = 25
                    print(f"You drink a health potion, healing for {healed} health.")
                    for x in self.inventory:
                        if x.name == "a health potion":
                            self.inventory.remove(x)
                            break

    def goTo(self, direction, room):
        print("----------------------------------------")
        if direction in room.doors:
            match direction:
                case "north":
                    self.coords[1] += 1
                case "south":
                    self.coords[1] -= 1
                case "east":
                    self.coords[0] += 1
                case "west":
                    self.coords[0] -= 1
            print(f"You go through the door to the {direction}.")
        else:
            print("You can't go there.")

class Monster:
    def __init__(self, species):
        self.species = species
        match species: #include article
            case "a small demon":
                self.hp = 10
            case "a demon guard":
                self.hp = 20
            case "a Demon Prince":
                self.hp = 30
            case "the Demon King":
                self.hp = 40

class Room:
    def __init__(self, coords, contents: list, monsters: list, doors: tuple, desc: str):
        self.coords = coords
        self.contents = contents
        self.monsters = monsters
        self.doors = doors
        self.desc = desc

class Loot:
    def __init__(self, name):
        self.name = name #include article

#ENVIRONMENT SETUP
player = Player()
sword = Loot("the sword")
staff = Loot("the staff")
hp1 = Loot("a health potion")
hp2 = Loot("a health potion")
hp3 = Loot("a health potion")
hp4 = Loot("a health potion")
dp1 = Loot("a death potion")
dp2 = Loot("a death potion")
smallDemon1 = Monster("a small demon")
smallDemon2 = Monster("a small demon")
smallDemon3 = Monster("a small demon")
demonGuard1 = Monster("a demon guard")
demonGuard2 = Monster("a demon guard")
demonPrince1 = Monster("a Demon Prince")
demonPrince2 = Monster("a Demon Prince")
demonKing = Monster("the Demon King")
monstersAlive = [smallDemon1, smallDemon2, smallDemon3, demonGuard1, demonGuard2, demonPrince1, demonPrince2, demonKing]
room11 = Room([1, 1], [], [], ("north", "east"), "a small, plain room. It looks like where you started from.")
room21 = Room([2, 1], [sword, hp1], [], ("north", "east", "west"), "a small room with a couple of black marks on the floor.")
room31 = Room([3, 1], [dp2], [smallDemon1], ("north", "west"), "a small room with a number of black streaks across the walls, floor, and ceiling. It's cool in here...")
room12 = Room([1, 2], [staff, hp2], [], ("north", "east", "south"), "a room with a dirty flickering lightbulb.")
room22 = Room([2, 2], [hp3, dp1], [smallDemon2], ("north", "east", "south", "west"), "a room with dark cracks spreading from the corners across the floor and walls. It's rather chilly here.")
room32 = Room([3, 2], [], [demonGuard1], ("north", "south", "west"), "a room with large gashes across the floor and walls, oozing black mist. You feel an evil presence...")
room13 = Room([1, 3], [hp4], [smallDemon3], ("east", "south"), "a large room with several black stains along the walls and floor. It's cool in here...")
room23 = Room([2, 3], [], [demonGuard2], ("east", "south", "west"), "a large room. Black mould creeps along the walls and ceiling, and the floor is half-rotted. You sense an evil presence...")
room33 = Room([3, 3], [], [demonPrince1, demonPrince2, demonKing], ("south", "west"), "a huge room. It's filled with black mist and freezing cold, and you sense a great evil nearby.")
rooms = [room11, room12, room13, room21, room22, room23, room31, room32, room33]

#COMBAT LOOP
def fight(monsterFighting, combatRoom):
    player.fighting = True
    while player.hp > 0 and monsterFighting.hp > 0:
        #fight intro
        print("----------------------------------------")
        print(f"You're fighting {monsterFighting.species}.")
        print(f"You have {player.hp} HP and it has {monsterFighting.hp} HP.")
        inventoryStr = ""
        if player.inventory:
            for x in range(len(player.inventory) - 1):
                inventoryStr += f"{player.inventory[x].name}, "
            inventoryStr += f"and {player.inventory[-1].name}"
            print(f"You have {inventoryStr}")
        #combat action
        validCombat = False
        while validCombat == False:
            action = input("What do you use? ").lower()
            if re.search("^use .*", action):
                objectToUse = action[4:]
                found = False
                for x in player.inventory:
                    if ("the " + objectToUse) == x.name or ("a " + objectToUse) == x.name or objectToUse == x.name:
                        player.use(x, monsterFighting)
                        found = True
                        validCombat = True
                        break
                if found == False:
                    print("You don't have that item.")
            elif re.search("^go .*", action):
                print("Stop running away.")
            elif re.search("^pick up .*", action):
                print("Finish the fight before you pick anything up.")
            elif re.search("^fight .*", action):
                print(f"You're already fighting {monsterFighting.species}, choose something to use.")
            else:
                print("Choose something to use in the fight.")
        #monster action
        if monsterFighting.hp > 0:
            match monsterFighting.species:
                case "a small demon":
                    dmg = random.randint(2, 4)
                    player.hp -= dmg
                    print(f"The small demon bites you, dealing {dmg} damage.")
                case "a demon guard":
                    dmg = random.randint(4, 6)
                    player.hp -= dmg
                    print(f"The demon guard thrusts his spear, hitting you for {dmg} damage.")
                case "a Demon Prince":
                    dmg = random.randint(6, 7)
                    player.hp -= dmg
                    print(f"The Demon Prince casts a curse on you, dealing {dmg} damage.")
                case "the Demon King":
                    dmg = random.randint(7, 8)
                    player.hp -= dmg
                    print(f"The Demon King strikes you with black magic, dealing {dmg} damage.")
    #fight result
    if player.hp <= 0:
        print(f"You got beaten up by {monsterFighting.species} and died.")
    else:
        print(f"You defeated {monsterFighting.species}.")
        combatRoom.monsters.remove(monsterFighting)
        monstersAlive.remove(monsterFighting)
        player.fighting = False

#GAME START
print("You find yourself in a dark room with no memory of how you got there. There is a torch at your feet.")
print("(Use simple commands like 'pick up torch' or 'go south'.)")
torch = Loot("the torch")
while True:
    action = input().lower()
    if action == "pick up torch":
        player.pickUp(torch)
        break
    else:
        print("You get scared of the dark and pee your pants.")

print("There is a door to the north and a door to the east.")
while True:
    action = input().lower()
    if re.search("^go .*", action):
        print("----------------------------------------")
        direction = action[3:]
        match direction:
            case "north":
                player.coords[1] += 1
                print("You go through the door to the north.")
                break
            case "east":
                player.coords[0] += 1
                print("You go through the door to the east.")
                break
            case _:
                print("You can't go there.")
    else:
        print("----------------------------------------")
        print("Pick a direction to go.")

#MAIN BODY
while True:
    #describe room
    for x in rooms:
        if player.coords == x.coords:
            currRoom = x
            break
    print(f"You find yourself in {currRoom.desc}")
    
    #show contents
    if currRoom.contents:
        currRoomContents = ""
        if len(currRoom.contents) > 1:
            for x in range(len(currRoom.contents) - 1):
                currRoomContents += f"{currRoom.contents[x].name}, "
            currRoomContents += f"and {currRoom.contents[-1].name}"
        else:
            currRoomContents = currRoom.contents[0].name
        
        daRandNum = random.randint(1, 5)
        match daRandNum:
            case 1:
                print("In the room you see " + currRoomContents + ".")
            case 2:
                print("You notice " + currRoomContents + ".")
            case 3:
                print("There's " + currRoomContents + " nearby.")
            case 4:
                print("You spot " + currRoomContents + ".")
            case 5:
                print("You find " + currRoomContents + ".")
    
    #show monsters
    if currRoom.monsters:
        currRoomMonsters = ""
        if len(currRoom.monsters) > 1:
            for x in range(len(currRoom.monsters) - 1):
                currRoomMonsters += f"{currRoom.monsters[x].species}, "
            currRoomMonsters += f"and {currRoom.monsters[-1].species}"
        else:
            currRoomMonsters = currRoom.monsters[0].species

        daRandNum = random.randint(1, 3)
        match daRandNum:
            case 1:
                print("You can't help but notice that there's " + currRoomMonsters + " here too.")
            case 2:
                print("Unfortunately, you also spot " + currRoomMonsters + ".")
            case 3:
                print("You also notice " + currRoomMonsters + " lurking in a corner.")
    
    #show doors
    currRoomDoors = ""
    for x in range(len(currRoom.doors) - 1):
        currRoomDoors += f"{currRoom.doors[x]}, "
    currRoomDoors += f"and {currRoom.doors[-1]}"
    print("There are doors to the " + currRoomDoors + ".")

    #action loop
    validAction = False
    while validAction == False:
        action = input().lower()
        if re.search("^go .*", action):
            directionToGo = action[3:]
            player.goTo(directionToGo, currRoom)
            validAction = True
        elif re.search("^pick up .*", action):
            objectToPick = action[8:]
            found = False
            for x in currRoom.contents:
                if ("the " + objectToPick) == x.name or ("a " + objectToPick) == x.name or objectToPick == x.name:
                    player.pickUp(x)
                    currRoom.contents.remove(x)
                    found = True
                    validAction = True
                    break
            if found == False:
                print("That doesn't exist here.")
        elif re.search("^use .*", action):
            objectToUse = action[4:]
            found = False
            for x in player.inventory:
                if ("the " + objectToUse) == x.name or ("a " + objectToUse) == x.name or objectToUse == x.name:
                    player.use(x)
                    found = True
                    validAction = True
                    break
            if found == False:
                print("You don't have that item.")
        elif re.search("^fight .*", action):
            monsterToFight = action[6:]
            found = False
            for x in currRoom.monsters:
                if ("the " + monsterToFight) == x.species.lower() or ("a " + monsterToFight) == x.species.lower() or monsterToFight == x.species.lower():
                    fight(x, currRoom)
                    found = True
                    validAction = True
                    break
            if found == False:
                print("There's nothing like that to fight here.")
        else:
            print("Go somewhere, pick up something, use something, or fight something.")
    
    #game end check
    if player.hp <= 0:
        break
    if len(monstersAlive) == 0:
        print("You killed all the demons!")
        break

#OUTRO MUSIC
print("--GAME END--")
input("Press Enter to exit.")