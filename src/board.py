"""
Contains Board class
"""

# My modules
from player import Player


class Board:
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
        
        self.player_one = player_one
        self.player_two = player_two
        self.players = [player_one, player_two]

    # Public Methods

    def parse_input(self, move: str) -> bytes:
        """
        Parses user input (EX: 'a1') and converts it to a binary representation.

        Args:
            move (str): Move input by player.

        Returns:
            bytes: Binary representation of move (0b001000000)
        """
        # TODO: check for bad inputs
        #! breaks if string is wrong length or if both are letters
        move_list = [0,int(move[1])]
        move_list[0] = self.ALPHABET.index(list(move)[0])
        
        # Shifts a one to the proper column position
        # abs() so that we don't get a negative shift
        column = 1 << abs(move_list[1] - 3)
        # Shifts the one to the proper row position
        out = column << abs((3*(move_list[0]-2)))
        
        return out
    
    def move(self, player: Player , move:bytes):

        # TODO: Better status codes?
        
        if self.is_move_valid(move, player):
            # TODO: Better way to select board?
            if player.player_num == 0:
                self.board_one = self.board_one + move
                return self.board_one
            
            elif player.player_num == 1:
                self.board_two = self.board_two + move
                return self.board_two
            
        else:
            return -1
            
    
    def is_move_valid(self, move = 0x1FF, player = -1) -> bool:
        """
        Checks if move is valid for current board state.

        Args:
            move (binary): Move made. Defaults to 0x1FF.
            player (Player, optional): Player making the move. Defaults to -1. NEEDED?

        Returns:
            bool: If move is valid or not.
        """
        
        # TODO: Need more checks?
        #? Something with the player?
        
        valid = False
        valid_one = not (move & self.board_one)
        valid_two = not (move & self.board_two)
        valid = valid_one & valid_two
        
        return valid
    
    def check_for_win(self, player = None) -> Player | None:
        test = 0b0
        row_condition = 0b111
        col_condition = 0b100100100
        diag_condition_lr = 0b100010001
        diag_condition_rl = 0b001010100
        
        # Checking row win conditions
        for row in range(self.BOARD_ROWS):
            test = row_condition & (self.board_one >> (self.BOARD_ROWS * row))
            if test == row_condition:
                print(f'Row {row + 1} win')
                return self.player_one

        # Checking column win conditions
        for col in range(self.BOARD_COLUMNS):
            condition = col_condition >> col
            test = self.board_one & condition
            if test == condition:
                print(f'Column {col + 1} win')
                return self.player_one
        
        # Checking for diagonal win conditions
        if (self.board_one & diag_condition_lr) == diag_condition_lr:
            print('Diagonal win, top left to bottom right')
            return self.player_one
        elif (self.board_one & diag_condition_rl) == diag_condition_rl:
            print('Diagonal win, top right to bottom left')
            return self.player_one
        
        # TODO: Literally any better way to check both players
        
        # Checking row win conditions
        for row in range(self.BOARD_ROWS):
            test = row_condition & (self.board_two >> (self.BOARD_ROWS * row))
            if test == row_condition:
                print(f'Row {row + 1} win')
                return self.player_two

        # Checking column win conditions
        for col in range(self.BOARD_COLUMNS):
            condition = col_condition >> col
            test = self.board_two & condition
            if test == condition:
                print(f'Column {col + 1} win')
                return self.player_two
        
        # Checking for diagonal win conditions
        if (self.board_two & diag_condition_lr) == diag_condition_lr:
            print('Diagonal win, top left to bottom right')
            return self.player_two
        elif (self.board_two & diag_condition_rl) == diag_condition_rl:
            print('Diagonal win, top right to bottom left')
            return self.player_two
        
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
    
    def reset_board(self):
        self.board_one = self.DEFAULT_BOARD_BITS
        self.board_two = self.DEFAULT_BOARD_BITS
    
    # Private Methods
    
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
            # Returns an binary array of each player's move on row i.
            player_one_bits = [(self.board_one >> bit) & 1 for bit in range(num_bits - (row_length*i), num_bits - row_length - (row_length*i), -1)]
            player_two_bits = [(self.board_two >> bit) & 1 for bit in range(num_bits - (row_length*i), num_bits - row_length - (row_length*i), -1)]

            # Adds player one char to row one where moves have been made
            for j, bit in enumerate(player_one_bits):
                if bit:
                    char = self.player_one.player_char
                    row[j] = char

            # Adds player two char to row one where moves have been made
            for j, bit in enumerate(player_two_bits):
                if bit:
                    char = self.player_two.player_char
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
    board_test = Board(player_one_test, player_two_test)
    #board_test.board_one = 0b110110001
    board_test.move(player_one_test, board_test.parse_input('a2'))
    board_test.move(player_one_test, board_test.parse_input('b2'))
    board_test.move(player_one_test, board_test.parse_input('c2'))
    print(board_test.check_for_win())
    board_test.print_board()
