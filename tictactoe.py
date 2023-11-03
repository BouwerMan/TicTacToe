#https://numpydoc.readthedocs.io/en/latest/format.html#documenting-classes

import board
import player

playerOne = None
playerTwo = None
playerTwoComputer = False
playerOneChar = 'X'
playerTwoChar = 'O'


if __name__ == '__main__':
    userInput = 0 #!int(input("Player two computer? 0=false 1=true:\n"))

    correctInput = False

    # Makes sure userInput is a viable number
    while(correctInput == False):
        if userInput != 0 and userInput != 1:
            userInput = int(input("Please enter a 0 or a 1. 0=false 1=true:\n"))
        else:
            playerTwoComputer = bool(userInput)
            break

    board = board.Board()
    
    #? Allow player 1 to be computer?
    #Sets up player 1 as a normal player, defaults to X as it's char
    PlayerOne = player.Player(playerOneChar)

    # Sets up player 2 as either a computer or normal player
    if playerTwoComputer:
        playerTwo = player.Player(playerTwoChar, playerTwoComputer)
    else:
        playerTwo = player.Player(playerTwoChar)

    # Example board for print testing:
    board.boardOne = 0b001001101
    board.boardTwo = 0b100010000

    board.printBoard()