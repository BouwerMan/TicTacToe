"""Tic-Tac-Toe Console Game

I created this for my final project in COSC-1436.
Gameplay is simple, simply call ./tictactoe.py and follow the instructions on screen.

Unless I changed my mind, I probably submitted a single python script for ease of running.
If that is the case, I highly recommend looking at the code in github since the combined files is over 800 lines of code.

https://github.com/BouwerMan/TicTacToe

It is the same code, just split into different modules for readability.

I will note, I know I have over engineered this code. I got kind of carried away I guess.
"""

import random
from timeit import default_timer as timer


# Some intial variables and constants used by main function (at the bottom)
player_one = None
player_two = None
EXIT_OPTIONS = ['Quit', 'quit', 'q', 'Q', 'exit']
DEFAULT_COMPUTER_LEVEL = 8
turn_player = 0




"""
Contains Game class and constants used by the Game class.
"""

# Constants
DEFAULT_BOARD_LIST = [['a1','a2','a3'],['b1','b2','b3'],['c1','c2','c3']]
BOARD_ROWS = 3
BOARD_COLUMNS = 3
BOARD_BITS = BOARD_ROWS * BOARD_COLUMNS
PLAYER_ONE_CHAR = 'X'
PLAYER_TWO_CHAR = 'O'    
WIN_CONDITIONS = [0b111, 0b111000, 0b111000000,
                    0b100100100, 0b010010010, 0b001001001,
                    0b100010001, 0b001010100]

# Constants for is_move_valid
BOARD_COLUMN_MAX = 3
BOARD_COLUMN_MIN = 1

# Constants for check_for_winner and is_winner
NEITHER_PLAYER_WIN = 0
TIE = 3

class Game:
    """Contains all information on board state
    as well as methods handling state changes.
    """

    def __init__(self):
        # Default board state, bit details under mask section
        # Bit 16 just separates board_one and board_two, always 1
        self._board_state =          0b10100000000000001000000000000000

        # Masks for state manipulation
        # 32nd bit is game state, 1=no winner, 0=winner/tie
        self.game_state_mask =       0b10000000000000000000000000000000
        # 30th and 31st bit is who the current player is, 0b01 = player 1, 0b10 = player two, 0b11 = tie
        self.player_one_mask =       0b00100000000000000000000000000000
        self.player_two_mask =       0b01000000000000000000000000000000
        self.players_mask =          0b01100000000000000000000000000000
        # Bits 0-9 represent board one (X), first 3 bits of that number is the top row
        #                                    second 3 bits is the middle row
        #                                    last 3 bits is the bottom row
        self.board_one_mask =        0b00000000000000000000000111111111
        # Bits 17-25 represent board two (O), bit order same as board one
        self.board_two_mask =        0b00000001111111110000000000000000
        
        # Just a mask for both boards, allowing for selection of only the move bits. 
                                   # 0b00000001111111110000000111111111
        self.boards_mask = self.board_one_mask | self.board_two_mask
        
        # Bit length of each board (even though only 9 are used)
        self.board_shift = 16
        
        # Bit of players, used to shift to the player bits properly
        self.player_shift = 29
        
        # Bit of game state, used to shift to the game state bits properly
        self.game_state_shift = 31
        
    # Public Methods
    
    @property
    def game_state(self) -> bool:
        """Get or set game state bit
        which indicates whether the game should continue.
        """
        # Returns 1 if game is on still, 0 if game has a winner
        state = self._board_state & self.game_state_mask
        return bool(state >> self.game_state_shift)
    
    @game_state.setter
    def game_state(self, state: bool):
        state_bit = int(not state)
        # Modifies the game state bit
        self._board_state ^= (state_bit << self.game_state_shift)
        
    @property
    def player(self) -> int:
        """Get or set player bits. Player bits are binary representation of player num (1 or 2).
        Setting the player bit takes in player num (1 or 2) and modifies the main bitboard accordingly.
        """
        # Returns the player number (1 or 2)
        player_bits = self._board_state & self.players_mask
        return player_bits >> self.player_shift
    
    @player.setter
    def player(self, player_num: int):
        # Sets the player bit
        
        # Effectively sets both player bits to 0 allowing for replacement
        player_bits = self._board_state & ~self.players_mask

        # Shifts player bits to left and uses mask to trim extra bits
        new_player = (player_num << self.player_shift) & self.players_mask

        self._board_state = player_bits | new_player
    
    @property
    def board_one(self) -> int:
        """Gets player one's board from the main bitboard."""
        return self.get_board_one(self._board_state)
        
    @property
    def board_two(self) -> int:
        """Gets player two's board from the main bitboard."""
        return self.get_board_two(self._board_state)
        
    @property
    def boards(self) -> int:
        """Gets player one and player two bits and ORs them together
        into one 9 bit int representing every played move.
        """
        return self.get_boards(self._board_state)
    
    def get_board_one(self, board: int) -> int:
        """Gets player one's board from the bitboard.

        Args:
            board (int): Bitboard to extract bits from.

        Returns:
            int: Player one's move bits.
        """
        return board & self.board_one_mask
    
    def get_board_two(self, board: int) -> int:
        """Gets player two's board from the bitboard.

        Args:
            board (int): Bitboard to extract bits from.

        Returns:
            int: Player two's move bits.
        """
        return (board & self.board_two_mask) >> self.board_shift
    
    def get_boards(self, board:int) -> int:
        """Gets player one and player two bits and ORs them together
        into one 9 bit int representing every played move.

        Args:
            board (int): Bitboard to extract bits from.

        Returns:
            int: Bits representing every played move.
        """
        board_one = self.get_board_one(board)
        board_two = self.get_board_two(board)
        return board_one | board_two
        
    def parse_input(self, move: str, player_num : int = 1) -> int:
        """Parses user input (EX: 'a1') and converts it to a binary representation.

        Args:
            move (str): Move input by player.
            player_num (int): Player number, 1 = player one, 2 = player two

        Raises:
            ValueError: Input is invalid (out of bounds).

        Returns:
            int: Binary representation of move (ex: 0b001000000)
                    shifted to correct bitboard position.
        """
        
        move_row_raw: str = move[0]
        move_col_raw: int = int(move[1])

        move_dict = {
            'column': -1,
            'row': -1
        }


        # Checks that move is within column bounds
        if move_col_raw > BOARD_COLUMN_MAX or move_col_raw < BOARD_COLUMN_MIN:
            raise ValueError('Move out of bounds')
        else:
            move_dict['column'] = move_col_raw

        try:
            move_dict['row'] = 'abc'.index(move_row_raw)
        except ValueError as err:
            raise ValueError('Move out of bounds') from err
        
        # Shifts a 1 to the proper column position
        # abs() so that we don't get a negative shift
        column = 1 << abs(move_dict['column'] - 3)
        # Shifts the 1 to the proper row position
        output_move = column << abs((3*(move_dict['row']-2)))
        
        shift = self.board_shift * (player_num - 1)
        
        return output_move << shift
    
    def move(self, move: int) -> bool:
        """
        Modifies main board state to record a move from a player.

        Args:
            move (int): Bitboard of move, expects data
                to be properly shifted based on the player number.

        Returns:
            bool: True if move was valid and successfully added.
                        False if move was invalid.
        """
        # TODO: Better status codes?
        # Returns -1 if move is not valid.
        if not self.is_move_valid(move):
            return False
        
        self._board_state += move
        
        # Indicates success
        return True
    
    def is_move_valid(self, move: int) -> bool:
        """
        Checks if move is valid for current board state.

        Args:
            move (int): Move made.

        Returns:
            bool: If move is valid or not.
        """
        
        is_move_in_bounds = (move & self.boards_mask) != 0
        was_move_played = (move & self.boards) == 0
        
        return was_move_played and is_move_in_bounds
    
    def check_for_win(self, board: int = None) -> int:
        """
        Checks if there was a winner. Does not modify board state.

        Args:
            board (int, optional): Board to check. Defaults to self's board state.

        Returns:
            int: Winning player. 0 = neither player, 3 = tie, or player number (1 or 2)
        """
        
        # Sets default boards to current game state
        if board is None:
            board = self._board_state

        boards = [
            self.get_board_one(board),
            self.get_board_two(board)
        ]
        
        # Iterates from board 1 to board 2
        for board_num in range(2):
            for win in range(len(WIN_CONDITIONS)):
                
                trimmed_board =  boards[board_num] & WIN_CONDITIONS[win]
                is_winner = trimmed_board == WIN_CONDITIONS[win]
                
                if is_winner:
                    winning_player = board_num + 1
                    return winning_player
        
        is_tie = boards[0] | boards[1] == 0x1FF
        if is_tie:
            return TIE
        
        return NEITHER_PLAYER_WIN
    
    def is_winner(self) -> int:
        """Checks if there is a winner. Also modifies board state accordingly.

        Returns:
            int: Winning player. 0 = neither player, 3 = tie, or player number (1 or 2)
        """

        winner = self.check_for_win()
        
        if winner == NEITHER_PLAYER_WIN:
            return winner
        
        # Sets _board_state correctly
        self.player = winner
        self.game_state = False
        
        return winner
        
    def print_board(self):
        """Prints main bitboard in a human readable format.
        Assumes that the board is 3x3. Can only print class instanced bitboard.
        """
        
        # Padding
        print()
        board_readable = self.__convert_from_bitboard()

        for index, row in enumerate(board_readable):
            # Prints each row and pads the items to make things uniform
            print(f'{row[0]:^5}|{row[1]:^5}|{row[2]:^5}')
            # Prints a dividing line between lines but not after the last line
            if index < 2:
                print('-------------------')
        
        # Padding
        print()
    
    # Private Methods
    
    def __convert_from_bitboard(self):
        """Converts bitboard to nested array to make printing easier.

        Returns:
            list[list[str]]: Nested array representation of the board state.
        """

        output_list = DEFAULT_BOARD_LIST
        
        board_one = self.board_one
        board_two = self.board_two

        for row_num, row in enumerate(output_list):
            player_one_bits = self.__get_player_bits(board_one, row_num)
            player_two_bits = self.__get_player_bits(board_two, row_num)

            # Adds player one char to row one where moves have been made
            for spot, bit in enumerate(player_one_bits):
                if bit:
                    row[spot] = PLAYER_ONE_CHAR

            # Adds player two char to row one where moves have been made
            for spot, bit in enumerate(player_two_bits):
                if bit:
                    row[spot] = PLAYER_TWO_CHAR
                    
        return output_list
    
    def __get_player_bits(self, board: int, row: int):
        """Creates a binary array from a row in a single board.

        Args:
            board (int): Board to convert. Is not a full bitboard, just one board's bits.
            row (int): Row to check.

        Returns:
            list[int]: Binary array representing player moves.
        """
        # Subtract 1 since arrays start at 0
        num_bits = BOARD_BITS - 1
        # Number of columns == how long each row needs to be
        row_length = BOARD_COLUMNS
        
        bit_range_start = num_bits - (row_length*row)
        bit_range_end = bit_range_start - row_length
        bit_range = range(bit_range_start, bit_range_end, -1)
        
        bits = []
        
        for bit in bit_range:
            bit_in_position = (board >> bit) & 1
            bits.append(bit_in_position)

        return bits



"""
Contains Player class
"""

class Player:
    """Class containing all functionality for a human player"""

    def __init__(self, player_num = 1):
        """Initializes a player

        Args:
            player_num (int, optional): Player ID number. Defaults to 1.
        """
        self.player_num = player_num
    
    def __str__(self, ):
        """Formats self for standard printing and string manipulation"""
        return f'Player {self.player_num}'
   
    

"""
Contains Computer class
"""

class Computer(Player):
    """Type of player controlled by an algorithm instead of a human.
    
    Attributes:
        DEBUG (bool): True = verbose logging and timing.
    """
    
    DEBUG: bool = False
    
    def __init__(self, player_num = 2, computer_level = 0):
        """Initializes the instance with optional parameters.

        Args:
            player_num (int, optional): Player ID number (1 or 2). Defaults to 2.
            computer_level (int, optional): Computer level (0-8 inclusive). Defaults to 0.
        """
        super().__init__(player_num)
        self.game: Game = None
        
        # Can be 0-8 (0 being easiest, 8 being impossible)
        # 7 and 8 seem to be very similar, maybe if computer went first?
        self.depth_limit = computer_level
        
        #! Debugging setup
        self.hit_max_depth = False
        self.max_depth = 0
        self.eval_time = 0
        self.total_searches = 0
        self.max_eval_time = 0
    
    def create_move(self, current_game: Game) -> int:
        """Generates move on current game specified.
        If computer_level = 0, the computer picks a random square to move.

        Args:
            current_game (Game): Game to generate a move on.

        Returns:
            int: Move bit, shifted to correct position and section of the bitboard.
        """
        self.game = current_game
        if self.DEBUG:
            start = timer()
        # A max depth of 0 causes some exceptionally poor moves
        # Making the computer pick at random in that case just to
        if self.depth_limit == 0:
            move = self.__create_random_move()
            if not self.game.is_move_valid(move):
                print('invalid computer move')
                self.create_move(self.game)
        else:
            move = self.find_best_move()
        if self.DEBUG:
            end = timer()
            #! Debugging and timing information
            print('\nCOMPUTER DEBUGGING!')
            print(f'Time to find best move: {(end-start) * 1000:.4f}ms')
            print(f'Time spent evaluating: {self.eval_time * 1000:.4f}ms')
            print(f'Percent of time taken by evaluating: {(self.eval_time/(end-start))*100:.2f}%')
            print(f'Reached a depth of: {self.max_depth}')
            print(f'Hit max depth? {self.hit_max_depth}')
            print(f'Total searches: {self.total_searches}')
            print(f'Max eval time: {self.max_eval_time * 1000:.4f}ms')
            print()
            self.eval_time = 0
            self.total_searches = 0
        
        return move
    
    def evaluate(self, board: int) -> int:
        """Evaluate player advantage in a bitboard.

        Args:
            board (int): Bitboard to evaluate.

        Returns:
            int: Evaluated score from ideal computer's view.
                    10  = computer win\n
                    -10 = computer loss\n
                    0   = no win or loss
        """

        if self.DEBUG:
            start = timer()
        winner = self.game.check_for_win(board)
        if self.DEBUG:
            end = timer()
            self.max_eval_time = max(end-start, self.max_eval_time)
        # Check if we won
        if winner == self.player_num:
            return 10
        # Check if tie or no win
        elif (winner == 0b11) or (winner == 0b00):
            return 0
        # Only other option is we lost
        else:
            return -10
    
    def find_best_move(self) -> int:
        """Finds best move in instance's specified game.

        Returns:
            int: Best move found, shifted to correct position and section of the bitboard.
        """
        # TODO: Should probably clean this substantially
        best_move = 0
        best_score = -1000
        board = self.game._board_state
        moves = self.__get_available_moves(board)
        shift = self.game.board_shift * (self.player_num - 1)
        
        # Iterates through the possible moves and calls
        # __minimax() to find the score of said move
        for i in range(9):
            # If move is available on both boards
            if (moves >> i) & 1:
                guess_move = (1 << i) << shift
                
                # Checks if move blocked other player win
                # deals with depth limits by incentivising
                # moves that prevent other player from winning
                score_blocked = self.__did_move_block(board, guess_move)
                
                # Makes the move on a copied board
                board += guess_move
                
                score_minimax = self.__minimax(board, 0, False)
                
                # Undoes the move
                board -= guess_move
                
                score = max(score_blocked, score_minimax)
                if score > best_score:
                    best_score = score
                    best_move = guess_move
        
        return best_move
        
    def __minimax(self, board: int, depth: int, is_max: bool) -> int:
        """Recusively finds the next best move for both players.
        Depth is limited by depth_limit which somewhat simulates computer levels.

        Args:
            board (int): Bitboard to check.
            depth (int): Current depth.
            is_max (bool): Is maximizing(computer) player?

        Returns:
            int: Evaluation of checked tree branch.
                    10  = computer win\n
                    -10 = computer loss\n
                    0   = no win or loss
        """
        if self.DEBUG:
            self.total_searches += 1
            self.max_depth = max(depth, self.max_depth)
        moves = self.__get_available_moves(board)
        
        # Limits depth to simulate computer levels
        if depth > self.depth_limit:
            self.hit_max_depth = True
            # Returning -10 to not incentivise games that
            # the computer doesn't know the outcome of
            return -10

        start = timer()
        result = self.evaluate(board)
        end = timer()
        self.eval_time += end-start
        
        # Returns score if either the player or computer wins
        if (result == 10) or (result == -10):
            return result
        
        # Checks if no moves are left, indicating a tie
        if moves == 0:
            return 0

        # If maximizer(computer)'s move
        if is_max:
            best_score = -1000
            
            # Iterates through the possible moves and calls
            # __minimax() to find the score of said move
            for i in range(9):
                # If move is available
                if (moves >> i) & 1:
                    guess_move = (1 << i) << self.game.board_shift
                    # Makes the move
                    board += guess_move
                    score = self.__minimax(board, depth + 1, False)
                    # Undoes the move
                    board -= guess_move
                    best_score = max(score, best_score)
                    
            return best_score
        else:
            best_score = 1000
            
            # Iterates through the possible moves and calls
            # __minimax() to find the score of said move
            for i in range(9):
                # If move is available
                if (moves >> i) & 1:
                    guess_move = (1 << i)
                    # Makes the move
                    board += guess_move
                    score = self.__minimax(board, depth + 1, True)
                    # Undoes the move
                    board -= guess_move
                    best_score = min(score, best_score)
            return best_score
            
                
    def __get_available_moves(self, board: int) -> int:
        """Gets available moves.
        Does not evaluate each move, only shows what moves are available.

        Args:
            board (int): Board to find moves in.

        Returns:
            int: Bits of possible moves, looks like combined player bitboard.
        """
        combined_boards = self.game.get_boards(board)
        moves = (~(combined_boards)) & self.game.board_one_mask
        
        return moves
    
    def __create_random_move(self) -> int:
        """Generates a random move.
        Does not check move validity.

        Returns:
            int: Randomly generated move.
        """
        shift = self.game.board_shift * (self.player_num - 1)
        move_rand = 1 << random.randint(0, 8)
        return move_rand << shift
    
    def __did_move_block(self, board: int, move: int) -> int:
        """Checks if move prevents other player from winning.
        Allows for computer to slightly incentivize blocking moves
        when it reaches a depth limit instead of blindly picking a move.

        Args:
            board (int): Bitboard to check.
            move (int): Move to simulate.

        Returns:
            int: Evaluation of position after move.
                    5 = move does block a win\n
                    -20 = move did not block a win
        """
        # Creates hypothetical board
        if self.player_num == 1:
            alt_board = board + (move << self.game.board_shift)
        else:
            alt_board = board + (move >> self.game.board_shift)
        
        # Checks if other player won
        if self.evaluate(alt_board) == -10:
            return 5
        
        # Chose -20 to hopefully prevent interference with other evals
        return -20



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
