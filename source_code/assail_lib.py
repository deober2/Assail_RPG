#Collection of objects for the Assail game
import arcade 
import random 
import os

#Texture IDs and paths:
assailPath = os.getcwd()[0:-11]
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
KNIGHT_TEXTURE_DOWN = arcade.load_texture(assailPath + "resources/knight.png")


#Constants
XGRID = 25
YGRID = 14
XSCREEN = XGRID * 48
YSCREEN = YGRID * 48
GRID_AREA = YGRID * XGRID 
 
 
#Movement dictionary to get movement vectors
userInput = ['l', 'r', 'u', 'd']
moveVec = [[0,-1], [0,1], [1,0], [-1,0]]
moveDict = dict(zip(userInput, moveVec))
del userInput; del moveVec


#Archetype attack patterns
KNIGHT_ATTACK = [1]



#Game function definitions
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
                    walkable = check_walkable(battleMap, newLocation)
                    if (occupancy[newLocation[0]][newLocation[1]] == 0 and walkable):
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


def move_creature(creature, battleMap):
        #Function to enable player movement and actions
        ap = creature.apMax
        print('\n%s, it is your turn to move. You have %d action points (AP). Attacking costs 2 AP. ' % (creature.name, ap))
        print('Each move is represented by one lettter:\nl:left, r:right: u:up: d:down, a:attack, e:end turn')
        validMoves = ['l', 'r', 'u', 'd', 'a', 'e']
        move = []

        #filter valid moves, allow movement
        while (len(move) != 1 or ap > 0):
            print("Your are currently at ", end='')
            print(creature.battleMapLocation)
            print('with %d AP\n' % ap)
            move = input('Please enter a single move: ').strip().lower()
            print(move)
            print(len(move))

            if (len(move) == 1 and move in validMoves and ap >0):
                if move == 'e':
                    ap = 0
                elif (move == 'a' and  ap >= 2):
                    print('do attack procedure\n')
                    ap -= 2
                else:
                    moveVec = moveDict[move]
                    newLocation = elementwise_add(creature.battleMapLocation, moveVec)
                    if (check_bounds(newLocation)):
                        character.battleMapLocation = newLocation
                        ap -= 1
                        self.on_draw(self, battleMap=battleMap, participants=[creature], overlays=[])
                        print(creature.battleMapLocation)
                        print('New AP: %d' % ap)
                    else:
                        print(character.battleMapLocation)
                        print('move invalid')




#Game Object definitions
class creature:
    #Class representing moveable characters
    def __init__(self, name='noName', archetype='knight', battleMapLocation=[5, 10], team='red', apMax=4, orientation='down'):
        self.name = name
        self.archetype = archetype
        self.battleMapLocation = battleMapLocation
        self.team = team
        self.apMax = apMax
        self.apCurrent = apMax
        self.orientation = orientation
        self.texture = None
    
    def assign_texture(self):
        if self.archetype == 'knight':
            if self.orientation == 'down':
                self.texture = KNIGHT_TEXTURE_DOWN
    

class player(creature):
    def __init__(self, name='noName', archetype='knight', battleMapLocation=[5, 10], team='red', apMax=4, orientation='down', teamMembers=[], money=1000 ):
        super().__init__(self)
        self.name = name
        self.archetype = archetype
        self.battleMapLocation = battleMapLocation
        self.team = team
        self.apMax = apMax
        self.apCurrent = apMax
        self.orientation = orientation
        self.texture = None
        self.teamMembers = teamMembers
        self.money = money


class overlay:
    #Class representing images to be rendered on top of the map and participating creatures. 
    #Intended for animation
    def __init__(self, texture, battleMapLocation):
        self.texture = texture
        self.battleMapLocation = battleMapLocation

   
class battle(arcade.View):

    def __init__(self, windowObject, battleMap, occupancy, participants, overlays, activeIndex, firstIter):
        super().__init__()
        self.windowObject = windowObject
        self.battleMap = battleMap
        self.occupancy = occupancy
        self.participants = participants
        self.overlays = overlays
        self.activeIndex = activeIndex
        self.firstIter = firstIter
    
    def on_show(self):
        #Runs once, when the window is initialized
        arcade.set_background_color(arcade.color.WHITE)
        print('Battle has begun\n')
        print(self.activeIndex)

        
        

    def move_creature(self, creature):
        print('\n%s\'s turn to move. You have %d action points (AP). Moving costs 1 AP, attacking costs 2 AP. ' % (creature.name, creature.apCurrent))
        print('Each move is represented by one lettter:\nl:left, r:right: u:up: d:down, a:attack, e:end turn')
        validMoves = ['l', 'r', 'u', 'd', 'a', 'e']
        move = []

        #Filter invalid moves and perform acitons
        while (len(move) != 1 or move not in validMoves):
            move = input('Please enter a single valid move: ').strip().lower()
            if (move == 'a' and creature.apCurrent < 2):
                move = 'attack_not_valid'
        
        print('Your move is '); print(move)
        if (len(move) == 1 and move in validMoves and creature.apCurrent >0):
            if move == 'e':
                creature.apCurrent = 0
            elif (move == 'a' and  creature.apCurrent >= 2):
                print('do attack procedure: '); print(KNIGHT_ATTACK)
                creature.apCurrent -= 2
            else:
                moveVec = moveDict[move]
                newLocation = elementwise_add(creature.battleMapLocation, moveVec)
                if (check_bounds(newLocation) and check_vacancy(self.occupancy, newLocation) and check_walkable(self.battleMap, newLocation)):
                    self.occupancy[creature.battleMapLocation[0]][creature.battleMapLocation[1]] = 0
                    creature.battleMapLocation = newLocation
                    self.occupancy[creature.battleMapLocation[0]][creature.battleMapLocation[1]] = 1
                    creature.apCurrent -= 1
                    print(creature.battleMapLocation)
                    print('New AP: %d' % creature.apCurrent)
                else:
                    print(creature.battleMapLocation)
                    print('move invalid. Space is off-grid, occuppied or not walkable.')
            


    def on_draw(self):
        arcade.start_render()
        
        #Draw the battleMap tile background:
        for i in range(len(self.battleMap)):
            for j in range(len(self.battleMap[0])):
                x = 24 + 48 * j
                y = 24 + 48 * i 
                
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

                arcade.draw_scaled_texture_rectangle(x, y, texture, 1, 0)

        #Draw all participating creatures
        if self.participants:
            for participant in self.participants:
                x = 24 + 48 * participant.battleMapLocation[1]
                y = 24 + 48 * participant.battleMapLocation[0]

                arcade.draw_scaled_texture_rectangle(x, y, participant.texture, 1, 0)

        #Draw all overlay images
        if self.overlays:
            for overlay in self.overlays:
                x = 24 + 48 * overlay.battleLocation[1]
                y = 24 + 48 * overlay.battleLocation[0]
                arcade.draw_scaled_texture_rectangle(x, y, overlay.texture, 1, 0)


    def on_update(self, delta_time=0.1):
        #Main loop of the battle program. This is where all creature turns take place
        activeParticipant = self.participants[self.activeIndex]
        
        #closeWindow = input('Close Window?: ').strip().lower()
        #if (closeWindow == 'y' or closeWindow == 'yes'):
        #    self.windowObject.close_window()

        #if the active player is out of action points and they are the last player in the full turn,
        #Reset their current action points and go to the next player
        if (self.firstIter == False):
            if activeParticipant.apCurrent <= 0:
                    if self.activeIndex == (len(self.participants) - 1):
                        
                        activeParticipant.apCurrent = activeParticipant.apMax
                        self.activeIndex = 0
                    else:
                        activeParticipant.apCurrent = activeParticipant.apMax
                        self.activeIndex += 1
            
            elif activeParticipant.apCurrent > 0:
                self.move_creature(activeParticipant)
                print(self.activeIndex)
        self.firstIter = False
        updatedBattle = battle(self.windowObject, self.battleMap, self.occupancy, self.participants, self.overlays, self.activeIndex, self.firstIter )
        self.window.show_view(updatedBattle)