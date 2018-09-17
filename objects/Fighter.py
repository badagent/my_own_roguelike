import libtcodpy as libtcod

def player_death(player):
    player.level.game.game_state = "dead"
    player.char = '%'
    player.color = libtcod.dark_red
    player.message("You Died!")

def monster_death(monster):
    monster.char = '%'
    monster.message(monster.name.capitalize() + " is dead!")
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = "Remains of " + monster.name
    monster.level.send_to_back(monster)

class Fighter:
    def __init__(self,hp,defense,power,death_function = None):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.death_function = death_function
        self.power = power

    def take_damage(self,damage):
        if damage > 0:
            self.hp -= damage
        if(self.hp<=0):
            function = self.death_function
            if(function is not None):
                function(self.owner)
    
    def closest_monster(self,max_distance):
        
        closest_enemy = None
        closest_dist = max_distance+1
        for object in self.owner.level.objects:
            if(object.fighter and object != self.owner and self.owner.game.level.is_in_fov(object.x,object.y)):
                dist = self.owner.distance_to(object)
                if(dist<closest_dist):
                    closest_enemy=object
                    closest_dist=dist
        return closest_enemy

    def heal(self,amount):
        self.hp += amount
        if(self.hp>self.max_hp):
            self.hp = self.max_hp

    def attack(self,target):
        damage = self.power - target.fighter.defense

        if damage > 0:
            self.owner.message(self.owner.name.capitalize() + ' attacks ' + target.name + ' for ' + str(damage) + ' hit points')
            target.fighter.take_damage(damage)
        else:
            self.owner.message(self.owner.name.capitalize() + ' attacks ' + target.name + ' but there is no damage')

