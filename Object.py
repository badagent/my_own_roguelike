import libtcodpy as libtcod
import math
class Object:
    #Represents an object on Screen
    def __init__(self,con,level,x,y,char,name,color,blocks=False,fighter=None,ai=None,item=None):
        self.x = int(x)
        self.y = int(y)
        self.name = name
        self.char = char
        self.level = level
        #Needs to be relinked.
        self.con = con
        
        
        self.game = level.game
        self.color = color
        self.blocks = blocks
        self.fighter=fighter
        if self.fighter:
            self.fighter.owner = self
        self.item=item
        if self.item:
            self.item.owner = self
        self.ai = ai
        if self.ai:
            self.ai.owner = self

    def move(self,dx,dy):
        if not self.level.is_blocked(self.x+dx,self.y+dy):
            self.x += dx
            self.y += dy

    def message(self,msg,color=libtcod.white):
        self.level.game.message(msg,color)

    def move_towards(self,target_x,target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        dx = int(round(dx/distance))
        dy = int(round(dy/distance))
        self.move(dx,dy)

    def distance_to(self,other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx**2  + dy**2)
    
    def distance(self,x,y):
        return math.sqrt((x-self.x)**2  + (y-self.y)**2)

    def draw(self,fov_map):
        if(libtcod.map_is_in_fov(fov_map,self.x,self.y)):
            libtcod.console_set_default_foreground(self.con,self.color)
            libtcod.console_put_char(self.con,self.x,self.y,self.char,libtcod.BKGND_NONE)

    def clear(self):
        libtcod.console_put_char(self.con,self.x,self.y,' ',libtcod.BKGND_NONE)
