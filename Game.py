import libtcodpy as libtcod
from World import *
from UI import *
from Constants import Constants
from Menu import *
import shelve

class Game:
    
    def __init__(self):
        self.game_state = "playing"
        self.map_console = libtcod.console_new(Constants.MAP_WIDTH,Constants.MAP_HEIGHT)
        self.panel_console = libtcod.console_new(Constants.SCREEN_WIDTH,Constants.PANEL_HEIGHT)

        self.level = Level(self)
        self.level.make_map()

        self.inventory = []

        fighter_comp = Fighter(hp=30,defense=2,power=5,death_function=player_death)
        playerStart = self.level.playerStart
        self.player = Object(self.map_console,self.level,playerStart[0],playerStart[1],'@','Player',libtcod.white,blocks=True,fighter=fighter_comp)
        
        self.level.add_object(self.player)

        self.player_action = 'no turn';
        self.fov_recompute = True;

        self.UI = UI(self,self.panel_console)
        
        

        self.key = libtcod.Key()
        self.mouse = libtcod.Mouse()

        
    def save_game(self):
        file = shelve.open('save','n')
        file['map'] = self.level
        file['player'] = self.level.objects.index(self.player)
        file['inventory'] = self.inventory
        file['messages'] = self.UI.messages
        file['game_state']=self.game_state
        print(self.game_state)
        file.close()

    def load_game(self):
        file = shelve.open('save','r')
        self.level = file['map']
        self.level.console = self.map_console
        self.player = self.level.objects[file['player']]
        self.inventory = file['inventory']

        self.UI.messages =file['messages']

        self.game_state = file['game_state']
        print(self.game_state)
        file.close()
        self.level.game = self
        self.level.make_fov_map()
        for obj in self.inventory:
            obj.con = self.map_console
            obj.game = self
        for obj in self.level.objects:
            obj.con = self.map_console
            obj.game = self


    def player_move_or_attack(self,dx,dy):
        x=self.player.x + dx
        y=self.player.y + dy
        target = None
        for object in self.level.objects:
            if object.fighter and object.x==x and object.y == y:
                target = object
                break
        if target is not None:
            self.player.fighter.attack(target)
        else:
            self.player.move(dx,dy)
            self.fov_recompute = True

    def message(self,msg,color=libtcod.white):
        self.UI.message(msg,color)

    def get_names_at_mouse_pos(self):
        (x,y) = (self.mouse.cx,self.mouse.cy)
        objects = self.level.get_visible_objects_at_pos(x,y)
        return ', '.join([ obj.name.capitalize() for obj in objects ])

    def handle_keys(self):

        if(self.key.vk == libtcod.KEY_ENTER and self.key.lalt):
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
            return 'no turn'

        if(self.key.vk == libtcod.KEY_ESCAPE):
            return 'exit'
        if self.game_state=='playing':
            if self.key.vk==libtcod.KEY_UP:
                self.player_move_or_attack(0,-1)
                self.fov_recompute = True
                return 'move'
            elif self.key.vk==libtcod.KEY_DOWN:
                self.player_move_or_attack(0,1)
                self.fov_recompute = True
                return 'move'
            elif self.key.vk==libtcod.KEY_LEFT:
                self.player_move_or_attack(-1,0)
                self.fov_recompute = True
                return 'move'
            elif self.key.vk==libtcod.KEY_RIGHT:
                self.player_move_or_attack(1,0)
                self.fov_recompute = True
                return 'move'
            else:
                key_char = chr(self.key.c)
                if(key_char=='g'):
                    #pick up
                    objects = self.level.get_visible_objects_at_pos(self.player.x,self.player.y)
                    items = [ obj for obj in objects if obj.item ]
                    if(len(items)>0):
                        items.pop().item.pick_up()
                if(key_char=='i'):
                    #show inventory
                    options = [item.name for item in self.inventory]
                    if(len(options)==0):
                        options.append("Your Inventory is empty.")
                    dialog = Menu(self.map_console,"Inventory",options,Constants.INVENTORY_WIDTH)
                    index = dialog.show()
                    if(len(self.inventory)>0 and index != None):
                        self.inventory[index].item.use()
        return 'no turn'

    def get_target_tile(self,max_range=None):
        while True:
            libtcod.console_flush()
            libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE,self.key,self.mouse)
            self.render_all()

            (x,y) = (self.mouse.cx,self.mouse.cy)

            if(self.mouse.lbutton_pressed and self.level.is_in_fov(x,y) and (max_range is None or self.player.distance(x,y)<=max_range)):
                return (x,y)

            if(self.mouse.rbutton_pressed or self.key.vk==libtcod.KEY_ESCAPE):
                return(None,None)
    
    def render_all(self):
        if(self.fov_recompute):
            self.fov_recompute = False
            
            libtcod.map_compute_fov(self.level.fov_map, self.player.x, self.player.y, Constants.TORCH_RADIUS, Constants.FOV_LIGHT_WALLS, Constants.FOV_ALGO)
            
        for y in range(Constants.MAP_HEIGHT):
            for x in range(Constants.MAP_WIDTH):
                wall = self.level.map[x][y].block_sight
                visible = self.level.is_in_fov(x,y)
                if not visible:
                    if self.level.map[x][y].explored:
                        if(wall):
                            libtcod.console_put_char_ex(self.map_console,x,y,'#',libtcod.white,Constants.COLOR_DARK_WALL)
                        else:
                            libtcod.console_put_char_ex(self.map_console,x,y,'.',libtcod.white,Constants.COLOR_DARK_GROUND)
                else:
                    self.level.map[x][y].explored = True
                    if(wall):
                        libtcod.console_put_char_ex(self.map_console,x,y,'#',libtcod.white,Constants.COLOR_LIGHT_WALL)
                    else:
                        libtcod.console_put_char_ex(self.map_console,x,y,'.',libtcod.white,Constants.COLOR_LIGHT_GROUND)
        
        for object in self.level.objects:
            object.draw(self.level.fov_map)
        
        #Stats
        #libtcod.console_set_default_foreground(self.map_console,libtcod.white)
        #libtcod.console_print_ex(self.map_console,1,Constants.SCREEN_HEIGHT-2,libtcod.BKGND_NONE,libtcod.LEFT,'HP: '+str(self.player.fighter.hp) + '/' + str(self.player.fighter.max_hp)+' ')
        
        libtcod.console_blit(self.map_console,0,0,Constants.MAP_WIDTH,Constants.MAP_HEIGHT,0,0,0)
                
        self.UI.update()

    
    def main_loop(self):
        while not libtcod.console_is_window_closed():
            libtcod.console_set_default_foreground(self.map_console,libtcod.white)
            
            libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE,self.key,self.mouse)
            
            self.render_all()
            libtcod.console_flush()

            for object in self.level.objects:
                object.clear()
            
            self.player_action = self.handle_keys()

            if(self.player_action=='exit'):
                break

            if(self.game_state=='playing' and self.player_action!='no turn'):
                for object in self.level.objects:
                    if object != self.player:
                        if object.ai:
                            object.ai.take_turn()