"""Tic-Tac-Toe Console Game

I created this for my final project in COSC-1436.
Gameplay is simple, simply call ./tictactoe.py and follow the instructions on screen.

Unless I changed my mind, I probably submitted a single python script for ease of running.
If that is the case, I highly recommend looking at the code in github since the combined files is over 800 lines of code.

https://github.com/BouwerMan/TicTacToe

It is the same code, just split into different modules for readability.

I will note, I know I have over engineered this code. I got kind of carried away I guess.
"""
#https://numpydoc.readthedocs.io/en/latest/format.html#documenting-classes
#https://google.github.io/styleguide/pyguide.html

from src.game import Game
from src.player import Player
from src.computer import Computer

player_one = None
player_two = None
EXIT_OPTIONS = ['Quit', 'quit', 'q', 'Q', 'exit']
DEFAULT_COMPUTER_LEVEL = 8
turn_player = 0

# Dang that's a long function name
def get_player_two_computer_input() -> bool:
    """Asks user if player two should be a computer. Input validity is checked.

    Returns:
        bool: User's response. Defaults to True if input is invalid
    """

    try:
        is_player_two_computer = bool(int(input('Is player two a computer? 0=false 1=true (default=1): ')))
    except ValueError:
        print('Invalid input. Defaulting to 1 (Computer).')
        is_player_two_computer = True
    return is_player_two_computer

def get_computer_level() -> int:
    """Asks user what level should the computer be. Input validity is checked.
    Input validation alerts the user when it fails and sets the level to a default.

    Returns:
        int: User's response. Defaults to 8 if input is invalid.
                If input is out of range then it defaults to the nearest
                number within expected range.
    """
    try:
        level = int(input('Enter a computer level from 0-8 (0=easiest, 8=impossible, default=8): '))
        if level > 8:
            level = 8
            raise IndexError('Computer level out of bounds, closest is 8')
        
        elif level < 0:
            level = 0
            raise IndexError('Computer level out of bounds, closest is 0')
        
    except ValueError:
        level = DEFAULT_COMPUTER_LEVEL
        print('Invalid input. Defaulting to 8')
    except IndexError as err:
        level = DEFAULT_COMPUTER_LEVEL
        print(err)
        print(f'Computer level set to {level}')
    
    return level

if __name__ == '__main__':

    player_one = Player(1)
    
    if get_player_two_computer_input():    
        computer_level = get_computer_level()
        player_two = Computer(2, computer_level)
    else:
        player_two = Player(2)
        
    players = [player_one, player_two]
    board = Game()
    
    while True:
        if isinstance(players[turn_player], Computer):
            move = players[turn_player].create_move(board)
            print('Computer has generated it\'s move:')
        else:
            board.print_board()
            move_raw = input(f'{players[turn_player]} Select your square: ')
            if move_raw in EXIT_OPTIONS:
                break
            try:
                move = board.parse_input(move_raw, board.player)
            except ValueError:
                print('Invalid move. Please select an empty square.')
                continue
                
            
        board_status = board.move(move)
        if not board_status:
            print('Invalid move. Please select an empty square.')
            continue
        
        # Checks for win condition and handles result
        # Not using a switch statement here because zylabs is running python 3.8
        winner = board.is_winner()
        if winner == 1:
            board.print_board() 
            print('Player 1 Won!')
            break
        elif winner == 2:
            board.print_board() 
            print('Player 2 Won!')
            break
        elif winner == 3:
            board.print_board() 
            print('Tie!')
            break

        # Incrementing player whose turn it is
        turn_player ^= 1
        board.player = turn_player + 1
