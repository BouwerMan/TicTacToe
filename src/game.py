"""
Contains Game class
"""
from timeit import default_timer as timer

# My modules
from player import Player


class Game:
    """
    Contains all information on board state

    BitBoard format:
        bit 0-2: row 1
        bit 3-5: row 2
        bit 5-8: row 3
    """

    DEFAULT_BOARD_STR = [['a1','a2','a3'],['b1','b2','b3'],['c1','c2','c3']]
    DEFAULT_BOARD_BITS = 0b000000000
    ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
    BOARD_ROWS = 3
    BOARD_COLUMNS = 3

    def __init__(self, player_one: Player, player_two: Player):
        self.reset_board()
        #self.board = [self.board_one, self.board_two]
        
        self.player_one_old = player_one
        self.player_two_old = player_two
        #? IDK bout this thing
        self.players = [player_one, player_two]
        self.board = [self.board_one, self.board_two]
        
        # TODO: This guy needed?
        self.boards = self.board_one | self.board_two
        
        #! New 32-bit implementation of bitboards below:
        
        # Default board state, bit details under mask section
        # Bit 17 just separates board_one and board_two, always 1
        self.board_state = 0b10000000000000001000000000000000

        # Masks for state manipulation
        # 1st bit is game state, 1=no winner, 0=winner/tie
        self.game_state =       0b10000000000000000000000000000000
        # 2nd and 3rd bit is who won, 10 = player 1, 01 = player two, 00 = tie
        self.player_one =       0b01000000000000000000000000000000
        self.player_two =       0b00100000000000000000000000000000
        # Bits 24-32 represent board one (X), first 3 bits of that number is the top row
        #                                    second 3 bits is the middle row
        #                                    last 3 bits is the bottom row
        self.board_one_mask =   0b00000000000000000000000111111111
        # Bits 8-16 represent board two (O), bit order same as board one
        self.board_two_mask =   0b00000001111111110000000000000000
        
        
        # Bit length of each board (even though only 9 are used)
        self.board_bitlen = 16
        
    # Public Methods

    def parse_input(self, move: str, player_num : int = 0) -> bytes:
        """
        Parses user input (EX: 'a1') and converts it to a binary representation.

        Args:
            move (str): Move input by player.
            player_num (int): Player number, 0 = player one, 1 = player two

        Returns:
            bytes: Binary representation of move (0b001000000)
        """
        # TODO: redo parse input to return a move in the correct board in the boardstate
        # TODO: check for bad inputs
        #! breaks if string is wrong length or if both are letters
        move_list = [0,int(move[1])]
        move_list[0] = self.ALPHABET.index(list(move)[0])
        
        # Shifts a one to the proper column position
        # abs() so that we don't get a negative shift
        column = 1 << abs(move_list[1] - 3)
        # Shifts the one to the proper row position
        out = column << abs((3*(move_list[0]-2)))
        
        # Shifts out to the correct board
        return (out << (self.board_bitlen * player_num))
    
    def move(self, move: bytes) -> int:
        # TODO: Better status codes?
        # Returns -1 if move is not valid.
        if not self.is_move_valid(move):
            return -1
        
        # Checks if the move is 
        
        
        
        # Player 0 is player_one or the X player, therefore the relevant bits are 8-16
        #if player.player_num == 0:
        #    # TODO: redo parse input to return a move in the correct board in the boardstate
        #    board = self.board_state & self.board_one_mask
        #    board += move
        #    self.board_state &= (board << self.board_bitlen)
        #    return 0
        
        #elif player.player_num == 1:
        #    self.board_two = self.board_two + move
        #    self.update_board()
        #    return 1
            
    
    def is_move_valid(self, move: bytes = 0b0) -> bool:
        """
        Checks if move is valid for current board state.

        Args:
            move (bytes): Move made. Defaults to 0b0.

        Returns:
            bool: If move is valid or not.
        """
        # TODO: Need more checks?
        valid = False
        
        # Checks if the move is in either board
        if 0 == (move & (self.board_one_mask | self.board_two_mask)):
            return False
        
        # Have to shift board_one to the right to line up bits
        board_one = (self.game_state & self.board_one_mask) >> self.board_bitlen
        board_two = self.game_state & self.board_two_mask
        boards = board_one | board_two
        
        valid = not (move & boards)
        
        return valid
    
    def check_for_win(self, board = None) -> Player | None:
        # This version isnt much faster than old one, but is much cleaner
        # Sets default boards to current game state
        if board is None:
            board = [self.board[0], self.board[1]]
            
        test_conditions = [0b111, 0b111000, 0b111000000,
                           0b100100100, 0b010010010, 0b001001001,
                           0b100010001, 0b001010100]
        
        for i in range(len(board)):
            for j in range(len(test_conditions)):
                if (board[i] & test_conditions[j]) == test_conditions[j]:
                    return i
        
        return None
        
    def print_board(self):
        """
        Prints current board state in a human readable format.
        Assumes that the board is 3x3.
        """
        ## TODO: Convert to __str__?
        #? Make it not assume 3x3?
        board = self.__convert_from_bitboard()

        for i, row in enumerate(board):
            # Prints each row and pads the items to make things uniform
            print(f'{row[0]:^5}|{row[1]:^5}|{row[2]:^5}')
            # Prints a dividing line between lines but not after the last line
            if i < 2:
                print('-------------------')
    
    def update_board(self):
        self.board = [self.board_one, self.board_two]
        self.boards = self.board_one | self.board_two
        return self.boards
    
    def reset_board(self):
        self.board_one = self.DEFAULT_BOARD_BITS
        self.board_two = self.DEFAULT_BOARD_BITS
    
    # Private Methods
    
    def __get_board(self, board_sel = 0,) -> bytes:
        board_mask = self.board_one_mask << (self.board_bitlen * abs(board_sel - 1))
        return self.board
    
    def __convert_from_bitboard(self) -> list[list[str]]:
        """
        Converts bitboard to nested array to make printing easier

        Returns:
            list[list[str]]: Nested array representation of the board state.
        """

        out = self.DEFAULT_BOARD_STR

        for i, row in enumerate(out):
            num_bits = 8
            row_length = 3
            # TODO: Abstract bits to array?
            # Returns an binary array of each player's moves on row i.
            player_one_bits = [(self.board_one >> bit) & 1 for bit in range(num_bits - (row_length*i), num_bits - row_length - (row_length*i), -1)]
            player_two_bits = [(self.board_two >> bit) & 1 for bit in range(num_bits - (row_length*i), num_bits - row_length - (row_length*i), -1)]

            # Adds player one char to row one where moves have been made
            for j, bit in enumerate(player_one_bits):
                if bit:
                    char = self.player_one_old.player_char
                    row[j] = char

            # Adds player two char to row one where moves have been made
            for j, bit in enumerate(player_two_bits):
                if bit:
                    char = self.player_two_old.player_char
                    row[j] = char
        return out

    def __get_binary_array(self, binary = 0x1FF, num_bits = 8, row_length = 3):
        # TODO: Abstract bits to array section of __convert_from_bitboard?
        raise NotImplementedError('__get_binary_array() is not implemented!')

        i = 0
        loop_range = range(num_bits - (row_length*i), num_bits - row_length - (row_length*i), -1)
        return -1


if __name__ == '__main__':
    #! Temporary test code
    player_one_test = Player('X', 0)
    player_two_test = Player('O', 1)
    board_test = Game(player_one_test, player_two_test)
