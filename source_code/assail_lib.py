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

#Movement dictionary to get movement vectors
userInput = ['l', 'r', 'u', 'd']
moveVec = [[-1,0], [1,0], [0,1], [0,-1]]
modeDict = dict(zip(userInput, moveVec))
del userInput; del moveVec


#Archetype attack patterns
KNIGHT_ATTACK = [1]



#Game function definitions


#Game Object definitions

class creature:
    #Class representing moveable characters
    def __init__(self, name='noName', archetype='knight', battleMapLocation=[5, 10]):
        self.archetype = archetype
        self.battleMapLocation = battleMapLocation
        self.texture = None
        self.name = name
        self.apMax = 4

        if (self.archetype == 'knight'):
            self.texture = KNIGHT_TEXTURE_DOWN

   


class overlay:
    #Class representing images to be rendered on top of the map and participating creatures. 
    #Intended for animation
    def __init__(self, texture, battleMapLocation):
        self.texture = texture
        self.battleMapLocation = battleMapLocation


class player:
    #Class defining a player. Can be a human or computer, once cpu algorithm is implemented
    def __init__(self, name='noName', color='gold', money=1000, archetype='knight', teamMembers=[], maxAP=4):
        self.name = name
        self.color = color
        self.money = money
        self.archetype = archetype
        self.teamMembers = teamMembers
        self.ap = maxAP
        self.character = creature(name='player1', archetype='knight', battleMapLocation=[5, 10])
    
    def playerMove(self):
        print('%s, it is your turn to move.\nYou have %d action points (AP). Attacking costs 2 AP\n' % (self.name, self.ap))
        print('Enter your full move as a string of letters without spacecs.\n')
        print('"l" for left, "r" for right, "u" for up, "d" for down and "a" for attack:\n')
        validMoves = ['lrdua']
        move = input('Please enter your move: ').strip().lower()
        acceptMove = False

        #Screen for valid move syntax
        while (any(move) not in validMoves or acceptMove == False):
            if any(move) not in validMoves:
                print('You entered an invalid move. Please limit your move input to the characters "lruda".\n')
                move = input('Please enter your move: ').strip().lower()
            
            if acceptMove == False:
                print('Your proposed move is %s.\n' % move)
                acceptMove = input("Do you accept this move? (y/n)").strip().lower()
                if acceptMove == 'y' or acceptMove == 'yes':
                    acceptMove = True
                elif acceptMove == 'n' or acceptMove == 'no':
                    acceptMove = False
                    move = input('Please enter your move: ').strip().lower()
                else:
                    print('You may have entered an invalid answer (not y/n). Returning to move selection\n')
        
        #build a proposed movement path. 
        for char in move:
            if char == 'a':
                print('You proposed an attack from this location.\n')
                attackDirection = input('Enter an attack direction (lrud): ')

   

class battle(arcade.Window):
    #class to create and run a battle map
    

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT ):
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.GRID_OFFSET = 24
        self.CREATURE_OFFSET = 16
        self.SCALE = 1

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT)


    def generate_battle(self,oldBattleMap=[], buildNewBattleMap=True, baseTexture=0, newTexture=2, percentNewTexture=60):
        #Method to procedurally Generate a battleMap (an mxn grid of integers representing individual tile textures).
        #Can pass an existing battleMap and generate on top of the old map, or generate a completely new map.
        #Arguments:
        #   oldBattleMap (mxn list): existing battleMap that you wish to write on top of. Default is an empty list
        #   buildNewBattleMap (boolean): Whether or not to generate a completely new map. Pair True with empty oldBattleMap, or False with filled oldBattleMap
        #   baseTexture (int, [0-4]): defines the base texture to fill the initial map. Refers to one of the textures defined above
        #   newTexture (int, [0-4]): defines the new texture to draw on top of the existing battle map. Refers to one of the textures defined above
        #   percentNewTexture (int, [1-100]): defines the percentage of the map that newTexture should occupy
        
        XGRID = 25
        YGRID = 14
        XSCREEN = XGRID * 48
        YSCREEN = YGRID * 48
        GRID_AREA = YGRID * XGRID


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


    def on_draw(self, battleMap, participants, overlays):
        #Method to draw the battleMap, all participating characters, and all other overlay images
        #Arguments:
        #   battleMap: mxn list of integers representing the texture for each grid coordinate
        #   participants: list of creature objects to draw to the window
        #   overlays: list of overlay images intended for use as steps in an animation
        #Draws onto the battle window in three stages:
        #   1. draws the tile background 
        #   2. draws all participating characters
        #   3. draws all overlay images 
        #   4. renders to the window

        arcade.start_render()

        #Draw the battleMap tile background:
        for i in range(len(battleMap)):
            for j in range(len(battleMap[0])):
                x = self.GRID_OFFSET + 48 * j
                y = self.GRID_OFFSET + 48 * i 
                
                if battleMap[i][j] == WATER:
                    texture = WATER_TEXTURE
                elif battleMap[i][j] == TREE:
                    texture = TREE_TEXTURE
                elif battleMap[i][j] == GRASS:
                    texture = GRASS_TEXTURE
                elif battleMap[i][j] == ROCK:
                    texture = ROCK_TEXTURE
                elif battleMap[i][j] == DIRT:
                    texture = DIRT_TEXTURE

                arcade.draw_scaled_texture_rectangle(x, y, texture, self.SCALE, 0)

        #Draw all participating creatures
        if participants:
            for participant in participants:
                x = self.GRID_OFFSET + 48 * participant.battleMapLocation[1]
                y = self.GRID_OFFSET + 48 * participant.battleMapLocation[0]

                arcade.draw_scaled_texture_rectangle(x, y, participant.texture, self.SCALE, 0)

        #Draw all overlay images
        if overlays:
            for overlay in overlays:
                x = self.GRID_OFFSET + 48 * overlay.battleLocation[1]
                y = self.GRID_OFFSET + 48 * overlay.battleLocation[0]
                arcade.draw_scaled_texture_rectangle(x, y, overlay.texture, self.SCALE, 0)

        #arcade.finish_render()

    def move_player(self, character, battleMap):
        ap = character.apMax
        print('\n%s, it is your turn to move. You have %d action points (AP). Attacking costs 2 AP. ' % (character.name, ap))
        print('Each move is represented by one lettter:\nl:left, r:right: u:up: d:down, a:attack, e:end turn')
        validMoves = ['l', 'r', 'u', 'd', 'a', 'e']
        move = []

        #filter valid moves, allow movement
        while (len(move) != 1 or ap > 0):
            print("Your are currently at ", end='')
            print(character.battleMapLocation)
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
                    newLocation = [character.battleMapLocation[0] + moveVec[0], character.battleMapLocation[1] + moveVec[1]]
                    if (newLocation[0] > -1 and newLocation[1] > -1 and newLocation[0] < len(battleMap) and newLocation[1] < len(battleMap[0])):
                        character.battleMapLocation = newLocation
                        ap -= 1
                        self.on_draw(self, battleMap=battleMap, participants=[character], overlays=[])
                        print(character.battleMapLocation)
                        print('New AP: %d' % ap)
                    else:
                        print(character.battleMapLocation)
                        print('move invalid')

    def run_battle(self, battleMap, participants):
        #arcade.open_window(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, 'Battle Map')

        self.on_draw(battleMap, participants=participants, overlays=[])
        
        arcade.run()

        

        




