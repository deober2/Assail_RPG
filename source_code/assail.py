import arcade 
import assail_lib as al


test = al.battle(1200, 672)
battleMap = test.generate_battle(oldBattleMap=[],buildNewBattleMap=True, baseTexture=0, newTexture=3, percentNewTexture=20)
battleMap = test.generate_battle(oldBattleMap=battleMap, buildNewBattleMap=False, baseTexture=0, newTexture=1, percentNewTexture=30)
battleMap = test.generate_battle(oldBattleMap=battleMap, buildNewBattleMap=False, baseTexture=0, newTexture=4, percentNewTexture=30)
battleMap = test.generate_battle(oldBattleMap=battleMap, buildNewBattleMap=False, baseTexture=0, newTexture=2, percentNewTexture=40)

hero = al.creature(archetype='knight')

#test.run_battle(battleMap, participants=[hero])


