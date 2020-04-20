#Collection of objects for the Assail game
import arcade 
import random 
import os
import assail_lib as al

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

def generate_battle(oldBattleMap=[], buildNewBattleMap=True, baseTexture=0, newTexture=2, percentNewTexture=60):
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





class battleView(arcade.View):

    def __init__(self, battleMap, participants, overlays):
        super().__init__()
        self.battleMap = battleMap
        self.participants = participants
        self.overlays = overlays

    
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)
        print('hello')

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
        text = input('Trying to pause the refresh process')
        print(text)
        newBattleMap = generate_battle()
        battleMapLocation = [random.randint(0,13), random.randint(0,24)]
        hero = al.creature(archetype='knight', battleMapLocation=battleMapLocation)
        newBattleView = battleView(newBattleMap, participants=[hero], overlays=[])
        self.window.show_view(newBattleView)



window = arcade.Window(1200, 672, "Battle")

newBattleMap = generate_battle()
battleMapLocation = [random.randint(0,13), random.randint(0,24)]
hero = al.creature(archetype='knight', battleMapLocation=battleMapLocation)
battleStart = battleView(newBattleMap, participants=[hero], overlays=[] )
window.show_view(battleStart)
arcade.run()