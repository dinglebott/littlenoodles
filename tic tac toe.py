from time import sleep

#move functions
def xMove(coord):
    index = coordToIndex[coord]
    global board
    board = board[:index] + "X" + board[index + 1:]
    del coordToIndex[coord]
    xCoords.add(coord)

def oMove(coord):
    index = coordToIndex[coord]
    global board
    board = board[:index] + "O" + board[index + 1:]
    del coordToIndex[coord]
    oCoords.add(coord)

#game tree
tree = None
def tryWin(win, alt):
    global oCoords
    if win in oCoords:
        return alt
    else:
        return win

def treeLookup():
    global tree
    global oCoords

    if len(oCoords) == 0:
        return "A3"
    #1st round
    if oCoords == {"A2"}:
        tree = "1"
        return "C3"
    if oCoords == {"B3"}:
        tree = "1M"
        return "A1"
    if oCoords == {"A1"}:
        tree = "2"
        return "C1"
    if oCoords == {"C3"}:
        tree = "2M"
        return "C1"
    if oCoords == {"B1"}:
        tree = "3"
        return "C3"
    if oCoords == {"C2"}:
        tree = "3M"
        return "A1"
    if oCoords == {"C1"}:
        tree = "4"
        return "C3"
    if oCoords == {"B2"}:
        tree = "5"
        return "C1"
    #2nd round
    if tree == "1":
        if "B3" in oCoords:
            tree = "1W"
            return "C1"
        else:
            return "B3"
    if tree == "1M":
        if "A2" in oCoords:
            tree = "1MW"
            return "C1"
        else:
            return "A2"
    if tree == "2":
        if "B2" in oCoords:
            tree = "2W"
            return "C3"
        else:
            return "B2"
    if tree == "2M":
        if "B2" in oCoords:
            tree = "2MW"
            return "C3"
        else:
            return "B2"
    if tree == "3":
        if "B3" in oCoords:
            tree = "3W"
            return "B2"
        else:
            return "B3"
    if tree == "3M":
        if "A2" in oCoords:
            tree = "3MW"
            return "B2"
        else:
            return "A2"
    if tree == "4":
        if "B3" in oCoords:
            tree = "4W"
            return "A1"
        else:
            return "B3"
    if tree == "4M":
        if "A2" in oCoords:
            tree = "4MW"
            return "C3"
        else:
            return "A2"
    if tree == "5":
        if "A2" in oCoords:
            tree = "51"
            return "C2"
        if "B3" in oCoords:
            tree = "51M"
            return "B1"
        if "A1" in oCoords:
            tree = "52W"
            return "C3"
        if "C3" in oCoords:
            tree = "52MW"
            return "A1"
        if "B1" in oCoords:
            tree = "53"
            return "B3"
        if "C2" in oCoords:
            tree = "53M"
            return "A2"
    #3rd round
    if tree == "1W":
        return tryWin("B2", "C2")
    if tree == "1MW":
        return tryWin("B2", "B1")
    if tree == "2W":
        return tryWin("B3", "C2")
    if tree == "2MW":
        return tryWin("A2", "B1")
    if tree == "3W":
        return tryWin("A1", "C1")
    if tree == "3MW":
        return tryWin("C3", "C1")
    if tree == "4W":
        return tryWin("A2", "B2")
    if tree == "4MW":
        return tryWin("B3", "B2")
    if tree == "51":
        if "C3" in oCoords:
            tree = "51a"
            return "A1"
        else:
            return "C3"
    if tree == "51M":
        if "A1" in oCoords:
            tree = "51Ma"
            return "C3"
        else:
            return "A1"
    if tree == "52W":
        return tryWin("B3", "C2")
    if tree == "52MW":
        return tryWin("A2", "B1")
    if tree == "53":
        if "C3" in oCoords:
            tree = "53a"
            return "A1"
        else:
            return "C3"
    if tree == "53M":
        if "A1" in oCoords:
            tree = "53Ma"
            return "C3"
        else:
            return "A1"
    #4th round
    if tree == "51a":
        return tryWin("B1", "C2")
    if tree == "51Ma":
        return tryWin("C2", "B1")
    if tree == "53a":
        return tryWin("A2", "C2")
    if tree == "53Ma":
        return tryWin("B3", "B1")

#main loop
gameOngoing = True
wantsToPlay = True
print("Below is the tictactoe board. Give your move by typing the coordinates of the square you wish to place in e.g. A1, B2")
while wantsToPlay:
    #game setup
    board = " 1   2   3 \n   |   |   \n___|___|___   A\n   |   |   \n___|___|___   B\n   |   |   \n   |   |      C"
    winCons = ({"A1", "A2", "A3"}, {"B1", "B2", "B3"}, {"C1", "C2", "C3"}, {"A1", "B1", "C1"}, {"A2", "B2", "C2"}, {"A3", "B3", "C3"}, {"A1", "B2", "C3"}, {"A3", "B2", "C1"})
    xCoords = set()
    oCoords = set()
    coordToIndex = {
        "A1": 25,
        "A2": 29,
        "A3": 33,
        "B1": 53,
        "B2": 57,
        "B3": 61,
        "C1": 81,
        "C2": 85,
        "C3": 89,
    }
    print(board)
    input("Press Enter to begin.")

    while gameOngoing:
        #computer turn
        print("----------------------------------")
        print("Computer thinking...")
        xMove(treeLookup())
        sleep(0.8)
        print(board)
        #check for end
        for x in winCons:
            if x <= xCoords:
                print("X wins the game.")
                gameOngoing = False
                break
            elif x <= oCoords:
                print("O wins the game.")
                gameOngoing = False
                break
            elif len(coordToIndex) == 0:
                print("Game result: Draw")
                gameOngoing = False
                break
        if not gameOngoing:
            break
        #player turn
        while True:
            playerMove = input("Your turn: ").upper()
            if playerMove in coordToIndex:
                oMove(playerMove)
                break
            else:
                print("That's not a valid move.")
        print(board)
    
    #check play again
    while True:
        response = input("Do you want to play again? (Y/N) ").lower()
        if response == "y":
            print("----------------------------------")
            gameOngoing = True
            break
        elif response == "n":
            wantsToPlay = False
            break
        else:
            print("Type 'Y' or 'N' dummy.")