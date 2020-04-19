import arcade 
import random
import os


name = 'player1'
ap = 4
location = [13,24]
xUpperBound = 25
yUpperBound = 14

#Movement dictionary to get movement vectors
userInput = ['l', 'r', 'u', 'd']
moveVec = [[0,-1], [0,1], [1,0], [-1,0]]
moveDict = dict(zip(userInput, moveVec))
del userInput; del moveVec

print('\n%s, it is your turn to move. You have %d action points (AP). Attacking costs 2 AP. ' % (name, ap))
print('Each move is represented by one lettter:\nl:left, r:right: u:up: d:down, a:attack, e:end turn')
validMoves = ['l', 'r', 'u', 'd', 'a', 'e']
move = []
while (len(move) != 1 or ap > 0):

    print("Your are currently at ", end='')
    print(location)
    print('with %d AP\n' % ap)
    move = input('Please enter a single move: ').strip().lower()
    print(move)
    print(len(move))
    
    if (len(move) == 1 and move in validMoves and ap >0):

        if move == 'e':
            ap = 0
        
        elif (move == 'a' and  ap >= 2):
            print('do attack procedure')
            ap -= 2
        
        else:
            moveVec = moveDict[move]
            newLocation = [location[0] + moveVec[0], location[1] + moveVec[1]]
            if (newLocation[0] > -1 and newLocation[1] > -1 and newLocation[0] < yUpperBound and newLocation[1] < xUpperBound):
                location = newLocation
                ap -= 1
                print('move successful. New location:')
                print(location)
                print('New AP: %d' % ap)
            else:
                print(location)
                print('move invalid')



        




