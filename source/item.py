
# generates items
import random
from source.lists import getRandomWeaponName, getRandomItemPrefix, getRandomArmourSlot, getRandomArmourName, getRandomConsumableName

class Item():
    def __init__(self, player, name, customDescription='', rarity = None, _type=None, armourSlot = None, damage=0, block=0, sellValue = None,  consumable=None, scale=True):
        '''
        Rarities: None, common, rare, epic, legendary
        Types: weapon, armour, consumable, quest, misc
        ArmourSlots: head, offhand, chest, legs, feet
        Set sellValue to None to generate a default value, or 0 if unable to be sold
        consumable is False or a Consumable object
        if scale as true, stats will be scaled to fit player level
        '''
        self.player = player
        self.name = name
        self.rarity = rarity 
        self.type = _type    
        self.damage = damage
        self.block = block
        self.equipped = False
        self.consumable = consumable
        self.customDescription = customDescription

        if self.type == 'armour': self.armourSlot = armourSlot
        else: self.armourSlot = None

        if sellValue == None: self.sellValue = self.generateSellValue() 
        else: self.sellValue = sellValue

        if scale: self.scale()

        self.description = self.buildItemDescriptionString()

    def getName(self):
        '''changes return value if item is equipped'''
        if self.equipped:
            return self.name + ' (equipped)'
        else:
            return self.name
        
    def toggleEquipped(self):
        if not self.equipped:
            self.equipped = True
        else:
            self.equipped = False
        self.description = self.buildItemDescriptionString()
        
    def generateSellValue(self):
        mult =1
        if self.rarity == None: mult =1
        elif self.rarity == 'rare': mult =2
        elif self.rarity == 'epic': mult =3
        elif self.rarity == 'legendary': mult =4
        return int( random.randint(1+self.player.level,1+self.player.level * 2) * mult ) # SCALING

    def buildItemDescriptionString(self): # used in UIs
        s = ''
        if not self.rarity == None: # if has a rarity
            s += ' [' + self.rarity.capitalize() + '] ' + '\n'
        elif self.type == 'weapon' or self.type == 'armour': # if doesnt have rarity and is a weapon or armour
            s += ' [Common] ' + '\n'
        if self.sellValue > 0:
            s += 'Value: $' + str(self.sellValue) +  '\n'
        if self.damage > 0:
            s += 'Damage: ' + str(self.damage) + '\n'
        if self.block > 0:
            s += 'Block:  ' + str(self.block) + '\n'
        if not self.customDescription == "" and not self.customDescription == None:
            s += "\n" + self.customDescription
        if self.equipped: s += '\n' + "You're " + self.whereIsIt()
        elif self.type == 'weapon' or self.type =='armour': s+= '\n' + self.whereDoesItGo()
        return s.strip()
        # TODO: flavorize

    def whereIsIt(self):
        if not 'hand' in self.player.aspect: hand = 'right'
        else: hand = self.player.aspect["hand"]
        if hand == 'right': otherhand='left'
        else: otherhand='right'
        if self.type ==  "weapon":
            return "holding this in your " + hand + " hand."
        elif self.armourSlot == "head":
            return "wearing this on your head."
        elif self.armourSlot == "chest":
            return "wearing this."
        elif self.armourSlot == "feet" or self.armourSlot == "legs":
            return "wearing these."
        elif self.armourSlot == "offhand":
            return "holding this in your " + otherhand + " hand."

    def whereDoesItGo(self):
        if not 'hand' in self.player.aspect: hand = 'right'
        else: hand = self.player.aspect["hand"]
        if hand == 'right': otherhand='left'
        else: otherhand='right'
        if self.type ==   "weapon":
            return "This goes in your " + hand + " hand"
        elif self.armourSlot == "head":
            return "This goes on your head."
        elif self.armourSlot == "chest":
            return "This goes on your chest."
        elif self.armourSlot == "legs":
            return "This goes on your legs."
        elif self.armourSlot == "feet":
            return 'This goes on your feet.'
        elif self.armourSlot == "offhand":
            return "This goes in your " + otherhand + " hand."
        return "You can't hold this."

    def scale(self): #SCALING
        '''change an items stats to scale with player level'''
        self.damage = self.player.scale(self.damage)
        self.block = self.player.scale(self.block)
        self.sellValue = self.sellValue + self.player.level # TODO not sure about this

def generateRandomArmourOrWeapon(player, _type='armour',rarity = None, armourSlot=None, bonus=0, extreme=False, customDescription='', prefix=True, scale=True): 
    ''' bonus makes the weapon a lot better (or worse if neg)
        bonus and rarity both add points for prefix'''
    if rarity == None:
        rarity = getRarityBasedOnNumber(bonus)
    if prefix == True: 
        prefix = generatePrefix(player, _type=_type ,prefixLevelOutOf5=bonus+2 + getNumberBasedOnRarity(rarity))
    if _type == 'armour':
        if armourSlot == None: armourSlot = getRandomArmourSlot()
        damage = 0
        block = prefix.blockMod
        name = prefix.adjective + " " + getRandomArmourName(armourSlot)
    else:
        _type = 'weapon'
        damage = prefix.damageMod
        block = 0
        name = prefix.adjective + " " + getRandomWeaponName(extreme) 
    i = Item(player, name, customDescription=customDescription, rarity=rarity, _type=_type, armourSlot = armourSlot, damage=damage, block=block, scale=scale)
    i.damage = int(i.damage) # round
    i.block = int(i.block)
    i.description = i.buildItemDescriptionString()
    return i

def getNumberBasedOnRarity(rarity):
    if rarity == None or rarity == 'common':
        return 0
    if rarity == 'rare':
        return 1
    if rarity == 'epic':
        return 2
    if rarity == 'legendary':
        return 3

def getRarityBasedOnNumber(number):
    number = int(number)
    if number == None or number <= 0 :
        return 'common'
    if number == 1 :
        return 'rare'
    if number == 2 :
        return 'epic'
    if number >= 3 :
        return 'legendary'


class ItemPrefix():
    def __init__(self, adjective, damageMod = 0, blockMod=0):
        self.adjective = adjective
        self.damageMod = damageMod
        self.blockMod = blockMod

def generatePrefix(player, _type='weapon', prefixLevelOutOf5 = 3):
    '''prefix level: 1 is shitty, 5 is really good'''
    i = ItemPrefix(getRandomItemPrefix(prefixLevelOutOf5))
    luckOfTheDraw = random.uniform(0,1)
    if _type == 'weapon':
        i.damageMod = prefixLevelOutOf5 + luckOfTheDraw
    elif _type == 'armour':
        i.blockMod = prefixLevelOutOf5 + luckOfTheDraw
    if i.damageMod<0: i.damageMod==0
    if i.blockMod<0: i.blockMod==0
    # TODO advanced combat make more special
    return i

def tryForDrop(percent): 
    dropchance = random.randint(1, 100)
    if dropchance <= percent:
        return True
    else:
        return False

class Consumable():
    def __init__ (self, player, consumableType='heal', consumeText=None, heal=0, xpgain=0, dealDamage=0, karma=0, scale=True):
        self.player =  player
        self.consumableType = consumableType
        self.consumeText=consumeText
        self.heal = heal
        self.xpgain = xpgain
        self.dealDamage = dealDamage
        self.karma=karma

        if scale: self.scaleConsumable()

    def scaleConsumable(self):
        aLittleBit = random.uniform(0, 1)
        if self.heal != 0: self.heal = self.player.scale(self.heal+aLittleBit)
        if self.xpgain != 0: self.xpgain = self.player.scale(self.xpgain+aLittleBit)
        if self.dealDamage != 0: self.dealDamage = self.player.scale(self.dealDamage+aLittleBit)

def consume(item): # for consuming consumables
    text=''
    if item.type=='consumable' and item.consumable != None:
        if item.consumable.consumeText == None:
            if item.consumable.consumableType == 'xp' or item.consumable.consumableType == 'heal': 
                text = checkForSpecialItems(item)
                if text == '':
                    text += "You ate the " + str(item.name) + ".\n It was delicious.\n"
        else:
            text += item.consumable.consumeText + '\n' 

        

        if item.consumable.dealDamage != 0:
            if item.player.inCombat == True:
                return item # this gets messy
            else:
                text += "There is no one to throw that at."
                return text

        if item.consumable.heal != 0:
            item.player.regenHealth(health = item.consumable.heal, returnString=True, showCurrentHealth=False)
            text += "You regained " + str(item.consumable.heal) + " HP!\n"

        if item.consumable.xpgain != 0:

            text += str(item.player.gainXp(item.consumable.xpgain, returnString=True)) + '\n' 

        if item.consumable.karma != 0:
            item.player.karma = item.player.karma + item.consumable.karma
            # if item.consumable.karma <0:
            #     text += 'You didn\'t feel too great about doing that.\n'
            # elif item.consumable.karma >0:
            #     text += "You're proud of yourself for doing that.\n"

        item.player.inventory.remove(item)
    else:
        text = "You can't use that!"
    return text

def checkForSpecialItems(item):
    name = item.name
    if name == 'beer' or name == 'Bottle of Vodka' or name == 'Jar of Moonshine':
        if player.aspect['age'] <21:
            return "You're not old enough to have that!\nYou throw it on the ground."
    return ""


def generateRandomConsumable(player, name = None, consumableType=None, customDescription='', consumable=None, powerLevel=0, returnItem=True):
    # returns an item of type consumable or just a consumable object if returnItem is false (in which case name and description are not used)
    # can pass a consumable object to add random effects to it (this functino wont change consume text or karma)
    # powerLevel can be negative, but values less than 3 can hurt you
    # consumable types: damage, heal, xp
    if consumable:
        c = consumable
    else:
        if consumableType == None:
            r = random.randint(1,3)
            if r == 1:
                consumableType = 'xp'
            elif r == 2:
                consumableType = 'heal'
            elif r == 3:
                consumableType = 'damage' 
        c = Consumable(player, consumableType)
    for i in range(powerLevel+1):
        aLittleBit = random.uniform(0, 1)
        if consumableType == 'heal':
            c.heal += player.scale(1+powerLevel+aLittleBit)
        elif consumableType == 'damage':
            c.dealDamage += player.scale(1+powerLevel+aLittleBit) # TODO advanced combat, SCALING
        elif consumableType == 'xp':
            c.xpgain += player.scale(1+powerLevel+aLittleBit)

    if name == None: 
        name = getRandomConsumableName(consumableType)     
    if returnItem:
        return Item(player, name, customDescription=customDescription, _type='consumable', consumable=c)
    else:
        return c
    
# TODO make it so you cant use damage consumables outside of comabt