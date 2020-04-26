import arcade 
import assail_lib as al
import random

WINDOW_SCALE = 1

battleMap = al.generate_battle(oldBattleMap=[],buildNewBattleMap=True, baseTexture=0, newTexture=3, percentNewTexture=20)
battleMap = al.generate_battle(oldBattleMap=battleMap, buildNewBattleMap=False, baseTexture=0, newTexture=1, percentNewTexture=30)
battleMap = al.generate_battle(oldBattleMap=battleMap, buildNewBattleMap=False, baseTexture=0, newTexture=4, percentNewTexture=30)
battleMap = al.generate_battle(oldBattleMap=battleMap, buildNewBattleMap=False, baseTexture=0, newTexture=2, percentNewTexture=40)


window = arcade.Window(round(WINDOW_SCALE * 1200), round(WINDOW_SCALE * 672), "Battle")
player1 = al.player(name=al.random_name())
player2 = al.player(name=al.random_name(), archetype='mage', team='red')

players = [player1, player2]
for player in players:
    player.assign_attributes()
    print(player2.team)

#Important!!!! can't append to the player.teamMembers array. Need to re-assign (seen in the player.teamMembers = members line)
members = []
for i in range(1):
    name = al.random_name()
    creature = al.creature(name=name, archetype='knight')
    creature.assign_attributes()
    members.append(creature)
print(player2.team)
player1.teamMembers = members

occupancy = al.assign_locations(battleMap, players)
participants = al.randomize_participants(players)
for i in participants:
    print(i.name)
for creature in participants:
    creature.assign_attributes()
print(player2.team)
battleStart = al.battle(arcade.get_window(), battleMap, occupancy, participants=participants, overlays=[], activeIndex=0, firstIter = True )
window.show_view(battleStart)
arcade.run()


