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
computer_level = 8
turn_player = 0


if __name__ == '__main__':

    # Asks user if player 2 is computer
    try:
        player_two_computer = bool(int(input('Is player two a computer? 0=false 1=true (default=1): ')))
    except ValueError:
        print('Invalid input. Defaulting to 1 (Computer).')
        player_two_computer = True

    player_one = Player(player_one_char, 1)
    if player_two_computer:
        # Gets computer level then creates player_two
        try:
            computer_level = int(input('Enter a computer level from 0-8 (0=easiest, 8=impossible, default=8): '))
            if computer_level > 8:
                computer_level = 8
                raise IndexError('Computer level out of bounds, closest is 8')
            
            elif computer_level < 0:
                computer_level = 0
                raise IndexError('Computer level out of bounds, closest is 0')
            
        except ValueError:
            print('Invalid input. Defaulting to 8')
        except IndexError as err:
            print(err)
            print(f'Computer level set to {computer_level}')
        player_two = Computer(player_two_char, 2, computer_level)
        
    else:
        player_two = Player(player_two_char, 2)
        
    players = [player_one, player_two]
    board = Game(player_one, player_two)
    
    while True:
        
        if isinstance(players[turn_player], Computer):
            move = players[turn_player].create_move(board)
            # TODO: Reverse parse?
            print(f'Computer move is {(move>>board.board_bitlen):#011b}:')
        else:
            board.print_board()
            move_raw = input(f'{players[turn_player]} Select your square: ')
            if move_raw in exit_options:
                break
            try:
                move = board.parse_input(move_raw, board.player)
            except ValueError:
                print('Invalid move. Please select an empty square.')
                continue
                
            
        board_status = board.move(move)
        if board_status == -1:
            print('Invalid move. Please select an empty square.')
            continue
        
        turn_player ^= 1
        board.player = turn_player + 1
        
        # Checks for win condition and handles result
        match board.is_winner():
            case 0b01:
                board.print_board() 
                print('Player 1 Won!')
                break
            case 0b10:
                board.print_board() 
                print('Player 2 Won!')
                break
            case 0b11:
                board.print_board() 
                print('Tie!')
                break
            case _:
                pass
    
    output = format(board._board_state, '#034b')
    print(output)
