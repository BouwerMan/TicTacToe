#https://numpydoc.readthedocs.io/en/latest/format.html#documenting-classes
#https://google.github.io/styleguide/pyguide.html

# TODO: Do better directory stuff
from board import Board
from player import Player
from computer import Computer

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
    #player_two = Player(player_two_char, 1)
    player_two = Computer(player_two_char, 1, 0)
    players = [player_one, player_two]
    board = Board(player_one, player_two)
    #!TEMP
    player_two.board = board
    
    turn_player = 0
    while True:
        board.print_board()
        win_player = board.check_for_win()
        if win_player:
            print(f'{win_player} Won!')
            break
        if isinstance(players[turn_player], Computer):
            move = players[turn_player].create_move()
            # TODO: Reverse parse?
            print(f'Computer move is {move:#011b}')
        else:
            move_raw = input(f'{players[turn_player]} Select your square: ')
            if move_raw in exit_options:
                break
            move = board.parse_input(move_raw)
            
        board_status = board.move(players[turn_player], move)
        if board_status == -1:
            print("Invalid move. Please select an empty square.")
            continue
        turn_player = ~turn_player
