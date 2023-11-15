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
        
        self.player_one = player_one
        self.player_two = player_two
        #? IDK bout this thing
        self.players = [player_one, player_two]
        self.board = [self.board_one, self.board_two]
        
        # TODO: This guy needed?
        self.boards = self.board_one | self.board_two

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
                self.update_board()
                return self.board_one
            
            elif player.player_num == 1:
                self.board_two = self.board_two + move
                self.update_board()
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
        # TODO: Swap to using self.boards
        #? Something with the player?
        
        valid = False
        valid_one = not (move & self.board_one)
        valid_two = not (move & self.board_two)
        valid = valid_one & valid_two
        
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
    board_test = Game(player_one_test, player_two_test)
    #board_test.board_one = 0b110110001
    board_test.move(player_one_test, board_test.parse_input('a2'))
    board_test.move(player_one_test, board_test.parse_input('b2'))
    board_test.move(player_one_test, board_test.parse_input('c2'))
    print(board_test.check_for_win())
    board_test.print_board()
