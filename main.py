from Game import Game
import libtcodpy as libtcod
from Menu import Menu
from Constants import Constants
import sys

##TODO Create Player Class


def intro():
    return

def msgbox(screen,message,width=50):
    m = Menu(screen,message,[],width)
    m.show()

def main_menu():
    img = libtcod.image_load("menu_background1.png")
    
    while not libtcod.console_is_window_closed():
        screen = libtcod.console_new(Constants.SCREEN_WIDTH,Constants.SCREEN_HEIGHT)
        libtcod.image_blit_2x(img,0,0,0)
        mmenu = Menu(screen,'',['New Game','Load Game','Quit'],24)

        #Title and Credits
        libtcod.console_set_default_foreground(0, libtcod.light_yellow)
        libtcod.console_print_ex(0, int(Constants.SCREEN_WIDTH/2), int(Constants.SCREEN_HEIGHT/2-4), libtcod.BKGND_NONE, libtcod.CENTER,
            'Into the Unknown')
        libtcod.console_print_ex(0, int(Constants.SCREEN_WIDTH/2), int(Constants.SCREEN_HEIGHT-2), libtcod.BKGND_NONE, libtcod.CENTER,
            'by badagent')

        choice = mmenu.show()

        if choice==0:
            game = Game()
            game.message("Welcome to the lands of Doom! Be prepared to find a heroic end and die for a greater cause.",libtcod.red)      
            game.main_loop()
        if choice==1:
            worked=True
            game = Game()
            try:
                game.load_game()
            except:
                msgbox(screen,"\nNo saved Game.\n",24)
                worked=False
            if(worked):
                game.main_loop()
            
        if choice==2:
            libtcod.console_set_fullscreen(False)
            if(game!=None):
                game.save_game()
            sys.exit(0)


libtcod.console_set_custom_font('arial10x10.png',libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(Constants.SCREEN_WIDTH,Constants.SCREEN_HEIGHT,'Tutorial',False)
libtcod.sys_set_fps(Constants.LIMIT_FPS)

main_menu()

