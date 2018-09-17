import libtcodpy as libtcod
import textwrap
from Constants import Constants
class UI:
    def __init__(self,game,panel):
        self.game = game
        self.panel = panel
        self.messages = []
        self.shown_messages = []
    
    def render_bar(self,x,y,total_width,name,value,maximum,bar_color,back_color):
        bar_width = int(float(value)/maximum*total_width)
        #render Background
        libtcod.console_set_default_background(self.panel,back_color)
        libtcod.console_rect(self.panel,x,y,total_width,1,False,libtcod.BKGND_SCREEN)

        #Render bar
        libtcod.console_set_default_background(self.panel,bar_color)
        if(bar_width>0):
            libtcod.console_rect(self.panel,x,y,bar_width,1,False,libtcod.BKGND_SCREEN)

        libtcod.console_set_default_foreground(self.panel,libtcod.white)
        libtcod.console_print_ex(self.panel,int(x + total_width/2),y,libtcod.BKGND_NONE,libtcod.CENTER, name+": "+str(value)+"/"+str(maximum))

    def message(self,msg,color=libtcod.white):
        msg_lines = textwrap.wrap(msg,Constants.MESSAGE_WIDTH)
        for line in msg_lines:
            self.messages.append((line,color))
        

        
    def update(self):
        libtcod.console_set_default_background(self.panel,libtcod.black)
        libtcod.console_clear(self.panel)
        player = self.game.player
        self.render_bar(1,1,Constants.BAR_WIDTH,"HP",player.fighter.hp,player.fighter.max_hp,libtcod.red,libtcod.dark_red)
        
        libtcod.console_set_default_foreground(self.panel,libtcod.light_gray)
        libtcod.console_print_ex(self.panel,1,0,libtcod.BKGND_NONE,libtcod.LEFT,self.game.get_names_at_mouse_pos())

        y=1
        for (line,color) in self.messages[-Constants.MESSAGE_HEIGHT:]:
            libtcod.console_set_default_foreground(self.panel,color)
            libtcod.console_print_ex(self.panel,Constants.MESSAGE_X_POS,y,libtcod.BKGND_NONE,libtcod.LEFT,line)
            y+=1
        
        libtcod.console_blit(self.panel,0,0,Constants.SCREEN_WIDTH,Constants.PANEL_HEIGHT,0,0,Constants.SCREEN_HEIGHT-Constants.PANEL_HEIGHT)

    
    def menu(header,options,width):
        if(len(options)>26):
            raise ValueError("Cannot have more than 26 options in Menu!")
            
        

