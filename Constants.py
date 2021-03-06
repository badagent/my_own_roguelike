import libtcodpy as libtcod

class Constants:
    SCREEN_WIDTH = 80
    SCREEN_HEIGHT = 50
    LIMIT_FPS = 20


    MAP_WIDTH = 80
    MAP_HEIGHT = 43

    PANEL_HEIGHT = SCREEN_HEIGHT-MAP_HEIGHT

    #COLOR_DARK_WALL = libtcod.Color(0,0,100)
    COLOR_DARK_WALL = libtcod.Color(0,0,0)
    COLOR_LIGHT_WALL = libtcod.Color(130,110,50)
    COLOR_LIGHT_GROUND = libtcod.Color(200,180,50)
    COLOR_DARK_GROUND = libtcod.Color(50,50,150)
    HEAL_AMOUNT = 10

    LIGHNING_DAMAGE=20
    LIGHNING_RANGE=5

    FIREBALL_RADIUS = 3
    FIREBALL_DAMAGE = 12

    CONFUSE_NUM_TURNS = 10
    CONFUSE_RANGE=8

    ROOM_MAX_SIZE = 10
    ROOM_MIN_SIZE = 6
    MAX_ROOMS = 30
    MAX_ROOM_MONSTERS = 3
    MAX_ROOM_ITEMS = 2
    MAX_ITEMS_IN_INVENTORY = 26
    INVENTORY_WIDTH = 50

    FOV_ALGO = 0
    FOV_LIGHT_WALLS = True
    TORCH_RADIUS = 10

    BAR_WIDTH = 20

    MESSAGE_X_POS = BAR_WIDTH+2
    MESSAGE_WIDTH = SCREEN_WIDTH-MESSAGE_X_POS
    MESSAGE_HEIGHT = PANEL_HEIGHT-1
