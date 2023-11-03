import board

player2Computer = False

if __name__ == '__main__':
    userInput = int(input("Player two computer? 0=false 1=true"))

    correctInput = False

    while(correctInput == False):
        if userInput != 0 and userInput != 1:
            userInput = int(input("Please enter a 0 or a 1. 0=false 1=true"))
        else:
            break