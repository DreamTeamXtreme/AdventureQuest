dogecoin = 1000
dankpoints = 0
perkpoints = 0
#dont include that ^

def slot_machine():
    global dogecoin
    print("You take a seat at this dank slot machine. ")
    play = raw_input("Give it a pull? Press P to play (Pay 10 Dogecoin), or leave. \n").lower().strip()
    if play == "p":
        slot_machine_play()
    else:
        print("You leave the chair.")
def slot_machine_play():
    global dogecoin, perkpoints, dankpoints
    if (dogecoin - 10) < 0:
        print("You don't even have enough money to play you filthy scrublord.")
        print("You leave the chair feeling sorrowed and out of swagger.")
        return

    dogecoin -= 10
    # 13.8% chance of winning
    import random
    tiles = ["(weed)", "(weed)", "(weed)", "(hitmarker)", "(hitmarker)", "(weed)", "(hitmarker)", "(Sample Text)", "(Sample Text)", "(Mountain Dew)", "(Sniper Rifle)", "(Doritos)"]
    a = random.randrange(0, 12)
    b = random.randrange(0, 12)
    c = random.randrange(0, 12)
    autowin = random.randrange(0, 30)
    if autowin == 0:
            a = random.randrange(1, 12)
            a = b = c
    # cheater
    # a=b=c= 0
    print ("(-10 Dogecoin) The rollers spin and land on \n")
    print tiles[a], " ", tiles[b], " ", tiles[c], "\n"
#winnings
    if tiles[a] == tiles[b] == tiles[c] == "(weed)":
        #1/24 chance means
        mult = random.randrange(1, 11)
        win = 40 + mult*2
        dogecoin += win
        print("Congratulations, you won %s Dogecoin.") %win
    elif tiles[a] == tiles[b] == tiles[c] == "(hitmarker)":
        #1/24 chance
        mult = random.randrange(1, 31)
        win = 20 + mult*2
        dogecoin += win
        print("Congratulations, you won %s Dogecoin.") %win
    elif tiles[a] == tiles[b] == tiles[c] == "(Sample Text)":
        #1/72 chance
        mult = random.randrange(1, 11)
        win = 1 + (mult**2) *2
        dogecoin += win
        print("Congratulations, you won %s Dogecoin.") %win
    elif tiles[a] == tiles[b] == tiles[c] == "(Mountain Dew)":
        #1/72 chance
        print("A small buzzer goes off. The lights flash and the machine chants, \"You are dank.\"")
        print("The machine starts to rumble and a steaming can of Mountain Dew falls out.")
        print("You have gained 420 dank points.")
        print(" ")
        dankpoints=+420
    elif tiles[a] == tiles[b] == tiles[c] == "(Sniper Rifle)":
        #1/72 chance
        print("The machine explodes and in the crater you find what you've needed all long. Its a ")
        #randomweapon() thing
    elif tiles[a] == tiles[b] == tiles[c] == "(Doritos)":
        #1/72 chance
        print("The machine rumbles and out comes a single Dorito chip.")
        print("You gently bite off a corner of the chip and place the rest in your pocket for later.")
        print("You have gained one Perk Point.")
        print(" ")
        perkpoints += 1
        # PerkPoint()
    print("Hit p to play again. (You have %s Dogecoin.)") % dogecoin
    again = raw_input("").lower().strip()
    if again == "p":
        slot_machine_play()
    else:
        print('You\'re getting pretty bored. "Maybe I should leave..." you think.')

slot_machine()
