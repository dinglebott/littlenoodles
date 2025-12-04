import random
#create lists
fruits = ("apple", "banana", "kiwi", "strawberry", "watermelon", "grape", "mango", "lychee", "papaya", "orange", "grapefruit", "pineapple", "durian")
animals = ("snake", "cow", "sheep", "goat", "pig", "chicken", "lion", "tiger", "bear", "mouse", "horse", "dog", "cat", "rabbit", "deer")
letters = []
for x in range(97, 123):
    letters.append(chr(x))

#category selection
def pickCategory():
    global catChoice
    catChoice = input("Would you like to play animals or fruits? ").lower()
    if catChoice == "animals" or catChoice == "fruits":
        pass
    else:
        print("Type 'animals' or 'fruits' dumbass.")
        pickCategory()
pickCategory()

#initialise game
if catChoice == "animals":
    wordToGuess = tuple(animals[random.randint(0, 14)])
    print("An animal has been chosen.")
else:
    wordToGuess = tuple(fruits[random.randint(0, 12)])
    print("A fruit has been chosen.")

currentState = ["_" for x in wordToGuess]

#main loop
guessed = False
guessCount = 0
wrongCount = 0
while guessed == False:
    #display currentState
    for x in currentState:
        print(x, end=" ")
    #get guess
    def getGuess():
        global userGuess
        userGuess = input("Guess a letter: ").lower()
        if userGuess in letters:
            pass
        else:
            print("Type a letter dumbass...")
            getGuess()
    getGuess()
    guessCount += 1
    #check guess
    guessedRight = False    
    for i in range(len(wordToGuess)):
        if userGuess == wordToGuess[i]:
            currentState[i] = userGuess
            guessedRight = True
    if guessedRight == False:
        wrongCount += 1
    #check if word is guessed
    if "_" in currentState:
        pass
    else:
        guessed = True

#outro music
print("Congrats! The word was \"" + "".join(wordToGuess) + "\".")
print("You took " + str(guessCount) + " tries, and " + str(wrongCount) + f" of them {"was" if wrongCount == 1 else "were"} wrong.")
input("Press Enter to exit.")