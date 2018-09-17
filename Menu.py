from Constants import Constants
import libtcodpy as libtcod
class Menu:
    def __init__(self,panel,header,options,width):
        if(len(options)>26):
            raise ValueError("Cannot have more than 26 options in Menu!")
        self.header = header
        self.options = options
        self.width = width
        self.panel = panel
        self.header_height = libtcod.console_get_height_rect(self.panel,0,0,self.width,Constants.SCREEN_HEIGHT,header)
        if(header==''):
            self.height = len(options)
        else:
            self.height = self.header_height+len(options)
        

        self.window = libtcod.console_new(self.width,self.height)
        
        libtcod.console_set_default_foreground(self.window,libtcod.white) 
        libtcod.console_print_rect_ex(self.window,0,0,self.width,self.height,libtcod.BKGND_NONE,libtcod.LEFT,self.header)

        

        y = self.header_height
        if(self.header==''):
            y=0
        letter = ord('a')
        for opt in options:
            text = '('+chr(letter)+') ' + opt
            libtcod.console_print_ex(self.window,0,y,libtcod.BKGND_NONE,libtcod.LEFT,text)
            y+=1
            letter+=1
        
    
    def show(self):
        x = Constants.SCREEN_WIDTH/2 - self.width/2
        y = Constants.SCREEN_HEIGHT/2 - self.height/2

        libtcod.console_blit(self.window,0,0,self.width,self.height,0,int(x),int(y),1.0,0.7)

        
        
        libtcod.console_flush()
        
        key = libtcod.console_wait_for_keypress(True)
        if key.vk == libtcod.KEY_ENTER and key.lalt:  #(special case) Alt+Enter: toggle fullscreen
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
        index = key.c-ord('a')
        if index >= 0 and index < len(self.options): return index
        return None
        