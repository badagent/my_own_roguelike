import libtcodpy as libtcod
from Object import Object
from objects.Fighter import *
from objects.Ai import *
from objects.Item import *
from Constants import Constants

class Level:

    def __init__(self,game):
        self.console = game.map_console
        self.objects = []
        self.game = game

    def add_object(self,object):
        self.objects.append(object)

    def is_in_fov(self,x,y):
        return libtcod.map_is_in_fov(self.fov_map,x,y)
    
    def place_items(self,room):
        num_items = libtcod.random_get_int(0,0,Constants.MAX_ROOM_ITEMS)
        for i in range(num_items):
            x = libtcod.random_get_int(0,room.x1+1,room.x2-1)
            y = libtcod.random_get_int(0,room.y1+1,room.y2-1)

            if not self.is_blocked(x,y):
                dice = libtcod.random_get_int(0,0,100)
                if dice < 55:
                    item = Object(self.console,self,x,y,"!","healing potion",libtcod.violet,item=Item(use_function=heal_player))
                elif dice < 55+15:
                    item_component = Item(use_function=cast_lightning)
                    item = Object(self.console,self,x,y,"#","scroll of lightning bolt",libtcod.light_yellow,item=item_component)
                elif dice < 55+15+15:
                    item_component = Item(use_function=cast_fireball)
                    item = Object(self.console,self,x,y,"#","scroll of fireball",libtcod.light_yellow,item=item_component)
                else:
                    item_component = Item(use_function=cast_confuse)
                    item = Object(self.console,self,x,y,"#","scroll of confusion",libtcod.light_yellow,item=item_component)
                self.objects.append(item)
                        
                        
                self.send_to_back(item)


    def place_objects(self,room):
        num_monsters = libtcod.random_get_int(0,0,Constants.MAX_ROOM_MONSTERS)

        for i in range(num_monsters):
            x = libtcod.random_get_int(0,room.x1+1,room.x2-1)
            y = libtcod.random_get_int(0,room.y1+1,room.y2-1)
            if not self.is_blocked(x,y):
                if libtcod.random_get_int(0,0,100) < 80:
                    fighter_comp = Fighter(hp=10,defense=0,power=3,death_function=monster_death)
                    ai_comp = BasicMonster()
                    monster = Object(self.console,self,x,y,'o','Orc', libtcod.desaturated_green,blocks=True,fighter=fighter_comp,ai=ai_comp)
                else:
                    fighter_comp = Fighter(hp=16,defense=1,power=4,death_function=monster_death)
                    ai_comp = BasicMonster()
                    monster = Object(self.console,self,x,y,'T','Troll',libtcod.darker_green,blocks=True,ai=ai_comp,fighter=fighter_comp)
                self.add_object(monster)


    def send_to_back(self,object):
        self.objects.remove(object)
        self.objects.insert(0,object)

    def create_room(self,room):
        for x in range(room.x1+1,room.x2):
            for y in range(room.y1+1,room.y2):
                self.map[x][y].blocked=False
                self.map[x][y].block_sight=False

    def make_map(self):
        self.map = [[ Tile(True) for y in range(Constants.MAP_HEIGHT) ] for x in range(Constants.MAP_WIDTH)]
        self.rooms = []
        num_rooms = 0
        for r in range(Constants.MAX_ROOMS):
            w = libtcod.random_get_int(0,Constants.ROOM_MIN_SIZE,Constants.ROOM_MAX_SIZE)
            h = libtcod.random_get_int(0,Constants.ROOM_MIN_SIZE,Constants.ROOM_MAX_SIZE)
            x = libtcod.random_get_int(0,0,Constants.MAP_WIDTH-w-1)
            y = libtcod.random_get_int(0,0,Constants.MAP_HEIGHT-h-1)
            new_room = Rect(x,y,w,h)
            failed = False
            for other in self.rooms:
                if(new_room.intersect(other)):
                    failed = True
                    break
            if not failed:
                self.create_room(new_room)
                (new_x,new_y) = new_room.center()
                if num_rooms == 0:
                    self.playerStart = (new_x,new_y)
                else:
                    (prev_x,prev_y) = self.rooms[num_rooms-1].center()
                    if(libtcod.random_get_int(0,0,1)==1):
                        self.create_h_tunnel(prev_x,new_x,prev_y)
                        self.create_v_tunnel(new_x,prev_y,new_y)
                    else:
                        self.create_v_tunnel(prev_x,prev_y,new_y)
                        self.create_h_tunnel(prev_x,new_x,new_y)
                self.place_items(new_room)
                self.place_objects(new_room)
                self.rooms.append(new_room)
                num_rooms+=1
        self.make_fov_map()

    def get_visible_objects_at_pos(self,x,y):
        return [obj for obj in self.objects if obj.x == x and obj.y == y and self.is_in_fov(x,y)]

    def make_fov_map(self):
        self.game.fov_recompute = True
        self.fov_map = libtcod.map_new(Constants.MAP_WIDTH,Constants.MAP_HEIGHT)
        for x in range(Constants.MAP_WIDTH):
            for y in range(Constants.MAP_HEIGHT):
                libtcod.map_set_properties(self.fov_map,x,y,not self.map[x][y].block_sight, not self.map[x][y].blocked)
    

    def is_blocked(self,x,y):
        if self.map[x][y].blocked:
            return True
        for object in self.objects:
            if(object.blocks and object.x==x and object.y==y):
                return True
        return False

    def create_h_tunnel(self,x1,x2,y):
        for x in range(min(x1,x2),max(x1,x2)+1):
            self.map[x][y].blocked=False
            self.map[x][y].block_sight=False

    def create_v_tunnel(self,x,y1,y2):
        for y in range(min(y1,y2),max(y1,y2)+1):
            self.map[x][y].blocked=False
            self.map[x][y].block_sight=False

class Rect:
    def __init__(self,x,y,w,h):
        self.x1=x
        self.x2=x+w
        self.y1=y
        self.y2=y+h

    def center(self):
        center_x = int((self.x1+self.x2)/2)
        center_y = int((self.y1+self.y2)/2)
        return (center_x,center_y)

    def intersect(self,other):
        return(self.x1<=other.x2 and self.x2>=other.x1 and self.y1<=other.y2 and self.y2>=other.y1)

class Tile:
    def __init__(self,blocked, block_sight=None):
        self.explored = False
        self.blocked = blocked
        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight
