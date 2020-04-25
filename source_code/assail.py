import arcade 
import assail_lib as al
import random


battleMap = al.generate_battle(oldBattleMap=[],buildNewBattleMap=True, baseTexture=0, newTexture=3, percentNewTexture=20)
battleMap = al.generate_battle(oldBattleMap=battleMap, buildNewBattleMap=False, baseTexture=0, newTexture=1, percentNewTexture=30)
battleMap = al.generate_battle(oldBattleMap=battleMap, buildNewBattleMap=False, baseTexture=0, newTexture=4, percentNewTexture=30)
battleMap = al.generate_battle(oldBattleMap=battleMap, buildNewBattleMap=False, baseTexture=0, newTexture=2, percentNewTexture=40)


window = arcade.Window(1200, 672, "Battle")
player1 = al.player(name='player1')
player2 = al.player(name='player2', archetype='mage')

players = [player1, player2]
for player in players:
    player.assign_texture()
    player.assign_attack()

#Important!!!! can't append to the player.teamMembers array. Need to re-assign (seen in the player.teamMembers = members line)
members = []
for i in range(4):
    name = 'creature_' + str(i)
    creature = al.creature(name=name, archetype='knight')
    creature.assign_texture()
    creature.assign_attack()
    members.append(creature)
player1.teamMembers = members


occupancy = al.assign_locations(battleMap, players)
participants = al.randomize_participants(players)
for i in participants:
    print(i.name)
for creature in participants:
    creature.assign_texture()
battleStart = al.battle(arcade.get_window(), battleMap, occupancy, participants=participants, overlays=[], activeIndex=0, firstIter = True )
window.show_view(battleStart)
arcade.run()


