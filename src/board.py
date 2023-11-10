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
    ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

    def __init__(self, player_one: Player, player_two: Player):
        self.board_one = 0b000000000
        self.board_two = 0b000000000
        #self.board = [self.board_one, self.board_two]
        
        self.player_one = player_one
        self.player_two = player_two

    # Public Methods

    def parse_input(self, move: str) -> bytes:
        # TODO: check for bad inputs
        move_list = list(move)
        print(move_list)
        
        print(self.ALPHABET.index(move_list[0]))
    
    def move(self, player: Player , move:bytes) -> bytes:

        if self.is_move_valid(move, player):
            # TODO: Better way to select board?
            if player.player_num == 0:
                self.board_one = self.board_one + move
                return self.board_one
            
            elif player.player_num == 1:
                self.board_two = self.board_two + move
                return self.board_two
            
        else:
            print('Invalid move.')
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
    
    def print_board(self):
        """
        Prints current board state in a human readable format.
        Assumes that the board is 3x3.
        """
        #? Make it not assume 3x3?
        board = self.__convert_from_bitboard()

        for i, row in enumerate(board):
            # Prints each row and pads the items to make things uniform
            print(f'{row[0]:^5}|{row[1]:^5}|{row[2]:^5}')
            # Prints a dividing line between lines but not after the last line
            if i < 2:
                print('-------------------')
    
    def reset_board(self):
        self.board_one = 0b000000000
        self.board_two = 0b000000000
    
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
        print('ERROR: __get_binary_array() is not implemented!')
        raise NotImplementedError

        i = 0
        loop_range = range(num_bits - (row_length*i), num_bits - row_length - (row_length*i), -1)
        return -1


if __name__ == '__main__':
    #! Temporary test code
    player_one_test = Player('X', 0)
    player_two_test = Player('O', 1)
    board_test = Board(player_one_test, player_two_test)
    board_test.parse_input('a1')

    board_test.print_board()
