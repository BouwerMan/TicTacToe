class Board:
    """
    Contains all information on board state

    ...

    Attributes
    -------
    boardOne: int
        Binary representation of playerOne's moves. Contains 1's where a move was played and 0's where no move from playerOne was played
        First 3 bits: Top row
        Second 3 bits: Middle row
        Last 3 bits: Bottom row 


    boardTwo: int
    """

    boardOne = 0b0
    boardTwo = 0b0

    def __init__(self):
        pass

    def __convertFromBitBoard(self) -> list[list[str]]:
        """
        Converts bit board to nested array to make printing easier

        ...

        Returns
        -------
        list: list[list[str]]
        """
        numBits = 3
        [print(i) for i in range(numBits - 1, -1, -1)]
        rowOneBits = [bin((self.boardOne >> bit) & 1) for bit in range(numBits - 1, -1, -1)]
        print(rowOneBits)

        #boardList = [
        #    [str(RowOne)],
        #    [''],
        #    ['']
        #]
        return [['']]

    def printBoard(self):
        #Board parsing from bitboard
        self.__convertFromBitBoard()
        pass