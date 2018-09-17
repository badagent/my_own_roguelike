from Constants import Constants
import libtcodpy as libtcod
from objects.Ai import *

def cast_fireball(item):
    player = item.game.player
    game = item.game
    game.message("Left click a target for the fireball. Right click to cancel.",libtcod.light_cyan)
    (x,y) = game.get_target_tile()
    if x is None:
        return 'cancelled'
    game.message('The fireball explodes, burning everything withing ' + str(Constants.FIREBALL_RADIUS) +" tiles.",libtcod.orange)

    for object in game.level.objects:
        if object.distance(x,y) <= Constants.FIREBALL_RADIUS and object.fighter:
            game.message("The " + object.name + " gets burned for " + str(Constants.FIREBALL_DAMAGE) + " hitpoints.",libtcod.orange)
            object.fighter.take_damage(Constants.FIREBALL_DAMAGE)

def heal_player(item):
    player = item.game.player
    game = item.game
    if(player.fighter.hp==player.fighter.max_hp):
        game.message("You already have full hp.",libtcod.red)
        return 'cancelled'
    else:
        game.message("You feel better.",libtcod.light_violet)
        player.fighter.heal(Constants.HEAL_AMOUNT)


def cast_lightning(item):
    player = item.game.player
    game = item.game
    monster = player.fighter.closest_monster(Constants.LIGHNING_RANGE)
    if monster is None:
        game.message("No monster is close enough.",libtcod.red)
        return 'cancelled'
    game.message("A lighning bold strikes " + monster.name + " with a loud thunder. The damage is " + str(Constants.LIGHNING_DAMAGE) + " hit points!",libtcod.light_blue)
    monster.fighter.take_damage(Constants.LIGHNING_DAMAGE)

def cast_confuse(item):
    player = item.game.player
    game = item.game
    monster = player.fighter.closest_monster(Constants.CONFUSE_RANGE)
    if monster is None:
        game.message("No monster is close enough.",libtcod.red)
        return 'cancelled'
    old_ai = monster.ai
    monster.ai = ConfusedMonster(old_ai)
    monster.ai.owner = monster
    game.message("The " + monster.name + " is confused and starts stumbling around aimlessly.",libtcod.light_green)


class Item:

    def __init__(self,use_function=None):
        self.use_function = use_function
    
    def use(self):
        item = self.owner
        if(self.use_function is None):
            item.message("The " + item.name + " cannot be used.",)
        else:
            if(self.use_function(item)!='cancelled'):
                item.game.inventory.remove(item)


    def pick_up(self):
        item = self.owner
        inventory = self.owner.level.game.inventory
        if(len(inventory)>Constants.MAX_ITEMS_IN_INVENTORY):
            item.message("Your inventory is full. Can not pick up " + item.name + ".",libtcod.red)
        else:
            inventory.append(item)
            item.level.objects.remove(item)
            item.message("You picked up a " + item.name +".",libtcod.green)

