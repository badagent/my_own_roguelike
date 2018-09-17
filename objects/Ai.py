import libtcodpy as libtcod
from Constants import Constants
class BasicMonster:
    def take_turn(self):
        monster = self.owner
        if (self.owner.level.is_in_fov(monster.x,monster.y)):
            player = self.owner.level.game.player
            if monster.distance_to(player) >= 2:
                monster.move_towards(player.x,player.y)
            elif player.fighter.hp > 0:
                monster.fighter.attack(player)

class ConfusedMonster:
    def __init__(self,old_ai,num_turns=Constants.CONFUSE_NUM_TURNS):
        self.old_ai = old_ai
        self.num_turns = num_turns

    def take_turn(self):
        if(self.num_turns>0):
            self.owner.move(libtcod.random_get_int(0,-1,1),libtcod.random_get_int(0,-1,1))
            self.num_turns-=1
        else:
            self.owner.ai = self.old_ai
            self.owner.message("The " + self.owner.name + " is not confused anymore.",libtcod.red)

