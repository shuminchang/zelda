import os

dir_path = os.getcwd()

# game setup
WIDTH    = 1280	
HEIGHT   = 720
FPS      = 60
TILESIZE = 64
HITBOX_OFFSET = {
    'player': -26,
    'object': -40,
    'grass': -10,
    'invisible': 0}

# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = os.path.join(dir_path, 'graphics', 'font', 'joystix.ttf')
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'

# weapons 
weapon_data = {
	'sword': {'cooldown': 100, 'damage': 15,'graphic': os.path.join(dir_path, 'graphics', 'weapons', 'sword', 'full.png')},
	'lance': {'cooldown': 400, 'damage': 30,'graphic': os.path.join(dir_path, 'graphics', 'weapons', 'lance', 'full.png')},
	'axe': {'cooldown': 300, 'damage': 20, 'graphic': os.path.join(dir_path, 'graphics', 'weapons', 'axe', 'full.png')},
	'rapier':{'cooldown': 50, 'damage': 8, 'graphic': os.path.join(dir_path, 'graphics', 'weapons', 'rapier', 'full.png')},
	'sai':{'cooldown': 80, 'damage': 10, 'graphic': os.path.join(dir_path, 'graphics', 'weapons', 'sai', 'full.png')}}

# magic
magic_data = {
    'flame': {'strength': 5, 'cost': 20, 'graphic': os.path.join(dir_path, 'graphics', 'particles', 'flame', 'fire.png')},
    'heal': {'strength': 20, 'cost': 10, 'graphic': os.path.join(dir_path, 'graphics', 'particles', 'heal', 'heal.png')}
}

# enemy
monster_data = {
	'squid': {'health': 100,'exp':100,'damage':20,'attack_type': 'slash', 'attack_sound': os.path.join(dir_path, 'audio', 'attack', 'slash.wav'), 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
	'raccoon': {'health': 300,'exp':250,'damage':40,'attack_type': 'claw',  'attack_sound': os.path.join(dir_path, 'audio', 'attack', 'claw.wav'),'speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
	'spirit': {'health': 100,'exp':110,'damage':8,'attack_type': 'thunder', 'attack_sound': os.path.join(dir_path, 'audio', 'attack', 'fireball.wav'), 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
	'bamboo': {'health': 70,'exp':120,'damage':6,'attack_type': 'leaf_attack', 'attack_sound': os.path.join(dir_path, 'audio', 'attack', 'slash.wav'), 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300}}


story = """
Title: "The Chronicles of Eldoria: Shadows of the Lost Kingdom"

Chapter 1: The Awakening

In the mystical land of Eldoria, where magic intertwines with nature, a young adventurer named Arya awakens in the ancient forest of Eldorwood. With no memory of her past, she finds herself clutching a mysterious amulet that pulses with arcane energy. Arya soon learns that she is in a world plagued by darkness, where the once-mighty Kingdom of Eldoria has fallen into ruin, and its people are scattered and oppressed by malevolent forces.

Chapter 2: The Quest Begins

Determined to uncover her past and the secrets of the amulet, Arya journeys through the lush, yet perilous, landscapes of Eldoria. She encounters the remnants of the once-great civilization - abandoned villages, overgrown ruins, and cryptic temples. In the village of Sunstone, she meets an old sage who reveals that her amulet is a key to an ancient power capable of restoring Eldoria.

Chapter 3: Allies and Adversaries

Arya's quest leads her to ally with diverse characters: Thane, a stoic warrior seeking redemption; Lira, a mischievous mage with her own agenda; and Rook, a mysterious wanderer with a connection to the shadows. Together, they face formidable enemies: corrupted creatures, the spectral minions of a dark sorcerer, and rival adventurers with conflicting goals.

Chapter 4: The Four Elemental Temples

The group learns of four elemental temples - Earth, Wind, Fire, and Water - each holding a piece of the key to unlock the amulet's full potential. As Arya and her companions traverse to these temples, they face trials that test their resolve, uncovering abilities and secrets hidden within themselves and the lands of Eldoria.

Chapter 5: Shadows of the Past

In their journey, Arya's fragmented memories resurface, revealing her royal lineage as the lost princess of Eldoria and the amulet's role in the kingdom's downfall. The dark sorcerer, revealed to be a former royal advisor corrupted by forbidden magic, seeks to harness the amulet’s power for his twisted vision.

Chapter 6: The Final Confrontation

With the power of the elemental temples infused in the amulet, Arya and her allies make their stand against the dark sorcerer in his shadowy fortress. In an epic battle of magic and might, Arya confronts the sorcerer, realizing that the amulet can either restore Eldoria or doom it forever.

Chapter 7: Dawn of a New Era

Upon defeating the sorcerer, Arya faces a choice: to use the amulet's power to erase the darkness or to destroy it, losing her powers but ensuring it can never be misused again. Depending on the player's choice, Eldoria either witnesses the rebirth of its kingdom under Arya's benevolent rule or sees the dawn of a new era where magic is no more, and its people embark on a path of rebuilding through unity and resilience.

Epilogue: The Legacy of Eldoria

As the game concludes, the story reflects on the journey of Arya and her companions, each finding their place in the new world they've helped shape. Arya, whether as a wise queen or a humble hero, leaves a legacy that forever echoes in the annals of Eldoria: a tale of courage, friendship, and the enduring light that shines even in the darkest of times.
"""