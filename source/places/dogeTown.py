from source.utils import show, input
from source.lists import getInvalidOptionText

#TODO QUEST get information from dogetown (but its funny because they only say bark)
# TODO the rest of this
def dogeTown(player):
    if player.getVisits("dogeTown", "add") == 1 :
        show("As you ou approach what seems to be a town completely inhabited by polite and playful doggos.")
        show("It's magnificent. You have never seen anything like it. There are puggos and long boys and shoobos and wrinklers... All types of doge boys run about playing fetch and chase through the streets and in the open fields around the town.")
        show("Yappers are yipping from rooftops and floofers woof from below.")
        show("A smol baby doge pupper runs by you at hecking fast speeds and zooms through a doggie door.")
        show("You continue to a marble staircase and begin to climb.")
        show("Marveling at the beautiful architecture, you wonder how such a place has been only 5 distances away from your home town all this time.")
        show("You reach the top of the staircase and are halted by 2 shoobers armed with spears crossed to block your path.")
        show("Another doggo approaches. This doge, a shibe, greets you with the grandeur of a king. He is surely the doggest. ")
        show('"Bork."')
        x = input(player)
        show('"Woof bork!"')
        x = input(player)
        show('"Yip yip bark boof woof, bork yip bark boof?"')
        x = input(player)
        show("The doge nods his head to the shoober soliders and they uncross their spears. It seems that thanks to your cunning choice of words you have been granted access into Dogetown.")
        
        
        
        # gabe

    while True:
        show("Around you are a few buildings with doors large enough for you to enter.")
        show("There is one called 'party' puppo's puppy palace.")
        show("Another is 'Bony's Convenience Store.")
        show("On your left rests a towering structure that looks like a 'church'. You hear howling from inside. ")
        show("There is also a path to what looks to be the 'king's quarters.")
        show("Or you can 'leave'.")
        x = input(player)
        if (x == "party" or x == "p"):
# sub woofer
            
        elif (x == "bony" or x == "b" or x == "bony's"):
            # TODO shop
            # treat, healing item
            # 
            
        elif (x == "king" or x == "k" or x == "king's"):


        elif (x == "king" or x == "k" or x == "king's"):
            show("The church has massive stained glass windows of grand grizlords, slippery tube dudes, and big scary teeth doggos. ")
            show("Though threatened by the colossal artistry, you open the mighty door and enter.")

        elif (x == "leave" or x == "l"):
            show("Because you are insane, you decide to leave Dogetown. After all, the rest of the world can't be that much worse.")
            show("Can it?")
            break
        else:
            print(getInvalidOptionText())


