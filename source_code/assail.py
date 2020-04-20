import arcade 
import assail_lib as al
import random


battleMap = al.generate_battle(oldBattleMap=[],buildNewBattleMap=True, baseTexture=0, newTexture=3, percentNewTexture=20)
battleMap = al.generate_battle(oldBattleMap=battleMap, buildNewBattleMap=False, baseTexture=0, newTexture=1, percentNewTexture=30)
battleMap = al.generate_battle(oldBattleMap=battleMap, buildNewBattleMap=False, baseTexture=0, newTexture=4, percentNewTexture=30)
battleMap = al.generate_battle(oldBattleMap=battleMap, buildNewBattleMap=False, baseTexture=0, newTexture=2, percentNewTexture=40)


window = arcade.Window(1200, 672, "Battle")
player1 = al.player(name='Essen')
player2 = al.player(name='Caric')
players = [player1, player2]

occupancy = al.assign_locations(battleMap, players)
participants = al.randomize_participants(players)
print(participants)
for creature in participants:
    creature.assign_texture()
battleStart = al.battle(arcade.get_window(), battleMap, occupancy, participants=participants, overlays=[], activeIndex=0, firstIter = True )
window.show_view(battleStart)
arcade.run()


