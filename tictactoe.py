#https://numpydoc.readthedocs.io/en/latest/format.html#documenting-classes
#https://google.github.io/styleguide/pyguide.html


import board
import player

player_one = None
player_two = None
player_two_computer = False
player_one_char = 'X'
player_two_char = 'O'


if __name__ == '__main__':
    user_input = 0 #!int(input("Player two computer? 0=false 1=true:\n"))

    correct_input = False

    # Makes sure userInput is a viable number
    while(correct_input is False):
        if user_input != 0 and user_input != 1:
            user_input = int(input('Please enter a 0 or a 1. 0=false 1=true:\n'))
        else:
            player_two_computer = bool(user_input)
            break

    board = board.Board()
    
    #? Allow player 1 to be computer?
    #Sets up player 1 as a normal player, defaults to X as it's char
    PlayerOne = player.Player(player_one_char)

    # Sets up player 2 as either a computer or normal player
    '''
    if playerTwoComputer:
        playerTwo = player.Player(playerTwoChar, playerTwoComputer)
    else:
        playerTwo = player.Player(playerTwoChar)
    '''
    
    # Example board for print testing:
    board.board_one = 0b001001101
    board.board_two = 0b100010010

    board.print_board()
