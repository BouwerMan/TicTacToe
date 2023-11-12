#https://numpydoc.readthedocs.io/en/latest/format.html#documenting-classes
#https://google.github.io/styleguide/pyguide.html

# TODO: Do better directory stuff
from board import Board
from player import Player

player_one = None
player_two = None
player_two_computer = False
player_one_char = 'X'
player_two_char = 'O'
exit_options = ['Quit', 'quit', 'q', 'Q', 'exit']


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
    # TODO: Implement computers
    player_one = Player(player_one_char, 0)
    player_two = Player(player_two_char, 1)
    players = [player_one, player_two]
    board = Board(player_one, player_two)
    
    game = True
    turn_player = 0
    while game:
        board.print_board()
        move_raw = input(f'{players[turn_player]}Select your square: ')
        if move_raw in exit_options:
            break
        move_parsed = board.parse_input(move_raw)
        board_status = board.move(players[turn_player], move_parsed)
        if board_status == -1:
            print("Invalid move. Please select an empty square.")
            continue
        turn_player = not turn_player
        
    
    #? Allow player 1 to be computer?
    #Sets up player 1 as a normal player, defaults to X as it's char


    # Sets up player 2 as either a computer or normal player
    '''
    if playerTwoComputer:
        playerTwo = player.Player(playerTwoChar, playerTwoComputer)
    else:
        playerTwo = player.Player(playerTwoChar)
    '''
