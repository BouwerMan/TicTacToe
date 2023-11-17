#https://numpydoc.readthedocs.io/en/latest/format.html#documenting-classes
#https://google.github.io/styleguide/pyguide.html

###############
# MASTER TODO #
###############
# TODO: Switch to one number for gamestate (both boards, winning player, active player, etc)
# TODO: Document classes and modules
# TODO: consolidate how we access and change data in regards to the game state


# TODO: Do better directory stuff
from game import Game
from player import Player
from computer import Computer

player_one = None
player_two = None
player_two_computer = False
player_one_char = 'X'
player_two_char = 'O'
exit_options = ['Quit', 'quit', 'q', 'Q', 'exit']
computer_level = 7


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
    #player_two = Player(player_two_char, 1)
    player_two = Computer(player_two_char, 1, computer_level)
    players = [player_one, player_two]
    board = Game(player_one, player_two)
    #!TEMP
    player_two.game = board
    
    turn_player = 0
    while True:
        
        # Checks for win condition and handles result
        win_player = board.check_for_win()
        if win_player == player_one:
            print('Player 1 Won!')
            break
        elif win_player == player_two:
            print('Player 2 Won!')
            break
        elif (board.board_one | board.board_two) == 0x1FF:
            print("Tie!")
            break
        
        if isinstance(players[turn_player], Computer):
            move = players[turn_player].create_move()
            # TODO: Reverse parse?
            print(f'Computer move is {move:#011b}:')
        else:
            board.print_board()
            move_raw = input(f'{players[turn_player]} Select your square: ')
            if move_raw in exit_options:
                break
            move = board.parse_input(move_raw)
            
        board_status = board.move(move)
        if board_status == -1:
            print("Invalid move. Please select an empty square.")
            continue
        
        turn_player ^= 1
