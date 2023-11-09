"""
Contains Board class
"""

class Board:
    """
    Contains all information on board state
    
    Board format:
    

    Returns:
        _type_: _description_
    """

    default_board_str = [['-','-','-'],['-','-','-'],['-','-','-']]
    
    def __init__(self):
        self.board_one = 0b0
        self.board_two = 0b0
        # TODO: make this better?
        self.player_one_char = 'X'
        self.player_two_char = 'O'

    def __convert_from_bitboard(self) -> list[list[str]]:
        """
        Converts bitboard to nested array to make printing easier

        Returns:
            list[list[str]]: Nested array representation of the board state
        """
        
        out = self.default_board_str
        print(bin(self.board_one), bin(self.board_two))
        for i, row in enumerate(out):
            #? num_bits = 3
            #TODO: Understand and hopefully reverse order
            #player_one_bits = [] 
            #[print(d) for d in bin(self.board_one)[(i-2):(i+3)]]
            num_bits = 8
            player_one_bits = [(self.board_one >> bit) & 1 for bit in range(num_bits - (3*i), num_bits - 3 - (3*i), -1)]
            player_two_bits = [(self.board_two >> bit) & 1 for bit in range(num_bits - (3*i), num_bits - 3 - (3*i), -1)]
            
            
            #[print(i) for i in range(num_bits - (3*i), num_bits - 3 - (3*i), -1)]
            print(player_one_bits)
            #print(player_two_bits)
            # Adds player one char to row one where moves have been made
            
            for j, bit in enumerate(player_one_bits):
                if bit:
                    char = self.player_one_char
                    out[i][j] = char
            
            # Adds player two char to row one where moves have been made
            for j, bit in enumerate(player_two_bits):
                if bit:
                    char = self.player_two_char
                    out[i][j] = char
            
        print(out)
        print(bin(self.xor(self.board_one, self.board_two)))
        
        #boardList = [
        #    [str(RowOne)],
        #    [''],
        #    ['']
        #]
        return [['']]
    def xor(self, a, b):
        return (a and not b) or (not a and b)

    def print_board(self):
        #Board parsing from bitboard
        self.__convert_from_bitboard()
        pass
    
#! Temporary test code
board = Board()
board.board_one = 0b111001101
board.board_two = 0b000010010

board.print_board()