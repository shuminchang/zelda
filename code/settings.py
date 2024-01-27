import os

# game setup
WIDTH    = 1280	
HEIGHT   = 720
FPS      = 60
TILESIZE = 64

dir_path = os.getcwd()

# weapons 
weapon_data = {
	'sword': {'cooldown': 100, 'damage': 15,'graphic': os.path.join(dir_path, 'graphics\\weapons\\sword\\full.png')},
	'lance': {'cooldown': 400, 'damage': 30,'graphic': os.path.join(dir_path, 'graphics\\weapons\\lance\\full.png')},
	'axe': {'cooldown': 300, 'damage': 20, 'graphic': os.path.join(dir_path, 'graphics\\weapons\\axe\\full.png')},
	'rapier':{'cooldown': 50, 'damage': 8, 'graphic': os.path.join(dir_path, 'graphics\\weapons\\rapier\\full.png')},
	'sai':{'cooldown': 80, 'damage': 10, 'graphic': os.path.join(dir_path, 'graphics\\weapons\\sai\\full.png')}}