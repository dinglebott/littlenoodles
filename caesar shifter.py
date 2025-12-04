#encoding func
def encodeChar(char, shiftBy):
    newAscii = ord(char.lower()) + shiftBy
    #check for wraparound (a-z: 97-122)
    if newAscii > 122:
        newAscii -= 26
    if newAscii < 97:
        newAscii += 26
    #check for uppercase
    if char.lower() == char:
        return chr(newAscii)
    else:
        return chr(newAscii).upper()

#initialise
print("This is a Caesar shift encoder")
stillEncoding = True
#main loop
while stillEncoding:
    #get input
    plaintext = input("Type your message to be encoded (NO NUMBERS): ")
    shift = int(input("Shift number: "))
    #process input
    output = ""
    keepList = [" ", ",", ".", "/", "?", "!", "'", "\"", "(", ")", ":", ";"]
    for x in plaintext:
        if x in keepList:
            output += x
        else:
            output += encodeChar(x, shift)
    #display output and await further
    print("Output: " + output)
    def checkForMore():
        response = input("Do you want to continue? (Y/N): ")
        if response.lower() == "y":
            pass
        elif response.lower() == "n":
            global stillEncoding
            stillEncoding = False
        else:
            print("Y or N only dumbass")
            checkForMore()
    checkForMore()

#outro music
print("Thanks for using my encoder :)")
input("Press Enter to exit.")