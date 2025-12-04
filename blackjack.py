import random
import time
deck = []
print("Welcome to blackjack. Rules: can only hit or stand (no casino rules cos idk how to code that)")

#build Player class
class Player:
    def __init__(self, name):
        self.name = name
        self.cardTotal = 0
        self.cardsHeld = []
        self.aceCount = 0
        self.isMyTurn = False
    
    def drawCard(self):
        global deck
        cardId = deck[random.randrange(0, len(deck))]
        deck.remove(cardId)
        self.cardsHeld.append(cardId)
        #add card value to total
        match cardId % 13:
            case 2|3|4|5|6|7|8|9|10: #2-10
                self.cardTotal += cardId % 13
            case 11|12|0: #J, Q, K
                self.cardTotal += 10
            case 1: #Ace behaviour coded later
                self.cardTotal += 11
                self.aceCount += 1
    
    def showHand(self, message=""):
        print(self.name + "'s hand: ", end="")
        for x in self.cardsHeld:
            card = ""
            #find card face value
            match x % 13:
                case 2|3|4|5|6|7|8|9|10:
                    card += str(x % 13)
                case 11:
                    card += "J"
                case 12:
                    card += "Q"
                case 0:
                    card += "K"
                case 1:
                    card += "A"
            #find card suit
            if x <= 13:
                card += chr(9824) #spades
            elif x <= 26:
                card += chr(9825) #hearts
            elif x <= 39:
                card += chr(9827) #clubs
            else:
                card += chr(9826) #diamonds
            #print card
            print(card, end=" ")
        print(message) #for displaying round end results

#player action function
def getAction(thisPlayer):
    action = input("Would you like to hit or stand? ").lower()
    if action == "hit":
        print("Drawing a card...")
        thisPlayer.drawCard()
        time.sleep(1)
        thisPlayer.showHand()
    elif action == "stand":
        print("Ending turn...")
        thisPlayer.isMyTurn = False
        time.sleep(1)
    else:
        print("Type 'hit' or 'stand' dumbass.")
        getAction(thisPlayer)

#end of round function
def roundEnd():
    playAgain = input("Another round? (Y/N) ").lower()
    if playAgain == "y":
        pass
    elif playAgain == "n":
        global stillPlaying
        stillPlaying = False
    else:
        print("Type 'Y' or 'N' dumbass.")
        roundEnd()

#setup players
numOfPlayers = 0
playerList = []
def getPlayers():
    global numOfPlayers
    numOfPlayers = input("How many players? ")
    try:
        numOfPlayers = int(numOfPlayers)
    except:
        print("Enter a number dumbass...")
getPlayers()
for x in range(0, numOfPlayers):
    username = input(f"Enter your username, player no. {str(x+1)}: ")
    playerList.append(Player(username))
dealer = Player("Dealer")

#main loop
stillPlaying = True
while stillPlaying:
    #reset players
    for x in playerList:
        x.cardTotal = 0
        x.cardsHeld.clear()
        x.aceCount = 0
    dealer.cardTotal = 0
    dealer.cardsHeld.clear()
    #prepare deck
    print("Shuffling...")
    deck = [x for x in range(1, 53)]
    time.sleep(1)
    #deal cards
    print("Dealing...")
    for x in playerList:
        x.drawCard()
        x.drawCard()
    dealer.drawCard()
    dealer.drawCard()
    time.sleep(1)
    #round begins
    for x in playerList:
        x.isMyTurn = True
        x.showHand()
        while x.isMyTurn:
            getAction(x)
    #dealer plays
    print("Dealer playing...")
    while dealer.cardTotal < 16:
        dealer.drawCard()
    time.sleep(1)
    #update cardTotals for Aces
    for x in playerList:
        if x.aceCount == 2: #double Ace
            x.cardTotal = 21
        elif x.aceCount == 1:
            if (x.cardTotal > 21) or (len(x.cardsHeld) >= 3): #Ace = 10
                x.cardTotal -= 1
            if x.cardTotal > 21: #Ace = 1
                x.cardTotal -= 9
    #end of round
    print("Dealer done. Opening all hands...")
    time.sleep(1.5)
    dealer.showHand(f"({dealer.cardTotal})")
    for x in playerList:
        if x.cardTotal > 21:
            x.showHand(f"({x.cardTotal}: burst...)")
        elif x.cardTotal < 16:
            x.showHand(f"({x.cardTotal}: ??? disqualified)")
        elif (x.cardTotal == 21) and (len(x.cardsHeld) == 2):
            x.showHand("(BLACKJACK!!)")
        elif x.cardTotal == 21:
            x.showHand(f"({x.cardTotal}: Perfect!)")
        elif (x.cardTotal > dealer.cardTotal) or (dealer.cardTotal > 21):
            x.showHand(f"({x.cardTotal}: Win {chr(128522)})")
        elif (x.cardTotal < dealer.cardTotal) and (dealer.cardTotal <= 21):
            x.showHand(f"({x.cardTotal}: Lose {chr(128542)})")
        elif x.cardTotal == dealer.cardTotal:
            x.showHand(f"({x.cardTotal}: Draw)")
    #ask for another round
    roundEnd()

#outro music
print("Thank you for playing!")
input("Press Enter to exit.")