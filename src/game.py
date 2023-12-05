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
