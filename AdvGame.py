import random as rn
import numpy as np
import sys

class color:
    purple = '\033[95m'
    cyan = '\033[96m'
    darkcyan = '\033[36m'
    blue = '\033[94m'
    green = '\033[92m'
    yellow = '\033[93m' 
    red = '\033[91m'
    bold = '\033[1m'
    underline = '\033[4m'
    end = '\033[0m'


helpText = \
f'''This game about discovering dungeons. Commands that you can use in the command line:
{color.purple}left, right, up, down{color.yellow} ->{color.cyan} to move{color.end}
{color.purple}pos{color.yellow} ->{color.cyan} your position{color.end}
{color.purple}stats{color.yellow} ->{color.cyan} self info{color.end}
{color.purple}comm{color.yellow} ->{color.cyan} all commands{color.end}
{color.purple}map{color.yellow} ->{color.cyan} map{color.end} ({color.green}X{color.end} - {color.cyan}you{color.end}, {color.red}*{color.end} - {color.cyan}undiscovered rooms{color.end}, {color.blue}о{color.end} - {color.cyan}discovered rooms{color.end})
--------------------------Special commands---------------------------
{color.purple}attack(a){color.yellow} ->{color.cyan} attack the enemy
{color.purple}run(r){color.yellow} ->{color.cyan} run from the enemy into a random room
{color.purple}yes(y){color.yellow} ->{color.cyan} agree.{color.purple} no(n){color.yellow} ->{color.cyan} deny{color.end}
=====================================================================
{color.green}Goal{color.end} - go deep in dungeon as much as possible'''

commText = \
    f'''---------------------------Common commands---------------------------:
{color.purple}left, right, up, down{color.yellow} ->{color.cyan} to move{color.end}
{color.purple}pos{color.yellow} ->{color.cyan} your position{color.end}
{color.purple}stats{color.yellow} ->{color.cyan} self info{color.end}
{color.purple}comm{color.yellow} ->{color.cyan} all commands{color.end}
{color.purple}map{color.yellow} ->{color.cyan} map{color.end} ({color.green}X{color.end} - {color.cyan}you{color.end}, {color.red}*{color.end} - {color.cyan}undiscovered rooms{color.end}, {color.blue}о{color.end} - {color.cyan}discovered rooms{color.end})
--------------------------Special commands---------------------------
{color.purple}attack(a){color.yellow} ->{color.cyan} attack the enemy
{color.purple}run(r){color.yellow} ->{color.cyan} run from the enemy into a random room
{color.purple}yes(y){color.yellow} ->{color.cyan} agree.{color.purple} no(n){color.yellow} ->{color.cyan} deny{color.end}'''







class Enemy():
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack
        self.alive = True

    def attackPlayer(self):
        print(f"{color.purple}Player: {Game.health} hp.{color.green}     {self.name}: {self.health} hp.{color.end}")
        if(self.attack > Game.armor):
            Game.health -= self.attack - Game.armor
        if(Game.health <= 0):
            Game.alive = False
            return
    
    def TakeDamage(self):
        print(f"{color.green}Player: {Game.health} hp.{color.purple}     {self.name}: {self.health} hp.{color.end}")
        self.health -= Game.attack
        if(self.health <= 0):
            self.alive = False
            return

class Room():
    rooms = {
        'enemy' : 30,
        'heal' : 5,
        'weapon' : 20,
        'armor' : 15,
        'potion' : 20,
        'empty' : 10
    }
    def __init__(self, posX, posY):
        self.posX = posX
        self.posY = posY
        self.info = None

    def setEmpty(self):
        self.info = 'empty'

    def spawnRoom(self, type='Rand'):
        if(type == 'Rand'):
            self.info = Game.randItem(Room.rooms, 0)
        else:
            self.info = type


class Game():
    rooms = []
    roomsTypes = {}
    roomsItems = {}
    discoveredRooms = 0
    stagesCompleted = 0
    enemies = {
    'a Rat' : (5, 1, 35),
    'a Goblin' : (15, 5, 25),
    'a Skeleton' : (10, 7, 20),
    'an Orc' : (30, 10, 15),
    'empty' : (0, 0, 5)
    }
    weapons = {
        'fists' : (1, 0),
        'a wooden sword' : (3, 25),
        'a metal sword' : (5, 15),
        'a stick' : (2, 50),
        'a crossbow' : (6, 10)
    }
    armors = {
        'a wooden shield' : (1, 25, 0),
        'a metal shield' : (3, 10, 0),
        'a leather armor' : (1, 35, 1),
        'a mail' : (2, 20, 1),
        'a metal armor' : (3, 10, 1)
    }
    
    #---------stats---------#
    health = 100
    alive = True
    attack = 1
    armor = 0

    def __init__(self, width='none', height='none', posX='none', posY='none'):
        self.width = width
        self.height = height
        if((width == 'none' and height == 'none') or (width == 'n' and height == 'n')):
            while(True):
                if(type(self.width) == int and type(self.height) == int and (self.width != 1 or self.height != 1)):
                    break
                if(type(posX) == int and type(posY) == int):
                    self.width = rn.randint(posX, 18)
                    self.height = rn.randint(posY, 18)
                elif(type(posX) == int and type(posY) != int):
                    self.width = rn.randint(posX, 18)
                    self.height = rn.randint(1, 18)
                elif(type(posX) != int and type(posY) == int):
                    self.width = rn.randint(1, 18)
                    self.height = rn.randint(posY, 18)
                else:
                    self.width = rn.randint(1, 18)
                    self.height = rn.randint(1, 18)
        elif((width != 'none' and height == 'none') or (width != 'n' and height == 'n')):
            while(True):
                if(type(self.height) == int and (self.width != 1 or self.height != 1)):
                    break
                if(type(posY) == int):
                    self.height = rn.randint(posY, 18)
                else:
                    self.height = rn.randint(1, 18)
        elif((width == 'none' and height != 'none') or (width == 'n' and height != 'n')):
            while(True):
                if(type(self.width) == int and (self.width != 1 or self.height != 1)):
                    break
                if(type(posX) == int):
                    self.width = rn.randint(posX, 18)
                else:
                    self.width = rn.randint(1, 18)

        if((posX == 'none' and posY == 'none') or (posX == 'n' and posY == 'n')):
            self.posX = rn.randint(1, self.width)
            self.posY = rn.randint(1, self.height)
        elif((posX != 'none' and posY == 'none') or (posX != 'n' and posY == 'n')):
            self.posX = posX
            self.posY = rn.randint(1, self.height)
        elif((posX == 'none' and posY != 'none') or (posX == 'n' and posY != 'n')):
            self.posX = rn.randint(1, self.width)
            self.posY = posY
        else:
            self.posX = posX
            self.posY = posY

        print(helpText)

        print(f'{color.end}' + '-' * 69)
        print(f'{color.blue}Generated map size{color.purple} {self.width, self.height}.{color.green} Player pos -{color.purple} {self.getPos()}{color.end}')
        print('-' * 69)

        self.weapon = 'fists'
        self.armor = None
        self.shield = None

        self.createRoom('empty')
        self.createExit()
        self.createMap()

    @staticmethod
    def randItem(dict, whereIschance):
        rand = rn.randint(1,100)
        lastChance = 0
        chances = 0

        for item in dict:
            if(type(dict.get(item)) == tuple):
                chances += dict.get(item)[whereIschance]
            else:
                chances += dict.get(item)

        if(chances != 100):
            print(f"{color.yellow}Warning! Sum of the all chances isn't equal 100!{color.end}")

        for item in dict:
            if(type(dict.get(item)) == tuple):
                chance = dict.get(item)[whereIschance]
            else:
                chance = dict.get(item)

            if(lastChance < rand <= lastChance + chance):
                return item
            lastChance += chance

    def gameOver(self):
        print(f"{color.red}You've lost!\n{color.cyan}You've discovered {Game.discoveredRooms} rooms{color.end} \
and{color.blue} completed {Game.stagesCompleted} stages.\n{color.purple}Your score: {Game.discoveredRooms * 5 * (Game.stagesCompleted + 1)} {color.end}")
        sys.exit()
    
    def checkUserAnswer(self, text):
        userAnsw = input(text).lower()
        if(userAnsw == 'yes' or userAnsw == 'y'):
            return True
        elif(userAnsw == 'n' or userAnsw == 'no'):
            return False
        elif(userAnsw == 'stats'):
            self.command(userAnsw)
            return self.checkUserAnswer(text)
        else:
            print(f"{color.red}Wrong command!{color.end}")
            self.checkUserAnswer(text)

    def createExit(self):
        exitPos = (rn.randint(1, self.width), rn.randint(1, self.height))
        while(True):
            if(exitPos != self.getPos()):
                break
            exitPos = (rn.randint(1, self.width), rn.randint(1, self.height))
        Game.rooms.append([exitPos])
        Game.roomsTypes[exitPos] = 'exit'
    
    def enterExit(self):
        print(f"{color.darkcyan}You've entered in{color.purple} exit{color.cyan} room{color.end}")
        if(self.checkUserAnswer(f'{color.cyan}Will you enter the next level?{color.yellow} ->{color.green} ')):
            Game.stagesCompleted += 1
            Game.rooms.clear()
            Game.roomsTypes.clear()

            self.createRoom('empty')
            self.createExit()
            self.createMap()
            Game.stagesCompleted += 1
        else:
            return
   # Rooms
    def isHereARoom(self):
        if([(self.posX, self.posY)] in Game.rooms):
            return True
        else:
            False

    def createRoom(self, type='Rand'):
        if(self.isHereARoom()):
            if(Game.roomsTypes.get(self.getPos()) == 'exit'):
                Game.discoveredRooms += 1
                self.enterExit()
            return
        Game.discoveredRooms += 1
        Game.roomsTypes[self.getPos()] = Room(self.posX, self.posY)
        Game.roomsTypes.get(self.getPos()).spawnRoom(type)
        Game.rooms.append([self.getPos()])

    def enterRoom(self):
        room = Game.roomsTypes.get(self.getPos())
        roomItem = Game.roomsItems.get(room, None)
        print(f"{color.darkcyan}You've entered in{color.purple} {room.info}{color.cyan} room{color.end}")
        if(room.info == 'enemy'):
            if(roomItem == None):
                enemy = self.randItem(Game.enemies, 2)
                if(enemy == 'empty'):
                    print(f"{color.green}The room was empty{color.end}")
                    return
            else:
                enemy = roomItem
            print(f"There is {enemy} in the room. (Health - {Game.enemies.get(enemy)[0]}, attack: {Game.enemies.get(enemy)[1]})")
            spawnedEnemy = Enemy(enemy, Game.enemies.get(enemy)[0], Game.enemies.get(enemy)[1])
            self.runOrAttack(spawnedEnemy, room)
        elif(room.info == 'heal'):
            print(f'{color.green}You found a heal potion{color.end}')
            if(self.checkUserAnswer(f'{color.cyan}Will you drink it?{color.yellow} ->{color.green} ')):
                heal = rn.randint(1,15)
                Game.health += heal
                print(f"You've restored {heal} hp")
                if(Game.health > 100):
                    Game.health = 100
                room.setEmpty()
        elif(room.info == 'potion'):
            rand = rn.randint(1,30)
            if(self.checkUserAnswer(f"{color.cyan}Will you drink the potion?{color.yellow} ->{color.green} ")):
                if(rn.randint(0,1) == 1):
                    Game.health += rand
                    print(f"{color.green}You've drank the heal potion and restored{color.end} {rand} hp")
                    if(Game.health > 100):
                        Game.health = 100
                else:
                    Game.health -= rand
                    print(f"{color.red}You've drank the poisoned potion and lost{color.end} {rand} hp")
                    if(Game.health <= 0):
                        self.gameOver()
                room.setEmpty()
        elif(room.info == 'weapon'):
            if(roomItem == None):
                weapon = self.randItem(Game.weapons, 1)
            else:
                weapon = roomItem
            print(f"{color.green}You've found {weapon}.{color.red} {Game.weapons.get(weapon)[0]} damage{color.end}")

            if(self.weapon == 'fists'):
                text = f'{color.cyan}Will you take it?{color.yellow} ->{color.green} '
            else:
                text = f'{color.cyan}Will you take{color.green} {weapon}{color.end} instead of{color.purple} {self.weapon}{color.yellow} ->{color.green} '
            
            if(weapon != self.weapon):
                if(self.checkUserAnswer(text)):
                    if(self.weapon == 'fists'):
                        room.setEmpty()
                        self.weapon = weapon
                        Game.attack = Game.weapons.get(weapon)[0]    

                    Game.roomsItems[room] = self.weapon
                    self.weapon = weapon
                    Game.attack = Game.weapons.get(weapon)[0]
                else:
                    Game.roomsItems[room] = weapon
        elif(room.info == 'armor'):
            armor = None
            shield = None
            if(roomItem == None):
                item = self.randItem(Game.armors, 1)
                if(Game.armors.get(item)[2] == 1):
                    armor = item
                else:
                    shield = item
            else:
                if((room, 'armor') in Game.roomsItems):
                    armor = roomItem
                else:
                    shield = roomItem

            if(shield == None):
                print(f"{color.green}You've found {armor}.{color.blue} {Game.armors.get(armor)[0]} defense{color.end}")
                if(self.armor == None):
                    text = f'{color.cyan}Will you take it?{color.yellow} ->{color.green} '
                else:
                    text = f'{color.cyan}Will you take{color.green} {armor}{color.end} instead of{color.purple} {self.armor}{color.yellow} ->{color.green} '
                
                if(armor != self.armor):
                    if(self.checkUserAnswer(text)):
                        if(self.armor == None):
                            Game.armor += Game.armors.get(armor)[0]
                            room.setEmpty()
                        else:
                            Game.armor += Game.armors.get(armor)[0] - Game.armors.get(self.armor)[0]
                            Game.roomsItems[(room, 'armor')] = self.armor
                        self.armor = armor
                    else:
                        Game.roomsItems[(room, 'armor')] = armor
            else:
                print(f"{color.green}You've found {shield}.{color.blue} {Game.armors.get(shield)[0]} defense{color.end}")
                if(self.shield == None):
                    text = f'{color.cyan}Will you take it?{color.yellow} ->{color.green} '
                else:
                    text = f'{color.cyan}Will you take {color.green}{shield}{color.end} instead of{color.purple} {self.shield} {color.yellow}->{color.green} '
                
                if(shield != self.shield):
                    if(self.checkUserAnswer(text)):
                        if(self.shield == None):
                            Game.armor += Game.armors.get(shield)[0]
                            room.setEmpty()
                        else:
                            Game.armor += Game.armors.get(shield)[0] - Game.armors.get(self.shield)[0]
                            Game.roomsItems[room] = self.shield
                        self.shield = shield
                    else:
                        Game.roomsItems[room] = shield

    # Fight
    def runOrAttack(self, spawnedEnemy, room):
        userInput = input(f'{color.cyan}Attack/Run (a/r){color.yellow} ->{color.green} ').lower()
        if(userInput == 'attack' or userInput == 'a'):
            self.fight(spawnedEnemy, True)
        elif(userInput == 'run' or userInput == 'r'):
            rand = rn.randint(1,100)
            if(rand <= 30):
                print(f"{color.green}You've succesfully ran{color.end}")
                self.command(rn.choice(self.whereCanGo()))
                Game.roomsItems[room] = spawnedEnemy.name
            else:
                print(f"{color.red}You haven't escaped{color.end}")
                self.fight(spawnedEnemy, False)
        else:
            print(f'{color.red}Wrong command!{color.end}')
            self.runOrAttack(spawnedEnemy, room)
 
    def fight(self, spawnedEnemy, isplayerTurn):
        print('-' * 15 + 'Fight' + '-' * 15)
        skip = False
        while(Game.alive and spawnedEnemy.alive):
            if(skip == False):
                userInp = input(f'{color.cyan}Press "Enter" to continue or type "s" or "skip" to skip{color.yellow} ->{color.end} ')
                if(userInp.lower() == 'skip' or userInp.lower() == 's'):
                    skip = True

            if(isplayerTurn):
                print(f"{color.green}Player's turn:{color.end}")
                spawnedEnemy.TakeDamage()
                isplayerTurn = not isplayerTurn
                print('-' * 40)
            else:
                print(f"{color.purple}Enemy's turn:{color.end}")
                spawnedEnemy.attackPlayer()
                isplayerTurn = not isplayerTurn
                print('-' * 40)
        if(Game.alive == False):
            self.gameOver()
        else:
            print(f"{color.green}You've killed a {color.end} {spawnedEnemy.name}")
        Game.roomsTypes.get(self.getPos()).setEmpty()
    
    # Map
    def createMap(self):
        self.map = np.array([['*'] * self.width] * self.height)
        self.lastPos = self.getPos()
        self.changeMap(False)

    def changeMap(self, placeO=True):
        self.map[self.height - self.posY][self.posX-1] = 'X'
        if(self.map[self.height - self.lastPos[1]][self.lastPos[0]-1] == 'X' and placeO):
            self.map[self.height - self.lastPos[1]][self.lastPos[0]-1] = 'o'
        self.lastPos = self.getPos()

    # Movement
    def getPos(self):
        return (self.posX, self.posY)

    def whereCanGo(self):
        #-----------------------------Left Down Corner-----------------------------#
        if(self.posX == 1 and self.posY == 1 and self.height > 1 and self.width > 1):
            return ['right', 'up']
        elif(self.posX == 1 and self.posY == 1 and self.height > 1 and self.width == 1):
            return ['up']
        elif(self.posX == 1 and self.posY == 1 and self.height == 1 and self.width > 1):
            return ['right']
        #-----------------------------Right Down Corner----------------------------#
        elif(self.posX == self.width and self.posY == 1 and self.height > 1 and self.width > 1):
            return ['left', 'up']
        elif(self.posX == self.width and self.posY == 1 and self.height > 1 and self.width == 1):
            return ['up']
        elif(self.posX == self.width and self.posY == 1 and self.height == 1 and self.width > 1):
            return ['left']
        #-------------------------------Left Up Corner------------------------------#
        elif(self.posX == 1 and self.posY == self.height and self.height > 1 and self.width > 1):          
            return ['right', 'down']
        elif(self.posX == 1 and self.posY == self.height and self.height > 1 and self.width == 1):
            return ['down']
        elif(self.posX == 1 and self.posY == self.height and self.height == 1 and self.width > 1):
            return ['right']
        #-------------------------------Right Up Corner-----------------------------#
        elif(self.posX == self.width and self.posY == self.height and self.height > 1 and self.width > 1):                     # Right Up Corner
            return ['left', 'down']
        elif(self.posX == self.width and self.posY == self.height and self.height > 1 and self.width == 1):                     # Right Up Corner
            return ['down']
        elif(self.posX == self.width and self.posY == self.height and self.height == 1 and self.width > 1):                     # Right Up Corner
            return ['left']
        elif(self.posX == 1 and self.posY > 1 and self.posY < self.height):             # Left Side
            return ['up', 'right', 'down']
        elif(self.posX > 1 and self.posX < self.width and self.posY == self.height):    # Up Side
            return ['left', 'right', 'down']
        elif(self.posX == self.width and self.posY < self.height and self.posY > 1):    # Right Side
            return ['left', 'up', 'down']
        elif(self.posX > 1 and self.posX < self.width and self.posY == 1):              # Down Side
            return ['left', 'right','up' ]
        else:
            return ['left', 'right', 'up', 'down']

    def move(self):
        self.changeMap()
        self.createRoom()
        if(Game.roomsTypes[self.getPos()] != 'exit'):
            self.enterRoom()

    def goLeft(self):
        if('left' in self.whereCanGo()):
            self.posX -= 1
            self.move()
        else:
            print(f"{color.red}You can't go there, there is no any door{color.end}")
    def goRight(self):
        if('right' in self.whereCanGo()):
            self.posX += 1
            self.move()
        else:
            print(f"{color.red}You can't go there, there is no any door{color.end}")
    def goUp(self):
        if('up' in self.whereCanGo()):
            self.posY += 1
            self.move()
        else:
            print(f"{color.red}You can't go there, there is no any door{color.end}")
    def goDown(self):
        if('down' in self.whereCanGo()):
            self.posY -= 1
            self.move()
        else:
            print(f"{color.red}You can't go there, there is no door{color.end}")
    
    def command(self, input):
        if(input == 'left'):
            self.goLeft()
        elif(input == 'right'):
            self.goRight()
        elif(input == 'up'):
            self.goUp()
        elif(input == 'down'):
            self.goDown()
        elif(input == 'pos'):
            self.whereAmI()
        elif(input == 'map'):
            print(self.map)
        elif(input == 'stats'):
            print(f'{color.end}' + '-' * 20 + 'Stats' + '-' * 20)

            if(Game.health == 100):
                spaces = ' ' * 15
            elif(Game.health >= 10):
                spaces = ' ' * 16
            else:
                spaces = ' ' * 17
            
            armorDefense = None
            shieldDefense = None
            if(type(Game.armors.get(self.armor)) != None and armorDefense != self.armor):
                armorDefense = Game.armors.get(self.armor)[0]
            if(type(Game.armors.get(self.shield)) != None and shieldDefense != self.shield):
                shieldDefense = Game.armors.get(self.shield)[0]

            statsText = \
            f'''{color.green}Health: {Game.health}{spaces}{color.yellow}Weapon: {self.weapon} ({Game.attack} damage)
{color.red}Damage: {Game.attack}                 {color.cyan}Armor: {self.armor} ({armorDefense} defense)       
{color.blue}Defense: {Game.armor}                {color.darkcyan}Shield: {self.shield} ({shieldDefense} defense){color.end}'''
            print(statsText)

        elif(input == 'help'):
            print(helpText)
        elif(input == 'comm'):
            print(commText)
        else:
            print(f"{color.red}Wrong command!{color.end}")

    def whereAmI(self):
        print(f"{color.cyan}You are now at{color.purple} {self.getPos()}{color.end}")
  

def setVar(text):
    userInput = input(text).lower()
    if(userInput != 'n' and userInput != 'none'):
        try:
            return int(userInput)
        except ValueError:
            print(f"{color.red}Wrong input!.{color.end}")
            return setVar(text)
    else:
        return userInput

def setMap():
    global width, height
    width = setVar(f'{color.cyan}Input width of the map or{color.purple} "None", "n"{color.cyan} if want to randomize it{color.yellow} ->{color.green} ')
    height = setVar(f'{color.cyan}Input height of the map or{color.purple} "None", "n"{color.cyan} if want to randomize it{color.yellow} ->{color.green} ')
    if(width == 1 and height == 1):
        print(f"{color.red}Map can't be 1x1 size{color.end}")
        setMap()
    if((type(width) == int and width > 18) or (type(height) == int and height > 18)):
        print(f"{color.red}X or Y size of the map can't be more than 18")
        setMap()

def setPlayer():
    global posX, posY
    posX = setVar(f'{color.cyan}Input x pos of spawnpoint or{color.purple} "None", "n"{color.cyan} if want to randomize it{color.yellow} ->{color.green} ')
    posY = setVar(f'{color.cyan}Input y pos of spawnpoint or{color.purple} "None", "n"{color.cyan} if want to randomize it{color.yellow} ->{color.green} ')
    if(type(width) == int and type(height) == int and type(posX) == int and type(posY) == int):
        if(posX > width or posX < 1 or posY > height or posY < 1):
            print(f"{color.red}Player beyond the map, try another value{color.end}")
            setPlayer()
    elif(type(width) == int and type(posX) == int and posX > width):
        print(f"{color.red}Player beyond the map, use X value that lower or equal {width}{color.end}")
        setPlayer()
    elif(type(height) == int and type(posY) == int and posY > height):
        print(f"{color.red}Player beyond the map, use Y value that lower or equal {height}{color.end}")
        setPlayer()
    elif((type(posX) == int and posX > 18) or (type(posY) == int and posY > 18)):
        print(f"{color.red}Player X or Y position can't be more than 18")
        setPlayer()

setMap()
setPlayer()
print(f'{color.end}' + '=' * 69)
game = Game(width, height, posX, posY)
while(True):
    game.command(input(f"{color.cyan}Enter a command{color.yellow} ->{color.green} ").lower())
    print(f'{color.end}' + '=' * 69)