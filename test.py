import json
from Character.Main_Char import Adventurer, Enemy
import yaml


a_file = open("Enemies/enemies.yml", "r")
yaml_object = yaml.load_all(a_file, Loader=yaml.FullLoader)

dungeon = {}
for data in yaml_object :
    dungeon = data

a_file.close()

slime = Enemy(fname = 'slime', **dungeon['Slime'])

print(slime.action(0.1))