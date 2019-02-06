import random
from source.utils import show, clear
from source.lists import getRandomEnemyName, getRandomAttackVerb
from source.enemy import *
from source.combatUI import *
from source.item import tryForDrop, generateRandomArmourOrWeapon
#  TODO: consult other adventure games to see what a good attack:HP ratio is

class Combat:
    def __init__(self, player, biome=None, alert=True, enemy=None, enemyToughness=0 ,startCombatNow=True):
        self.player = player
        self.biome = biome
        self.result = None # win, escaped, lose
        if not enemy == None: # if giving enemy
            self.enemy = enemy
        else: 
            self.enemy = Enemy(player,biome, toughness=enemyToughness) # make random enemy with given biome
        self.dropchance = 0 # TODO drops
        if alert: self.alert()
        if startCombatNow: self.startCombat()

        # TODO: May later be affected by level as well as biome

    def alert(self):
        # map.getTileDescription prints something about where you are.
        s = ''
        s += "From over your shoulder you notice " # TODO flavor
        s += self.enemy.name
        s += " attempting to " # TODO flavor text about realizing your're being attacked
        attack = getRandomAttackVerb() 
        if attack[-1] == "*": # if attack finishes the sentence
            s += attack[:-1] # remove *
        else :
            s += attack
            s += " you!"
        printc(s)
        show("@You're being attacked!@red@") 

    def startCombat(self, GivenCombatUI=None):
        if GivenCombatUI==None: c = CombatUI(self.player, self.enemy)
        else: c = GivenCombatUI
        c.run()
        self.result = c.result
        clear()
        if c.result == "win":
            show("You defeated " + self.enemy.name + "!")
            self.player.gainXp(self.enemy.xpworth, scale=False) # xp already scales when creating enemy
            self.player.regenHealth()# gain health
            if tryForDrop(25): 
                show("You got some loot!")
                self.getLoot()
        elif c.result == "lose":
            self.player.death()
        elif c.result == "escaped":
            show("You escaped from " + self.enemy.name + "! That was a close one!")
        elif c.result == 'inventory':
            self.player.openInventory()
            self.startCombat(c)
        return

    def getLoot(self):
        bonus = self.enemy.toughness
        self.player.addToInventory(generateRandomArmourOrWeapon(self.player, bonus=bonus))
        


        
        
