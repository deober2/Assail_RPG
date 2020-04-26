#Collection of objects for the Assail game
import arcade 
import random 
import os
import time

#Texture IDs and paths:
assailPath = os.getcwd()[0:-11]
resources = assailPath + 'resources/'
print(assailPath)
WATER = 0
TREE = 1
GRASS = 2
ROCK = 3
DIRT = 4
WATER_TEXTURE = arcade.load_texture(assailPath + "resources/WaterBackground.png")
TREE_TEXTURE = arcade.load_texture(assailPath + "resources/TreeBackground.png")
GRASS_TEXTURE = arcade.load_texture(assailPath + "resources/GrassBackground.png")
ROCK_TEXTURE = arcade.load_texture(assailPath + "resources/RockBackground.png")
DIRT_TEXTURE = arcade.load_texture(assailPath + "resources/DirtBackground.png")
KNIGHT_TEXTURE = arcade.load_texture(assailPath + "resources/knight.png")
MAGE_TEXTURE = arcade.load_texture(resources + 'mage.png')
FIRE = arcade.load_texture(resources + 'fire.png')
FORWARD_SLASH = arcade.load_texture(resources + 'forward_slash.png')
BACK_SLASH = arcade.load_texture(resources + 'back_slash.png')
VERTICAL_SHOT = arcade.load_texture(resources + 'shot_vertical.png')
HORIZONTAL_SHOT = arcade.load_texture(resources + 'shot_horizontal.png')
FIRE_COLUMN_1 = arcade.load_texture(resources + 'fire_column_1.png')
FIRE_COLUMN_2 = arcade.load_texture(resources + 'fire_column_2.png')
SELECT_BOX_WHITE = arcade.load_texture(resources + 'select_box_white.png')
BONES = arcade.load_texture(resources + 'bones.png')

#Constants
SCALE = 1
GRID_PIXEL = 48 * SCALE
XGRID = 25
YGRID = 14
XSCREEN = XGRID * GRID_PIXEL
YSCREEN = YGRID * GRID_PIXEL
GRID_AREA = YGRID * XGRID 

 
 
#Movement dictionary to get movement vectors
userInput = ['l', 'r', 'u', 'd']
moveVec = [[0,-1], [0,1], [1,0], [-1,0]]
moveDict = dict(zip(userInput, moveVec))
del userInput; del moveVec


#Archetype attack patterns 
attackNames = ['melee', 'mageBlast', 'arrow']
patterns = [ [[1,0]],    [[3,0],[3,0],[2,0],[4,0],[3,-1],[3,1]],   [[2,0],[1,0],[3,0]]   ]
damages = [ 7, 3, 6 ]
animationNames = ['melee', 'mageBlast', 'arrowVert', 'arrowHoriz']
animations = [ [FORWARD_SLASH, BACK_SLASH], [FIRE_COLUMN_1, FIRE_COLUMN_2], [VERTICAL_SHOT], [HORIZONTAL_SHOT]   ]
attackPatternDict = dict(zip(attackNames, patterns))
attackAminationDict = dict(zip(animationNames, animations))
attackDamageDict = dict(zip(attackNames, damages))
del attackNames; del patterns; del animations; del animationNames; del damages




#Game function definitions
def random_name():
    name = ''
    firstLetter = True
    consonants = 'bcdfghjklmnpqrstvwxz'
    commonConsonants = 'tnsrhldcfp'
    vowels = 'aeiouy'
    nameLength = random.randint(2,7)
    for i in range(nameLength):
        if firstLetter == True:
            
            if random.random() > .3:
                if random.random() > .4:
                    name += random.choice(commonConsonants)
                else:
                    name += random.choice(consonants)
            else:
                name += random.choice(vowels)
            firstLetter = False
        

        else:
            if name[-1] in consonants:
                if random.random() > 0.9:
                    if random.random() > .35:
                        name += '\''
                    elif random.random() > .3:
                        name += random.choice(commonConsonants)
                    else:    
                        name += random.choice(consonants)
                else:
                    name += random.choice(vowels)
            
            elif name[-1] == '\'':
                if random.random() > 0.2:
                    if random.random() > 0.5:
                        name += random.choice(commonConsonants)
                    else:
                        name += random.choice(consonants)
                else:
                    name += random.choice(vowels) 
            else:
                if random.random() > 0.4:
                    if random.random() > .50:
                        name += random.choice(commonConsonants)
                    else:
                        name += random.choice(consonants)
                else:
                    name += random.choice(vowels)
    name = name[0].upper() + name[1:]
    return name

        
def mat_mult(A, direction):

    if direction == 'l':
        B = [[0,-1],[1,0]]
    elif direction == 'r':
        B = [[0,1],[-1,0]]
    elif direction == 'd':
        B = [[-1,0],[0,1]]
    else:
        B = [[1,0],[0,1]]

    #Where row vector = [[1,2,3,4...]] and column vector = [[1], [2], [3], [4], [...]]
    newPattern = []
    for i in range(len(A)):
        newPattern.append([0]*len(B[0]))
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                newPattern[i][j] += int(A[i][k]) * int(B[k][j])
                

    return newPattern


def drunk_walk():
    move = random.randint(-1,1)
    direction = random.randint(0,1)
    if direction == 0:
        move = [0, move]
    else:
        move = [move, 0]
    return move


def elementwise_add(list1, list2):
    listSum = [a + b for a, b in zip(list1,list2)]
    return listSum


def check_walkable(battleMap, location):
    terrain = battleMap[location[0]][location[1]]
    if (terrain == GRASS or terrain == DIRT):
        walkable = True
    else:
        walkable = False 
    return walkable


def check_vacancy(occupancy, location):
    if occupancy[location[0]][location[1]] == 0:
        vacant = True
    elif occupancy[location[0]][location[1]] == 1:
        vacant = False
    return vacant


def check_bounds(location):
    if (location[0] >=0 and location[0] < YGRID and location[1] >= 0 and location[1] < XGRID):
        inBounds = True
    else:
        inBounds = False
    return inBounds 


def generate_battle(oldBattleMap=[], buildNewBattleMap=True, baseTexture=0, newTexture=2, percentNewTexture=60):
    #Method to procedurally Generate a battleMap (an mxn grid of integers representing individual tile textures).
    #Can pass an existing battleMap and generate on top of the old map, or generate a completely new map.
    #Arguments:
    #   oldBattleMap (mxn list): existing battleMap that you wish to write on top of. Default is an empty list
    #   buildNewBattleMap (boolean): Whether or not to generate a completely new map. Pair True with empty oldBattleMap, or False with filled oldBattleMap
    #   baseTexture (int, [0-4]): defines the base texture to fill the initial map. Refers to one of the textures defined above
    #   newTexture (int, [0-4]): defines the new texture to draw on top of the existing battle map. Refers to one of the textures defined above
    #   percentNewTexture (int, [1-100]): defines the percentage of the map that newTexture should occupy


    #Build a matrix to represent each gridpoint
    if buildNewBattleMap:
        battleMap = []
        for y in range(YGRID):
            battleMap.append([])
            for x in range(XGRID):
                battleMap[y].append(baseTexture)
    else:
        battleMap = oldBattleMap
        del oldBattleMap


    #Deposit new textures on the base texture 
    location = [random.randint(0,len(battleMap)-1) , random.randint(0,len(battleMap[0])-1) ]
    battleMap[location[0]][location[1]] = newTexture
    newTextureCount = 1

    #Random walk algorithm to generate grid spaces
    while ((100 * newTextureCount / GRID_AREA) < percentNewTexture):
        move = random.randint(-1,1)
        direction = random.randint(0,1)
        if direction == 0:
            move = [0, move]
        else:
            move = [move, 0]
            
        newCoord = [ location[0] + move[0], location[1] + move[1] ]
        try:
            if (newCoord[0] > -1 and newCoord[1] > -1 and newCoord[0] < len(battleMap) and newCoord[1] < len(battleMap[0]) ):
                location = newCoord
                #print(newCoord)
                if (battleMap[location[0]][location[1]] != newTexture):
                    battleMap[location[0]][location[1]] = newTexture
                    newTextureCount += 1
                    #print('generated. percent ' + str(100*newTextureCount/GRID_AREA) + '\n')
        except:
            pass

    return battleMap  
    #Returns battleMap, an mxn list of integers representing different tile textures


def assign_locations(battleMap, players):
    #Assigns positions to each character occupant. Returns an mxn "occupancy" array of 0 (vacant) and 1 (occupied) spaces
    occupancy = []
    teams = []

    #Array of mxn = shape_of(battleMap) to show whether a site is vacant or occupied. 0 = vacant, 1 = occupied
    for y in range(YGRID):
        occupancy.append([])
        for x in range(XGRID):
            occupancy[y].append(0)

    for player in players:
        teams.append( [player] + player.teamMembers )

    #Choose a valid starting location for the player, then deposit teammates around him- only on valid squares
    for team in teams:
        validStart = False
        while (validStart == False):
            [i,j] = [random.randint(0,13), random.randint(0,24)]
            if (battleMap[i][j] == GRASS or battleMap[i][j] == DIRT):
                validStart = True
                location = [i,j]
                player = team[0]
                player.battleMapLocation = location    #assign player location
                occupancy[i][j] = 1
            else:
                validStart = False
        
        #Deposit the rest of the team members
        if (len(team) > 1):
            for i in range(1,len(team)):
                validDeposit = False
                while (validDeposit == False):
                    move = drunk_walk()
                    newLocation = [location[0] + move[0], location[1] + move[1]  ]
                    if check_bounds(newLocation):
                        if (check_vacancy(occupancy, newLocation) and check_walkable(battleMap, newLocation) ):
                            validDeposit = True
                            location = newLocation
                            member = team[i]
                            member.battleMapLocation = location
                            occupancy[location[0]][location[1]] = 1

                        else:
                            validDeposit = False
    return occupancy
                

def randomize_participants(players):
    participants = []
    for player in players:
        participants =  participants + [player] + player.teamMembers
        random.shuffle(participants)
    return participants




#Game Object definitions
class creature:
    #Class representing moveable characters
    def __init__(self, name='noName', archetype='knight', battleMapLocation=[5, 10], team='blue', apMax=4, health=20, armorClass=10, attackName='melee'):
        self.name = name
        self.archetype = archetype
        self.battleMapLocation = battleMapLocation
        self.team = team
        self.apMax = apMax
        self.apCurrent = apMax
        self.health = health
        self.texture = None
        self.armorClass = armorClass
        self.attackName = attackName
        self.living = True
        self.healthMax = None
        self.isPlayer = False
    
    def assign_attributes(self):
        if self.archetype == 'knight':
            self.texture = KNIGHT_TEXTURE
            self.attackName = 'melee'
        elif self.archetype == 'mage':
            self.texture = MAGE_TEXTURE
            self.attackName = 'mageBlast'
        self.attackPattern = attackPatternDict[self.attackName]
        self.armorClass = 5
        self.healthMax = 10
    
    

    def get_value(self):
        value = self.healthMax + self.armorClass + attackDamageDict[self.attackName] * len(attackPatternDict[self.attackName])
        return round(value ** 1.1)


class player(creature):
    def __init__(self, name='noName', archetype='knight', battleMapLocation=[5, 10], team='blue', apMax=4, health=20, teamMembers=[], money=1000 ):
        super().__init__(self)
        self.name = name
        self.archetype = archetype
        self.battleMapLocation = battleMapLocation
        self.team = team
        self.apMax = apMax
        self.apCurrent = apMax
        self.health = 20
        self.texture = None
        self.teamMembers = teamMembers
        self.money = money
        self.attackName = None
        self.attackPattern = None
        self.living = True
        self.healthMax = None
        self.armorClass = None
        self.isPlayer = True


class overlay:
    #Class representing images to be rendered on top of the map and participating creatures. 
    #Intended for animation
    def __init__(self, texture, battleMapLocation, rotation=0):
        self.texture = texture
        self.battleMapLocation = battleMapLocation
        self.rotation = rotation

   
class battle(arcade.View):

    def __init__(self, windowObject, battleMap, occupancy, participants, overlays, activeIndex, firstIter):
        super().__init__()
        self.windowObject = arcade.get_window()
        self.battleMap = battleMap
        self.occupancy = occupancy
        self.participants = participants
        self.overlays = overlays
        self.activeIndex = activeIndex
        self.firstIter = firstIter
        self.skipToRefresh = False
        self.winningTeam = None
    
    def on_show(self):
        #Runs once, when the window is initialized
        arcade.set_background_color(arcade.color.WHITE)
        #print('On show')
        #print(self.activeIndex)

        
    def move_creature(self, creature):
        print('\n%s: %d AP. 1AP moves:{l(left) r(right) u(up) d(down)} 2AP:{a(attack)} e(end turn) c(concede) ' % (creature.name, creature.apCurrent))
        validMoves = ['l', 'r', 'u', 'd', 'a', 'e', 'c']
        validAttack = ['l', 'r', 'u', 'd']
        move = []

        #Filter invalid moves and perform acitons
        while (len(move) != 1 or move not in validMoves):
            move = input('Please enter a single valid move: ').strip().lower()
            if (move == 'a' and creature.apCurrent < 2):
                move = 'attack_not_valid'
        
        if (len(move) == 1 and move in validMoves and creature.apCurrent >0):
            
            if move == 'c':
                for participant in self.participants:
                    if (participant.team != creature.team):
                        self.winningTeam = participant.team
                        self.exit_battle()
                creature.apCurrent = 0

            if move == 'e':
                creature.apCurrent = 0
            elif (move == 'a' and  creature.apCurrent >= 2):
                direction = []
                while (len(direction) != 1 or direction not in validAttack):
                    direction = input('Please enter a valid attack direction: ').strip().lower()
                creature.apCurrent -= 2
                self.attack_procedure( creature, direction)

            else:
                moveVec = moveDict[move]
                newLocation = elementwise_add(creature.battleMapLocation, moveVec)
                if (check_bounds(newLocation) and check_vacancy(self.occupancy, newLocation) and check_walkable(self.battleMap, newLocation)):
                    self.occupancy[creature.battleMapLocation[0]][creature.battleMapLocation[1]] = 0
                    creature.battleMapLocation = newLocation
                    self.occupancy[creature.battleMapLocation[0]][creature.battleMapLocation[1]] = 1
                    creature.apCurrent -= 1
                else:
                    print(creature.battleMapLocation)
                    print('move invalid. Space is off-grid, occuppied or not walkable.')
            

    def attack_procedure(self, creature, direction):
        #print(attackPatternDict[creature.attackName])
        pattern = attackPatternDict[creature.attackName]
        pattern = mat_mult(pattern, direction)
        for i in range(len(pattern)):
            pattern[i] = elementwise_add(pattern[i], creature.battleMapLocation)
        damage = attackDamageDict[creature.attackName]
        animation = attackAminationDict[creature.attackName]
        for i in range(len(self.participants)):
            for j in range(len(pattern)):
                if (self.participants[i].battleMapLocation == pattern[j]):
                    self.participants[i].health -= damage
                    if self.participants[i].health <= 0:
                        self.participants[i].living = False

        for image in animation:
            newOverlay = overlay(texture=image, battleMapLocation=pattern[0])
            self.overlays.append(newOverlay)

                
    def on_draw(self):
        arcade.start_render()
        for i in range(len(self.battleMap)):
        #Draw the battleMap tile background:
            for j in range(len(self.battleMap[0])):
                x = GRID_PIXEL/2 + GRID_PIXEL * j
                y = GRID_PIXEL/2 + GRID_PIXEL * i 
                
                if self.battleMap[i][j] == WATER:
                    texture = WATER_TEXTURE
                elif self.battleMap[i][j] == TREE:
                    texture = TREE_TEXTURE
                elif self.battleMap[i][j] == GRASS:
                    texture = GRASS_TEXTURE
                elif self.battleMap[i][j] == ROCK:
                    texture = ROCK_TEXTURE
                elif self.battleMap[i][j] == DIRT:
                    texture = DIRT_TEXTURE

                arcade.draw_scaled_texture_rectangle(x, y, texture, SCALE, 0)

        #Draw all participating creatures
        if self.participants:
            for participant in self.participants:
                x = GRID_PIXEL/2 + GRID_PIXEL * participant.battleMapLocation[1]
                y = GRID_PIXEL/2 + GRID_PIXEL * participant.battleMapLocation[0]

                arcade.draw_scaled_texture_rectangle(x, y, participant.texture, SCALE, 0)
        
        
        #Draw selection box to show current player
        selectBoxLocation = self.participants[self.activeIndex].battleMapLocation
        x = GRID_PIXEL/2 + GRID_PIXEL * selectBoxLocation[1]
        y = GRID_PIXEL/2 + GRID_PIXEL * selectBoxLocation[0]
        arcade.draw_scaled_texture_rectangle(x, y, SELECT_BOX_WHITE, SCALE, 0)
        
        #Draw all overlay images
        if self.overlays:
            image = self.overlays[0]
            x = GRID_PIXEL/2 + GRID_PIXEL * image.battleMapLocation[1]
            y = GRID_PIXEL/2 + GRID_PIXEL * image.battleMapLocation[0]
            arcade.draw_scaled_texture_rectangle(x, y, image.texture, SCALE, image.rotation)
            del self.overlays[0]
            self.skipToRefresh = True


    def exit_battle(self):
        #method to close the battle window
        loot = 0
        livingParticipants = []
        for i in range(len(self.participants)):
            if self.participants[i] == False:
                loot += self.participants[i].get_value()
                print('%s is Dead!' % self.participants[i].name)
            else:
                livingParticipants.append(self.participants[i])
        self.participants = livingParticipants
            

        
        for character in self.participants:
            print('character and player types are:',end=''); print(type(character),end='');print(type(player))
            if (character.isPlayer and (character.team == self.winningTeam)):
                character.money += loot
                print('%s has earned %d gold' % (character.name, loot))
                arcade.close_window()
            else:
                print('There was an error in deciding the victor')


    def check_victory(self):
        teamTally = []
        for creature in self.participants:
            if (creature.living == True):
                teamTally.append(creature.team)
            print(teamTally)
        if ( all(ele == teamTally[0] for ele in teamTally)):
            self.winningTeam = teamTally[0]
            print('winning team is:', end=''); print(self.winningTeam)
            self.exit_battle()
        


    def on_update(self, delta_time=0.1):
        #Main loop of the battle program. This is where all creature turns take place
        activeParticipant = self.participants[self.activeIndex]
        
        #closeWindow = input('Close Window?: ').strip().lower()
        #if (closeWindow == 'y' or closeWindow == 'yes'):
        #    self.windowObject.close_window()

        #if the active player is out of action points and they are the last player in the full turn,
        #Reset their current action points and go to the next player

         
        if (self.firstIter == False):
        #First loop doesn't render the screen. Redo the first render so that first player can see the map before the first move


            #Check to see if an entire team is wiped out
            self.check_victory()
            

            if (len(self.overlays) == 0 and self.skipToRefresh == False):
            #Skip any turns while there is still something to render
                
                for creature in self.participants:
                #Check for dead players; set their texture to bones and put their AP to 0 so they can't move
                    if (creature.living == False):
                        creature.apCurrent = 0
                        creature.apMax = 0
                        creature.texture = BONES
                        self.occupancy[creature.battleMapLocation[0]][creature.battleMapLocation[1]] = 0


                if activeParticipant.apCurrent <= 0:
                #If the current player is out of AP, reset their AP to the max, and move to the next player
                        if self.activeIndex == (len(self.participants) - 1):
                            activeParticipant.apCurrent = activeParticipant.apMax
                            self.activeIndex = 0
                        else:
                            activeParticipant.apCurrent = activeParticipant.apMax
                            self.activeIndex += 1
                
                #If the current player HAS AP, allow them to move
                elif activeParticipant.apCurrent > 0:
                    self.move_creature(activeParticipant)
        
        if (self.skipToRefresh):
        #Inserting a time delay for the animation to render 
            time.sleep(0.1)
        
        self.firstIter = False
        updatedBattle = battle(self.windowObject, self.battleMap, self.occupancy, self.participants, self.overlays, self.activeIndex, self.firstIter )
        #Create a new battle scene with the updated settings

        self.window.show_view(updatedBattle)
        #show the new battle map