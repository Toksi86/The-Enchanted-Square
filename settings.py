WIDTH = 1280
HEIGHT = 720
FPS = 90
TILESIZE = 64
# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'


# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 150
ITEM_BOX_SIZE = 80
UI_FONT = 'path'
UI_FONT_SIZE = 18

# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UBGRADE_BG_COLOR_SELECTED = '#EEEEEE'

# weapons
weapon_data = {
    'sword': {'cooldown': 100, 'damage': 10, 'graphic': 'sprites/weapons/sword/full.png'},
    'axe': {'cooldown': 200, 'damage': 25, 'graphic': 'sprites/weapons/axe/full.png'},
}
# magic
magic_data = {
    'flame': {'strength': 5, 'cost': 20, 'graphic': 'sprites/magic/flame/full.png'},
    'heal': {'strength': 20, 'cost': 10, 'graphic': 'sprites/magic/heal/full.png'}
}

# enemy
monster_data = {
    'rabbit': {'health': 100, 'exp': 100, 'damage': 10, 'attack_type': 'claw', 'attack_cooldown': 500,
               'attack_sound': 'path_to_sound',
               'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
    'wolf': {'health': 300, 'exp': 250, 'damage': 40, 'attack_type': 'slash', 'attack_cooldown': 900,
             'attack_sound': 'path_to_sound',
             'speed': 3, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
    'fox': {'health': 200, 'exp': 175, 'damage': 20, 'attack_type': 'thunder', 'attack_cooldown': 750,
            'attack_sound': 'path_to_sound',
            'speed': 3, 'resistance': 3, 'attack_radius': 100, 'notice_radius': 300},

}
